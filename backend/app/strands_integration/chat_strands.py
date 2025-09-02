"""
Main chat function for Strands integration.
"""

import logging
from typing import Callable

from app.agents.tools.agent_tool import ToolRunResult
from app.bedrock import is_tooluse_supported
from app.prompt import get_prompt_to_cite_tool_results
from app.repositories.models.conversation import (
    AttachmentContentModel,
    ConversationModel,
    ImageContentModel,
    MessageModel,
    TextContentModel,
)
from app.routes.schemas.conversation import ChatInput
from app.stream import OnStopInput, OnThinking
from app.usecases.chat import prepare_conversation, trace_to_root
from app.user import User
from strands.types.content import ContentBlock, Message

from .agent import create_strands_agent
from .converters import (
    convert_attachment_to_content_block,
    convert_messages_to_content_blocks,
    convert_simple_messages_to_strands_messages,
    map_to_image_format,
)
from .handlers import ToolResultCapture, create_callback_handler
from .processors import post_process_strands_result
from .telemetry import StrandsTelemetryManager

logger = logging.getLogger(__name__)


def chat_with_strands(
    user: User,
    chat_input: ChatInput,
    on_stream: Callable[[str], None] | None = None,
    on_stop: Callable[[OnStopInput], None] | None = None,
    on_thinking: Callable[[OnThinking], None] | None = None,
    on_tool_result: Callable[[ToolRunResult], None] | None = None,
    on_reasoning: Callable[[str], None] | None = None,
) -> tuple[ConversationModel, MessageModel]:
    """
    Chat with Strands agents.

    Architecture Overview:

    1. Reasoning Content:
       - Streaming: CallbackHandler processes reasoning events for real-time display
       - Persistence: Telemetry (ReasoningSpanProcessor) extracts from OpenTelemetry spans

    2. Tool Use/Result (Thinking Log):
       - Streaming: ToolResultCapture processes tool events for real-time display
       - Persistence: ToolResultCapture stores processed data for DynamoDB storage

    3. Related Documents (Citations):
       - Source: ToolResultCapture only
       - Reason: Requires access to raw tool results for source_link extraction

    Why This Hybrid Approach:

    - ToolResultCapture: Processes raw tool results during execution hooks, enabling
      source_link extraction and citation functionality. Telemetry only captures
      post-processed data, losing metadata required for citations.

    - Telemetry: Captures complete reasoning content from OpenTelemetry spans,
      providing reliable persistence for reasoning data that may not be available
      in final AgentResult when tools are used.

    - CallbackHandler: Handles real-time streaming of reasoning content during
      agent execution for immediate user feedback.
    """
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

    # Setup telemetry manager for reasoning capture
    telemetry_manager = StrandsTelemetryManager()
    telemetry_manager.setup(conversation.id, user.id)

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

    agent.callback_handler = create_callback_handler(
        on_stream=on_stream,
        on_reasoning=on_reasoning,
    )

    # Convert SimpleMessageModel list to Strands Messages format
    strands_messages = convert_simple_messages_to_strands_messages(
        messages, chat_input.message.model, bot.prompt_caching_enabled if bot else True
    )

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
                    image_format = map_to_image_format(content.media_type)

                    image_content_block: ContentBlock = {
                        "image": {
                            "format": image_format,
                            "source": {"bytes": image_bytes},
                        }
                    }
                    current_content_blocks.append(image_content_block)
                except Exception as e:
                    logger.warning(f"Failed to convert image content: {e}")
            elif isinstance(content, AttachmentContentModel):
                try:
                    attachment_content_block = convert_attachment_to_content_block(
                        content
                    )
                    current_content_blocks.append(attachment_content_block)
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
                    continue_text_block: ContentBlock = {"text": content.body}
                    continue_content_blocks.append(continue_text_block)

            if continue_content_blocks:
                continue_message: Message = {
                    "role": "assistant",
                    "content": continue_content_blocks,
                }
                strands_messages.append(continue_message)

    # Convert Messages to ContentBlock list for agent
    content_blocks_for_agent = convert_messages_to_content_blocks(
        strands_messages, continue_generate
    )

    result = agent(content_blocks_for_agent)

    # Post handling: process the result and update conversation
    return post_process_strands_result(
        result=result,
        conversation=conversation,
        user_msg_id=user_msg_id,
        bot=bot,
        user=user,
        model_name=chat_input.message.model,
        continue_generate=continue_generate,
        telemetry_manager=telemetry_manager,
        tool_capture=tool_capture,
        on_stop=on_stop,
    )
