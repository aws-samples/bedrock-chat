import json
import logging
import os
from typing import List

import boto3
from app.repositories.common import _get_table_client
from app.repositories.custom_bot import decompose_bot_id, update_knowledge_base_id
from app.routes.schemas.bot import type_sync_status
from retry import retry
from typing_extensions import TypedDict

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
    stack_output: StackOutput = event["stack_output"]

    kb_id = (
        stack_output["KnowledgeBaseId"] if "KnowledgeBaseId" in stack_output else None
    )
    if not kb_id:
        raise ValueError("KnowledgeBaseId not found in stack outputs")

    # Filter out None values and ensure all elements are strings
    data_source_ids: List[str] = [
        item["DataSourceId"]
        for item in stack_output.get("items", [])
        if item.get("DataSourceId")
    ]

    user_id = pk
    bot_id = decompose_bot_id(sk)

    update_knowledge_base_id(user_id, bot_id, kb_id, data_source_ids)
