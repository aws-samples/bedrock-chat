"""
Internet search tool for Strands integration.
"""

import logging

from app.agents.tools.internet_search import InternetSearchInput, _internet_search
from strands import tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_internet_search_tool(bot):
    """Create an internet search tool with bot context."""

    @tool
    def internet_search(query: str, country: str = "jp-jp", time_limit: str = "d") -> str:
        """
        Search the internet for information.

        Args:
            query: Search query
            country: Country code for search (default: jp-jp)
            time_limit: Time limit for search results (default: d for day)

        Returns:
            Search results as formatted string
        """
        logger.debug(
            f"[INTERNET_SEARCH_TOOL] Starting internet search for query: {query}"
        )
        logger.debug(
            f"[INTERNET_SEARCH_TOOL] Country: {country}, Time limit: {time_limit}"
        )

        try:
            # Use the bot passed during tool creation
            current_bot = bot
            logger.debug(
                f"[INTERNET_SEARCH_TOOL] Using bot from tool creation: {current_bot.id if current_bot else None}"
            )

            # Use existing _internet_search function with proper bot configuration
            tool_input = InternetSearchInput(
                query=query, country=country, time_limit=time_limit
            )

            logger.debug(
                "[INTERNET_SEARCH_TOOL] Using existing _internet_search with bot configuration"
            )
            results = _internet_search(
                tool_input=tool_input,
                bot=current_bot,  # Pass the actual bot with Firecrawl config
                model="claude-v3.7-sonnet",
            )

            # Return results as list for citation support
            if results:
                logger.debug(
                    f"[INTERNET_SEARCH_TOOL] Search returned {len(results)} results"
                )
                return results  # Return list for proper citation support
            else:
                logger.debug("[INTERNET_SEARCH_TOOL] No results returned")
                return "No information found in internet search."

        except Exception as e:
            logger.error(f"[INTERNET_SEARCH_TOOL] Internet search error: {e}")
            return f"An error occurred during internet search: {str(e)}"

    return internet_search
