import logging
import traceback
from retry import retry
from botocore.exceptions import ClientError

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from app.vector_search import search_related_docs

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AuroraAutoResumeError(Exception):
    """Raised when Aurora Knowledge Base is auto-paused and recovering."""


class KnowledgeToolInput(BaseModel):
    query: str = Field(
        description=(
            "Input suitable for vector search, full text search, and hybrid search. "
            "When searching continuously, the query must be designed so that it "
            "does not overlap with past contexts."
        )
    )


@retry(
    retry_on_exception=lambda e: isinstance(e, AuroraAutoResumeError),
    wait_exponential_multiplier=1000,  # base delay = 1s
    wait_exponential_max=60000,  # cap delay at 60s
    stop_max_attempt_number=3,  # total tries = 3
)
def _search_with_retry(bot: BotModel, query: str) -> list:
    """
    Wraps the actual search call and raises AuroraAutoResumeError
    on “auto-paused” errors so the decorator retries.
    """
    try:
        return search_related_docs(bot, query=query)
    except Exception as e:
        msg = str(e).lower()
        if isinstance(e, ClientError) and "resuming after being auto-paused" in msg:
            logger.warning(f"Aurora KB auto-paused, retrying: {msg}")
            raise AuroraAutoResumeError(msg) from e
        raise  # non-Aurora errors bubble up immediately


def search_knowledge(
    tool_input: KnowledgeToolInput,
    bot: BotModel | None,
    model: type_model_name | None,
) -> list:
    """
    Entry point for the AgentTool. Delegates to _search_with_retry,
    which will retry on Aurora auto-pauses.
    """
    assert bot is not None, "BotModel is required"
    query = tool_input.query
    logger.info(f"Running AnswerWithKnowledgeTool with query: {query}")

    try:
        return _search_with_retry(bot, query)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Failed to run AnswerWithKnowledgeTool: {e}\n{tb}")
        raise


def create_knowledge_tool(bot: BotModel) -> AgentTool:
    description = (
        "Answer a user's question using information. The description is: "
        f"{bot.knowledge.__str_in_claude_format__()}"
    )
    logger.info(f"Creating knowledge base tool with description: {description}")
    return AgentTool(
        name="knowledge_base_tool",
        description=description,
        args_schema=KnowledgeToolInput,
        function=search_knowledge,
    )
