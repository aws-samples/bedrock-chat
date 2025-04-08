import logging

from app.repositories.common import (
    RecordNotFoundError,
)
from app.repositories.group import (
    find_groups_by_user_id
)

from app.repositories.lti_data import (
    get_lti_data_list
)

from app.routes.schemas.group import (
    GroupOutput,
    ACTION_CONFIG_MAP,
    ROLE_HIERARCHY
)
from app.repositories.group import (
    find_all_creator_id_by_group_id
)
from app.repositories.models.custom_bot import (
    BotCreatorModel
)
from app.repositories.metadata_repository import MetadataRepository

logger = logging.getLogger(__name__)

def fetch_all_groups_by_user_id(user_id: str) -> list[GroupOutput]:
    
    try:
        groups = find_groups_by_user_id(user_id)

        group_metas = []
        for group in groups:
            group_metas.append(
                GroupOutput(
                    group_id=group.group_id,
                    group_name=group.group_name,
                    create_time=group.create_time,
                    update_time=group.update_time,
                    create_by=group.create_by,
                    role=group.role,
                    user_name=group.user_name,
                )
            )

        return group_metas

    except RecordNotFoundError:
        raise RecordNotFoundError(
            f"User not found."
        )

def fetch_all_groups_with_lti_data(user_id: str) -> list[GroupOutput]:
    # For a specific user, get the group list with the lti name
    # lti_name retrieved from lti table
    try:
        lti_items = get_lti_data_list()

        lti_map = {}

        for item in lti_items:  
            lti_map[item.get('lti_id')] = item

        groupList = fetch_all_groups_by_user_id(user_id)

        for group in groupList:
            # extract the lti_id from the group_id
            group_lti_id = group.group_id.split("-")[0]
            lti_name = lti_map.get(group_lti_id, {}).get("lti_name", "")
            group.lti_name = lti_name

        return groupList
    except RecordNotFoundError:
        raise RecordNotFoundError(
            f"User not found."
        )
    


def get_role_by_user_id(user_id: str) -> str:
    # get user role from grouplist with the highest level of permissions
    groupList = fetch_all_groups_by_user_id(user_id)
    if not groupList: 
        return "STUDENT"
    max(groupList, key=lambda group: ROLE_HIERARCHY.index(group.role))
    return max(groupList, key=lambda group: ROLE_HIERARCHY.index(group.role)).role


def is_user_authorized(action: str, user_id: str) -> bool:
    try:
        role = get_role_by_user_id(user_id)
        logger.info(f"User Role: {role}");
        return ACTION_CONFIG_MAP.get(action, {}).get(role, False)
    except Exception:
        logger.error("Failed to check authorization status", exc_info=True)
    return False

def get_user_name(user_id: str) -> str:
    # get name of user
    groupList = fetch_all_groups_by_user_id(user_id)
    if not groupList: 
        return "Not in DB"
    return groupList[0].user_name

def validate_user_access_to_bot(user_id: str, bot_id: str) -> BotCreatorModel:
    # Validate that the user has access to the bot
    # Step 1: Get the user's list of groups
    # Step 2: Try to get bot details from metadata table
    # Step 3: If metadata not available, search through groups
    # Step 4: Return the bot_id and creator_id
    logger.info(f"Validating user: {user_id} has access to bot: {bot_id}")

    # First get user's groups
    groupList = fetch_all_groups_by_user_id(user_id)
    if not groupList:
        raise RecordNotFoundError(f"Failed to find groups for user: {user_id}")

    # Try to get bot details from metadata table
    try:
        bot_creator, group_id = _get_bot_details_by_bot_metadata(bot_id)
        if bot_creator and group_id:
            # Check if user has access to the group
            if any(group.group_id == group_id for group in groupList):
                logger.info(f"Found bot access through metadata for bot: {bot_id}")
                return bot_creator
    except Exception as e:
        logger.warning(f"Could not get bot details from metadata for bot {bot_id}: {str(e)}")
        # Continue with group search if metadata lookup fails

    # If metadata lookup failed or group access not found, search through groups
    logger.info(f"Searching through groupList for bot: {bot_id}")
    for group in groupList:
        groupId = group.group_id
        botListFromGroup = find_all_creator_id_by_group_id(groupId)
        for bot in botListFromGroup:
            if bot.bot_id == bot_id:
                logger.info(f"Found bot access through group search for bot: {bot_id}")
                return bot

    # Failed to find bot
    raise RecordNotFoundError(f"Failed to find bot: {bot_id}")


def _get_bot_details_by_bot_metadata(bot_id: str) -> tuple[BotCreatorModel, str]:
    try:
        bot_metadata = MetadataRepository().get_bot_metadata(bot_id)
        if not bot_metadata:
            logger.error(f"Bot metadata not found for bot_id: {bot_id}")
            return None, None
            
        # Ensure we have all required fields
        if not all([
            bot_metadata.bot_id,
            bot_metadata.owner_user_id,
            bot_metadata.group_id
        ]):
            logger.error(f"Missing required fields in bot metadata for bot_id: {bot_id}")
            return None, None

        bot_creator = BotCreatorModel(
            bot_id=bot_id,
            user_id=bot_metadata.owner_user_id,
        )
        group_id = bot_metadata.group_id
        logger.info(f"Found bot_metadata details for bot: {bot_id} - Bot creator: {bot_creator} - Group ID: {group_id}")
        return bot_creator, group_id
    except Exception as e:
        logger.error(f"Error getting bot details for bot_id {bot_id}: {str(e)}", exc_info=True)
        return None, None
