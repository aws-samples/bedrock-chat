import logging

from app.repositories.common import (
    RecordNotFoundError,
)
from app.repositories.group import (
    find_groups_by_user_id
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
    # Step 2: For each group:
    #           iterate through the bots and
    #           get bot_id and creator_id
    # Step 3: Validate that the bot_id is in one of the groups
    # Step 4: Return the bot_id and creator_id
    logger.info(f"Validating user: {user_id} has access to bot: {bot_id}")
    groupList = fetch_all_groups_by_user_id(user_id)
    if not groupList:
        raise RecordNotFoundError(f"Failed to find groups for user: {user_id}")
    for group in groupList:
        groupId = group.group_id
        botListFromGroup = find_all_creator_id_by_group_id(groupId)
        for bot in botListFromGroup:
            if bot.bot_id == bot_id:
                return bot
    # Failed to find bot
    raise RecordNotFoundError(f"Failed to find bot: {bot_id}")