from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")

class MetadataValue(BaseModel):
    """Base class for metadata values with common fields"""
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class HierarchyMetadata(MetadataValue):
    """Represents a hierarchical metadata value like school, district, department"""
    parent_id: Optional[str] = None
    level: str  # e.g. "district", "school", "department"
    path: List[str] = Field(default_factory=list)  # Full path from root, e.g. ["SDCC", "Math Department"]

class TagMetadata(MetadataValue):
    """Represents a tag that can be applied to bots"""
    category: str  # e.g. "subject", "grade_level", "difficulty"
    
class AttributeMetadata(MetadataValue):
    """Represents a key-value attribute for bots"""
    key: str  # e.g. "language", "target_age"
    value: Union[str, int, float, bool]
    data_type: str = "string"  # one of: string, number, boolean

class MetadataConfig(BaseModel):
    """Configuration for metadata validation"""
    allowed_hierarchy_levels: List[str]  # e.g. ["district", "school", "department"]
    allowed_tag_categories: List[str]  # e.g. ["subject", "grade_level"]
    required_attributes: List[str]  # e.g. ["language", "target_age"]
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "allowed_hierarchy_levels": ["district", "school", "department"],
                "allowed_tag_categories": ["subject", "grade_level", "difficulty"],
                "required_attributes": ["owner", "assistant_type"]
            }
        }
    )

class BotMetadata(BaseModel):
    """Complete metadata for a bot"""
    bot_id: str
    title: str
    description: str
    instruction_hash: str
    owner_user_id: str
    is_public: bool
    group_id: Optional[str] = None
    create_time: float
    last_used_time: float
    hierarchy: List[HierarchyMetadata] = Field(default_factory=list)
    tags: List[TagMetadata] = Field(default_factory=list)
    attributes: List[AttributeMetadata] = Field(default_factory=list)
    updated_at: Optional[str] = None
    is_deleted: bool = False
    deleted_at: Optional[str] = None

    def add_hierarchy(self, hierarchy: HierarchyMetadata):
        self.hierarchy.append(hierarchy)
        
    def add_tag(self, tag: TagMetadata):
        self.tags.append(tag)
        
    def add_attribute(self, attribute: AttributeMetadata):
        self.attributes.append(attribute)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "bot_id": "bot-123",
                "title": "Math Tutor Bot",
                "description": "A bot that helps with math problems",
                "instruction_hash": "abc123",
                "owner_user_id": "user-456",
                "is_public": True,
                "group_id": "group-789",
                "create_time": 1234567890.0,
                "last_used_time": 1234567890.0,
                "hierarchy": [{
                    "id": "sdcc-math",
                    "name": "SDCC Math Department",
                    "level": "department",
                    "parent_id": "sdcc",
                    "path": ["SDCC", "Math Department"]
                }],
                "tags": [{
                    "id": "calculus",
                    "name": "Calculus",
                    "category": "subject"
                }],
                "attributes": [{
                    "id": "lang-en",
                    "name": "English",
                    "key": "language",
                    "value": "en"
                }],
                "updated_at": "2024-03-20T12:00:00Z",
                "is_deleted": False,
                "deleted_at": None
            }
        }
    ) 