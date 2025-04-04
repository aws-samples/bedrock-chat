import logging

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

    logger.info(f"Found groups: {groupList}")
    return groupList

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