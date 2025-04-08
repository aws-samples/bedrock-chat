import sys
import unittest
from unittest.mock import MagicMock, patch

from backend.app.repositories.models.bot_metadata import BotMetadata, MetadataConfig, HierarchyMetadata, TagMetadata, AttributeMetadata
from app.services.metadata_service import MetadataService
from app.services.metadata_validator import MetadataValidator, ValidationError


class TestMetadataService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create mocks
        self.mock_repository = MagicMock()
        self.mock_validator = MagicMock()
        
        # Create a service with mocked repository
        self.service = MetadataService()
        self.service.repository = self.mock_repository
        self.service._validator = self.mock_validator
        
        # Create test data
        self.test_config = MetadataConfig(
            allowed_hierarchy_levels=["district", "school", "department"],
            allowed_tag_categories=["subject", "grade_level"],
            required_attributes=["language", "target_age"]
        )
        
        self.test_metadata = BotMetadata(
            hierarchy=[
                HierarchyMetadata(
                    id="test-hierarchy",
                    name="Test Hierarchy",
                    level="school",
                    parent_id=None,
                    path=["Test Hierarchy"]
                )
            ],
            tags=[
                TagMetadata(
                    id="test-tag",
                    name="Test Tag",
                    category="subject"
                )
            ],
            attributes=[
                AttributeMetadata(
                    id="test-attr",
                    name="Test Attribute",
                    key="language",
                    value="en",
                    data_type="string"
                )
            ]
        )
        
    async def test_get_validator_new(self):
        """Test getting a new validator when none exists."""
        # Reset validator
        self.service._validator = None
        self.service._config = None
        
        # Mock repository response
        self.mock_repository.get_config.return_value = self.test_config
        
        # Call method
        result = await self.service.get_validator()
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MetadataValidator)
        self.mock_repository.get_config.assert_called_once()
        
    async def test_get_validator_existing(self):
        """Test getting an existing validator."""
        # Create a mock validator
        mock_validator = MagicMock()
        self.service._validator = mock_validator
        self.service._config = self.test_config
        
        # Call method
        result = await self.service.get_validator()
        
        # Assertions
        self.assertEqual(result, mock_validator)
        self.mock_repository.get_config.assert_not_called()
        
    async def test_update_config(self):
        """Test updating configuration."""
        # Call method
        await self.service.update_config(self.test_config)
        
        # Assertions
        self.mock_repository.save_config.assert_called_once_with(self.test_config)
        self.assertEqual(self.service._config, self.test_config)
        self.assertIsNotNone(self.service._validator)
        
    async def test_get_bot_metadata(self):
        """Test retrieving bot metadata."""
        # Create test data
        test_bot_id = "test-bot-1"
        test_metadata = BotMetadata(
            bot_id=test_bot_id,
            title='Test Bot',
            description='A test bot',
            instruction_hash='abc123',
            owner_user_id='user-1',
            is_public=True,
            group_id='group-1',
            create_time=1234567890.0,
            last_used_time=1234567890.0,
            hierarchy=[
                {
                    'id': 'school-1',
                    'name': 'Test School',
                    'level': 'school',
                    'path': ['Test School']
                }
            ],
            tags=[
                {
                    'id': 'tag-1',
                    'name': 'Test Tag',
                    'category': 'test',
                    'value': 'test'
                }
            ],
            attributes=[
                {
                    'id': 'attr-1',
                    'name': 'Test Attribute',
                    'key': 'test_key',
                    'value': 'test_value'
                }
            ],
            updated_at='2024-03-20T12:00:00Z',
            is_deleted=False,
            deleted_at=None
        )

        # Mock repository response
        self.mock_repository.get_bot_metadata.return_value = test_metadata

        # Call the method
        result = self.service.get_bot_metadata(test_bot_id)

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

        # Verify repository was called correctly
        self.mock_repository.get_bot_metadata.assert_called_once_with(test_bot_id)

    async def test_get_bot_metadata_not_found(self):
        """Test retrieving non-existent bot metadata."""
        # Mock repository response for non-existent item
        self.mock_repository.get_bot_metadata.return_value = None

        # Call the method
        result = self.service.get_bot_metadata('non-existent-bot')

        # Verify the result
        assert result is None

    async def test_save_bot_metadata(self):
        """Test saving bot metadata."""
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
            sync_status='synced',
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
            creator_config=None
        )

        # Call the method
        self.service.save_bot_metadata(test_bot)

        # Verify repository was called correctly
        self.mock_repository.save_normalized_bot_metadata.assert_called_once_with(test_bot)
        
    async def test_update_bot_metadata_valid(self):
        """Test updating bot metadata with valid data."""
        # Mock validator
        self.mock_validator.validate.return_value = True
        
        # Call method
        bot_id = "test-bot"
        await self.service.update_bot_metadata(bot_id, self.test_metadata)
        
        # Assertions
        self.mock_validator.validate.assert_called_once_with(self.test_metadata)
        self.mock_repository.save_bot_metadata.assert_called_once_with(bot_id, self.test_metadata)
        
    async def test_update_bot_metadata_invalid(self):
        """Test updating bot metadata with invalid data."""
        # Mock validator to raise an exception
        error_message = "Validation failed"
        self.mock_validator.validate.side_effect = ValidationError(error_message)
        
        # Call method and check exception
        bot_id = "test-bot"
        with self.assertRaises(ValidationError) as context:
            await self.service.update_bot_metadata(bot_id, self.test_metadata)
            
        # Assertions
        self.assertEqual(str(context.exception), error_message)
        self.mock_validator.validate.assert_called_once_with(self.test_metadata)
        self.mock_repository.save_bot_metadata.assert_not_called()
        
    async def test_search_bots(self):
        """Test searching for bots."""
        # Mock repository response
        expected_result = {
            'items': ["bot-1", "bot-2"],
            'last_evaluated_key': None
        }
        self.mock_repository.search_metadata.return_value = expected_result
        
        # Call method
        query = {"hierarchy": {"level": "school"}}
        result = await self.service.search_bots(query)
        
        # Assertions
        self.assertEqual(result, expected_result)
        self.mock_repository.search_metadata.assert_called_once_with(query, 50, None)
        
    async def test_search_bots_with_pagination(self):
        """Test searching for bots with pagination."""
        # Mock repository response
        expected_result = {
            'items': ["bot-3", "bot-4"],
            'last_evaluated_key': {'bot_id': 'bot-4'}
        }
        self.mock_repository.search_metadata.return_value = expected_result
        
        # Call method
        query = {"tags": {"category": "subject"}}
        last_key = {'bot_id': 'bot-2'}
        limit = 2
        result = await self.service.search_bots(query, limit, last_key)
        
        # Assertions
        self.assertEqual(result, expected_result)
        self.mock_repository.search_metadata.assert_called_once_with(query, limit, last_key)
        
    async def test_get_hierarchy_values(self):
        """Test getting hierarchy values."""
        # Mock repository response
        expected_values = [
            {'id': 'hier-1', 'name': 'Hierarchy 1', 'level': 'district'},
            {'id': 'hier-2', 'name': 'Hierarchy 2', 'level': 'school'}
        ]
        self.mock_repository.get_metadata_values.return_value = expected_values
        
        # Call method
        result = await self.service.get_hierarchy_values()
        
        # Assertions
        self.assertEqual(result, expected_values)
        self.mock_repository.get_metadata_values.assert_called_once_with('hierarchy')
        
    async def test_get_tag_values(self):
        """Test getting tag values."""
        # Mock repository response
        expected_values = [
            {'id': 'tag-1', 'name': 'Tag 1', 'category': 'subject'},
            {'id': 'tag-2', 'name': 'Tag 2', 'category': 'grade_level'}
        ]
        self.mock_repository.get_metadata_values.return_value = expected_values
        
        # Call method
        result = await self.service.get_tag_values()
        
        # Assertions
        self.assertEqual(result, expected_values)
        self.mock_repository.get_metadata_values.assert_called_once_with('tag')
        
    async def test_add_hierarchy_value(self):
        """Test adding a hierarchy value."""
        # Test data
        hierarchy_value = {
            'id': 'hier-new',
            'name': 'New Hierarchy',
            'level': 'school',
            'parent_id': None,
            'path': ['New Hierarchy']
        }
        
        # Call method
        await self.service.add_hierarchy_value(hierarchy_value)
        
        # Assertions
        self.mock_repository.save_metadata_value.assert_called_once_with('hierarchy', hierarchy_value)
        
    async def test_add_tag_value(self):
        """Test adding a tag value."""
        # Test data
        tag_value = {
            'id': 'tag-new',
            'name': 'New Tag',
            'category': 'subject'
        }
        
        # Call method
        await self.service.add_tag_value(tag_value)
        
        # Assertions
        self.mock_repository.save_metadata_value.assert_called_once_with('tag', tag_value)
        
    async def test_delete_hierarchy_value(self):
        """Test deleting a hierarchy value."""
        # Call method
        value_id = "hier-1"
        await self.service.delete_hierarchy_value(value_id)
        
        # Assertions
        self.mock_repository.delete_metadata_value.assert_called_once_with('hierarchy', value_id)
        
    async def test_delete_tag_value(self):
        """Test deleting a tag value."""
        # Call method
        value_id = "tag-1"
        await self.service.delete_tag_value(value_id)
        
        # Assertions
        self.mock_repository.delete_metadata_value.assert_called_once_with('tag', value_id)
        
    async def test_get_metadata_stats(self):
        """Test getting metadata statistics."""
        # Mock repository scan response
        mock_items = [
            {
                'bot_id': 'bot-1',
                'hierarchy': [
                    {'level': 'school', 'id': 'school-1'},
                    {'level': 'department', 'id': 'dept-1'}
                ],
                'tags': [
                    {'category': 'subject', 'id': 'subj-1'},
                    {'category': 'grade_level', 'id': 'grade-1'}
                ],
                'attributes': [
                    {'key': 'language', 'id': 'lang-1'},
                    {'key': 'target_age', 'id': 'age-1'}
                ]
            },
            {
                'bot_id': 'bot-2',
                'hierarchy': [
                    {'level': 'school', 'id': 'school-2'}
                ],
                'tags': [
                    {'category': 'subject', 'id': 'subj-2'}
                ],
                'attributes': [
                    {'key': 'language', 'id': 'lang-2'}
                ]
            }
        ]
        
        self.mock_repository.bot_metadata_table.scan.return_value = {'Items': mock_items}
        
        # Call method
        stats = await self.service.get_metadata_stats()
        
        # Assertions
        self.assertEqual(stats['total_bots'], 2)
        self.assertEqual(stats['hierarchy_usage']['school'], 2)
        self.assertEqual(stats['hierarchy_usage']['department'], 1)
        self.assertEqual(stats['tag_usage']['subject'], 2)
        self.assertEqual(stats['tag_usage']['grade_level'], 1)
        self.assertEqual(stats['attribute_usage']['language'], 2)
        self.assertEqual(stats['attribute_usage']['target_age'], 1)
        self.mock_repository.bot_metadata_table.scan.assert_called()


if __name__ == "__main__":
    unittest.main() 