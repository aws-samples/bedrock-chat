from typing import TypedDict, NotRequired
from boto3.dynamodb.conditions import Attr

from app.repositories.custom_bot import (
    find_bot_by_id,
    find_queued_bots,
    get_bot_table_client,
)
from app.repositories.models.custom_bot import BotModel
from app.repositories.models.custom_bot_kb import (
    BedrockKnowledgeBaseModel,
    calc_knowledge_base_hash,
)


def handler(event, context):
    queued_bots_from_event = event.get("QueuedBots")
    if queued_bots_from_event is not None:
        queued_bots = get_queued_bots_from_event(queued_bots_from_event)

    else:
        queued_bots = get_queued_bots()

    shared_knowledge_bases = find_shared_knowledge_bases(queued_bots)

    return {
        "QueuedBots": [
            {
                "OwnerUserId": queued_bot["bot"].owner_user_id,
                "BotId": queued_bot["bot"].id,
                **(
                    {
                        "Files": queued_bot["files"],
                    }
                    if "files" in queued_bot
                    else {}
                ),
                "Knowledge": queued_bot["bot"].knowledge.model_dump(),
                "KnowledgeBaseHash": (
                    calc_knowledge_base_hash(queued_bot["bot"].bedrock_knowledge_base)
                    if queued_bot["bot"].bedrock_knowledge_base is not None
                    else None
                ),
                "KnowledgeBase": (
                    queued_bot["bot"].bedrock_knowledge_base.model_dump(
                        exclude={
                            "knowledge_base_id",
                            "exist_knowledge_base_id",
                            "data_source_ids",
                        }
                    )
                    if queued_bot["bot"].bedrock_knowledge_base is not None
                    and queued_bot["bot"].bedrock_knowledge_base.type == "dedicated"
                    else {}
                ),
                "Guardrails": (
                    queued_bot["bot"].bedrock_guardrails.model_dump()
                    if queued_bot["bot"].bedrock_guardrails is not None
                    and queued_bot["bot"].bedrock_guardrails.is_guardrail_enabled
                    else {}
                ),
            }
            for queued_bot in queued_bots
        ],
        "SharedKnowledgeBases": {
            "KnowledgeBases": [
                {
                    "KnowledgeBaseHash": shared_knowledge_base["knowledge_base_hash"],
                    "KnowledgeBase": shared_knowledge_base["knowledge_base"].model_dump(
                        exclude={
                            "knowledge_base_id",
                            "exist_knowledge_base_id",
                            "data_source_ids",
                        }
                    ),
                }
                for shared_knowledge_base in shared_knowledge_bases
            ],
            "QueuedBotsForKnowledgeBases": [
                {
                    "KnowledgeBaseHash": shared_knowledge_base["knowledge_base_hash"],
                    "Bots": [
                        {
                            "OwnerUserId": queued_bot["bot"].owner_user_id,
                            "BotId": queued_bot["bot"].id,
                            **(
                                {
                                    "Files": queued_bot["files"],
                                }
                                if "files" in queued_bot
                                else {}
                            ),
                        }
                        for queued_bot in shared_knowledge_base["queued_bots"]
                    ],
                }
                for shared_knowledge_base in shared_knowledge_bases
            ],
        },
    }


class BotFiles(TypedDict):
    Added: list[str]
    Deleted: list[str]


class QueuedBot(TypedDict):
    bot: BotModel
    files: NotRequired[BotFiles]


def get_queued_bots_from_event(queued_bots_from_event: list[dict]) -> list[QueuedBot]:
    result: list[QueuedBot] = []
    for queued_bot in queued_bots_from_event:
        user_id = queued_bot.get("OwnerUserId")
        bot_id = queued_bot.get("BotId")
        if user_id and bot_id:
            bot = find_bot_by_id(bot_id)
            files = queued_bot.get("Files", {})

            added_files = files.get("Added", [])
            deleted_files = files.get("Deleted", [])
            if added_files or deleted_files:
                result.append(
                    {
                        "bot": bot,
                        "files": {
                            "Added": added_files,
                            "Deleted": deleted_files,
                        },
                    }
                )

            else:
                result.append(
                    {
                        "bot": bot,
                    }
                )

    return result


def get_queued_bots() -> list[QueuedBot]:
    bots = find_queued_bots()
    return [
        {
            "bot": bot,
        }
        for bot in bots
    ]


class SharedKnowledgeBase(TypedDict):
    knowledge_base_hash: str
    knowledge_base: BedrockKnowledgeBaseModel
    queued_bots: list[QueuedBot]


def find_shared_knowledge_bases(
    queued_bots: list[QueuedBot],
) -> list[SharedKnowledgeBase]:
    bot_table = get_bot_table_client()
    scan_params = {
        "FilterExpression": Attr("BedrockKnowledgeBase.type").eq("shared"),
    }

    queued_bots_dict = dict(
        (queued_bot["bot"].id, queued_bot) for queued_bot in queued_bots
    )
    knowledge_bases: dict[str, SharedKnowledgeBase] = {}
    while True:
        response = bot_table.scan(**scan_params)
        items = response["Items"]
        for item in items:
            bot = BotModel.from_dynamo_item(item)
            if bot.bedrock_knowledge_base is not None:
                knowledge_base_hash = calc_knowledge_base_hash(
                    bot.bedrock_knowledge_base
                )
                if knowledge_base_hash not in knowledge_bases:
                    knowledge_bases[knowledge_base_hash] = {
                        "knowledge_base_hash": knowledge_base_hash,
                        "knowledge_base": bot.bedrock_knowledge_base,
                        "queued_bots": [],
                    }

                queued_bot = queued_bots_dict.get(bot.id)
                if queued_bot is not None:
                    knowledge_bases[knowledge_base_hash]["queued_bots"].append(
                        queued_bot
                    )

        last_evaluated_key = response.get("LastEvaluatedKey")
        if last_evaluated_key is None:
            break

        scan_params["ExclusiveStartKey"] = last_evaluated_key

    return list(knowledge_bases.values())
