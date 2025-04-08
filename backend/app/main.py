import logging
import os
import traceback
from typing import Callable

from app.dependencies import get_current_user
from app.repositories.common import (
    RecordAccessNotAllowedError,
    RecordNotFoundError,
    ResourceConflictError,
)
from app.routes.admin import router as admin_router
from app.routes.api_publication import router as api_publication_router
from app.routes.bot import router as bot_router
from app.routes.lti import router as lti_router
from app.routes.conversation import router as conversation_router
from app.routes.published_api import router as published_api_router
from app.routes.group import router as group_router
from app.routes.metadata import router as metadata_router
from app.routes.analytics import router as analytics_router
from app.user import User
from app.utils import is_running_on_lambda
from app.websocket_local import register_websocket_routes
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Message

CORS_ALLOW_ORIGINS = os.environ.get("CORS_ALLOW_ORIGINS", "*")
PUBLISHED_API_ID = os.environ.get("PUBLISHED_API_ID", None)

is_published_api = PUBLISHED_API_ID is not None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s:%(lineno)d  - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if not is_published_api:
    openapi_tags = [
        {"name": "conversation", "description": "Conversation API"},
        {"name": "bot", "description": "Bot API"},
        {"name": "api_publication", "description": "API Publication API"},
        {"name": "admin", "description": "Admin API"},
        {"name": "metadata", "description": "Metadata API"},
    ]
    title = "Bedrock Claude Chat"
else:
    openapi_tags = [{"name": "published_api", "description": "Published API"}]
    title = "Bedrock Claude Chat Published API"


app = FastAPI(
    openapi_tags=openapi_tags,
    title=title,
)


if not is_published_api:
    app.include_router(conversation_router)
    app.include_router(bot_router)
    app.include_router(lti_router)
    app.include_router(api_publication_router)
    app.include_router(admin_router)
    app.include_router(group_router)
    app.include_router(metadata_router)
    app.include_router(analytics_router)
else:
    app.include_router(published_api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def error_handler_factory(status_code: int) -> Callable[[Request, Exception], Response]:
    def error_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.error(exc)
        logger.error("".join(traceback.format_tb(exc.__traceback__)))
        return JSONResponse({"errors": [str(exc)]}, status_code=status_code)

    return error_handler  # type: ignore


app.add_exception_handler(RecordNotFoundError, error_handler_factory(404))
app.add_exception_handler(FileNotFoundError, error_handler_factory(404))
app.add_exception_handler(RecordAccessNotAllowedError, error_handler_factory(403))
app.add_exception_handler(ValueError, error_handler_factory(400))
app.add_exception_handler(TypeError, error_handler_factory(400))
app.add_exception_handler(AssertionError, error_handler_factory(400))
app.add_exception_handler(PermissionError, error_handler_factory(403))
app.add_exception_handler(ValidationError, error_handler_factory(422))
app.add_exception_handler(ResourceConflictError, error_handler_factory(409))
app.add_exception_handler(Exception, error_handler_factory(500))


@app.middleware("http")
def add_current_user_to_request(request: Request, call_next: ASGIApp):
    if is_running_on_lambda():
        if not is_published_api:
            authorization = request.headers.get("Authorization")
            if authorization:
                token_str = authorization.split(" ")[1]
                token = HTTPAuthorizationCredentials(
                    scheme="Bearer", credentials=token_str
                )
                request.state.current_user = get_current_user(token)
        else:
            request.state.current_user = User(
                id=f"PUBLISHED_API#{PUBLISHED_API_ID}",
                name=PUBLISHED_API_ID,  # type: ignore
                groups=[],
            )
    else:
        authorization = request.headers.get("Authorization")
        if authorization:
            token_str = authorization.split(" ")[1]
            token = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token_str)
            request.state.current_user = get_current_user(token)
        else:
            request.state.current_user = User(
                id="test_user", name="test_user", groups=[]
            )

    response = call_next(request)  # type: ignore
    return response


@app.middleware("http")
async def add_log_requests(request: Request, call_next: ASGIApp):
    logger.info(f"Request: {request.method} {request.url.path}")
    logger.debug(f"Request headers: {request.headers}")

    body = await request.body()
    logger.info(f"Request body: {body.decode('utf-8')[:100]}...")

    response = await call_next(request)  # type: ignore

    return response


# Register WebSocket routes when not running on Lambda
register_websocket_routes(app)