import os
import json
import logging

import boto3
from retry import retry
from app.routes.schemas.bot import type_sync_status
from app.repositories.common import _get_table_client
from app.repositories.custom_bot import decompose_bot_id, update_guardrails_params
from typing import TypedDict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class StackOutput(TypedDict):
    KnowledgeBaseId: str
    DataSourceId: str
    GuardrailArn: str
    GuardrailVersion: str


def handler(event, context):
    logger.info(f"Event: {event}")
    pk = event["pk"]
    sk = event["sk"]
    stack_output: list[StackOutput] = event["stack_output"]

    guardrail_arn = stack_output[0]["GuardrailArn"]
    guardrail_version = stack_output[0]["GuardrailVersion"]

    user_id = pk
    bot_id = decompose_bot_id(sk)

    update_guardrails_params(user_id, bot_id, guardrail_arn, guardrail_version)
