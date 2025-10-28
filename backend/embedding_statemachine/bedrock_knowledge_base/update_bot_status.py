import json
from typing import TypedDict

from app.repositories.common import compose_sk, get_bot_table_client
from app.routes.schemas.bot import type_sync_status
from reretry import retry

RETRIES_TO_UPDATE_SYNC_STATUS = 4
RETRY_DELAY_TO_UPDATE_SYNC_STATUS = 2


class SyncStatus(TypedDict):
    user_id: str
    bot_id: str
    status: type_sync_status
    reason: str
    last_exec_id: str


@retry(tries=RETRIES_TO_UPDATE_SYNC_STATUS, delay=RETRY_DELAY_TO_UPDATE_SYNC_STATUS)
def update_sync_status(sync_status: SyncStatus):
    table = get_bot_table_client()
    table.update_item(
        Key={
            "PK": sync_status["user_id"],
            "SK": compose_sk(sync_status["bot_id"], "bot"),
        },
        UpdateExpression="SET SyncStatus = :sync_status, SyncStatusReason = :sync_status_reason, LastExecId = :last_exec_id",
        ExpressionAttributeValues={
            ":sync_status": sync_status["status"],
            ":sync_status_reason": sync_status["reason"],
            ":last_exec_id": sync_status["last_exec_id"],
        },
    )


def handler(event, context):
    # Initialize variables
    queued_bots = event.get("QueuedBots")
    user_id = event.get("OwnerUserId")
    bot_id = event.get("BotId")
    sync_status: type_sync_status = event["SyncStatus"]
    sync_status_reason: str
    last_exec_id: str

    build = event.get("Build")
    if build:
        # CodeBuild
        sync_status_reason = json.dumps(build["Phases"])
        last_exec_id = build["Arn"]

    else:
        sync_status_reason = event.get("SyncStatusReason", "")
        last_exec_id = event.get("LastExecId", "")

    sync_status_updates: list[SyncStatus] = []

    if user_id and bot_id:
        sync_status_updates.append(
            {
                "user_id": user_id,
                "bot_id": bot_id,
                "status": sync_status,
                "reason": sync_status_reason,
                "last_exec_id": last_exec_id,
            }
        )

    if queued_bots:
        sync_status_updates.extend(
            {
                "user_id": queued_bot["OwnerUserId"],
                "bot_id": queued_bot["BotId"],
                "status": sync_status,
                "reason": sync_status_reason,
                "last_exec_id": last_exec_id,
            }
            for queued_bot in queued_bots
        )

    for sync_status_update in sync_status_updates:
        update_sync_status(sync_status_update)
