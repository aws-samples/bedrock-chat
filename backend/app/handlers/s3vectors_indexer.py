"""
DynamoDB Streams → S3 Vectors indexer Lambda.

Triggered by changes to the bot and conversation DynamoDB tables.
Generates Bedrock embeddings and stores/removes them in S3 Vector buckets.
"""
import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")
REGION = os.environ.get("REGION", "ap-southeast-2")
S3_VECTORS_BOT_BUCKET = os.environ.get("S3_VECTORS_BOT_BUCKET_NAME", "")
S3_VECTORS_CONV_BUCKET = os.environ.get("S3_VECTORS_CONVERSATION_BUCKET_NAME", "")
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
EMBEDDING_DIMENSION = 1024

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


def _ensure_bucket(bucket_name: str) -> None:
    """Create the vector bucket if it does not already exist."""
    client = _get_s3vectors()
    try:
        client.get_vector_bucket(vectorBucketName=bucket_name)
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code in ("ResourceNotFoundException", "NoSuchBucket", "404"):
            client.create_vector_bucket(vectorBucketName=bucket_name)
            logger.info(f"Created S3 Vector bucket: {bucket_name}")
        else:
            raise


def _embed(text: str) -> list[float]:
    """Return a 1024-dim embedding for the given text."""
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


def _ddb_str(image: dict, key: str) -> str:
    return image.get(key, {}).get("S", "")


def _ddb_num(image: dict, key: str) -> float:
    return float(image.get(key, {}).get("N", "0"))


def _ddb_list(image: dict, key: str) -> list[str]:
    return [v.get("S", "") for v in image.get(key, {}).get("L", [])]


# ── Bot record handling ────────────────────────────────────────────────────────

def _process_bot_insert_modify(new_image: dict, bucket: str) -> dict | None:
    """Build a vector entry for a bot record. Returns None if the record should be skipped."""
    bot_id = _ddb_str(new_image, "BotId")
    if not bot_id:
        return None
    title = _ddb_str(new_image, "Title")
    description = _ddb_str(new_image, "Description")
    instruction = _ddb_str(new_image, "Instruction")
    text = f"{title} {description} {instruction}".strip()
    if not text:
        return None

    try:
        embedding = _embed(text)
    except Exception as exc:
        logger.error(f"Embedding failed for bot {bot_id}: {exc}")
        return None

    usage_count_raw = (
        new_image.get("UsageStats", {})
        .get("M", {})
        .get("usage_count", {})
        .get("N", "0")
    )

    create_time = _ddb_num(new_image, "CreateTime")
    return {
        "key": bot_id,
        "data": {"float32": embedding},
        "metadata": {
            "BotId": bot_id,
            "Title": title,
            "Description": description,
            "SharedScope": _ddb_str(new_image, "SharedScope") or "private",
            "SharedStatus": _ddb_str(new_image, "SharedStatus"),
            "SyncStatus": _ddb_str(new_image, "SyncStatus"),
            "PK": _ddb_str(new_image, "PK"),
            "CreateTime": create_time,
            "LastUsedTime": _ddb_num(new_image, "LastUsedTime") or create_time,
            "UsageCount": float(usage_count_raw),
            "AllowedCognitoUsers": _ddb_list(new_image, "AllowedCognitoUsers"),
            "AllowedCognitoGroups": _ddb_list(new_image, "AllowedCognitoGroups"),
        },
    }


# ── Conversation record handling ───────────────────────────────────────────────

def _process_conv_insert_modify(new_image: dict, bucket: str) -> dict | None:
    """Build a vector entry for a conversation record."""
    pk = _ddb_str(new_image, "PK")
    sk = _ddb_str(new_image, "SK")
    title = _ddb_str(new_image, "Title")
    if not pk or not sk or not title:
        return None

    # Extract the conversation ID from SK: "{userId}#CONV#{convId}"
    parts = sk.split("#CONV#")
    if len(parts) != 2:
        return None
    conv_id = parts[1]

    text = title
    try:
        embedding = _embed(text)
    except Exception as exc:
        logger.error(f"Embedding failed for conversation {conv_id}: {exc}")
        return None

    return {
        "key": f"{pk}#{conv_id}",
        "data": {"float32": embedding},
        "metadata": {
            "ConversationId": conv_id,
            "UserId": pk,
            "Title": title,
            "CreateTime": _ddb_num(new_image, "CreateTime"),
        },
    }


# ── Main handler ──────────────────────────────────────────────────────────────

def handler(event, context):
    if not S3_VECTORS_BOT_BUCKET or not S3_VECTORS_CONV_BUCKET:
        logger.error("S3 Vectors bucket names not configured")
        return

    _ensure_bucket(S3_VECTORS_BOT_BUCKET)
    _ensure_bucket(S3_VECTORS_CONV_BUCKET)

    bot_upserts: list[dict] = []
    bot_deletes: list[str] = []
    conv_upserts: list[dict] = []
    conv_deletes: list[str] = []

    for record in event.get("Records", []):
        event_name = record.get("eventName", "")
        ddb = record.get("dynamodb", {})
        new_image = ddb.get("NewImage", {})
        old_image = ddb.get("OldImage", {})

        sk_new = _ddb_str(new_image, "SK")
        sk_old = _ddb_str(old_image, "SK")
        sk = sk_new or sk_old

        is_bot = sk.startswith("BOT") or "#CONV#" not in sk and "BotId" in new_image
        # More reliable: check for the BOT SK prefix pattern
        is_bot_record = sk.upper().startswith("BOT")
        is_conv_record = "#CONV#" in sk

        if event_name == "REMOVE":
            if is_bot_record:
                bot_id = _ddb_str(old_image, "BotId")
                if bot_id:
                    bot_deletes.append(bot_id)
            elif is_conv_record:
                pk = _ddb_str(old_image, "PK")
                parts = sk_old.split("#CONV#")
                if len(parts) == 2:
                    conv_deletes.append(f"{pk}#{parts[1]}")
        elif event_name in ("INSERT", "MODIFY"):
            if is_bot_record:
                entry = _process_bot_insert_modify(new_image, S3_VECTORS_BOT_BUCKET)
                if entry:
                    bot_upserts.append(entry)
            elif is_conv_record:
                entry = _process_conv_insert_modify(new_image, S3_VECTORS_CONV_BUCKET)
                if entry:
                    conv_upserts.append(entry)

    client = _get_s3vectors()

    # Bot operations
    if bot_deletes:
        try:
            client.delete_vectors(
                vectorBucketName=S3_VECTORS_BOT_BUCKET, keys=bot_deletes
            )
            logger.info(f"Deleted {len(bot_deletes)} bot vectors")
        except Exception as exc:
            logger.error(f"Failed to delete bot vectors: {exc}")

    for i in range(0, len(bot_upserts), 100):
        batch = bot_upserts[i : i + 100]
        try:
            client.put_vectors(
                vectorBucketName=S3_VECTORS_BOT_BUCKET, vectors=batch
            )
            logger.info(f"Indexed {len(batch)} bot vectors")
        except Exception as exc:
            logger.error(f"Failed to put bot vectors: {exc}")

    # Conversation operations
    if conv_deletes:
        try:
            client.delete_vectors(
                vectorBucketName=S3_VECTORS_CONV_BUCKET, keys=conv_deletes
            )
            logger.info(f"Deleted {len(conv_deletes)} conversation vectors")
        except Exception as exc:
            logger.error(f"Failed to delete conversation vectors: {exc}")

    for i in range(0, len(conv_upserts), 100):
        batch = conv_upserts[i : i + 100]
        try:
            client.put_vectors(
                vectorBucketName=S3_VECTORS_CONV_BUCKET, vectors=batch
            )
            logger.info(f"Indexed {len(batch)} conversation vectors")
        except Exception as exc:
            logger.error(f"Failed to put conversation vectors: {exc}")
