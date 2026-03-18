import json
import logging
import os

import boto3

from app.repositories.common import (
    S3_VECTORS_CONVERSATION_BUCKET_NAME,
    REGION,
)
from app.repositories.models.conversation_search import ConversationSearchModel
from app.user import User

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
EMBEDDING_DIMENSION = 1024

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_bedrock = None
_s3vectors = None


def _get_bedrock():
    global _bedrock
    if _bedrock is None:
        _bedrock = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
    return _bedrock


def _get_s3vectors():
    global _s3vectors
    if _s3vectors is None:
        _s3vectors = boto3.client("s3vectors", region_name=REGION)
    return _s3vectors


def _embed(text: str) -> list[float]:
    response = _get_bedrock().invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=json.dumps(
            {
                "inputText": text[:8000],
                "dimensions": EMBEDDING_DIMENSION,
                "normalize": True,
            }
        ),
    )
    return json.loads(response["body"].read())["embedding"]


def find_conversations_by_query(
    query: str,
    user: User,
    limit: int = 20,
) -> list[ConversationSearchModel]:
    """Search conversations semantically via S3 Vectors, filtered to the requesting user."""
    logger.info(f"Searching conversations with query: {query} for user: {user.id}")

    if not S3_VECTORS_CONVERSATION_BUCKET_NAME:
        logger.warning(
            "S3_VECTORS_CONVERSATION_BUCKET_NAME is not set; returning empty list"
        )
        return []

    try:
        embedding = _embed(query)
    except Exception as exc:
        logger.error(f"Embedding failed for query '{query}': {exc}")
        return []

    # Over-fetch to allow filtering down to user's own conversations
    top_k = min(limit * 10, 500)
    try:
        response = _get_s3vectors().query_vectors(
            vectorBucketName=S3_VECTORS_CONVERSATION_BUCKET_NAME,
            queryVector={"float32": embedding},
            topK=top_k,
            returnMetadata="ALL",
        )
    except Exception as exc:
        logger.error(f"S3 Vectors query failed: {exc}")
        return []

    conversations: list[ConversationSearchModel] = []
    for item in response.get("vectors", []):
        meta = item.get("metadata", {})
        if meta.get("UserId", "") != user.id:
            continue
        conversations.append(
            ConversationSearchModel(
                id=meta.get("ConversationId", ""),
                title=meta.get("Title", "Untitled conversation"),
                bot_id=meta.get("BotId"),
                last_updated_time=float(meta.get("CreateTime", 0)),
            )
        )
        if len(conversations) >= limit:
            break

    logger.info(
        f"Found {len(conversations)} conversations matching query: {query}"
    )
    return conversations
