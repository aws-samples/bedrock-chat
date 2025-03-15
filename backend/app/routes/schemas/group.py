from __future__ import annotations

from app.routes.schemas.base import BaseSchema

class GroupOutput(BaseSchema):
    group_id: str
    group_name: str
    create_time: float
    update_time: float
    create_by: str
    role: str
    user_name: str
    lti_name: str

# Role hierarchy from lowest to highest
ROLE_HIERARCHY = ["STUDENT", "TEACHER", "SCHOOLADMIN", "DISTRICTADMIN", "SUPERADMIN"]

ACTION_CONFIG_MAP = {
    # For TEACHERs and admins
    "view_assistantList":        {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    "get_assistant":             {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    "create_assistant":          {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    "edit_assistant":            {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    "delete_assistant":          {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    "edit_assistant_visibility": {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    "delete_uploaded_file":      {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    "get_assistant_agents":      {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    "get_presigned_url":         {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": True, "STUDENT": False},
    # Only for admins
    "view_analytics":            {"SUPERADMIN": True, "DISTRICTADMIN": True, "SCHOOLADMIN": True, "TEACHER": False, "STUDENT": False},
}

