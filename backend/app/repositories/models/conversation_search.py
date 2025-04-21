from __future__ import annotations

import json
import logging
from typing import Self

from app.repositories.common import decompose_conv_id
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SearchHighlight(BaseModel):
    """Model representing highlight information for search results"""

    field_name: str  # "Title" or "MessageMap"
    fragments: list[str]  # Text fragments containing the search term


class ConversationSearchModel(BaseModel):
    """Model representing conversation metadata with search results"""

    id: str
    title: str
    model: str
    bot_id: str | None
    last_updated_time: float = Field(default=0.0)
    highlights: list[SearchHighlight] | None = None
    highlight_texts: list[str] | None = None

    @classmethod
    def from_opensearch_response(cls, hit: dict) -> Self:
        """Create a ConversationSearchModel instance from OpenSearch response"""
        DEFAULT_MODEL = "claude-v3.5-haiku"
        source = hit["_source"]

        # Extract conversation ID from SK (e.g. "{user_id}#CONV#{conversation_id}" -> "{conversation_id}")
        sk = source.get("SK", "")
        conversation_id = decompose_conv_id(sk)

        # Get model directly from extractedModel field
        model = source.get("extractedModel", DEFAULT_MODEL)

        # Get last updated time from source with fallback logic
        last_updated_time = 0.0

        # Try to get LastUpdateTime first
        if source.get("LastUpdateTime"):
            last_updated_time = float(source.get("LastUpdateTime"))
            logger.info(f"Found LastUpdateTime in source: {last_updated_time}")
        # If not found, try to get it from CreateTime or create_time as fallback
        elif source.get("CreateTime"):
            last_updated_time = float(source.get("CreateTime"))
        elif source.get("create_time"):
            last_updated_time = float(source.get("create_time"))

        # Create conversation meta instance
        conversation = cls(
            id=conversation_id,
            title=source.get("Title", "Untitled conversation"),
            model=model,
            bot_id=source.get("BotId"),
            last_updated_time=last_updated_time,
        )

        # Add highlight information if available
        if "highlight" in hit:
            highlights = []
            highlight_texts = []

            for field, fragments in hit["highlight"].items():
                if field == "extractedContent":
                    highlights.append(
                        SearchHighlight(field_name="MessageBody", fragments=fragments)
                    )
                    highlight_texts.extend(fragments)
                elif field == "Title":
                    highlights.append(
                        SearchHighlight(field_name=field, fragments=fragments)
                    )
                    highlight_texts.extend(fragments)
                elif field == "messages.value.content.body":
                    highlights.append(
                        SearchHighlight(field_name="MessageBody", fragments=fragments)
                    )
                    highlight_texts.extend(fragments)

            if highlights:
                conversation.highlights = highlights

            if highlight_texts:
                conversation.highlight_texts = highlight_texts

        return conversation
