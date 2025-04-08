import sys
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, UTC
import boto3
import pytest
from botocore.exceptions import ClientError
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

sys.path.insert(0, ".")

from app.repositories.metadata_repository import MetadataRepository
from app.repositories.models.bot_metadata import (
    MetadataConfig,
    BotMetadata,
    HierarchyMetadata,
    TagMetadata,
    AttributeMetadata,
)
from app.repositories.models.custom_bot import (
    BotModel,
    GenerationParamsModel,
    AgentModel,
    AgentToolModel,
    KnowledgeModel,
    ActiveModelsModel,
    AssistantConfigModel,
    CreatorConfigModel,
)

# Add UTC constant if not available in datetime
try:
    from datetime import UTC
except ImportError:
    # Python < 3.11 compatibility
    from datetime import timezone
    UTC = timezone.utc


class TestMetadataRepository(unittest.TestCase):
    def setUp(self):
        # Create mocks for tables
        self.mock_config_table = MagicMock()
        self.mock_bot_metadata_table = MagicMock()
        
        # Patch the get_table function to return our mocks
        self.get_table_patcher = patch('app.repositories.metadata_repository.get_table')
        self.mock_get_table = self.get_table_patcher.start()
        
        # Configure get_table to return different mocks based on table name
        def get_table_side_effect(table_name):
            if table_name == 'metadata_config':
                return self.mock_config_table
            elif table_name == 'bot_metadata':
                return self.mock_bot_metadata_table
            return MagicMock()
            
        self.mock_get_table.side_effect = get_table_side_effect
        
        # Create repository
        self.repository = MetadataRepository()
        # Directly set the tables after creation to bypass the environment variable check
        self.repository.config_table = self.mock_config_table
        self.repository.bot_metadata_table = self.mock_bot_metadata_table
        
        # Set up common test data
        self.test_config = MetadataConfig(
            allowed_hierarchy_levels=["district", "school", "department"],
            allowed_tag_categories=["subject", "grade_level", "difficulty"],
            required_attributes=["owner", "assistant_type"]
        )
        
        self.test_bot_metadata = BotMetadata(
            bot_id="test-bot-1",
            title="Test Bot",
            description="A test bot",
            instruction_hash="abc123",
            owner_user_id="user-1",
            is_public=True,
            group_id="group-1",
            create_time=1234567890.0,
            last_used_time=1234567890.0,
            hierarchy=[
                HierarchyMetadata(id="h1", name="Engineering", level="department", path=["Engineering"])
            ],
            tags=[
                TagMetadata(id="t1", name="Python", category="language")
            ],
            attributes=[
                AttributeMetadata(id="a1", name="English", key="language", value="en", data_type="string")
            ],
            updated_at=datetime.now(UTC).isoformat(),
            is_deleted=False,
            deleted_at=None
        )
        
        # Test bot model with metadata
        self.test_bot_model = BotModel(
            id="test-bot-id",
            group_id="test-group",
            title="Test Bot",
            description="A test bot",
            instruction="This is a test instruction",
            owner_user_id="user123",
            create_time=1700000000,
            last_used_time=1700100000,
            metadata=self.test_bot_metadata,
            public_bot_id=None,
            is_pinned=False,
            generation_params=GenerationParamsModel(
                max_tokens=3000,
                top_k=250,
                top_p=0.999,
                temperature=0.0,
                stop_sequences=["Human: ", "Assistant: "],
            ),
            agent=AgentModel(
                tools=[
                    AgentToolModel(name="tool1", description="tool1 description"),
                ]
            ),
            knowledge=KnowledgeModel(
                source_urls=[],
                sitemap_urls=[],
                filenames=[],
                s3_urls=[],
            ),
            sync_status="RUNNING",
            sync_status_reason="reason",
            sync_last_exec_id="",
            published_api_stack_name=None,
            published_api_datetime=None,
            published_api_codebuild_id=None,
            display_retrieved_chunks=True,
            conversation_quick_starters=[],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
            active_models=ActiveModelsModel(),
            version="1.0",
            assistant_config=AssistantConfigModel(
                assistant_type="general",
                assistant_topics="test topics"
            ),
            creator_config=CreatorConfigModel(
                user_id="user123",
                user_name="Test User"
            ),
        )
        
    def tearDown(self):
        self.get_table_patcher.stop()

    def test_get_config_existing(self):
        """Test getting an existing metadata configuration (synchronous version)."""
        # Setup mock response
        self.mock_config_table.get_item.return_value = {
            "Item": {
                "id": "default",
                "allowed_hierarchy_levels": ["district", "school", "department"],
                "allowed_tag_categories": ["subject", "grade_level", "difficulty"],
                "required_attributes": ["language", "target_age"]
            }
        }
        
        # Call method (now synchronous)
        config = self.repository.get_config()
        
        # Assertions
        self.mock_config_table.get_item.assert_called_once_with(
            Key={"id": "default"}
        )
        self.assertEqual(config.allowed_hierarchy_levels, ["district", "school", "department"])
        self.assertEqual(config.allowed_tag_categories, ["subject", "grade_level", "difficulty"])
        self.assertEqual(config.required_attributes, ["language", "target_age"])

    def test_get_config_default(self):
        """Test getting default configuration when no item is found (synchronous version)."""
        # Setup mock response for no item
        self.mock_config_table.get_item.return_value = {}
        
        # Call method (now synchronous)
        config = self.repository.get_config()
        
        # Assertions
        self.mock_config_table.get_item.assert_called_once_with(
            Key={"id": "default"}
        )
        self.assertEqual(config.allowed_hierarchy_levels, ["district", "school", "department"])
        self.assertEqual(config.allowed_tag_categories, ["subject", "grade_level", "difficulty"])
        self.assertEqual(config.required_attributes, ["owner", "assistant_type"])

    def test_save_config(self):
        """Test saving a metadata configuration (synchronous version)."""
        # Setup mock
        self.mock_config_table.put_item.return_value = {}
        
        # Call method (now synchronous)
        self.repository.save_config(self.test_config)
        
        # Assertions
        self.mock_config_table.put_item.assert_called_once()
        # Check that the item was saved with the correct data
        call_args = self.mock_config_table.put_item.call_args[1]
        self.assertEqual(call_args["Item"]["id"], "default")
        self.assertEqual(call_args["Item"]["allowed_hierarchy_levels"], self.test_config.allowed_hierarchy_levels)
        self.assertEqual(call_args["Item"]["allowed_tag_categories"], self.test_config.allowed_tag_categories)
        self.assertEqual(call_args["Item"]["required_attributes"], self.test_config.required_attributes)

    def test_save_normalized_bot_metadata(self):
        """Test saving normalized bot metadata."""
        # Create test bot model
        test_bot = BotModel(
            id='test-bot-1',
            title='Test Bot',
            description='A test bot',
            instruction='Test instruction',
            create_time=1234567890.0,
            last_used_time=1234567890.0,
            public_bot_id=None,
            owner_user_id='user-1',
            is_pinned=False,
            generation_params=GenerationParamsModel(
                max_tokens=100,
                top_k=10,
                top_p=0.9,
                temperature=0.7,
                stop_sequences=[]
            ),
            agent=AgentModel(tools=[]),
            knowledge=KnowledgeModel(
                source_urls=[],
                sitemap_urls=[],
                filenames=[],
                s3_urls=[]
            ),
            sync_status='SUCCEEDED',
            sync_status_reason='',
            sync_last_exec_id='',
            published_api_stack_name=None,
            published_api_datetime=None,
            published_api_codebuild_id=None,
            display_retrieved_chunks=False,
            conversation_quick_starters=[],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
            active_models=ActiveModelsModel(),
            version=None,
            group_id='group-1',
            assistant_config=None,
            creator_config=None,
            metadata=self.test_bot_metadata
        )

        # Call the method
        self.repository.save_normalized_bot_metadata(test_bot)

        # Verify DynamoDB was called with correct data
        self.mock_bot_metadata_table.put_item.assert_called_once()
        call_args = self.mock_bot_metadata_table.put_item.call_args[1]['Item']
        
        # Verify required fields
        assert call_args['bot_id'] == 'test-bot-1'
        assert call_args['title'] == 'Test Bot'
        assert call_args['description'] == 'A test bot'
        assert 'instruction_hash' in call_args
        assert call_args['owner_user_id'] == 'user-1'
        assert call_args['is_public'] is False
        assert call_args['group_id'] == 'group-1'
        assert call_args['create_time'] == Decimal('1234567890.0')
        assert call_args['last_used_time'] == Decimal('1234567890.0')
        assert 'hierarchy' in call_args
        assert 'tags' in call_args
        assert 'attributes' in call_args
        assert 'updated_at' in call_args
        assert call_args['is_deleted'] is False
        assert 'deleted_at' not in call_args  # None values are not included in DynamoDB items

    def test_mark_bot_metadata_as_deleted(self):
        """Test marking a bot as deleted in BotsMetadataTable (synchronous version)."""
        # Setup mock
        self.mock_bot_metadata_table.update_item.return_value = {
            "Attributes": {
                "is_deleted": True,
                "deleted_at": "2023-06-30T12:34:56+00:00"
            }
        }
        
        # Create a fixed timestamp for testing
        test_datetime = datetime.fromisoformat("2023-06-30T12:34:56+00:00")
        fixed_timestamp = test_datetime.isoformat()  # Ensures consistent format
        
        with patch('app.repositories.metadata_repository.datetime') as mock_datetime:
            mock_datetime.now.return_value = test_datetime
            mock_datetime.UTC = UTC
            
            # Call method (now synchronous)
            self.repository.mark_bot_metadata_as_deleted("test-bot-id")
        
        # Assertions
        self.mock_bot_metadata_table.update_item.assert_called_once()
        
        # Check update call parameters
        call_args = self.mock_bot_metadata_table.update_item.call_args[1]
        self.assertEqual(call_args["Key"], {"bot_id": "test-bot-id"})
        self.assertEqual(call_args["UpdateExpression"], "SET is_deleted = :del_flag, deleted_at = :del_time")
        self.assertEqual(call_args["ExpressionAttributeValues"][":del_flag"], True)
        self.assertEqual(call_args["ExpressionAttributeValues"][":del_time"], fixed_timestamp)
        self.assertEqual(call_args["ConditionExpression"], "attribute_exists(bot_id)")
        self.assertEqual(call_args["ReturnValues"], "UPDATED_NEW")

    def test_mark_bot_metadata_as_deleted_not_found(self):
        """Test marking a non-existent bot as deleted handles the exception gracefully."""
        # Setup mock for ConditionalCheckFailedException
        error_response = {'Error': {'Code': 'ConditionalCheckFailedException', 'Message': 'Item does not exist'}}
        self.mock_bot_metadata_table.update_item.side_effect = ClientError(error_response, 'UpdateItem')
        
        # Call method
        result = self.repository.mark_bot_metadata_as_deleted("nonexistent-bot")
        
        # Assertions
        self.mock_bot_metadata_table.update_item.assert_called_once()
        # Method should return None on this specific error
        self.assertIsNone(result)
        
    def test_search_metadata(self):
        """Test searching for metadata based on hierarchy."""
        # Setup mock response
        expected_result = {
            'Items': [
                {
                    'bot_id': 'test-bot-1',
                    'hierarchy': [{'level': 'department', 'id': 'h1', 'name': 'Engineering'}],
                    'tags': [{'category': 'language', 'id': 't1', 'name': 'Python'}],
                    'attributes': [{'key': 'model', 'value': 'claude-3', 'id': 'a1'}]
                }
            ],
            'LastEvaluatedKey': None
        }
        self.mock_bot_metadata_table.query.return_value = expected_result

        # Call method
        result = self.repository.find_bots_by_hierarchy('department', 'h1')

        # Verify query parameters
        self.mock_bot_metadata_table.query.assert_called_once()
        call_args = self.mock_bot_metadata_table.query.call_args[1]
        assert call_args['IndexName'] == 'HierarchyIndex'
        assert 'KeyConditionExpression' in call_args
        assert call_args['Limit'] == 50

        # Assertions
        assert result['items'] == expected_result['Items']
        assert result['last_evaluated_key'] == expected_result['LastEvaluatedKey']

    def test_search_metadata_empty_results(self):
        """Test search with no matching results."""
        # Mock response for no results
        self.mock_bot_metadata_table.query.return_value = {
            'Items': [],
            'LastEvaluatedKey': None
        }

        # Call method
        result = self.repository.find_bots_by_hierarchy('department', 'h1')

        # Verify query parameters
        self.mock_bot_metadata_table.query.assert_called_once()
        call_args = self.mock_bot_metadata_table.query.call_args[1]
        assert call_args['IndexName'] == 'HierarchyIndex'
        assert 'KeyConditionExpression' in call_args
        assert call_args['Limit'] == 50

        # Assertions
        assert len(result['items']) == 0
        assert result['last_evaluated_key'] is None

    def test_search_metadata_error_handling(self):
        """Test search error handling."""
        # Setup mock to raise exception
        error_response = {
            'Error': {
                'Code': 'InternalServerError',
                'Message': 'Internal server error'
            }
        }
        self.mock_bot_metadata_table.query.side_effect = ClientError(error_response, 'Query')

        # Call method and expect empty results (error is logged but not raised)
        result = self.repository.find_bots_by_hierarchy('department', 'h1')
        assert result['items'] == []
        assert result['last_evaluated_key'] is None

    def test_search_metadata_with_tag_query(self):
        """Test searching with tag criteria."""
        # Setup mock response
        expected_result = {
            'Items': [
                {
                    'bot_id': 'test-bot-1',
                    'tags': [{'category': 'language', 'id': 't1', 'name': 'Python'}]
                }
            ],
            'LastEvaluatedKey': None
        }
        self.mock_bot_metadata_table.query.return_value = expected_result

        # Call method
        result = self.repository.find_bots_by_tag_category('language')

        # Verify query parameters
        self.mock_bot_metadata_table.query.assert_called_once()
        call_args = self.mock_bot_metadata_table.query.call_args[1]
        assert call_args['IndexName'] == 'TagCategoryIndex'
        assert 'KeyConditionExpression' in call_args
        assert call_args['Limit'] == 50

        # Assertions
        assert result['items'] == expected_result['Items']
        assert result['last_evaluated_key'] == expected_result['LastEvaluatedKey']

    def test_search_metadata_with_attribute_query(self):
        """Test searching with attribute criteria."""
        # Setup mock response
        expected_result = {
            'Items': [
                {
                    'bot_id': 'test-bot-2',
                    'attributes': [{'key': 'model', 'value': 'claude-3', 'id': 'a2'}]
                }
            ],
            'LastEvaluatedKey': None
        }
        self.mock_bot_metadata_table.query.return_value = expected_result

        # Call method
        result = self.repository.find_bots_by_attribute_key('model')

        # Verify query parameters
        self.mock_bot_metadata_table.query.assert_called_once()
        call_args = self.mock_bot_metadata_table.query.call_args[1]
        assert call_args['IndexName'] == 'AttributeKeyIndex'
        assert 'KeyConditionExpression' in call_args
        assert call_args['Limit'] == 50

        # Assertions
        assert result['items'] == expected_result['Items']
        assert result['last_evaluated_key'] == expected_result['LastEvaluatedKey']

    def test_get_bot_metadata(self):
        """Test retrieving bot metadata."""
        # Create test data
        test_bot_id = "test-bot-1"
        test_item = {
            'bot_id': test_bot_id,
            'title': 'Test Bot',
            'description': 'A test bot',
            'instruction_hash': 'abc123',
            'owner_user_id': 'user-1',
            'is_public': True,
            'group_id': 'group-1',
            'create_time': Decimal('1234567890.0'),
            'last_used_time': Decimal('1234567890.0'),
            'hierarchy': [
                {
                    'id': 'school-1',
                    'name': 'Test School',
                    'level': 'school',
                    'path': ['Test School']
                }
            ],
            'tags': [
                {
                    'id': 'tag-1',
                    'name': 'Test Tag',
                    'category': 'test',
                    'value': 'test'
                }
            ],
            'attributes': [
                {
                    'id': 'attr-1',
                    'name': 'Test Attribute',
                    'key': 'test_key',
                    'value': 'test_value'
                }
            ],
            'updated_at': '2024-03-20T12:00:00Z',
            'is_deleted': False,
            'deleted_at': None
        }

        # Mock DynamoDB response
        self.mock_bot_metadata_table.get_item.return_value = {'Item': test_item}

        # Call the method
        result = self.repository.get_bot_metadata(test_bot_id)

        # Verify the result
        assert result is not None
        assert result.bot_id == test_bot_id
        assert result.title == 'Test Bot'
        assert result.description == 'A test bot'
        assert result.instruction_hash == 'abc123'
        assert result.owner_user_id == 'user-1'
        assert result.is_public is True
        assert result.group_id == 'group-1'
        assert result.create_time == 1234567890.0
        assert result.last_used_time == 1234567890.0
        assert len(result.hierarchy) == 1
        assert len(result.tags) == 1
        assert len(result.attributes) == 1
        assert result.updated_at == '2024-03-20T12:00:00Z'
        assert result.is_deleted is False
        assert result.deleted_at is None

        # Verify DynamoDB was called correctly
        self.mock_bot_metadata_table.get_item.assert_called_once_with(Key={'bot_id': test_bot_id})

    def test_get_bot_metadata_not_found(self):
        """Test retrieving non-existent bot metadata."""
        # Mock DynamoDB response for non-existent item
        self.mock_bot_metadata_table.get_item.return_value = {}

        # Call the method
        result = self.repository.get_bot_metadata('non-existent-bot')

        # Verify the result
        assert result is None


if __name__ == "__main__":
    unittest.main() 