"""
Reasoning span processor for Strands telemetry.
"""

import json
import logging
from typing import Any, Optional

from app.repositories.models.conversation import ReasoningContentModel
from opentelemetry.context import Context
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor

logger = logging.getLogger(__name__)


class ReasoningSpanProcessor(SpanProcessor):
    """Processes spans to extract reasoning content for DynamoDB storage."""

    def __init__(self) -> None:
        self.reasoning_data: list[ReasoningContentModel] = []
        self.conversation_id: str = ""
        self.user_id: str = ""

    def set_context(self, conversation_id: str, user_id: str) -> None:
        """Set conversation context for this processor."""
        self.conversation_id = conversation_id
        self.user_id = user_id

    def on_start(
        self, span: ReadableSpan, parent_context: Optional[Context] = None
    ) -> None:
        """Called when a span starts."""
        pass

    def on_end(self, span: ReadableSpan) -> None:
        """Called when a span ends - extract reasoning content."""
        if span.name == "execute_event_loop_cycle":
            logger.debug(f"Processing Cycle span: {span.name}")
            reasoning = self._extract_reasoning_from_span(span)
            if reasoning:
                self.reasoning_data.append(reasoning)
                logger.debug(f"Extracted reasoning content from span: {span.name}")
            else:
                logger.debug(f"No reasoning content found in span: {span.name}")

    def shutdown(self) -> None:
        """Called when the processor is shutdown."""
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Force flush any pending data."""
        return True

    def get_reasoning_data(self) -> list[ReasoningContentModel]:
        """Get extracted reasoning data."""
        return self.reasoning_data.copy()

    def _extract_reasoning_from_span(
        self, span: ReadableSpan
    ) -> Optional[ReasoningContentModel]:
        """
        Extract reasoning content from span events.

        Expected Data Structure:

        span.events contains gen_ai.choice events with the following structure:

        event.attributes["message"] = JSON string containing:
        [
            {
                "reasoningContent": {
                    "reasoningText": {
                        "text": "The user has provided what appears to be...",
                        "signature": "ErcBCkgIBxABGAIiQLG2dqOt..."
                    }
                }
            },
            {
                "text": "I'll calculate the result for you."
            },
            {
                "toolUse": {
                    "toolUseId": "tooluse_xxx",
                    "name": "calculator",
                    "input": {"expression": "5432/64526234"}
                }
            }
        ]
        """
        if not span.events:
            logger.debug("No events found in span")
            return None

        for event in span.events:
            if event.name == "gen_ai.choice":
                if event.attributes is None:
                    continue

                logger.debug(f"Found gen_ai.choice event: {event.attributes.keys()}")
                try:
                    message_attr = event.attributes.get("message")
                    if not isinstance(message_attr, str):
                        continue

                    message_content = json.loads(message_attr)
                    logger.debug(
                        f"Parsed message content: {len(message_content)} items"
                    )

                    for content_block in message_content:
                        if "reasoningContent" in content_block:
                            reasoning_data = content_block["reasoningContent"]
                            logger.debug(
                                f"Found reasoningContent: {reasoning_data.keys()}"
                            )

                            if "reasoningText" in reasoning_data:
                                reasoning_text_data = reasoning_data["reasoningText"]
                                text = reasoning_text_data.get("text", "")
                                signature = reasoning_text_data.get("signature", "")

                                if text:
                                    logger.debug(
                                        f"Extracted reasoning text: {len(text)} chars"
                                    )
                                    return ReasoningContentModel(
                                        content_type="reasoning",
                                        text=text,
                                        signature=signature,
                                        redacted_content=b"",
                                    )
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning(f"Failed to parse reasoning content from event: {e}")

        logger.debug("No reasoning content found in any events")
        return None
