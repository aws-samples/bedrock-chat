"""
Context manager for Strands integration.
Provides access to bot and user context within Strands tools.
"""

import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Generator, Optional

from app.repositories.models.custom_bot import BotModel
from app.user import User

logger = logging.getLogger(__name__)

# Context variables for storing current execution context
_current_bot: ContextVar[Optional[BotModel]] = ContextVar('current_bot', default=None)
_current_user: ContextVar[Optional[User]] = ContextVar('current_user', default=None)


def _set_current_context(bot: Optional[BotModel], user: User):
    """Set the current bot and user context for tool execution."""
    logger.debug(f"[STRANDS_CONTEXT] Setting context - bot: {bot.id if bot else None}, user: {user.id}")
    _current_bot.set(bot)
    _current_user.set(user)


def get_current_bot() -> Optional[BotModel]:
    """Get the current bot context."""
    bot = _current_bot.get()
    if bot is None:
        logger.warning("[STRANDS_CONTEXT] No bot context available - ensure set_current_context was called")
    else:
        logger.debug(f"[STRANDS_CONTEXT] Getting current bot: {bot.id}")
    return bot


def get_current_user() -> Optional[User]:
    """Get the current user context."""
    user = _current_user.get()
    if user is None:
        logger.warning("[STRANDS_CONTEXT] No user context available - ensure set_current_context was called")
    else:
        logger.debug(f"[STRANDS_CONTEXT] Getting current user: {user.id}")
    return user


def _clear_current_context():
    """Clear the current context."""
    logger.debug("[STRANDS_CONTEXT] Clearing context")
    _current_bot.set(None)
    _current_user.set(None)


@contextmanager
def strands_context(bot: Optional[BotModel], user: User) -> Generator[None, None, None]:
    """
    Context manager for automatic Strands context management.
    
    Usage:
        with strands_context(bot, user):
            # Context is automatically set and cleared
            result = some_strands_tool()
    
    Args:
        bot: Optional bot configuration
        user: User making the request
    """
    logger.debug(f"[STRANDS_CONTEXT] Entering context manager - bot: {bot.id if bot else None}, user: {user.id}")
    _set_current_context(bot, user)
    try:
        yield
    finally:
        logger.debug("[STRANDS_CONTEXT] Exiting context manager - clearing context")
        _clear_current_context()


