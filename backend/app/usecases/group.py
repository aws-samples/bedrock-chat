import logging

from app.repositories.common import (
    RecordNotFoundError,
)
from app.repositories.group import (
    find_groups_by_user_id,
)

from app.routes.schemas.group import (
    GroupOutput,
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