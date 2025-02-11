from __future__ import annotations

from app.routes.schemas.base import BaseSchema

class GroupOutput(BaseSchema):
    group_id: str
    group_name: str
    create_time: float
    update_time: float
    create_by: str
    role: str