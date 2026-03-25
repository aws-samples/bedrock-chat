import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from queue import SimpleQueue
from threading import Thread
from typing import BinaryIO, Literal, TypedDict

import boto3
from app.agents.tools.agent_tool import ToolRunResult
from app.auth import verify_token
from app.repositories.conversation import RecordNotFoundError
from app.routes.schemas.conversation import ChatInput
from app.stream import OnStopInput, OnThinking
from app.usecases.chat import chat
from app.user import User

LARGE_PAYLOAD_SUPPORT_BUCKET = os.environ["LARGE_PAYLOAD_SUPPORT_BUCKET"]

s3_client = boto3.client("s3")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _chunk_prefix(connection_id: str) -> str:
    return f"ws-chunks/{connection_id}/"


def _session_key(connection_id: str) -> str:
    return f"{_chunk_prefix(connection_id)}session.json"


def _chunk_key(connection_id: str, index: int) -> str:
    # Zero-pad so lexicographic sort matches numeric order
    return f"{_chunk_prefix(connection_id)}{index:010d}"


class _NotifyCommand(TypedDict):
    type: Literal["notify"]
    payload: bytes | BinaryIO


class _FinishCommand(TypedDict):
    type: Literal["finish"]


_Command = _NotifyCommand | _FinishCommand


class NotificationSender:
    def __init__(self, endpoint_url: str, connection_id: str) -> None:
        self.commands = SimpleQueue[_Command]()
        self.endpoint_url = endpoint_url
        self.connection_id = connection_id

    def run(self):
        import boto3

        gatewayapi = boto3.client(
            "apigatewaymanagementapi",
            endpoint_url=self.endpoint_url,
        )

        while True:
            command = self.commands.get()
            if command["type"] == "notify":
                try:
                    logger.debug(
                        f"[WEBSOCKET_SEND] Sending to connection {self.connection_id}: {command['payload'][:200]}..."
                    )
                    gatewayapi.post_to_connection(
                        ConnectionId=self.connection_id,
                        Data=command["payload"],
                    )
                    logger.debug(
                        f"[WEBSOCKET_SEND] Successfully sent to connection {self.connection_id}"
                    )

                except (
                    gatewayapi.exceptions.GoneException,
                    gatewayapi.exceptions.ForbiddenException,
                ) as e:
                    logger.exception(
                        f"Shutdown the notification sender due to an exception: {e}"
                    )
                    break

                except Exception as e:
                    logger.exception(f"Failed to send notification: {e}")

            elif command["type"] == "finish":
                break

    def finish(self):
        self.commands.put(
            {
                "type": "finish",
            }
        )

    def notify(self, payload: bytes | BinaryIO):
        self.commands.put(
            {
                "type": "notify",
                "payload": payload,
            }
        )

    def on_stream(self, token: str):
        payload = json.dumps(
            dict(
                status="STREAMING",
                completion=token,
            )
        ).encode("utf-8")

        self.notify(payload=payload)

    def on_stop(self, arg: OnStopInput):
        logger.debug(f"[WEBSOCKET_ON_STOP] WebSocket on_stop called with: {arg}")
        payload = json.dumps(
            dict(
                status="STREAMING_END",
                completion="",
                stop_reason=arg["stop_reason"],
                token_count=dict(
                    input=arg["input_token_count"],
                    output=arg["output_token_count"],
                    cache_read_input=arg["cache_read_input_count"],
                    cache_write_input=arg["cache_write_input_count"],
                ),
                price=arg["price"],
            )
        ).encode("utf-8")

        self.notify(payload=payload)

    def on_agent_thinking(self, tool_use: OnThinking):
        payload = json.dumps(
            dict(
                status="AGENT_THINKING",
                log={
                    tool_use["tool_use_id"]: {
                        "name": tool_use["name"],
                        "input": tool_use["input"],
                    },
                },
            )
        ).encode("utf-8")

        self.notify(payload=payload)

    def on_agent_tool_result(self, run_result: ToolRunResult):
        self.notify(
            payload=json.dumps(
                dict(
                    status="AGENT_TOOL_RESULT",
                    result={
                        "toolUseId": run_result["tool_use_id"],
                        "status": run_result["status"],
                    },
                )
            ).encode("utf-8")
        )

        for related_document in run_result["related_documents"]:
            self.notify(
                payload=json.dumps(
                    dict(
                        status="AGENT_RELATED_DOCUMENT",
                        result={
                            "toolUseId": run_result["tool_use_id"],
                            "relatedDocument": related_document.to_schema().model_dump(
                                by_alias=True
                            ),
                        },
                    )
                ).encode("utf-8")
            )

    def on_reasoning(self, token: str):
        payload = json.dumps(
            dict(
                status="REASONING",
                completion=token,
            )
        ).encode("utf-8")
        self.notify(payload=payload)


def process_chat_input(
    user: User,
    chat_input: ChatInput,
    notificator: NotificationSender,
) -> dict:
    """Process chat input and send the message to the client."""
    logger.info(
        f"Processing chat input for conversation: {chat_input.conversation_id}, "
        f"model: {chat_input.message.model}"
    )

    try:
        chat(
            user=user,
            chat_input=chat_input,
            on_stream=lambda token: notificator.on_stream(
                token=token,
            ),
            on_stop=lambda arg: notificator.on_stop(arg=arg),
            on_thinking=lambda tool_use: notificator.on_agent_thinking(
                tool_use=tool_use,
            ),
            on_tool_result=lambda run_result: notificator.on_agent_tool_result(
                run_result=run_result
            ),
            on_reasoning=lambda token: notificator.on_reasoning(
                token=token,
            ),
        )

        return {"statusCode": 200, "body": "Message sent."}

    except RecordNotFoundError:
        reason = (
            f"bot {chat_input.bot_id} not found."
            if chat_input.bot_id
            else "Invalid request."
        )
        status_code = 404 if chat_input.bot_id else 400
        notificator.notify(
            json.dumps(dict(status="ERROR", reason=reason)).encode("utf-8")
        )
        return {"statusCode": status_code, "body": "Error."}

    except Exception as e:
        logger.exception(f"Failed to run stream handler: {e}")
        reason = f"Failed to run stream handler: {e}"
        # Send the error via post_to_connection so it reaches the client even
        # when the Lambda response is ignored after the API Gateway 29-second
        # integration timeout.
        notificator.notify(
            json.dumps(dict(status="ERROR", reason=reason)).encode("utf-8")
        )
        return {"statusCode": 500, "body": "Error."}


def _cleanup_s3_chunks(connection_id: str) -> None:
    """Delete all S3 objects for this connection. Best-effort; errors are logged only."""
    try:
        prefix = _chunk_prefix(connection_id)
        paginator = s3_client.get_paginator("list_objects_v2")
        objects_to_delete = []
        for page in paginator.paginate(Bucket=LARGE_PAYLOAD_SUPPORT_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []):
                objects_to_delete.append({"Key": obj["Key"]})
        if objects_to_delete:
            s3_client.delete_objects(
                Bucket=LARGE_PAYLOAD_SUPPORT_BUCKET,
                Delete={"Objects": objects_to_delete},
            )
            logger.info(f"Cleaned up {len(objects_to_delete)} S3 chunks for {connection_id}")
    except Exception as e:
        logger.warning(f"Failed to clean up S3 chunks for {connection_id}: {e}")


def handler(event, context):
    logger.info(f"Received event: {event}")
    route_key = event["requestContext"]["routeKey"]

    if route_key == "$connect":
        return {"statusCode": 200, "body": "Connected."}
    elif route_key == "$disconnect":
        return {"statusCode": 200, "body": "Disconnected."}

    connection_id = event["requestContext"]["connectionId"]
    domain_name = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    endpoint_url = f"https://{domain_name}/{stage}"
    notificator = NotificationSender(
        endpoint_url=endpoint_url,
        connection_id=connection_id,
    )

    body = json.loads(event["body"])
    step = body.get("step")
    token = body.get("token")

    notification_thread = Thread(
        target=lambda: notificator.run(),
        daemon=True,
    )
    notification_thread.start()
    try:
        # API Gateway (websocket) has a hard limit of 32KB per message, so if the message
        # is larger than that we chunk it client-side and reassemble here.
        # Life cycle:
        # 1. Client sends START  → Lambda stores session metadata in S3.
        # 2. Client sends BODY chunks  → Lambda stores each chunk as an S3 object.
        # 3. Client sends END  → Lambda reads + concatenates all chunks from S3,
        #                        calls Bedrock, streams response back.
        if step == "START":
            try:
                decoded = verify_token(token)
            except Exception as e:
                logger.exception(f"Invalid token: {e}")
                notificator.notify(
                    json.dumps(dict(status="ERROR", reason="Invalid token.")).encode("utf-8")
                )
                return {"statusCode": 200, "body": "Error."}

            user_id = decoded["sub"]

            s3_client.put_object(
                Bucket=LARGE_PAYLOAD_SUPPORT_BUCKET,
                Key=_session_key(connection_id),
                Body=json.dumps({"user_id": user_id}),
            )
            return {"statusCode": 200, "body": "Session started."}

        elif step == "END":
            decoded = verify_token(token)
            user = User.from_decoded_token(decoded)

            # Read session metadata
            session_obj = s3_client.get_object(
                Bucket=LARGE_PAYLOAD_SUPPORT_BUCKET,
                Key=_session_key(connection_id),
            )
            session_data = json.loads(session_obj["Body"].read())
            user_id = session_data["user_id"]  # noqa: F841 – kept for audit / future use

            # List all chunk objects (excludes session.json via prefix filtering)
            chunk_prefix = _chunk_prefix(connection_id)
            response = s3_client.list_objects_v2(
                Bucket=LARGE_PAYLOAD_SUPPORT_BUCKET,
                Prefix=chunk_prefix,
            )
            chunk_objects = sorted(
                [
                    obj
                    for obj in response.get("Contents", [])
                    if not obj["Key"].endswith("session.json")
                ],
                key=lambda obj: obj["Key"],
            )

            logger.info(f"Number of message chunks: {len(chunk_objects)}")

            # Read all chunks in parallel
            def _read_chunk(obj: dict) -> str:
                resp = s3_client.get_object(
                    Bucket=LARGE_PAYLOAD_SUPPORT_BUCKET, Key=obj["Key"]
                )
                return resp["Body"].read().decode("utf-8")

            with ThreadPoolExecutor(max_workers=max(1, min(len(chunk_objects), 20))) as executor:
                chunks = list(executor.map(_read_chunk, chunk_objects))

            full_message = "".join(chunks)

            # Clean up S3 objects before processing so they don't linger
            _cleanup_s3_chunks(connection_id)

            chat_input = ChatInput(**json.loads(full_message))
            return process_chat_input(
                user=user,
                chat_input=chat_input,
                notificator=notificator,
            )

        else:
            # BODY step — store this chunk as an S3 object
            part_index = body["index"]
            message_part = body["part"]

            s3_client.put_object(
                Bucket=LARGE_PAYLOAD_SUPPORT_BUCKET,
                Key=_chunk_key(connection_id, part_index),
                Body=message_part,
            )
            return {"statusCode": 200, "body": "Message part received."}

    except Exception as e:
        logger.exception(f"Operation failed: {e}")
        notificator.notify(
            json.dumps(dict(status="ERROR", reason=str(e))).encode("utf-8")
        )
        return {"statusCode": 200, "body": "Error."}

    finally:
        notificator.finish()
        notification_thread.join(timeout=60)
