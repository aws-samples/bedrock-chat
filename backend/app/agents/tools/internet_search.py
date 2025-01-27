import logging
import json
import os
from typing import List, Dict
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import boto3
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field, model_validator

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name

logger = logging.getLogger(__name__)


def get_bing_api_key() -> str:
    """Get Bing API key from AWS Secrets Manager."""
    try:
        # Validate environment variable
        secret_arn = os.environ.get('BING_API_SECRET_ARN')
        if not secret_arn:
            logger.error("BING_API_SECRET_ARN environment variable not set")
            return ""

        # Initialize AWS client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=secret_arn.split(':')[3]  # Extract region from ARN
        )

        # Retrieve and parse secret
        secret = client.get_secret_value(SecretId=secret_arn)
        secret_dict = json.loads(secret['SecretString'])
        
        if 'search_api_key' not in secret_dict:
            logger.error("'search_api_key' not found in secret value")
            return ""
            
        return secret_dict['search_api_key']

    except client.exceptions.ResourceNotFoundException:
        logger.error(f"Secret {secret_arn} not found")
    except client.exceptions.InvalidRequestException as e:
        logger.error(f"Invalid request for secret: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse secret value as JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error retrieving Bing API key: {e}")
    
    return ""


class InternetSearchInput(BaseModel):
    query: str = Field(description="The query to search for on the internet.")
    country: str = Field(
        description="The country code you wish for search. Must be one of: jp-jp (Japan), kr-kr (Korea), cn-zh (China), fr-fr (France), de-de (Germany), es-es (Spain), it-it (Italy), us-en (United States)"
    )
    time_limit: str = Field(
        description="The time limit for the search. Options are 'd' (day), 'w' (week), 'm' (month), 'y' (year)."
    )

    @model_validator(mode='before')
    @classmethod
    def validate_country(cls, data: dict) -> dict:
        if data.get("country") not in [
            "jp-jp", "kr-kr", "cn-zh", "fr-fr", "de-de", "es-es", "it-it", "us-en",
        ]:
            raise ValueError(
                "Country must be one of: jp-jp (Japan), kr-kr (Korea), cn-zh (China), "
                "fr-fr (France), de-de (Germany), es-es (Spain), it-it (Italy), us-en (United States)"
            )
        return data

def search_duckduckgo(query: str, country: str, time_limit: str) -> List[Dict]:
    """Perform a DuckDuckGo search."""
    SAFE_SEARCH = "moderate"
    MAX_RESULTS = 10
    BACKEND = "auto"
    
    # In search_duckduckgo
    logger.info("DDG Search params - query: %s, country: %s, time: %s", query, country, time_limit)
    try:
        with DDGS() as ddgs:
            results = ddgs.text(
                keywords=query,
                region=country,
                safesearch=SAFE_SEARCH,
                timelimit=time_limit,
                max_results=MAX_RESULTS,
                backend=BACKEND,
            )
            if not results:
                return []

            logger.info(f"DDGS results: {str(results)[:500]}...")
            return [
                {
                    "content": result.get("body", "No content available"),
                    "source_name": result["title"],
                    "source_link": result["href"],
                }
                for result in results
            ]

    except Exception as e:
        logger.error("DuckDuckGo search failed", exc_info=True)
        raise    

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def search_bing(query: str, country: str) -> List[Dict]:
    """Fallback Bing search with retry logic."""
    api_key = get_bing_api_key()
    if not api_key:
        raise ValueError("Bing Search API key not configured for fallback")
        
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    market = country.replace("-", "-") if "-" in country else f"{country}-{country}"
    
    params = {
        "q": query,
        "count": 10,
        "offset": 0,
        "mkt": market,
        "responseFilter": "Webpages",
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    results = search_results.get("webPages", {}).get("value", [])
    
    return [
        {
            "content": result["snippet"],
            "source_name": result["name"],
            "source_link": result["url"],
        }
        for result in results
    ]

def _perform_internet_search(
    tool_input: InternetSearchInput,
    bot: BotModel | None,
    model: type_model_name | None
) -> dict:
    """
    Performs internet search using DuckDuckGo with Bing fallback.

    Args:
        tool_input: Search parameters (query, country, time_limit)
        bot: Bot model instance
        model: Model name 

    Returns:
        dict: {
            "status": "success"|"error",
            "error": Optional[str],
            "related_documents": List[Dict]
        }
    """
    try:
        results = search_duckduckgo(
            query=tool_input.query,
            country=tool_input.country,
            time_limit=tool_input.time_limit
        )
        
        if not results:  # No results triggers Bing fallback
            logger.warning(f"No DuckDuckGo results for query: {tool_input.query}")
            return _try_bing_fallback(tool_input)
            
        return {
            "status": "success", 
            "related_documents": results
        }
        
    except Exception as dds_error:
        error_msg = str(dds_error).lower()
        if "202 ratelimit" in error_msg:
            logger.warning("DuckDuckGo rate limit hit, trying Bing")
        else:
            logger.error(f"DuckDuckGo search failed: {str(dds_error)}")
        return _try_bing_fallback(tool_input)

def _try_bing_fallback(tool_input: InternetSearchInput) -> dict:
    """Helper function for Bing fallback logic"""
    bing_key = get_bing_api_key()
    if not bing_key:
        return {
            "status": "error",
            "error": "Search services unavailable - no Bing API key",
            "related_documents": []
        }
        
    try:
        logger.info("Attempting Bing search")
        bing_results = search_bing(
            query=tool_input.query,
            country=tool_input.country
        )
        if not bing_results:
            return {
                "status": "error",
                "error": "No results found",
                "related_documents": []
            }
        return {
            "status": "success",
            "related_documents": bing_results
        }
    except Exception as bing_error:
        logger.error(f"Bing search failed: {str(bing_error)}")
        return {
            "status": "error",
            "error": str(bing_error),
            "related_documents": []
        }


def internet_search(
    tool_input: InternetSearchInput,
    bot: BotModel | None,
    model: type_model_name | None
) -> List[str]:
    """
    Search the internet and return formatted citation strings.

    Args:
        tool_input: Search parameters (query, country, time_limit)
        bot: Bot model instance 
        model: Model name

    Returns:
        List[str]: Each string formatted as '[^N] Source: Content' where N is citation number.
        On error, returns single-item list with error message.
    """
    raw_results = _perform_internet_search(tool_input, bot, model)
    
    if raw_results["status"] != "success":
        return [f"Search failed: {raw_results.get('error', 'Unknown error')}"]
        
    return [
        f"{doc['source_link']} - {doc['source_name']}: {doc['content']}"
        for i, doc in enumerate(raw_results["related_documents"])
    ]


def create_internet_search_tool() -> AgentTool:
    """
    Create a internet search tool instance
    
    Returns:
        AgentTool instance configured for internet search
    """
    description = (
        "Search the internet for information using DuckDuckGo with Bing fallback."
    )
    
    logger.info(f"Creating internet search tool with description: {description}")
    
    return AgentTool(
        name="internet_search",
        description=description,
        args_schema=InternetSearchInput,
        function=internet_search,
    )