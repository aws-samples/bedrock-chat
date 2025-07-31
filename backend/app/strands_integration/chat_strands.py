"""
Strands integration for chat functionality.
This module provides a Strands-based implementation of the chat function
that maintains compatibility with the existing chat API.
"""

import logging
from typing import Callable

from app.agents.tools.agent_tool import ToolRunResult
from app.repositories.models.conversation import ConversationModel, MessageModel
from app.routes.schemas.conversation import ChatInput
from app.stream import OnStopInput, OnThinking
from app.user import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
    Strands implementation core logic.
    """
    from app.repositories.conversation import store_conversation
    from app.repositories.models.conversation import MessageModel, TextContentModel
    from app.usecases.chat import prepare_conversation
    from app.utils import get_current_time
    from strands import Agent
    from strands.models import BedrockModel
    from ulid import ULID

    # 1. 既存の会話準備ロジックを流用
    user_msg_id, conversation, bot = prepare_conversation(user, chat_input)

    # 2. Strandsエージェント作成（リファクタリング版）
    from app.strands_integration.agent_factory import create_strands_agent
    
    # モデル名をchat_inputから取得
    model_name = chat_input.message.model if chat_input.message.model else "claude-v3.5-sonnet"
    agent = create_strands_agent(bot, user, model_name)

    # 推論機能設定
    if chat_input.enable_reasoning:
        # Strandsでの推論機能設定（実装に応じて調整）
        try:
            # BedrockModelの推論機能を有効化
            if hasattr(agent.model, 'enable_reasoning'):
                agent.model.enable_reasoning = True
            elif hasattr(agent.model, 'additional_request_fields'):
                agent.model.additional_request_fields = {
                    "thinking": {"type": "enabled", "budget_tokens": 1024}
                }
        except Exception as e:
            logger.warning(f"Could not enable reasoning: {e}")

    # 3. コールバックハンドラー設定
    if any([on_stream, on_thinking, on_tool_result, on_reasoning]):
        agent.callback_handler = _create_callback_handler(
            on_stream, on_thinking, on_tool_result, on_reasoning
        )

    # 4. ユーザーメッセージ取得
    user_message = _get_user_message_text(chat_input, conversation, user_msg_id)

    # 5. Strandsでチャット実行
    result = agent(user_message)

    # 6. 結果を既存形式に変換（リファクタリング版）
    from app.strands_integration.message_converter import strands_result_to_message_model
    
    assistant_message = strands_result_to_message_model(result, user_msg_id, bot)

    # 7. 会話更新・保存
    _update_conversation_with_strands_result(
        conversation, user_msg_id, assistant_message, result
    )
    store_conversation(user.id, conversation)

    return conversation, assistant_message


def _get_bedrock_model_id(model_name: str) -> str:
    """モデル名をBedrock model IDに変換"""
    import os
    from app.bedrock import get_model_id
    
    bedrock_region = os.environ.get("BEDROCK_REGION", "us-east-1")
    enable_cross_region = os.environ.get("ENABLE_BEDROCK_CROSS_REGION_INFERENCE", "false").lower() == "true"
    
    return get_model_id(
        model_name, 
        bedrock_region=bedrock_region,
        enable_cross_region=enable_cross_region
    )


def _create_callback_handler(on_stream, on_thinking, on_tool_result, on_reasoning):
    """コールバックハンドラー作成"""
    
    # Track streamed content to avoid duplicates
    streamed_content = set()

    def callback_handler(**kwargs):
        if "data" in kwargs and on_stream:
            data = kwargs["data"]
            # Only stream if we haven't seen this exact content before
            if data not in streamed_content:
                streamed_content.add(data)
                on_stream(data)
        elif "current_tool_use" in kwargs and on_thinking:
            on_thinking(kwargs["current_tool_use"])
        elif "reasoning" in kwargs and on_reasoning:
            on_reasoning(kwargs.get("reasoningText", ""))

    return callback_handler


def _get_user_message_text(
    chat_input: ChatInput, conversation: ConversationModel, user_msg_id: str
) -> str:
    """ユーザーメッセージのテキストを取得"""
    user_message = conversation.message_map[user_msg_id]
    for content in user_message.content:
        if hasattr(content, "content_type") and content.content_type == "text":
            return content.body
    return "Hello"


def _update_conversation_with_strands_result(
    conversation: ConversationModel,
    user_msg_id: str,
    assistant_message: MessageModel,
    result,
):
    """会話をStrands結果で更新"""
    from ulid import ULID

    # 新しいアシスタントメッセージIDを生成
    assistant_msg_id = str(ULID())

    # 会話マップに追加
    conversation.message_map[assistant_msg_id] = assistant_message
    conversation.message_map[user_msg_id].children.append(assistant_msg_id)
    conversation.last_message_id = assistant_msg_id

    # 価格を更新（Strandsの結果から取得）
    if hasattr(result, 'usage') and result.usage:
        # Strandsの使用量情報から価格を計算
        from app.bedrock import calculate_price
        try:
            price = calculate_price(
                model_name=model_name,
                input_tokens=getattr(result.usage, 'input_tokens', 0),
                output_tokens=getattr(result.usage, 'output_tokens', 0)
            )
            conversation.total_price += price
        except Exception as e:
            logger.warning(f"Could not calculate price: {e}")
            conversation.total_price += 0.001  # Fallback
    else:
        conversation.total_price += 0.001  # Fallback
