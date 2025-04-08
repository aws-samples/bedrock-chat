# backend/app/usecases/analytics_usecases.py
import logging
import asyncio
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta, UTC

from app.user import User
from app.repositories import usage_analysis # Import specific functions if preferred
# Import scope determination functions specifically:
from app.repositories.custom_bot import (
    find_private_bots_by_user_id,
    find_all_bots_by_group_id, # This finds bots, IDs can be extracted
    validate_user_access_to_bot, # Import the targeted validation function
)
# Import specific exceptions if needed for handling
from app.repositories.common import RecordNotFoundError, RecordAccessNotAllowedError
from app.repositories.models.usage_analysis import (
    BotAnalytics
    # Removed AnalyticsSummary, DailyUsage import from repo models as we use schema models now
)
from app.routes.schemas import analytics as schemas_analytics # Import the whole schema module
# Use specific schemas for return types
from app.routes.schemas.analytics import (
    SummaryAnalyticsData, TopEntitiesData, TopicsData
)
from app.dependencies import user_has_permission # Import helper
from app.repositories.metadata_repository import MetadataRepository # Added
from app.repositories.models.bot_metadata import BotMetadata # Added

# If specific exceptions are defined elsewhere:
# from app.errors import NotFoundError, AuthorizationError

logger = logging.getLogger(__name__)

# --- Helper for Scope Determination ---

async def _get_user_accessible_bot_ids(user: User) -> Optional[List[str]]:
    """Determines the list of bot IDs accessible to the user based on their permissions."""
    logger.debug(f"Determining accessible bot IDs for user {user.id}")

    # 1. Check for global view permission first (handles SUPERADMIN and Cognito Admin group)
    has_global_view = user_has_permission(user, "view_all_bots_analytics")
    if has_global_view:
        logger.info(f"User {user.id} has global view permission. Returning None (all bots).")
        return None

    # 2. Check if user has basic permission to view the dashboard at all
    can_view_dashboard = user_has_permission(user, "view_analytics_dashboard")
    if not can_view_dashboard:
        logger.info(f"User {user.id} lacks view_analytics_dashboard permission. Returning [].")
        return []

    accessible_bot_ids = set()

    # 3. Check for Creator/Teacher scope (owned bots)
    is_creator = user_has_permission(user, "create_assistant")
    if is_creator:
        try:
            logger.debug(f"Fetching owned bots for user {user.id} (creator scope)")
            owned_bots_data = find_private_bots_by_user_id(user.id) # Synchronous
            owned_ids = {bot_data.id for bot_data in owned_bots_data if bot_data.id}
            logger.debug(f"Found {len(owned_ids)} owned bots for user {user.id}")
            accessible_bot_ids.update(owned_ids)
        except Exception as e:
            logger.error(f"Error fetching owned bots for user {user.id}: {e}", exc_info=True)

    # 4. Check for Scoped Admin scope (School/District) - ONLY if global view wasn't granted
    scoped_admin_group_ids = []
    user_is_scoped_admin = False
    if hasattr(user, 'memberships') and isinstance(user.memberships, list):
        for membership in user.memberships:
            # Directly check for the specific roles
            if membership.role in ["SCHOOLADMIN", "DISTRICTADMIN"]:
                user_is_scoped_admin = True # Mark that the user holds at least one relevant role
                if membership.group_id: # Check if group_id exists for this role membership
                    scoped_admin_group_ids.append(membership.group_id)
                else:
                     logger.warning(f"User {user.id} has role {membership.role} but no associated group_id in membership data.")

    if user_is_scoped_admin: # Proceed only if the user holds one of the roles
        if scoped_admin_group_ids: # Check if we actually collected any group IDs
            try:
                logger.debug(f"Fetching group bots for user {user.id} in groups {scoped_admin_group_ids} (scoped admin roles)")
                group_bot_id_set = set()
                for group_id in scoped_admin_group_ids:
                    group_bots = find_all_bots_by_group_id(group_id) # Synchronous
                    group_bot_id_set.update({bot.id for bot in group_bots if bot.id})

                logger.debug(f"Found {len(group_bot_id_set)} bots for groups {scoped_admin_group_ids}")
                accessible_bot_ids.update(group_bot_id_set)
            except Exception as e:
                logger.error(f"Error fetching group bots for user {user.id}: {e}", exc_info=True)
        else:
            # Log if the user has the role but we couldn't find any group IDs
            logger.warning(f"User {user.id} identified as SCHOOLADMIN/DISTRICTADMIN but no group IDs were found to fetch bots.")

    final_scope = list(accessible_bot_ids)
    logger.info(f"User {user.id} final accessible bot scope size: {len(final_scope)}")
    return final_scope

# --- Use Case Functions ---

async def get_summary_metrics(
    current_user: User,
    from_str: Optional[str],
    to_str: Optional[str]
) -> SummaryAnalyticsData: # Use specific schema if defined
    """Use case to fetch summary metrics and daily usage."""
    logger.info(f"Use case: get_summary_metrics for user {current_user.id}")
    filter_bot_ids = await _get_user_accessible_bot_ids(current_user)

    # Check if scope determination resulted in explicitly empty list
    if isinstance(filter_bot_ids, list) and not filter_bot_ids:
         logger.info(f"User {current_user.id} has access, but to zero bots in scope. Returning empty summary.")
         # Return a dictionary matching the structure, not a Pydantic instance
         return {
             "summary": {"num_sessions": 0, "num_messages": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0, "total_bots": 0, "total_users": 0},
             "daily_usage": []
         }

    # Call repository function to get aggregated data
    # NOTE: Parameter names are now standardized to from_str, to_str
    summary, daily_usage = await usage_analysis.get_summary_and_daily_data(
        filter_bot_ids=filter_bot_ids, 
        from_str=from_str, # Use from_str
        to_str=to_str      # Use to_str
    )

    # Check if the user has permission to view cost data
    can_view_cost = user_has_permission(current_user, "view_cost_data")
    if not can_view_cost:
        logger.debug(f"User {current_user.id} lacks view_cost_data permission. Nullifying cost and token fields.")
        if summary:
            summary.cost = None
            summary.input_tokens = None
            summary.output_tokens = None
        if daily_usage:
            for day in daily_usage:
                day.cost = None
                day.input_tokens = None
                day.output_tokens = None

    # Ensure summary is not None before conversion
    if summary is None:
         # Create an empty schema summary if repo returned None (shouldn't happen now)
         schema_summary_obj = schemas_analytics.AnalyticsSummary()
    else:
        # Convert the potentially modified repository summary object to the schema's AnalyticsSummary type
        schema_summary_obj = schemas_analytics.AnalyticsSummary(
            num_sessions=summary.num_sessions,
            num_messages=summary.num_messages,
            input_tokens=summary.input_tokens, # Will pass None if modified
            output_tokens=summary.output_tokens, # Will pass None if modified
            cost=summary.cost, # Will pass None if modified
            total_bots=getattr(summary, 'total_bots', 0),
            total_users=getattr(summary, 'total_users', 0)
        )

    # Convert each potentially modified repository DailyUsage object to the schema's DailyUsage type
    schema_daily_usage_list = [
        schemas_analytics.DailyUsage(
            date=item.date,
            # Map field names to match frontend expectations
            num_sessions=item.num_sessions,
            num_messages=item.num_messages,
            input_tokens=item.input_tokens, # Will pass None if modified
            output_tokens=item.output_tokens, # Will pass None if modified
            cost=item.cost # Will pass None if modified
        ) for item in (daily_usage or [])
    ]

    # Return the SummaryAnalyticsData using the correctly typed objects
    return schemas_analytics.SummaryAnalyticsData(summary=schema_summary_obj, daily_usage=schema_daily_usage_list)


async def get_top_entities_data(
    current_user: User,
    from_str: Optional[str],
    to_str: Optional[str],
    limit: int
) -> TopEntitiesData: # Use specific schema if defined
    """Use case to fetch top users and bots."""
    logger.info(f"Use case: get_top_entities_data for user {current_user.id}")
    filter_bot_ids = await _get_user_accessible_bot_ids(current_user)

    if isinstance(filter_bot_ids, list) and not filter_bot_ids:
         logger.info(f"User {current_user.id} has access, but to zero bots in scope. Returning empty entities.")
         return TopEntitiesData(top_users=[], top_bots=[])

    # Call repository function
    # NOTE: Parameter names are now standardized to from_str, to_str
    entities_dict = await usage_analysis.get_top_entities(
        from_str=from_str, # Use from_str
        to_str=to_str,   # Use to_str
        limit=limit,
        filter_bot_ids=filter_bot_ids
    )

    # Extract lists of Output objects from repo result
    top_users_output_list = entities_dict.get('top_users', []) # List[UsagePerUserOutput]
    top_bots_output_list = entities_dict.get('top_bots', [])   # List[UsagePerBotOutput]

    # Convert to schema types (UsagePerUser, UsagePerBot)
    schema_top_users_list = [
        schemas_analytics.UsagePerUser(
            id=user.id,
            email=user.email or 'N/A', # Schema expects non-optional email
            total_price=user.total_price, # Allow null values
            num_sessions=getattr(user, 'num_sessions', 0), # Add if needed
            num_messages=getattr(user, 'message_count', 0) # Use getattr for safety
        ) for user in top_users_output_list
    ]

    schema_top_bots_list = [
        schemas_analytics.UsagePerBot(
            id=bot.id,
            title=bot.title or f'Bot {bot.id[:8]}...', # Schema expects non-optional
            description=bot.description or '', # Schema expects non-optional
            published_api_stack_name=getattr(bot, 'published_api_stack_name', None),
            published_api_datetime=getattr(bot, 'published_api_datetime', None),
            owner_user_id=bot.owner_user_id or 'unknown', # Schema expects non-optional
            total_price=bot.total_price, # Allow null values
            num_of_users=getattr(bot, 'num_of_users', 0), # Use getattr for safety
            num_of_convos=getattr(bot, 'num_of_convos', 0), # Use getattr for safety
            # assistant_config and creator_config not in UsagePerBotOutput, omit
            group_id=bot.group_id
        ) for bot in top_bots_output_list
    ]

    # Filter sensitive fields based on permission (applied AFTER converting to schema types)
    can_view_cost = user_has_permission(current_user, "view_cost_data")
    if not can_view_cost:
        logger.debug(f"User {current_user.id} lacks view_cost_data permission. Nullifying cost fields in entities.")
        for user_usage in schema_top_users_list:
            user_usage.total_price = None
        for bot_usage in schema_top_bots_list:
            bot_usage.total_price = None

    # Return using the correctly typed lists
    return TopEntitiesData(top_users=schema_top_users_list, top_bots=schema_top_bots_list)


async def get_topics_data(
    current_user: User,
    from_str: Optional[str],
    to_str: Optional[str],
    limit: int
) -> TopicsData: # Use specific schema if defined
    """Use case to fetch topic analysis."""
    logger.info(f"Use case: get_topics_data for user {current_user.id}")
    filter_bot_ids = await _get_user_accessible_bot_ids(current_user)

    if isinstance(filter_bot_ids, list) and not filter_bot_ids:
         logger.info(f"User {current_user.id} has access, but to zero bots in scope. Returning empty topics.")
         return TopicsData(topics=[], total_count=0)

    # Call repository function
    logger.debug(f"Calling repository to get topics analysis with filter_bot_ids: {filter_bot_ids}")
    # NOTE: Parameter names are now standardized to from_str, to_str
    topics_dict = await usage_analysis.get_topics_analysis(
        from_str=from_str, # Use from_str
        to_str=to_str,   # Use to_str
        limit=limit,
        filter_bot_ids=filter_bot_ids
    )

    # Extract list of repository TopicAnalysis objects
    repo_topics_list = topics_dict.get('topics', []) # List[repo_models.TopicAnalysis]
    total_count = topics_dict.get('total_count', 0)

    logger.debug(f"Got {len(repo_topics_list)} topics from repository with total_count: {total_count}")

    # Convert repository TopicAnalysis objects to schema objects with explicit field mapping
    # Account for the field name difference: 'count' in repo model vs 'message_count' in schema
    schema_topics_list = [
        schemas_analytics.TopicAnalysis(
            topic=topic.topic,
            message_count=topic.count, # Map count to message_count 
            percentage=(topic.count / total_count * 100) if total_count > 0 else 0.0 # Calculate percentage
        ) for topic in repo_topics_list
    ]

    # No need to filter cost/token fields here as they don't exist in TopicAnalysis
    logger.debug(f"Returning {len(schema_topics_list)} topics")
    
    # Return TopicsData with correctly typed objects
    return TopicsData(
        topics=schema_topics_list,
        total_count=total_count
    )


async def get_bot_analytics(
    current_user: User,
    bot_id: str,
    from_str: Optional[str],
    to_str: Optional[str]
) -> schemas_analytics.BotAnalytics: # Changed return type hint to schema version
    """Use case to fetch analytics for a specific bot."""
    logger.info(f"Use case: get_bot_analytics for user {current_user.id}, bot_id {bot_id}")

    # 1. Authorization Check:
    # First, check for global permission
    can_view_all = user_has_permission(current_user, "view_all_bots_analytics")
    
    if not can_view_all:
        # If no global permission, perform targeted check for this specific bot
        try:
            logger.debug(f"Performing targeted access check for user {current_user.id} on bot {bot_id}")
            # This function should raise an exception if access is denied
            validate_user_access_to_bot(current_user.id, bot_id)
            logger.debug(f"Targeted access check passed for user {current_user.id} on bot {bot_id}")
        except (RecordNotFoundError, RecordAccessNotAllowedError) as e:
            logger.warning(f"Authorization failed: User {current_user.id} cannot access bot {bot_id}. Reason: {e}")
            # Re-raise as PermissionError for the route handler to catch as 403
            raise PermissionError(f"User not authorized to view analytics for bot {bot_id}") from e
        except Exception as e:
            logger.error(f"Unexpected error during targeted access check for user {current_user.id} on bot {bot_id}: {e}", exc_info=True)
            raise # Re-raise unexpected errors
    else:
        logger.info(f"User {current_user.id} has global view permission, skipping targeted check for bot {bot_id}.")

    # 2. Call repository function
    repo_bot_analytics_data: Optional[BotAnalytics] = await usage_analysis.get_bot_specific_analytics(
        bot_id=bot_id,
        from_str=from_str,
        to_str=to_str
    )

    # 3. Handle case where NO usage data is found
    if repo_bot_analytics_data is None:
        logger.warning(f"Analytics usage data not found for bot {bot_id}. Fetching metadata for empty response.")
        # Initialize with defaults
        bot_title, bot_description, bot_owner_id = "N/A", "N/A", "N/A"
        try:
            metadata_repo = MetadataRepository()
            bot_meta: Optional[BotMetadata] = await asyncio.to_thread(metadata_repo.get_bot_metadata, bot_id)
            # If metadata is found, update the variables (regardless of deletion status)
            if bot_meta:
                logger.debug(f"Found metadata for bot {bot_id} (is_deleted={bot_meta.is_deleted}). Using for empty analytics response.")
                bot_title = bot_meta.title or bot_title # Keep default if meta field is empty
                bot_description = bot_meta.description or bot_description
                bot_owner_id = bot_meta.owner_user_id or bot_owner_id
            # No 'else' needed, defaults are already set
        except Exception as meta_e:
            # Log error but continue with defaults
            logger.error(f"Error fetching metadata for bot {bot_id}: {meta_e}", exc_info=True)

        # Construct the empty analytics object using the determined values
        empty_analytics = schemas_analytics.BotAnalytics(
            bot_id=bot_id,
            title=bot_title, # Uses fetched value or default 'N/A'
            description=bot_description, # Uses fetched value or default 'N/A'
            owner_user_id=bot_owner_id, # Uses fetched value or default 'N/A'
            total_users=0, total_sessions=0, total_messages=0,
            total_input_tokens=0, total_output_tokens=0, total_cost=0.0,
            daily_usage=[], top_users=[], top_topics=[]
        )

        # Apply cost permission check even to the empty object
        can_view_cost = user_has_permission(current_user, "view_cost_data")
        if not can_view_cost:
            empty_analytics.total_cost = None
            empty_analytics.total_input_tokens = None
            empty_analytics.total_output_tokens = None

        return empty_analytics # Return the object with metadata and zero usage

    # 4. Convert repository model to schema model (This part runs only if usage data WAS found)
    # Convert daily usage list
    schema_daily_usage_list = [
        schemas_analytics.DailyUsage(
            date=item.date,
            num_sessions=item.num_sessions,
            num_messages=item.num_messages,
            input_tokens=item.input_tokens,
            output_tokens=item.output_tokens,
            cost=item.cost
        ) for item in (repo_bot_analytics_data.daily_usage or [])
    ]
    # Convert top users list
    schema_top_users_list = [
        schemas_analytics.UsagePerUser(
            id=user.id,
            email=user.email or 'N/A',
            total_price=user.total_price,
            num_sessions=user.num_sessions,
            num_messages=user.num_messages
        ) for user in (repo_bot_analytics_data.top_users or [])
    ]
    # Convert top topics list
    schema_top_topics = [
        schemas_analytics.TopicAnalysis(
            topic=item.topic,
            message_count=item.message_count,
            percentage=item.percentage
        ) for item in (repo_bot_analytics_data.top_topics or [])
    ]

    # Construct the main schema object first
    schema_bot_analytics = schemas_analytics.BotAnalytics(
        bot_id=repo_bot_analytics_data.bot_id,
        title=repo_bot_analytics_data.title,
        description=repo_bot_analytics_data.description,
        owner_user_id=repo_bot_analytics_data.owner_user_id,
        total_users=repo_bot_analytics_data.total_users,
        total_sessions=repo_bot_analytics_data.total_sessions,
        total_messages=repo_bot_analytics_data.total_messages,
        total_input_tokens=repo_bot_analytics_data.total_input_tokens,
        total_output_tokens=repo_bot_analytics_data.total_output_tokens,
        total_cost=repo_bot_analytics_data.total_cost,
        daily_usage=schema_daily_usage_list, # Use converted list
        top_users=schema_top_users_list, # Use converted list
        top_topics=schema_top_topics # Assuming TopicAnalysis is the same in repo and schema
    )

    # Now, filter the schema object based on permission
    can_view_cost = user_has_permission(current_user, "view_cost_data")
    if not can_view_cost:
        logger.debug(f"User {current_user.id} lacks view_cost_data permission. Nullifying cost and token fields in BotAnalytics.")
        schema_bot_analytics.total_cost = None
        schema_bot_analytics.total_input_tokens = None
        schema_bot_analytics.total_output_tokens = None
        for day in schema_bot_analytics.daily_usage:
            day.cost = None
            day.input_tokens = None
            day.output_tokens = None
        for user_usage in schema_bot_analytics.top_users:
            user_usage.total_price = None
            # NOTE: Schema UsagePerUser doesn't have tokens

    return schema_bot_analytics 