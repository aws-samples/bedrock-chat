import logging

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel, InternetToolModel
from app.routes.schemas.conversation import type_model_name
from duckduckgo_search import DDGS
from firecrawl.firecrawl import FirecrawlApp
from pydantic import BaseModel, Field, root_validator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class InternetSearchInput(BaseModel):
    query: str = Field(description="The query to search for on the internet.")
    country: str = Field(
        description="The country code you wish for search. Must be one of: jp-jp (Japan), kr-kr (Korea), cn-zh (China), fr-fr (France), de-de (Germany), es-es (Spain), it-it (Italy), us-en (United States)"
    )
    time_limit: str = Field(
        description="The time limit for the search. Options are 'd' (day), 'w' (week), 'm' (month), 'y' (year)."
    )

    @root_validator(pre=True)
    def validate_country(cls, values):
        country = values.get("country")
        if country not in [
            "jp-jp",
            "kr-kr",
            "cn-zh",
            "fr-fr",
            "de-de",
            "es-es",
            "it-it",
            "us-en",
        ]:
            raise ValueError(
                f"Country must be one of: jp-jp (Japan), kr-kr (Korea), cn-zh (China), fr-fr (France), de-de (Germany), es-es (Spain), it-it (Italy), us-en (United States)"
            )
        return values


def _search_with_duckduckgo(query: str, time_limit: str, country: str) -> list:
    REGION = country
    SAFE_SEARCH = "moderate"
    MAX_RESULTS = 20
    BACKEND = "api"
    logger.info(
        f"Executing DuckDuckGo search with query: {query}, region: {REGION}, time_limit: {time_limit}"
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
        logger.info(f"DuckDuckGo search completed. Found {len(results)} results")
        return [
            {
                "content": result["body"],
                "source_name": result["title"],
                "source_link": result["href"],
            }
            for result in results
        ]


def _search_with_firecrawl(
    query: str, api_key: str, country: str, max_results: int = 10
) -> list:
    logger.info(f"Searching with Firecrawl. Query: {query}, Max Results: {max_results}")

    try:
        app = FirecrawlApp(api_key=api_key)

        # Search using Firecrawl
        # SearchParams: https://github.com/mendableai/firecrawl/blob/main/apps/python-sdk/firecrawl/firecrawl.py#L24
        results = app.search(
            query,
            {
                "limit": max_results,
                "lang": country,
                "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True},
            },
        )

        if not results:
            logger.warning("No results found")
            return []
        logger.info(f"results of firecrawl: {results}")

        # Format search results
        search_results = [
            {
                "content": data.get("markdown", {}),
                "source_name": data.get("title", ""),
                "source_link": data.get("metadata", {}).get("sourceURL", ""),
            }
            for data in results.get("data", [])
            if isinstance(data, dict)
        ]

        logger.info(f"Found {len(search_results)} results from Firecrawl")
        return search_results

    except Exception as e:
        logger.error(f"Error searching with Firecrawl: {e}")
        raise e


def _internet_search(
    tool_input: InternetSearchInput, bot: BotModel | None, model: type_model_name | None
) -> list:
    query = tool_input.query
    time_limit = tool_input.time_limit
    country = tool_input.country

    logger.info(
        f"Internet search request - Query: {query}, Time Limit: {time_limit}, Country: {country}"
    )

    if bot is None:
        logger.warning("Bot is None, defaulting to DuckDuckGo search")
        return _search_with_duckduckgo(query, time_limit, country)

    # Find internet search tool
    internet_tool = next(
        (tool for tool in bot.agent.tools if isinstance(tool, InternetToolModel)),
        None,
    )

    # If no internet tool found or search engine is duckduckgo, use DuckDuckGo
    if not internet_tool or internet_tool.search_engine == "duckduckgo":
        logger.info("No internet tool found or search engine is DuckDuckGo")
        return _search_with_duckduckgo(query, time_limit, country)

    # Handle Firecrawl search
    if internet_tool.search_engine == "firecrawl":
        if not internet_tool.firecrawl_config:
            raise ValueError("Firecrawl configuration is not set in the bot.")

        try:
            api_key = internet_tool.firecrawl_config.api_key
            if not api_key:
                raise ValueError("Firecrawl API key is empty")

            return _search_with_firecrawl(
                query=query,
                api_key=api_key,
                country=country,
                max_results=internet_tool.firecrawl_config.max_results,
            )
        except Exception as e:
            logger.error(f"Error with Firecrawl search: {e}")
            raise e

    # Fallback to DuckDuckGo for any unexpected cases
    logger.warning("Unexpected search engine configuration, falling back to DuckDuckGo")
    return _search_with_duckduckgo(query, time_limit, country)


internet_search_tool = AgentTool(
    name="internet_search",
    description="Search the internet for information.",
    args_schema=InternetSearchInput,
    function=_internet_search,
)
