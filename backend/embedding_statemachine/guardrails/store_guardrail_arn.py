import os
import json
import logging

import boto3
from retry import retry
from app.routes.schemas.bot import type_sync_status
from app.repositories.common import _get_table_client
from app.repositories.custom_bot import decompose_bot_id, update_guardrails_params
from typing import TypedDict, List

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Items(TypedDict):
    KnowledgeBaseId: str
    DataSourceId: str
    GuardrailArn: str
    GuardrailVersion: str
    PK: str
    SK: str


class StackOutput(TypedDict):
    KnowledgeBaseId: str
    items: List[Items]


def handler(event, context):
    logger.info(f"Event: {event}")
    pk = event["pk"]
    sk = event["sk"]
    stack_output: List[StackOutput] = event["stack_output"]

    # Check if stack_output is valid and has at least one item
    if (
        not stack_output
        or not isinstance(stack_output["items"], list)
        or len(stack_output["items"]) == 0
    ):
        logger.warning("Empty or invalid stack_output received")
        guardrail_arn = ""
        guardrail_version = ""
    else:
        # Access the first item directly since we know it exists
        first_output = stack_output["items"][0]
        guardrail_arn = first_output.get("GuardrailArn", "")
        guardrail_version = first_output.get("GuardrailVersion", "")

    user_id = pk
    bot_id = decompose_bot_id(sk)

    update_guardrails_params(user_id, bot_id, guardrail_arn, guardrail_version)
