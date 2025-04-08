import sys
import unittest
from datetime import datetime, UTC
import pytest
from pydantic import ValidationError

from backend.app.repositories.models.bot_metadata import (
    BotMetadata,
    HierarchyMetadata,
    TagMetadata,
    AttributeMetadata,
    MetadataConfig,
    MetadataValue
)


class TestMetadataModels(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.test_bot_id = "test-bot-1"
        self.test_metadata = BotMetadata(
            bot_id=self.test_bot_id,
            title="Test Bot",
            description="A test bot",
            instruction_hash="abc123",
            owner_user_id="user-1",
            is_public=True,
            group_id="group-1",
            create_time=1234567890.0,
            last_used_time=1234567890.0,
            hierarchy=[],
            tags=[],
            attributes=[],
            updated_at=datetime.now(UTC).isoformat(),
            is_deleted=False,
            deleted_at=None
        )

    def test_metadata_value_base_class(self):
        """Test the MetadataValue base class."""
        metadata_value = MetadataValue(
            id="test-id",
            name="Test Value"
        )
        
        self.assertEqual(metadata_value.id, "test-id")
        self.assertEqual(metadata_value.name, "Test Value")
        self.assertIsNone(metadata_value.description)
        self.assertIsInstance(metadata_value.created_at, datetime)
        self.assertIsInstance(metadata_value.updated_at, datetime)
        
    def test_hierarchy_metadata(self):
        """Test the HierarchyMetadata class."""
        hierarchy = HierarchyMetadata(
            id="dept-math",
            name="Math Department",
            level="department",
            parent_id="school-1",
            path=["School 1", "Math Department"]
        )
        
        self.assertEqual(hierarchy.id, "dept-math")
        self.assertEqual(hierarchy.name, "Math Department")
        self.assertEqual(hierarchy.level, "department")
        self.assertEqual(hierarchy.parent_id, "school-1")
        self.assertEqual(hierarchy.path, ["School 1", "Math Department"])
        
    def test_tag_metadata(self):
        """Test the TagMetadata class."""
        tag = TagMetadata(
            id="tag-calculus",
            name="Calculus",
            category="subject"
        )
        
        self.assertEqual(tag.id, "tag-calculus")
        self.assertEqual(tag.name, "Calculus")
        self.assertEqual(tag.category, "subject")
        
    def test_attribute_metadata(self):
        """Test the AttributeMetadata class."""
        # String attribute
        string_attr = AttributeMetadata(
            id="attr-lang",
            name="Language",
            key="language",
            value="en",
            data_type="string"
        )
        
        self.assertEqual(string_attr.id, "attr-lang")
        self.assertEqual(string_attr.key, "language")
        self.assertEqual(string_attr.value, "en")
        self.assertEqual(string_attr.data_type, "string")
        
        # Number attribute
        num_attr = AttributeMetadata(
            id="attr-age",
            name="Target Age",
            key="target_age",
            value=18,
            data_type="number"
        )
        
        self.assertEqual(num_attr.key, "target_age")
        self.assertEqual(num_attr.value, 18)
        self.assertEqual(num_attr.data_type, "number")
        
        # Boolean attribute
        bool_attr = AttributeMetadata(
            id="attr-active",
            name="Is Active",
            key="is_active",
            value=True,
            data_type="boolean"
        )
        
        self.assertEqual(bool_attr.key, "is_active")
        self.assertEqual(bool_attr.value, True)
        self.assertEqual(bool_attr.data_type, "boolean")
        
    def test_metadata_config(self):
        """Test the MetadataConfig class."""
        config = MetadataConfig(
            allowed_hierarchy_levels=["district", "school", "department"],
            allowed_tag_categories=["subject", "grade_level"],
            required_attributes=["language"]
        )
        
        self.assertEqual(config.allowed_hierarchy_levels, ["district", "school", "department"])
        self.assertEqual(config.allowed_tag_categories, ["subject", "grade_level"])
        self.assertEqual(config.required_attributes, ["language"])
        
    def test_bot_metadata(self):
        """Test the BotMetadata class."""
        # Test initialization with required fields
        metadata = BotMetadata(
            bot_id=self.test_bot_id,
            title="Test Bot",
            description="A test bot",
            instruction_hash="abc123",
            owner_user_id="user-1",
            is_public=True,
            group_id="group-1",
            create_time=1234567890.0,
            last_used_time=1234567890.0,
            hierarchy=[],
            tags=[],
            attributes=[],
            updated_at=datetime.now(UTC).isoformat(),
            is_deleted=False,
            deleted_at=None
        )
        
        self.assertEqual(metadata.bot_id, self.test_bot_id)
        self.assertEqual(metadata.title, "Test Bot")
        self.assertEqual(metadata.description, "A test bot")
        self.assertEqual(len(metadata.hierarchy), 0)
        self.assertEqual(len(metadata.tags), 0)
        self.assertEqual(len(metadata.attributes), 0)
        
    def test_bot_metadata_helper_methods(self):
        """Test the helper methods on BotMetadata."""
        metadata = self.test_metadata
        
        # Test add_hierarchy
        hierarchy = HierarchyMetadata(
            id="dept-math",
            name="Math Department",
            level="department",
            parent_id=None,
            path=["Math Department"]
        )
        metadata.add_hierarchy(hierarchy)
        self.assertEqual(len(metadata.hierarchy), 1)
        
        # Test add_tag
        tag = TagMetadata(
            id="tag-calculus",
            name="Calculus",
            category="subject"
        )
        metadata.add_tag(tag)
        self.assertEqual(len(metadata.tags), 1)
        
        # Test add_attribute
        attribute = AttributeMetadata(
            id="attr-lang",
            name="Language",
            key="language",
            value="en",
            data_type="string"
        )
        metadata.add_attribute(attribute)
        self.assertEqual(len(metadata.attributes), 1)

    def test_bot_metadata_creation(self):
        """Test creating a BotMetadata instance with all fields."""
        metadata = BotMetadata(
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
                HierarchyMetadata(
                    id="school-1",
                    name="Test School",
                    level="school",
                    path=["Test School"]
                )
            ],
            tags=[
                TagMetadata(
                    id="tag-1",
                    name="Test Tag",
                    category="test",
                    value="test"
                )
            ],
            attributes=[
                AttributeMetadata(
                    id="attr-1",
                    name="Test Attribute",
                    key="test_key",
                    value="test_value"
                )
            ],
            updated_at=datetime.now(UTC).isoformat(),
            is_deleted=False,
            deleted_at=None
        )

        self.assertEqual(metadata.bot_id, "test-bot-1")
        self.assertEqual(metadata.title, "Test Bot")
        self.assertEqual(metadata.description, "A test bot")
        self.assertEqual(metadata.instruction_hash, "abc123")
        self.assertEqual(metadata.owner_user_id, "user-1")
        self.assertEqual(metadata.is_public, True)
        self.assertEqual(metadata.group_id, "group-1")
        self.assertEqual(metadata.create_time, 1234567890.0)
        self.assertEqual(metadata.last_used_time, 1234567890.0)
        self.assertEqual(len(metadata.hierarchy), 1)
        self.assertEqual(len(metadata.tags), 1)
        self.assertEqual(len(metadata.attributes), 1)
        self.assertIsNotNone(metadata.updated_at)
        self.assertEqual(metadata.is_deleted, False)
        self.assertEqual(metadata.deleted_at, None)

    def test_bot_metadata_default_values(self):
        """Test creating a BotMetadata instance with default values."""
        metadata = BotMetadata(
            bot_id="test-bot-2",
            title="Test Bot 2",
            description="Another test bot",
            instruction_hash="def456",
            owner_user_id="user-2",
            is_public=False,
            group_id=None,
            create_time=1234567890.0,
            last_used_time=1234567890.0,
            updated_at=datetime.now(UTC).isoformat()
        )

        self.assertEqual(metadata.bot_id, "test-bot-2")
        self.assertEqual(metadata.title, "Test Bot 2")
        self.assertEqual(metadata.description, "Another test bot")
        self.assertEqual(metadata.instruction_hash, "def456")
        self.assertEqual(metadata.owner_user_id, "user-2")
        self.assertEqual(metadata.is_public, False)
        self.assertEqual(metadata.group_id, None)
        self.assertEqual(metadata.create_time, 1234567890.0)
        self.assertEqual(metadata.last_used_time, 1234567890.0)
        self.assertEqual(len(metadata.hierarchy), 0)
        self.assertEqual(len(metadata.tags), 0)
        self.assertEqual(len(metadata.attributes), 0)
        self.assertIsNotNone(metadata.updated_at)
        self.assertEqual(metadata.is_deleted, False)
        self.assertEqual(metadata.deleted_at, None)

    def test_bot_metadata_validation(self):
        """Test validation of required fields."""
        with self.assertRaises(ValidationError):
            BotMetadata()  # Should fail without required fields

        with self.assertRaises(ValidationError):
            BotMetadata(
                bot_id="test-bot-3",
                title="Test Bot 3",
                description="Test bot 3",
                instruction_hash="ghi789",
                owner_user_id="user-3",
                is_public=True,
                group_id="group-3",
                create_time="invalid",  # Should be float
                last_used_time=1234567890.0
            )


if __name__ == "__main__":
    unittest.main() 