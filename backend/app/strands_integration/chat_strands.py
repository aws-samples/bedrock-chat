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
logger.setLevel(logging.DEBUG)


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
    logger.debug(f"[STRANDS_CHAT] Starting chat_with_strands for user: {user.id}")
    logger.debug(f"[STRANDS_CHAT] Chat input: conversation_id={chat_input.conversation_id}, enable_reasoning={chat_input.enable_reasoning}")
    
    import time
    start_time = time.time()
    from app.repositories.conversation import store_conversation
    from app.repositories.models.conversation import MessageModel, TextContentModel
    from app.usecases.chat import prepare_conversation
    from app.utils import get_current_time
    from strands import Agent
    from strands.models import BedrockModel
    from ulid import ULID

    # 1. Reuse existing conversation preparation logic
    logger.debug(f"[STRANDS_CHAT] Step 1: Preparing conversation...")
    prep_start = time.time()
    user_msg_id, conversation, bot = prepare_conversation(user, chat_input)
    prep_time = time.time() - prep_start
    logger.debug(f"[STRANDS_CHAT] Step 1 completed in {prep_time:.3f}s - user_msg_id: {user_msg_id}, bot: {bot.id if bot else None}")

    # 2. Create Strands agent (refactored version)
    logger.debug(f"[STRANDS_CHAT] Step 2: Creating Strands agent...")
    agent_start = time.time()
    from app.strands_integration.agent_factory import create_strands_agent
    
    # Get model name from chat_input
    model_name = chat_input.message.model if chat_input.message.model else "claude-v3.5-sonnet"
    logger.debug(f"[STRANDS_CHAT] Using model: {model_name}, reasoning: {chat_input.enable_reasoning}")
    agent = create_strands_agent(bot, user, model_name, enable_reasoning=chat_input.enable_reasoning)
    agent_time = time.time() - agent_start
    logger.debug(f"[STRANDS_CHAT] Step 2 completed in {agent_time:.3f}s - agent created")
    
    # Log reasoning functionality status
    if chat_input.enable_reasoning:
        logger.info("Reasoning functionality enabled in agent creation")
    else:
        logger.info("Reasoning functionality disabled")

    # 3. Setup callback handlers
    logger.debug(f"[STRANDS_CHAT] Step 3: Setting up callback handlers...")
    callback_start = time.time()
    if any([on_stream, on_thinking, on_tool_result, on_reasoning]):
        logger.debug(f"[STRANDS_CHAT] Callbacks enabled - stream: {on_stream is not None}, thinking: {on_thinking is not None}, tool: {on_tool_result is not None}, reasoning: {on_reasoning is not None}")
        agent.callback_handler = _create_callback_handler(
            on_stream, on_thinking, on_tool_result, on_reasoning
        )
    else:
        logger.debug(f"[STRANDS_CHAT] No callbacks provided")
    callback_time = time.time() - callback_start
    logger.debug(f"[STRANDS_CHAT] Step 3 completed in {callback_time:.3f}s")

    # 4. Get user message content
    logger.debug(f"[STRANDS_CHAT] Step 4: Getting user message content...")
    msg_start = time.time()
    user_message = _get_user_message_content(chat_input, conversation, user_msg_id)
    msg_time = time.time() - msg_start
    logger.debug(f"[STRANDS_CHAT] Step 4 completed in {msg_time:.3f}s - message type: {type(user_message)}, length: {len(str(user_message))}")

    # 5. Execute chat with Strands
    logger.debug(f"[STRANDS_CHAT] Step 5: Executing chat with Strands agent...")
    exec_start = time.time()
    result = agent(user_message)
    exec_time = time.time() - exec_start
    logger.debug(f"[STRANDS_CHAT] Step 5 completed in {exec_time:.3f}s - result type: {type(result)}")
    logger.debug(f"[STRANDS_CHAT] Result attributes: {[attr for attr in dir(result) if not attr.startswith('_')]}")

    # 6. Convert result to existing format (refactored version)
    logger.debug(f"[STRANDS_CHAT] Step 6: Converting result to message model...")
    convert_start = time.time()
    from app.strands_integration.message_converter import strands_result_to_message_model
    
    assistant_message = strands_result_to_message_model(result, user_msg_id, bot)
    convert_time = time.time() - convert_start
    logger.debug(f"[STRANDS_CHAT] Step 6 completed in {convert_time:.3f}s - message role: {assistant_message.role}, content count: {len(assistant_message.content)}")

    # 7. Update and save conversation
    logger.debug(f"[STRANDS_CHAT] Step 7: Updating conversation and saving to DynamoDB...")
    update_start = time.time()
    _update_conversation_with_strands_result(
        conversation, user_msg_id, assistant_message, result
    )
    update_time = time.time() - update_start
    logger.debug(f"[STRANDS_CHAT] Step 7a (update) completed in {update_time:.3f}s")
    
    save_start = time.time()
    store_conversation(user.id, conversation)
    save_time = time.time() - save_start
    logger.debug(f"[STRANDS_CHAT] Step 7b (save) completed in {save_time:.3f}s")
    
    total_time = time.time() - start_time
    logger.debug(f"[STRANDS_CHAT] Total chat_with_strands completed in {total_time:.3f}s")

    return conversation, assistant_message


def _get_bedrock_model_id(model_name: str) -> str:
    """Convert model name to Bedrock model ID"""
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
    """Create callback handler"""
    
    # Track streamed content to avoid duplicates
    streamed_content = set()

    def callback_handler(**kwargs):
        logger.debug(f"[STRANDS_CALLBACK] Callback triggered with keys: {list(kwargs.keys())}")
        
        if "data" in kwargs and on_stream:
            data = kwargs["data"]
            logger.debug(f"[STRANDS_CALLBACK] Stream data received: {len(data)} chars")
            # Only stream if we haven't seen this exact content before
            if data not in streamed_content:
                streamed_content.add(data)
                on_stream(data)
            else:
                logger.debug(f"[STRANDS_CALLBACK] Duplicate stream data ignored")
        elif "current_tool_use" in kwargs and on_thinking:
            logger.debug(f"[STRANDS_CALLBACK] Thinking event received")
            on_thinking(kwargs["current_tool_use"])
        elif "reasoning" in kwargs and on_reasoning:
            reasoning_text = kwargs.get("reasoningText", "")
            logger.debug(f"[STRANDS_CALLBACK] Reasoning received: {len(reasoning_text)} chars")
            on_reasoning(reasoning_text)
        else:
            logger.debug(f"[STRANDS_CALLBACK] Unhandled callback: {kwargs}")

    return callback_handler


def _get_user_message_content(
    chat_input: ChatInput, conversation: ConversationModel, user_msg_id: str
):
    """Get user message content (multimodal support)"""
    user_message = conversation.message_map[user_msg_id]
    
    # Process multimodal content with Strands
    content_parts = []
    
    for content in user_message.content:
        if hasattr(content, "content_type"):
            if content.content_type == "text":
                content_parts.append({"text": content.body})
            elif content.content_type == "attachment":
                # Process attachment - handle as text
                try:
                    import base64
                    decoded_content = base64.b64decode(content.body).decode('utf-8', errors='ignore')
                    content_parts.append({"text": f"[Attachment: {content.file_name}]\n{decoded_content}"})
                except Exception as e:
                    logger.warning(f"Could not process attachment {content.file_name}: {e}")
                    content_parts.append({"text": f"[Attachment: {content.file_name} - processing error]"})
            elif content.content_type == "image":
                # Process image content - convert to Strands image format
                try:
                    if hasattr(content, 'media_type') and content.media_type:
                        # Process image data
                        image_format = content.media_type.split('/')[-1]  # e.g., "image/jpeg" -> "jpeg"
                        
                        # Determine if content.body is already in bytes format or base64 encoded
                        if isinstance(content.body, bytes):
                            image_data = content.body
                        else:
                            # Case of base64 encoded string
                            import base64
                            image_data = base64.b64decode(content.body)
                        
                        content_parts.append({
                            "image": {
                                "format": image_format,
                                "source": {"bytes": image_data}
                            }
                        })
                    else:
                        # Fallback: process as text
                        content_parts.append({"text": f"[Image attachment: {getattr(content, 'file_name', 'image')}]"})
                except Exception as e:
                    logger.warning(f"Could not process image content: {e}")
                    content_parts.append({"text": f"[Image attachment - processing error: {e}]"})
    
    # Return as string for single text content
    if len(content_parts) == 1 and "text" in content_parts[0]:
        return content_parts[0]["text"]
    
    # Return as list for multimodal content
    return content_parts if content_parts else "Hello"


def _update_conversation_with_strands_result(
    conversation: ConversationModel,
    user_msg_id: str,
    assistant_message: MessageModel,
    result,
):
    """Update conversation with Strands result"""
    from ulid import ULID

    logger.debug(f"[STRANDS_UPDATE] Starting conversation update...")
    
    # Generate new assistant message ID
    assistant_msg_id = str(ULID())
    logger.debug(f"[STRANDS_UPDATE] Generated assistant message ID: {assistant_msg_id}")

    # Add to conversation map
    conversation.message_map[assistant_msg_id] = assistant_message
    conversation.message_map[user_msg_id].children.append(assistant_msg_id)
    conversation.last_message_id = assistant_msg_id
    logger.debug(f"[STRANDS_UPDATE] Updated conversation map and last_message_id")

    # Update price (from Strands result)
    if hasattr(result, 'usage') and result.usage:
        # Calculate price from Strands usage information
        from app.bedrock import calculate_price
        try:
            # Get model name from assistant message
            model_name = assistant_message.model
            logger.debug(f"[STRANDS_UPDATE] Calculating price for model: {model_name}")
            price = calculate_price(
                model_name=model_name,
                input_tokens=getattr(result.usage, 'input_tokens', 0),
                output_tokens=getattr(result.usage, 'output_tokens', 0)
            )
            conversation.total_price += price
            logger.debug(f"[STRANDS_UPDATE] Price calculated: {price}, total: {conversation.total_price}")
        except Exception as e:
            logger.warning(f"Could not calculate price: {e}")
            conversation.total_price += 0.001  # Fallback
            logger.debug(f"[STRANDS_UPDATE] Using fallback price, total: {conversation.total_price}")
    else:
        conversation.total_price += 0.001  # Fallback
        logger.debug(f"[STRANDS_UPDATE] No usage info, using fallback price, total: {conversation.total_price}")
    
    logger.debug(f"[STRANDS_UPDATE] Conversation update completed")
