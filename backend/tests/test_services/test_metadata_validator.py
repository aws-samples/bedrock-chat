import sys
import unittest
from unittest.mock import MagicMock, patch

from backend.app.repositories.models.bot_metadata import BotMetadata, MetadataConfig, HierarchyMetadata, TagMetadata, AttributeMetadata
from app.services.metadata_validator import MetadataValidator, ValidationError


class TestMetadataValidator(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a test config
        self.config = MetadataConfig(
            allowed_hierarchy_levels=["district", "school", "department"],
            allowed_tag_categories=["subject", "grade_level", "difficulty"],
            required_attributes=["language", "target_age"]
        )
        
        # Create a validator with the test config
        self.validator = MetadataValidator(config=self.config)
        
        # Create a valid metadata object for testing
        self.valid_metadata = BotMetadata(
            hierarchy=[
                HierarchyMetadata(
                    id="district-1",
                    name="Test District",
                    level="district",
                    parent_id=None,
                    path=["Test District"]
                ),
                HierarchyMetadata(
                    id="school-1",
                    name="Test School",
                    level="school",
                    parent_id="district-1",
                    path=["Test District", "Test School"]
                )
            ],
            tags=[
                TagMetadata(
                    id="subject-math",
                    name="Math",
                    category="subject"
                ),
                TagMetadata(
                    id="grade-high",
                    name="High School",
                    category="grade_level"
                )
            ],
            attributes=[
                AttributeMetadata(
                    id="attr-lang",
                    name="Language",
                    key="language",
                    value="en",
                    data_type="string"
                ),
                AttributeMetadata(
                    id="attr-age",
                    name="Target Age",
                    key="target_age",
                    value=16,
                    data_type="number"
                )
            ]
        )
        
    async def test_validate_valid_metadata(self):
        """Test validation with valid metadata."""
        # This should not raise any exceptions
        result = await self.validator.validate(self.valid_metadata)
        self.assertTrue(result)
        
    async def test_validate_invalid_hierarchy_level(self):
        """Test validation with invalid hierarchy level."""
        # Create invalid metadata with an invalid hierarchy level
        invalid_metadata = BotMetadata(
            hierarchy=[
                HierarchyMetadata(
                    id="invalid-1",
                    name="Invalid Level",
                    level="invalid_level",  # This level is not in allowed_hierarchy_levels
                    parent_id=None,
                    path=["Invalid Level"]
                )
            ],
            tags=self.valid_metadata.tags,
            attributes=self.valid_metadata.attributes
        )
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(invalid_metadata)
        
        self.assertIn("Invalid hierarchy level", str(context.exception))
        
    async def test_validate_invalid_parent_child_relationship(self):
        """Test validation with invalid parent-child relationship in hierarchy."""
        # Create invalid metadata with a department as parent of a school
        invalid_metadata = BotMetadata(
            hierarchy=[
                HierarchyMetadata(
                    id="department-1",
                    name="Math Department",
                    level="department",
                    parent_id=None,
                    path=["Math Department"]
                ),
                HierarchyMetadata(
                    id="school-1",
                    name="Test School",
                    level="school",
                    parent_id="department-1",  # School cannot be child of department
                    path=["Math Department", "Test School"]
                )
            ],
            tags=self.valid_metadata.tags,
            attributes=self.valid_metadata.attributes
        )
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(invalid_metadata)
        
        self.assertIn("Invalid hierarchy", str(context.exception))
        
    async def test_validate_missing_parent(self):
        """Test validation with a missing parent in hierarchy."""
        # Create invalid metadata with a reference to a non-existent parent
        invalid_metadata = BotMetadata(
            hierarchy=[
                HierarchyMetadata(
                    id="school-1",
                    name="Test School",
                    level="school",
                    parent_id="nonexistent-parent",  # This parent doesn't exist
                    path=["Missing", "Test School"]
                )
            ],
            tags=self.valid_metadata.tags,
            attributes=self.valid_metadata.attributes
        )
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(invalid_metadata)
        
        self.assertIn("Parent not found", str(context.exception))
        
    async def test_validate_missing_path(self):
        """Test validation with a missing path in hierarchy."""
        # Create invalid metadata with a missing path
        invalid_metadata = BotMetadata(
            hierarchy=[
                HierarchyMetadata(
                    id="district-1",
                    name="Test District",
                    level="district",
                    parent_id=None,
                    path=[]  # Empty path is invalid
                )
            ],
            tags=self.valid_metadata.tags,
            attributes=self.valid_metadata.attributes
        )
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(invalid_metadata)
        
        self.assertIn("Path is required", str(context.exception))
        
    async def test_validate_invalid_tag_category(self):
        """Test validation with invalid tag category."""
        # Create invalid metadata with an invalid tag category
        invalid_metadata = BotMetadata(
            hierarchy=self.valid_metadata.hierarchy,
            tags=[
                TagMetadata(
                    id="invalid-tag",
                    name="Invalid Tag",
                    category="invalid_category"  # This category is not in allowed_tag_categories
                )
            ],
            attributes=self.valid_metadata.attributes
        )
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(invalid_metadata)
        
        self.assertIn("Invalid tag category", str(context.exception))
        
    async def test_validate_missing_required_attribute(self):
        """Test validation with missing required attribute."""
        # Create invalid metadata with missing required attribute
        invalid_metadata = BotMetadata(
            hierarchy=self.valid_metadata.hierarchy,
            tags=self.valid_metadata.tags,
            attributes=[
                # Missing 'target_age' attribute which is required
                AttributeMetadata(
                    id="attr-lang",
                    name="Language",
                    key="language",
                    value="en",
                    data_type="string"
                )
            ]
        )
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(invalid_metadata)
        
        self.assertIn("Missing required attributes", str(context.exception))
        
    async def test_validate_invalid_attribute_data_type(self):
        """Test validation with invalid attribute data type."""
        # Create invalid metadata with an invalid attribute data type
        invalid_metadata = BotMetadata(
            hierarchy=self.valid_metadata.hierarchy,
            tags=self.valid_metadata.tags,
            attributes=[
                AttributeMetadata(
                    id="attr-lang",
                    name="Language",
                    key="language",
                    value="en",
                    data_type="string"
                ),
                AttributeMetadata(
                    id="attr-age",
                    name="Target Age",
                    key="target_age",
                    value=16,
                    data_type="invalid_type"  # This data type is not allowed
                )
            ]
        )
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(invalid_metadata)
        
        self.assertIn("Invalid data type", str(context.exception))
        
    async def test_validate_type_mismatch(self):
        """Test validation with type mismatch in attribute value."""
        # Create invalid metadata with a type mismatch
        invalid_metadata = BotMetadata(
            hierarchy=self.valid_metadata.hierarchy,
            tags=self.valid_metadata.tags,
            attributes=[
                AttributeMetadata(
                    id="attr-lang",
                    name="Language",
                    key="language",
                    value="en",
                    data_type="string"
                ),
                AttributeMetadata(
                    id="attr-age",
                    name="Target Age",
                    key="target_age",
                    value="sixteen",  # String value for number type
                    data_type="number"
                )
            ]
        )
        
        # This should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            await self.validator.validate(invalid_metadata)
        
        self.assertIn("Invalid value type", str(context.exception))

    def test_validate_bot_metadata(self):
        """Test validating bot metadata."""
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

        # Call the method
        result = self.validator.validate_bot_metadata(test_metadata)

        # Verify the result
        assert result is True

    def test_validate_bot_metadata_missing_required_fields(self):
        """Test validating bot metadata with missing required fields."""
        # Create test metadata with missing required fields
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
            hierarchy=[],
            tags=[],
            attributes=[],
            updated_at='2024-03-20T12:00:00Z',
            is_deleted=False,
            deleted_at=None
        )

        # Call the method
        result = self.validator.validate_bot_metadata(test_metadata)

        # Verify the result
        assert result is True  # All required fields are present

    def test_validate_bot_metadata_invalid_fields(self):
        """Test validating bot metadata with invalid fields."""
        # Create test metadata with invalid fields
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
                    'level': 'invalid_level',  # Invalid level
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

        # Call the method
        result = self.validator.validate_bot_metadata(test_metadata)

        # Verify the result
        assert result is False  # Invalid hierarchy level


if __name__ == "__main__":
    unittest.main() 