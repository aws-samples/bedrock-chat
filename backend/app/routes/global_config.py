from fastapi import APIRouter

from app.usecases.global_config import (
    get_logo_path,
    get_global_available_models,
)

router = APIRouter(tags=["config"])


@router.get("/config/global")
def get_global_config():
    """Get global configuration including available models."""
    global_models = get_global_available_models()
    logo_path = get_logo_path()
    return {
        "globalAvailableModels": global_models,
        "logoPath": logo_path,
    }
