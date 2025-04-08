import sys
import unittest
from unittest.mock import MagicMock, patch

from backend.app.repositories.models.bot_metadata import BotMetadata, MetadataConfig
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestMetadataRoutes(unittest.TestCase):
    def setUp(self):
        # Create mock for metadata_service
        self.mock_service_patcher = patch('app.routes.metadata.metadata_service')
        self.mock_service = self.mock_service_patcher.start()
        
        # Create mock for get_current_user dependency
        self.mock_user_patcher = patch('app.dependencies.get_current_user')
        self.mock_user = self.mock_user_patcher.start()
        
        # Setup user
        self.mock_user.return_value = MagicMock(
            id="test-user",
            name="Test User",
            groups=["Admin"]
        )
        
    def tearDown(self):
        self.mock_service_patcher.stop()
        self.mock_user_patcher.stop()
        
    def test_get_config(self):
        """Test GET /metadata/config endpoint."""
        # Setup mock
        self.mock_service.repository.get_config.return_value = MetadataConfig(
            allowed_hierarchy_levels=["district", "school"],
            allowed_tag_categories=["subject", "grade_level"],
            required_attributes=["language"]
        )
        
        # Call endpoint
        response = client.get("/metadata/config")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("allowed_hierarchy_levels", data["data"])
        self.assertEqual(data["data"]["allowed_hierarchy_levels"], ["district", "school"])
        
    def test_update_config(self):
        """Test POST /metadata/config endpoint."""
        # Test data
        config_data = {
            "allowed_hierarchy_levels": ["district", "school", "department"],
            "allowed_tag_categories": ["subject", "grade_level"],
            "required_attributes": ["language", "target_age"]
        }
        
        # Call endpoint
        response = client.post("/metadata/config", json=config_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.mock_service.update_config.assert_called_once()
        
    def test_get_bot_metadata(self):
        """Test GET /metadata/bot/{bot_id} endpoint."""
        # Setup mock
        bot_id = "test-bot"
        self.mock_service.get_bot_metadata.return_value = BotMetadata()
        
        # Call endpoint
        response = client.get(f"/metadata/bot/{bot_id}")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("hierarchy", data["data"])
        self.assertIn("tags", data["data"])
        self.assertIn("attributes", data["data"])
        self.mock_service.get_bot_metadata.assert_called_once_with(bot_id)
        
    def test_update_bot_metadata(self):
        """Test POST /metadata/bot/{bot_id} endpoint."""
        # Test data
        bot_id = "test-bot"
        metadata_data = {
            "hierarchy": [
                {
                    "id": "hier-1",
                    "name": "Hierarchy 1",
                    "level": "school",
                    "parent_id": None,
                    "path": ["Hierarchy 1"]
                }
            ],
            "tags": [
                {
                    "id": "tag-1",
                    "name": "Tag 1",
                    "category": "subject"
                }
            ],
            "attributes": [
                {
                    "id": "attr-1",
                    "name": "Attribute 1",
                    "key": "language",
                    "value": "en",
                    "data_type": "string"
                }
            ]
        }
        
        # Call endpoint
        response = client.post(f"/metadata/bot/{bot_id}", json=metadata_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.mock_service.update_bot_metadata.assert_called_once()
        
    def test_get_hierarchy_values(self):
        """Test GET /metadata/values/hierarchy endpoint."""
        # Setup mock
        hierarchy_values = [
            {
                "id": "hier-1",
                "name": "Hierarchy 1",
                "level": "school"
            },
            {
                "id": "hier-2",
                "name": "Hierarchy 2",
                "level": "district"
            }
        ]
        self.mock_service.get_hierarchy_values.return_value = hierarchy_values
        
        # Call endpoint
        response = client.get("/metadata/values/hierarchy")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"], hierarchy_values)
        self.mock_service.get_hierarchy_values.assert_called_once()
        
    def test_get_tag_values(self):
        """Test GET /metadata/values/tags endpoint."""
        # Setup mock
        tag_values = [
            {
                "id": "tag-1",
                "name": "Tag 1",
                "category": "subject"
            },
            {
                "id": "tag-2",
                "name": "Tag 2",
                "category": "grade_level"
            }
        ]
        self.mock_service.get_tag_values.return_value = tag_values
        
        # Call endpoint
        response = client.get("/metadata/values/tags")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"], tag_values)
        self.mock_service.get_tag_values.assert_called_once()
        
    def test_add_hierarchy_value(self):
        """Test POST /metadata/values/hierarchy endpoint."""
        # Test data
        hierarchy_value = {
            "id": "hier-new",
            "name": "New Hierarchy",
            "level": "school",
            "parent_id": None,
            "path": ["New Hierarchy"]
        }
        
        # Call endpoint
        response = client.post("/metadata/values/hierarchy", json=hierarchy_value)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.mock_service.add_hierarchy_value.assert_called_once_with(hierarchy_value)
        
    def test_add_tag_value(self):
        """Test POST /metadata/values/tags endpoint."""
        # Test data
        tag_value = {
            "id": "tag-new",
            "name": "New Tag",
            "category": "subject"
        }
        
        # Call endpoint
        response = client.post("/metadata/values/tags", json=tag_value)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.mock_service.add_tag_value.assert_called_once_with(tag_value)
        
    def test_delete_hierarchy_value(self):
        """Test DELETE /metadata/values/hierarchy/{value_id} endpoint."""
        # Test data
        value_id = "hier-1"
        
        # Call endpoint
        response = client.delete(f"/metadata/values/hierarchy/{value_id}")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.mock_service.delete_hierarchy_value.assert_called_once_with(value_id)
        
    def test_delete_tag_value(self):
        """Test DELETE /metadata/values/tags/{value_id} endpoint."""
        # Test data
        value_id = "tag-1"
        
        # Call endpoint
        response = client.delete(f"/metadata/values/tags/{value_id}")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.mock_service.delete_tag_value.assert_called_once_with(value_id)
        
    def test_search_bots(self):
        """Test POST /metadata/search endpoint."""
        # Setup mock
        search_results = {
            'items': ["bot-1", "bot-2"],
            'last_evaluated_key': None
        }
        self.mock_service.search_bots.return_value = search_results
        
        # Test data
        query = {
            "hierarchy": {"level": "school"},
            "tags": {"category": "subject"}
        }
        
        # Call endpoint
        response = client.post("/metadata/search", json=query)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"], search_results['items'])
        self.assertEqual(data["last_evaluated_key"], search_results['last_evaluated_key'])
        self.mock_service.search_bots.assert_called_once()
        
    def test_search_bots_with_pagination(self):
        """Test POST /metadata/search endpoint with pagination parameters."""
        # Setup mock
        search_results = {
            'items': ["bot-3", "bot-4"],
            'last_evaluated_key': {"bot_id": "bot-4"}
        }
        self.mock_service.search_bots.return_value = search_results
        
        # Test data
        query = {"tags": {"category": "subject"}}
        last_key = {"bot_id": "bot-2"}
        limit = 2
        
        # Call endpoint
        response = client.post(
            "/metadata/search", 
            json=query, 
            params={"limit": limit, "last_evaluated_key": '{"bot_id": "bot-2"}'}
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"], search_results['items'])
        self.assertEqual(data["last_evaluated_key"], search_results['last_evaluated_key'])
        
    def test_get_metadata_stats(self):
        """Test GET /metadata/stats endpoint."""
        # Setup mock
        stats = {
            'total_bots': 5,
            'hierarchy_usage': {'school': 3, 'department': 2},
            'tag_usage': {'subject': 4, 'grade_level': 1},
            'attribute_usage': {'language': 5, 'target_age': 3}
        }
        self.mock_service.get_metadata_stats.return_value = stats
        
        # Call endpoint
        response = client.get("/metadata/stats")
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"], stats)
        self.mock_service.get_metadata_stats.assert_called_once()
        
    def test_error_handling(self):
        """Test error handling in metadata routes."""
        # Setup mock to raise an exception
        error_message = "Test error"
        self.mock_service.get_bot_metadata.side_effect = Exception(error_message)
        
        # Call endpoint
        response = client.get("/metadata/bot/test-bot")
        
        # Assertions
        self.assertEqual(response.status_code, 200)  # FastAPI wrapper keeps 200 but sets success=False
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], error_message)


if __name__ == "__main__":
    unittest.main() 