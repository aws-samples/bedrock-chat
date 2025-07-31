"""
Internet search tool for Strands integration.
"""

import logging
import os
from typing import Any

from strands import tool

logger = logging.getLogger(__name__)

# Firecrawl API key will be read from environment variable


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
    try:
        # Import here to avoid circular imports
        from app.agents.tools.internet_search import _search_with_firecrawl, _internet_search, InternetSearchInput
        
        # Try Firecrawl first if API key is available
        api_key = os.environ.get("FIRECRAWL_API_KEY")
        if api_key:
            logger.info("Using Firecrawl for internet search")
            try:
                results = _search_with_firecrawl(
                    query=query,
                    api_key=api_key,
                    country=country,
                    max_results=10
                )
                if results:
                    # Format Firecrawl results
                    formatted_results = []
                    for result in results:
                        formatted_results.append(
                            f"**{result['source_name']}**\n"
                            f"URL: {result['source_link']}\n"
                            f"Content: {result['content']}\n"
                        )
                    return "\n".join(formatted_results)
            except Exception as firecrawl_error:
                logger.warning(f"Firecrawl search failed: {firecrawl_error}, falling back to DuckDuckGo")
        else:
            logger.info("FIRECRAWL_API_KEY not set, using DuckDuckGo search")
        
        # Fallback to DuckDuckGo search
        logger.info("Using DuckDuckGo for internet search")
        tool_input = InternetSearchInput(
            query=query,
            country=country,
            time_limit=time_limit
        )
        
        results = _internet_search(
            tool_input=tool_input,
            bot=None,  # Use None to default to DuckDuckGo
            model="claude-v3.5-sonnet"
        )
        
        # Format DuckDuckGo results
        if results:
            formatted_results = []
            for result in results:
                formatted_results.append(
                    f"**{result['source_name']}**\n"
                    f"URL: {result['source_link']}\n"
                    f"Content: {result['content']}\n"
                )
            return "\n".join(formatted_results)
        else:
            return "No information found in internet search."
            
    except Exception as e:
        logger.error(f"Internet search error: {e}")
        return f"An error occurred during internet search: {str(e)}"