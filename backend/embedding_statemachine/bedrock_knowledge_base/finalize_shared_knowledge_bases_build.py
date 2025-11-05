import os
from typing import TypedDict

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
    """Obtain the ID of the shared Knowledge Bases built by `BrChatSharedKbStack`, and update `knowledge_base_id` of the referring bots."""
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

    # Dict of Knowledge Bases built by `BrChatSharedKbStack`. Key is knowledge base hash.
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

    # Dict of data sources that require entire synchronization. Key is data source ID.
    data_sources: dict[str, DataSource] = {}

    if queued_bots:
        # If there are `QUEUED` bots, synchronize only shared Knowledge Bases that they reference.
        for queued_bot in queued_bots:
            knowledge_base_hash = queued_bot.get("KnowledgeBaseHash")
            if knowledge_base_hash and knowledge_base_hash in knowledge_bases:
                knowledge_base = knowledge_bases[knowledge_base_hash]
                if "FilesDiff" in queued_bot:
                    # Assign shared KB's DataSources to individual bot for processing in MapQueuedBots flow.
                    # This preserves bot-specific file diff information needed for:
                    # - Constructing bot-specific S3 paths (user_id/bot_id/filename)
                    # - Individual bot status tracking
                    # - Proper ingestion attribution
                    # The bot will update the shared Knowledge Base's DataSources in MapQueuedBots flow.
                    queued_bot["DataSources"] = [
                        {
                            "KnowledgeBaseId": knowledge_base["knowledge_base_id"],
                            "DataSourceId": data_source_id,
                        }
                        for data_source_id in knowledge_base["data_source_ids"]
                    ]

                else:
                    # Otherwise, the data sources to be synchronized entirely.
                    data_sources.update(
                        (
                            data_source_id,
                            {
                                "KnowledgeBaseId": knowledge_base["knowledge_base_id"],
                                "DataSourceId": data_source_id,
                                "FilesDiffs": [],
                            },
                        )
                        for data_source_id in knowledge_base["data_source_ids"]
                    )
                    pass

                # Add the bots referencing this Knowledge Base to the list.
                knowledge_base["queued_bots"].append(
                    {
                        "user_id": queued_bot["OwnerUserId"],
                        "bot_id": queued_bot["BotId"],
                    }
                )

        # Update `knowledge_base_id` of the bots using shared Knowledge Bases.
        for knowledge_base in knowledge_bases.values():
            for queued_bot in knowledge_base["queued_bots"]:
                update_knowledge_base_id(
                    user_id=queued_bot["user_id"],
                    bot_id=queued_bot["bot_id"],
                    knowledge_base_id=knowledge_base["knowledge_base_id"],
                    data_source_ids=knowledge_base["data_source_ids"],
                )

    else:
        # Otherwise, synchronize all shared Knowledge Bases.
        data_sources.update(
            (
                data_source_id,
                {
                    "KnowledgeBaseId": knowledge_base["knowledge_base_id"],
                    "DataSourceId": data_source_id,
                    "FilesDiffs": [],
                },
            )
            for knowledge_base in knowledge_bases.values()
            for data_source_id in knowledge_base["data_source_ids"]
        )

    return {
        "QueuedBots": queued_bots,
        "SharedKnowledgeBases": shared_knowledge_bases,
        "DataSources": list(data_sources.values()),
        **(
            {
                "Lock": event["Lock"],
            }
            if "Lock" in event
            else {}
        ),
    }
