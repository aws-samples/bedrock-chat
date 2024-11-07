import logging
from copy import deepcopy
from typing import Literal, Callable

from app.agents.tools.knowledge import create_knowledge_tool
from app.agents.utils import get_tool_by_name
from app.bedrock import (
    ConverseApiToolResult,
    call_converse_api,
    compose_args_for_converse_api,
)
from app.prompt import build_rag_prompt
from app.repositories.conversation import (
    RecordNotFoundError,
    find_conversation_by_id,
    store_conversation,
)
from app.repositories.custom_bot import find_alias_by_id, store_alias
from app.repositories.models.conversation import (
    AgentMessageModel,
    ChunkModel,
    ConversationModel,
    MessageModel,
    TextContentModel,
    ToolUseContentModel,
    ToolResultContentModel,
    ToolResultContentModelBody,
)
from app.repositories.models.custom_bot import (
    BotAliasModel,
    BotModel,
    ConversationQuickStarterModel,
)
from app.routes.schemas.conversation import (
    AgentMessage,
    ChatInput,
    ChatOutput,
    Chunk,
    Conversation,
    FeedbackOutput,
    MessageOutput,
    RelatedDocumentsOutput,
    type_model_name,
    TextContent,
)
from app.stream import ConverseApiStreamHandler, OnStopInput, OnThinking
from app.usecases.bot import fetch_bot, modify_bot_last_used_time
from app.utils import get_current_time
from app.vector_search import (
    SearchResult,
    filter_used_results,
    get_source_link,
    search_related_docs,
    to_guardrails_grounding_source,
)
from ulid import ULID

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def prepare_conversation(
    user_id: str,
    chat_input: ChatInput,
) -> tuple[str, ConversationModel, BotModel | None]:
    current_time = get_current_time()
    bot = None

    try:
        # Fetch existing conversation
        conversation = find_conversation_by_id(user_id, chat_input.conversation_id)
        logger.info(f"Found conversation: {conversation}")
        parent_id = chat_input.message.parent_message_id
        if chat_input.message.parent_message_id == "system" and chat_input.bot_id:
            # The case editing first user message and use bot
            parent_id = "instruction"
        elif chat_input.message.parent_message_id is None:
            parent_id = conversation.last_message_id
        if chat_input.bot_id:
            logger.info("Bot id is provided. Fetching bot.")
            owned, bot = fetch_bot(user_id, chat_input.bot_id)
    except RecordNotFoundError:
        # The case for new conversation. Note that editing first user message is not considered as new conversation.
        logger.info(
            f"No conversation found with id: {chat_input.conversation_id}. Creating new conversation."
        )

        initial_message_map = {
            # Dummy system message, which is used for root node of the message tree.
            "system": MessageModel(
                role="system",
                content=[
                    TextContentModel(
                        content_type="text",
                        body="",
                    )
                ],
                model=chat_input.message.model,
                children=[],
                parent=None,
                create_time=current_time,
                feedback=None,
                used_chunks=None,
                thinking_log=None,
            )
        }
        parent_id = "system"
        if chat_input.bot_id:
            logger.info("Bot id is provided. Fetching bot.")
            parent_id = "instruction"
            # Fetch bot and append instruction
            owned, bot = fetch_bot(user_id, chat_input.bot_id)
            initial_message_map["instruction"] = MessageModel(
                role="instruction",
                content=[
                    TextContentModel(
                        content_type="text",
                        body=bot.instruction,
                    )
                ],
                model=chat_input.message.model,
                children=[],
                parent="system",
                create_time=current_time,
                feedback=None,
                used_chunks=None,
                thinking_log=None,
            )
            initial_message_map["system"].children.append("instruction")

            if not owned:
                try:
                    # Check alias is already created
                    find_alias_by_id(user_id, chat_input.bot_id)
                except RecordNotFoundError:
                    logger.info(
                        "Bot is not owned by the user. Creating alias to shared bot."
                    )
                    # Create alias item
                    store_alias(
                        user_id,
                        BotAliasModel(
                            id=bot.id,
                            title=bot.title,
                            description=bot.description,
                            original_bot_id=chat_input.bot_id,
                            create_time=current_time,
                            last_used_time=current_time,
                            is_pinned=False,
                            sync_status=bot.sync_status,
                            has_knowledge=bot.has_knowledge(),
                            has_agent=bot.is_agent_enabled(),
                            conversation_quick_starters=(
                                []
                                if bot.conversation_quick_starters is None
                                else [
                                    ConversationQuickStarterModel(
                                        title=starter.title,
                                        example=starter.example,
                                    )
                                    for starter in bot.conversation_quick_starters
                                ]
                            ),
                        ),
                    )

        # Create new conversation
        conversation = ConversationModel(
            id=chat_input.conversation_id,
            title="New conversation",
            total_price=0.0,
            create_time=current_time,
            message_map=initial_message_map,
            last_message_id="",
            bot_id=chat_input.bot_id,
            should_continue=False,
        )

    # Append user chat input to the conversation
    if not chat_input.continue_generate:
        new_message = MessageModel.from_message_input(chat_input.message)
        new_message.parent = parent_id
        new_message.create_time = current_time

        if chat_input.message.message_id:
            message_id = chat_input.message.message_id
        else:
            message_id = str(ULID())

        conversation.message_map[message_id] = new_message
        conversation.message_map[parent_id].children.append(message_id)  # type: ignore

    # If the "Generate continue" button is pressed, a new_message is not generated.
    else:
        message_id = (
            conversation.message_map[conversation.last_message_id].parent
            or "instruction"
        )

    return (message_id, conversation, bot)


def trace_to_root(
    node_id: str | None, message_map: dict[str, MessageModel]
) -> list[AgentMessageModel]:
    """Trace message map from leaf node to root node."""
    result: list[AgentMessageModel] = []
    if not node_id or node_id == "system":
        node_id = "instruction" if "instruction" in message_map else "system"

    current_node = message_map.get(node_id)
    while current_node:
        result.append(AgentMessageModel.from_message_model(message=current_node))
        if current_node.thinking_log:
            result.extend(
                log
                for log in reversed(current_node.thinking_log)
                if any(
                    isinstance(content, ToolUseContentModel)
                    or isinstance(content, ToolResultContentModel)
                    for content in log.content
                )
            )

        parent_id = current_node.parent
        if parent_id is None:
            break
        current_node = message_map.get(parent_id)

    return result[::-1]


def insert_knowledge(
    conversation: ConversationModel,
    search_results: list[SearchResult],
    display_citation: bool = True,
) -> ConversationModel:
    """Insert knowledge to the conversation."""
    if len(search_results) == 0:
        return conversation

    conversation_with_context = deepcopy(conversation)
    content = conversation_with_context.message_map["instruction"].content[0]
    if isinstance(content, TextContentModel):
        inserted_prompt = build_rag_prompt(
            conversation,
            search_results,
            display_citation,
        )
        logger.info(f"Inserted prompt: {inserted_prompt}")

        content.body = inserted_prompt

    return conversation_with_context


def chat(
    user_id: str,
    chat_input: ChatInput,
    on_stream: Callable[[str], None] | None = None,
    on_fetching_knowledge: Callable[[], None] | None = None,
    on_stop: Callable[[OnStopInput], None] | None = None,
    on_thinking: Callable[[OnThinking], None] | None = None,
    on_tool_result: Callable[[ConverseApiToolResult], None] | None = None,
) -> tuple[ConversationModel, MessageModel]:
    user_msg_id, conversation, bot = prepare_conversation(user_id, chat_input)

    tools = (
        {t.name: get_tool_by_name(t.name) for t in bot.agent.tools}
        if bot and bot.is_agent_enabled()
        else {}
    )

    message_map = conversation.message_map
    search_results: list[SearchResult] = []
    if bot and bot.has_knowledge():
        if bot.is_agent_enabled():
            # Add knowledge tool
            knowledge_tool = create_knowledge_tool(bot, chat_input.message.model)
            tools[knowledge_tool.name] = knowledge_tool

        else:
            if on_fetching_knowledge:
                on_fetching_knowledge()

            # Fetch most related documents from vector store
            # NOTE: Currently embedding not support multi-modal. For now, use the last content.
            content = conversation.message_map[user_msg_id].content[-1]
            if isinstance(content, TextContentModel):
                search_results = search_related_docs(bot=bot, query=content.body)
                logger.info(f"Search results from vector store: {search_results}")

                # Insert contexts to instruction
                conversation_with_context = insert_knowledge(
                    conversation,
                    search_results,
                    display_citation=bot.display_retrieved_chunks,
                )
                message_map = conversation_with_context.message_map

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

    if continue_generate:
        message_for_continue_generate = AgentMessageModel.from_message_model(
            message=message_map[conversation.last_message_id],
        )

    else:
        messages.append(
            AgentMessageModel.from_message_model(message=message_map[user_msg_id]),
        )
        message_for_continue_generate = None

    instruction: str | None = (
        message_map["instruction"].content[0].body  # type: ignore
        if "instruction" in message_map
        else None
    )

    generation_params = bot.generation_params if bot else None

    # Guardrails
    guardrail = bot.bedrock_guardrails if bot else None
    grounding_source = None
    if guardrail and guardrail.is_guardrail_enabled:
        grounding_source = to_guardrails_grounding_source(search_results)

    stream_handler = ConverseApiStreamHandler(
        model=chat_input.message.model,
        instruction=instruction,
        generation_params=generation_params,
        guardrail=guardrail,
        grounding_source=grounding_source,
        tools=tools,
        on_stream=on_stream,
        on_thinking=on_thinking,
    )

    thinking_log: list[AgentMessageModel] = []
    while True:
        result = stream_handler.run(
            messages=messages,
            message_for_continue_generate=message_for_continue_generate,
        )

        message = result["message"]
        stop_reason = result["stop_reason"]

        # Used chunks for RAG generation
        used_chunks: list[ChunkModel] | None = None
        if bot and bot.display_retrieved_chunks:
            if not bot.is_agent_enabled() and len(search_results) > 0:
                reply_txt = (
                    message.content[0].body
                    if len(message.content) > 0
                    and isinstance(message.content[0], TextContentModel)
                    else ""
                )

                used_chunks = []
                for r in filter_used_results(reply_txt, search_results):
                    content_type, source_link = get_source_link(r.source)
                    used_chunks.append(
                        ChunkModel(
                            content=r.content,
                            content_type=content_type,
                            source=source_link,
                            rank=r.rank,
                        )
                    )

        message.used_chunks = used_chunks

        conversation.total_price += result["price"]
        conversation.should_continue = stop_reason == "max_tokens"

        if stop_reason != "tool_use":
            message.parent = user_msg_id

            if len(thinking_log) > 0:
                message.thinking_log = thinking_log

            if chat_input.continue_generate:
                # For continue generate
                if len(thinking_log) == 0:
                    assistant_msg_id = conversation.last_message_id
                    conversation.message_map[assistant_msg_id] = message
                    break

                else:
                    old_assistant_msg_id = conversation.last_message_id
                    conversation.message_map[user_msg_id].children.remove(
                        old_assistant_msg_id
                    )
                    del conversation.message_map[old_assistant_msg_id]

            # Issue id for new assistant message
            assistant_msg_id = str(ULID())
            conversation.message_map[assistant_msg_id] = message

            # Append children to parent
            conversation.message_map[user_msg_id].children.append(assistant_msg_id)
            conversation.last_message_id = assistant_msg_id
            break

        tool_use_message = AgentMessageModel.from_message_model(message=message)
        if continue_generate:
            messages[-1] = tool_use_message

            continue_generate = False
            message_for_continue_generate = None

        else:
            messages.append(tool_use_message)

        thinking_log.append(tool_use_message)

        tool_use_contents = [
            content
            for content in tool_use_message.content
            if isinstance(content, ToolUseContentModel)
        ]

        tool_results: list[ConverseApiToolResult] = []
        for content in tool_use_contents:
            tool = tools[content.body.name]
            run_result = tool.run(
                tool_use_id=content.body.tool_use_id,
                input=content.body.input,
            )

            tool_result = ConverseApiToolResult(
                toolUseId=run_result["tool_use_id"],
                content=run_result["body"],
                status="success" if run_result["succeeded"] else "error",
            )
            tool_results.append(tool_result)

            if on_tool_result:
                on_tool_result(tool_result)

        tool_result_message = AgentMessageModel(
            role="user",
            content=[
                ToolResultContentModel(
                    content_type="toolResult",
                    body=ToolResultContentModelBody.from_tool_result(result),
                )
                for result in tool_results
            ],
        )
        messages.append(tool_result_message)
        thinking_log.append(tool_result_message)

    # Store conversation before finish streaming so that front-end can avoid 404 issue
    store_conversation(user_id, conversation)

    if on_stop:
        on_stop(result)

    # Update bot last used time
    if chat_input.bot_id:
        logger.info("Bot id is provided. Updating bot last used time.")
        # Update bot last used time
        modify_bot_last_used_time(user_id, chat_input.bot_id)

    return conversation, message


def chat_output_from_message(
    conversation: ConversationModel,
    message: MessageModel,
) -> ChatOutput:
    return ChatOutput(
        conversation_id=conversation.id,
        create_time=conversation.create_time,
        message=MessageOutput(
            role=message.role,
            content=[c.to_content() for c in message.content],
            model=message.model,
            children=message.children,
            parent=message.parent,
            feedback=None,
            used_chunks=(
                [
                    Chunk(
                        content=c.content,
                        content_type=c.content_type,
                        source=c.source,
                        rank=c.rank,
                    )
                    for c in message.used_chunks
                ]
                if message.used_chunks
                else None
            ),
            thinking_log=(
                [AgentMessage.from_model(m) for m in message.thinking_log]
                if message.thinking_log
                else None
            ),
        ),
        bot_id=conversation.bot_id,
    )


def propose_conversation_title(
    user_id: str,
    conversation_id: str,
    model: type_model_name = "claude-v3-haiku",
) -> str:
    PROMPT = """Reading the conversation above, what is the appropriate title for the conversation? When answering the title, please follow the rules below:
<rules>
- Title length must be from 15 to 20 characters.
- Prefer more specific title than general. Your title should always be distinct from others.
- Return the conversation title only. DO NOT include any strings other than the title.
- Title must be in the same language as the conversation.
</rules>
"""
    # Fetch existing conversation
    conversation = find_conversation_by_id(user_id, conversation_id)

    messages = trace_to_root(
        node_id=conversation.last_message_id,
        message_map=conversation.message_map,
    )

    # Append message to generate title
    new_message = AgentMessageModel(
        role="user",
        content=[
            TextContentModel(
                content_type="text",
                body=PROMPT,
            )
        ],
    )
    messages.append(new_message)

    # Invoke Bedrock
    args = compose_args_for_converse_api(
        messages=[
            message
            for message in messages
            if not any(
                isinstance(content, ToolUseContentModel)
                or isinstance(content, ToolResultContentModel)
                for content in message.content
            )
        ],
        model=model,
    )
    response = call_converse_api(args)
    reply_txt = (
        response["output"]["message"]["content"][0]["text"]
        if "message" in response["output"]
        and len(response["output"]["message"]["content"]) > 0
        and "text" in response["output"]["message"]["content"][0]
        else ""
    )

    return reply_txt


def fetch_conversation(user_id: str, conversation_id: str) -> Conversation:
    conversation = find_conversation_by_id(user_id, conversation_id)

    message_map = {
        message_id: MessageOutput(
            role=message.role,
            content=[c.to_content() for c in message.content],
            model=message.model,
            children=message.children,
            parent=message.parent,
            feedback=(
                FeedbackOutput(
                    thumbs_up=message.feedback.thumbs_up,
                    category=message.feedback.category,
                    comment=message.feedback.comment,
                )
                if message.feedback
                else None
            ),
            used_chunks=(
                [
                    Chunk(
                        content=c.content,
                        content_type=c.content_type,
                        source=c.source,
                        rank=c.rank,
                    )
                    for c in message.used_chunks
                ]
                if message.used_chunks
                else None
            ),
            thinking_log=(
                [AgentMessage.from_model(m) for m in message.thinking_log]
                if message.thinking_log
                else None
            ),
        )
        for message_id, message in conversation.message_map.items()
    }
    # Omit instruction
    if "instruction" in message_map:
        for c in message_map["instruction"].children:
            message_map[c].parent = "system"
        message_map["system"].children = message_map["instruction"].children

        del message_map["instruction"]

    output = Conversation(
        id=conversation_id,
        title=conversation.title,
        create_time=conversation.create_time,
        last_message_id=conversation.last_message_id,
        message_map=message_map,
        bot_id=conversation.bot_id,
        should_continue=conversation.should_continue,
    )
    return output


def fetch_related_documents(
    user_id: str, chat_input: ChatInput
) -> list[RelatedDocumentsOutput] | None:
    """Retrieve related documents from vector store.
    If `display_retrieved_chunks` is disabled, return None.
    """
    if not chat_input.bot_id:
        return []

    _, bot = fetch_bot(user_id, chat_input.bot_id)
    if not bot.has_knowledge() or not bot.display_retrieved_chunks:
        return None

    content = chat_input.message.content[-1]
    chunks = (
        search_related_docs(bot=bot, query=content.body)
        if isinstance(content, TextContent)
        else []
    )

    documents = []
    for chunk in chunks:
        content_type, source_link = get_source_link(chunk.source)
        documents.append(
            RelatedDocumentsOutput(
                chunk_body=chunk.content,
                content_type=content_type,
                source_link=source_link,
                rank=chunk.rank,
            )
        )
    return documents
