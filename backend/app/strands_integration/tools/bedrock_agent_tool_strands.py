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
        from app.agents.tools.bedrock_agent import invoke_bedrock_agent
        
        # Use existing bedrock agent implementation
        result = invoke_bedrock_agent(
            tool_input={
                "query": query,
                "agent_id": agent_id
            },
            bot=None,  # Will need proper bot context
            model="claude-v3.5-sonnet"
        )
        
        if result and hasattr(result, 'content'):
            return result.content
        else:
            return "Bedrock Agentからの応答を取得できませんでした。"
            
    except Exception as e:
        logger.error(f"Bedrock Agent error: {e}")
        return f"Bedrock Agent実行中にエラーが発生しました: {str(e)}"