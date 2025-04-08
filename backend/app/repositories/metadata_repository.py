from typing import Any, List, Optional, Dict
from boto3.dynamodb.conditions import Key, Attr
from app.repositories.models.bot_metadata import BotMetadata, MetadataConfig, HierarchyMetadata, TagMetadata, AttributeMetadata
from app.utils import get_table, get_table_name_from_arn
from datetime import datetime, UTC
import boto3
import asyncio
import logging
import os
from functools import partial
from decimal import Decimal
from app.repositories.models.custom_bot import BotModel
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# Table names from environment variables with fallbacks
BOTS_METADATA_CONFIG_TABLE_NAME = os.environ.get("BOTS_METADATA_CONFIG_TABLE_NAME")
BOTS_METADATA_TABLE_ARN = os.environ.get("BOTS_METADATA_TABLE_ARN")

class MetadataRepository:
    def __init__(self):
        self.config_table = get_table(BOTS_METADATA_CONFIG_TABLE_NAME)
        if not BOTS_METADATA_TABLE_ARN:
            logger.error("BOTS_METADATA_TABLE_ARN environment variable not set!")
            self.bot_metadata_table = None
        else:
            try:
                metadata_table_name = get_table_name_from_arn(BOTS_METADATA_TABLE_ARN)
                logger.debug(f"Initializing BotsMetadataTable with ARN pointing to table: {metadata_table_name}") # Log derived name
                self.bot_metadata_table = get_table(metadata_table_name)
                if not self.bot_metadata_table:
                     logger.error(f"Failed to get table resource for BotsMetadataTable: {metadata_table_name}")
                else:
                     logger.debug("BotsMetadataTable resource initialized successfully.")
            except Exception as e:
                 logger.error(f"Error initializing BotsMetadataTable from ARN '{BOTS_METADATA_TABLE_ARN}': {e}", exc_info=True)
                 self.bot_metadata_table = None
        
    def get_config(self) -> MetadataConfig:
        """Retrieves the metadata configuration"""
        def get_config_item():
            return self.config_table.get_item(Key={'id': 'default'})
        
        try:
             response = get_config_item()
        except ClientError as e:
            logger.error(f"Error fetching metadata config: {e}", exc_info=True)
            return MetadataConfig(
                allowed_hierarchy_levels=["district", "school", "department"],
                allowed_tag_categories=["subject", "grade_level", "difficulty"],
                required_attributes=["owner", "assistant_type"]
            )

        if 'Item' not in response:
            # Return default config if none exists
            return MetadataConfig(
                allowed_hierarchy_levels=["district", "school", "department"],
                allowed_tag_categories=["subject", "grade_level", "difficulty"],
                required_attributes=["owner", "assistant_type"]
            )
        return MetadataConfig(**response['Item'])
        
    def save_config(self, config: MetadataConfig):
        """Saves the metadata configuration"""
        item = {
            'id': 'default',
            **config.model_dump(),
            'updated_at': datetime.now(UTC).isoformat()
        }
        
        def save_config_item(item_data):
            return self.config_table.put_item(Item=item_data)
            
        try:
             save_config_item(item)
        except ClientError as e:
             logger.error(f"Error saving metadata config: {e}", exc_info=True)
             raise
        
    def save_normalized_bot_metadata(self, bot_model: BotModel):
        """Saves the structured, normalized bot definition to BotsMetadataTable (Synchronous Version)."""
        # Logging: Confirm function entry and bot ID
        logger.debug(f"Entering save_normalized_bot_metadata for bot_id: {bot_model.id}")

        if not self.bot_metadata_table:
             logger.error(f"BotsMetadataTable client not initialized. Skipping save for bot {bot_model.id}.")
             return # Or raise an error?

        logger.info(f"Saving normalized metadata for bot {bot_model.id}")

        # --- Basic Validation --- 
        if not bot_model.id:
            raise ValueError("Bot ID cannot be empty")
        if not bot_model.owner_user_id:
             # Owner is crucial for many operations, raise error
             logger.error(f"Owner User ID is missing for bot {bot_model.id}, cannot save normalized metadata.")
             raise ValueError("Owner User ID cannot be empty")
        
        # --- Serialization --- 
        item_to_save = {
            'bot_id': bot_model.id, # Partition Key
            'title': bot_model.title,
            'description': bot_model.description,
            'instruction_hash': str(hash(bot_model.instruction)), # Example
            'owner_user_id': bot_model.owner_user_id,
            'is_public': bot_model.public_bot_id is not None,
            'group_id': bot_model.group_id,
            'create_time': Decimal(str(bot_model.create_time)),
            'last_used_time': Decimal(str(bot_model.last_used_time)),
            'hierarchy': [h.model_dump(mode='json') for h in bot_model.metadata.hierarchy],
            'tags': [t.model_dump(mode='json') for t in bot_model.metadata.tags],
            'attributes': [a.model_dump(mode='json') for a in bot_model.metadata.attributes],
            'updated_at': datetime.now(UTC).isoformat(),
            'is_deleted': False, 
            'deleted_at': None 
        }
        
        # --- GSI Key Population --- 
        # Clear existing GSI keys first to handle updates where metadata might be removed
        item_to_save['hierarchy_level'] = None
        item_to_save['hierarchy_id'] = None
        item_to_save['tag_category'] = None
        item_to_save['attribute_key'] = None

        hierarchy_list = bot_model.metadata.hierarchy
        tags_list = bot_model.metadata.tags
        attributes_list = bot_model.metadata.attributes

        # 1. HierarchyIndex: Index the *first* (assume highest) level found.
        if hierarchy_list:
            first_hierarchy = hierarchy_list[0]
            # Ensure the hierarchy item is a dict or has .get method (model_dump yields dict)
            hierarchy_dict = first_hierarchy.model_dump(mode='json')
            item_to_save['hierarchy_level'] = hierarchy_dict.get('level')
            item_to_save['hierarchy_id'] = hierarchy_dict.get('id')

        # 2. TagCategoryIndex: Index the category of the *first* tag found.
        # TODO: Iterate over all tags and index each one
        if tags_list:
            first_tag = tags_list[0]
            tag_dict = first_tag.model_dump(mode='json')
            item_to_save['tag_category'] = tag_dict.get('category')

        # 3. AttributeKeyIndex: Index the key of the *first* attribute found.
        # TODO: Iterate over all attributes and index each one
        if attributes_list:
            first_attribute = attributes_list[0]
            attribute_dict = first_attribute.model_dump(mode='json')
            item_to_save['attribute_key'] = attribute_dict.get('key')
            
        # Remove keys with None values before saving
        item_to_save_filtered = {k: v for k, v in item_to_save.items() if v is not None}

        # --- DynamoDB Call (Synchronous) ---
        try:
            # --- Troubleshooting Start ---
            # Log the type of updated_at again
            if 'updated_at' in item_to_save_filtered:
                 logger.debug(f"Type of 'updated_at' before put: {type(item_to_save_filtered['updated_at'])}")
            # Log the representation of the entire item being sent
            logger.debug(f"Item representation before put_item: {repr(item_to_save_filtered)}")
            # --- Troubleshooting End ---

            logger.debug(f"Attempting to put item to BotsMetadataTable: {item_to_save_filtered}")
            response = self.bot_metadata_table.put_item(Item=item_to_save_filtered)
            logger.info(f"Successfully saved normalized metadata for bot {bot_model.id}")
            return response
        except ClientError as e:
            logger.error(f"DynamoDB error saving normalized metadata for bot {bot_model.id}: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
            raise # Re-raise to be caught by caller
        except Exception as e:
            logger.error(f"Unexpected error saving normalized metadata for bot {bot_model.id}: {e}", exc_info=True)
            raise # Re-raise

    def mark_bot_metadata_as_deleted(self, bot_id: str):
        """Marks a bot as deleted in the BotsMetadataTable (soft delete - Synchronous Version)."""
        if not self.bot_metadata_table:
             logger.error(f"BotsMetadataTable client not initialized. Skipping delete mark for bot {bot_id}.")
             return

        logger.info(f"Marking bot {bot_id} as deleted in BotsMetadataTable.")
        delete_time = datetime.now(UTC).isoformat()
        key = {'bot_id': bot_id}

        try:
            # Direct synchronous call
            response = self.bot_metadata_table.update_item(
                Key=key,
                UpdateExpression="SET is_deleted = :del_flag, deleted_at = :del_time",
                ExpressionAttributeValues={
                    ':del_flag': True,
                    ':del_time': delete_time
                },
                ConditionExpression="attribute_exists(bot_id)", # Ensure item exists
                ReturnValues="UPDATED_NEW"
            )
            logger.info(f"Successfully marked bot {bot_id} as deleted.")
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                logger.error(f"Bot {bot_id} not found in BotsMetadataTable. Cannot mark as deleted.")
                # Don't raise an error, just log it, as the primary delete succeeded (in ConversationTable)
                return None 
            else:
                logger.error(f"DynamoDB error marking bot {bot_id} as deleted: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
                # Re-raise other DynamoDB errors, callers should handle
                raise 
        except Exception as e:
            logger.error(f"Unexpected error marking bot {bot_id} as deleted: {e}", exc_info=True)
            # Re-raise other errors
            raise 

    def get_bot_metadata(self, bot_id: str) -> BotMetadata:
        """Retrieves bot metadata from the BotsMetadataTable."""
        if not self.bot_metadata_table:
            logger.error("BotsMetadataTable client not initialized. Cannot retrieve bot metadata.")
            return None

        try:
            response = self.bot_metadata_table.get_item(Key={'bot_id': bot_id})
            if 'Item' in response:
                item = response['Item']
                # Create a dictionary with all fields from DynamoDB
                metadata_dict = {
                    'bot_id': item.get('bot_id'),
                    'title': item.get('title'),
                    'description': item.get('description'),
                    'instruction_hash': item.get('instruction_hash'),
                    'owner_user_id': item.get('owner_user_id'),
                    'is_public': item.get('is_public'),
                    'group_id': item.get('group_id'),
                    'create_time': item.get('create_time'),
                    'last_used_time': item.get('last_used_time'),
                    'hierarchy': item.get('hierarchy', []),
                    'tags': item.get('tags', []),
                    'attributes': item.get('attributes', []),
                    'updated_at': item.get('updated_at'),
                    'is_deleted': item.get('is_deleted'),
                    'deleted_at': item.get('deleted_at')
                }
                return BotMetadata(**metadata_dict)
            else:
                logger.error(f"Bot {bot_id} not found in BotsMetadataTable.")
                return None 
        except ClientError as e:
            logger.error(f"DynamoDB error retrieving bot metadata for bot {bot_id}: {e.response['Error']['Code']} - {e.response['Error']['Message']}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving bot metadata for bot {bot_id}: {e}", exc_info=True)
            return None
        
    # --- Bots Metadata Lookup (DynamoDB) ---
    # NOTE: This function fetches only a subset of metadata for a list of bot IDs from the Bots Metadata DynamoDB table.
    # It is used by the Usage Analysis usecase to fetch metadata for a list of bot IDs.
    async def fetch_bots_metadata_from_ddb(self, bot_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Fetches metadata for a list of bot IDs from the Bots Metadata DynamoDB table."""
        bots_dict: Dict[str, Dict[str, Any]] = {}
        if not bot_ids or not self.bot_metadata_table:
            if not self.bot_metadata_table: logger.error("Bots Metadata DDB table not initialized.")
            return bots_dict

        # Deduplicate and remove empty IDs
        unique_bot_ids = list(set(bot_id for bot_id in bot_ids if bot_id))
        if not unique_bot_ids:
            return bots_dict

        logger.debug(f"Fetching DDB metadata for {len(unique_bot_ids)} unique bot IDs.")

        keys_to_get = [{'bot_id': bot_id} for bot_id in unique_bot_ids] # Assuming PK is 'bot_id'

        # batch_get_item can retrieve up to 100 items at a time
        items_fetched = {}
        unprocessed_keys = keys_to_get
        attempts = 0
        max_attempts = 5 # Prevent infinite loops

        while unprocessed_keys and attempts < max_attempts:
            attempts += 1
            try:
                response = self.bot_metadata_table.meta.client.batch_get_item(
                    RequestItems={
                        self.bot_metadata_table.name: { # Use actual table name string here
                            'Keys': unprocessed_keys[:100], # Get up to 100 at a time
                            'ProjectionExpression': "bot_id, title, description, owner_user_id, group_id" # Request only needed fields
                        }
                    }
                )

                results = response.get('Responses', {}).get(self.bot_metadata_table.name, [])
                for item in results:
                    # Convert DynamoDB Decimal to standard types if necessary (e.g., float, int)
                    # For now, assume fields are strings or handled by Pydantic later
                    bot_id = item.get('bot_id')
                    if bot_id:
                        items_fetched[bot_id] = {
                            "id": bot_id,
                            "title": item.get("title", f"Bot {bot_id[:8]}..."),
                            "description": item.get("description", ""),
                            "owner_user_id": item.get("owner_user_id", ""),
                            "group_id": item.get("group_id"), # Can be None
                        }

                unprocessed_keys = response.get('UnprocessedKeys', {}).get(self.bot_metadata_table.name, {}).get('Keys', [])
                if unprocessed_keys:
                    logger.warning(f"Unprocessed keys remaining after batch_get_item attempt {attempts}: {len(unprocessed_keys)}")
                    await asyncio.sleep(0.5 * attempts) # Basic exponential backoff
                else:
                    # Process next batch of input keys if needed
                    unprocessed_keys = keys_to_get[len(items_fetched):] # Simplified view, actual unprocessed is complex

            except ClientError as e:
                logger.error(f"DynamoDB ClientError during batch_get_item attempt {attempts}: {e}", exc_info=True)
                # Decide how to handle partial failures - retry unprocessed, or fail?
                # For now, break and return potentially partial results
                break
            except Exception as e:
                logger.error(f"Unexpected error during batch_get_item attempt {attempts}: {e}", exc_info=True)
                break # Stop processing on unexpected error

        if attempts >= max_attempts and unprocessed_keys:
            logger.error(f"Max attempts reached fetching bot metadata. Failed to fetch {len(unprocessed_keys)} keys.")

        logger.info(f"Successfully fetched metadata for {len(items_fetched)} bots from DynamoDB.")
        return items_fetched

    
    def _query_bots_metadata_table(self, index_name: str, key_condition_expression, filter_expression=None, limit: int = 50, last_evaluated_key: Optional[Dict] = None) -> Dict:
        """Helper function to execute a query against BotsMetadataTable or its GSIs."""
        if not self.bot_metadata_table:
            logger.error(f"BotsMetadataTable client not initialized. Cannot perform query.")
            return {'items': [], 'last_evaluated_key': None}

        query_params = {
            'IndexName': index_name,
            'KeyConditionExpression': key_condition_expression,
            'Limit': limit,
            # Only return necessary fields, adjust as needed
            'ProjectionExpression': 'bot_id, title, description, owner_user_id, hierarchy, tags, attributes, is_public, create_time, last_used_time'
        }

        # Always add filter to exclude deleted bots
        # Use Attr for filter expressions
        not_deleted_filter = Attr('is_deleted').ne(True)
        if filter_expression:
            combined_filter = not_deleted_filter & filter_expression
        else:
            combined_filter = not_deleted_filter

        query_params['FilterExpression'] = combined_filter

        if last_evaluated_key:
            query_params['ExclusiveStartKey'] = last_evaluated_key

        try:
            logger.debug(f"Executing query on BotsMetadataTable index '{index_name}' with params: {query_params}")
            response = self.bot_metadata_table.query(**query_params)
            logger.debug(f"Query completed. Found {len(response.get('Items', []))} items.")

            # Optional: Parse into Pydantic models if needed downstream
            # items = [BotMetadataModel(**item) for item in response.get('Items', [])]
            items = response.get('Items', []) # Return raw dicts for now

            return {
                'items': items,
                'last_evaluated_key': response.get('LastEvaluatedKey')
            }
        except ClientError as e:
            logger.error(f"DynamoDB query error on index {index_name}: {e.response['Error']['Code']} - {e.response['Error']['Message']}", exc_info=True)
            return {'items': [], 'last_evaluated_key': None}
        except Exception as e:
            logger.error(f"Unexpected error during metadata query on index {index_name}: {e}", exc_info=True)
            return {'items': [], 'last_evaluated_key': None}

    def find_bots_by_hierarchy(self, level: str, hierarchy_id: str, limit: int = 50, last_evaluated_key: Optional[Dict] = None) -> Dict:
        """Finds bots associated with a specific hierarchy level and ID using the HierarchyIndex GSI."""
        logger.debug(f"Searching for bots by hierarchy: level='{level}', id='{hierarchy_id}'")
        key_condition = Key('hierarchy_level').eq(level) & Key('hierarchy_id').eq(hierarchy_id)
        return self._query_bots_metadata_table(
            index_name='HierarchyIndex',
            key_condition_expression=key_condition,
            limit=limit,
            last_evaluated_key=last_evaluated_key
        )

    def find_bots_by_tag_category(self, category: str, limit: int = 50, last_evaluated_key: Optional[Dict] = None) -> Dict:
        """Finds bots associated with a specific tag category using the TagCategoryIndex GSI."""
        logger.debug(f"Searching for bots by tag category: '{category}'")
        key_condition = Key('tag_category').eq(category)
        # Note: This GSI only has the category as PK. Further filtering (e.g., by tag value) happens in the FilterExpression.
        # You could enhance this by adding a filter_expression argument if needed.
        return self._query_bots_metadata_table(
            index_name='TagCategoryIndex',
            key_condition_expression=key_condition,
            limit=limit,
            last_evaluated_key=last_evaluated_key
        )

    def find_bots_by_attribute_key(self, key: str, limit: int = 50, last_evaluated_key: Optional[Dict] = None) -> Dict:
        """Finds bots associated with a specific attribute key using the AttributeKeyIndex GSI."""
        logger.debug(f"Searching for bots by attribute key: '{key}'")
        key_condition = Key('attribute_key').eq(key)
        # Note: This GSI only has the key as PK. Further filtering (e.g., by attribute value) happens in the FilterExpression.
        # You could enhance this by adding a filter_expression argument if needed.
        return self._query_bots_metadata_table(
            index_name='AttributeKeyIndex',
            key_condition_expression=key_condition,
            limit=limit,
            last_evaluated_key=last_evaluated_key
        )

    def sync_bot_analytics_metadata(self, bot_id: str, analytics_data: Dict):
        """Saves/Updates metadata for a specific bot in the analytics table (Synchronous Version)."""
        if not self.bot_metadata_table:
             logger.error(f"Analytics table client not initialized. Skipping sync for bot {bot_id}.")
             return

        # No need for event loop
        item_to_save = {
            'bot_id': bot_id,
            **analytics_data,
            'updated_at': datetime.now(UTC).isoformat()
        }
        logger.debug(f"Syncing analytics metadata for bot_id: {bot_id}")
        logger.debug(f"Analytics data being saved: {item_to_save}") # Debug print

        try:
            # Direct synchronous call
            response = self.bot_metadata_table.put_item(Item=item_to_save)
            logger.info(f"Successfully synced analytics metadata for bot_id: {bot_id}")
            return response
        except ClientError as e:
            logger.error(f"Error saving analytics metadata for bot {bot_id}: {e}")
            raise # Re-raise ClientError
        except Exception as e:
            logger.error(f"Unexpected error saving analytics metadata for bot {bot_id}: {e}", exc_info=True)
            raise # Re-raise other exceptions