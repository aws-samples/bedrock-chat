import os
from typing import List, TypedDict

import boto3
from app.repositories.custom_bot import (
    update_knowledge_base_id,
    update_guardrails_params,
)

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
    files = event.get("Files")

    # Note: stack naming rule is defined on:
    # cdk/bin/bedrock-custom-bot.ts
    stack_name = f"BrChatKbStack{bot_id}"

    response = cfn.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0].get("Outputs")
    if not outputs:
        raise ValueError(f"No outputs found in CloudFormation stack '{stack_name}'")

    knowledge_base_id = None
    data_source_ids: List[str] = []

    guardrail_arn = None
    guardrail_version = None

    for output in outputs:
        key = output.get("OutputKey")
        value = output.get("OutputValue")
        if key and value:
            if key == "KnowledgeBaseId":
                knowledge_base_id = value

            elif key.startswith("DataSource"):
                data_source_ids.append(value)

            elif key == "GuardrailArn":
                guardrail_arn = value

            elif key == "GuardrailVersion":
                guardrail_version = value

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
                "Files": (
                    [
                        {
                            "OwnerUserId": user_id,
                            "BotId": bot_id,
                            "Added": files["Added"],
                            "Deleted": files["Deleted"],
                        }
                    ]
                    if files is not None
                    else []
                ),
            }
            for data_source_id in data_source_ids
        )
        update_knowledge_base_id(user_id, bot_id, knowledge_base_id, data_source_ids)

    if guardrail_arn and guardrail_version:
        update_guardrails_params(user_id, bot_id, guardrail_arn, guardrail_version)

    return result
