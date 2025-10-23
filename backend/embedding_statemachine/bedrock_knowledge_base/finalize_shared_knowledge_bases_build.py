import os
from typing import List, TypedDict

import boto3
from app.repositories.custom_bot import update_knowledge_base_id

BEDROCK_REGION = os.environ.get("BEDROCK_REGION")

cfn = boto3.client("cloudformation", BEDROCK_REGION)


class DataSourceFiles(TypedDict):
    OwnerUserId: str
    BotId: str
    Added: list[str]
    Deleted: list[str]


class DataSource(TypedDict):
    KnowledgeBaseId: str
    DataSourceId: str
    Files: list[DataSourceFiles]


class StackOutput(TypedDict):
    DataSources: List[DataSource]


def handler(event, context) -> StackOutput:
    print(event)
    queued_bots_for_knowledge_bases = event["SharedKnowledgeBases"][
        "QueuedBotsForKnowledgeBases"
    ]

    # Note: stack naming rule is defined on:
    # cdk/bin/bedrock-shared-knowledge-bases.ts
    stack_name = "BrChatSharedKbStack"

    response = cfn.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0].get("Outputs")
    if not outputs:
        raise ValueError(f"No outputs found in CloudFormation stack '{stack_name}'")

    print(outputs)

    result: StackOutput = {
        "DataSources": [],
    }

    for queued_bots_for_knowledge_base in queued_bots_for_knowledge_bases:
        knowledge_base_hash = queued_bots_for_knowledge_base["KnowledgeBaseHash"]

        knowledge_base_id = None
        data_source_ids: List[str] = []

        for output in outputs:
            key = output.get("OutputKey")
            value = output.get("OutputValue")
            if key and value:
                if key == f"KnowledgeBaseId{knowledge_base_hash}":
                    knowledge_base_id = value

                elif key.startswith(f"DataSource{knowledge_base_hash}"):
                    data_source_ids.append(value)

        if knowledge_base_id:
            bots = queued_bots_for_knowledge_base["Bots"]
            data_source_files: list[DataSourceFiles] = []
            for bot in bots:
                user_id = bot["OwnerUserId"]
                bot_id = bot["BotId"]
                files = bot.get("Files")
                if files is not None:
                    data_source_files.append(
                        {
                            "OwnerUserId": user_id,
                            "BotId": bot_id,
                            "Added": files["Added"],
                            "Deleted": files["Deleted"],
                        }
                    )

                update_knowledge_base_id(
                    user_id, bot_id, knowledge_base_id, data_source_ids
                )

            result["DataSources"].extend(
                (
                    {
                        "KnowledgeBaseId": knowledge_base_id,
                        "DataSourceId": data_source_id,
                        "Files": data_source_files,
                    }
                    for data_source_id in data_source_ids
                )
            )

    return result
