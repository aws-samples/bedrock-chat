import os
import boto3
from app.repositories.custom_bot import (
    decompose_bot_id,
)

BEDROCK_REGION = os.environ.get("BEDROCK_REGION")

cf_client = boto3.client("cloudformation", BEDROCK_REGION)


def handler(event, context):
    print(event)
    pk = event["pk"]
    sk = event["sk"]

    bot_id = decompose_bot_id(sk)

    # Note: stack naming rule is defined on:
    # cdk/bin/bedrock-knowledge-base.ts
    stack_name = f"BrChatKbStack{bot_id}"

    response = cf_client.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0]["Outputs"]

    knowledge_base_id = None
    data_source_ids = []
    guardrail_arn = None
    guardrail_version = None
    result = []

    for output in outputs:
        if output["OutputKey"] == "KnowledgeBaseId":
            knowledge_base_id = output["OutputValue"]
        elif output["OutputKey"].startswith("DataSource"):
            data_source_ids.append(output["OutputValue"])
        elif output["OutputKey"] == "GuardrailArn":
            guardrail_arn = output["OutputValue"]
        elif output["OutputKey"] == "GuardrailVersion":
            guardrail_version = output["OutputValue"]

    # If no data sources exist, create a result with just the KnowledgeBaseId
    if not data_source_ids and knowledge_base_id:
        result.append(
            {
                "KnowledgeBaseId": knowledge_base_id,
                "DataSourceId": "",
                "GuardrailArn": guardrail_arn if guardrail_arn != None else "",
                "GuardrailVersion": (
                    guardrail_version if guardrail_version != None else ""
                ),
                "PK": pk,
                "SK": sk,
            }
        )
    else:
        for data_source_id in data_source_ids:
            result.append(
                {
                    "KnowledgeBaseId": knowledge_base_id,
                    "DataSourceId": data_source_id,
                    "GuardrailArn": guardrail_arn if guardrail_arn != None else "",
                    "GuardrailVersion": (
                        guardrail_version if guardrail_version != None else ""
                    ),
                    "PK": pk,
                    "SK": sk,
                }
            )

    return result
