"""Usage analysis repository."""

import asyncio
import json
import logging
import os
import re
import time
from datetime import date, datetime, timedelta, UTC
from functools import partial
from typing import Dict, List, Optional, Any, Union, Tuple
from decimal import Decimal, InvalidOperation

import boto3
from boto3.dynamodb.conditions import Key # Import Key for DDB queries if needed later
from botocore.exceptions import ClientError

from app.repositories.common import RecordNotFoundError

from app.repositories.models.usage_analysis import (
    DailyUsage,
    TopicAnalysis,
    BotAnalytics,
    AnalyticsDashboard,
    AnalyticsSummary,
    UsagePerUser as ModelUsagePerUser,
)
from app.routes.schemas.analytics import UsagePerUserOutput, UsagePerBotOutput
from app.user import User
from app.repositories.metadata_repository import MetadataRepository

REGION = os.environ.get("REGION", "us-east-1")
USAGE_ANALYSIS_DATABASE = os.environ.get("USAGE_ANALYSIS_DATABASE", "")
USAGE_ANALYSIS_TABLE = os.environ.get("USAGE_ANALYSIS_TABLE", "")
USAGE_ANALYSIS_WORKGROUP = os.environ.get("USAGE_ANALYSIS_WORKGROUP", "")
USAGE_ANALYSIS_OUTPUT_LOCATION = os.environ.get("USAGE_ANALYSIS_OUTPUT_LOCATION", "")
USER_POOL_ID = os.environ.get("USER_POOL_ID", "")
BOTS_ANALYTICS_TABLE_ARN = os.environ.get("BOTS_ANALYTICS_TABLE_ARN", "")
QUERY_LIMIT = 1000



logger = logging.getLogger(__name__)
athena_client = boto3.client("athena")
cognito_client = boto3.client("cognito-idp")

# Function to extract table name from Glue table ARN
def get_table_name_from_arn(arn: str) -> str:
    if not arn:
        return ""
    # Format: arn:aws:glue:<region>:<account-id>:table/<database-name>/<table-name>
    return arn.split('/')[-1]

# Extract the table name
BOTS_ANALYTICS_TABLE_NAME = get_table_name_from_arn(BOTS_ANALYTICS_TABLE_ARN)

logger = logging.getLogger(__name__)
athena_client = boto3.client("athena")

def _find_cognito_user_by_id(user_id: str) -> dict | None:
    """Find user by id from cognito."""
    if not USER_POOL_ID:
        logger.error("USER_POOL_ID not configured. Cannot fetch Cognito user.")
        return None
    try:
        response = cognito_client.admin_get_user(UserPoolId=USER_POOL_ID, Username=user_id)
        user_attributes = response["UserAttributes"]
        email = next((attr["Value"] for attr in user_attributes if attr["Name"] == "email"), None)
        # Add other attributes if needed, e.g., name
        # name = next((attr["Value"] for attr in user_attributes if attr["Name"] == "name"), None)
        return {"id": user_id, "email": email}
    except cognito_client.exceptions.UserNotFoundException:
        logger.warning(f"Cognito user not found: {user_id}")
        return None
    except Exception as e:
        logger.error(f"Error fetching cognito user {user_id}: {e}", exc_info=True)
        return None

async def _find_cognito_users_by_ids(user_ids: list[str]) -> dict[str, dict]:
    """Find users by ids from cognito, handling potential errors. Returns a dict mapping id to user data."""
    users_dict: Dict[str, Dict] = {}
    if not user_ids or not USER_POOL_ID:
        return users_dict

    # Remove duplicates and empty strings
    unique_user_ids = list(set(uid for uid in user_ids if uid))
    if not unique_user_ids:
        return users_dict

    loop = asyncio.get_running_loop()
    # Batching might be needed for very large lists, but Cognito BatchGetUser is not standard
    # For now, run concurrently
    tasks = [loop.run_in_executor(None, partial(_find_cognito_user_by_id, user_id)) for user_id in unique_user_ids]

    results = await asyncio.gather(*tasks)
    for result in results:
        if result and result.get("id"):
            users_dict[result["id"]] = result

    logger.info(f"Fetched Cognito info for {len(users_dict)} out of {len(unique_user_ids)} unique requested users.")
    return users_dict

async def run_athena_query(
    query: str,
    database: str = USAGE_ANALYSIS_DATABASE, # Default to primary usage analysis DB
    workgroup: str = USAGE_ANALYSIS_WORKGROUP, # Default to primary usage analysis WG
    output_location: str = USAGE_ANALYSIS_OUTPUT_LOCATION, # Default to primary usage analysis output
    max_wait_time: int = 180, # 3 minutes timeout
) -> Dict[str, Any]:
    """Run athena query and wait for completion. Returns raw Athena GetQueryResults response."""
    logger.debug(f"Starting Athena query execution in database: {database}, workgroup: {workgroup}")
    logger.debug(f"Output location: {output_location}")
    logger.debug(f"EXECUTING ATHENA QUERY:\n{query}") # Log full query at DEBUG

    try:
        query_execution = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database},
            WorkGroup=workgroup,
            ResultConfiguration={
                "OutputLocation": output_location,
            },
        )
        execution_id = query_execution["QueryExecutionId"]
        logger.info(f"Athena query execution started. Execution ID: {execution_id}")

        start_time = time.time()
        last_log_time = start_time
        while True:
            current_time = time.time()
            if current_time - start_time > max_wait_time:
                logger.warning(f"Athena query {execution_id} exceeded max wait time ({max_wait_time}s). Attempting to stop.")
                try:
                    athena_client.stop_query_execution(QueryExecutionId=execution_id)
                except ClientError as stop_err:
                     logger.error(f"Failed to stop timed out Athena query {execution_id}: {stop_err}")
                raise TimeoutError(f"Query execution {execution_id} timed out after {max_wait_time} seconds")

            query_execution = athena_client.get_query_execution(QueryExecutionId=execution_id)
            status = query_execution["QueryExecution"]["Status"]["State"]

            if status == "SUCCEEDED":
                elapsed_time = current_time - start_time
                logger.info(f"Athena query {execution_id} succeeded after {elapsed_time:.2f} seconds")
                break
            elif status in ["FAILED", "CANCELLED"]:
                reason = query_execution["QueryExecution"]["Status"].get("StateChangeReason", "No reason provided")
                logger.error(f"Athena query {execution_id} {status} after {current_time - start_time:.2f} seconds. Reason: {reason}")
                # Log the failed query at ERROR level for easier debugging
                logger.error(f"Failed/Cancelled Athena Query (ID: {execution_id}):\n{query}")
                raise Exception(f"Athena query {execution_id} {status}. Reason: {reason}")
            else: # QUEUED, RUNNING
                # Log progress periodically
                if current_time - last_log_time > 10: # Log every 15 seconds
                     logger.info(f"Waiting for Athena query {execution_id}. Status: {status}, Elapsed: {current_time - start_time:.0f}s")
                     last_log_time = current_time
                await asyncio.sleep(2) # Check status every 2 seconds

        logger.debug(f"Retrieving Athena query results for {execution_id} with limit: {QUERY_LIMIT}")
        results = athena_client.get_query_results(
            QueryExecutionId=execution_id, MaxResults=QUERY_LIMIT # Limit results fetched
        )

        row_count = len(results.get("ResultSet", {}).get("Rows", []))
        data_row_count = max(0, row_count -1) # Subtract header if present
        logger.info(f"Athena query {execution_id} returned {data_row_count} data rows (fetched up to limit {QUERY_LIMIT}).")

        # Log schema and sample data if available
        if row_count > 0:
            try:
                metadata = results.get("ResultSet", {}).get("ResultSetMetadata", {})
                if metadata:
                    column_info = metadata.get("ColumnInfo", [])
                    schema_str = ', '.join([f'{col.get("Name")}:{col.get("Type")}' for col in column_info])
                    logger.debug(f"Athena query {execution_id} result schema: {schema_str}")

                if data_row_count == 0 and row_count > 0:
                     logger.info(f"Athena query {execution_id} returned schema but NO DATA rows.")
                elif data_row_count > 0:
                    first_data_row_raw = results["ResultSet"]["Rows"][1].get("Data", [])
                    if first_data_row_raw and column_info:
                         sample_data = {column_info[i].get('Name'): row.get('VarCharValue', 'NULL')
                                      for i, row in enumerate(first_data_row_raw) if i < len(column_info)}
                         logger.debug(f"Sample data (first row) for {execution_id}: {sample_data}")
            except Exception as parse_err:
                 logger.warning(f"Error parsing result schema/sample data for {execution_id}: {parse_err}")

        return results
    except ClientError as e:
         error_code = e.response.get("Error", {}).get("Code")
         error_message = e.response.get("Error", {}).get("Message", str(e))
         logger.error(f"AWS ClientError running Athena query: {error_code} - {error_message}", exc_info=True)
         logger.error(f"Failed Athena Query (ClientError):\n{query}")
         raise # Re-raise the exception
    except Exception as e:
        logger.error(f"Unexpected error in run_athena_query: {str(e)}", exc_info=True)
        logger.error(f"Failed Athena Query (Unexpected Error):\n{query}")
        raise

async def _execute_athena_query(query: str) -> List[Dict[str, Any]]:
    """Executes an Athena query and parses the results into a list of dictionaries."""
    logger.debug(f"Executing helper _execute_athena_query")
    try:
        response = await run_athena_query(query) # Use default DB, WG, Output

        rows = response.get("ResultSet", {}).get("Rows", [])
        if not rows or len(rows) <= 1: # No data rows, only header possibly
             logger.info("Athena query returned no data rows.")
             return []

        header_data = rows[0].get("Data", [])
        column_names = [col.get("VarCharValue") for col in header_data]
        # Filter out potential None column names if header parsing failed
        valid_column_names = [name for name in column_names if name is not None]
        if len(valid_column_names) != len(column_names):
            logger.warning("Header row contained missing column names.")

        parsed_results = []
        for row in rows[1:]: # Skip header row
            row_data = {}
            values = row.get("Data", [])
            for i, col_name in enumerate(valid_column_names):
                 if i < len(values):
                    # Store value as string, let caller handle type conversion
                    # Handle potential missing VarCharValue key
                    row_data[col_name] = values[i].get("VarCharValue")
            if row_data: # Avoid adding empty rows
                parsed_results.append(row_data)

        logger.debug(f"Parsed {len(parsed_results)} rows from Athena result.")
        return parsed_results

    except Exception as e:
        # Error is logged within run_athena_query or here
        logger.error(f"Error during _execute_athena_query wrapper: {e}", exc_info=True)
        return [] # Return empty list on error


def _format_datetime_for_athena(dt: Optional[datetime] = None) -> str:
    """Format datetime for Athena queries (YYYY/MM/DD/HH). Defaults to now UTC."""
    if dt is None:
        dt = datetime.now(UTC)
    # Ensure timezone is handled, default to UTC if naive
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    else:
        dt = dt.astimezone(UTC)
    # Format includes hour
    return dt.strftime("%Y/%m/%d/%H")

def _format_date_range(from_str: Optional[str], to_str: Optional[str]) -> Tuple[str, str]:
    """Parses YYYYMMDD or YYYYMMDDHH input strings and returns formatted Athena date strings."""
    # Default 'from' is 30 days ago, start of day UTC
    default_from_dt = (datetime.now(UTC) - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
    # Default 'to' is now UTC
    default_to_dt = datetime.now(UTC)

    try:
        if from_str and len(from_str) == 8:
            from_dt = datetime.strptime(from_str, "%Y%m%d").replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=UTC)
        elif from_str and len(from_str) == 10:
            from_dt = datetime.strptime(from_str, "%Y%m%d%H").replace(tzinfo=UTC)
        else:
            from_dt = default_from_dt
    except ValueError:
        logger.warning(f"Invalid 'from_date' format: {from_str}. Using default.")
        from_dt = default_from_dt

    try:
        if to_str and len(to_str) == 8:
            # Include the entire day
            to_dt = datetime.strptime(to_str, "%Y%m%d").replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=UTC)
        elif to_str and len(to_str) == 10:
             # Include the entire hour specified
             to_dt = datetime.strptime(to_str, "%Y%m%d%H").replace(minute=59, second=59, microsecond=999999, tzinfo=UTC)
        else:
             to_dt = default_to_dt
    except ValueError:
        logger.warning(f"Invalid 'to_date' format: {to_str}. Using default.")
        to_dt = default_to_dt

    # Format for Athena
    from_hour_str = _format_datetime_for_athena(from_dt)
    # Format 'to' date's hour string correctly for comparison (use the calculated datetime)
    to_hour_str = _format_datetime_for_athena(to_dt)


    logger.debug(f"Formatted date range for Athena: {from_hour_str} to {to_hour_str}")
    return from_hour_str, to_hour_str

def _build_common_where_clauses(
    from_hour_str: str,
    to_hour_str: str,
    filter_bot_ids: Optional[List[str]] = None
) -> Tuple[str, str]:
    """Builds date and bot ID WHERE clauses for Athena queries against DDB export table."""

    # 1. Date Clause (Always present)
    # Use datehour which is expected to be YYYY/MM/DD/HH format string
    date_clause = f"datehour >= '{from_hour_str}' AND datehour <= '{to_hour_str}'"


    # If filter_bot_ids is None or empty list, scan all partitions
    # 2. Bot ID Filter Clause
    MAX_IN_CLAUSE_ITEMS = 800
    botid_filter_clause = ""
    # Define the field for bot ID - **CRITICAL**: Adjust to match your Glue schema
    # Examples: NewImage.BotId.S, OldImage.BotId.S, bot_id
    # Assuming it's nested under NewImage or OldImage for DDB exports:
    bot_id_field = "COALESCE(NewImage.BotId.S, OldImage.BotId.S)"

    if filter_bot_ids:
        valid_bot_ids = [str(id) for id in filter_bot_ids if id] # Ensure strings, filter empty
        if valid_bot_ids:
            if len(valid_bot_ids) <= MAX_IN_CLAUSE_ITEMS:
                # Escape single quotes in bot IDs
                safe_bot_ids = [id.replace("'", "''") for id in valid_bot_ids]
                formatted_bot_ids = ', '.join([f"'{id}'" for id in safe_bot_ids])
                botid_filter_clause = f"AND {bot_id_field} IN ({formatted_bot_ids})"
            else:
                logger.warning(f"Bot ID list length ({len(valid_bot_ids)}) exceeds threshold ({MAX_IN_CLAUSE_ITEMS}). Omitting direct BotId IN clause.")
                # Rely solely on date filter if list is too long - comment below was inaccurate
                # Rely solely on partition filter if list is too long

    logger.debug(f"Built clauses: date='{date_clause}', botid='{botid_filter_clause}'")
    return date_clause, botid_filter_clause

# --- Main Repository Functions ---

async def get_summary_and_daily_data(
    from_str: Optional[str] = None,
    to_str: Optional[str] = None,
    filter_bot_ids: Optional[List[str]] = None
) -> Tuple[AnalyticsSummary, List[DailyUsage]]:
    """Fetches summary stats and daily usage, applying partition filters."""
    bots_filter_info = f"{len(filter_bot_ids)} bots specified" if filter_bot_ids else "all bots (no filter)"
    logger.info(f"Getting summary/daily data: from={from_str}, to={to_str}, bots_filter={bots_filter_info}")
    from_hour_str, to_hour_str = _format_date_range(from_str, to_str)
    date_clause, botid_filter_clause = _build_common_where_clauses(
        from_hour_str, to_hour_str, filter_bot_ids
    )

    # Field definitions
    input_tokens_field = "COALESCE(CAST(newimage.InputTokens.N AS bigint), 0)"
    output_tokens_field = "COALESCE(CAST(newimage.OutputTokens.N AS bigint), 0)"
    cost_field = "COALESCE(CAST(newimage.TotalPrice.N AS DECIMAL(20,10)), 0.0)"
    session_id_field = "Keys.SK.S"
    create_time_field = "COALESCE(CAST(newimage.CreateTime.N AS double), CAST(OldImage.CreateTime.N AS double))"
    usage_date_field = f"date_trunc('day', from_unixtime({create_time_field}))"
    # Use json_size again for CORRECT message counting (entries in MessageMap)
    message_count_field = "CAST(GREATEST(COALESCE(TRY((json_size(JSON_PARSE(newimage.MessageMap.S), '$') - 2) / 2.0), 0), 0) AS INTEGER)"
    user_id_field = "newimage.PK.S"
    bot_id_field = "newimage.BotId.S"

    # Correct Filter
    conversation_filter = "AND Keys.SK.S LIKE CONCAT(Keys.PK.S, '#CONV#%')"
    cost_exists_filter = "AND newimage.TotalPrice.N IS NOT NULL"

    # Revert query structure BUT use correct message count logic
    query_daily = f"""
    SELECT
        DATE_FORMAT(PARSE_DATETIME(datehour, 'yyyy/MM/dd/HH'), '%Y-%m-%d') as day,
        COUNT(DISTINCT Keys.SK.S) as daily_sessions,
        SUM({message_count_field}) as daily_messages, -- Use SUM of json_size per record
        SUM(COALESCE(CAST(newimage.InputTokens.N as BIGINT), 0)) as daily_input_tokens,
        SUM(COALESCE(CAST(newimage.OutputTokens.N as BIGINT), 0)) as daily_output_tokens,
        SUM(COALESCE(CAST(newimage.TotalPrice.N as DECIMAL(20,10)), 0.0)) as daily_cost
    FROM
        "{USAGE_ANALYSIS_DATABASE}"."{USAGE_ANALYSIS_TABLE}"
    WHERE
        {date_clause}
        {botid_filter_clause}
        {conversation_filter}
        -- Keep cost filter? Let's assume TotalPrice might be null even if MessageMap exists
        -- {cost_exists_filter} -- Remove cost filter from WHERE for wider message counting?
        -- Let's keep the conversation filter ONLY for daily summary
    GROUP BY
        DATE_FORMAT(PARSE_DATETIME(datehour, 'yyyy/MM/dd/HH'), '%Y-%m-%d')
    ORDER BY
        day ASC
    """

    # Query to count total unique bots and users
    query_entity_counts = f"""
    SELECT
        COUNT(DISTINCT {bot_id_field}) as total_bots,
        COUNT(DISTINCT {user_id_field}) as total_users
    FROM
        "{USAGE_ANALYSIS_DATABASE}"."{USAGE_ANALYSIS_TABLE}"
    WHERE
        {date_clause}
        {botid_filter_clause}
        {conversation_filter}
        AND {bot_id_field} IS NOT NULL
        AND {user_id_field} IS NOT NULL
    """

    # Execute the corrected daily query
    results_daily = await _execute_athena_query(query_daily)
    results_counts = await _execute_athena_query(query_entity_counts)

    # Extract total bots and users counts
    total_bots = 0
    total_users = 0
    if results_counts and len(results_counts) > 0:
        total_bots = int(results_counts[0].get('total_bots', 0) or 0)
        total_users = int(results_counts[0].get('total_users', 0) or 0)
        logger.info(f"Entity counts: {total_bots} unique bots, {total_users} unique users")

    # Process results (field names match the reverted query)
    daily_usage_list: List[DailyUsage] = []
    total_sessions_agg = 0
    total_messages_agg = 0
    total_input_tokens_agg = 0
    total_output_tokens_agg = 0
    total_cost_agg = Decimal("0.0")

    for row in results_daily:
        try:
            day_str = row.get('day')
            if not day_str: continue

            # Adjust field names based on the reverted query_daily aliases
            daily_sessions = int(row.get('daily_sessions', 0) or 0)
            daily_messages = int(row.get('daily_messages', 0) or 0) # From SUM(json_size)
            daily_input = int(row.get('daily_input_tokens', 0) or 0)
            daily_output = int(row.get('daily_output_tokens', 0) or 0)
            
            # --- Added Logging --- 
            raw_daily_cost = row.get('daily_cost') # Get raw value from Athena result
            logger.debug(f"Processing daily row for {day_str}. Raw daily_cost from Athena: '{raw_daily_cost}' (Type: {type(raw_daily_cost)})")
            # --- End Added Logging ---
            
            # Handle potential None or empty string before Decimal conversion
            daily_cost_str = str(raw_daily_cost or '0.0') # Default to '0.0' if None or empty
            if not daily_cost_str.strip(): # Handle empty strings after potential str conversion
                daily_cost_str = '0.0'
                logger.warning(f"Raw daily_cost for {day_str} was empty string after defaulting None; using '0.0'.")

            daily_cost = Decimal(daily_cost_str) # Convert potentially cleaned string to Decimal
            
            # --- Added Logging ---
            cost_to_pass = daily_cost if daily_cost is not None else None
            logger.debug(f"Value being passed to DailyUsage cost field for {day_str}: {cost_to_pass} (Type: {type(cost_to_pass)}) - Original Decimal was: {daily_cost}")
            # --- End Added Logging ---
            
            daily_usage_list.append(DailyUsage(
                date=day_str,
                num_sessions=daily_sessions,
                num_messages=daily_messages, # Using SUM(json_size) now
                input_tokens=daily_input,
                output_tokens=daily_output,
                cost=cost_to_pass # Use the prepared value
            ))

            # Accumulate totals
            total_sessions_agg += daily_sessions
            total_messages_agg += daily_messages
            total_input_tokens_agg += daily_input
            total_output_tokens_agg += daily_output
            # Ensure accumulation handles potential None if logic changes
            total_cost_agg += daily_cost if daily_cost is not None else Decimal("0.0")

        except (ValueError, TypeError, InvalidOperation) as e:
             logger.warning(f"Skipping daily data row due to parsing error: {e}. Row: {row}")
             continue

    summary = AnalyticsSummary(
        num_sessions=total_sessions_agg,
        num_messages=total_messages_agg, # Using SUM(json_size)
        input_tokens=total_input_tokens_agg,
        output_tokens=total_output_tokens_agg,
        cost=total_cost_agg if total_cost_agg is not None else None, # Pass Decimal or None directly
        total_bots=total_bots,
        total_users=total_users
    )

    logger.info(f"Summary/Daily Data (Corrected Message Count): {summary.num_sessions} sessions, {summary.num_messages} messages, {summary.input_tokens} input tokens, {summary.output_tokens} output tokens retrieved. Unique entities: {total_bots} bots, {total_users} users.")
    return summary, daily_usage_list

async def _get_total_sessions(from_hour_str: str, to_hour_str: str, filter_bot_ids: Optional[List[str]]) -> int:
    # ... (This function remains deprecated and returns 0) ...
    logger.warning("_get_total_sessions is deprecated; session count now aggregated in get_summary_and_daily_data.")
    return 0

async def get_top_entities(
    from_str: Optional[str] = None,
    to_str: Optional[str] = None,
    limit: int = 10,
    filter_bot_ids: Optional[List[str]] = None
) -> Dict[str, List]:
    """Fetches top bots and users using new partitioning and filtering."""
    bots_filter_info = f"{len(filter_bot_ids)} bots specified" if filter_bot_ids else "all bots (no filter)"
    logger.info(f"Getting top entities (Corrected Message Count): from={from_str}, to={to_str}, limit={limit}, bots_filter={bots_filter_info}")
    from_hour_str, to_hour_str = _format_date_range(from_str, to_str)
    date_clause, botid_filter_clause = _build_common_where_clauses(
        from_hour_str, to_hour_str, filter_bot_ids
    )

    # Field definitions
    user_id_field = "newimage.PK.S"
    bot_id_field = "newimage.BotId.S"
    cost_field = "COALESCE(CAST(newimage.TotalPrice.N AS DECIMAL(20,10)), 0.0)"
    input_tokens_field = "COALESCE(CAST(newimage.InputTokens.N AS bigint), 0)"
    output_tokens_field = "COALESCE(CAST(newimage.OutputTokens.N AS bigint), 0)"
    session_id_field = "Keys.SK.S"
    # Use json_size for CORRECT message counting
    # message_count_field = "COALESCE(TRY(json_size(JSON_PARSE(newimage.MessageMap.S), '$')), 0)"
    message_count_field = "CAST(GREATEST(COALESCE(TRY((json_size(JSON_PARSE(newimage.MessageMap.S), '$') - 2) / 2.0), 0), 0) AS INTEGER)"

    # Correct Filter
    conversation_filter = "AND Keys.SK.S LIKE CONCAT(Keys.PK.S, '#CONV#%')"

    # Top users query with corrected message count
    top_users_query = f'''
    SELECT
        {user_id_field} as user_id,
        SUM({cost_field}) as total_cost,
        COUNT(DISTINCT {session_id_field}) as num_sessions,
        SUM({message_count_field}) as total_messages, -- Use SUM(json_size)
        SUM({input_tokens_field}) as total_input_tokens,
        SUM({output_tokens_field}) as total_output_tokens
    FROM "{USAGE_ANALYSIS_DATABASE}"."{USAGE_ANALYSIS_TABLE}"
    WHERE
        {date_clause}
        {botid_filter_clause}
        {conversation_filter}
        AND {user_id_field} IS NOT NULL
    GROUP BY {user_id_field}
    ORDER BY total_cost DESC
    LIMIT {limit}
    '''

    # Top bots query with corrected message count
    top_bots_query = f'''
    SELECT
        {bot_id_field} as bot_id,
        SUM({cost_field}) as total_cost,
        COUNT(DISTINCT {user_id_field}) as num_users,
        COUNT(DISTINCT {session_id_field}) as num_sessions,
        SUM({message_count_field}) as total_messages, -- Use SUM(json_size)
        SUM({input_tokens_field}) as total_input_tokens,
        SUM({output_tokens_field}) as total_output_tokens
    FROM "{USAGE_ANALYSIS_DATABASE}"."{USAGE_ANALYSIS_TABLE}"
    WHERE
        {date_clause}
        {botid_filter_clause}
        {conversation_filter}
        AND {bot_id_field} IS NOT NULL
    GROUP BY {bot_id_field}
    ORDER BY total_cost DESC
    LIMIT {limit}
    '''

    top_users_result_output: List[UsagePerUserOutput] = []
    top_bots_result_output: List[UsagePerBotOutput] = []

    try:
        logger.debug("Starting concurrent execution for top users and top bots queries (Corrected Message Count).")
        user_results_task = asyncio.create_task(_execute_athena_query(top_users_query))
        bot_results_task = asyncio.create_task(_execute_athena_query(top_bots_query))
        user_results, bot_results = await asyncio.gather(user_results_task, bot_results_task)
        logger.debug(f"Top users query returned {len(user_results)} rows. Top bots query returned {len(bot_results)} rows.")

        # --- Process User Results ---
        user_ids = [r.get('user_id') for r in user_results if r.get('user_id')]
        user_cognito_map = await _find_cognito_users_by_ids(user_ids)

        for row in user_results:
            user_id = row.get('user_id')
            if not user_id: continue
            try:
                cognito_info = user_cognito_map.get(user_id, {})
                total_price_str = str(row.get('total_cost', '0.0') or '0.0')
                total_price = Decimal(total_price_str)
                num_sessions = int(row.get('num_sessions', 0) or 0)
                total_messages = int(row.get('total_messages', 0) or 0) # From SUM(json_size)
                total_input_tokens = int(row.get('total_input_tokens', 0) or 0)
                total_output_tokens = int(row.get('total_output_tokens', 0) or 0)

                top_users_result_output.append(UsagePerUserOutput(
                    id=user_id,
                    email=cognito_info.get('email', 'Not Found'),
                    total_price=total_price,
                    num_sessions=num_sessions,
                    message_count=total_messages,
                    input_tokens=total_input_tokens,
                    output_tokens=total_output_tokens
                ))
            except (ValueError, TypeError, InvalidOperation) as parse_error:
                logger.warning(f"Skipping user result row due to parsing error: {parse_error}. Row: {row}")
                continue

        # --- Process Bot Results ---
        bot_ids = [r.get('bot_id') for r in bot_results if r.get('bot_id')]
        bot_metadata_map = await MetadataRepository().fetch_bots_metadata_from_ddb(bot_ids)

        for row in bot_results:
            bot_id = row.get('bot_id')
            if not bot_id: continue
            try:
                metadata = bot_metadata_map.get(bot_id, {})
                total_price_str = str(row.get('total_cost', '0.0') or '0.0')
                total_price = Decimal(total_price_str)
                num_convos = int(row.get('num_sessions', 0) or 0)
                num_users = int(row.get('num_users', 0) or 0)
                total_messages = int(row.get('total_messages', 0) or 0) # From SUM(json_size)
                total_input_tokens = int(row.get('total_input_tokens', 0) or 0)
                total_output_tokens = int(row.get('total_output_tokens', 0) or 0)

                top_bots_result_output.append(UsagePerBotOutput(
                    id=bot_id,
                    title=metadata.get('title', f'Bot {bot_id[:8]}...'),
                    description=metadata.get('description', ''),
                    owner_user_id=metadata.get('owner_user_id', ''),
                    total_price=total_price,
                    num_of_convos=num_convos,
                    num_of_users=num_users,
                    message_count=total_messages,
                    group_id=metadata.get('group_id'),
                    input_tokens=total_input_tokens,
                    output_tokens=total_output_tokens
                ))
            except (ValueError, TypeError, InvalidOperation) as parse_error:
                logger.warning(f"Skipping bot result row due to parsing error: {parse_error}. Row: {row}")
                continue

    except Exception as e:
        logger.error(f"Failed processing top entities: {e}", exc_info=True)

    logger.info(f"Returning top entities (Corrected Message Count): {len(top_users_result_output)} users, {len(top_bots_result_output)} bots.")
    return {"top_users": top_users_result_output, "top_bots": top_bots_result_output}

async def get_topics_analysis(
    from_str: Optional[str] = None,
    to_str: Optional[str] = None,
    limit: int = 20,
    filter_bot_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Fetches topic analysis using new partitioning and filtering."""
    bots_filter_info = f"{len(filter_bot_ids)} bots specified" if filter_bot_ids else "all bots (no filter)"
    logger.info(f"Getting topics analysis: from={from_str}, to={to_str}, limit={limit}, bots_filter={bots_filter_info}")
    from_hour_str, to_hour_str = _format_date_range(from_str, to_str)
    date_clause, botid_filter_clause = _build_common_where_clauses(
        from_hour_str, to_hour_str, filter_bot_ids
    )

    # Correct Filter
    conversation_filter = "AND Keys.SK.S LIKE CONCAT(Keys.PK.S, '#CONV#%')"
    # Keep cost filter as it implies activity? Or remove if topic analysis is independent?
    # Let's assume topic analysis should happen even if cost is 0/missing for a convo
    # cost_exists_filter = "AND newimage.TotalPrice.N IS NOT NULL"
    message_map_exists_filter = "AND newimage.MessageMap.S IS NOT NULL AND newimage.MessageMap.S <> ''" # Filter out empty/null maps

    # Fix for Athena compatibility - use direct JSON extraction with proper CAST
    # Updated based on actual MessageMap.S structure (directly contains message objects)
    topic_query = f'''
    WITH MessageData AS (
        SELECT
            newimage.MessageMap.S as message_map_json
        FROM
            "{USAGE_ANALYSIS_DATABASE}"."{USAGE_ANALYSIS_TABLE}"
        WHERE
            {date_clause}
            {botid_filter_clause}
            {conversation_filter}
            {message_map_exists_filter}
    ),
    -- Extract topic values with updated JSON paths based on actual message structure
    -- The structure seems to have messages directly at the first level
    FlattenedTopics AS (
        SELECT 
            DISTINCT 
            -- Look for topic in several possible locations based on message structure
            COALESCE(
                JSON_EXTRACT_SCALAR(message_entry, '$.topic'),                  -- Direct topic field
                JSON_EXTRACT_SCALAR(message_entry, '$.content[0].topic'),       -- If inside content array
                JSON_EXTRACT_SCALAR(message_entry, '$.content.topic')           -- If inside content object 
            ) as topic
        FROM 
            MessageData
        -- Correct fix: Parse string, CAST to map, extract map values, then unnest
        CROSS JOIN UNNEST(MAP_VALUES(CAST(JSON_PARSE(message_map_json) AS map(varchar, json)))) AS t (message_entry)
        WHERE 
            message_map_json IS NOT NULL
    )
    SELECT
        topic,
        COUNT(*) as message_count
    FROM FlattenedTopics
    WHERE
        topic IS NOT NULL
        AND topic <> ''
    GROUP BY topic
    ORDER BY message_count DESC
    LIMIT {limit}
    '''

    topics_result_output: List[TopicAnalysis] = []
    total_topic_messages = 0

    try:
        logger.debug("Executing topics analysis query.")
        results = await _execute_athena_query(topic_query)
        logger.debug(f"Topics query returned {len(results)} rows.")
        total_topic_messages = sum(int(row.get('message_count', 0) or 0) for row in results)
        for row in results:
            try:
                count = int(row.get('message_count', 0) or 0)
                topic = row.get('topic', 'Unknown Topic')
                topics_result_output.append(TopicAnalysis(
                    topic=topic,
                    count=count,
                ))
            except (ValueError, TypeError) as parse_error:
                 logger.warning(f"Skipping topic result row due to parsing error: {parse_error}. Row: {row}")
                 continue
        logger.info(f"Processed {len(topics_result_output)} topics, total messages count in top topics: {total_topic_messages}")
    except Exception as e:
        logger.error(f"Failed executing topics analysis query: {e}", exc_info=True)
    return {"topics": topics_result_output, "total_count": total_topic_messages}

# --- Analytics Endpoint Data Fetchers (Refactored to use internal functions) ---

async def get_bot_specific_analytics(
    bot_id: str,
    from_str: Optional[str] = None,
    to_str: Optional[str] = None
) -> Optional[BotAnalytics]: # Return Optional to signal no data
    """Fetches all data required for the bot-specific analytics page."""
    # Basic validation
    if not bot_id:
         logger.error("Bot ID is required for get_bot_specific_analytics")
         raise ValueError("Bot ID is required.")

    # Authorization checks are handled in the use case layer before calling this repo function.
    # Fetch metadata needed for response construction (e.g., title, owner - owner might be needed by use case for auth)
    metadata_map = await MetadataRepository().fetch_bots_metadata_from_ddb([bot_id])
    bot_metadata = metadata_map.get(bot_id)
    if not bot_metadata:
         # If metadata is essential and not found, it might indicate an issue or the bot doesn't exist.
         logger.warning(f"Metadata not found for bot {bot_id} during analytics fetch.")
         # Depending on requirements, either raise RecordNotFound or proceed cautiously.
         raise RecordNotFoundError(f"Bot metadata not found for id {bot_id}.")
         # Or: bot_metadata = {} # Proceed with default/missing info

    logger.info(f"Fetching data for Bot Analytics Page: bot_id={bot_id}, from={from_str}, to={to_str}")

    # Define the specific bot ID filter
    filter_bot_ids = [bot_id]

    # Fetch data concurrently
    # Pass consistent string names to all internal calls
    summary_daily_task = asyncio.create_task(get_summary_and_daily_data(from_str=from_str, to_str=to_str, filter_bot_ids=filter_bot_ids))
    top_users_task = asyncio.create_task(get_top_entities(from_str=from_str, to_str=to_str, limit=10, filter_bot_ids=filter_bot_ids))
    topics_task = asyncio.create_task(get_topics_analysis(from_str=from_str, to_str=to_str, limit=20, filter_bot_ids=filter_bot_ids))
    # We already have bot_metadata from the auth check above

    # Wait for all tasks
    summary_result, top_entities_result, topics_data = await asyncio.gather(
        summary_daily_task, top_users_task, topics_task
    )

    # Unpack results
    summary, daily_usage = summary_result
    # Only need top users for this specific bot's page
    top_users_output = top_entities_result.get("top_users", []) # List[UsagePerUserOutput]
    topics = topics_data.get("topics", []) # List[TopicAnalysis]

    # Check if core data (summary) was found
    if summary is None or (summary.num_messages == 0 and summary.num_sessions == 0): # Check if any activity
        logger.warning(f"No analytics activity found for bot {bot_id} in the specified period.")
        return None # Signal no data to the route handler

    # Convert UsagePerUserOutput to UsagePerUser objects
    converted_top_users = []
    for user_output in top_users_output:
        try:
            # Map fields from UsagePerUserOutput to UsagePerUser
            converted_top_users.append(
                ModelUsagePerUser(
                    id=user_output.id,
                    email=user_output.email or "Unknown",
                    total_price=user_output.total_price,
                    num_sessions=getattr(user_output, "num_sessions", 0),
                    num_messages=getattr(user_output, "num_messages", 0) or getattr(user_output, "message_count", 0) or 0
                )
            )
        except Exception as e:
            logger.warning(f"Error converting user output to UsagePerUser: {e}")
            # Skip this record instead of failing the entire operation

    # Construct the final BotAnalytics object
    # Ensure the BotAnalytics Pydantic model matches the fields being populated
    try:
        bot_analytics_data = BotAnalytics(
            bot_id=bot_id,
            # Populate from fetched metadata
            title=bot_metadata.get('title', f'Bot {bot_id[:8]}...'),
            description=bot_metadata.get('description', ''),
            owner_user_id=bot_metadata.get('owner_user_id', ''),
            # Populate from summary and top entities results
            # total_users calculation might need refinement - distinct count from summary query?
            total_users=len(top_users_output), # Approx based on top users?
            total_sessions=summary.num_sessions,
            total_messages=summary.num_messages,
            total_input_tokens=summary.input_tokens,
            total_output_tokens=summary.output_tokens,
            total_cost=summary.cost,
            daily_usage=daily_usage, # List[DailyUsage]
            top_users=converted_top_users, # Use the converted list of UsagePerUser objects
            top_topics=topics, # List[TopicAnalysis] - Check BotAnalytics model def
        )
    except Exception as pydantic_error:
         logger.error(f"Error creating BotAnalytics model for {bot_id}: {pydantic_error}", exc_info=True)
         # Failed to construct the object, treat as error/no data
         return None

    logger.info(f"Successfully fetched data for Bot Analytics page: {bot_id}")
    return bot_analytics_data