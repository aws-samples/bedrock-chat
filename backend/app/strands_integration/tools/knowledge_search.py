import logging
import traceback

from strands import tool
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _search_knowledge_standalone(bot, query: str) -> list:
    """Standalone knowledge search implementation."""
    try:
        from app.vector_search import search_related_docs

        logger.info(f"Running knowledge search with query: {query}")

        search_results = search_related_docs(bot, query=query)

        logger.info(f"Knowledge search completed. Found {len(search_results)} results")
        return search_results

    except Exception as e:
        error_traceback = traceback.format_exc()
        logger.error(f"Failed to run knowledge search: {e}\nTraceback: {error_traceback}")
        return [
            {
                "content": f"Knowledge search error: {str(e)}",
                "source_name": "Error",
                "source_link": "",
            }
        ]


def create_knowledge_search_tool(bot) -> StrandsAgentTool:
    """Create a knowledge search tool with bot context captured in closure."""

    @tool
    def knowledge_search(query: str) -> dict:
        """
        Search knowledge base for relevant information.

        Args:
            query: Search query for vector search, full text search, and hybrid search

        Returns:
            list: Search results for citation support
        """
        logger.debug(f"[KNOWLEDGE_SEARCH_V3] Starting search: query={query}")

        try:
            # # Bot is captured on closure
            current_bot = bot

            if not current_bot:
                logger.warning("[KNOWLEDGE_SEARCH_V3] No bot context available")
                return {
                    "toolUseId": "placeholder",
                    "status": "error",
                    "content": [
                        {
                            "text": f"Knowledge search requires bot configuration. Query was: {query}"
                        }
                    ],
                }

            # Check if bot has knowledge base
            if not current_bot.has_knowledge():
                logger.warning(
                    "[KNOWLEDGE_SEARCH_V3] Bot has no knowledge base configured"
                )
                return {
                    "toolUseId": "placeholder",
                    "status": "error",
                    "content": [
                        {
                            "text": f"Bot does not have a knowledge base configured. Query was: {query}"
                        }
                    ],
                }

            logger.debug(
                f"[KNOWLEDGE_SEARCH_V3] Executing search with bot: {current_bot.id}"
            )

            # Run knowledge search
            results = _search_knowledge_standalone(current_bot, query)

            if not results:
                return {
                    "toolUseId": "placeholder",
                    "status": "success",
                    "content": [
                        {"text": "No relevant information found in the knowledge base."}
                    ],
                }

            logger.debug(f"[KNOWLEDGE_SEARCH_V3] Search completed successfully")
            return {
                "toolUseId": "placeholder",
                "status": "success",
                "content": [{"json": results}],
            }

        except Exception as e:
            logger.error(f"[KNOWLEDGE_SEARCH_V3] Knowledge search error: {e}")
            return {
                "toolUseId": "placeholder",
                "status": "error",
                "content": [
                    {"text": f"An error occurred during knowledge search: {str(e)}"}
                ],
            }

    return knowledge_search
