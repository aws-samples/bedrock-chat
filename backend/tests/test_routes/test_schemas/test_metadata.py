import sys
import unittest
from datetime import datetime

from backend.app.repositories.models.bot_metadata import (
    MetadataValue,
    HierarchyMetadata,
    TagMetadata,
    AttributeMetadata,
    BotMetadata,
    MetadataConfig,
    SearchQuery
)


class TestMetadataSchemas(unittest.TestCase):
    def test_metadata_value_schema(self):
        """Test the MetadataValue schema validation."""
        # Test valid initialization
        value = MetadataValue(id="test-id", name="Test Name")
        self.assertEqual(value.id, "test-id")
        self.assertEqual(value.name, "Test Name")
        
        # Test schema validation
        value_dict = value.model_dump()
        self.assertIn("id", value_dict)
        self.assertIn("name", value_dict)
        
    def test_hierarchy_metadata_schema(self):
        """Test the HierarchyMetadata schema validation."""
        # Test valid initialization with all fields
        hierarchy = HierarchyMetadata(
            id="hier-1",
            name="Hierarchy 1",
            level="school",
            parent_id="parent-1",
            path=["Parent", "Hierarchy 1"]
        )
        
        self.assertEqual(hierarchy.id, "hier-1")
        self.assertEqual(hierarchy.name, "Hierarchy 1")
        self.assertEqual(hierarchy.level, "school")
        self.assertEqual(hierarchy.parent_id, "parent-1")
        self.assertEqual(hierarchy.path, ["Parent", "Hierarchy 1"])
        
        # Test valid initialization with minimum fields
        hierarchy_min = HierarchyMetadata(
            id="hier-2",
            name="Hierarchy 2",
            level="district",
            path=["Hierarchy 2"]
        )
        
        self.assertEqual(hierarchy_min.id, "hier-2")
        self.assertEqual(hierarchy_min.name, "Hierarchy 2")
        self.assertEqual(hierarchy_min.level, "district")
        self.assertIsNone(hierarchy_min.parent_id)
        self.assertEqual(hierarchy_min.path, ["Hierarchy 2"])
        
        # Test schema validation
        hierarchy_dict = hierarchy.model_dump()
        self.assertIn("id", hierarchy_dict)
        self.assertIn("name", hierarchy_dict)
        self.assertIn("level", hierarchy_dict)
        self.assertIn("parent_id", hierarchy_dict)
        self.assertIn("path", hierarchy_dict)
        
    def test_tag_metadata_schema(self):
        """Test the TagMetadata schema validation."""
        # Test valid initialization
        tag = TagMetadata(
            id="tag-1",
            name="Tag 1",
            category="subject"
        )
        
        self.assertEqual(tag.id, "tag-1")
        self.assertEqual(tag.name, "Tag 1")
        self.assertEqual(tag.category, "subject")
        
        # Test schema validation
        tag_dict = tag.model_dump()
        self.assertIn("id", tag_dict)
        self.assertIn("name", tag_dict)
        self.assertIn("category", tag_dict)
        
    def test_attribute_metadata_schema(self):
        """Test the AttributeMetadata schema validation."""
        # Test valid initialization with string value
        attr_string = AttributeMetadata(
            id="attr-1",
            name="Attribute 1",
            key="language",
            value="en",
            data_type="string"
        )
        
        self.assertEqual(attr_string.id, "attr-1")
        self.assertEqual(attr_string.name, "Attribute 1")
        self.assertEqual(attr_string.key, "language")
        self.assertEqual(attr_string.value, "en")
        self.assertEqual(attr_string.data_type, "string")
        
        # Test valid initialization with number value
        attr_number = AttributeMetadata(
            id="attr-2",
            name="Attribute 2",
            key="target_age",
            value=12,
            data_type="number"
        )
        
        self.assertEqual(attr_number.id, "attr-2")
        self.assertEqual(attr_number.name, "Attribute 2")
        self.assertEqual(attr_number.key, "target_age")
        self.assertEqual(attr_number.value, 12)
        self.assertEqual(attr_number.data_type, "number")
        
        # Test valid initialization with boolean value
        attr_boolean = AttributeMetadata(
            id="attr-3",
            name="Attribute 3",
            key="is_certified",
            value=True,
            data_type="boolean"
        )
        
        self.assertEqual(attr_boolean.id, "attr-3")
        self.assertEqual(attr_boolean.name, "Attribute 3")
        self.assertEqual(attr_boolean.key, "is_certified")
        self.assertEqual(attr_boolean.value, True)
        self.assertEqual(attr_boolean.data_type, "boolean")
        
        # Test valid initialization with datetime value
        dt = datetime.now()
        attr_datetime = AttributeMetadata(
            id="attr-4",
            name="Attribute 4",
            key="created_at",
            value=dt.isoformat(),
            data_type="datetime"
        )
        
        self.assertEqual(attr_datetime.id, "attr-4")
        self.assertEqual(attr_datetime.name, "Attribute 4")
        self.assertEqual(attr_datetime.key, "created_at")
        self.assertEqual(attr_datetime.value, dt.isoformat())
        self.assertEqual(attr_datetime.data_type, "datetime")
        
        # Test schema validation
        attr_dict = attr_string.model_dump()
        self.assertIn("id", attr_dict)
        self.assertIn("name", attr_dict)
        self.assertIn("key", attr_dict)
        self.assertIn("value", attr_dict)
        self.assertIn("data_type", attr_dict)
        
    def test_bot_metadata_schema(self):
        """Test bot metadata schema validation."""
        # Create test data
        test_data = {
            'bot_id': 'test-bot-1',
            'title': 'Test Bot',
            'description': 'A test bot',
            'instruction_hash': 'abc123',
            'owner_user_id': 'user-1',
            'is_public': True,
            'group_id': 'group-1',
            'create_time': 1234567890.0,
            'last_used_time': 1234567890.0,
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

        # Create schema instance
        schema = BotMetadataSchema()

        # Validate data
        result = schema.load(test_data)

        # Verify result
        assert result.bot_id == test_data['bot_id']
        assert result.title == test_data['title']
        assert result.description == test_data['description']
        assert result.instruction_hash == test_data['instruction_hash']
        assert result.owner_user_id == test_data['owner_user_id']
        assert result.is_public == test_data['is_public']
        assert result.group_id == test_data['group_id']
        assert result.create_time == test_data['create_time']
        assert result.last_used_time == test_data['last_used_time']
        assert len(result.hierarchy) == len(test_data['hierarchy'])
        assert len(result.tags) == len(test_data['tags'])
        assert len(result.attributes) == len(test_data['attributes'])
        assert result.updated_at == test_data['updated_at']
        assert result.is_deleted == test_data['is_deleted']
        assert result.deleted_at == test_data['deleted_at']

    def test_bot_metadata_schema_missing_required_fields(self):
        """Test bot metadata schema validation with missing required fields."""
        # Create test data with missing required fields
        test_data = {
            'bot_id': 'test-bot-1',
            'title': 'Test Bot',
            'description': 'A test bot',
            'instruction_hash': 'abc123',
            'owner_user_id': 'user-1',
            'is_public': True,
            'group_id': 'group-1',
            'create_time': 1234567890.0,
            'last_used_time': 1234567890.0,
            'hierarchy': [],
            'tags': [],
            'attributes': [],
            'updated_at': '2024-03-20T12:00:00Z',
            'is_deleted': False,
            'deleted_at': None
        }

        # Create schema instance
        schema = BotMetadataSchema()

        # Validate data
        result = schema.load(test_data)

        # Verify result
        assert result.bot_id == test_data['bot_id']
        assert result.title == test_data['title']
        assert result.description == test_data['description']
        assert result.instruction_hash == test_data['instruction_hash']
        assert result.owner_user_id == test_data['owner_user_id']
        assert result.is_public == test_data['is_public']
        assert result.group_id == test_data['group_id']
        assert result.create_time == test_data['create_time']
        assert result.last_used_time == test_data['last_used_time']
        assert len(result.hierarchy) == 0
        assert len(result.tags) == 0
        assert len(result.attributes) == 0
        assert result.updated_at == test_data['updated_at']
        assert result.is_deleted == test_data['is_deleted']
        assert result.deleted_at == test_data['deleted_at']

    def test_bot_metadata_schema_invalid_fields(self):
        """Test bot metadata schema validation with invalid fields."""
        # Create test data with invalid fields
        test_data = {
            'bot_id': 'test-bot-1',
            'title': 'Test Bot',
            'description': 'A test bot',
            'instruction_hash': 'abc123',
            'owner_user_id': 'user-1',
            'is_public': True,
            'group_id': 'group-1',
            'create_time': 1234567890.0,
            'last_used_time': 1234567890.0,
            'hierarchy': [
                {
                    'id': 'school-1',
                    'name': 'Test School',
                    'level': 'invalid_level',  # Invalid level
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

        # Create schema instance
        schema = BotMetadataSchema()

        # Validate data and expect validation error
        with pytest.raises(ValidationError) as exc_info:
            schema.load(test_data)

        # Verify error message
        assert 'Invalid hierarchy level' in str(exc_info.value)

    def test_metadata_config_schema(self):
        """Test the MetadataConfig schema validation."""
        # Test initialization with defaults
        config_default = MetadataConfig()
        self.assertEqual(config_default.allowed_hierarchy_levels, [])
        self.assertEqual(config_default.allowed_tag_categories, [])
        self.assertEqual(config_default.required_attributes, [])
        
        # Test initialization with values
        config = MetadataConfig(
            allowed_hierarchy_levels=["district", "school", "department"],
            allowed_tag_categories=["subject", "grade_level"],
            required_attributes=["language", "target_age"]
        )
        
        self.assertEqual(config.allowed_hierarchy_levels, ["district", "school", "department"])
        self.assertEqual(config.allowed_tag_categories, ["subject", "grade_level"])
        self.assertEqual(config.required_attributes, ["language", "target_age"])
        
        # Test schema validation
        config_dict = config.model_dump()
        self.assertIn("allowed_hierarchy_levels", config_dict)
        self.assertIn("allowed_tag_categories", config_dict)
        self.assertIn("required_attributes", config_dict)
        
    def test_search_query_schema(self):
        """Test the SearchQuery schema validation."""
        # Test empty query
        empty_query = SearchQuery()
        self.assertEqual(empty_query.hierarchy, {})
        self.assertEqual(empty_query.tags, {})
        self.assertEqual(empty_query.attributes, {})
        
        # Test query with values
        query = SearchQuery(
            hierarchy={"level": "school", "id": "school-1"},
            tags={"category": "subject", "id": "subject-1"},
            attributes={"key": "language", "value": "en"}
        )
        
        self.assertEqual(query.hierarchy, {"level": "school", "id": "school-1"})
        self.assertEqual(query.tags, {"category": "subject", "id": "subject-1"})
        self.assertEqual(query.attributes, {"key": "language", "value": "en"})
        
        # Test schema validation
        query_dict = query.model_dump()
        self.assertIn("hierarchy", query_dict)
        self.assertIn("tags", query_dict)
        self.assertIn("attributes", query_dict)


if __name__ == "__main__":
    unittest.main() 