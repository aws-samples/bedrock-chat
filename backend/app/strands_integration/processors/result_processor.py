"""
Result processing utilities for Strands integration.
"""
import logging
from typing import Callable

from app.repositories.conversation import store_conversation, store_related_documents
from app.repositories.models.conversation import (
    ConversationModel,
    MessageModel,
    type_model_name,
)
from app.repositories.models.custom_bot import BotModel
from app.stream import OnStopInput
from app.usecases.bot import modify_bot_last_used_time, modify_bot_stats
from app.user import User
from app.utils import get_current_time
from strands.agent import AgentResult
from ulid import ULID

from ..converters.message_converter import convert_strands_message_to_message_model
from ..handlers.tool_result_capture import ToolResultCapture
from .cost_calculator import calculate_conversation_cost
from .document_extractor import (
    build_thinking_log_from_tool_capture,
    extract_related_documents_from_tool_capture,
)

logger = logging.getLogger(__name__)


def create_on_stop_input(
    result: AgentResult, message: MessageModel, price: float
) -> OnStopInput:
    """Create OnStopInput from AgentResult."""
    return {
        "message": message,
        "stop_reason": result.stop_reason,
        "price": price,
        "input_token_count": result.metrics.accumulated_usage.get("inputTokens", 0),
        "output_token_count": result.metrics.accumulated_usage.get("outputTokens", 0),
        # Cache token metrics not yet supported in strands-agents 1.3.0
        # See: https://github.com/strands-agents/sdk-python/issues/529
        "cache_read_input_count": result.metrics.accumulated_usage.get(
            "cacheReadInputTokens", 0
        ),
        "cache_write_input_count": result.metrics.accumulated_usage.get(
            "cacheWriteInputTokens", 0
        ),
    }


def post_process_strands_result(
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
    # NOTE: Strands agent limitation - when tool use is involved, reasoning content is only
    # available during streaming but not included in the final AgentResult.message.
    # This means reasoning is not persisted for tool use scenarios.
    message = convert_strands_message_to_message_model(
        result.message, model_name, current_time
    )

    # 2. Calculate cost and update conversation
    price = calculate_conversation_cost(result.metrics, model_name)
    conversation.total_price += price
    conversation.should_continue = result.stop_reason == "max_tokens"

    # 3. Build thinking_log from tool capture
    thinking_log = build_thinking_log_from_tool_capture(tool_capture)
    if thinking_log:
        message.thinking_log = thinking_log

    # 4. Set message parent and generate assistant message ID
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

    # 5. Extract related documents from tool capture
    related_documents = extract_related_documents_from_tool_capture(
        tool_capture, assistant_msg_id
    )

    # 6. Store conversation and related documents
    store_conversation(user.id, conversation)
    if related_documents:
        store_related_documents(
            user_id=user.id,
            conversation_id=conversation.id,
            related_documents=related_documents,
        )

    # 7. Call on_stop callback
    if on_stop:
        on_stop_input = create_on_stop_input(result, message, price)
        on_stop(on_stop_input)

    # 8. Update bot statistics
    if bot:
        logger.debug("Bot is provided. Updating bot last used time.")
        modify_bot_last_used_time(user, bot)
        modify_bot_stats(user, bot, increment=1)

    return conversation, message
