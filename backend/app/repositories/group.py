import logging
from decimal import Decimal
import json # Import json for logging the key dict

from app.repositories.common import (
    _get_table_client,
)
from app.repositories.models.group import (
    GroupModel,
)
from boto3.dynamodb.conditions import Key
from app.repositories.models.custom_bot import (
    BotCreatorModel
)
from app.repositories.common import (
    decompose_bot_id
)
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def extractGroupId(group_id: str): 
    return group_id.split("#")[-1]

def find_groups_by_user_id(user_id: str) -> list[GroupModel]:
    """Find all groups by user id."""
    table = _get_table_client(user_id)
    logger.info(f"Finding all groups with id: {user_id}")

    query_params = {
        "KeyConditionExpression": Key("PK").eq(user_id)
        # NOTE: Need SK to fetch only groups
        & Key("SK").begins_with(f"{user_id}#GROUP#"),
    }

    

    response = table.query(**query_params)
    groupList = [
        GroupModel(
            group_id=extractGroupId(item["SK"]),
            group_name=item["GroupName"],
            create_time=float(item["CreateTime"]),
            update_time=float(item["UpdateTime"]),
            create_by=item["CreateBy"],
            role=item["Role"],
            user_name=item["UserName"]
        )
        for item in response["Items"]
    ]

    logger.info(f"Found {len(groupList)} groups for user {user_id}")
    return groupList

def find_group_details(user_id: str, group_id: str) -> GroupModel | None:
    """Find specific group details for a user based on the exact group_id."""
    # --- Troubleshooting Start ---
    logger.debug(f"Entering find_group_details with user_id='{user_id}', group_id='{group_id}'")
    try:
        table = _get_table_client(user_id)
        if table is None:
            logger.error(f"_get_table_client returned None for user_id '{user_id}'. Cannot proceed.")
            return None
        # Log the actual table name being used
        logger.debug(f"Targeting table: '{table.table_name}' for user_id '{user_id}'")
    except Exception as e:
        logger.error(f"Error calling _get_table_client for user_id '{user_id}': {e}", exc_info=True)
        return None
    # --- Troubleshooting End ---

    target_sk = f"{user_id}#GROUP#{group_id}"
    # --- Troubleshooting Start ---
    logger.debug(f"Constructed target SK: '{target_sk}'")
    key_to_get = {'PK': user_id, 'SK': target_sk}
    logger.debug(f"Attempting GetItem with Key: {json.dumps(key_to_get)}")
    # --- Troubleshooting End ---

    try:
        response = table.get_item(Key=key_to_get) # Use the constructed dict
        item = response.get('Item')
        # --- Troubleshooting Start ---
        # Log the raw response metadata for clues (e.g., request ID, retries)
        response_metadata = response.get('ResponseMetadata', {})
        logger.debug(f"GetItem ResponseMetadata: {json.dumps(response_metadata)}")
        if item:
             logger.debug(f"GetItem successful. Raw item found: {json.dumps(item, default=str)}") # Log raw item before processing
        else:
            logger.warning(f"GetItem returned, but no 'Item' found for key {json.dumps(key_to_get)} in table '{table.table_name}'")
        # --- Troubleshooting End ---


        if not item:
            # logger.warning(f"No group details found for user {user_id} and group {group_id} (SK: {target_sk})") # Already logged above more specifically
            return None

        # --- Handle Potential Decimal Types for Timestamps ---
        create_time_raw = item.get("CreateTime")
        update_time_raw = item.get("UpdateTime")

        # Convert Decimal to float, handle None or other types gracefully
        create_time_float = 0.0
        if isinstance(create_time_raw, Decimal):
            create_time_float = float(create_time_raw)
        elif isinstance(create_time_raw, (int, float, str)): # Handle if it's somehow already number/string
             try:
                 create_time_float = float(create_time_raw)
             except (ValueError, TypeError):
                 logger.warning(f"Could not convert CreateTime '{create_time_raw}' to float for group {group_id}")

        update_time_float = 0.0
        if isinstance(update_time_raw, Decimal):
            update_time_float = float(update_time_raw)
        elif isinstance(update_time_raw, (int, float, str)):
             try:
                 update_time_float = float(update_time_raw)
             except (ValueError, TypeError):
                 logger.warning(f"Could not convert UpdateTime '{update_time_raw}' to float for group {group_id}")
        # --- End Timestamp Handling ---

        # The group_id passed in is the specific ID we need for the model
        actual_group_id = group_id

        # Use .get() for all fields for safety
        group_model = GroupModel(
            group_id=actual_group_id,
            group_name=item.get("GroupName", "Unknown Group"),
            # Use the converted float values
            create_time=create_time_float,
            update_time=update_time_float,
            create_by=item.get("CreateBy", ""),
            role=item.get("Role", "Unknown Role"),
            user_name=item.get("UserName", "Unknown User")
        )
        logger.debug(f"Found group details: {group_model}")
        return group_model

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        # --- Troubleshooting Start ---
        # Log the request ID from the error response if available
        error_metadata = e.response.get("ResponseMetadata", {})
        request_id = error_metadata.get("RequestId")
        logger.error(f"DynamoDB ClientError ({error_code}) RequestId: {request_id} - fetching group details for PK='{user_id}', SK='{target_sk}': {e}")
        # --- Troubleshooting End ---
        if error_code == "ResourceNotFoundException":
             logger.error(f"ResourceNotFoundException explicitly confirmed for PK: {user_id}, SK: {target_sk} on table '{table.table_name}'") # Include table name
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching group details for user {user_id}, group {group_id} on table '{table.table_name}': {e}", exc_info=True) # Include table name
        return None

def find_all_creator_id_by_group_id(group_id: str) -> list[BotCreatorModel]:
    table = _get_table_client(group_id)
    logger.debug(f"Finding creators for group: {group_id}")
    query_params = {
        "IndexName": "GroupIdIndex",
        "KeyConditionExpression": Key("GroupId").eq(group_id),
    }
    response = table.query(**query_params)
    creators = [
        BotCreatorModel(
            bot_id=decompose_bot_id(item["SK"]),
            user_id=item["SK"].split("#")[0]
        )
        for item in response["Items"]
    ]
    logger.debug(f"Found all creators in group: {creators}")
    return creators

def find_group_by_group_id(user_id: str, group_id: str) -> str:
    table = _get_table_client(group_id)
    logger.debug(f"Finding creators for group: {group_id}")
    query_params = {
        "KeyConditionExpression": Key("PK").eq(user_id)
        & Key("SK").eq(f"{user_id}#GROUP#{group_id}"),
    }
    response = table.query(**query_params)
    item = response["Items"][0]
    group = GroupModel(
        group_id=extractGroupId(item["SK"]),
        group_name=item["GroupName"],
        create_time=float(item["CreateTime"]),
        update_time=float(item["UpdateTime"]),
        create_by=item["CreateBy"],
        role=item["Role"],
        user_name=item["UserName"]
    )
    return group