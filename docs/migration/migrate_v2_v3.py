#!/usr/bin/env python3
import argparse
import base64
import json
import logging
import os
import time
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from reretry import retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migration")


################################
# Configuration
################################

# Region where dynamodb is located
REGION = "ap-northeast-1"

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX"
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX"
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX"

################################
# End Configuration
################################

BATCH_SIZE = 25  # DynamoDB WriteReques limit (DO NOT CHANGE)


def get_dynamodb_client():
    return boto3.client("dynamodb", region_name=REGION)


def get_v2_table():
    return boto3.resource("dynamodb", region_name=REGION).Table(V2_CONVERSATION_TABLE)


def get_v3_bot_table():
    return boto3.resource("dynamodb", region_name=REGION).Table(V3_BOT_TABLE)


def get_v3_conv_table():
    return boto3.resource("dynamodb", region_name=REGION).Table(V3_CONVERSATION_TABLE)


def decompose_bot_id(composed_bot_id: str) -> str:
    return composed_bot_id.split("#")[-1]


def decompose_bot_alias_id(composed_alias_id: str) -> str:
    """Extract the actual alias ID from the V2 alias ID"""
    return composed_alias_id.split("#")[-1]


def compose_item_type(user_id: str, item_type: str) -> str:
    if item_type == "bot":
        return f"{user_id}#BOT"
    elif item_type == "alias":
        return f"{user_id}#ALIAS"
    else:
        raise ValueError(f"Invalid item type: {item_type}")


def fetch_original_bot_owner(user_id: str, bot_id: str) -> Optional[str]:
    """元ボットの所有者IDを取得"""
    try:
        # 公開ボットとして検索
        table = get_v2_table()
        logger.info(f"Finding owner for bot: {bot_id}")

        items = query_items(
            table, Key("PublicBotId").eq(bot_id), index_name="PublicBotIdIndex"
        )

        if items:
            # 公開ボットのオーナーIDを返す
            return items[0]["PK"]

        # どこにも情報がない場合はNoneを返す
        logger.warning(f"Could not find owner for bot {bot_id}, will use fallback")
        return None
    except Exception as e:
        logger.error(f"Error fetching original bot owner: {e}")
        return None


def scan_items(
    table, projection_expression=None, filter_expression=None, consistent_read=False
):
    """Generic function to scan items from a DynamoDB table

    Args:
        table: DynamoDB table resource
        projection_expression: Optional attributes to retrieve
        filter_expression: Optional filter expression
        consistent_read: Whether to use consistent read

    Returns:
        List of items from the table
    """
    items = []
    last_evaluated_key = None

    while True:
        scan_kwargs = {"ConsistentRead": consistent_read}
        if projection_expression:
            scan_kwargs["ProjectionExpression"] = projection_expression
        if filter_expression:
            scan_kwargs["FilterExpression"] = filter_expression
        if last_evaluated_key:
            scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

        response = table.scan(**scan_kwargs)
        items.extend(response.get("Items", []))

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

    return items


def scan_all_users() -> List[str]:
    """Scan all users from V2 table"""
    table = get_v2_table()
    items = scan_items(table, projection_expression="PK")

    # Extract unique user IDs
    users = set(item["PK"] for item in items)
    return list(users)


def query_items(table, key_condition_expression, filter_expression=None, index_name=None):
    """Generic function to query items from a DynamoDB table

    Args:
        table: DynamoDB table resource
        key_condition_expression: Key condition expression for the query
        filter_expression: Optional filter expression
        index_name: Optional index name to query against

    Returns:
        List of items matching the query
    """
    items = []
    last_evaluated_key = None

    while True:
        query_kwargs = {"KeyConditionExpression": key_condition_expression}
        if filter_expression:
            query_kwargs["FilterExpression"] = filter_expression
        if index_name:
            query_kwargs["IndexName"] = index_name
        if last_evaluated_key:
            query_kwargs["ExclusiveStartKey"] = last_evaluated_key

        response = table.query(**query_kwargs)
        items.extend(response.get("Items", []))

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

    return items


def get_all_bots_for_user(user_id: str) -> List[Dict]:
    """ユーザーの全ボット取得"""
    table = get_v2_table()
    return query_items(
        table,
        Key("PK").eq(user_id) & Key("SK").begins_with(f"{user_id}#BOT#"),
        Attr("OriginalBotId").not_exists() | Attr("OriginalBotId").eq(""),
    )


def get_all_aliases_for_user(user_id: str) -> List[Dict]:
    """Get all aliases for a user"""
    table = get_v2_table()
    return query_items(
        table, Key("PK").eq(user_id) & Key("SK").begins_with(f"{user_id}#BOT_ALIAS#")
    )


def get_all_conversations_for_user(user_id: str) -> List[Dict]:
    """ユーザーの全会話取得"""
    table = get_v2_table()
    return query_items(
        table, Key("PK").eq(user_id) & Key("SK").begins_with(f"{user_id}#CONV#")
    )


def get_all_related_documents_for_user(user_id: str) -> List[Dict]:
    """ユーザーの全関連ドキュメント取得"""
    table = get_v2_table()
    return query_items(
        table,
        Key("PK").eq(user_id) & Key("SK").begins_with(f"{user_id}#RELATED_DOCUMENT#"),
    )


def convert_bot_item(item: Dict) -> Dict:
    """V2ボットアイテムをV3形式に変換"""
    user_id = item["PK"]
    bot_id = decompose_bot_id(item["SK"])

    new_item = {
        "PK": user_id,
        "SK": f"BOT#{bot_id}",
        "ItemType": compose_item_type(user_id, "bot"),
        "BotId": bot_id,
        "Title": item["Title"],
        "Description": item["Description"],
        "Instruction": item["Instruction"],
        "CreateTime": item["CreateTime"],
        "SyncStatus": item["SyncStatus"],
        "SyncStatusReason": item["SyncStatusReason"],
        "LastExecId": item["LastExecId"],
        "DisplayRetrievedChunks": item.get("DisplayRetrievedChunks", False),
        "GenerationParams": item.get("GenerationParams", {}),
        "AgentData": item.get("AgentData", {"tools": []}),
        "Knowledge": item.get(
            "Knowledge",
            {"source_urls": [], "sitemap_urls": [], "filenames": [], "s3_urls": []},
        ),
    }

    # ConversationQuickStarters
    if "ConversationQuickStarters" in item:
        new_item["ConversationQuickStarters"] = item["ConversationQuickStarters"]
    else:
        new_item["ConversationQuickStarters"] = []

    # ActiveModels
    if "ActiveModels" in item:
        new_item["ActiveModels"] = item["ActiveModels"]

    # BedrockKnowledgeBase
    if "BedrockKnowledgeBase" in item:
        new_item["BedrockKnowledgeBase"] = item["BedrockKnowledgeBase"]

    # GuardrailsParams
    if "GuardrailsParams" in item:
        new_item["GuardrailsParams"] = item["GuardrailsParams"]

    # APIパブリッシュ情報
    if "ApiPublishmentStackName" in item:
        new_item["ApiPublishmentStackName"] = item["ApiPublishmentStackName"]
    if "ApiPublishedDatetime" in item:
        new_item["ApiPublishedDatetime"] = item["ApiPublishedDatetime"]
    if "ApiPublishCodeBuildId" in item:
        new_item["ApiPublishCodeBuildId"] = item["ApiPublishCodeBuildId"]

    # 共有状態の変換
    if "PublicBotId" in item:
        new_item["SharedScope"] = "all"
        new_item["SharedStatus"] = "shared"
    else:
        new_item["SharedStatus"] = "unshared"  # SharedScopeはsparse indexのため設定しない

    # 許可ユーザー・グループ
    new_item["AllowedCognitoUsers"] = []
    new_item["AllowedCognitoGroups"] = []

    # スター状態の変換（ピン留めからスターへ）
    if item.get("IsPinned", False):
        new_item["IsStarred"] = "TRUE"

    # 最終使用時間
    if "LastBotUsed" in item:
        new_item["LastUsedTime"] = item["LastBotUsed"]

    # 使用統計初期化
    new_item["UsageStats"] = {"usage_count": 0}

    return new_item


def convert_alias_item(item: Dict) -> Optional[Dict]:
    """V2エイリアスアイテムをV3形式に変換"""
    user_id = item["PK"]
    original_bot_id = item["OriginalBotId"]

    # 元ボットの所有者IDを取得
    owner_user_id = fetch_original_bot_owner(user_id, original_bot_id)
    if not owner_user_id:
        # 所有者が見つからない場合は処理をスキップ
        logger.warning(
            f"Skipping alias processing for bot {original_bot_id} as owner was not found"
        )
        return None

    new_item = {
        "PK": user_id,
        "SK": f"ALIAS#{original_bot_id}",
        "ItemType": compose_item_type(user_id, "alias"),
        "OriginalBotId": original_bot_id,
        "OwnerUserId": owner_user_id,
        "IsOriginAccessible": True,  # 初期値はTrue
        "Title": item["Title"],
        "Description": item["Description"],
        "CreateTime": item["CreateTime"],
        "SyncStatus": item["SyncStatus"],
        "HasKnowledge": item.get("HasKnowledge", False),
        "HasAgent": item.get("HasAgent", False),
    }

    # ConversationQuickStarters
    if "ConversationQuickStarters" in item:
        new_item["ConversationQuickStarters"] = item["ConversationQuickStarters"]
    else:
        new_item["ConversationQuickStarters"] = []

    # ActiveModels
    if "ActiveModels" in item:
        new_item["ActiveModels"] = item["ActiveModels"]

    # スター状態の変換（ピン留めからスターへ）
    if item.get("IsPinned", False):
        new_item["IsStarred"] = "TRUE"

    # 最終使用時間
    if "LastBotUsed" in item:
        new_item["LastUsedTime"] = item["LastBotUsed"]

    return new_item


def batch_write_items(table, items: List[Dict]):
    """テーブルにアイテムをバッチ書き込み (より詳細なリトライ処理)"""
    if not items:
        return

    client = boto3.client("dynamodb", region_name=REGION)
    total_processed = 0

    # バッチごとに処理
    for i in range(0, len(items), BATCH_SIZE):
        batch = items[i : i + BATCH_SIZE]
        batch_processed = process_batch_with_retries(client, table, batch)
        total_processed += batch_processed

        # 進捗表示
        logger.info(
            f"Processed {min(i + BATCH_SIZE, len(items))} out of {len(items)} items (success: {total_processed})"
        )

        # バッチ間で少し待機してスロットリングを回避
        time.sleep(0.5)

    if total_processed < len(items):
        logger.warning(
            f"⚠️ Only {total_processed} of {len(items)} items were successfully processed"
        )
    else:
        logger.info(f"✅ All {len(items)} items successfully processed")


@retry(
    exceptions=(ClientError),
    tries=5,  # バッチ全体の再試行回数
    delay=2,  # 初回遅延(秒)
    max_delay=30,  # 最大遅延(秒)
    backoff=2,  # 指数バックオフ倍率
    logger=logger,
)
def process_batch_with_retries(client, table, batch_items):
    """単一バッチの処理と詳細なリトライロジック"""
    remaining_items = batch_items
    success_count = 0
    max_item_retries = 3  # 個別アイテムの最大再試行回数

    for attempt in range(max_item_retries):
        if not remaining_items:
            break

        request_items = {
            table.name: [
                {
                    "PutRequest": {
                        "Item": boto3.dynamodb.types.TypeSerializer().serialize(item)["M"]
                    }
                }
                for item in remaining_items
            ]
        }

        try:
            response = client.batch_write_item(RequestItems=request_items)
            unprocessed = response.get("UnprocessedItems", {}).get(table.name, [])

            # この試行で処理できたアイテム数
            processed_this_attempt = len(remaining_items) - len(unprocessed)
            success_count += processed_this_attempt

            # 未処理アイテムがある場合、次の試行用に保存
            if unprocessed:
                # PutRequest.Item から元のアイテムに変換
                remaining_items = [
                    boto3.dynamodb.types.TypeDeserializer().deserialize(
                        {"M": item["PutRequest"]["Item"]}
                    )
                    for item in unprocessed
                ]

                logger.warning(
                    f"Attempt {attempt+1}/{max_item_retries}: {len(unprocessed)} items unprocessed, will retry"
                )
                time.sleep((attempt + 1) * 2)  # 徐々に待機時間を長く
            else:
                # すべて処理完了
                return success_count + len(remaining_items)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ProvisionedThroughputExceededException":
                logger.warning(f"Throughput exceeded on attempt {attempt+1}, backing off")
                # このエラーはリトライデコレータが補足して再試行する
                raise
            else:
                logger.error(f"Unexpected error: {error_code} - {str(e)}")
                raise

    # 最大再試行回数に達した場合
    if remaining_items:
        logger.error(
            f"Failed to process {len(remaining_items)} items after {max_item_retries} attempts"
        )

    return success_count


def migrate_conversations_for_user(user_id: str) -> Tuple[int, int]:
    """ユーザーの会話データを移行"""
    # 会話データの取得
    conversations = get_all_conversations_for_user(user_id)
    related_documents = get_all_related_documents_for_user(user_id)

    # 変換は不要、そのまま新テーブルに書き込む
    if conversations:
        batch_write_items(get_v3_conv_table(), conversations)

    if related_documents:
        batch_write_items(get_v3_conv_table(), related_documents)

    return len(conversations), len(related_documents)


def migrate_user(user_id: str) -> Dict[str, Any]:
    """ユーザーデータのマイグレーション実行"""
    start_time = time.time()
    stats = {
        "user_id": user_id,
        "bots_count": 0,
        "aliases_count": 0,
        "conversations_count": 0,
        "related_documents_count": 0,
        "skipped_aliases_count": 0,
    }

    try:
        # ボット取得と変換
        bots = get_all_bots_for_user(user_id)
        converted_bots = [convert_bot_item(bot) for bot in bots]
        if converted_bots:
            batch_write_items(get_v3_bot_table(), converted_bots)
        stats["bots_count"] = len(converted_bots)

        # エイリアス取得と変換
        aliases = get_all_aliases_for_user(user_id)
        converted_aliases = []
        skipped_aliases = 0

        for alias in aliases:
            converted_alias = convert_alias_item(alias)
            if converted_alias:
                converted_aliases.append(converted_alias)
            else:
                skipped_aliases += 1

        if converted_aliases:
            batch_write_items(get_v3_bot_table(), converted_aliases)
        stats["aliases_count"] = len(converted_aliases)
        stats["skipped_aliases_count"] = skipped_aliases

        # 会話データの移行
        conv_count, doc_count = migrate_conversations_for_user(user_id)
        stats["conversations_count"] = conv_count
        stats["related_documents_count"] = doc_count

        stats["success"] = True
        stats["duration"] = time.time() - start_time

    except Exception as e:
        logger.error(f"Error migrating user {user_id}: {str(e)}")
        stats["success"] = False
        stats["error"] = str(e)
        stats["duration"] = time.time() - start_time

    return stats


def migrate_all_users(users: List[str] = None) -> List[Dict[str, Any]]:
    """全ユーザーのマイグレーション実行"""
    if not users:
        logger.info("No users provided, scanning all users...")
        users = scan_all_users()
        logger.info(f"Found {len(users)} users to migrate")

    stats = []
    total_start = time.time()

    for i, user_id in enumerate(users):
        logger.info(f"Migrating user {i+1}/{len(users)}: {user_id}")
        user_stats = migrate_user(user_id)
        stats.append(user_stats)

    total_duration = time.time() - total_start
    logger.info(f"Migration completed in {total_duration:.2f} seconds")

    return stats


def scan_table_items(table):
    """テーブル全体を効率的にスキャンする"""
    items = []
    last_evaluated_key = None

    while True:
        scan_kwargs = {"ConsistentRead": True}
        if last_evaluated_key:
            scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

        response = table.scan(**scan_kwargs)
        items.extend(response.get("Items", []))

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

    return items


def verify_migration(users: List[str]) -> Dict[str, Any]:
    """マイグレーション結果の検証（V3テーブル構造に対応）"""
    verification = {
        "source": {
            "bots": 0,
            "aliases": 0,
            "conversations": 0,
            "related_documents": 0,
        },
        "destination": {
            "bots": 0,
            "aliases": 0,
            "conversations": 0,
            "related_documents": 0,
        },
        "success": True,
    }

    # ソーステーブルのカウント - 変更なし
    for user_id in users:
        verification["source"]["bots"] += len(get_all_bots_for_user(user_id))
        verification["source"]["aliases"] += len(get_all_aliases_for_user(user_id))
        verification["source"]["conversations"] += len(
            get_all_conversations_for_user(user_id)
        )
        verification["source"]["related_documents"] += len(
            get_all_related_documents_for_user(user_id)
        )

    # 宛先テーブルのカウント - V3の構造に合わせる
    bot_table = get_v3_bot_table()
    conversation_table = get_v3_conv_table()

    # 整合性のため待機
    logger.info("Waiting for DynamoDB consistency...")
    time.sleep(5)

    # テーブルごとにスキャン
    bot_items = scan_items(bot_table, consistent_read=True)
    conversation_items = scan_items(conversation_table, consistent_read=True)

    # ユーザーIDベースでフィルタリング
    user_set = set(users)

    # ボットカウント
    bots_count = sum(
        1
        for item in bot_items
        if item.get("PK") in user_set and item.get("SK", "").startswith("BOT#")
    )
    verification["destination"]["bots"] = bots_count

    # エイリアスカウント
    aliases_count = sum(
        1
        for item in bot_items
        if item.get("PK") in user_set and item.get("SK", "").startswith("ALIAS#")
    )
    verification["destination"]["aliases"] = aliases_count

    # 会話カウント（SKパターンを確認）
    for item in conversation_items:
        if item.get("PK") not in user_set:
            continue

        sk = item.get("SK", "")
        if "#CONV#" in sk:
            verification["destination"]["conversations"] += 1
        elif "#RELATED_DOCUMENT#" in sk:
            verification["destination"]["related_documents"] += 1

    # 検証チェック - 変更なし
    if verification["source"]["bots"] != verification["destination"]["bots"]:
        verification["success"] = False
        verification["error_bots"] = (
            f"Source: {verification['source']['bots']}, Destination: {verification['destination']['bots']}"
        )

    if verification["source"]["aliases"] != verification["destination"]["aliases"]:
        verification["success"] = False
        verification["error_aliases"] = (
            f"Source: {verification['source']['aliases']}, Destination: {verification['destination']['aliases']}"
        )

    if (
        verification["source"]["conversations"]
        != verification["destination"]["conversations"]
    ):
        verification["success"] = False
        verification["error_conversations"] = (
            f"Source: {verification['source']['conversations']}, Destination: {verification['destination']['conversations']}"
        )

    if (
        verification["source"]["related_documents"]
        != verification["destination"]["related_documents"]
    ):
        verification["success"] = False
        verification["error_related_documents"] = (
            f"Source: {verification['source']['related_documents']}, Destination: {verification['destination']['related_documents']}"
        )

    return verification


def save_migration_report(
    stats: List[Dict[str, Any]], verification: Dict[str, Any]
) -> str:
    """マイグレーション統計をJSONファイルに保存"""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"migration_report_{now}.json"

    report = {
        "timestamp": now,
        "source_table": V2_CONVERSATION_TABLE,
        "destination_bot_table": V3_BOT_TABLE,
        "destination_conversation_table": V3_CONVERSATION_TABLE,
        "user_stats": stats,
        "verification": verification,
        "summary": {
            "total_users": len(stats),
            "successful_users": sum(1 for s in stats if s.get("success", False)),
            "failed_users": sum(1 for s in stats if not s.get("success", False)),
            "total_bots": sum(s.get("bots_count", 0) for s in stats),
            "total_aliases": sum(s.get("aliases_count", 0) for s in stats),
            "total_skipped_aliases": sum(
                s.get("skipped_aliases_count", 0) for s in stats
            ),
            "total_conversations": sum(s.get("conversations_count", 0) for s in stats),
            "total_related_documents": sum(
                s.get("related_documents_count", 0) for s in stats
            ),
            "total_duration_seconds": sum(s.get("duration", 0) for s in stats),
        },
    }

    with open(filename, "w") as f:
        json.dump(
            report,
            f,
            indent=2,
        )

    logger.info(f"Migration report saved to {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(description="Migrate data from v2 to v3 schema")
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify migration without migrating data",
    )
    parser.add_argument("--users", nargs="+", help="Specific users to migrate")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be migrated without actually migrating",
    )
    args = parser.parse_args()

    # ユーザーリストを一度だけ取得
    users = args.users
    if not users:
        logger.info("Scanning all users from database...")
        users = scan_all_users()

    logger.info(f"Working with {len(users)} users")

    if args.verify_only:
        logger.info("Verification only mode")
        verification = verify_migration(users)
        print(json.dumps(verification, indent=2, default=str))
        if verification["success"]:
            logger.info("✅ Verification PASSED")
        else:
            logger.error("❌ Verification FAILED")
        return

    if args.dry_run:
        logger.info("Dry run mode - no changes will be made")
        for user_id in users:
            bots = get_all_bots_for_user(user_id)
            aliases = get_all_aliases_for_user(user_id)
            convs = get_all_conversations_for_user(user_id)
            docs = get_all_related_documents_for_user(user_id)

            logger.info(
                f"User {user_id} would migrate: {len(bots)} bots, {len(aliases)} aliases, "
                f"{len(convs)} conversations, {len(docs)} documents"
            )

            # サンプル表示（1つだけ）
            if bots:
                logger.info(
                    f"Sample bot conversion: {json.dumps(convert_bot_item(bots[0]), indent=2, default=str)}"
                )
            if aliases:
                logger.info(
                    f"Sample alias conversion: {json.dumps(convert_alias_item(aliases[0]), indent=2, default=str)}"
                )
        return

    # 実際のマイグレーション実行
    logger.info("Starting migration")
    stats = migrate_all_users(users)

    # 検証
    logger.info("Verifying migration")
    verification = verify_migration(users)

    # レポート保存
    report_file = save_migration_report(stats, verification)
    logger.info(f"Migration completed. Report saved to {report_file}")

    if verification["success"]:
        logger.info("✅ Migration completed successfully")
    else:
        logger.warning(
            "❗ Migration completed with some errors, check the report for details"
        )


if __name__ == "__main__":
    main()
