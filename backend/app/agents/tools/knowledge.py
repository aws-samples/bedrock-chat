import logging
from typing import List

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from app.vector_search import search_related_docs

from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)


class KnowledgeToolInput(BaseModel):
    query: str = Field(description="User's original question string.")


def search_knowledge(
    tool_input: KnowledgeToolInput, bot: BotModel | None, model: type_model_name | None
) -> List:
    """
    Search the knowledge base for relevant documents using the provided query.
    
    Args:
        tool_input: The input containing the search query
        bot: The bot instance containing the knowledge base
        model: The model type name
        
    Returns:
        List of search results
        
    Raises:
        ValueError: If bot is not provided
        Exception: If search fails
    """
    if bot is None:
        raise ValueError("Bot instance is required for knowledge base search")
        
    query = tool_input.query
    logger.info(f"Running AnswerWithKnowledgeTool with query: {query}")

    try:
        search_results = search_related_docs(
            bot,
            query=query,
        )

        # # For testing purpose
        # search_results = dummy_search_results

        return search_results

    except Exception as e:
        logger.error(f"Failed to run AnswerWithKnowledgeTool: {e}")
        raise e


def create_knowledge_tool(bot: BotModel) -> AgentTool:
    """
    Create a knowledge base search tool instance for a specific bot and model.
    
    Args:
        bot: The bot instance containing the knowledge base
        
    Returns:
        AgentTool instance configured for knowledge base search
    """
    description = (
        #"Search and answer questions using the knowledge base."
        "Search and answer questions using the knowledge base. Available knowledge: {}"
        .format(bot.knowledge.__str_in_claude_format__())
    )
    
    logger.info(f"Creating knowledge base tool with description: {description}")
    
    return AgentTool(
        name="knowledge_base_search",
        description=description,
        args_schema=KnowledgeToolInput,
        function=search_knowledge,
    )
