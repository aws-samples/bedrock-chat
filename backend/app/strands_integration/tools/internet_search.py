import json
import logging

from strands import tool
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _search_with_duckduckgo_standalone(
    query: str, time_limit: str, country: str
) -> list:
    """Standalone DuckDuckGo search implementation."""
    try:
        from duckduckgo_search import DDGS

        REGION = country
        SAFE_SEARCH = "moderate"
        MAX_RESULTS = 20
        BACKEND = "api"

        logger.info(
            f"Executing DuckDuckGo search: query={query}, region={REGION}, time_limit={time_limit}"
        )

        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    keywords=query,
                    region=REGION,
                    safesearch=SAFE_SEARCH,
                    timelimit=time_limit,
                    max_results=MAX_RESULTS,
                    backend=BACKEND,
                )
            )

        # Format results for citation support
        formatted_results = []
        for result in results:
            formatted_results.append(
                {
                    "content": _summarize_content_standalone(
                        result["body"], result["title"], result["href"], query
                    ),
                    "source_name": result["title"],
                    "source_link": result["href"],
                }
            )

        logger.info(
            f"DuckDuckGo search completed. Found {len(formatted_results)} results"
        )
        return formatted_results

    except Exception as e:
        logger.error(f"DuckDuckGo search error: {e}")
        return [
            {
                "content": f"Search error: {str(e)}",
                "source_name": "Error",
                "source_link": "",
            }
        ]


def _search_with_firecrawl_standalone(
    query: str, api_key: str, country: str, max_results: int = 10
) -> list:
    """Standalone Firecrawl search implementation."""
    try:
        from firecrawl import FirecrawlApp, ScrapeOptions

        logger.info(
            f"Searching with Firecrawl: query={query}, max_results={max_results}"
        )

        app = FirecrawlApp(api_key=api_key)

        results = app.search(
            query,
            limit=max_results,
            location=country,
            scrape_options=ScrapeOptions(formats=["markdown"], onlyMainContent=True),
        )

        if not results or not hasattr(results, "data") or not results.data:
            logger.warning("No results found from Firecrawl")
            return []

        # Format results
        formatted_results = []
        for data in results.data:
            if isinstance(data, dict):
                title = data.get("title", "")
                url = data.get("url", "") or (
                    data.get("metadata", {}).get("sourceURL", "")
                    if isinstance(data.get("metadata"), dict)
                    else ""
                )
                content = data.get("markdown", "") or data.get("content", "")

                if title or content:
                    formatted_results.append(
                        {
                            "content": _summarize_content_standalone(
                                content, title, url, query
                            ),
                            "source_name": title,
                            "source_link": url,
                        }
                    )

        logger.info(
            f"Firecrawl search completed. Found {len(formatted_results)} results"
        )
        return formatted_results

    except Exception as e:
        logger.error(f"Firecrawl search error: {e}")
        return []


def _summarize_content_standalone(
    content: str, title: str, url: str, query: str
) -> str:
    """Standalone content summarization."""
    try:
        from app.utils import get_bedrock_runtime_client

        # Truncate content if too long
        max_input_length = 8000
        if len(content) > max_input_length:
            content = content[:max_input_length] + "..."

        client = get_bedrock_runtime_client()

        prompt = f"""Please provide a concise summary of the following web content in 500-800 tokens maximum. Focus on information that directly answers or relates to the user's query: "{query}"

Title: {title}
URL: {url}
Content: {content}

Summary:"""

        response = client.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 800,
                    "messages": [{"role": "user", "content": prompt}],
                }
            ),
        )

        response_body = json.loads(response["body"].read())
        summary = response_body["content"][0]["text"].strip()

        logger.info(
            f"Summarized content from {len(content)} chars to {len(summary)} chars"
        )
        return summary

    except Exception as e:
        logger.error(f"Error summarizing content: {e}")
        # Fallback: return truncated content
        fallback_content = content[:1000] + "..." if len(content) > 1000 else content
        return fallback_content


def _get_internet_tool_config(bot):
    """Extract internet tool configuration from bot."""
    if not bot or not bot.agent or not bot.agent.tools:
        return None

    for tool_config in bot.agent.tools:
        if tool_config.tool_type == "internet":
            return tool_config

    return None


def create_internet_search_tool(bot) -> StrandsAgentTool:
    """Create an internet search tool with bot context captured in closure."""

    @tool
    def internet_search(
        query: str, country: str = "jp-jp", time_limit: str = "d"
    ) -> dict:
        """
        Search the internet for information.

        Args:
            query: Search query
            country: Country code for search (default: jp-jp)
            time_limit: Time limit for search results (default: d for day)

        Returns:
            dict: ToolResult format with search results in json field
        """
        logger.debug(
            f"[INTERNET_SEARCH_V3] Starting search: query={query}, country={country}, time_limit={time_limit}"
        )

        try:
            # # Bot is captured on closure
            current_bot = bot

            # Use DuckDuckGo if no bot context
            if not current_bot:
                logger.debug("[INTERNET_SEARCH_V3] No bot context, using DuckDuckGo")
                results = _search_with_duckduckgo_standalone(query, time_limit, country)
            else:
                internet_tool = _get_internet_tool_config(current_bot)

                if (
                    internet_tool
                    and internet_tool.search_engine == "firecrawl"
                    and internet_tool.firecrawl_config
                    and internet_tool.firecrawl_config.api_key
                ):

                    logger.debug("[INTERNET_SEARCH_V3] Using Firecrawl search")
                    results = _search_with_firecrawl_standalone(
                        query=query,
                        api_key=internet_tool.firecrawl_config.api_key,
                        country=country,
                        max_results=internet_tool.firecrawl_config.max_results,
                    )

                    # If no results from Firecrawl, fallback to DuckDuckGo
                    if not results:
                        logger.warning(
                            "[INTERNET_SEARCH_V3] Firecrawl returned no results, falling back to DuckDuckGo"
                        )
                        results = _search_with_duckduckgo_standalone(
                            query, time_limit, country
                        )
                else:
                    logger.debug("[INTERNET_SEARCH_V3] Using DuckDuckGo search")
                    results = _search_with_duckduckgo_standalone(
                        query, time_limit, country
                    )

            # Return in ToolResult format to prevent Strands from converting to string
            return {
                "toolUseId": "placeholder",  # Will be replaced by Strands
                "status": "success",
                "content": [{"json": results}],
            }

        except Exception as e:
            logger.error(f"[INTERNET_SEARCH_V3] Internet search error: {e}")
            return {
                "toolUseId": "placeholder",
                "status": "error",
                "content": [{"text": f"Search error: {str(e)}"}],
            }

    return internet_search
