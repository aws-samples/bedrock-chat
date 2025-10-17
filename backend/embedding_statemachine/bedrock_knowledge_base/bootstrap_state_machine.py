from typing import TypedDict
from boto3.dynamodb.conditions import Key

from app.repositories.common import get_bot_table_client
from app.repositories.models.custom_bot import BotModel, BedrockKnowledgeBaseModel


def handler(event, context):
    bots = find_queued_bots()
    shared_knowledge_bases = find_shared_knowledge_bases()
    return {
        "Bots": [
            {
                "BotId": bot.id,
                "OwnerUserId": bot.owner_user_id,
                "Knowledge": bot.knowledge.model_dump(),
                "KnowledgeBaseHash": knowledge_base_hash,
                "KnowledgeBase": (
                    bot.bedrock_knowledge_base.model_dump(
                        exclude={
                            "knowledge_base_id",
                            "exist_knowledge_base_id",
                            "data_source_ids",
                        }
                    )
                    if bot.bedrock_knowledge_base is not None
                    and bot.bedrock_knowledge_base.type == "dedicated"
                    else {}
                ),
                "Guardrails": (
                    bot.bedrock_guardrails.model_dump()
                    if bot.bedrock_guardrails is not None
                    and bot.bedrock_guardrails.is_guardrail_enabled
                    else {}
                ),
            }
            for bot, knowledge_base_hash in bots
        ],
        "SharedKnowledgeBases": [
            {
                "KnowledgeBaseHash": shared_knowledge_base["knowledge_base_hash"],
                "KnowledgeBase": shared_knowledge_base["knowledge_base"].model_dump(
                    exclude={
                        "knowledge_base_id",
                        "exist_knowledge_base_id",
                        "data_source_ids",
                    }
                ),
                "Bots": [
                    {
                        "OwnerUserId": bot.owner_user_id,
                        "BotId": bot.id,
                    }
                    for bot in shared_knowledge_base["bots"]
                ],
            }
            for shared_knowledge_base in shared_knowledge_bases
        ],
    }


def find_queued_bots() -> list[tuple[BotModel, str | None]]:
    bot_table = get_bot_table_client()

    bots: list[tuple[BotModel, str | None]] = []
    query_params = {
        "IndexName": "SyncStatusIndex",
        "KeyConditionExpression": Key("SyncStatus").eq("QUEUED"),
    }
    while True:
        response = bot_table.query(**query_params)
        items = response["Items"]
        bots.extend(
            (BotModel.from_dynamo_item(item), item.get("BedrockKnowledgeBaseHash"))
            for item in items
        )

        last_evaluated_key = response.get("LastEvaluatedKey")
        if last_evaluated_key is None:
            break

        query_params["ExclusiveStartKey"] = last_evaluated_key

    return bots


class SharedKnowledgeBase(TypedDict):
    knowledge_base_hash: str
    knowledge_base: BedrockKnowledgeBaseModel
    bots: list[BotModel]


def find_shared_knowledge_bases() -> list[SharedKnowledgeBase]:
    bot_table = get_bot_table_client()

    knowledge_bases: dict[str, SharedKnowledgeBase] = {}
    query_params = {
        "IndexName": "KnowledgeBaseTypeIndex",
        "KeyConditionExpression": Key("BedrockKnowledgeBaseType").eq("shared"),
    }
    while True:
        response = bot_table.query(**query_params)
        items = response["Items"]
        for item in items:
            bot = BotModel.from_dynamo_item(item)
            knowledge_base_hash = item.get("BedrockKnowledgeBaseHash")
            if (
                bot.bedrock_knowledge_base is not None
                and knowledge_base_hash is not None
            ):
                if knowledge_base_hash not in knowledge_bases:
                    knowledge_bases[knowledge_base_hash] = {
                        "knowledge_base_hash": knowledge_base_hash,
                        "knowledge_base": bot.bedrock_knowledge_base,
                        "bots": [bot],
                    }

                else:
                    knowledge_bases[knowledge_base_hash]["bots"].append(bot)

        last_evaluated_key = response.get("LastEvaluatedKey")
        if last_evaluated_key is None:
            break

        query_params["ExclusiveStartKey"] = last_evaluated_key

    return list(knowledge_bases.values())
