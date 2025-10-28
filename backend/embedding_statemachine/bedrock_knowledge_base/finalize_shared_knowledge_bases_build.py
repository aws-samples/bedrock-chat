import os
from typing import List, TypedDict

import boto3
from app.repositories.custom_bot import update_knowledge_base_id

BEDROCK_REGION = os.environ.get("BEDROCK_REGION")

cfn = boto3.client(
    service_name="cloudformation",
    region_name=BEDROCK_REGION,
)


class QueuedBot(TypedDict):
    user_id: str
    bot_id: str


class KnowledgeBase(TypedDict):
    knowledge_base_id: str
    data_source_ids: list[str]
    queued_bots: list[QueuedBot]


class BotFilesDiff(TypedDict):
    OwnerUserId: str
    BotId: str
    Added: list[str]
    Unchanged: list[str]
    Deleted: list[str]


class DataSource(TypedDict):
    KnowledgeBaseId: str
    DataSourceId: str
    FilesDiffs: list[BotFilesDiff]


def handler(event, context):
    queued_bots = event["QueuedBots"]
    shared_knowledge_bases = event["SharedKnowledgeBases"]

    # Note: stack naming rule is defined on:
    # cdk/bin/bedrock-shared-knowledge-bases.ts
    stack_name = "BrChatSharedKbStack"

    response = cfn.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0].get("Outputs")
    if not outputs:
        raise ValueError(f"No outputs found in CloudFormation stack '{stack_name}'")

    stack_outputs = dict(
        (output["OutputKey"], output["OutputValue"])
        for output in outputs
        if "OutputKey" in output and "OutputValue" in output
    )

    knowledge_bases: dict[str, KnowledgeBase] = {}

    for shared_knowledge_base in shared_knowledge_bases:
        knowledge_base_hash = shared_knowledge_base["KnowledgeBaseHash"]
        knowledge_base_id = stack_outputs.get(f"KnowledgeBaseId{knowledge_base_hash}")
        if knowledge_base_id:
            knowledge_bases[knowledge_base_hash] = {
                "knowledge_base_id": knowledge_base_id,
                "data_source_ids": [
                    value
                    for key, value in stack_outputs.items()
                    if key.startswith(f"DataSource{knowledge_base_hash}")
                ],
                "queued_bots": [],
            }

    data_sources: list[DataSource] = []

    for queued_bot in queued_bots:
        knowledge_base_hash = queued_bot.get("KnowledgeBaseHash")
        if knowledge_base_hash and knowledge_base_hash in knowledge_bases:
            knowledge_base = knowledge_bases[knowledge_base_hash]
            if "FilesDiff" in queued_bot:
                queued_bot["DataSources"] = [
                    {
                        "KnowledgeBaseId": knowledge_base["knowledge_base_id"],
                        "DataSourceId": data_source_id,
                    }
                    for data_source_id in knowledge_base["data_source_ids"]
                ]

            else:
                data_sources.extend(
                    {
                        "KnowledgeBaseId": knowledge_base["knowledge_base_id"],
                        "DataSourceId": data_source_id,
                        "FilesDiffs": [],
                    }
                    for data_source_id in knowledge_base["data_source_ids"]
                )
                pass

            knowledge_base["queued_bots"].append(
                {
                    "user_id": queued_bot["OwnerUserId"],
                    "bot_id": queued_bot["BotId"],
                }
            )

    for knowledge_base in knowledge_bases.values():
        for queued_bot in knowledge_base["queued_bots"]:
            update_knowledge_base_id(
                user_id=queued_bot["user_id"],
                bot_id=queued_bot["bot_id"],
                knowledge_base_id=knowledge_base["knowledge_base_id"],
                data_source_ids=knowledge_base["data_source_ids"],
            )

    return {
        "QueuedBots": queued_bots,
        "SharedKnowledgeBases": shared_knowledge_bases,
        "DataSources": data_sources,
        **(
            {
                "Lock": event["Lock"],
            }
            if "Lock" in event
            else {}
        ),
    }
