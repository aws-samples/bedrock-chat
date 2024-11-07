import json
import logging
import os
import traceback
from datetime import datetime
from decimal import Decimal as decimal

import boto3
from app.auth import verify_token
from app.bedrock import (
    ConverseApiToolResult,
)
from app.repositories.conversation import RecordNotFoundError
from app.routes.schemas.conversation import ChatInput
from app.stream import OnStopInput, OnThinking
from app.usecases.chat import (
    chat,
)
from boto3.dynamodb.conditions import Attr, Key

WEBSOCKET_SESSION_TABLE_NAME = os.environ["WEBSOCKET_SESSION_TABLE_NAME"]

dynamodb_client = boto3.resource("dynamodb")
table = dynamodb_client.Table(WEBSOCKET_SESSION_TABLE_NAME)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def on_stream(token: str, gatewayapi, connection_id: str):
    # Send completion
    gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(
            dict(
                status="STREAMING",
                completion=token,
            )
        ).encode("utf-8"),
    )


def on_fetching_knowledge(gatewayapi, connection_id: str):
    gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(
            dict(
                status="FETCHING_KNOWLEDGE",
            )
        ).encode("utf-8"),
    )


def on_stop(arg: OnStopInput, gatewayapi, connection_id: str):
    gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(
            dict(
                status="STREAMING_END",
                completion="",
                stop_reason=arg["stop_reason"],
            )
        ).encode("utf-8"),
    )


def on_agent_thinking(log: OnThinking, gatewayapi, connection_id: str):
    gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(
            dict(
                status="AGENT_THINKING",
                log={
                    log["tool_use_id"]: {
                        "name": log["name"],
                        "input": log["input"],
                    },
                },
            )
        ).encode("utf-8"),
    )


def on_agent_tool_result(
    tool_result: ConverseApiToolResult, gatewayapi, connection_id: str
):
    gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(
            dict(
                status="AGENT_TOOL_RESULT",
                result={
                    "toolUseId": tool_result["toolUseId"],
                    "status": tool_result["status"],
                    "content": tool_result["content"],
                },
            )
        ).encode("utf-8"),
    )


def process_chat_input(
    user_id: str, chat_input: ChatInput, gatewayapi, connection_id: str
) -> dict:
    """Process chat input and send the message to the client."""
    logger.info(f"Received chat input: {chat_input}")

    try:
        chat(
            user_id=user_id,
            chat_input=chat_input,
            on_stream=lambda token: on_stream(token, gatewayapi, connection_id),
            on_fetching_knowledge=lambda: on_fetching_knowledge(
                gatewayapi,
                connection_id,
            ),
            on_stop=lambda arg: on_stop(
                arg,
                gatewayapi,
                connection_id,
            ),
            on_thinking=lambda log: on_agent_thinking(log, gatewayapi, connection_id),
            on_tool_result=lambda result: on_agent_tool_result(
                result, gatewayapi, connection_id
            ),
        )

        return {"statusCode": 200, "body": "Message sent."}

    except RecordNotFoundError:
        if chat_input.bot_id:
            return {
                "statusCode": 404,
                "body": json.dumps(
                    dict(
                        status="ERROR",
                        reason=f"bot {chat_input.bot_id} not found.",
                    )
                ),
            }
        else:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    dict(
                        status="ERROR",
                        reason="Invalid request.",
                    )
                ),
            }

    except Exception as e:
        logger.error(f"Failed to run stream handler: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(
                dict(
                    status="ERROR",
                    reason=f"Failed to run stream handler: {e}",
                )
            ),
        }


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
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)

    now = datetime.now()
    expire = int(now.timestamp()) + 60 * 2  # 2 minute from now
    body = json.loads(event["body"])
    step = body.get("step")

    try:
        # API Gateway (websocket) has hard limit of 32KB per message, so if the message is larger than that,
        # need to concatenate chunks and send as a single full message.
        # To do that, we store the chunks in DynamoDB and when the message is complete, send it to SNS.
        # The life cycle of the message is as follows:
        # 1. Client sends `START` message to the WebSocket API.
        # 2. This handler receives the `Session started` message.
        # 3. Client sends message parts to the WebSocket API.
        # 4. This handler receives the message parts and appends them to the item in DynamoDB with index.
        # 5. Client sends `END` message to the WebSocket API.
        # 6. This handler receives the `END` message, concatenates the parts and sends the message to Bedrock.
        if step == "START":
            token = body["token"]
            try:
                # Verify JWT token
                decoded = verify_token(token)
            except Exception as e:
                logger.error(f"Invalid token: {e}")
                return {
                    "statusCode": 403,
                    "body": json.dumps(
                        dict(
                            status="ERROR",
                            reason="Invalid token.",
                        )
                    ),
                }

            user_id = decoded["sub"]

            # Store user id
            response = table.put_item(
                Item={
                    "ConnectionId": connection_id,
                    # Store as zero
                    "MessagePartId": decimal(0),
                    "UserId": user_id,
                    "expire": expire,
                }
            )
            return {"statusCode": 200, "body": "Session started."}
        elif step == "END":
            # Retrieve user id
            response = table.query(
                KeyConditionExpression=Key("ConnectionId").eq(connection_id),
                FilterExpression=Attr("UserId").exists(),
            )
            user_id = response["Items"][0]["UserId"]

            # Concatenate the message parts
            message_parts = []
            last_evaluated_key = None

            while True:
                if last_evaluated_key:
                    response = table.query(
                        KeyConditionExpression=Key("ConnectionId").eq(connection_id)
                        # Zero is reserved for user id, so start from 1
                        & Key("MessagePartId").gte(1),
                        ExclusiveStartKey=last_evaluated_key,
                    )
                else:
                    response = table.query(
                        KeyConditionExpression=Key("ConnectionId").eq(connection_id)
                        & Key("MessagePartId").gte(1),
                    )

                message_parts.extend(response["Items"])

                if "LastEvaluatedKey" in response:
                    last_evaluated_key = response["LastEvaluatedKey"]
                else:
                    break

            logger.info(f"Number of message chunks: {len(message_parts)}")
            message_parts.sort(key=lambda x: x["MessagePartId"])
            full_message = "".join(item["MessagePart"] for item in message_parts)

            # Process the concatenated full message
            chat_input = ChatInput(**json.loads(full_message))
            return process_chat_input(
                user_id=user_id,
                chat_input=chat_input,
                gatewayapi=gatewayapi,
                connection_id=connection_id,
            )
        else:
            # Store the message part of full message
            # Zero is reserved for user id, so start from 1
            part_index = body["index"] + 1
            message_part = body["part"]

            # Store the message part with its index
            table.put_item(
                Item={
                    "ConnectionId": connection_id,
                    "MessagePartId": decimal(part_index),
                    "MessagePart": message_part,
                    "expire": expire,
                }
            )
            return {"statusCode": 200, "body": "Message part received."}

    except Exception as e:
        logger.error(f"Operation failed: {e}")
        logger.error("".join(traceback.format_tb(e.__traceback__)))
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "status": "ERROR",
                    "reason": str(e),
                }
            ),
        }
