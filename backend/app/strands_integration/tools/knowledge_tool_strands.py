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
        from app.agents.tools.knowledge import search_related_docs
        from app.repositories.custom_bot import find_bot_by_id
        from app.user import User
        
        # For now, we'll need to get bot and user context from somewhere
        # This is a simplified implementation
        results = search_related_docs(
            tool_input={"query": query},
            bot=None,  # Will need proper bot context
            model="claude-v3.5-sonnet"
        )
        
        if results:
            formatted_results = []
            for result in results:
                formatted_results.append(f"- {result.content}")
            return "\\n".join(formatted_results)
        else:
            return "関連する情報が見つかりませんでした。"
            
    except Exception as e:
        logger.error(f"Knowledge search error: {e}")
        return f"検索中にエラーが発生しました: {str(e)}"