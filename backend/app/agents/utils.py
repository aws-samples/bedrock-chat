from typing import List
import logging

from app.agents.tools.agent_tool import AgentTool
from app.routes.schemas.bot import AgentTool as AgentToolSchema
from app.agents.tools.internet_search import create_internet_search_tool
from app.agents.tools.knowledge import create_knowledge_tool
from app.agents.tools.simple_quiz import create_simple_quiz_tool
from app.agents.tools.lesson_plan import create_unified_lesson_planner_tool

logger = logging.getLogger(__name__)

# Tool registry for available tools
AVAILABLE_TOOLS: dict[str, AgentTool] = {
    "internet_search": create_internet_search_tool,
    "knowledge_base_tool": create_knowledge_tool,
    "quiz_generator": create_simple_quiz_tool,
    "lesson_planner": create_unified_lesson_planner_tool,
}

def get_available_tools() -> list[AgentTool]:
    """
    Get all available tools based on agent configuration.
    Returns actual AgentTool instances rather than schemas.
    """
    tools: list[AgentTool] = []
    
    # Instantiate all tools from the registry
    logger.info(f"Available tools: {list(AVAILABLE_TOOLS.keys())}")
    tools = [func() for func in AVAILABLE_TOOLS.values()]
    
    return tools


def get_tool_by_name(name: str) -> AgentTool:
    """Get a tool instance by name."""
    if name not in AVAILABLE_TOOLS:
        logger.error(f"Tool with name {name} not found")        
        raise ValueError(f"Tool with name {name} not found")
    return AVAILABLE_TOOLS[name]()