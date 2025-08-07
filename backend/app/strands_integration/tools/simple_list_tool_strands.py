"""
Simple list tool for Strands integration.
This is a thin wrapper around the traditional AgentTool simple_list implementation.
"""

import logging

# Import the core simple_list function from the traditional AgentTool
from app.agents.tools.simple_list import generate_simple_list
from strands import tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@tool
def simple_list(topic: str, count: int = 5) -> str:
    """
    Generate a simple list of items for a given topic.

    Args:
        topic: Topic to generate list about (e.g., 'colors', 'fruits', 'countries')
        count: Number of items to return in the list (default: 5, max: 10)

    Returns:
        str: JSON string containing list of items
    """
    logger.debug(f"[STRANDS_SIMPLE_LIST_TOOL] Delegating to core simple_list: topic={topic}, count={count}")

    # Delegate to the core simple_list implementation
    result = generate_simple_list(topic, count)

    logger.debug(f"[STRANDS_SIMPLE_LIST_TOOL] Core simple_list result: {len(result)} chars")
    return result
