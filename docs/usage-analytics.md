# Usage Analytics

## Overview

The Usage Analytics system provides comprehensive tracking, analysis, and visualization of user interactions with the Bedrock Claude Chat platform. This system enables administrators to understand usage patterns, optimize costs, and make data-driven decisions about bot deployment and configuration.

## Architecture

The Usage Analytics system consists of several integrated components:

### 1. Data Collection Layer

- **DynamoDB Stream**: Captures all changes to the conversation table
- **Token Tracking**: Records input and output tokens for all model interactions
- **Cost Calculation**: Computes usage costs based on model-specific pricing
- **Metadata Integration**: Associates usage with metadata for dimensional analysis

### 2. Data Storage Layer

- **S3 Export**: DynamoDB streams are exported to S3 for long-term storage
- **Partitioning**: Data is partitioned by date/hour for efficient querying
- **Compression**: Data is stored in compressed format for cost efficiency

### 3. Analytics Layer

- **AWS Glue**: Defines the schema for the analytics data
- **Amazon Athena**: Provides SQL-based query capabilities
- **Custom Views**: Pre-defined views for common analytics scenarios

### 4. API Layer

- **Usage Endpoints**: REST APIs for retrieving analytics data
- **Token Analytics**: Specialized endpoints for token usage analysis
- **Feedback Analytics**: Endpoints for analyzing user feedback
- **Metadata Analytics**: Analysis by organizational hierarchy, tags, and attributes

## Key Enhancements

### 1. Token Analytics

The system now tracks detailed token usage:

- **Input Tokens**: Tracks tokens sent to the model
- **Output Tokens**: Tracks tokens received from the model
- **Total Tokens**: Aggregates total token usage
- **Cost Per Model**: Calculates cost based on model-specific pricing
- **Time-based Analysis**: Analyzes token usage over time

### 2. Feedback Integration

Feedback data is now integrated into the analytics system:

- **Rating Analysis**: Tracks user satisfaction ratings
- **Category Distribution**: Analyzes feedback by category
- **Comment Analysis**: Provides capabilities for analyzing free-text comments
- **Tag Analysis**: Examines feedback based on user-applied tags
- **Sentiment Analysis**: Analyzes overall sentiment from user interactions

### 3. Metadata Dimensions

The analytics system now incorporates metadata dimensions:

- **Hierarchical Analysis**: Examines usage across organizational hierarchies
- **Tag-based Analysis**: Analyzes usage based on tags (subject, grade level, etc.)
- **Attribute Analysis**: Examines usage based on specific attributes
- **Cross-dimensional Analysis**: Combines multiple dimensions for in-depth insights

## Implementation Details

### Database Schema

The Glue database schema has been enhanced with the following fields:

```typescript
// New fields added to the analytics schema
{
  "InputTokens": {
    type: glue.Schema.struct([
      { name: "N", type: glue.Schema.decimal(20, 0) },
    ]),
  },
  "OutputTokens": {
    type: glue.Schema.struct([
      { name: "N", type: glue.Schema.decimal(20, 0) },
    ]),
  },
  "Metadata": {
    type: glue.Schema.struct([{
      name: "L",
      type: glue.Schema.array(
        glue.Schema.struct([
          {
            name: "M",
            type: glue.Schema.struct([
              { name: "key", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
              { name: "value", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
              { name: "type", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
              { name: "parent_key", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) }
            ])
          }
        ])
      )
    }])
  },
  "Feedback": {
    type: glue.Schema.struct([{
      name: "M",
      type: glue.Schema.struct([
        { name: "rating", type: glue.Schema.struct([{ name: "N", type: glue.Schema.INTEGER }]) },
        { name: "category", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
        { name: "comment", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
        { name: "tags", type: glue.Schema.struct([{ 
          name: "L", 
          type: glue.Schema.array(glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]))
        }]) },
        { name: "metrics", type: glue.Schema.struct([{
          name: "M",
          type: glue.Schema.map(glue.Schema.STRING, glue.Schema.decimal(10, 2))
        }]) },
        { name: "created_at", type: glue.Schema.struct([{ name: "N", type: glue.Schema.decimal(20, 0) }]) }
      ])
    }])
  },
  "Sentiment": {
    type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
  },
  "Topic": {
    type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
  }
}
```

### Athena Views

The system includes the following Athena views for analytics:

1. **token_analytics**: Provides token usage statistics by bot, model, and time period
2. **feedback_analytics**: Analyzes feedback data including ratings, categories, and sentiment
3. **metadata_hierarchy**: Original metadata view for backward compatibility
4. **hierarchy_metadata_view**: Enhanced hierarchical analysis
5. **tag_metadata_view**: Tag-based analysis
6. **attribute_metadata_view**: Attribute-based analysis
7. **metadata_analytics_view**: Combined metadata statistics

### API Endpoints

New and enhanced API endpoints for analytics:

```python
@router.get("/analytics/token/{bot_id}")     # Get token analytics for a specific bot
@router.get("/analytics/feedback/{bot_id}")  # Get feedback analytics for a specific bot
@router.get("/analytics/metadata/{bot_id}")  # Get metadata analytics for a specific bot
@router.get("/analytics/dashboard")          # Get an overview dashboard of analytics
```

## Usage Examples

### Token Usage Analysis

```typescript
// Example response from token analytics endpoint
{
  "bot_id": "bot123",
  "total_input_tokens": 5432198,
  "total_output_tokens": 987654,
  "total_cost": 123.45,
  "model_breakdown": [
    {
      "model": "anthropic.claude-v2",
      "input_tokens": 4321098,
      "output_tokens": 876543,
      "cost": 100.23
    },
    {
      "model": "anthropic.claude-instant-v1",
      "input_tokens": 1111100,
      "output_tokens": 111111,
      "cost": 23.22
    }
  ],
  "daily_usage": [
    {
      "date": "2023-07-01",
      "input_tokens": 123456,
      "output_tokens": 23456,
      "cost": 7.89
    },
    // Additional daily entries...
  ]
}
```

### Feedback Analysis

```typescript
// Example response from feedback analytics endpoint
{
  "bot_id": "bot123",
  "average_rating": 4.6,
  "feedback_count": 1234,
  "category_breakdown": {
    "accuracy": 45,
    "helpfulness": 67,
    "clarity": 23,
    "other": 12
  },
  "sentiment_breakdown": {
    "positive": 78,
    "neutral": 15,
    "negative": 7
  },
  "top_tags": [
    {"name": "helpful", "count": 456},
    {"name": "informative", "count": 345},
    {"name": "responsive", "count": 234}
  ]
}
```

## Configuration

The Usage Analytics system uses the following environment variables:

```
USAGE_ANALYSIS_DATABASE=bedrockchatstack_usage_analysis
USAGE_ANALYSIS_TABLE=ddb_export
USAGE_ANALYSIS_WORKGROUP=bedrockchatstack_wg
USAGE_ANALYSIS_OUTPUT_LOCATION=s3://bedrockchatstack-athena-results
```

## Future Enhancements

1. **Real-time Analytics**: Add real-time analytics capabilities
2. **Predictive Analytics**: Implement predictive models for usage forecasting
3. **Advanced Visualizations**: Enhance dashboard visualization capabilities
4. **Export Capabilities**: Add capabilities to export analytics data in various formats
5. **Custom Report Builder**: Allow users to create custom analytics reports 