from typing import Literal

from pydantic import BaseModel

from app.repositories.models.custom_bot import AssistantConfigModel, CreatorConfigModel


class UsagePerBot(BaseModel):
    id: str  # bot_id
    title: str
    description: str
    published_api_stack_name: str | None
    published_api_datetime: int | None
    owner_user_id: str
    total_price: float
    num_of_users: int
    num_of_convos: int
    assistant_config: AssistantConfigModel | None = None
    creator_config: CreatorConfigModel | None = None
    group_id: str | None = None


class UsagePerUser(BaseModel):
    id: str  # user_id
    email: str
    total_price: float
