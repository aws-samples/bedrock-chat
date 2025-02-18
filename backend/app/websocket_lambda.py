# websocket_lambda.py
import json
import logging
import os
from threading import Thread

from app.auth import verify_token
from app.websocket_handler import WebSocketHandler, NotificationSender, DynamoDBMessageStore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LambdaNotificationSender(NotificationSender):
    """Lambda-specific notification sender implementation"""
    def __init__(self, endpoint_url: str, connection_id: str) -> None:
        super().__init__()
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
                    gatewayapi.post_to_connection(
                        ConnectionId=self.connection_id,
                        Data=command["payload"],
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

def handler(event, context):
    """AWS Lambda handler for WebSocket connections"""
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
    
    notificator = LambdaNotificationSender(
        endpoint_url=endpoint_url,
        connection_id=connection_id,
    )

    # Start notification thread
    notification_thread = Thread(
        target=lambda: notificator.run(),
        daemon=True,
    )
    notification_thread.start()

    try:
        body = json.loads(event["body"])
        
        message_store = DynamoDBMessageStore(
            table_name=os.environ["WEBSOCKET_SESSION_TABLE_NAME"]
        )
        
        websocket_handler = WebSocketHandler(
            message_store=message_store,
            token_verifier=verify_token,
        )
        
        return websocket_handler.handle_message(
            connection_id=connection_id,
            message=body,
            notificator=notificator
        )
    finally:
        notificator.finish()
        notification_thread.join(timeout=60)