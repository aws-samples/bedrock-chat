"""
Callback handler for Strands integration.
"""

import logging
from typing import Callable

from strands.types.content import Message

logger = logging.getLogger(__name__)


class CallbackHandler:
    """Class-based callback handler to maintain state."""

    def __init__(
        self,
        on_stream: Callable[[str], None] | None = None,
        on_reasoning: Callable[[str], None] | None = None,
        on_message: Callable[[Message], None] | None = None,
    ):
        self.on_stream = on_stream
        self.on_reasoning = on_reasoning
        self.on_message = on_message
        self.collected_messages: list[Message] = []

    def __call__(self, **kwargs):
        """Make the instance callable like a function."""
        logger.debug(
            f"[STRANDS_CALLBACK] Callback triggered with keys: {list(kwargs.keys())}"
        )
        if "data" in kwargs and self.on_stream:
            data = kwargs["data"]
            self.on_stream(data)

        elif "reasoning" in kwargs and self.on_reasoning:
            reasoning_text = kwargs.get("reasoningText", "")
            self.on_reasoning(reasoning_text)

        elif "message" in kwargs and self.on_message:
            message: Message = kwargs["message"]
            self.on_message(message)


def create_callback_handler(
    on_stream: Callable[[str], None] | None = None,
    on_reasoning: Callable[[str], None] | None = None,
    on_message: Callable[[Message], None] | None = None,
) -> CallbackHandler:
    """Create a callback handler instance."""
    return CallbackHandler(
        on_stream=on_stream,
        on_reasoning=on_reasoning,
        on_message=on_message,
    )
