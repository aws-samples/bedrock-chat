# Metadata System

## Overview

The Metadata System is a flexible, extensible framework for organizing and categorizing bots/assistants in the Bedrock Claude Chat platform. This system supports multiple organizational models (education, enterprise, healthcare, etc.) through a three-tiered approach that combines hierarchical structures, tags, and attributes.

## Core Concepts

The Metadata System consists of three primary components:

1. **Hierarchy**: Organizational structure like district → school → department
2. **Tags**: Categorical labels like subject, difficulty level, or purpose
3. **Attributes**: Key-value pairs for specific characteristics

## Architecture

### 1. Data Models

The system uses a set of carefully designed Pydantic models:

```python
# Base class for all metadata values
class MetadataValue(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Hierarchical structure model
class HierarchyMetadata(MetadataValue):
    parent_id: Optional[str] = None
    level: str  # e.g. "district", "school", "department"
    path: List[str]  # Full path from root, e.g. ["SDCC", "Math Department"]

# Tag categorization model
class TagMetadata(MetadataValue):
    category: str  # e.g. "subject", "grade_level", "difficulty"
    
# Key-value attribute model
class AttributeMetadata(MetadataValue):
    key: str  # e.g. "language", "target_age"
    value: Union[str, int, float, bool]
    data_type: str = "string"  # one of: string, number, boolean

# Container for all metadata
class BotMetadata(BaseModel):
    hierarchy: List[HierarchyMetadata] = Field(default_factory=list)
    tags: List[TagMetadata] = Field(default_factory=list)
    attributes: List[AttributeMetadata] = Field(default_factory=list)

# Configuration for validation
class MetadataConfig(BaseModel):
    allowed_hierarchy_levels: List[str]
    allowed_tag_categories: List[str]
    required_attributes: List[str]
```

### 2. Storage Layer

The system uses three DynamoDB tables for metadata storage:

1. **metadata_config**: Configuration for metadata validation
   - Primary key: `id` (default)
   - Stores validation rules for hierarchies, tags, and attributes

2. **metadata_values**: Predefined metadata values
   - Partition key: `type` (hierarchy, tag)
   - Sort key: `id`
   - Stores reusable metadata values

3. **bot_metadata**: Bot-specific metadata
   - Primary key: `bot_id`
   - Stores bot-specific metadata collections

Global Secondary Indexes (GSIs) for efficient querying:
- `HierarchyIndex`: Query by hierarchy level and ID
- `TagCategoryIndex`: Query by tag category
- `AttributeKeyIndex`: Query by attribute key

### 3. Service Layer

The system includes a comprehensive service layer for metadata operations:

```python
class MetadataValidator:
    # Validates metadata against configuration rules
    async def validate(self, metadata: BotMetadata) -> bool
    async def _validate_hierarchy(self, hierarchy: List[HierarchyMetadata])
    async def _validate_tags(self, tags: List[TagMetadata])
    async def _validate_attributes(self, attributes: List[AttributeMetadata])

class MetadataService:
    # Core service methods
    async def get_config(self) -> MetadataConfig
    async def update_config(self, config: MetadataConfig)
    async def get_bot_metadata(self, bot_id: str) -> BotMetadata
    async def update_bot_metadata(self, bot_id: str, metadata: BotMetadata)
    
    # Metadata values management
    async def get_hierarchy_values(self) -> List[Dict]
    async def get_tag_values(self) -> List[Dict]
    async def add_hierarchy_value(self, value: Dict)
    async def add_tag_value(self, value: Dict)
    async def delete_hierarchy_value(self, value_id: str)
    async def delete_tag_value(self, value_id: str)
    
    # Search and analytics
    async def search_bots(self, query: Dict) -> List[str]
    async def get_metadata_stats(self) -> Dict
```

### 4. API Layer

The system exposes the following REST API endpoints:

```python
# Configuration management
@router.get("/metadata/config")            # Get metadata configuration
@router.post("/metadata/config")           # Update metadata configuration

# Bot metadata management
@router.get("/metadata/bot/{bot_id}")      # Get bot metadata
@router.post("/metadata/bot/{bot_id}")     # Update bot metadata

# Metadata values management
@router.get("/metadata/values/hierarchy")  # Get hierarchy values
@router.get("/metadata/values/tags")       # Get tag values
@router.post("/metadata/values/hierarchy") # Add a hierarchy value
@router.post("/metadata/values/tags")      # Add a tag value
@router.delete("/metadata/values/hierarchy/{value_id}") # Delete hierarchy value
@router.delete("/metadata/values/tags/{value_id}")      # Delete tag value

# Search and analytics
@router.post("/metadata/search")           # Search bots by metadata
@router.get("/metadata/stats")             # Get metadata statistics
```

### 5. Analytics Integration

The system integrates with the analytics pipeline through Athena views:

- `hierarchy_metadata_view`: View for hierarchy metadata
- `tag_metadata_view`: View for tag metadata
- `attribute_metadata_view`: View for attribute metadata
- `metadata_analytics_view`: Combined view for metadata statistics

## Use Cases

### Education Vertical

For educational institutions with hierarchical structure:

```python
# Example for a math tutoring bot in a school district
metadata = BotMetadata()

# Add hierarchy
metadata.add_hierarchy(HierarchyMetadata(
    id="sdcc",
    name="San Diego Community College",
    level="district",
    path=["SDCC"]
))

metadata.add_hierarchy(HierarchyMetadata(
    id="math-dept",
    name="Math Department",
    level="department",
    parent_id="sdcc",
    path=["SDCC", "Math Department"]
))

# Add tags
metadata.add_tag(TagMetadata(
    id="calculus",
    name="Calculus",
    category="subject"
))

metadata.add_tag(TagMetadata(
    id="college",
    name="College",
    category="grade_level"
))

# Add attributes
metadata.add_attribute(AttributeMetadata(
    id="lang-en",
    name="English",
    key="language",
    value="en"
))

metadata.add_attribute(AttributeMetadata(
    id="age-18-22",
    name="College Age",
    key="target_age",
    value="18-22"
))
```

### Enterprise Vertical

For corporate environments with different organizational structures:

```python
# Example for a sales training bot in a corporation
metadata = BotMetadata()

# Add hierarchy
metadata.add_hierarchy(HierarchyMetadata(
    id="acme-corp",
    name="ACME Corporation",
    level="company",
    path=["ACME"]
))

metadata.add_hierarchy(HierarchyMetadata(
    id="sales-div",
    name="Sales Division",
    level="division",
    parent_id="acme-corp",
    path=["ACME", "Sales Division"]
))

# Add tags
metadata.add_tag(TagMetadata(
    id="sales-training",
    name="Sales Training",
    category="function"
))

metadata.add_tag(TagMetadata(
    id="beginner",
    name="Beginner",
    category="difficulty"
))

# Add attributes
metadata.add_attribute(AttributeMetadata(
    id="role-sales-rep",
    name="Sales Representative",
    key="target_role",
    value="sales_rep"
))
```

## Implementation Details

### Bot Model Integration

The Metadata System integrates with the existing BotModel:

```python
class BotModel(BaseModel):
    # Existing fields...
    metadata: BotMetadata = Field(default_factory=BotMetadata)
    
    # Helper methods
    def get_hierarchy(self, level: str) -> List[HierarchyMetadata]:
        """Get hierarchical metadata of a specific level"""
        return [h for h in self.metadata.hierarchy if h.level == level]
    
    def get_tags(self, category: Optional[str] = None) -> List[TagMetadata]:
        """Get all tags, optionally filtered by category"""
        if category:
            return [t for t in self.metadata.tags if t.category == category]
        return self.metadata.tags
    
    def get_attributes(self) -> List[AttributeMetadata]:
        """Get all attributes"""
        return self.metadata.attributes
        
    def get_attribute_value(self, key: str) -> Any:
        """Get the value of a specific attribute"""
        for attr in self.metadata.attributes:
            if attr.key == key:
                return attr.value
        return None
```

### Validation Rules

The system enforces the following validation rules:

1. Hierarchy levels must be in the allowed list
2. Parent-child relationships must follow the hierarchy level order
3. Tag categories must be in the allowed list
4. Required attributes must be present
5. Attribute values must match the specified data type

### DynamoDB Repository Pattern

The system follows the established pattern for DynamoDB operations:

```python
async def get_bot_metadata(self, bot_id: str) -> BotMetadata:
    """Retrieves metadata for a specific bot"""
    loop = asyncio.get_running_loop()
    
    def get_metadata_item(bot_id):
        return self.bot_metadata_table.get_item(Key={'bot_id': bot_id})
        
    response = await loop.run_in_executor(None, partial(get_metadata_item, bot_id))
    
    if 'Item' not in response:
        return BotMetadata()
        
    item = response['Item']
    return BotMetadata(
        hierarchy=[HierarchyMetadata(**h) for h in item.get('hierarchy', [])],
        tags=[TagMetadata(**t) for t in item.get('tags', [])],
        attributes=[AttributeMetadata(**a) for a in item.get('attributes', [])]
    )
```

### Environment Variables

The system uses environment variables with fallbacks:

```python
# Table names from environment variables with fallbacks
METADATA_CONFIG_TABLE = os.environ.get("METADATA_CONFIG_TABLE", "metadata_config")
METADATA_VALUES_TABLE = os.environ.get("METADATA_VALUES_TABLE", "metadata_values")
BOT_METADATA_TABLE = os.environ.get("BOT_METADATA_TABLE", "bot_metadata")
```

### Initialization

The system includes a migration script for initializing default metadata values:

```python
async def initialize_metadata_config():
    """Initialize metadata configuration with default values"""
    # Default configuration for validation
    default_config = {
        "id": "default",
        "allowed_hierarchy_levels": ["district", "school", "department"],
        "allowed_tag_categories": ["subject", "grade_level", "difficulty"],
        "required_attributes": ["language", "target_age"]
    }
    
async def initialize_hierarchy_values():
    """Initialize hierarchy values with default examples"""
    # Example hierarchy values for education
    
async def initialize_tag_values():
    """Initialize tag values with default examples"""
    # Example tag values by category
```

## Analytics Capabilities

The Metadata System enables the following analytics capabilities:

1. **Hierarchical Analytics**: Analyze usage across organizational hierarchies
   - Usage by district/school/department
   - Comparison across organizational units
   - Hierarchy traversal analytics

2. **Tag Analytics**: Analyze usage by tag categories
   - Subject popularity
   - Difficulty level distribution
   - Function/purpose analysis

3. **Attribute Analytics**: Analyze usage by specific attributes
   - Language distribution
   - Target age/role patterns
   - Other attribute-specific metrics

4. **Combined Analytics**: Analyze across multiple dimensions
   - Hierarchical breakdown by subject
   - Subject popularity by age group
   - Cross-dimensional correlations

## CDK Integration

The system is integrated with the AWS CDK infrastructure:

```typescript
// Metadata config table
const metadataConfigTable = new Table(this, "MetadataConfigTable", {
  tableName: "metadata_config",
  partitionKey: { name: "id", type: AttributeType.STRING },
  billingMode: BillingMode.PAY_PER_REQUEST,
  removalPolicy: RemovalPolicy.DESTROY,
  encryption: TableEncryption.AWS_MANAGED,
  pointInTimeRecovery: props?.pointInTimeRecovery,
});

// Metadata values table
const metadataValuesTable = new Table(this, "MetadataValuesTable", {
  tableName: "metadata_values",
  partitionKey: { name: "type", type: AttributeType.STRING },
  sortKey: { name: "id", type: AttributeType.STRING },
  billingMode: BillingMode.PAY_PER_REQUEST,
  removalPolicy: RemovalPolicy.DESTROY,
  encryption: TableEncryption.AWS_MANAGED,
  pointInTimeRecovery: props?.pointInTimeRecovery,
});

// Bot metadata table
const botMetadataTable = new Table(this, "BotMetadataTable", {
  tableName: "bot_metadata",
  partitionKey: { name: "bot_id", type: AttributeType.STRING },
  billingMode: BillingMode.PAY_PER_REQUEST,
  removalPolicy: RemovalPolicy.DESTROY,
  encryption: TableEncryption.AWS_MANAGED,
  pointInTimeRecovery: props?.pointInTimeRecovery,
});

// Add GSIs for searching by metadata
botMetadataTable.addGlobalSecondaryIndex({
  indexName: "HierarchyIndex",
  partitionKey: { name: "hierarchy_level", type: AttributeType.STRING },
  sortKey: { name: "hierarchy_id", type: AttributeType.STRING },
});

botMetadataTable.addGlobalSecondaryIndex({
  indexName: "TagCategoryIndex",
  partitionKey: { name: "tag_category", type: AttributeType.STRING },
});

botMetadataTable.addGlobalSecondaryIndex({
  indexName: "AttributeKeyIndex",
  partitionKey: { name: "attribute_key", type: AttributeType.STRING },
});
```

## Future Enhancements

1. **Metadata Templates**: Create predefined templates for common use cases
2. **Bulk Import/Export**: Add capabilities for bulk metadata operations
3. **Advanced Search**: Enhance search with logical operators (AND, OR, NOT)
4. **Visualization**: Add graphical visualization of hierarchical relationships
5. **Auto-suggestions**: Implement AI-powered metadata suggestions based on bot content
6. **Inheritance**: Support for metadata inheritance across organizational levels
7. **Access Control**: Granular access control based on metadata properties 