"""
Agent module for Strands integration.
"""

from .config import get_bedrock_model_config
from .factory import create_strands_agent

__all__ = [
    "get_bedrock_model_config",
    "create_strands_agent",
]
