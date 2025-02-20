# websocket_handler.py
import json
import logging
from datetime import datetime
from decimal import Decimal as decimal
from queue import SimpleQueue
from typing import BinaryIO, Literal, Protocol, TypedDict, Any
from threading import Thread

import boto3
from boto3.dynamodb.conditions import Attr, Key
from app.routes.schemas.conversation import ChatInput
from app.agents.tools.agent_tool import ToolRunResult
from app.stream import OnStopInput, OnThinking
from app.repositories.conversation import RecordNotFoundError
from app.usecases.chat import chat

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WebSocketStatus:
    START = 'START'
    BODY = 'BODY' 
    STREAMING = 'STREAMING'
    STREAMING_END = 'STREAMING_END'
    AGENT_THINKING = 'AGENT_THINKING'
    AGENT_TOOL_RESULT = 'AGENT_TOOL_RESULT'
    AGENT_RELATED_DOCUMENT = 'AGENT_RELATED_DOCUMENT'
    ERROR = 'ERROR'
    END = 'END'
    # Additional statuses for responses
    CONNECTED = 'CONNECTED'
    SUCCESS = 'SUCCESS'


class _NotifyCommand(TypedDict):
    type: Literal["notify"]
    payload: bytes | BinaryIO

class _FinishCommand(TypedDict):
    type: Literal["finish"]

_Command = _NotifyCommand | _FinishCommand

class NotificationSender:
    """Base notification sender that implements common notification logic"""
    def __init__(self) -> None:
        self.commands = SimpleQueue[_Command]()

    def finish(self):
        """Signal the notification sender to finish"""
        self.commands.put({"type": "finish"})

    def notify(self, payload: bytes | BinaryIO):
        """Add a notification to the queue"""
        self.commands.put({
            "type": "notify",
            "payload": payload,
        })

    def run(self):
        """Start processing notifications - must be implemented by subclasses"""
        raise NotImplementedError()

    def on_stream(self, token: str):
        payload = json.dumps({
            "status": WebSocketStatus.STREAMING,
            "completion": token,
        }).encode("utf-8")
        self.notify(payload=payload)

    def on_stop(self, arg: OnStopInput):
        payload = json.dumps({
            "status": WebSocketStatus.STREAMING_END,
            "completion": "",
            "stop_reason": arg["stop_reason"],
        }).encode("utf-8")
        self.notify(payload=payload)

    def on_agent_thinking(self, tool_use: OnThinking):
        payload = json.dumps({
            "status": WebSocketStatus.AGENT_THINKING,
            "log": {
                tool_use["tool_use_id"]: {
                    "name": tool_use["name"],
                    "input": tool_use["input"],
                },
            },
        }).encode("utf-8")
        self.notify(payload=payload)

    def on_agent_tool_result(self, run_result: ToolRunResult):
        self.notify(
            payload=json.dumps({
                "status": WebSocketStatus.AGENT_TOOL_RESULT,
                "result": {
                    "toolUseId": run_result["tool_use_id"],
                    "status": run_result["status"],
                },
            }).encode("utf-8")
        )

        for related_document in run_result["related_documents"]:
            self.notify(
                payload=json.dumps({
                    "status": WebSocketStatus.AGENT_RELATED_DOCUMENT,
                    "result": {
                        "toolUseId": run_result["tool_use_id"],
                        "relatedDocument": related_document.to_schema().model_dump(
                            by_alias=True
                        ),
                    },
                }).encode("utf-8")
            )

def process_chat_input(user_id: str, chat_input: ChatInput, notificator: NotificationSender) -> dict:
    """Process chat input and send the message to the client."""
    logger.info(f"Received chat input: {chat_input}")
    
    try:
        chat(
            user_id=user_id,
            chat_input=chat_input,
            on_stream=lambda token: notificator.on_stream(token=token),
            on_stop=lambda arg: notificator.on_stop(arg=arg),
            on_thinking=lambda tool_use: notificator.on_agent_thinking(tool_use=tool_use),
            on_tool_result=lambda run_result: notificator.on_agent_tool_result(run_result=run_result),
        )
        return {"statusCode": 200, "body": "Message sent."}
    except RecordNotFoundError:
        if chat_input.bot_id:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "status": "ERROR",
                    "reason": f"bot {chat_input.bot_id} not found.",
                }),
            }
        return {
            "statusCode": 400,
            "body": json.dumps({
                "status": "ERROR",
                "reason": "Invalid request.",
            }),
        }
    except Exception as e:
        logger.exception(f"Failed to process chat: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "ERROR",
                "reason": f"Failed to process chat: {e}",
            }),
        }

class MessageStore(Protocol):
    """Protocol for message storage implementations"""
    def store_user_session(self, connection_id: str, user_id: str, expire: int) -> None: ...
    def store_message_part(self, connection_id: str, part_index: int, message_part: str, expire: int) -> None: ...
    def get_user_id(self, connection_id: str) -> str: ...
    def get_message_parts(self, connection_id: str) -> list[str]: ...

class DynamoDBMessageStore:
    """DynamoDB implementation of message storage"""
    def __init__(self, table_name: str):
        self.table = boto3.resource("dynamodb").Table(table_name)

    def store_user_session(self, connection_id: str, user_id: str, expire: int) -> None:
        self.table.put_item(
            Item={
                "ConnectionId": connection_id,
                "MessagePartId": decimal(0),
                "UserId": user_id,
                "expire": expire,
            }
        )

    def store_message_part(self, connection_id: str, part_index: int, message_part: str, expire: int) -> None:
        self.table.put_item(
            Item={
                "ConnectionId": connection_id,
                "MessagePartId": decimal(part_index + 1),  # Start from 1, 0 is reserved for session
                "MessagePart": message_part,
                "expire": expire,
            }
        )

    def get_user_id(self, connection_id: str) -> str:
        response = self.table.query(
            KeyConditionExpression=Key("ConnectionId").eq(connection_id),
            FilterExpression=Attr("UserId").exists(),
        )
        return response["Items"][0]["UserId"]

    def get_message_parts(self, connection_id: str) -> list[str]:
        message_parts = []
        last_evaluated_key = None

        while True:
            query_args = {
                "KeyConditionExpression": Key("ConnectionId").eq(connection_id) 
                & Key("MessagePartId").gte(1)
            }
            if last_evaluated_key:
                query_args["ExclusiveStartKey"] = last_evaluated_key
            
            response = self.table.query(**query_args)
            message_parts.extend(response["Items"])
            
            if "LastEvaluatedKey" not in response:
                break
            last_evaluated_key = response["LastEvaluatedKey"]

        message_parts.sort(key=lambda x: x["MessagePartId"])
        return [item["MessagePart"] for item in message_parts]

class WebSocketHandler:
    def __init__(self, message_store: MessageStore, token_verifier: Any) -> None:
        self.message_store = message_store
        self.verify_token = token_verifier

    def handle_message(self, connection_id: str, message: dict, notificator: NotificationSender) -> dict:
        """Handle incoming WebSocket message"""
        now = datetime.now()
        expire = int(now.timestamp()) + 60 * 2  # 2 minute expiry
        step = message.get("step")

        try:
            if step == "START":
                return self._handle_start(connection_id, message, expire)
            elif step == "END":
                return self._handle_end(connection_id, notificator)
            else:
                return self._handle_part(connection_id, message, expire)
        except Exception as e:
            logger.exception(f"Operation failed: {e}")
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "status": "ERROR",
                    "reason": str(e),
                }),
            }


    def _handle_start(self, connection_id: str, body: dict, expire: int) -> dict:
        try:
            logger.info("Attempting to verify token...")
            logger.debug(f"Token: {body['token'][:20]}...")
            decoded = self.verify_token(body["token"])
            user_id = decoded["sub"]
            logger.info(f"Token verified successfully for user_id: {user_id}")
            self.message_store.store_user_session(connection_id, user_id, expire)
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": WebSocketStatus.CONNECTED,
                    "message": "Session started."
                })
            }
        except Exception as e:
            logger.error(f"Invalid token: {e}")
            return {
                "statusCode": 403,
                "body": json.dumps({
                    "status": WebSocketStatus.ERROR,
                    "reason": "Invalid token."
                })
            }

    def _handle_end(self, connection_id: str, notificator: NotificationSender) -> dict:
        """Handle END message - process complete message"""
        user_id = self.message_store.get_user_id(connection_id)
        message_parts = self.message_store.get_message_parts(connection_id)
        full_message = "".join(message_parts)

        try:
            chat_input = ChatInput(**json.loads(full_message))
            return process_chat_input(
                user_id=user_id,
                chat_input=chat_input,
                notificator=notificator,
            )
        except Exception as e:
            logger.exception(f"Failed to process chat: {e}")
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "status": WebSocketStatus.ERROR,
                    "reason": f"Failed to process chat: {e}",
                }),
            }


    def _handle_part(self, connection_id: str, body: dict, expire: int) -> dict:
        """Handle message part"""
        try:
            part_index = body["index"]
            message_part = body["part"]
            self.message_store.store_message_part(connection_id, part_index, message_part, expire)
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": WebSocketStatus.SUCCESS,
                    "message": "Message part received."
                })
            }
        except Exception as e:
            logger.error(f"Failed to store message part: {e}")
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "status": WebSocketStatus.ERROR,
                    "reason": str(e)
                })
            }