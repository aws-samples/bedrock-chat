import json
import logging

import boto3
from app.repositories.common import compose_sk, get_bot_table_client
from app.routes.schemas.bot import type_sync_status
from reretry import retry

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

RETRIES_TO_UPDATE_SYNC_STATUS = 4
RETRY_DELAY_TO_UPDATE_SYNC_STATUS = 2


@retry(tries=RETRIES_TO_UPDATE_SYNC_STATUS, delay=RETRY_DELAY_TO_UPDATE_SYNC_STATUS)
def update_sync_status(
    user_id: str,
    bot_id: str,
    sync_status: type_sync_status,
    sync_status_reason: str,
    last_exec_id: str,
):
    table = get_bot_table_client()
    table.update_item(
        Key={"PK": user_id, "SK": compose_sk(bot_id, "bot")},
        UpdateExpression="SET SyncStatus = :sync_status, SyncStatusReason = :sync_status_reason, LastExecId = :last_exec_id",
        ExpressionAttributeValues={
            ":sync_status": sync_status,
            ":sync_status_reason": sync_status_reason,
            ":last_exec_id": last_exec_id,
        },
    )


def extract_from_cause(cause_str: str) -> tuple:
    logger.debug(f"Extracting OWNER_USER_ID and BOT_ID from cause: {cause_str}")
    cause = json.loads(cause_str)
    logger.debug(f"Cause: {cause}")
    environment_variables = cause["Build"]["Environment"]["EnvironmentVariables"]
    logger.debug(f"Environment variables: {environment_variables}")

    user_id = next(
        (
            item["Value"]
            for item in environment_variables
            if item["Name"] == "OWNER_USER_ID"
        ),
        None,
    )
    bot_id = next(
        (item["Value"] for item in environment_variables if item["Name"] == "BOT_ID"),
        None,
    )

    if not user_id or not bot_id:
        raise ValueError("PK or SK not found in cause.")

    build_arn = cause["Build"].get("Arn", "")

    logger.debug(f"PK: {user_id}, SK: {bot_id}, Build ARN: {build_arn}")

    return user_id, bot_id, build_arn


def handler(event, context):
    logger.info(f"Event: {event}")
    try:
        cause = event.get("cause", None)
        ingestion_job = event.get("ingestion_job", None)

        # Initialize variables
        user_id: str
        bot_id: str
        sync_status: type_sync_status
        sync_status_reason: str
        last_exec_id: str

        if cause:
            # UpdateSymcStatusFailed
            user_id, bot_id, build_arn = extract_from_cause(cause)
            sync_status = "FAILED"
            sync_status_reason = cause
            last_exec_id = build_arn
        elif ingestion_job:
            # UpdateSymcStatusFailedForIngestion
            user_id = event["user_id"]
            bot_id = event["bot_id"]
            sync_status = "FAILED"
            sync_status_reason = str(ingestion_job["ingestionJob"]["failureReasons"])
            last_exec_id = ingestion_job["ingestionJob"]["ingestionJobId"]
        else:
            user_id = event["user_id"]
            bot_id = event["bot_id"]
            sync_status = event["sync_status"]
            sync_status_reason = event.get("sync_status_reason", "")
            last_exec_id = event.get("last_exec_id", "")

        logger.info(
            f"Updating sync status for bot {bot_id} of user {user_id} to {sync_status} with reason: {sync_status_reason}"
        )

        update_sync_status(
            user_id, bot_id, sync_status, sync_status_reason, last_exec_id
        )

        return {
            "statusCode": 200,
            "body": json.dumps("Sync status updated successfully."),
        }
    except Exception as e:
        logger.error(f"Error updating sync status: {e}")
        return {"statusCode": 500, "body": json.dumps("Error updating sync status.")}
