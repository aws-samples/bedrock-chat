import asyncio
import logging
import os
import re
import time
from datetime import date, datetime, timedelta
from functools import partial
from typing import Any

from app.utils import AEST

import boto3
from app.repositories.common import get_bot_table_client
from app.repositories.models.custom_bot import BotMetaWithStackInfo
from app.repositories.models.usage_analysis import (
    ConversationUsage,
    UsagePerBot,
    UsagePerUser,
)
from boto3.dynamodb.conditions import Attr, Key

REGION = os.environ.get("REGION", "us-east-1")
USAGE_ANALYSIS_DATABASE = os.environ.get(
    "USAGE_ANALYSIS_DATABASE", "bedrockchatstack_usage_analysis"
)
USAGE_ANALYSIS_TABLE = os.environ.get("USAGE_ANALYSIS_TABLE", "ddb_export")
USAGE_ANALYSIS_WORKGROUP = os.environ.get(
    "USAGE_ANALYSIS_WORKGROUP", "bedrockchatstack_wg"
)
USAGE_ANALYSIS_OUTPUT_LOCATION = os.environ.get(
    "USAGE_ANALYSIS_OUTPUT_LOCATION", "s3://bedrockchatstack-athena-results"
)
USER_POOL_ID = os.environ.get("USER_POOL_ID", "us-east-1_XXXXXXXXX")
QUERY_LIMIT = 1000


logger = logging.getLogger(__name__)
athena = boto3.client("athena")


def _find_cognito_user_by_id(user_id: str) -> dict | None:
    """Find user by id from cognito."""
    cognito = boto3.client("cognito-idp")
    try:
        response = cognito.admin_get_user(UserPoolId=USER_POOL_ID, Username=user_id)
    except cognito.exceptions.UserNotFoundException:
        return None
    user_attributes = response["UserAttributes"]

    email = next(
        (attr["Value"] for attr in user_attributes if attr["Name"] == "email"), None
    )

    return {
        "id": user_id,
        "email": email,
    }


async def _find_cognito_users_by_ids(user_ids: list[str]) -> list[dict]:
    """Find users by ids from cognito."""
    loop = asyncio.get_running_loop()
    tasks = [
        loop.run_in_executor(None, partial(_find_cognito_user_by_id, user_id))
        for user_id in user_ids
    ]
    results = await asyncio.gather(*tasks)
    return [result for result in results if result is not None]


async def _query_bot_by_id(bot_id: str) -> list[dict]:
    """Query DynamoDB to find a public bot by bot_id."""
    table = get_bot_table_client()
    response = table.query(
        IndexName="BotIdIndex",
        KeyConditionExpression=Key("BotId").eq(bot_id),
    )
    return response["Items"]


async def _find_bots_by_ids(bot_ids: list[str]) -> dict[str, BotMetaWithStackInfo]:
    """Find bot metadata by a list of bot ids and return a dict keyed by bot_id."""
    loop = asyncio.get_running_loop()

    tasks = []
    for bot_id in bot_ids:
        tasks.append(loop.run_in_executor(None, _query_bot_by_id, bot_id))

    results = await asyncio.gather(*tasks)

    bots_dict = {}
    for items_result in results:
        items = await items_result  # Await the coroutine to get the actual items
        for item in items:
            bot_obj = BotMetaWithStackInfo(
                id=item["BotId"],
                title=item["Title"],
                description=item["Description"],
                create_time=float(item["CreateTime"]),
                last_used_time=float(item.get("LastUsedTime", item["CreateTime"])),
                sync_status=item["SyncStatus"],
                owner_user_id=item["PK"],
                published_api_stack_name=item.get("ApiPublishmentStackName", None),
                published_api_datetime=item.get("ApiPublishedDatetime", None),
                shared_scope=item.get("SharedScope", "private"),
                shared_status=item.get("SharedStatus", "private"),
            )
            bots_dict[item["BotId"]] = bot_obj

    return bots_dict


async def run_athena_query(
    query: str,
    database: str,
    workgroup: str,
    output_location: str,
    query_limit: int = QUERY_LIMIT,
):
    """Run athena query."""
    query_execution = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": database},
        WorkGroup=workgroup,
        ResultConfiguration={
            "OutputLocation": output_location,
        },
    )
    execution_id = query_execution["QueryExecutionId"]
    logger.debug(f"query_execution_id: {execution_id}")

    # Wait until query completed
    while True:
        query_execution = athena.get_query_execution(QueryExecutionId=execution_id)
        status = query_execution["QueryExecution"]["Status"]["State"]
        logger.debug(f"status: {status}")
        if status == "SUCCEEDED":
            break
        elif status == "FAILED":
            reason = query_execution["QueryExecution"]["Status"]["StateChangeReason"]
            logger.error(f"query failed.")
            raise Exception(reason)
        else:
            await asyncio.sleep(1)

    # Get query results
    results = athena.get_query_results(
        QueryExecutionId=execution_id, MaxResults=query_limit
    )
    return results


async def find_bots_sorted_by_price(
    limit: int = 20,
    from_: str | None = None,
    to_: str | None = None,
) -> list[UsagePerBot]:
    """Find bots sorted by price. This is intended to be used by admin.
    - start: start date of the period to be analyzed. The format is `YYYYMMDDHH`.
    - end: end date of the period to be analyzed. The format is `YYYYMMDDHH`.
    """
    assert 1 <= limit <= 1000, "Limit must be between 1 and 1000."

    assert (from_ and to_) or (
        not from_ and not to_
    ), "Both from_ and to_ must be specified or omitted."

    if from_ is not None and to_ is not None:
        from_str = re.sub(r"(\d{4})(\d{2})(\d{2})(\d{2})", r"\1/\2/\3/\4", from_)  # type: ignore
        to_str = re.sub(r"(\d{4})(\d{2})(\d{2})(\d{2})", r"\1/\2/\3/\4", to_)  # type: ignore
    else:
        today = datetime.now(tz=AEST).date()
        from_str = today.strftime("%Y/%m/%d/00")
        to_str = today.strftime("%Y/%m/%d/23")

    # To avoid duplication of conversation, apply most the latest conversation by using subquery
    query = f"""
WITH LatestRecords AS (
    SELECT
        newimage.BotId.S AS BotId,
        newimage.SK.S AS SK,
        MAX(datehour) AS LatestDateHour
    FROM
        {USAGE_ANALYSIS_DATABASE}.{USAGE_ANALYSIS_TABLE}
    WHERE
        datehour BETWEEN '{from_str}' AND '{to_str}'
        AND Keys.SK.S LIKE CONCAT(Keys.PK.S, '#CONV#%')
    GROUP BY
        newimage.BotId.S,
        newimage.SK.S
),
PreAggregatedData AS (
    SELECT
        d.newimage.BotId.S AS BotId,
        d.newimage.SK.S AS SK,
        d.datehour,
        d.newimage.TotalPrice.N AS TotalPrice
    FROM
        {USAGE_ANALYSIS_DATABASE}.{USAGE_ANALYSIS_TABLE} d
    WHERE
        datehour BETWEEN '{from_str}' AND '{to_str}'
        AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
),
AggregatedData AS (
    SELECT
        p.BotId,
        p.TotalPrice
    FROM
        PreAggregatedData p
    JOIN
        LatestRecords lr ON p.BotId = lr.BotId AND p.SK = lr.SK AND p.datehour = lr.LatestDateHour
)
SELECT
    BotId,
    SUM(TotalPrice) AS TotalPrice
FROM
    AggregatedData
GROUP BY
    BotId
ORDER BY
    TotalPrice DESC
LIMIT {limit};
"""

    logger.debug(query)
    response = await run_athena_query(
        query,
        USAGE_ANALYSIS_DATABASE,
        USAGE_ANALYSIS_WORKGROUP,
        USAGE_ANALYSIS_OUTPUT_LOCATION,
    )
    rows = response["ResultSet"]["Rows"][1:]

    bot_ids = [
        row["Data"][0].get("VarCharValue", "")
        for row in rows
        if row["Data"][0].get("VarCharValue", None) is not None
    ]

    # Fetch bot meta data directly
    bots_dict = await _find_bots_by_ids(bot_ids)

    # Join bot meta data and usage data
    bot_usage = []
    for row in rows:
        bot_id = row["Data"][0].get("VarCharValue", "")
        total_price = float(row["Data"][1].get("VarCharValue", 0))

        bot = bots_dict.get(bot_id)

        if bot:
            bot_usage.append(
                UsagePerBot(
                    id=bot_id,
                    title=bot.title,
                    description=bot.description,
                    published_api_stack_name=bot.published_api_stack_name,
                    published_api_datetime=bot.published_api_datetime,
                    owner_user_id=bot.owner_user_id,
                    total_price=total_price,
                    shared_scope=bot.shared_scope,
                    shared_status=bot.shared_status,
                )
            )

    return bot_usage


async def find_users_sorted_by_price(
    limit: int = 20,
    from_: str | None = None,
    to_: str | None = None,
) -> list[UsagePerUser]:
    assert 1 <= limit <= 1000, "Limit must be between 1 and 1000."

    assert (from_ and to_) or (
        not from_ and not to_
    ), "Both from_ and to_ must be specified or omitted."

    if from_ is not None and to_ is not None:
        from_str = re.sub(r"(\d{4})(\d{2})(\d{2})(\d{2})", r"\1/\2/\3/\4", from_)  # type: ignore
        to_str = re.sub(r"(\d{4})(\d{2})(\d{2})(\d{2})", r"\1/\2/\3/\4", to_)  # type: ignore
    else:
        today = datetime.now(tz=AEST).date()
        from_str = today.strftime("%Y/%m/%d/00")
        to_str = today.strftime("%Y/%m/%d/23")

    # To avoid duplication of conversation, apply most the latest conversation by using subquery
    query = f"""
WITH LatestRecords AS (
    SELECT
        newimage.PK.S AS UserId,
        newimage.SK.S AS SK,
        MAX(datehour) AS LatestDateHour
    FROM
        {USAGE_ANALYSIS_DATABASE}.{USAGE_ANALYSIS_TABLE}
    WHERE
        datehour BETWEEN '{from_str}' AND '{to_str}'
        AND Keys.SK.S LIKE CONCAT(Keys.PK.S, '#CONV#%')
    GROUP BY
        newimage.PK.S,
        newimage.SK.S
),
PreAggregatedData AS (
    SELECT
        d.newimage.PK.S AS UserId,
        d.newimage.SK.S AS SK,
        d.datehour,
        d.newimage.TotalPrice.N AS TotalPrice
    FROM
        {USAGE_ANALYSIS_DATABASE}.{USAGE_ANALYSIS_TABLE} d
    WHERE
        datehour BETWEEN '{from_str}' AND '{to_str}'
        AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
),
AggregatedData AS (
    SELECT
        p.UserId,
        p.TotalPrice
    FROM
        PreAggregatedData p
    JOIN
        LatestRecords lr ON p.UserId = lr.UserId AND p.SK = lr.SK AND p.datehour = lr.LatestDateHour
)
SELECT
    UserId,
    SUM(TotalPrice) AS TotalPrice
FROM
    AggregatedData
GROUP BY
    UserId
ORDER BY
    TotalPrice DESC
LIMIT {limit};
"""

    logger.debug(query)
    response = await run_athena_query(
        query,
        USAGE_ANALYSIS_DATABASE,
        USAGE_ANALYSIS_WORKGROUP,
        USAGE_ANALYSIS_OUTPUT_LOCATION,
    )
    rows = response["ResultSet"]["Rows"][1:]

    users = await _find_cognito_users_by_ids(
        user_ids=[
            item["Data"][0]["VarCharValue"]
            for item in rows
            if item["Data"][0].get("VarCharValue", None) is not None
        ]
    )
    users_dict = {user["id"]: user for user in users}
    usages = []
    for row in rows:
        user_id = row["Data"][0].get("VarCharValue", "")
        total_price = float(row["Data"][1].get("VarCharValue", 0))

        user = users_dict.get(user_id)
        if user:
            usages.append(
                UsagePerUser(
                    id=user_id,
                    email=user["email"],
                    total_price=total_price,
                )
            )
    return usages


async def find_conversations_by_user(
    user_id: str,
    limit: int = 100,
    from_: str | None = None,
    to_: str | None = None,
) -> list[ConversationUsage]:
    """Find conversations for a specific user sorted by create time descending.
    - user_id: the Cognito user ID (PK in the conversation table).
    - limit: must be between 1 and 1000.
    - from_: start date in `YYYYMMDDHH` format.
    - to_: end date in `YYYYMMDDHH` format.
    - If from_ and to_ are omitted, defaults to today 00:00–23:00.
    """
    assert 1 <= limit <= 1000, "Limit must be between 1 and 1000."
    assert (from_ and to_) or (
        not from_ and not to_
    ), "Both from_ and to_ must be specified or omitted."

    # Validate user_id to prevent SQL injection (Cognito UUIDs are alphanumeric + hyphens)
    if not re.match(r"^[a-zA-Z0-9_\-]+$", user_id):
        raise ValueError(f"Invalid user_id format: {user_id}")

    if from_ is not None and to_ is not None:
        from_str = re.sub(r"(\d{4})(\d{2})(\d{2})(\d{2})", r"\1/\2/\3/\4", from_)
        to_str = re.sub(r"(\d{4})(\d{2})(\d{2})(\d{2})", r"\1/\2/\3/\4", to_)
    else:
        today = datetime.now(tz=AEST).date()
        from_str = today.strftime("%Y/%m/%d/00")
        to_str = today.strftime("%Y/%m/%d/23")

    query = f"""
WITH LatestRecords AS (
    SELECT
        newimage.SK.S AS SK,
        MAX(datehour) AS LatestDateHour
    FROM
        {USAGE_ANALYSIS_DATABASE}.{USAGE_ANALYSIS_TABLE}
    WHERE
        datehour BETWEEN '{from_str}' AND '{to_str}'
        AND Keys.PK.S = '{user_id}'
        AND Keys.SK.S LIKE CONCAT(Keys.PK.S, '#CONV#%')
    GROUP BY
        newimage.SK.S
),
ConversationData AS (
    SELECT
        d.newimage.SK.S AS SK,
        d.newimage.Title.S AS Title,
        d.newimage.CreateTime.N AS CreateTime,
        d.newimage.TotalPrice.N AS TotalPrice,
        d.newimage.BotId.S AS BotId,
        d.datehour
    FROM
        {USAGE_ANALYSIS_DATABASE}.{USAGE_ANALYSIS_TABLE} d
    WHERE
        datehour BETWEEN '{from_str}' AND '{to_str}'
        AND d.Keys.PK.S = '{user_id}'
        AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
)
SELECT
    cd.SK,
    cd.Title,
    cd.CreateTime,
    cd.TotalPrice,
    cd.BotId
FROM ConversationData cd
JOIN LatestRecords lr ON cd.SK = lr.SK AND cd.datehour = lr.LatestDateHour
ORDER BY cd.CreateTime DESC
LIMIT {limit};
"""

    logger.debug(query)
    response = await run_athena_query(
        query,
        USAGE_ANALYSIS_DATABASE,
        USAGE_ANALYSIS_WORKGROUP,
        USAGE_ANALYSIS_OUTPUT_LOCATION,
    )
    rows = response["ResultSet"]["Rows"][1:]

    conversations = []
    for row in rows:
        data = row["Data"]
        sk = data[0].get("VarCharValue", "")
        title = data[1].get("VarCharValue", "")
        create_time_str = data[2].get("VarCharValue", "0")
        total_price_str = data[3].get("VarCharValue", "0")
        bot_id = data[4].get("VarCharValue", None) or None

        # Extract conversation ID from SK: "{user_id}#CONV#{conversation_id}"
        conv_id = sk.split("#CONV#", 1)[1] if "#CONV#" in sk else sk

        conversations.append(
            ConversationUsage(
                id=conv_id,
                title=title,
                create_time=float(create_time_str),
                total_price=float(total_price_str),
                bot_id=bot_id,
            )
        )

    return conversations
