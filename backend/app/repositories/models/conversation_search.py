from __future__ import annotations

import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SearchHighlightModel(BaseModel):
    """Model representing highlight information for search results"""

    field_name: str  # "Title" or "MessageMap"
    fragments: list[str]  # Text fragments containing the search term


class ConversationSearchModel(BaseModel):
    """Model representing conversation metadata with search results"""

    id: str
    title: str
    bot_id: str | None
    last_updated_time: float = Field(default=0.0)
    highlights: list[SearchHighlightModel] | None = None

