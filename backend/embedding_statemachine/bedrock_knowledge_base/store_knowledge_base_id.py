import logging
from typing import List

from app.repositories.common import decompose_sk
from app.repositories.custom_bot import update_knowledge_base_id
from typing_extensions import TypedDict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class StackItem(TypedDict):
    KnowledgeBaseId: str
    DataSourceId: str
    PK: str
    SK: str


class StackOutput(TypedDict):
    KnowledgeBaseId: str
    items: List[StackItem]
    GuardrailArn: str
    GuardrailVersion: str


def handler(event, context):
    logger.info(f"Event: {event}")
    pk = event["pk"]
    sk = event["sk"]
    stack_output: StackOutput = event["stack_output"]

    knowledge_base_id: str | None
    data_source_ids: list[str] | None

    # Check if stack_output is valid
    if not stack_output:
        logger.warning("No stack_output received")
        knowledge_base_id = None
        data_source_ids = None

    else:
        kb_id = stack_output.get("KnowledgeBaseId")

        # Filter out None values and ensure all elements are strings
        ds_ids = [
            item["DataSourceId"]
            for item in stack_output.get("items", [])
            if item.get("DataSourceId")
        ]

        knowledge_base_id = kb_id if kb_id else None
        data_source_ids = ds_ids if kb_id else None

    user_id = pk
    bot_id = decompose_sk(sk)

    if knowledge_base_id is not None:
        update_knowledge_base_id(user_id, bot_id, knowledge_base_id, data_source_ids)
