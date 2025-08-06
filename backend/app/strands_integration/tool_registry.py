"""
Tool registry for Strands integration with citation support.
"""

import logging
import time
import random
from typing import Optional

from strands import tool

from app.agents.tools.agent_tool import AgentTool
from app.agents.tools.bedrock_agent import bedrock_agent_tool
from app.agents.tools.calculator import calculator_tool
from app.agents.tools.internet_search import internet_search_tool
from app.agents.tools.knowledge import create_knowledge_tool
from app.repositories.models.custom_bot import BotModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_tools_for_bot(bot: Optional[BotModel], display_citation: bool = False) -> list:
    """
    Get tools for bot configuration with optional citation support.
    
    Converts AgentTool instances to Strands-compatible DecoratedFunctionTool
    using the @tool decorator. When display_citation=True, tools will embed 
    source_id information in their results.
    
    Args:
        bot: Bot configuration (None for no tools)
        display_citation: Whether to enable citation support
        
    Returns:
        List of Strands-compatible DecoratedFunctionTool objects
    """
    logger.debug(f"[TOOL_REGISTRY] Getting tools for bot: {bot.id if bot else None}")
    logger.debug(f"[TOOL_REGISTRY] Citation enabled: {display_citation}")
    
    tools = []
    
    # Return empty list if no bot or agent not enabled
    if not bot or not bot.is_agent_enabled():
        logger.debug(f"[TOOL_REGISTRY] No bot or agent not enabled, returning empty tools")
        return tools
    
    # Get available tools from agent configuration
    available_tools = {
        "internet_search": internet_search_tool,
        "bedrock_agent": bedrock_agent_tool,
        "calculator": calculator_tool,
    }
    
    # Add configured tools from bot
    for tool_config in bot.agent.tools:
        tool_name = tool_config.name
        if tool_name in available_tools:
            original_tool = available_tools[tool_name]
            
            # Convert AgentTool to Strands-compatible format
            strands_tool = _convert_agentool_to_strands(original_tool, display_citation)
            tools.append(strands_tool)
            logger.debug(f"[TOOL_REGISTRY] Added Strands-compatible tool: {tool_name} (citation: {display_citation})")
    
    # Add knowledge tool if bot has knowledge base
    if bot.has_knowledge():
        knowledge_tool = create_knowledge_tool(bot=bot)
        strands_knowledge_tool = _convert_agentool_to_strands(knowledge_tool, display_citation)
        tools.append(strands_knowledge_tool)
        logger.debug(f"[TOOL_REGISTRY] Added Strands-compatible knowledge tool (citation: {display_citation})")
    
    logger.debug(f"[TOOL_REGISTRY] Total tools created: {len(tools)}")
    
    # Debug: Log tool types and names
    for i, tool in enumerate(tools):
        logger.debug(f"[TOOL_REGISTRY] Tool {i}: type={type(tool)}")
        if hasattr(tool, 'tool_name'):
            logger.debug(f"[TOOL_REGISTRY] Tool {i}: tool_name={tool.tool_name}")
        logger.debug(f"[TOOL_REGISTRY] Tool {i}: callable={callable(tool)}")
    
    return tools


def _convert_agentool_to_strands(agent_tool: AgentTool, display_citation: bool = False):
    """
    Convert AgentTool to Strands-compatible DecoratedFunctionTool.
    
    This function creates a wrapper function that:
    1. Handles the AgentTool's input/output format
    2. Optionally adds citation information to results
    3. Applies Strands @tool decorator for proper recognition
    
    Args:
        agent_tool: Original AgentTool instance
        display_citation: Whether to embed citation information
        
    Returns:
        Strands DecoratedFunctionTool
    """
    logger.debug(f"[TOOL_REGISTRY] Converting AgentTool to Strands format: {agent_tool.name}")
    
    # Create wrapper function with proper signature for Strands
    def tool_wrapper(expression: str) -> str:
        """Strands-compatible wrapper for AgentTool."""
        logger.debug(f"[TOOL_REGISTRY] Executing Strands wrapper for {agent_tool.name}")
        logger.debug(f"[TOOL_REGISTRY] Input expression: {expression}")
        
        # Convert expression to AgentTool input format
        if hasattr(agent_tool, 'args_schema') and agent_tool.args_schema:
            try:
                # Create input object using the tool's schema
                # For calculator, this should be CalculatorInput(expression=expression)
                tool_input = agent_tool.args_schema(expression=expression)
                logger.debug(f"[TOOL_REGISTRY] Created tool input: {tool_input}")
            except Exception as e:
                logger.error(f"[TOOL_REGISTRY] Failed to create tool input: {e}")
                return f"Error: Invalid input for {agent_tool.name}: {str(e)}"
        else:
            # Fallback: create a simple object with expression attribute
            class SimpleInput:
                def __init__(self, expression):
                    self.expression = expression
            tool_input = SimpleInput(expression)
        
        # Execute original AgentTool function
        try:
            result = agent_tool.function(tool_input, bot=None, model=None)
            logger.debug(f"[TOOL_REGISTRY] AgentTool execution result: {result}")
        except Exception as e:
            logger.error(f"[TOOL_REGISTRY] AgentTool execution failed: {e}")
            import traceback
            logger.error(f"[TOOL_REGISTRY] Traceback: {traceback.format_exc()}")
            return f"Error executing {agent_tool.name}: {str(e)}"
        
        # Add citation information if enabled
        if display_citation:
            # Generate unique source_id
            source_id = f"{agent_tool.name}_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Embed source_id in result
            if isinstance(result, str):
                enhanced_result = f"{result} [source_id: {source_id}]"
            elif isinstance(result, dict):
                enhanced_result = result.copy()
                enhanced_result['source_id'] = source_id
                enhanced_result = str(enhanced_result)
            else:
                enhanced_result = f"{str(result)} [source_id: {source_id}]"
            
            logger.debug(f"[TOOL_REGISTRY] Added citation source_id: {source_id}")
            return enhanced_result
        else:
            # Return result as string for Strands
            return str(result) if not isinstance(result, str) else result
    
    # Set function metadata
    tool_wrapper.__name__ = agent_tool.name
    tool_wrapper.__doc__ = agent_tool.description
    
    # Apply Strands @tool decorator to create DecoratedFunctionTool
    strands_tool = tool(tool_wrapper)
    
    logger.debug(f"[TOOL_REGISTRY] Created Strands DecoratedFunctionTool: {agent_tool.name}")
    logger.debug(f"[TOOL_REGISTRY] Strands tool type: {type(strands_tool)}")
    
    return strands_tool
