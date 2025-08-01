"""
Bedrock Agent tool for Strands integration.
"""

import logging
from typing import Any

from strands import tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@tool
def bedrock_agent_invoke(query: str, agent_id: str = None) -> str:
    """
    Invoke Bedrock Agent for specialized tasks.
    
    Args:
        query: Query to send to the agent
        agent_id: Optional agent ID (will use bot configuration if not provided)
        
    Returns:
        Agent response as string
    """
    logger.debug(f"[BEDROCK_AGENT_TOOL] Starting Bedrock Agent invocation for query: {query}")
    logger.debug(f"[BEDROCK_AGENT_TOOL] Agent ID: {agent_id}")
    
    try:
        # Import here to avoid circular imports
        from app.agents.tools.bedrock_agent import _bedrock_agent_invoke, BedrockAgentInput
        from app.repositories.models.custom_bot import BotModel
        
        # Create tool input
        tool_input = BedrockAgentInput(input_text=query)
        logger.debug(f"[BEDROCK_AGENT_TOOL] Created tool input")
        
        # Get bot context from current execution context
        from app.strands_integration.context import get_current_bot, get_current_user
        
        current_bot = get_current_bot()
        current_user = get_current_user()
        
        if not current_bot:
            logger.warning("[BEDROCK_AGENT_TOOL] No bot context available")
            return f"Bedrock Agent requires bot configuration with agent setup. Query was: {query}"
        
        # Check if bot has bedrock agent configuration
        if not (hasattr(current_bot, 'bedrock_agent_id') and current_bot.bedrock_agent_id):
            logger.warning("[BEDROCK_AGENT_TOOL] Bot has no Bedrock Agent configured")
            return f"Bot does not have a Bedrock Agent configured. Query was: {query}"
        
        # Use provided agent_id or get from bot configuration
        effective_agent_id = agent_id or current_bot.bedrock_agent_id
        logger.debug(f"[BEDROCK_AGENT_TOOL] Using agent ID: {effective_agent_id}")
        
        try:
            # Execute bedrock agent invocation with proper bot context
            logger.debug(f"[BEDROCK_AGENT_TOOL] Executing invocation with bot: {current_bot.id}")
            result = _bedrock_agent_invoke(tool_input, bot=current_bot, model="claude-v3.5-sonnet")
            logger.debug(f"[BEDROCK_AGENT_TOOL] Invocation completed successfully")
            
            # Format the result
            if isinstance(result, str):
                return result
            elif hasattr(result, 'output'):
                return str(result.output)
            else:
                return str(result)
                
        except Exception as invoke_error:
            logger.warning(f"[BEDROCK_AGENT_TOOL] Direct invocation failed: {invoke_error}")
            # Return a helpful message indicating the limitation
            return f"Bedrock Agent is available but requires proper bot configuration with agent setup. Query was: {query}"
        
    except Exception as e:
        logger.error(f"[BEDROCK_AGENT_TOOL] Bedrock Agent error: {e}")
        return f"An error occurred during Bedrock Agent invocation: {str(e)}"