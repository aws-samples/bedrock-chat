from app.routes.schemas.group import (
    GroupOutput,
)
from app.usecases.group import (
    fetch_all_groups_by_user_id,
)

from app.user import User
from fastapi import APIRouter, Request



router = APIRouter(tags=["bot"])


@router.get("/group/self", response_model=list[GroupOutput])
def fetch_all_groups_for_user(
    request: Request
):
    """Get all groups for a user."""
    current_user: User = request.state.current_user
    
    groups = fetch_all_groups_by_user_id(current_user.id)
    return groups