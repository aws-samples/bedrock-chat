# websocket_local.py
import os
from queue import Empty
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState
import json
import logging
import asyncio
from datetime import datetime 
from typing import List, Optional

from app.auth import verify_token
from app.utils import is_running_on_lambda
from app.websocket_handler import WebSocketHandler, NotificationSender, MessageStore, WebSocketStatus

logger = logging.getLogger(__name__)

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')

class InMemoryMessageStore(MessageStore):
    """In-memory implementation of message storage for local development"""
    def __init__(self):
        self.sessions = {}
        self.messages = {}
        logger.info("InMemoryMessageStore initialized")
        
    def store_user_session(self, connection_id: str, user_id: str, expire: int) -> None:
        logger.info(f"Storing user session: {connection_id} -> {user_id}")
        self.sessions[connection_id] = {
            'user_id': user_id,
            'expire': expire,
            'created_at': datetime.now().timestamp()
        }
        logger.info(f"Session stored successfully. Current sessions: {self.sessions}")

    def store_message_part(self, connection_id: str, part_index: int, message_part: str, expire: int) -> None:
        if connection_id not in self.messages:
            self.messages[connection_id] = []
            logger.info(f"Created new message buffer for connection {connection_id}")
            
        while len(self.messages[connection_id]) <= part_index:
            self.messages[connection_id].append("")
            
        self.messages[connection_id][part_index] = message_part
        logger.info(f"Stored message part {part_index} for {connection_id}: {message_part[:50]}...")
        logger.info(f"Current message parts for {connection_id}: {self.messages[connection_id]}")

    def get_user_id(self, connection_id: str) -> str:
        session = self.sessions.get(connection_id)
        if not session:
            logger.error(f"No session found for connection {connection_id}")
            raise ValueError(f"No session found for connection {connection_id}")
            
        if session['expire'] < datetime.now().timestamp():
            logger.warning(f"Session expired for connection {connection_id}")
            del self.sessions[connection_id]
            raise ValueError(f"Session expired for connection {connection_id}")
            
        logger.info(f"Retrieved user_id {session['user_id']} for connection {connection_id}")
        return session['user_id']

    def get_message_parts(self, connection_id: str) -> list[str]:
        parts = self.messages.get(connection_id, [])
        if not parts:
            logger.warning(f"No message parts found for connection {connection_id}")
        else:
            logger.info(f"Retrieved {len(parts)} message parts for {connection_id}")
        return parts


class FastAPINotificationSender(NotificationSender):
    """FastAPI-specific notification sender implementation"""
    def __init__(self, websocket: WebSocket):
        super().__init__()
        self.websocket = websocket
        self._task: Optional[asyncio.Task] = None
        self._running = True
        logger.info("FastAPINotificationSender initialized")

    def run(self):
        """Start the notification sender"""
        logger.info("Starting FastAPI notification sender")
        if not self._task:
            loop = asyncio.get_event_loop()
            self._task = loop.create_task(self._process_notifications())

    async def wait(self):
        """Wait for all notifications to be processed"""
        try:
            if self._task:
                await self._task
        except Exception as e:
            logger.error(f"Error waiting for notification task: {e}", exc_info=True)

    def finish(self):
        """Signal the notification sender to finish"""
        logger.info("Signaling notification sender to finish")
        self._running = False
        super().finish()

    async def _process_notifications(self):
        """Process notifications in the queue"""
        logger.info("Starting notification processing loop")
        try:
            while self._running:
                try:
                    command = self.commands.get_nowait()
                    logger.info(f"Processing command: {command['type']}")

                    if command["type"] == "notify":
                        if not self._running:
                            break
                            
                        try:
                            if isinstance(command["payload"], bytes):
                                data = json.loads(command["payload"])
                                logger.info(f"Sending notification: {json.dumps(data)[:100]}...")
                            else:
                                data = json.loads(command["payload"].read())
                                logger.debug(f"Sending BinaryIO notification: {json.dumps(data)[:100]}...")

                            if self.websocket.client_state != WebSocketState.DISCONNECTED:
                                await self.websocket.send_json(data)
                            else:
                                logger.info("WebSocket disconnected, stopping notification sender")
                                break

                        except RuntimeError as e:
                            if "websocket.send" in str(e):
                                logger.info("WebSocket already closed, stopping notification sender")
                                break
                            raise
                        except Exception as e:
                            logger.error(f"Failed to send notification: {e}", exc_info=True)
                            
                    elif command["type"] == "finish":
                        logger.info("Received finish command")
                        break
                        
                except Empty:
                    await asyncio.sleep(0.1)
                    continue
                except Exception as e:
                    logger.error(f"Error processing notification: {e}", exc_info=True)
                    break
                    
        except Exception as e:
            logger.error(f"Error in notification processing loop: {e}", exc_info=True)
        finally:
            self._running = False
            logger.info("Notification processing loop ended")


async def local_websocket_endpoint(websocket: WebSocket):
    """FastAPI WebSocket endpoint for local development"""
    connection_id = None
    notificator = None
    websocket_closed = False
    
    try:
        await websocket.accept()
        logger.info("WebSocket connection accepted")
        
        # Use connection client host:port as connection_id
        connection_id = f"{websocket.client.host}:{websocket.client.port}"
        logger.info(f"Connection established with ID: {connection_id}")
        
        # Initialize message store and handler
        message_store = InMemoryMessageStore()
        websocket_handler = WebSocketHandler(
            message_store=message_store,
            token_verifier=verify_token,
        )
        
        while True:
            try:
                # Log waiting for message
                logger.info("Waiting for WebSocket message...")
                
                # Receive message with timeout
                message = await websocket.receive_text()
                logger.info(f"Received raw message: {message[:100]}...")
                
                data = json.loads(message)
                logger.info(f"Parsed message step: {data.get('step')}")
                
                # Create new notificator for each message
                if notificator:
                    logger.info("Cleaning up previous notificator")
                    notificator.finish()
                    await notificator.wait()
                
                logger.info("Creating new notificator")
                notificator = FastAPINotificationSender(websocket)

                # Start notification sender
                logger.info("Starting notification sender")
                notificator.run()
                
                # Process message
                logger.info(f"Processing message with step: {data.get('step')}")
                result = websocket_handler.handle_message(
                    connection_id=connection_id,
                    message=data,
                    notificator=notificator,
                )
                logger.info(f"Handler result status: {result.get('statusCode')}")
                
                # Wait for notification sender
                if data.get('step') == WebSocketStatus.END:
                    logger.info("Waiting for notification sender to complete")
                    await notificator.wait()
                    logger.debug("Notification sender completed")

                # Send result
                if not websocket_closed:
                    await websocket.send_json(json.loads(result["body"]))
                
            except WebSocketDisconnect:
                logger.warning(f"WebSocket disconnected while processing message")
                websocket_closed = True
                break
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON message: {e}")
                if not websocket_closed:
                    await websocket.send_json({
                        "status": "ERROR",
                        "reason": "Invalid message format"
                    })
            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)
                if not websocket_closed:
                    await websocket.send_json({
                        "status": "ERROR",
                        "reason": str(e)
                    })
                
    except WebSocketDisconnect:
        logger.warning(f"WebSocket disconnected: {connection_id}")
        websocket_closed = True
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
    finally:
        if notificator:
            logger.debug("Cleaning up notificator in finally block")
            try:
                notificator.finish()
                await notificator.wait()
            except Exception as e:
                logger.error(f"Error during notificator cleanup: {e}", exc_info=True)
        
        if not websocket_closed:
            try:
                await websocket.close()
            except Exception as e:
                logger.error(f"Error closing WebSocket: {e}", exc_info=True)


# Example of FastAPI route registration
def register_websocket_routes(app):
    """Register WebSocket routes if not running on Lambda"""
    if not is_running_on_lambda():
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=ALLOWED_ORIGINS,  # Your frontend dev server
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await local_websocket_endpoint(websocket)