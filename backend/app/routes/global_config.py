import json
import logging
import os

from fastapi import APIRouter

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s - %(message)s")
logger = logging.getLogger(__name__)

GLOBAL_AVAILABLE_MODELS = os.environ.get("GLOBAL_AVAILABLE_MODELS")
router = APIRouter(tags=["config"])


def get_global_available_models() -> list[str] | None:
    """
    Get the list of globally available models from environment variable.
    Returns None if not configured, which means all models are available.
    """
    if GLOBAL_AVAILABLE_MODELS:
        try:
            models = json.loads(GLOBAL_AVAILABLE_MODELS)
            logger.info(f"Global available models (JSON): {models}")
            return models
        except json.JSONDecodeError:
            # If JSON parsing fails, return error
            logger.error("Failed to parse GLOBAL_AVAILABLE_MODELS as JSON")
            return None
        
    logger.info("No global available models configured - all models are available")
    return None


@router.get("/config/global")
def get_global_config():
    """Get global configuration including available models."""
    global_models = get_global_available_models()
    return {"globalAvailableModels": global_models}
