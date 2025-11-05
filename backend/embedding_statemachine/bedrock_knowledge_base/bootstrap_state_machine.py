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
    """To build the information necessary for processing the embedded state machine, retrieve information about bots and shared Knowledge Bases from the database."""
    queued_bots_from_event = event.get("QueuedBots")
    if queued_bots_from_event is not None:
        # The bots to be processed were specified in the input.
        queued_bots = get_queued_bots_from_event(queued_bots_from_event)

    else:
        # Otherwise, retrieve bots with `SynsStatus of `QUEUED` from the database.
        queued_bots = get_queued_bots()

    if not queued_bots or any(
        queued_bot["sync_shared_knowledge_bases_required"] for queued_bot in queued_bots
    ):
        # If there are updates to shared Knowledge Bases, or the state machine is started without specifying a queued bot, retrieve information about the shared Knowledge Bases from the database.
        shared_knowledge_bases = find_shared_knowledge_bases()

    else:
        # Otherwise, skip the processing related to shared Knowledge Bases.
        shared_knowledge_bases = None

    return {
        "QueuedBots": [
            {
                # Bot configuration for State Machine processing
                # - Shared bots: KnowledgeBaseHash set, KnowledgeBase empty
                # - Dedicated bots: KnowledgeBase set, KnowledgeBaseHash None
                # - FilesDiff: Present when bot has specific file changes
                "OwnerUserId": queued_bot["bot"].owner_user_id,
                "BotId": queued_bot["bot"].id,
                **(
                    {
                        "FilesDiff": queued_bot["files_diff"],
                    }
                    if "files_diff" in queued_bot
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
        "SharedKnowledgeBases": (
            [
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
            ]
            if shared_knowledge_bases is not None
            else None
        ),
    }


class FilesDiff(TypedDict):
    Added: list[str]
    Unchanged: list[str]
    Deleted: list[str]


class QueuedBot(TypedDict):
    bot: BotModel
    files_diff: NotRequired[FilesDiff]
    sync_shared_knowledge_bases_required: bool


def get_queued_bots_from_event(queued_bots_from_event: list[dict]) -> list[QueuedBot]:
    result: list[QueuedBot] = []
    for queued_bot in queued_bots_from_event:
        user_id = queued_bot.get("OwnerUserId")
        bot_id = queued_bot.get("BotId")
        if user_id and bot_id:
            bot = find_bot_by_id(bot_id)
            files_diff = queued_bot.get("FilesDiff", {})
            sync_shared_knowledge_bases_required = queued_bot.get(
                "SyncSharedKnowledgeBasesRequired", True
            )

            added_files = files_diff.get("Added", [])
            unchanged_files = files_diff.get("Unchanged", [])
            deleted_files = files_diff.get("Deleted", [])
            if added_files or unchanged_files or deleted_files:
                result.append(
                    {
                        "bot": bot,
                        "files_diff": {
                            "Added": added_files,
                            "Unchanged": unchanged_files,
                            "Deleted": deleted_files,
                        },
                        "sync_shared_knowledge_bases_required": sync_shared_knowledge_bases_required,
                    }
                )

            else:
                result.append(
                    {
                        "bot": bot,
                        "sync_shared_knowledge_bases_required": sync_shared_knowledge_bases_required,
                    }
                )

    return result


def get_queued_bots() -> list[QueuedBot]:
    bots = find_queued_bots()
    return [
        {
            "bot": bot,
            "sync_shared_knowledge_bases_required": True,
        }
        for bot in bots
    ]


class SharedKnowledgeBase(TypedDict):
    knowledge_base_hash: str
    knowledge_base: BedrockKnowledgeBaseModel


def find_shared_knowledge_bases() -> list[SharedKnowledgeBase]:
    bot_table = get_bot_table_client()
    scan_params = {
        "FilterExpression": Attr("BedrockKnowledgeBase.type").eq("shared"),
    }

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
                    }

        last_evaluated_key = response.get("LastEvaluatedKey")
        if last_evaluated_key is None:
            break

        scan_params["ExclusiveStartKey"] = last_evaluated_key

    return list(knowledge_bases.values())
