"""
Knowledge search tool for Strands integration.
"""

import logging
from typing import Any

from strands import tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@tool
def knowledge_search(query: str) -> str:
    """
    Search knowledge base for relevant information.

    Args:
        query: Search query

    Returns:
        Search results as formatted string
    """
    logger.debug(f"[KNOWLEDGE_TOOL] Starting knowledge search for query: {query}")

    try:
        # Import here to avoid circular imports
        from app.agents.tools.knowledge import KnowledgeToolInput, search_knowledge
        from app.repositories.models.custom_bot import BotModel

        # Create tool input
        tool_input = KnowledgeToolInput(query=query)
        logger.debug(f"[KNOWLEDGE_TOOL] Created tool input")

        # Get bot context from current execution context
        from app.strands_integration.context import get_current_bot, get_current_user

        current_bot = get_current_bot()
        current_user = get_current_user()

        if not current_bot:
            logger.warning("[KNOWLEDGE_TOOL] No bot context available")
            return f"Knowledge search requires bot configuration with knowledge base setup. Query was: {query}"

        # Check if bot has knowledge configuration
        if not (current_bot.knowledge and current_bot.knowledge.source_urls):
            logger.warning("[KNOWLEDGE_TOOL] Bot has no knowledge base configured")
            return f"Bot does not have a knowledge base configured. Query was: {query}"

        try:
            # Execute knowledge search with proper bot context
            logger.debug(f"[KNOWLEDGE_TOOL] Executing search with bot: {current_bot.id}")
            result = search_knowledge(
                tool_input, bot=current_bot, model="claude-v3.5-sonnet"
            )
            logger.debug(f"[KNOWLEDGE_TOOL] Search completed successfully")

            # Format the result
            if isinstance(result, list) and result:
                formatted_results = []
                for item in result:
                    if hasattr(item, "content") and hasattr(item, "source"):
                        formatted_results.append(
                            f"Source: {item.source}Content: {item.content}"
                        )
                    else:
                        formatted_results.append(str(item))

                return "".join(formatted_results)
            else:
                return "No relevant information found in the knowledge base."

        except Exception as search_error:
            logger.warning(f"[KNOWLEDGE_TOOL] Direct search failed: {search_error}")
            # Return a helpful message indicating the limitation
            return f"Knowledge search is available but requires proper bot configuration with knowledge base setup. Query was: {query}"

    except Exception as e:
        logger.error(f"[KNOWLEDGE_TOOL] Knowledge search error: {e}")
        return f"An error occurred during knowledge search: {str(e)}"
