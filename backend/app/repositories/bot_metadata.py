# --- Metadata Construction Logic --- 

import logging
from datetime import datetime, UTC
from decimal import Decimal
from typing import Any

# Correctly import models from the models directory
from app.repositories.models.bot_metadata import BotMetadata, HierarchyMetadata, TagMetadata, AttributeMetadata
from app.repositories.models.custom_bot import BotModel
from app.repositories.models.group import GroupModel

# Import the group lookup function
from app.repositories.group import find_group_details

logger = logging.getLogger(__name__)

def _convert_timestamp(raw_value: Any, field_name: str, default_fallback_seconds: float) -> float:
    """
    Converts a raw timestamp value (potentially Decimal milliseconds, int/float)
    to a float representing seconds since the epoch.

    Args:
        raw_value: The raw value from DynamoDB (Decimal, int, float, None).
        field_name: The name of the field being converted (for logging).
        default_fallback_seconds: The fallback value (in seconds) if conversion fails.

    Returns:
        The timestamp converted to seconds (float).
    """
    if isinstance(raw_value, Decimal):
        try:
            # Assume Decimal represents milliseconds, convert to seconds (float)
            return float(raw_value / 1000)
        except Exception:
            logger.warning(f"Could not convert raw {field_name} '{raw_value}' (Decimal) to seconds. Defaulting.", exc_info=True)
            return default_fallback_seconds
    elif isinstance(raw_value, (int, float)):
        # If it's already a number, apply heuristic: assume milliseconds if very large.
        if raw_value > 3000000000: # Heuristic: if timestamp > ~year 2065, assume milliseconds
             try:
                 return float(raw_value / 1000)
             except Exception:
                  logger.warning(f"Could not convert large {field_name} '{raw_value}' (int/float) to seconds. Defaulting.", exc_info=True)
                  return default_fallback_seconds
        else:
             # Assume seconds if smaller or normal range
             return float(raw_value)
    elif raw_value is None:
        # If the value is None, return the fallback directly
        # logger.debug(f"{field_name} is None, using default fallback.") # Optional: log if None
        return default_fallback_seconds
    else:
        # If it's some other type (e.g., string), log warning and return fallback
        logger.warning(f"Invalid {field_name} format '{raw_value}' (type: {type(raw_value)}). Defaulting.")
        return default_fallback_seconds

def construct_bot_metadata(bot_model: BotModel) -> BotMetadata:
    """Constructs operational BotMetadata from BotModel and related group info."""
    hierarchy = []
    tags = []
    attributes = []
    group_info: GroupModel | None = None

    # --- 1. Fetch Group Details --- 
    if bot_model.group_id and bot_model.owner_user_id:
        try:
            # Logging: Log inputs before the call
            logger.info(f"Bot {bot_model.id}: Attempting to find group details with owner_user_id='{bot_model.owner_user_id}' and group_id='{bot_model.group_id}'")
            # NOTE: Assumes owner_user_id is populated correctly on bot_model
            group_info = find_group_details(bot_model.owner_user_id, bot_model.group_id)
        except Exception as e:
            logger.error(f"Failed to fetch group details during metadata construction for bot {bot_model.id}: {e}", exc_info=True)
            group_info = None 
    else:
        # Logging: Log if group info is skipped
        logger.info(f"Bot {bot_model.id}: Skipping group details fetch (group_id: {bot_model.group_id}, owner_user_id: {bot_model.owner_user_id})")

    # --- 2. Construct Hierarchy --- 
    if group_info:
        hierarchy.append(HierarchyMetadata(
            level="Course",
            id=group_info.group_id, 
            name=group_info.group_name
        ))
    # TODO: Add logic for School/District hierarchy levels if derivable

    # --- 3. Construct Tags --- 
    if bot_model.assistant_config:
        assistant_type = bot_model.assistant_config.assistant_type
        if assistant_type:
            tags.append(TagMetadata(
                id=f"assistant_type_{assistant_type}",
                name=assistant_type,
                category="AssistantType",
                value=assistant_type
            ))
        if bot_model.assistant_config.assistant_topics:
             topics = [topic.strip() for topic in bot_model.assistant_config.assistant_topics.split(',') if topic.strip()]
             for topic in topics:
                 tags.append(TagMetadata(
                     id=f"assistant_topic_{topic.replace(' ', '_').lower()}",
                     name=topic,
                     category="AssistantTopic",
                     value=topic
                 ))

    if group_info:
        role_value = group_info.role
        tags.append(TagMetadata(
            id=f"user_role_{role_value.lower()}",
            name=role_value,
            category="UserRoleInGroup",
            value=role_value
        ))
    # TODO: Add other relevant tags (e.g., knowledge source types)

    # --- 4. Construct Attributes --- 
    if bot_model.creator_config:
         creator_name_key = "CreatorName"
         attributes.append(AttributeMetadata(
             id=f"attribute_{creator_name_key.lower()}",
             name=creator_name_key,
             key=creator_name_key,
             value=bot_model.creator_config.user_name
         ))
    
    is_public_key = "IsPublic"
    attributes.append(AttributeMetadata(
        id=f"attribute_{is_public_key.lower()}",
        name=is_public_key,
        key=is_public_key,
        value=str(bot_model.public_bot_id is not None)
    ))
    sync_status_key = "SyncStatus"
    attributes.append(AttributeMetadata(
        id=f"attribute_{sync_status_key.lower()}",
        name=sync_status_key,
        key=sync_status_key,
        value=bot_model.sync_status
    ))
    creation_time_key = "CreationTimeISO"
    attributes.append(AttributeMetadata(
        id=f"attribute_{creation_time_key.lower()}",
        name=creation_time_key,
        key=creation_time_key,
        value=datetime.fromtimestamp(_convert_timestamp(bot_model.create_time, "create_time", 0.0)).isoformat()
    ))
    last_used_time_key = "LastUsedTimeISO"
    attributes.append(AttributeMetadata(
        id=f"attribute_{last_used_time_key.lower()}",
        name=last_used_time_key,
        key=last_used_time_key,
        value=datetime.fromtimestamp(_convert_timestamp(bot_model.last_used_time, "last_used_time", 0.0)).isoformat()
    ))
    owner_user_id_key = "OwnerUserId"
    attributes.append(AttributeMetadata(
        id=f"attribute_{owner_user_id_key.lower()}",
        name=owner_user_id_key,
        key=owner_user_id_key,
        value=bot_model.owner_user_id
    ))

    # Add version if it exists
    if bot_model.version:
        version_key = "Version"
        attributes.append(AttributeMetadata(
            id=f"attribute_{version_key.lower()}",
            name=version_key,
            key=version_key,
            value=bot_model.version
        ))

    # TODO: Add LTI platform info if derivable
    # TODO: Add other relevant attributes (model params?)

    # Create BotMetadata with all required fields
    return BotMetadata(
        bot_id=bot_model.id,
        title=bot_model.title,
        description=bot_model.description,
        instruction_hash=str(hash(bot_model.instruction)),
        owner_user_id=bot_model.owner_user_id,
        is_public=bot_model.public_bot_id is not None,
        group_id=bot_model.group_id,
        create_time=Decimal(str(bot_model.create_time)),
        last_used_time=Decimal(str(bot_model.last_used_time)),
        hierarchy=hierarchy,
        tags=tags,
        attributes=attributes,
        updated_at=datetime.now(UTC).isoformat(),
        is_deleted=False,
        deleted_at=None
    ) 