from __future__ import annotations
from typing import Optional, Dict

from app.routes.schemas.base import BaseSchema

class GroupOutput(BaseSchema):
    group_id: str
    group_name: str
    create_time: float
    update_time: float
    create_by: str
    role: str
    user_name: str
    lti_name: Optional[str] = None

# Role hierarchy from lowest to highest
ROLE_HIERARCHY = ["STUDENT", "TEACHER", "SCHOOLADMIN", "DISTRICTADMIN", "SUPERADMIN"]

ACTION_CONFIG_MAP: Dict[str, Dict[str, bool]] = {
    # Bot/Assistant Permissions
    "view_assistantList": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "get_assistant": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "create_assistant": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "edit_assistant": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "delete_assistant": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "edit_assistant_visibility": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "delete_uploaded_file": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "get_assistant_agents": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "get_presigned_url": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": True, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },

    # Analytics Permissions (New Granular Permissions)
    "view_analytics_dashboard": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "view_bot_analytics": {
        "SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": True, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
    "view_cost_data": {
        "SUPERADMIN": True, "DISTRICTADMIN": False, "SCHOOLADMIN": False, "TEACHER": False, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": False, "PublishingBotAllowed": False, "Admin": True # Cognito Functional Group
    },
    "view_all_bots_analytics": {
        "SUPERADMIN": True, "DISTRICTADMIN": False, "SCHOOLADMIN": False, "TEACHER": False, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": False, "PublishingBotAllowed": False, "Admin": True # Cognito Functional Group
    },

    # Add action for publishing
    "publish_assistant": {
        "SUPERADMIN": True, "DISTRICTADMIN": False, "SCHOOLADMIN": False, "TEACHER": False, "STUDENT": False, # Hierarchical Roles
        "CreatingBotAllowed": False, "PublishingBotAllowed": True, "Admin": True # Cognito Functional Group
    },
}