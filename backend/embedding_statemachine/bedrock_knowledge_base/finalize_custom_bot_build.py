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


class Bot(TypedDict):
    OwnerUserId: str
    BotId: str


class StackOutput(TypedDict):
    DataSources: List[DataSource]
    Bots: list[Bot]


def handler(event, context) -> StackOutput:
    print(event)
    user_id = event["OwnerUserId"]
    bot_id = event["BotId"]

    # Note: stack naming rule is defined on:
    # cdk/bin/bedrock-custom-bot.ts
    stack_name = f"BrChatKbStack{bot_id}"

    response = cf_client.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0]["Outputs"]

    knowledge_base_id = None
    data_source_ids: List[str] = []

    guardrail_arn = None
    guardrail_version = None

    for output in outputs:
        if output["OutputKey"] == "KnowledgeBaseId":
            knowledge_base_id = output["OutputValue"]

        elif output["OutputKey"].startswith("DataSource"):
            data_source_ids.append(output["OutputValue"])

        elif output["OutputKey"] == "GuardrailArn":
            guardrail_arn = output["OutputValue"]

        elif output["OutputKey"] == "GuardrailVersion":
            guardrail_version = output["OutputValue"]

    result: StackOutput = {
        "DataSources": [],
        "Bots": [
            {
                "OwnerUserId": user_id,
                "BotId": bot_id,
            },
        ],
    }

    if knowledge_base_id:
        result["DataSources"].extend(
            {
                "KnowledgeBaseId": knowledge_base_id,
                "DataSourceId": data_source_id,
            }
            for data_source_id in data_source_ids
        )
        update_knowledge_base_id(user_id, bot_id, knowledge_base_id, data_source_ids)

    if guardrail_arn and guardrail_version:
        update_guardrails_params(user_id, bot_id, guardrail_arn, guardrail_version)

    return result
