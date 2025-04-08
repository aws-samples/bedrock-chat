"""Test the metadata routes with enhanced coverage."""

import sys
import unittest
from unittest.mock import MagicMock, patch

from backend.app.repositories.models.bot_metadata import BotMetadata, MetadataConfig
from fastapi.testclient import TestClient
from app.main import app
from tests.base_test import ImportTrackingTestCase

client = TestClient(app)


class TestMetadataRoutesEnhanced(ImportTrackingTestCase):
    """Enhanced test case for metadata routes."""
    
    @classmethod
    def _import_modules(cls):
        """Import modules needed for this test class."""
        import app.routes.metadata
        import app.repositories.metadata_repository
        
    def setUp(self):
        # Create mock for metadata_service
        self.mock_service_patcher = patch("app.routes.metadata.metadata_service")
        self.mock_service = self.mock_service_patcher.start()
        self.addCleanup(self.mock_service_patcher.stop)
        
        # Create mock for get_current_user dependency
        self.mock_user_patcher = patch("app.dependencies.get_current_user")
        self.mock_user = self.mock_user_patcher.start()
        self.addCleanup(self.mock_user_patcher.stop)
        
        # Setup user
        self.mock_user.return_value = MagicMock(
            id="test-user",
            name="Test User",
            groups=["Admin"]
        )
        
    def test_get_tag_values(self):
        """Test getting tag values."""
        # Setup mock return value
        self.mock_service.get_tag_values.return_value = ["tag1", "tag2"]
        
        # Make the request
        response = client.get("/api/metadata/tags")
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["tag1", "tag2"])
        
        # Verify the service method was called
        self.mock_service.get_tag_values.assert_called_once()
    
    def test_get_hierarchy_values(self):
        """Test getting hierarchy values."""
        # Setup mock return value
        self.mock_service.get_hierarchy_values.return_value = ["hier1", "hier2"]
        
        # Make the request
        response = client.get("/api/metadata/hierarchies")
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["hier1", "hier2"])
        
        # Verify the service method was called
        self.mock_service.get_hierarchy_values.assert_called_once()
    
    def test_get_bot_metadata(self):
        """Test getting bot metadata endpoint."""
        # Create test metadata
        test_metadata = BotMetadata(
            bot_id='test-bot-1',
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

        # Mock service response
        self.mock_service.get_bot_metadata.return_value = test_metadata

        # Call the endpoint
        response = client.get(f"/api/v1/bots/{test_metadata.bot_id}/metadata")

        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert data['bot_id'] == test_metadata.bot_id
        assert data['title'] == test_metadata.title
        assert data['description'] == test_metadata.description
        assert data['instruction_hash'] == test_metadata.instruction_hash
        assert data['owner_user_id'] == test_metadata.owner_user_id
        assert data['is_public'] == test_metadata.is_public
        assert data['group_id'] == test_metadata.group_id
        assert data['create_time'] == test_metadata.create_time
        assert data['last_used_time'] == test_metadata.last_used_time
        assert len(data['hierarchy']) == len(test_metadata.hierarchy)
        assert len(data['tags']) == len(test_metadata.tags)
        assert len(data['attributes']) == len(test_metadata.attributes)
        assert data['updated_at'] == test_metadata.updated_at
        assert data['is_deleted'] == test_metadata.is_deleted
        assert data['deleted_at'] == test_metadata.deleted_at
    
    def test_get_bot_metadata_not_found(self):
        """Test getting bot metadata endpoint for non-existent bot."""
        # Mock service response for non-existent bot
        self.mock_service.get_bot_metadata.return_value = None

        # Call the endpoint
        response = client.get("/api/v1/bots/non-existent-bot/metadata")

        # Verify response
        assert response.status_code == 404
    
    def test_update_bot_metadata(self):
        """Test updating bot metadata endpoint."""
        # Create test metadata
        test_metadata = BotMetadata(
            bot_id='test-bot-1',
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

        # Create update request
        update_data = {
            'title': 'Updated Bot',
            'description': 'An updated bot',
            'is_public': False,
            'tags': [
                {
                    'id': 'tag-2',
                    'name': 'Updated Tag',
                    'category': 'test',
                    'value': 'updated'
                }
            ]
        }

        # Mock service response
        self.mock_service.update_bot_metadata.return_value = test_metadata

        # Call the endpoint
        response = client.put(
            f"/api/v1/bots/{test_metadata.bot_id}/metadata",
            json=update_data
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert data['bot_id'] == test_metadata.bot_id
        assert data['title'] == test_metadata.title
        assert data['description'] == test_metadata.description
        assert data['instruction_hash'] == test_metadata.instruction_hash
        assert data['owner_user_id'] == test_metadata.owner_user_id
        assert data['is_public'] == test_metadata.is_public
        assert data['group_id'] == test_metadata.group_id
        assert data['create_time'] == test_metadata.create_time
        assert data['last_used_time'] == test_metadata.last_used_time
        assert len(data['hierarchy']) == len(test_metadata.hierarchy)
        assert len(data['tags']) == len(test_metadata.tags)
        assert len(data['attributes']) == len(test_metadata.attributes)
        assert data['updated_at'] == test_metadata.updated_at
        assert data['is_deleted'] == test_metadata.is_deleted
        assert data['deleted_at'] == test_metadata.deleted_at
    
    def test_search_bots(self):
        """Test searching for bots."""
        # Setup mock return value
        test_metadata = [
            BotMetadata(
                id="test-bot-1",
                title="Test Bot 1",
                description="Test bot 1",
                tags=["tag1"],
                hierarchies=["hier1"]
            ),
            BotMetadata(
                id="test-bot-2",
                title="Test Bot 2",
                description="Test bot 2",
                tags=["tag2"],
                hierarchies=["hier2"]
            )
        ]
        self.mock_service.search_bots.return_value = {
            "items": test_metadata,
            "total": 2,
            "page": 1,
            "size": 10
        }
        
        # Make the request
        response = client.get("/api/metadata/bots?search=test")
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 2)
        self.assertEqual(len(response.json()["items"]), 2)
        
        # Verify the service method was called
        self.mock_service.search_bots.assert_called_once()
