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
from app.repositories.models.conversation import (
    AttachmentContentModel,
    ConversationModel,
    ImageContentModel,
    MessageModel,
    ReasoningContentModel,
    SimpleMessageModel,
    TextContentModel,
    ToolResultContentModel,
    ToolUseContentModel,
    type_model_name,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import ChatInput
from app.stream import OnStopInput, OnThinking
from app.usecases.chat import prepare_conversation, trace_to_root
from app.user import User
from strands import Agent
from strands.experimental.hooks import AfterToolInvocationEvent, BeforeToolInvocationEvent
from strands.hooks import (  # AfterInvocationEvent,; BeforeInvocationEvent,
    HookProvider,
    HookRegistry,
)
from strands.models import BedrockModel
from strands.types.content import ContentBlock, Message, Messages, Role
from strands.types.media import DocumentFormat, ImageFormat
from strands.types.tools import AgentTool, ToolResult, ToolResultContent

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


def _convert_simple_messages_to_strands_messages(
    simple_messages: list[SimpleMessageModel],
) -> Messages:
    """Convert SimpleMessageModel list to Strands Messages format."""
    messages: Messages = []

    for simple_msg in simple_messages:
        # Skip system messages as they are handled separately in Strands
        if simple_msg.role == "system":
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
                    import base64

                    image_bytes = base64.b64decode(content.body)
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
                # Convert attachment as document
                try:
                    import base64

                    doc_bytes = base64.b64decode(content.body)
                    doc_format = _map_to_document_format(content.file_name)
                    content_block: ContentBlock = {
                        "document": {
                            "format": doc_format,
                            "name": content.file_name,
                            "source": {"bytes": doc_bytes},
                        }
                    }
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


def _convert_messages_to_content_blocks(messages: Messages) -> list[ContentBlock]:
    """Convert Messages to ContentBlock list for Strands agent."""
    content_blocks: list[ContentBlock] = []

    for message in messages:
        # Add role information as text content block
        role_text = f"[{message['role'].upper()}]"
        role_block: ContentBlock = {"text": role_text}
        content_blocks.append(role_block)

        # Add all content blocks from the message
        content_blocks.extend(message["content"])

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

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self.before_tool_execution)
        registry.add_callback(AfterToolInvocationEvent, self.after_tool_execution)

    def before_tool_execution(self, event: BeforeToolInvocationEvent) -> None:
        """Handler called before a tool is executed."""
        logger.debug("Before tool execution: %r", event)

        if self.on_thinking:
            # Convert BeforeToolInvocationEvent to OnThinking format
            tool_use = event.tool_use
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


def get_strands_tools(
    bot: BotModel | None, model_name: type_model_name
) -> list[AgentTool]:
    if not is_tooluse_supported(model_name):
        logger.warning(
            f"Tool use is not supported for model {model_name}. Returning empty tool list."
        )
        return []

    # TODO. refer: backend/app/agents/utils.py


# def get_prompt_to_cite_tool_results(model: type_model_name) -> str:
#     # TODO. refer backend/app/prompt.py but
#     ...


def create_strands_agent(
    bot: BotModel | None,
    instructions: list[str],
    model_name: type_model_name,
    enable_reasoning: bool = False,
    on_tool_result: Callable[[ToolRunResult], None] | None = None,
) -> Agent:
    model_config = _get_bedrock_model_config(bot, model_name, enable_reasoning)
    logger.debug(f"[AGENT_FACTORY] Model config: {model_config}")
    model = BedrockModel(**model_config)

    # Strands does not support list of instructions, so we join them into a single string.
    system_prompt = "\n\n".join(instructions).strip() if instructions else None

    agent = Agent(
        model=model,
        tools=get_strands_tools(bot, model_name),
        hooks=[ToolResultCapture(on_tool_result)],
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


def _create_callback_handler(
    on_stream: Callable[[str], None] | None = None,
    on_thinking: Callable[[OnThinking], None] | None = None,
    on_tool_result: Callable[[ToolRunResult], None] | None = None,
    on_reasoning: Callable[[str], None] | None = None,
) -> Callable:
    collected_reasoning = []

    def callback_handler(**kwargs):
        logger.debug(
            f"[STRANDS_CALLBACK] Callback triggered with keys: {list(kwargs.keys())}"
        )
        if "data" in kwargs and on_stream:
            data = kwargs["data"]
            on_stream(data)
        elif "reasoning" in kwargs and on_reasoning:
            reasoning_text = kwargs.get("reasoningText", "")
            on_reasoning(reasoning_text)
            collected_reasoning.append(reasoning_text)
        elif "thinking" in kwargs and on_reasoning:
            thinking_text = kwargs.get("thinking", "")
            on_reasoning(thinking_text)
            collected_reasoning.append(thinking_text)
        # elif "event" in kwargs:
        #     event = kwargs["event"]
        #     print(f"[STRANDS_CALLBACK] Event: {event}")
        # elif "message" in kwargs:
        #     message = kwargs["message"]
        #     print(f"[STRANDS_CALLBACK] Message: {message}")

    return callback_handler


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

    agent = create_strands_agent(
        bot=bot,
        instructions=instructions,
        model_name=chat_input.message.model,
        enable_reasoning=chat_input.enable_reasoning,
        on_tool_result=on_tool_result,
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

        if current_content_blocks:
            current_message: Message = {
                "role": "user",
                "content": current_content_blocks,
            }
            strands_messages.append(current_message)

    # Convert Messages to ContentBlock list for agent
    content_blocks_for_agent = _convert_messages_to_content_blocks(strands_messages)

    result = agent(content_blocks_for_agent)

    # TODO: Post handling
    # - Save conversation / related documents
    # - Update bot last used time
