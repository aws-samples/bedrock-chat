import logging

from app.repositories.common import (
    _get_table_client,
)
from app.repositories.models.group import (
    GroupModel,
)
from boto3.dynamodb.conditions import Key

logger = logging.getLogger(__name__)


def find_groups_by_user_id(user_id: str) -> list[GroupModel]:
    """Find all groups by user id."""
    table = _get_table_client(user_id)
    logger.info(f"Finding all groups with id: {user_id}")


    query_params = {
        "KeyConditionExpression": Key("PK").eq(user_id)
        # NOTE: Need SK to fetch only groups
        & Key("SK").begins_with(f"{user_id}#GROUP#"),
        "ScanIndexForward": False,
    }

    def extractGroupId(group_id: str): 
        return group_id.split("#")[-1]

    response = table.query(**query_params)
    groupList = [
        GroupModel(
            group_id=extractGroupId(item["SK"]),
            group_name=item["GroupName"],
            create_time=float(item["CreateTime"]),
            update_time=float(item["UpdateTime"]),
            create_by=item["CreateBy"],
            role=item["Role"],
        )
        for item in response["Items"]
    ]

    logger.info(f"Found groups: {groupList}")
    return groupList