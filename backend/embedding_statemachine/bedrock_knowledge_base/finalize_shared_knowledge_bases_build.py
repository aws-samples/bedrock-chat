import os
from typing import Any, Dict, List, TypedDict, NotRequired

import boto3
from app.repositories.custom_bot import (
    update_knowledge_base_id,
    update_guardrails_params,
)

BEDROCK_REGION = os.environ.get("BEDROCK_REGION")

cf_client = boto3.client("cloudformation", BEDROCK_REGION)


class DataSource(TypedDict):
    KnowledgeBaseId: str
    DataSourceId: str


class StackOutput(TypedDict):
    DataSources: List[DataSource]


def handler(event, context) -> StackOutput:
    print(event)
    shared_knowledge_bases = event["SharedKnowledgeBases"]

    # Note: stack naming rule is defined on:
    # cdk/bin/bedrock-shared-knowledge-bases.ts
    stack_name = "BrChatSharedKbStack"

    response = cf_client.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0]["Outputs"]
    print(outputs)

    result: StackOutput = {
        "DataSources": [],
    }

    for shared_knowledge_base in shared_knowledge_bases:
        knowledge_base_hash = shared_knowledge_base["KnowledgeBaseHash"]

        knowledge_base_id = None
        data_source_ids: List[str] = []

        for output in outputs:
            if output["OutputKey"] == f"KnowledgeBaseId{knowledge_base_hash}":
                knowledge_base_id = output["OutputValue"]

            elif output["OutputKey"].startswith(f"DataSource{knowledge_base_hash}"):
                data_source_ids.append(output["OutputValue"])

        if knowledge_base_id:
            result["DataSources"].extend(
                {
                    "KnowledgeBaseId": knowledge_base_id,
                    "DataSourceId": data_source_id,
                }
                for data_source_id in data_source_ids
            )

            bots = shared_knowledge_base["Bots"]
            for bot in bots:
                update_knowledge_base_id(
                    bot["OwnerUserId"], bot["BotId"], knowledge_base_id, data_source_ids
                )

    return result
