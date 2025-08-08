import base64
import dataclasses
import json
import logging
import os
from typing import Callable, Optional

from app.agents.tools.agent_tool import (
    AgentTool,
    ToolFunctionResult,
    ToolRunResult,
    _function_result_to_related_document,
)
from app.bedrock import is_tooluse_supported
from app.prompt import get_prompt_to_cite_tool_results
from app.repositories.conversation import store_conversation, store_related_documents
from app.repositories.models.conversation import (
    AttachmentContentModel,
    ContentModel,
    ConversationModel,
    ImageContentModel,
    JsonToolResultModel,
    MessageModel,
    ReasoningContentModel,
    RelatedDocumentModel,
    SimpleMessageModel,
    TextContentModel,
    TextToolResultModel,
    ToolResultContentModel,
    ToolResultContentModelBody,
    ToolUseContentModel,
    ToolUseContentModelBody,
    type_model_name,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import ChatInput
from app.strands_integration.utils import get_strands_tools
from app.stream import OnStopInput, OnThinking
from app.usecases.bot import modify_bot_last_used_time, modify_bot_stats
from app.usecases.chat import prepare_conversation, trace_to_root
from app.user import User
from app.utils import get_current_time
from strands import Agent
from strands.agent import AgentResult
from strands.experimental.hooks import AfterToolInvocationEvent, BeforeToolInvocationEvent
from strands.hooks import (  # AfterInvocationEvent,; BeforeInvocationEvent,
    HookProvider,
    HookRegistry,
)
from strands.models import BedrockModel
from strands.telemetry.metrics import EventLoopMetrics
from strands.types.content import ContentBlock, Message, Messages, Role
from strands.types.media import DocumentFormat, ImageFormat
from strands.types.tools import AgentTool as StrandsAgentTool
from strands.types.tools import ToolResult, ToolResultContent
from ulid import ULID

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")


def _map_to_image_format(media_type: str) -> ImageFormat:
    """Map media type to Strands ImageFormat."""
    # Extract format from media type (e.g., "image/png" -> "png")
    format_str = media_type.split("/")[-1].lower()

    # Map to valid ImageFormat values
    if format_str in ["png", "jpeg", "jpg", "gif", "webp"]:
        if format_str == "jpg":
            return "jpeg"
        return format_str  # type: ignore
    else:
        # Default to png for unsupported formats
        logger.warning(f"Unsupported image format: {format_str}, defaulting to png")
        return "png"


def _map_to_document_format(file_name: str) -> DocumentFormat:
    """Map file extension to Strands DocumentFormat."""
    # Extract extension from filename
    if "." not in file_name:
        return "txt"

    ext = file_name.split(".")[-1].lower()

    # Map to valid DocumentFormat values
    valid_formats = ["pdf", "csv", "doc", "docx", "xls", "xlsx", "html", "txt", "md"]
    if ext in valid_formats:
        return ext  # type: ignore
    else:
        # Default to txt for unsupported formats
        logger.warning(f"Unsupported document format: {ext}, defaulting to txt")
        return "txt"


def _convert_attachment_to_content_block(content: AttachmentContentModel) -> ContentBlock:
    """Convert AttachmentContentModel to Strands ContentBlock format."""
    import re
    import urllib.parse
    from pathlib import Path

    # Use decoded filename for format detection
    try:
        decoded_name = urllib.parse.unquote(content.file_name)
    except:
        decoded_name = content.file_name

    # Extract format and name like legacy implementation
    format = Path(decoded_name).suffix[1:]  # Remove the dot
    name = Path(decoded_name).stem

    # Convert to valid file name (matching legacy)
    def _convert_to_valid_file_name(file_name: str) -> str:
        file_name = re.sub(r"[^a-zA-Z0-9\s\-\(\)\[\]]", "", file_name)
        file_name = re.sub(r"\s+", " ", file_name)
        return file_name.strip()

    valid_name = _convert_to_valid_file_name(name)

    return {
        "document": {
            "format": format,
            "name": valid_name,
            "source": {"bytes": content.body},  # Use body directly (already base64)
        }
    }


def _convert_simple_messages_to_strands_messages(
    simple_messages: list[SimpleMessageModel],
) -> Messages:
    """Convert SimpleMessageModel list to Strands Messages format."""
    messages: Messages = []

    for simple_msg in simple_messages:

        # Skip system messages as they are handled separately in Strands
        if simple_msg.role == "system":
            continue

        # Skip instruction messages as they are handled separately via message_map
        if simple_msg.role == "instruction":
            continue

        # Ensure role is valid
        if simple_msg.role not in ["user", "assistant"]:
            logger.warning(f"Invalid role: {simple_msg.role}, skipping message")
            continue

        role: Role = simple_msg.role  # type: ignore

        # Convert content to ContentBlock list
        content_blocks: list[ContentBlock] = []
        for content in simple_msg.content:
            if isinstance(content, TextContentModel):
                content_block: ContentBlock = {"text": content.body}
                content_blocks.append(content_block)
            elif isinstance(content, ImageContentModel):
                # Convert image content
                try:
                    # content.body is already binary data (Base64EncodedBytes), no need to decode
                    image_bytes = content.body
                    image_format = _map_to_image_format(content.media_type)
                    content_block: ContentBlock = {
                        "image": {
                            "format": image_format,
                            "source": {"bytes": image_bytes},
                        }
                    }
                    content_blocks.append(content_block)
                except Exception as e:
                    logger.warning(f"Failed to convert image content: {e}")
            elif isinstance(content, AttachmentContentModel):
                try:
                    content_block = _convert_attachment_to_content_block(content)
                    content_blocks.append(content_block)
                except Exception as e:
                    logger.warning(f"Failed to convert attachment content: {e}")
            elif isinstance(content, ToolUseContentModel):
                # Convert tool use
                content_block = {
                    "toolUse": {
                        "toolUseId": content.body.tool_use_id,
                        "name": content.body.name,
                        "input": content.body.input,
                    }
                }
                content_blocks.append(content_block)
            elif isinstance(content, ToolResultContentModel):
                # Convert tool result
                tool_result_content = []
                for result_item in content.body.content:
                    if hasattr(result_item, "text"):
                        tool_result_content.append({"text": result_item.text})
                    elif hasattr(result_item, "json_"):
                        tool_result_content.append({"json": result_item.json_})
                    else:
                        tool_result_content.append({"text": str(result_item)})

                content_block = {
                    "toolResult": {
                        "toolUseId": content.body.tool_use_id,
                        "content": tool_result_content,
                        "status": "success",  # Default status
                    }
                }
                content_blocks.append(content_block)
            elif isinstance(content, ReasoningContentModel):
                # Convert reasoning content
                content_block = {
                    "reasoningContent": {"reasoningText": {"text": content.text}}
                }
                content_blocks.append(content_block)
            else:
                logger.warning(f"Unknown content type: {type(content)}")

        # Only add message if it has content
        if content_blocks:
            message: Message = {
                "role": role,
                "content": content_blocks,
            }
            messages.append(message)

    return messages


def _convert_messages_to_content_blocks(messages: Messages, continue_generate: bool = False) -> list[ContentBlock]:
    """Convert Messages to ContentBlock list for Strands agent."""
    content_blocks: list[ContentBlock] = []

    for i, message in enumerate(messages):
        # Add role information as text content block
        role_text = f"[{message['role'].upper()}]"
        role_block: ContentBlock = {"text": role_text}
        content_blocks.append(role_block)

        # Add all content blocks from the message
        content_blocks.extend(message["content"])
        
        # If this is the last message and we're continuing generation, add continue instruction
        if continue_generate and i == len(messages) - 1 and message['role'] == 'assistant':
            continue_instruction: ContentBlock = {"text": "\n\n[CONTINUE THE ABOVE ASSISTANT MESSAGE]"}
            content_blocks.append(continue_instruction)

    return content_blocks


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


def create_strands_agent(
    bot: BotModel | None,
    instructions: list[str],
    model_name: type_model_name,
    enable_reasoning: bool = False,
    hooks: list[HookProvider] | None = None,
) -> Agent:
    model_config = _get_bedrock_model_config(bot, model_name, enable_reasoning)
    logger.debug(f"[AGENT_FACTORY] Model config: {model_config}")
    model = BedrockModel(**model_config)

    # Strands does not support list of instructions, so we join them into a single string.
    system_prompt = "\n\n".join(instructions).strip() if instructions else None

    agent = Agent(
        model=model,
        tools=get_strands_tools(bot, model_name),
        hooks=hooks or [],
        system_prompt=system_prompt,
    )
    return agent


def _get_bedrock_model_config(
    bot: BotModel | None,
    model_name: type_model_name = "claude-v3.5-sonnet",
    enable_reasoning: bool = False,
) -> dict:
    """Get Bedrock model configuration."""
    from app.bedrock import get_model_id

    model_id = get_model_id(model_name)

    config = {
        "model_id": model_id,
        "region_name": BEDROCK_REGION,
    }

    # Add model parameters if available
    if bot and bot.generation_params:
        if bot.generation_params.temperature is not None:
            config["temperature"] = bot.generation_params.temperature
        if bot.generation_params.top_p is not None:
            config["top_p"] = bot.generation_params.top_p
        if bot.generation_params.max_tokens is not None:
            config["max_tokens"] = bot.generation_params.max_tokens

    # Add Guardrails configuration (Strands way)
    if bot and bot.bedrock_guardrails:
        guardrails = bot.bedrock_guardrails
        config["guardrail_id"] = guardrails.guardrail_arn
        config["guardrail_version"] = guardrails.guardrail_version
        config["guardrail_trace"] = "enabled"  # Enable trace for debugging
        logger.info(f"Enabled Guardrails: {guardrails.guardrail_arn}")

    # Add reasoning functionality if explicitly enabled
    additional_request_fields = {}
    if enable_reasoning:
        # Import config for default values
        from app.config import DEFAULT_GENERATION_CONFIG

        # Enable thinking/reasoning functionality
        budget_tokens = DEFAULT_GENERATION_CONFIG["reasoning_params"][
            "budget_tokens"
        ]  # Use config default (1024)

        # Use bot's reasoning params if available
        if bot and bot.generation_params and bot.generation_params.reasoning_params:
            budget_tokens = bot.generation_params.reasoning_params.budget_tokens

        additional_request_fields["thinking"] = {
            "type": "enabled",
            "budget_tokens": budget_tokens,
        }
        # When thinking is enabled, temperature must be 1
        config["temperature"] = 1.0
        logger.debug(
            f"[AGENT_FACTORY] Reasoning enabled with budget_tokens: {budget_tokens}"
        )

    if additional_request_fields:
        config["additional_request_fields"] = additional_request_fields

    return config


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


def _create_callback_handler(
    on_stream: Callable[[str], None] | None = None,
    on_thinking: Callable[[OnThinking], None] | None = None,
    on_tool_result: Callable[[ToolRunResult], None] | None = None,
    on_reasoning: Callable[[str], None] | None = None,
) -> CallbackHandler:
    """Create a callback handler instance."""
    return CallbackHandler(on_stream, on_thinking, on_tool_result, on_reasoning)


def _convert_strands_message_to_message_model(
    message: Message, model_name: type_model_name, create_time: float
) -> MessageModel:
    """Convert Strands Message to MessageModel."""
    content_models: list[ContentModel] = []

    for content_block in message["content"]:
        content_model: ContentModel
        if "text" in content_block:
            content_model = TextContentModel(
                content_type="text", body=content_block["text"]
            )
            content_models.append(content_model)
        elif "reasoningContent" in content_block:
            reasoning_content = content_block["reasoningContent"]
            if "reasoningText" in reasoning_content:
                reasoning_text = reasoning_content["reasoningText"]
                content_model = ReasoningContentModel(
                    content_type="reasoning",
                    text=reasoning_text.get("text", ""),
                    signature=reasoning_text.get("signature", ""),
                    redacted_content=b"",  # Default empty
                )
                content_models.append(content_model)
        elif "toolUse" in content_block:
            tool_use = content_block["toolUse"]
            content_model = ToolUseContentModel(
                content_type="toolUse",
                body=ToolUseContentModelBody(
                    tool_use_id=tool_use["toolUseId"],
                    name=tool_use["name"],
                    input=tool_use["input"],
                ),
            )
            content_models.append(content_model)
        elif "toolResult" in content_block:
            tool_result = content_block["toolResult"]
            # Convert ToolResultContent to ToolResultModel
            from app.repositories.models.conversation import ToolResultModel

            result_models: list[ToolResultModel] = []
            for content_item in tool_result["content"]:
                if "text" in content_item:
                    result_models.append(TextToolResultModel(text=content_item["text"]))
                elif "json" in content_item:
                    result_models.append(JsonToolResultModel(json=content_item["json"]))
                # Add other content types as needed

            content_model = ToolResultContentModel(
                content_type="toolResult",
                body=ToolResultContentModelBody(
                    tool_use_id=tool_result["toolUseId"],
                    content=result_models,
                    status=tool_result.get("status", "success"),
                ),
            )
            content_models.append(content_model)

    return MessageModel(
        role=message["role"],
        content=content_models,
        model=model_name,
        children=[],
        parent=None,  # Will be set later
        create_time=create_time,
        feedback=None,
        used_chunks=None,
        thinking_log=None,
    )


def _extract_related_documents_from_tool_capture(
    tool_capture: ToolResultCapture, assistant_msg_id: str
) -> list[RelatedDocumentModel]:
    """Extract related documents from ToolResultCapture."""
    related_documents = []

    for tool_use_id, tool_result in tool_capture.captured_tool_results.items():
        for related_doc in tool_result["related_documents"]:
            # Update source_id to be based on assistant_msg_id for citation
            updated_doc = RelatedDocumentModel(
                content=related_doc.content,
                source_id=f"{assistant_msg_id}@{related_doc.source_id}",
                source_name=related_doc.source_name,
                source_link=related_doc.source_link,
                page_number=related_doc.page_number,
            )
            related_documents.append(updated_doc)

    return related_documents


def _calculate_conversation_cost(
    metrics: EventLoopMetrics, model_name: type_model_name
) -> float:
    """Calculate conversation cost from AgentResult metrics."""
    from app.bedrock import calculate_price

    # Extract token usage from metrics
    input_tokens = metrics.accumulated_usage.get("inputTokens", 0)
    output_tokens = metrics.accumulated_usage.get("outputTokens", 0)
    # Strands doesn't provide cache token info, so default to 0
    cache_read_input_tokens = 0
    cache_write_input_tokens = 0

    # Calculate price using the same function as chat_legacy
    price = calculate_price(
        model=model_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_read_input_tokens=cache_read_input_tokens,
        cache_write_input_tokens=cache_write_input_tokens,
    )

    logger.info(
        f"Strands token usage: input={input_tokens}, output={output_tokens}, price={price}"
    )

    return price


def _build_thinking_log_from_tool_capture(
    tool_capture: ToolResultCapture,
) -> list[SimpleMessageModel] | None:
    """Build thinking_log from ToolResultCapture for tool use/result pairs."""
    if not tool_capture.captured_tool_results:
        return None

    thinking_log = []

    for tool_use_id, tool_result in tool_capture.captured_tool_results.items():
        # Get tool use info from captured data
        tool_use_info = tool_capture.captured_tool_uses.get(tool_use_id, {})

        # Create tool use message
        tool_use_content = ToolUseContentModel(
            content_type="toolUse",
            body=ToolUseContentModelBody(
                tool_use_id=tool_use_id,
                name=tool_use_info.get("name", "unknown"),
                input=tool_use_info.get("input", {}),
            ),
        )

        tool_use_message = SimpleMessageModel(
            role="assistant", content=[tool_use_content]
        )
        thinking_log.append(tool_use_message)

        # Create tool result message
        from app.repositories.models.conversation import ToolResultModel

        result_models: list[ToolResultModel] = []
        for related_doc in tool_result["related_documents"]:
            result_models.append(related_doc.content)

        tool_result_content = ToolResultContentModel(
            content_type="toolResult",
            body=ToolResultContentModelBody(
                tool_use_id=tool_use_id,
                content=result_models,
                status=tool_result["status"],
            ),
        )

        tool_result_message = SimpleMessageModel(
            role="user", content=[tool_result_content]
        )
        thinking_log.append(tool_result_message)

    return thinking_log if thinking_log else None


def _extract_reasoning_from_message(message: Message) -> ReasoningContentModel | None:
    """Extract reasoning content from Strands Message."""
    for content_block in message["content"]:
        if "reasoningContent" in content_block:
            reasoning_content = content_block["reasoningContent"]
            if "reasoningText" in reasoning_content:
                reasoning_text = reasoning_content["reasoningText"]
                return ReasoningContentModel(
                    content_type="reasoning",
                    text=reasoning_text.get("text", ""),
                    signature=reasoning_text.get("signature", "")
                    or "",  # Ensure not None
                    redacted_content=b"",  # Default empty
                )
    return None


def _create_on_stop_input(
    result: AgentResult, message: MessageModel, price: float
) -> OnStopInput:
    """Create OnStopInput from AgentResult."""
    return {
        "message": message,
        "stop_reason": result.stop_reason,
        "price": price,
        "input_token_count": result.metrics.accumulated_usage.get("inputTokens", 0),
        "output_token_count": result.metrics.accumulated_usage.get("outputTokens", 0),
        "cache_read_input_count": 0,  # Strands doesn't provide cache token info
        "cache_write_input_count": 0,  # Strands doesn't provide cache token info
    }


def _post_process_strands_result(
    result: AgentResult,
    conversation: ConversationModel,
    user_msg_id: str,
    bot: BotModel | None,
    user: User,
    model_name: type_model_name,
    continue_generate: bool,
    tool_capture: ToolResultCapture,
    on_stop: Callable[[OnStopInput], None] | None = None,
) -> tuple[ConversationModel, MessageModel]:
    """Post-process Strands AgentResult and update conversation."""
    current_time = get_current_time()

    # 1. Convert Strands Message to MessageModel
    message = _convert_strands_message_to_message_model(
        result.message, model_name, current_time
    )

    # 2. Calculate cost and update conversation
    price = _calculate_conversation_cost(result.metrics, model_name)
    conversation.total_price += price
    conversation.should_continue = result.stop_reason == "max_tokens"

    # # 3. Extract reasoning content and add to message content if present
    # reasoning_content = _extract_reasoning_from_message(result.message)
    # if reasoning_content:
    #     message.content.insert(0, reasoning_content)

    # 4. Build thinking_log from tool capture
    thinking_log = _build_thinking_log_from_tool_capture(tool_capture)
    if thinking_log:
        message.thinking_log = thinking_log

    # 5. Set message parent and generate assistant message ID
    message.parent = user_msg_id

    if continue_generate:
        # For continue generate
        if not thinking_log:
            assistant_msg_id = conversation.last_message_id
            conversation.message_map[assistant_msg_id] = message
        else:
            # Remove old assistant message and create new one
            old_assistant_msg_id = conversation.last_message_id
            conversation.message_map[user_msg_id].children.remove(old_assistant_msg_id)
            del conversation.message_map[old_assistant_msg_id]

            assistant_msg_id = str(ULID())
            conversation.message_map[assistant_msg_id] = message
            conversation.message_map[user_msg_id].children.append(assistant_msg_id)
            conversation.last_message_id = assistant_msg_id
    else:
        # Normal case: create new assistant message
        assistant_msg_id = str(ULID())
        conversation.message_map[assistant_msg_id] = message
        conversation.message_map[user_msg_id].children.append(assistant_msg_id)
        conversation.last_message_id = assistant_msg_id

    # 6. Extract related documents from tool capture
    related_documents = _extract_related_documents_from_tool_capture(
        tool_capture, assistant_msg_id
    )

    # 7. Store conversation and related documents
    store_conversation(user.id, conversation)
    if related_documents:
        store_related_documents(
            user_id=user.id,
            conversation_id=conversation.id,
            related_documents=related_documents,
        )

    # 8. Call on_stop callback
    if on_stop:
        on_stop_input = _create_on_stop_input(result, message, price)
        on_stop(on_stop_input)

    # 9. Update bot statistics
    if bot:
        logger.info("Bot is provided. Updating bot last used time.")
        modify_bot_last_used_time(user, bot)
        modify_bot_stats(user, bot, increment=1)

    return conversation, message


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

    display_citation = bot is not None and bot.display_retrieved_chunks
    message_map = conversation.message_map
    instructions: list[str] = (
        [
            content.body
            for content in message_map["instruction"].content
            if isinstance(content, TextContentModel)
        ]
        if "instruction" in message_map
        else []
    )

    if bot is not None:
        if bot.is_agent_enabled() and is_tooluse_supported(chat_input.message.model):
            if display_citation:
                instructions.append(
                    get_prompt_to_cite_tool_results(
                        model=chat_input.message.model,
                    )
                )
        elif bot.has_knowledge() and not is_tooluse_supported(chat_input.message.model):
            logger.warning(
                f"Currently not supported for {chat_input.message.model} model."
            )

    # Leaf node id
    # If `continue_generate` is True, note that new message is not added to the message map.
    node_id = (
        chat_input.message.parent_message_id
        if chat_input.continue_generate
        else message_map[user_msg_id].parent
    )

    if node_id is None:
        raise ValueError("parent_message_id or parent is None")

    messages = trace_to_root(
        node_id=node_id,
        message_map=message_map,
    )

    continue_generate = chat_input.continue_generate

    # Create ToolResultCapture to capture tool execution data
    tool_capture = ToolResultCapture(
        on_thinking=on_thinking,
        on_tool_result=on_tool_result,
    )

    agent = create_strands_agent(
        bot=bot,
        instructions=instructions,
        model_name=chat_input.message.model,
        enable_reasoning=chat_input.enable_reasoning,
        hooks=[tool_capture],
    )

    agent.callback_handler = _create_callback_handler(
        on_stream=on_stream,
        on_thinking=on_thinking,
        on_tool_result=on_tool_result,
        on_reasoning=on_reasoning,
    )

    # Convert SimpleMessageModel list to Strands Messages format
    strands_messages = _convert_simple_messages_to_strands_messages(messages)

    # Add current user message if not continuing generation
    if not continue_generate:
        current_user_message = conversation.message_map[user_msg_id]
        current_content_blocks: list[ContentBlock] = []
        for content in current_user_message.content:
            if isinstance(content, TextContentModel):
                content_block: ContentBlock = {"text": content.body}
                current_content_blocks.append(content_block)
            elif isinstance(content, ImageContentModel):
                # Convert image content
                try:
                    # content.body is already binary data (Base64EncodedBytes), no need to decode
                    image_bytes = content.body
                    image_format = _map_to_image_format(content.media_type)

                    content_block: ContentBlock = {
                        "image": {
                            "format": image_format,
                            "source": {"bytes": image_bytes},
                        }
                    }
                    current_content_blocks.append(content_block)
                except Exception as e:
                    logger.warning(f"Failed to convert image content: {e}")
            elif isinstance(content, AttachmentContentModel):
                try:
                    content_block = _convert_attachment_to_content_block(content)
                    current_content_blocks.append(content_block)
                except Exception as e:
                    logger.warning(f"Failed to convert attachment content: {e}")

        if current_content_blocks:
            current_message: Message = {
                "role": "user",
                "content": current_content_blocks,
            }
            strands_messages.append(current_message)
    else:
        # For continue generation, add the last assistant message to continue from
        last_message = conversation.message_map[conversation.last_message_id]
        if last_message.role == "assistant":
            continue_content_blocks: list[ContentBlock] = []
            for content in last_message.content:
                if isinstance(content, TextContentModel):
                    content_block: ContentBlock = {"text": content.body}
                    continue_content_blocks.append(content_block)
            
            if continue_content_blocks:
                continue_message: Message = {
                    "role": "assistant",
                    "content": continue_content_blocks,
                }
                strands_messages.append(continue_message)

    # Convert Messages to ContentBlock list for agent
    content_blocks_for_agent = _convert_messages_to_content_blocks(strands_messages, continue_generate)

    result = agent(content_blocks_for_agent)

    # Post handling: process the result and update conversation
    return _post_process_strands_result(
        result=result,
        conversation=conversation,
        user_msg_id=user_msg_id,
        bot=bot,
        user=user,
        model_name=chat_input.message.model,
        continue_generate=continue_generate,
        tool_capture=tool_capture,
        on_stop=on_stop,
    )
