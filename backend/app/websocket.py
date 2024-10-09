import json
import logging
import os
import traceback
from datetime import datetime
from decimal import Decimal as decimal

import boto3
from app.agents.agent import AgentMessageModel, AgentRunner
from app.agents.agent import OnStopInput as AgentOnStopInput
from app.agents.tools.knowledge import create_knowledge_tool
from app.agents.utils import get_tool_by_name
from app.auth import verify_token
from app.bedrock import (
    ConverseApiRequest,
    ConverseApiToolResult,
    compose_args_for_converse_api,
)
from app.repositories.conversation import RecordNotFoundError, store_conversation
from app.repositories.models.conversation import (
    AgentToolUseContentModel,
    ChunkModel,
    ContentModel,
    ConversationModel,
    MessageModel,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import ChatInput
from app.stream import ConverseApiStreamHandler, OnStopInput
from app.usecases.bot import modify_bot_last_used_time
from app.usecases.chat import insert_knowledge, prepare_conversation, trace_to_root
from app.utils import get_current_time
from app.vector_search import (
    filter_used_results,
    get_source_link,
    search_related_docs,
    to_guardrails_grounding_source,
)
from boto3.dynamodb.conditions import Attr, Key
from ulid import ULID

WEBSOCKET_SESSION_TABLE_NAME = os.environ["WEBSOCKET_SESSION_TABLE_NAME"]

dynamodb_client = boto3.resource("dynamodb")
table = dynamodb_client.Table(WEBSOCKET_SESSION_TABLE_NAME)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def on_stream(token: str, gatewayapi, connection_id: str) -> None:
    # Send completion
    data_to_send = json.dumps(dict(status="STREAMING", completion=token)).encode(
        "utf-8"
    )
    gatewayapi.post_to_connection(ConnectionId=connection_id, Data=data_to_send)


def on_stop(
    arg: OnStopInput,
    gatewayapi,
    connection_id: str,
    user_id: str,
    conversation: ConversationModel,
    chat_input: ChatInput,
    user_msg_id: str,
    bot: BotModel | None = None,
    search_results=[],
) -> None:
    if chat_input.continue_generate:
        # For continue generate
        conversation.message_map[conversation.last_message_id].content[
            0
        ].body += arg.full_token  # type: ignore[operator]
    else:
        used_chunks = None
        if bot and bot.display_retrieved_chunks:
            if len(search_results) > 0:
                used_chunks = []
                for r in filter_used_results(arg.full_token, search_results):
                    content_type, source_link = get_source_link(r.source)
                    used_chunks.append(
                        ChunkModel(
                            content=r.content,
                            content_type=content_type,
                            source=source_link,
                            rank=r.rank,
                        )
                    )

        # Append entire completion as the last message
        assistant_msg_id = str(ULID())
        message = MessageModel(
            role="assistant",
            content=[
                ContentModel(
                    content_type="text",
                    body=arg.full_token,
                    media_type=None,
                    file_name=None,
                )
            ],
            model=chat_input.message.model,
            children=[],
            parent=user_msg_id,
            create_time=get_current_time(),
            feedback=None,
            used_chunks=used_chunks,
            thinking_log=None,
        )
        conversation.message_map[assistant_msg_id] = message
        conversation.message_map[user_msg_id].children.append(assistant_msg_id)
        conversation.last_message_id = assistant_msg_id

    conversation.total_price += arg.price

    conversation.should_continue = arg.stop_reason == "max_tokens"
    # Store conversation before finish streaming so that front-end can avoid 404 issue
    store_conversation(user_id, conversation)
    last_data_to_send = json.dumps(
        dict(status="STREAMING_END", completion="", stop_reason=arg.stop_reason)
    ).encode("utf-8")
    gatewayapi.post_to_connection(ConnectionId=connection_id, Data=last_data_to_send)


def on_agent_thinking(
    agent_log: list[AgentMessageModel], gatewayapi, connection_id: str
):
    assert len(agent_log) > 0
    assert agent_log[-1].role == "assistant"
    to_send = dict()
    for c in agent_log[-1].content:
        assert type(c.body) == AgentToolUseContentModel
        to_send[c.body.tool_use_id] = {
            "name": c.body.name,
            "input": c.body.input,
        }

    data_to_send = json.dumps(dict(status="AGENT_THINKING", log=to_send)).encode(
        "utf-8"
    )
    gatewayapi.post_to_connection(ConnectionId=connection_id, Data=data_to_send)


def on_agent_tool_result(
    tool_result: ConverseApiToolResult, gatewayapi, connection_id: str
):
    to_send = {
        "toolUseId": tool_result["toolUseId"],
        "status": tool_result["status"],  # type: ignore
        "content": tool_result["content"],
    }
    data_to_send = json.dumps(dict(status="AGENT_TOOL_RESULT", result=to_send)).encode(
        "utf-8"
    )
    gatewayapi.post_to_connection(ConnectionId=connection_id, Data=data_to_send)


def on_agent_stop(
    arg: AgentOnStopInput,
    gatewayapi,
    connection_id: str,
    user_id: str,
    conversation: ConversationModel,
    chat_input: ChatInput,
    user_msg_id: str,
):
    # Append entire completion as the last message
    assistant_msg_id = str(ULID())
    message = MessageModel(
        role="assistant",
        content=[
            ContentModel(
                content_type="text",
                body=arg.last_response["output"]["message"]["content"][0]["text"],  # type: ignore
                media_type=None,
                file_name=None,
            )
        ],
        model=chat_input.message.model,
        children=[],
        parent=user_msg_id,
        create_time=get_current_time(),
        feedback=None,
        used_chunks=None,
        thinking_log=arg.thinking_conversation,
    )
    conversation.message_map[assistant_msg_id] = message
    conversation.message_map[user_msg_id].children.append(assistant_msg_id)
    conversation.last_message_id = assistant_msg_id
    conversation.total_price += arg.price

    # Agent not support continue generate
    # conversation.should_continue = arg.stop_reason == "max_tokens"

    store_conversation(user_id, conversation)
    last_data_to_send = json.dumps(
        dict(status="STREAMING_END", completion="", stop_reason=arg.stop_reason)
    ).encode("utf-8")
    gatewayapi.post_to_connection(ConnectionId=connection_id, Data=last_data_to_send)


def process_chat_input(
    user_id: str, chat_input: ChatInput, gatewayapi, connection_id: str
) -> dict:
    """Process chat input and send the message to the client."""
    logger.info(f"Received chat input: {chat_input}")

    try:
        user_msg_id, conversation, bot = prepare_conversation(user_id, chat_input)
    except RecordNotFoundError:
        if chat_input.bot_id:
            gatewayapi.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps(
                    dict(
                        status="ERROR",
                        reason="bot_not_found",
                    )
                ).encode("utf-8"),
            )
            return {"statusCode": 404, "body": f"bot {chat_input.bot_id} not found."}
        else:
            return {"statusCode": 400, "body": "Invalid request."}

    if bot and bot.is_agent_enabled():
        logger.info("Bot has agent tools. Using agent for response.")
        tools = [get_tool_by_name(t.name) for t in bot.agent.tools]

        if bot.has_knowledge():
            # Add knowledge tool
            knowledge_tool = create_knowledge_tool(bot, chat_input.message.model)
            tools.append(knowledge_tool)

        runner = AgentRunner(
            bot=bot,
            tools=tools,
            model=chat_input.message.model,
            on_thinking=lambda log: on_agent_thinking(log, gatewayapi, connection_id),
            on_tool_result=lambda result: on_agent_tool_result(
                result, gatewayapi, connection_id
            ),
            on_stop=lambda arg: on_agent_stop(
                arg,
                gatewayapi,
                connection_id,
                user_id,
                conversation,
                chat_input,
                user_msg_id,
            ),
        )
        message_map = conversation.message_map
        messages = trace_to_root(
            node_id=conversation.message_map[user_msg_id].parent,
            message_map=message_map,
        )
        messages.append(chat_input.message)  # type: ignore
        _ = runner.run(messages)

        return {"statusCode": 200, "body": "Message sent."}

    message_map = conversation.message_map
    search_results = []
    if bot and bot.has_knowledge():
        gatewayapi.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(
                dict(
                    status="FETCHING_KNOWLEDGE",
                )
            ).encode("utf-8"),
        )

        # Fetch most related documents from vector store
        # NOTE: Currently embedding not support multi-modal. For now, use the last text content.
        query: str = conversation.message_map[user_msg_id].content[-1].body  # type: ignore[assignment]
        search_results = search_related_docs(bot=bot, query=query)
        logger.info(f"Search results from vector store: {search_results}")

        # Insert contexts to instruction
        conversation_with_context = insert_knowledge(
            conversation, search_results, display_citation=bot.display_retrieved_chunks
        )
        message_map = conversation_with_context.message_map

    messages = trace_to_root(
        node_id=conversation.message_map[user_msg_id].parent,
        message_map=message_map,
    )
    if not chat_input.continue_generate:
        messages.append(chat_input.message)  # type: ignore

    # Guardrails
    guardrail = bot.bedrock_guardrails if bot else None
    grounding_source = None
    if guardrail and guardrail.is_guardrail_enabled:
        grounding_source = to_guardrails_grounding_source(search_results)

    args = compose_args_for_converse_api(
        messages=messages,
        model=chat_input.message.model,
        instruction=(
            message_map["instruction"].content[0].body
            if "instruction" in message_map
            else None  # type: ignore[union-attr]
        ),
        generation_params=(bot.generation_params if bot else None),
        grounding_source=grounding_source,
        guardrail=guardrail,
    )

    stream_handler = ConverseApiStreamHandler(
        model=chat_input.message.model,
        on_stream=lambda token: on_stream(token, gatewayapi, connection_id),
        on_stop=lambda arg: on_stop(
            arg,
            gatewayapi,
            connection_id,
            user_id,
            conversation,
            chat_input,
            user_msg_id,
            bot,
            search_results,
        ),
    )
    try:
        for _ in stream_handler.run(args):
            # `StreamHandler.run` returns a generator, so need to iterate
            ...
    except Exception as e:
        logger.error(f"Failed to run stream handler: {e}")
        return {
            "statusCode": 500,
            "body": f"Failed to run stream handler: {e}",
        }

    # Update bot last used time
    if chat_input.bot_id:
        logger.info("Bot id is provided. Updating bot last used time.")
        modify_bot_last_used_time(user_id, chat_input.bot_id)

    return {"statusCode": 200, "body": "Message sent."}


def handler(event, context):
    logger.info(f"Received event: {event}")
    route_key = event["requestContext"]["routeKey"]

    if route_key == "$connect":
        return {"statusCode": 200, "body": "Connected."}
    elif route_key == "$disconnect":
        return {"statusCode": 200, "body": "Disconnected."}

    connection_id = event["requestContext"]["connectionId"]
    domain_name = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    endpoint_url = f"https://{domain_name}/{stage}"
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint_url)

    now = datetime.now()
    expire = int(now.timestamp()) + 60 * 2  # 2 minute from now
    body = json.loads(event["body"])
    step = body.get("step")

    try:
        # API Gateway (websocket) has hard limit of 32KB per message, so if the message is larger than that,
        # need to concatenate chunks and send as a single full message.
        # To do that, we store the chunks in DynamoDB and when the message is complete, send it to SNS.
        # The life cycle of the message is as follows:
        # 1. Client sends `START` message to the WebSocket API.
        # 2. This handler receives the `Session started` message.
        # 3. Client sends message parts to the WebSocket API.
        # 4. This handler receives the message parts and appends them to the item in DynamoDB with index.
        # 5. Client sends `END` message to the WebSocket API.
        # 6. This handler receives the `END` message, concatenates the parts and sends the message to Bedrock.
        if step == "START":
            token = body["token"]
            try:
                # Verify JWT token
                decoded = verify_token(token)
            except Exception as e:
                logger.error(f"Invalid token: {e}")
                return {"statusCode": 403, "body": "Invalid token."}
            user_id = decoded["sub"]

            # Store user id
            response = table.put_item(
                Item={
                    "ConnectionId": connection_id,
                    # Store as zero
                    "MessagePartId": decimal(0),
                    "UserId": user_id,
                    "expire": expire,
                }
            )
            return {"statusCode": 200, "body": "Session started."}
        elif step == "END":
            # Retrieve user id
            response = table.query(
                KeyConditionExpression=Key("ConnectionId").eq(connection_id),
                FilterExpression=Attr("UserId").exists(),
            )
            user_id = response["Items"][0]["UserId"]

            # Concatenate the message parts
            message_parts = []
            last_evaluated_key = None

            while True:
                if last_evaluated_key:
                    response = table.query(
                        KeyConditionExpression=Key("ConnectionId").eq(connection_id)
                        # Zero is reserved for user id, so start from 1
                        & Key("MessagePartId").gte(1),
                        ExclusiveStartKey=last_evaluated_key,
                    )
                else:
                    response = table.query(
                        KeyConditionExpression=Key("ConnectionId").eq(connection_id)
                        & Key("MessagePartId").gte(1),
                    )

                message_parts.extend(response["Items"])

                if "LastEvaluatedKey" in response:
                    last_evaluated_key = response["LastEvaluatedKey"]
                else:
                    break

            logger.info(f"Number of message chunks: {len(message_parts)}")
            message_parts.sort(key=lambda x: x["MessagePartId"])
            full_message = "".join(item["MessagePart"] for item in message_parts)

            # Process the concatenated full message
            chat_input = ChatInput(**json.loads(full_message))
            return process_chat_input(
                user_id=user_id,
                chat_input=chat_input,
                gatewayapi=gatewayapi,
                connection_id=connection_id,
            )
        else:
            # Store the message part of full message
            # Zero is reserved for user id, so start from 1
            part_index = body["index"] + 1
            message_part = body["part"]

            # Store the message part with its index
            table.put_item(
                Item={
                    "ConnectionId": connection_id,
                    "MessagePartId": decimal(part_index),
                    "MessagePart": message_part,
                    "expire": expire,
                }
            )
            return {"statusCode": 200, "body": "Message part received."}

    except Exception as e:
        logger.error(f"Operation failed: {e}")
        logger.error("".join(traceback.format_tb(e.__traceback__)))
        gatewayapi.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({"status": "ERROR", "reason": str(e)}).encode("utf-8"),
        )
        return {"statusCode": 500, "body": str(e)}
