"""
Callback handler for Strands integration.
"""

import logging
from typing import Callable

from app.agents.tools.agent_tool import ToolRunResult
from app.stream import OnThinking

logger = logging.getLogger(__name__)


class CallbackHandler:
    """Class-based callback handler to maintain state."""

    def __init__(
        self,
        on_stream: Callable[[str], None] | None = None,
        on_thinking: Callable[[OnThinking], None] | None = None,
        on_tool_result: Callable[[ToolRunResult], None] | None = None,
        on_reasoning: Callable[[str], None] | None = None,
    ):
        self.on_stream = on_stream
        self.on_thinking = on_thinking
        self.on_tool_result = on_tool_result
        self.on_reasoning = on_reasoning
        self.collected_reasoning: list[str] = []

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
            self.collected_reasoning.append(reasoning_text)
        elif "thinking" in kwargs and self.on_reasoning:
            thinking_text = kwargs.get("thinking", "")
            self.on_reasoning(thinking_text)
            self.collected_reasoning.append(thinking_text)
        # elif "event" in kwargs:
        #     event = kwargs["event"]
        #     print(f"[STRANDS_CALLBACK] Event: {event}")
        # elif "message" in kwargs:
        #     message = kwargs["message"]
        #     print(f"[STRANDS_CALLBACK] Message: {message}")


def create_callback_handler(
    on_stream: Callable[[str], None] | None = None,
    on_thinking: Callable[[OnThinking], None] | None = None,
    on_tool_result: Callable[[ToolRunResult], None] | None = None,
    on_reasoning: Callable[[str], None] | None = None,
) -> CallbackHandler:
    """Create a callback handler instance."""
    return CallbackHandler(on_stream, on_thinking, on_tool_result, on_reasoning)
