from typing import List, Optional, Dict
from ..repositories.models.bot_metadata import BotMetadata, MetadataConfig, HierarchyMetadata

class ValidationError(Exception):
    """Custom exception for metadata validation errors"""
    pass

class MetadataValidator:
    def __init__(self, config: MetadataConfig):
        self.config = config
        
    async def validate(self, metadata: BotMetadata) -> bool:
        """
        Validates the complete metadata against configuration rules
        Returns True if valid, raises ValidationError if invalid
        """
        await self._validate_hierarchy(metadata.hierarchy)
        await self._validate_tags(metadata.tags)
        await self._validate_attributes(metadata.attributes)
        return True
        
    async def _validate_hierarchy(self, hierarchy: List[HierarchyMetadata]):
        """Validates hierarchy metadata"""
        # Check if hierarchy levels are allowed
        for item in hierarchy:
            if item.level not in self.config.allowed_hierarchy_levels:
                raise ValidationError(f"Invalid hierarchy level: {item.level}")
                
            # Validate parent-child relationships
            if item.parent_id:
                parent = next((h for h in hierarchy if h.id == item.parent_id), None)
                if not parent:
                    raise ValidationError(f"Parent not found: {item.parent_id}")
                    
                # Validate level ordering
                parent_level_idx = self.config.allowed_hierarchy_levels.index(parent.level)
                item_level_idx = self.config.allowed_hierarchy_levels.index(item.level)
                if item_level_idx <= parent_level_idx:
                    raise ValidationError(f"Invalid hierarchy: {item.level} cannot be child of {parent.level}")
                    
            # Validate path
            if not item.path:
                raise ValidationError(f"Path is required for hierarchy item: {item.id}")
                
    async def _validate_tags(self, tags):
        """Validates tag metadata"""
        # Check if tag categories are allowed
        for tag in tags:
            if tag.category not in self.config.allowed_tag_categories:
                raise ValidationError(f"Invalid tag category: {tag.category}")
                
    async def _validate_attributes(self, attributes):
        """Validates attribute metadata"""
        # Check if all required attributes are present
        attribute_keys = {attr.key for attr in attributes}
        missing_attrs = set(self.config.required_attributes) - attribute_keys
        if missing_attrs:
            raise ValidationError(f"Missing required attributes: {missing_attrs}")
            
        # Validate data types
        for attr in attributes:
            if attr.data_type not in ["string", "number", "boolean"]:
                raise ValidationError(f"Invalid data type for attribute {attr.key}: {attr.data_type}")
                
            # Type checking
            if attr.data_type == "number" and not isinstance(attr.value, (int, float)):
                raise ValidationError(f"Invalid value type for attribute {attr.key}: expected number")
            elif attr.data_type == "boolean" and not isinstance(attr.value, bool):
                raise ValidationError(f"Invalid value type for attribute {attr.key}: expected boolean") 