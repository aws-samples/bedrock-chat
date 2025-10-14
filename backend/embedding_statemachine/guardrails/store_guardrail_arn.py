import logging
from typing import List, TypedDict

from app.repositories.common import decompose_sk
from app.repositories.custom_bot import update_guardrails_params

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class StackItem(TypedDict):
    KnowledgeBaseId: str
    DataSourceId: str
    PK: str
    SK: str


class StackOutput(TypedDict):
    """
    'stack_output': {
        'KnowledgeBaseId': 'ABCDEFGHIJKL',
        'items': [
            {
                'KnowledgeBaseId': 'MNOPQRSTUVWX',
                'DataSourceId': 'YZABCDEFGHI',
                'PK': '7801e3f0-40b1-70da-2e13-652d4adce1c3',
                'SK': 'BOT#01JKWE8RP6YWNX9SKFSCCNS73Z'
            }
        ],
        'GuardrailArn': 'arn:aws:bedrock:us-east-1:123456789012:guardrail/abcdefghijkl',
        'GuardrailVersion': 'DRAFT',
    }
    """

    KnowledgeBaseId: str
    items: List[StackItem]
    GuardrailArn: str
    GuardrailVersion: str


def handler(event, context):
    logger.info(f"Event: {event}")
    pk = event["pk"]
    sk = event["sk"]
    stack_output: StackOutput = event["stack_output"]

    # Check if stack_output is valid
    if not stack_output:
        logger.warning("No stack_output received")
        guardrail_arn = ""
        guardrail_version = ""

    else:
        guardrail_arn = stack_output.get("GuardrailArn", "")
        guardrail_version = stack_output.get("GuardrailVersion", "")

    user_id = pk
    bot_id = decompose_sk(sk)

    if guardrail_arn:
        update_guardrails_params(user_id, bot_id, guardrail_arn, guardrail_version)
