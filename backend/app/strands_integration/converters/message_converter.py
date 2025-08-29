"""
Message conversion utilities for Strands integration.
"""
import logging

from app.bedrock import is_prompt_caching_supported
from app.repositories.models.conversation import (
    AttachmentContentModel,
    ContentModel,
    ImageContentModel,
    JsonToolResultModel,
    MessageModel,
    ReasoningContentModel,
    SimpleMessageModel,
    TextContentModel,
    TextToolResultModel,
    ToolResultContentModel,
    ToolResultContentModelBody,
    ToolUseContentModel,
    ToolUseContentModelBody,
    type_model_name,
)
from strands.types.content import ContentBlock, Message, Messages, Role

from .content_converter import convert_attachment_to_content_block
from .format_mapper import map_to_image_format

logger = logging.getLogger(__name__)


def convert_simple_messages_to_strands_messages(
    simple_messages: list[SimpleMessageModel],
    model: type_model_name,
    prompt_caching_enabled: bool = True,
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

        # Skip messages with tool use content or reasoning content (from thinking_log)
        has_tool_or_reasoning_content = any(
            isinstance(
                content,
                (ToolUseContentModel, ToolResultContentModel, ReasoningContentModel),
            )
            for content in simple_msg.content
        )
        if has_tool_or_reasoning_content:
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
                    image_format = map_to_image_format(content.media_type)
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
                    content_block = convert_attachment_to_content_block(content)
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

    # Add message cache points (same logic as legacy bedrock.py)
    if prompt_caching_enabled and is_prompt_caching_supported(model, target="message"):
        for order, message in enumerate(
            filter(lambda m: m["role"] == "user", reversed(messages))
        ):
            if order >= 2:
                break

            message["content"] = [
                *(message["content"]),
                {
                    "cachePoint": {"type": "default"},
                },
            ]
            logger.debug(f"Added message cache point to user message: {message}")

    return messages


def convert_messages_to_content_blocks(
    messages: Messages, continue_generate: bool = False
) -> list[ContentBlock]:
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
        if (
            continue_generate
            and i == len(messages) - 1
            and message["role"] == "assistant"
        ):
            continue_instruction: ContentBlock = {
                "text": "\n\n[CONTINUE THE ABOVE ASSISTANT MESSAGE]"
            }
            content_blocks.append(continue_instruction)

    return content_blocks


def convert_strands_message_to_message_model(
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
