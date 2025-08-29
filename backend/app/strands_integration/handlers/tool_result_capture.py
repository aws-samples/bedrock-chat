"""
Tool result capture handler for Strands integration.
"""

import logging
from typing import Callable

from app.agents.tools.agent_tool import ToolRunResult
from app.stream import OnThinking
from strands.experimental.hooks import (
    AfterToolInvocationEvent,
    BeforeToolInvocationEvent,
)
from strands.hooks import HookProvider, HookRegistry

from ..converters.tool_converter import (
    convert_after_tool_event_to_tool_run_result,
    convert_raw_tool_result_to_tool_result,
    convert_tool_run_result_to_strands_tool_result,
)

logger = logging.getLogger(__name__)


class ToolResultCapture(HookProvider):
    def __init__(
        self,
        on_thinking: Callable[[OnThinking], None] | None = None,
        on_tool_result: Callable[[ToolRunResult], None] | None = None,
    ):
        self.on_thinking = on_thinking
        self.on_tool_result = on_tool_result
        self.captured_tool_results: dict[str, ToolRunResult] = {}
        self.captured_tool_uses: dict[str, dict] = {}  # Store tool use info

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self.before_tool_execution)
        registry.add_callback(AfterToolInvocationEvent, self.after_tool_execution)

    def before_tool_execution(self, event: BeforeToolInvocationEvent) -> None:
        """Handler called before a tool is executed."""
        logger.debug("Before tool execution: %r", event)

        # Store tool use information
        tool_use = event.tool_use
        self.captured_tool_uses[tool_use["toolUseId"]] = {
            "name": tool_use["name"],
            "input": tool_use["input"],
        }

        if self.on_thinking:
            # Convert BeforeToolInvocationEvent to OnThinking format
            thinking_data: OnThinking = {
                "tool_use_id": tool_use["toolUseId"],
                "name": tool_use["name"],
                "input": tool_use["input"],
            }
            self.on_thinking(thinking_data)

    def after_tool_execution(self, event: AfterToolInvocationEvent) -> None:
        """Handler called after a tool is executed."""
        # Convert tool's raw result to proper ToolResult format before processing
        converted_result = convert_raw_tool_result_to_tool_result(event)
        event.result = converted_result  # type: ignore

        # Convert event to ToolRunResult using the new function
        tool_result = convert_after_tool_event_to_tool_run_result(event)

        # Store the result
        self.captured_tool_results[tool_result["tool_use_id"]] = tool_result

        # Call callback if provided
        if self.on_tool_result:
            self.on_tool_result(tool_result)

        # Convert ToolRunResult back to Strands ToolResult format with `source_id` for citation
        enhanced_result = convert_tool_run_result_to_strands_tool_result(tool_result)
        event.result = enhanced_result  # type: ignore
