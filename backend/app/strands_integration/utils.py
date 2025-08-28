"""
Strands integration utilities - Independent tool management.
"""

import logging
from typing import Dict

from app.bedrock import is_tooluse_supported
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_strands_available_tools(bot: BotModel | None = None) -> list[StrandsAgentTool]:
    """Get list of available Strands tools."""
    from app.strands_integration.tools.calculator import (
        create_calculator_tool,
        create_advanced_calculator_tool,
    )
    from app.strands_integration.tools.simple_list import (
        simple_list,
        structured_list,
    )
    from app.strands_integration.tools.internet_search import (
        create_internet_search_tool,
    )
    from app.strands_integration.tools.bedrock_agent import (
        create_bedrock_agent_tool,
    )
    from app.strands_integration.tools.knowledge_search import (
        create_knowledge_search_tool,
    )

    tools: list[StrandsAgentTool] = []
    tools.append(create_calculator_tool(bot))
    tools.append(create_advanced_calculator_tool(bot))
    tools.append(simple_list)
    tools.append(structured_list)
    tools.append(create_internet_search_tool(bot))  # Pass bot for context
    tools.append(create_bedrock_agent_tool(bot))  # Pass bot for context
    tools.append(create_knowledge_search_tool(bot))  # Pass bot for context
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

    tools: list[StrandsAgentTool] = []

    # Get static tools
    available_static_tools = {
        tool.__name__: tool for tool in get_strands_available_tools(bot)
    }

    # Get tools based on bot's tool configuration
    for tool_config in bot.agent.tools:
        try:
            # Handle static tools
            if tool_config.name in available_static_tools:
                tools.append(available_static_tools[tool_config.name])

            # Handle dynamic tools that need bot context
            elif tool_config.name == "internet_search":
                from app.strands_integration.tools.internet_search import (
                    create_internet_search_tool,
                )

                internet_tool = create_internet_search_tool(bot)
                tools.append(internet_tool)

            elif (
                tool_config.name == "bedrock_agent"
                and tool_config.tool_type == "bedrock_agent"
            ):
                from app.strands_integration.tools.bedrock_agent import (
                    create_bedrock_agent_tool,
                )

                bedrock_tool = create_bedrock_agent_tool(bot)
                tools.append(bedrock_tool)

            else:
                logger.warning(f"Unknown tool: {tool_config.name}")

        except Exception as e:
            logger.error(f"Error processing tool {tool_config.name}: {e}")

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

    return tools
