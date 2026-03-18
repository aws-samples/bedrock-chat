import json
import logging
import os
import random

import boto3

from app.repositories.common import (
    S3_VECTORS_BOT_BUCKET_NAME,
    REGION,
    get_bot_table_client,
)
from app.repositories.models.custom_bot import BotMeta
from app.user import User
from boto3.dynamodb.conditions import Key

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
EMBEDDING_DIMENSION = 1024

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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


def _bot_meta_from_s3vectors_item(item: dict, user_id: str) -> BotMeta:
    """Build a BotMeta from an S3 Vectors query/list result item."""
    meta = item.get("metadata", {})
    create_time = float(meta.get("CreateTime", 0))
    return BotMeta(
        id=meta["BotId"],
        title=meta.get("Title", ""),
        description=meta.get("Description", ""),
        create_time=create_time,
        last_used_time=float(meta.get("LastUsedTime", create_time)),
        is_starred=False,
        sync_status=meta.get("SyncStatus", "RUNNING"),
        owned=meta.get("PK", "") == user_id,
        is_origin_accessible=True,
        shared_scope=meta.get("SharedScope", "private"),
        shared_status=meta.get("SharedStatus", "unshared"),
    )


def _is_bot_accessible(meta: dict, user: User) -> bool:
    """Check if the user has access to the bot based on metadata."""
    shared_scope = meta.get("SharedScope", "private")
    pk = meta.get("PK", "")

    if shared_scope == "all":
        return True
    if pk == user.id:
        return True
    if shared_scope == "partial":
        if user.is_admin():
            return True
        allowed_users = meta.get("AllowedCognitoUsers", [])
        allowed_groups = meta.get("AllowedCognitoGroups", [])
        if user.id in allowed_users:
            return True
        if any(g in allowed_groups for g in user.groups):
            return True
    return False


def find_bots_by_query(
    query: str,
    user: User,
    limit: int = 20,
) -> list[BotMeta]:
    """Search bots semantically via S3 Vectors, applying access-control filtering."""
    logger.info(f"Searching bots with query: {query}")

    if not S3_VECTORS_BOT_BUCKET_NAME:
        logger.warning("S3_VECTORS_BOT_BUCKET_NAME is not set; returning empty list")
        return []

    try:
        embedding = _embed(query)
    except Exception as exc:
        logger.error(f"Embedding failed for query '{query}': {exc}")
        return []

    # Over-fetch to account for access-control filtering
    top_k = min(limit * 10, 500)
    try:
        response = _get_s3vectors().query_vectors(
            vectorBucketName=S3_VECTORS_BOT_BUCKET_NAME,
            queryVector={"float32": embedding},
            topK=top_k,
            returnMetadata="ALL",
        )
    except Exception as exc:
        logger.error(f"S3 Vectors query failed: {exc}")
        return []

    bots: list[BotMeta] = []
    for item in response.get("vectors", []):
        meta = item.get("metadata", {})
        if _is_bot_accessible(meta, user):
            bots.append(_bot_meta_from_s3vectors_item(item, user.id))
            if len(bots) >= limit:
                break

    logger.info(f"Found {len(bots)} bots matching query: {query}")
    return bots


def find_bots_sorted_by_usage_count(
    user: User,
    limit: int = 20,
) -> list[BotMeta]:
    """Return bots sorted by usage count using DynamoDB SharedScopeIndex."""
    logger.info("Finding bots sorted by usage count")
    table = get_bot_table_client()

    # Collect candidate bots from DynamoDB
    items: list[dict] = []

    # 1. All public bots
    paginator_kwargs: dict = {
        "IndexName": "SharedScopeIndex",
        "KeyConditionExpression": Key("SharedScope").eq("all"),
    }
    response = table.query(**paginator_kwargs)
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.query(
            **paginator_kwargs, ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    # 2. Partial-shared bots — owner or permitted users can see them
    partial_kwargs: dict = {
        "IndexName": "SharedScopeIndex",
        "KeyConditionExpression": Key("SharedScope").eq("partial"),
    }
    response = table.query(**partial_kwargs)
    partial_items = response.get("Items", [])
    while "LastEvaluatedKey" in response:
        response = table.query(
            **partial_kwargs, ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        partial_items.extend(response.get("Items", []))

    for item in partial_items:
        allowed_users = item.get("AllowedCognitoUsers", [])
        allowed_groups = item.get("AllowedCognitoGroups", [])
        pk = item.get("PK", "")
        if (
            user.is_admin()
            or pk == user.id
            or user.id in allowed_users
            or any(g in allowed_groups for g in user.groups)
        ):
            items.append(item)

    # De-duplicate by BotId
    seen: set[str] = set()
    unique_items = []
    for item in items:
        bot_id = item.get("BotId", "")
        if bot_id and bot_id not in seen:
            seen.add(bot_id)
            unique_items.append(item)

    # Sort by usage count descending
    def _usage(item: dict) -> float:
        return float(
            item.get("UsageStats", {}).get("usage_count", 0) or 0
        )

    unique_items.sort(key=_usage, reverse=True)
    unique_items = unique_items[:limit]

    bots = [
        BotMeta.from_dynamo_item(item, owned=item.get("PK") == user.id, is_origin_accessible=True)
        for item in unique_items
    ]
    logger.info(f"Found {len(bots)} bots sorted by usage count")
    return bots


def find_random_bots(
    user: User,
    limit: int = 20,
) -> list[BotMeta]:
    """Return randomly selected accessible bots using DynamoDB SharedScopeIndex."""
    logger.info("Finding random bots")
    table = get_bot_table_client()

    items: list[dict] = []

    # Public bots
    public_kwargs: dict = {
        "IndexName": "SharedScopeIndex",
        "KeyConditionExpression": Key("SharedScope").eq("all"),
    }
    response = table.query(**public_kwargs)
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.query(
            **public_kwargs, ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    # Partial-shared bots the user can access
    partial_kwargs: dict = {
        "IndexName": "SharedScopeIndex",
        "KeyConditionExpression": Key("SharedScope").eq("partial"),
    }
    response = table.query(**partial_kwargs)
    partial_items = response.get("Items", [])
    while "LastEvaluatedKey" in response:
        response = table.query(
            **partial_kwargs, ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        partial_items.extend(response.get("Items", []))

    for item in partial_items:
        allowed_users = item.get("AllowedCognitoUsers", [])
        allowed_groups = item.get("AllowedCognitoGroups", [])
        pk = item.get("PK", "")
        if (
            user.is_admin()
            or pk == user.id
            or user.id in allowed_users
            or any(g in allowed_groups for g in user.groups)
        ):
            items.append(item)

    # De-duplicate
    seen: set[str] = set()
    unique_items = []
    for item in items:
        bot_id = item.get("BotId", "")
        if bot_id and bot_id not in seen:
            seen.add(bot_id)
            unique_items.append(item)

    random.shuffle(unique_items)
    unique_items = unique_items[:limit]

    bots = [
        BotMeta.from_dynamo_item(item, owned=item.get("PK") == user.id, is_origin_accessible=True)
        for item in unique_items
    ]
    logger.info(f"Found {len(bots)} random bots")
    return bots
