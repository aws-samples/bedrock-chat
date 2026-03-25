import json
import logging
import os

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel, InternetToolModel
from app.routes.schemas.conversation import type_model_name
from app.utils import get_bedrock_runtime_client
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field, root_validator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _load_tavily_api_key() -> str:
    """Load Tavily API key from env var or AWS Secrets Manager."""
    direct_key = os.environ.get("TAVILY_API_KEY", "")
    if direct_key:
        return direct_key

    secret_arn = os.environ.get("TAVILY_API_KEY_SECRET_ARN", "")
    if not secret_arn:
        return ""

    try:
        import boto3

        region = os.environ.get("REGION", "us-east-1")
        client = boto3.client("secretsmanager", region_name=region)
        response = client.get_secret_value(SecretId=secret_arn)
        key = response.get("SecretString", "").strip()
        logger.info("Loaded Tavily API key from Secrets Manager.")
        return key
    except Exception as e:
        logger.warning(f"Could not load Tavily API key from Secrets Manager: {e}")
        return ""


TAVILY_API_KEY = _load_tavily_api_key()


class InternetSearchInput(BaseModel):
    query: str = Field(description="The query to search for on the internet.")
    locale: str = Field(
        default="en-us",
        description="The country code and language code for the search. Must be `{language}-{country}` for example `jp-jp` (Japanese - Japan), `zh-cn` (Chinese - China), `en-ca` (English - Canada), `fr-ca` (French - Canada), `en-nz` (English - New Zealand), etc. If empty the default is `en-us`.",
    )
    time_limit: str = Field(
        description="Retrieve only the most recent results, for example `1w` only returns the results from the last week. Units are 'd' (day), 'w' (week), 'm' (month), 'y' (year). Use empty string to retrieve all results."
    )

    @root_validator(pre=True)
    def validate_locale(cls, values):
        locale = values.get("locale")
        # Basic validation for locale format
        if not locale or locale.count("-") != 1:
            # Get the default value from the field definition
            default_locale = cls.__fields__["locale"].default
            values["locale"] = default_locale
        return values


def _summarize_content(content: str, title: str, url: str, query: str) -> str:
    """
    Summarize content using Claude Haiku 4.5 to prevent context window bloat.
    Returns a concise summary (800-1500 tokens max) preserving key information.
    """
    try:
        client = get_bedrock_runtime_client()

        # Truncate content if it's too long to avoid token limits
        max_input_length = 8000  # Conservative limit for input
        if len(content) > max_input_length:
            content = content[:max_input_length] + "..."

        prompt = f"""Please provide a concise summary of the following web content in 800-1500 tokens maximum. Focus on information that directly answers or relates to the user's query: "{query}"

Title: {title}
URL: {url}
Content: {content}

Summary:"""

        response = client.invoke_model(
            modelId="anthropic.claude-haiku-4-5-20251001",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1500,
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
        # Fallback: return truncated content if summarization fails
        fallback_content = content[:1000] + "..." if len(content) > 1000 else content
        logger.info(f"Using fallback content: {len(fallback_content)} chars")
        return fallback_content


def _search_with_tavily(query: str, time_limit: str, locale: str, api_key: str) -> list:
    """Search using Tavily API."""
    try:
        from tavily import TavilyClient

        logger.info(f"Executing Tavily search with query: {query}, time_limit: {time_limit}")

        client = TavilyClient(api_key=api_key)

        days_map = {"d": 1, "w": 7, "m": 30, "y": 365}
        days = days_map.get(time_limit, None)

        search_kwargs: dict = {
            "query": query,
            "max_results": 10,
            "include_answer": False,
            "include_raw_content": False,
        }
        if days:
            search_kwargs["days"] = days

        response = client.search(**search_kwargs)
        results = response.get("results", [])

        logger.info(f"Tavily search completed. Found {len(results)} results")

        summarized_results = []
        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            content = r.get("content", "")
            summary = _summarize_content(content, title, url, query)
            summarized_results.append(
                {
                    "content": summary,
                    "source_name": title,
                    "source_link": url,
                }
            )

        return summarized_results

    except Exception as e:
        logger.error(f"Tavily search error: {e}")
        return []


def _search_with_firecrawl(
    query: str, api_key: str, locale: str, max_results: int = 10
) -> list:
    logger.info(
        f"Searching with Firecrawl. Query: {query}, Max Results: {max_results}, Locale: {locale}"
    )

    try:
        app = FirecrawlApp(api_key=api_key)

        # Search using Firecrawl
        # SearchParams: https://github.com/mendableai/firecrawl/blob/main/apps/python-sdk/firecrawl/firecrawl.py#L24
        from firecrawl import ScrapeOptions

        # Incoming locale is language-country (e.g. 'en-us').
        language, country = locale.split("-", 1)
        results = app.search(
            query,
            limit=max_results,
            lang=language,
            location=country,
            scrape_options=ScrapeOptions(formats=["markdown"], onlyMainContent=True),
        )

        if not results:
            logger.warning("No results found")
            return []

        # Log detailed information about the results object
        logger.info(
            f"results of firecrawl: success={getattr(results, 'success', 'unknown')} warning={getattr(results, 'warning', None)} error={getattr(results, 'error', None)}"
        )

        # Log the data structure
        if hasattr(results, "data"):
            data_sample = results.data[:1] if results.data else []
            logger.info(f"data sample: {data_sample}")
        else:
            logger.info(
                f"results attributes: {[attr for attr in dir(results) if not attr.startswith('_')]}"
            )
            logger.info(
                f"results as dict attempt: {dict(results) if hasattr(results, '__dict__') else 'no __dict__'}"
            )

        # Format and summarize search results
        search_results = []

        # Handle Firecrawl SearchResponse object structure
        # The Python SDK returns a SearchResponse object with .data attribute
        if hasattr(results, "data") and results.data:
            data_list = results.data
        else:
            logger.error(
                f"No data found in results. Results type: {type(results)}, attributes: {[attr for attr in dir(results) if not attr.startswith('_')]}"
            )
            return []

        logger.info(f"Found {len(data_list)} data items")
        for i, data in enumerate(data_list):
            try:
                logger.info(
                    f"Data item {i}: type={type(data)}, keys={list(data.keys()) if isinstance(data, dict) else 'not dict'}"
                )

                if isinstance(data, dict):
                    title = data.get("title", "")
                    # Try different URL fields based on Firecrawl API response structure
                    url = data.get("url", "") or (
                        data.get("metadata", {}).get("sourceURL", "")
                        if isinstance(data.get("metadata"), dict)
                        else ""
                    )
                    content = data.get("markdown", "") or data.get("content", "")

                    if not title and not content:
                        logger.warning(f"Skipping data item {i} - no title or content")
                        continue

                    # Summarize the content
                    summary = _summarize_content(content, title, url, query)

                    search_results.append(
                        {
                            "content": summary,
                            "source_name": title,
                            "source_link": url,
                        }
                    )
                else:
                    logger.warning(f"Data item {i} is not a dict: {type(data)}")
            except Exception as e:
                logger.error(f"Error processing data item {i}: {e}")
                continue

        logger.info(f"Found {len(search_results)} results from Firecrawl")
        return search_results

    except Exception as e:
        logger.error(f"Error searching with Firecrawl: {e}")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception args: {e.args}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")

        # Instead of raising, return empty list to allow fallback
        return []


def _internet_search(
    tool_input: InternetSearchInput, bot: BotModel | None, model: type_model_name | None
) -> list:
    from app.pdf_url_handler import download_pdfs_from_urls
    from app.repositories.models.conversation import DocumentToolResultModel

    query = tool_input.query
    time_limit = tool_input.time_limit
    locale = tool_input.locale

    logger.info(
        f"Internet search request - Query: {query}, Time Limit: {time_limit}, Locale: {locale}"
    )

    # Only Tavily is active. Firecrawl is available but deactivated.
    if TAVILY_API_KEY:
        logger.info("Using Tavily for internet search")
        results = _search_with_tavily(query, time_limit, locale, TAVILY_API_KEY)
        if results:
            # Download any PDFs found in search result URLs and include as documents
            source_urls = [r["source_link"] for r in results if r.get("source_link")]
            pdf_downloads = download_pdfs_from_urls(source_urls)
            if pdf_downloads:
                for filename, pdf_bytes, source_url in pdf_downloads:
                    results.append(
                        DocumentToolResultModel(
                            format="pdf",
                            name=filename.replace(".pdf", "").replace(".", "")[:50],
                            document=pdf_bytes,
                        )
                    )
                    logger.info(
                        f"Included PDF document from search result: {source_url}"
                    )
            return results
        logger.warning("Tavily returned no results")
        return []

    logger.warning(
        "No search provider configured (no Tavily API key). "
        "Set TAVILY_API_KEY or TAVILY_API_KEY_SECRET_ARN to enable internet search."
    )
    return []


internet_search_tool = AgentTool(
    name="internet_search",
    description="Search the internet for information.",
    args_schema=InternetSearchInput,
    function=_internet_search,
)
