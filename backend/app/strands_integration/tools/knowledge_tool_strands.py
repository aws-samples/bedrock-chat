"""
Knowledge search tool for Strands integration.
"""

import logging
from typing import Any

from strands import tool

logger = logging.getLogger(__name__)


@tool
def knowledge_search(query: str) -> str:
    """
    Search knowledge base for relevant information.
    
    Args:
        query: Search query
        
    Returns:
        Search results as formatted string
    """
    try:
        # Import here to avoid circular imports
        from app.agents.tools.knowledge import search_knowledge, KnowledgeToolInput
        
        # Create tool input
        tool_input = KnowledgeToolInput(query=query)
        
        # Note: This is a simplified wrapper - in real usage, bot context would be provided
        # For now, we'll return a placeholder indicating the tool needs proper bot context
        return "Knowledge search requires bot configuration with knowledge base setup."
        
    except Exception as e:
        logger.error(f"Knowledge search error: {e}")
        return f"An error occurred during knowledge search: {str(e)}"