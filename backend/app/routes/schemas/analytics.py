"""Analytics schema models."""

from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field

class DailyUsage(BaseModel):
    """Daily usage statistics."""
    date: str
    num_sessions: int = Field(default=0)
    num_messages: int = Field(default=0)
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost: Optional[float] = None

class TopicAnalysis(BaseModel):
    """Topic analysis statistics."""
    topic: str
    message_count: int = Field(default=0)
    percentage: float = Field(default=0.0)

class AnalyticsSummary(BaseModel):
    """Analytics summary data."""
    num_sessions: int = Field(default=0)
    num_messages: int = Field(default=0)
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost: Optional[float] = None
    total_bots: Optional[int] = None
    total_users: Optional[int] = None

class UsagePerBot(BaseModel):
    """Usage statistics per bot."""
    id: str
    title: str
    description: str
    published_api_stack_name: Optional[str] = None
    published_api_datetime: Optional[int] = None
    owner_user_id: str
    total_price: Optional[float] = None
    num_of_users: int = Field(default=0)
    num_of_convos: int = Field(default=0)
    assistant_config: Optional[Dict[str, Union[str, int, float, bool, dict]]] = None
    creator_config: Optional[Dict[str, Union[str, int, float, bool, dict]]] = None
    group_id: Optional[str] = None

class UsagePerUser(BaseModel):
    """Usage statistics per user."""
    id: str
    email: str
    num_sessions: int = Field(default=0)
    num_messages: int = Field(default=0)
    total_price: Optional[float] = None

class BotAnalytics(BaseModel):
    """Detailed bot analytics."""
    bot_id: str
    title: str
    description: str
    owner_user_id: str
    total_users: int = Field(default=0)
    total_sessions: int = Field(default=0)
    total_messages: int = Field(default=0)
    total_input_tokens: Optional[int] = None
    total_output_tokens: Optional[int] = None
    total_cost: Optional[float] = None
    daily_usage: List[DailyUsage] = Field(default_factory=list)
    top_users: List[UsagePerUser] = Field(default_factory=list)
    top_topics: List[TopicAnalysis] = Field(default_factory=list)

class AnalyticsDashboard(BaseModel):
    """Analytics dashboard data."""
    summary: AnalyticsSummary = Field(default_factory=AnalyticsSummary)
    top_bots: List[UsagePerBot] = Field(default_factory=list)
    top_users: List[UsagePerUser] = Field(default_factory=list)
    daily_usage: List[DailyUsage] = Field(default_factory=list)

class MetadataAnalytics(BaseModel):
    """Metadata analytics response model."""
    hierarchies: Dict[str, Dict[str, Union[str, List[str]]]] = Field(default_factory=dict)
    usage_count: int = Field(default=0)

class FeedbackAnalytics(BaseModel):
    """Feedback analytics response model."""
    average_rating: float = Field(default=0.0)
    total_feedback: int = Field(default=0)
    categories: Dict[str, Dict[str, Union[int, float]]] = Field(default_factory=dict)
    sentiments: Dict[str, int] = Field(default_factory=dict)
    topics: Dict[str, int] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)

class TokenAnalytics(BaseModel):
    """Token usage analytics response model."""
    total_input_tokens: int = Field(default=0)
    total_output_tokens: int = Field(default=0)
    total_cost: float = Field(default=0.0)
    models: Dict[str, Dict[str, Union[int, float]]] = Field(default_factory=dict)

class BotSummary(AnalyticsSummary):
    """Specific summary for a single bot (inherits general fields)."""
    pass

class SummaryAnalyticsData(BaseModel):
    """Response schema for the /dashboard/summary endpoint."""
    summary: AnalyticsSummary
    daily_usage: List[DailyUsage]

class TopEntitiesData(BaseModel):
    """Response schema for the /dashboard/top-entities endpoint."""
    top_users: List[UsagePerUser]
    top_bots: List[UsagePerBot]

class TopicsData(BaseModel):
    """Response schema for the /dashboard/topics endpoint."""
    topics: List[TopicAnalysis]
    total_count: int

class AnalyticsDashboard(BaseModel):
    """Represents the full (potentially legacy) dashboard structure."""
    summary: AnalyticsSummary
    daily_usage: List[DailyUsage]
    top_bots: List[UsagePerBot]
    top_users: List[UsagePerUser]

class UsagePerUserOutput(BaseModel):
    """Aggregated usage per user."""
    id: str
    email: Optional[str] = None
    total_price: Optional[float] = None
    message_count: Optional[int] = None
    num_sessions: Optional[int] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

class UsagePerBotOutput(BaseModel):
    """Aggregated usage per bot, including metadata."""
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    owner_user_id: Optional[str] = None
    total_price: Optional[float] = None
    num_of_convos: Optional[int] = None
    num_of_users: Optional[int] = None
    group_id: Optional[str] = None
    message_count: Optional[int] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

class MetadataAnalytics(BaseModel):
    """ Placeholder for Metadata Analytics Schema """
    pass

class FeedbackAnalytics(BaseModel):
    """ Placeholder for Feedback Analytics Schema """
    pass

class TokenAnalytics(BaseModel):
    """ Placeholder for Token Analytics Schema """
    pass 