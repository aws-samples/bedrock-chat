import json
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s - %(message)s")
logger = logging.getLogger(__name__)

GLOBAL_AVAILABLE_MODELS = os.environ.get("GLOBAL_AVAILABLE_MODELS")


def get_global_available_models() -> list[str]:
    """
    Get the list of globally available models from environment variable.
    Returns empty list if not configured or if an empty array is provided,
    which means all models are available.
    """
    if GLOBAL_AVAILABLE_MODELS:
        try:
            models = json.loads(GLOBAL_AVAILABLE_MODELS)
            logger.info(f"Global available models (JSON): {models}")
            # Ensure the result is a list
            if isinstance(models, list):
                return models
            else:
                logger.error(
                    f"GLOBAL_AVAILABLE_MODELS must be a JSON array, got {type(models)}"
                )
                return []
        except json.JSONDecodeError:
            logger.error("Failed to parse GLOBAL_AVAILABLE_MODELS as JSON")
            return []

    logger.info("No global available models configured - all models are available")
    return []
