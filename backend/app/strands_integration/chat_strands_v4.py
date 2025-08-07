import dataclasses
import json
import logging
from typing import Callable

from app.agents.tools.agent_tool import (
    AgentTool,
    ToolFunctionResult,
    ToolRunResult,
    _function_result_to_related_document,
)
from app.repositories.models.conversation import (
    ConversationModel,
    MessageModel,
    type_model_name,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import ChatInput
from app.stream import OnStopInput, OnThinking
from app.usecases.chat import prepare_conversation
from app.user import User
from strands import Agent
from strands.experimental.hooks import AfterToolInvocationEvent, BeforeToolInvocationEvent
from strands.hooks import (  # AfterInvocationEvent,; BeforeInvocationEvent,
    HookProvider,
    HookRegistry,
)
from strands.types.tools import ToolResult, ToolResultContent
from ulid import ULID

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _convert_tool_result_content_to_function_result(
    content_item: ToolResultContent,
) -> ToolFunctionResult:
    """Convert ToolResultContent to ToolFunctionResult format."""
    if "text" in content_item:
        return content_item["text"]
    elif "json" in content_item:
        return (
            content_item["json"]
            if isinstance(content_item["json"], dict)
            else {"data": content_item["json"]}
        )
    elif "document" in content_item:
        # Convert document to string
        doc_content = content_item["document"]
        if isinstance(doc_content, dict) and "source" in doc_content:
            # DocumentSource has bytes field according to Strands type definition
            doc_source = doc_content["source"]
            if isinstance(doc_source, dict) and "bytes" in doc_source:
                try:
                    # Try to decode bytes as UTF-8 text
                    return doc_source["bytes"].decode("utf-8")
                except (UnicodeDecodeError, AttributeError):
                    # If decoding fails, return a description
                    doc_name = doc_content.get("name", "document")
                    doc_format = doc_content.get("format", "unknown")
                    return f"[Document: {doc_name} ({doc_format})]"
            else:
                return str(doc_source)
        else:
            return str(doc_content)
    elif "image" in content_item:
        # Convert image to text description
        img_content = content_item["image"]
        if isinstance(img_content, dict):
            img_format = img_content.get("format", "unknown")
            return f"[Image content ({img_format})]"
        else:
            return "[Image content]"
    else:
        # Empty content
        return ""


def _convert_tool_run_result_to_strands_tool_result(
    tool_run_result: ToolRunResult,
) -> ToolResult:
    """Convert our ToolRunResult back to Strands ToolResult format with source_id included."""
    from app.repositories.models.conversation import (
        JsonToolResultModel,
        TextToolResultModel,
    )

    # Convert related documents back to ToolResultContent
    content_list = []
    for related_doc in tool_run_result["related_documents"]:
        content = related_doc.content
        source_id = related_doc.source_id

        # Always return as JSON with source_id included
        if isinstance(content, TextToolResultModel):
            # Convert text content to JSON with source_id
            original_content = {"text": content.text}
            enhanced_content = {**original_content, "source_id": source_id}
            tool_result_content: ToolResultContent = {"json": enhanced_content}
        elif isinstance(content, JsonToolResultModel):
            # Convert JSON content with source_id
            original_content = (
                content.json_
                if isinstance(content.json_, dict)
                else {"data": content.json_}
            )
            enhanced_content = {**original_content, "source_id": source_id}
            tool_result_content = {"json": enhanced_content}
        else:
            # Fallback to text converted to JSON with source_id
            original_content = {"text": str(content)}
            enhanced_content = {**original_content, "source_id": source_id}
            tool_result_content = {"json": enhanced_content}

        content_list.append(tool_result_content)

    # If no content, add empty JSON content with source_id
    if not content_list:
        content_list.append({"json": {"text": "", "source_id": "unknown"}})

    return ToolResult(
        content=content_list,
        status=tool_run_result["status"],
        toolUseId=tool_run_result["tool_use_id"],
    )


def _convert_after_tool_event_to_tool_run_result(
    event: AfterToolInvocationEvent,
) -> ToolRunResult:
    """Convert AfterToolInvocationEvent to our ToolRunResult format."""
    tool_input = event.tool_use["input"]
    tool_name = event.tool_use["name"]

    result = event.result
    tool_use_id = result["toolUseId"]
    tool_result_status = result["status"]
    tool_result_content = result["content"]

    # Convert content items to function results first
    function_results = []
    for content_item in tool_result_content:
        function_result = _convert_tool_result_content_to_function_result(content_item)
        function_results.append(function_result)

    # Handle like agent_tool.py: check if it's a list or single result
    if len(function_results) > 1:
        # Multiple results - treat as list
        related_documents = [
            _function_result_to_related_document(
                tool_name=tool_name,
                res=result,
                source_id_base=tool_use_id,
                rank=rank,
            )
            for rank, result in enumerate(function_results)
        ]
    else:
        # Single result
        single_result = function_results[0] if function_results else ""
        related_documents = [
            _function_result_to_related_document(
                tool_name=tool_name,
                res=single_result,
                source_id_base=tool_use_id,
            )
        ]

    return ToolRunResult(
        tool_use_id=tool_use_id,
        status=tool_result_status,
        related_documents=related_documents,
    )


class ToolResultCapture(HookProvider):
    def __init__(
        self,
        bot: BotModel,
        model: type_model_name,
        on_tool_result: Callable[[ToolRunResult], None] | None = None,
    ):
        self.bot = bot
        self.model = model
        self.on_tool_result = on_tool_result
        self.captured_tool_results: dict[str, ToolRunResult] = {}
        self.tool_mapping: dict[str, AgentTool] = {}

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self.before_tool_execution)
        registry.add_callback(AfterToolInvocationEvent, self.after_tool_execution)

    def before_tool_execution(self, event: BeforeToolInvocationEvent) -> None:
        """Handler called before a tool is executed."""
        logger.debug("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logger.debug("Before tool execution: %r", event)
        # Additional implementation as needed

    def after_tool_execution(self, event: AfterToolInvocationEvent) -> None:
        """Handler called after a tool is executed."""
        logger.debug("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logger.debug("After tool execution for tool: %r", event)

        # Convert event to ToolRunResult using the new function
        tool_result = _convert_after_tool_event_to_tool_run_result(event)

        # Store the result
        self.captured_tool_results[tool_result["tool_use_id"]] = tool_result

        # Call callback if provided
        if self.on_tool_result:
            self.on_tool_result(tool_result)

        # Convert ToolRunResult back to Strands ToolResult format with `source_id` for citation
        enhanced_result = _convert_tool_run_result_to_strands_tool_result(tool_result)
        event.result = enhanced_result


def chat_with_strands(
    user: User,
    chat_input: ChatInput,
    on_stream: Callable[[str], None] | None = None,
    on_stop: Callable[[OnStopInput], None] | None = None,
    on_thinking: Callable[[OnThinking], None] | None = None,
    on_tool_result: Callable[[ToolRunResult], None] | None = None,
    on_reasoning: Callable[[str], None] | None = None,
) -> tuple[ConversationModel, MessageModel]:
    user_msg_id, conversation, bot = prepare_conversation(user, chat_input)

    if bot:
        tool_capture = ToolResultCapture(bot, chat_input.message.model, on_tool_result)
