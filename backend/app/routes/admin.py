from datetime import date
import logging

from app.dependencies import check_is_user_authorized
from app.repositories.custom_bot import find_all_published_bots, find_public_bot_by_id
from app.routes.schemas.admin import (
    PublicBotOutput,
    PublishedBotOutput,
    PublishedBotOutputsWithNextToken,
)
from app.routes.schemas.bot import Knowledge
from app.user import User
from fastapi import APIRouter, Request

router = APIRouter(tags=["admin"])

logger = logging.getLogger(__name__)


@router.get("/admin/published-bots", response_model=PublishedBotOutputsWithNextToken)
def get_all_published_bots(
    request: Request,
    next_token: str | None = None,
    limit: int = 1000,
):
    """Get all published bots. This is intended to be used by admin."""
    current_user: User = request.state.current_user
    check_is_user_authorized("view_analytics", current_user)
    bots, next_token = find_all_published_bots(next_token=next_token, limit=limit)

    bot_outputs = [
        PublishedBotOutput(
            id=bot.id,
            title=bot.title,
            description=bot.description,
            published_stack_name=bot.published_api_stack_name,
            published_datetime=bot.published_api_datetime,
            owner_user_id=bot.owner_user_id,
        )
        for bot in bots
    ]

    return PublishedBotOutputsWithNextToken(bots=bot_outputs, next_token=next_token)


@router.get("/admin/bot/public/{bot_id}", response_model=PublicBotOutput)
def get_public_bot(
    request: Request, 
    bot_id: str,
    ):
    """Get public (shared) bot by id."""
    current_user: User = request.state.current_user
    check_is_user_authorized("view_analytics", current_user)

    bot = find_public_bot_by_id(bot_id)
    output = PublicBotOutput(
        id=bot.id,
        title=bot.title,
        instruction=bot.instruction,
        description=bot.description,
        create_time=bot.create_time,
        last_used_time=bot.last_used_time,
        owner_user_id=bot.owner_user_id,
        knowledge=Knowledge(
            source_urls=bot.knowledge.source_urls,
            sitemap_urls=bot.knowledge.sitemap_urls,
            filenames=bot.knowledge.filenames,
            s3_urls=bot.knowledge.s3_urls,
        ),
        sync_status=bot.sync_status,
        sync_status_reason=bot.sync_status_reason,
        sync_last_exec_id=bot.sync_last_exec_id,
    )
    return output
