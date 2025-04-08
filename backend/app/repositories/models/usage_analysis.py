from typing import Literal, List
from datetime import datetime

from pydantic import BaseModel

from app.repositories.models.custom_bot import AssistantConfigModel, CreatorConfigModel


class UsagePerBot(BaseModel):
    id: str  # bot_id
    title: str
    description: str
    published_api_stack_name: str | None
    published_api_datetime: int | None
    owner_user_id: str
    total_price: float | None = None
    num_of_users: int
    num_of_convos: int
    assistant_config: AssistantConfigModel | None = None
    creator_config: CreatorConfigModel | None = None
    group_id: str | None = None


class UsagePerUser(BaseModel):
    id: str  # user_id
    email: str
    total_price: float | None = None
    num_sessions: int = 0
    num_messages: int = 0


class DailyUsage(BaseModel):
    date: str  # YYYY-MM-DD format
    num_sessions: int
    num_messages: int
    input_tokens: int
    output_tokens: int
    cost: float | None = None


class TopicAnalysis(BaseModel):
    """Analysis of a specific topic."""
    topic: str
    count: int # Ensure this matches what get_topics_analysis returns
    # No percentage or cost fields needed in the repository model


class AnalyticsSummary(BaseModel):
    """Analytics summary data."""
    num_sessions: int = 0
    num_messages: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float | None = None
    total_bots: int = 0
    total_users: int = 0


class BotAnalytics(BaseModel):
    """Detailed analytics for a specific bot."""

    bot_id: str
    title: str
    description: str
    owner_user_id: str
    total_users: int
    total_sessions: int
    total_messages: int
    total_input_tokens: int
    total_output_tokens: int
    total_cost: float | None = None
    daily_usage: List[DailyUsage]
    top_users: List[UsagePerUser]
    top_topics: List[TopicAnalysis]


class AnalyticsDashboard(BaseModel):
    """Data structure for the analytics dashboard."""

    summary: AnalyticsSummary
    daily_usage: List[DailyUsage]
    top_bots: List[UsagePerBot]
    top_users: List[UsagePerUser]
