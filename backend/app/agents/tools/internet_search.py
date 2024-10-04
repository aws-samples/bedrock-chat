import json

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field, root_validator


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


def internet_search(
    tool_input: InternetSearchInput, bot: BotModel | None, model: type_model_name | None
) -> str:
    query = tool_input.query
    time_limit = tool_input.time_limit
    country = tool_input.country

    REGION = country
    SAFE_SEARCH = "moderate"
    MAX_RESULTS = 20
    BACKEND = "api"
    res = []
    with DDGS() as ddgs:
        res = ddgs.text(
            query,
            region=REGION,
            safesearch=SAFE_SEARCH,
            timelimit=time_limit,
            max_results=MAX_RESULTS,
            backend=BACKEND,
        )
    return json.dumps(res)


internet_search_tool = AgentTool(
    name="internet_search",
    description="Search the internet for information.",
    args_schema=InternetSearchInput,
    function=internet_search,
)
