"""
Strands integration utilities - Independent tool management.
"""

import logging
from typing import Dict

from app.bedrock import is_tooluse_supported
from app.repositories.models.custom_bot import BedrockAgentToolModel, BotModel
from app.routes.schemas.conversation import type_model_name
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_strands_registered_tools(bot: BotModel | None = None) -> list[StrandsAgentTool]:
    """Get list of available Strands tools."""
    from app.strands_integration.tools.bedrock_agent import create_bedrock_agent_tool
    from app.strands_integration.tools.calculator import create_calculator_tool
    from app.strands_integration.tools.internet_search import (
        create_internet_search_tool,
    )
    from app.strands_integration.tools.simple_list import simple_list, structured_list

    tools: list[StrandsAgentTool] = []
    tools.append(create_internet_search_tool(bot))
    tools.append(create_bedrock_agent_tool(bot))
    # tools.append(create_calculator_tool(bot))  # For testing purposes
    return tools


def get_strands_tools(
    bot: BotModel | None, model_name: type_model_name
) -> list[StrandsAgentTool]:
    """
    Get Strands tools based on bot configuration.

    Similar to agents/utils.py get_tools() but optimized for Strands.
    """
    if not is_tooluse_supported(model_name):
        logger.warning(
            f"Tool use is not supported for model {model_name}. Returning empty tool list."
        )
        return []

    # Return empty list if bot is None or agent is not enabled
    if not bot or not bot.is_agent_enabled():
        return []

    registered_tools = get_strands_registered_tools(bot)
    tools: list[StrandsAgentTool] = []

    # Get tools based on bot's tool configuration
    for tool in bot.agent.tools:
        if tool.name not in [t.tool_name for t in registered_tools]:
            continue

        # Append tool by matching name
        matched_tool = next(
            (t for t in registered_tools if t.tool_name == tool.name), None
        )
        if matched_tool:
            tools.append(matched_tool)

    # Add knowledge tool if bot has knowledge base
    if bot.has_knowledge():
        from app.strands_integration.tools.knowledge_search import (
            create_knowledge_search_tool,
        )

        knowledge_tool = create_knowledge_search_tool(bot)
        tools.append(knowledge_tool)

    if len(tools) == 0:
        logger.warning("No tools configured for bot. Returning empty tool list.")
        return []

    logger.info(f"Strands tools configured for bot: {[t.tool_name for t in tools]}")
    return tools
