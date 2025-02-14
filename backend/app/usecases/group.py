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

logger = logging.getLogger(__name__)


def fetch_all_groups_by_user_id(user_id: str) -> list[GroupOutput]:
    
    try:
        group_metas = []
        groups = find_groups_by_user_id(user_id)

        for group in groups:
            group_metas.append(
                GroupOutput(
                    group_id=group.group_id,
                    group_name=group.group_name,
                    create_time=group.create_time,
                    update_time=group.update_time,
                    create_by=group.create_by,
                    role=group.role,
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