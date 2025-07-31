"""
Bedrock Agent tool for Strands integration.
"""

import logging
from typing import Any

from strands import tool

logger = logging.getLogger(__name__)


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
    try:
        # Import here to avoid circular imports
        from app.agents.tools.bedrock_agent import _bedrock_agent_invoke, BedrockAgentInput
        
        # Create tool input
        tool_input = BedrockAgentInput(input_text=query)
        
        # Note: This is a simplified wrapper - in real usage, bot context would be provided
        # For now, we'll return a placeholder indicating the tool needs proper bot context
        return "Bedrock Agent requires bot configuration with agent setup."
        
    except Exception as e:
        logger.error(f"Bedrock Agent error: {e}")
        return f"An error occurred during Bedrock Agent invocation: {str(e)}"