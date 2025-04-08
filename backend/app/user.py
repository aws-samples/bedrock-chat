from pydantic import BaseModel
from typing import List, Optional

# Define a schema for a single membership
class UserMembership(BaseModel):
    group_id: Optional[str] = None
    role: str

class User(BaseModel):
    id: str
    name: str
    # Replace 'groups' and the old 'memberships' with a list of UserMembership objects
    memberships: List[UserMembership] = []
