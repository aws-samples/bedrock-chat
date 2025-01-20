from typing import List
import logging
import time

from app.agents.tools.agent_tool import AgentTool
from app.routes.schemas.bot import AgentTool as AgentToolSchema
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from app.agents.tools.internet_search import internet_search_tool
from app.agents.tools.knowledge import create_knowledge_tool
from app.agents.tools.simple_quiz import create_simple_quiz_tool
from app.agents.tools.lesson_plan import create_unified_lesson_planner_tool
from app.repositories.models.custom_bot import GenerationParamsModel, AgentModel, KnowledgeModel, ActiveModelsModel

logger = logging.getLogger(__name__)

DEFAULT_AGENT_MODEL = "claude_v3_5_haiku"

# Valid models for Agents
#     "claude_v3_5_sonnet_v2"
#     "claude_v3_5_sonnet"
#     "claude_v3_5_haiku"


# Tool registry for available tools
AVAILABLE_TOOLS: dict[str, AgentTool] = {
    "internet_search": internet_search_tool,
}

# Bot-specific tool creators
BOT_TOOL_CREATORS = {
    "knowledge_base_search": create_knowledge_tool,
    "quiz_generator": create_simple_quiz_tool,  # Changed key to match frontend expectation
    "lesson_planner": create_unified_lesson_planner_tool,  # Changed key to match frontend expectation
}

def fetch_available_agent_tools() -> List[AgentToolSchema]:
    """
    Fetch all available tools that can be added to a bot.
    Used by the /bot/{bot_id}/agent/available-tools endpoint.
    Returns schema representations of tools for API responses.
    
    This implementation uses get_available_tools logic to ensure consistency
    and avoid hard-coding of tools.
    """
    logger.info("Fetching available agent tool schemas")
    
    # Get all possible tools using get_available_tools
    # Pass bot=None to get all possible tools (new bot flow)
    all_tools = get_available_tools(bot=None)
    
    # Convert AgentTool instances to AgentToolSchema representations
    tool_schemas = []
    for tool in all_tools:
        logger.debug(f"Converting tool to schema: {tool.__class__.__name__}")
        tool_schemas.append(AgentToolSchema(
            name=tool.name,  # Use the tool's defined name property
            description=tool.description
        ))
    
    logger.info(f"Returning {len(tool_schemas)} tool schemas")
    return tool_schemas

def get_tool_by_name(
    name: str,
    bot: BotModel | None = None,
    model: type_model_name | None = None
) -> AgentTool:
    """
    Get a tool instance by name.
    For bot-specific tools, requires bot and model context.
    """
    logger.info(f"Getting tool by name: {name}, model: {model}")
    
    # Check static tools first
    if name in AVAILABLE_TOOLS:
        logger.debug(f"Found static tool: {name}")
        return AVAILABLE_TOOLS[name]
        
    # Check bot-specific tools
    if name in BOT_TOOL_CREATORS:
        # For creation flow, allow dummy bot
        if bot is None:
            logger.debug(f"Creating dummy bot for tool: {name}")
            bot = create_dummy_bot()
        if model is None:
            logger.debug("No model provided, using default")
            model = DEFAULT_AGENT_MODEL
            
        logger.debug(f"Creating bot-specific tool: {name} for bot_id={bot.id}, model={model}")
        return BOT_TOOL_CREATORS[name](bot, model)
    
    logger.error(f"Tool with name {name} not found")        
    raise ValueError(f"Tool with name {name} not found")    

def create_dummy_bot() -> BotModel:
    """Create a dummy bot with all required fields for tool creation"""
    current_timestamp = float(time.time())  # Import time module at the top
    
    return BotModel(
        # Required string fields - using reasonable defaults
        id="new",
        title="Dummy Bot",  # Empty string might not be valid
        description="Temporary bot for tool testing",
        instruction="Default instruction for dummy bot",
        
        # Timestamp fields - should be valid timestamps
        create_time=current_timestamp,
        last_used_time=current_timestamp,
        
        # Optional fields can be None
        public_bot_id=None,
        owner_user_id="dummy_user@qikrai.com",  # Should have a valid format
        
        # Boolean fields
        is_pinned=False,
        display_retrieved_chunks=False,
        
        # Nested models need proper initialization
        generation_params=GenerationParamsModel(
            max_tokens=1000,
            temperature=0.0,
            top_p=0.7,
            top_k=10,
            stop_sequences=[],
            presence_penalty=0.0,  # Adding missing defaults
            frequency_penalty=0.0
        ),
        
        # Agent configuration
        agent=AgentModel(
            tools=[],
            model=DEFAULT_AGENT_MODEL  # Add default model if required
        ),
        
        # Knowledge base configuration
        knowledge=KnowledgeModel(
            source_urls=[],
            sitemap_urls=[],
            filenames=[],
            s3_urls=[],
            chunk_size=500,  # Add if required
            chunk_overlap=50  # Add if required
        ),
        
        # Status fields - using valid enum values
        sync_status="SUCCEEDED",  # Using valid enum value
        sync_status_reason="Dummy bot initialization",
        sync_last_exec_id="dummy-exec-id",
        
        # API related fields
        published_api_stack_name=None,
        published_api_datetime=None,
        published_api_codebuild_id=None,
        
        # Additional configurations
        conversation_quick_starters=[],
        bedrock_knowledge_base=None,
        bedrock_guardrails=None,
        
        # Active models configuration
        active_models=ActiveModelsModel(
            chat=DEFAULT_AGENT_MODEL,  # Set default model if required
            knowledge_base=DEFAULT_AGENT_MODEL,
            tools=DEFAULT_AGENT_MODEL
        )
    )

def get_available_tools(
    bot: BotModel | None = None,
    model: type_model_name | None = None
) -> list[AgentTool]:
    """
    Get all available tools based on bot configuration.
    If bot is provided, includes bot-specific tools configured for that bot.
    Returns actual AgentTool instances rather than schemas.
    """
    logger.info(f"Getting available tools (bot={bot.id if bot else 'None'}, model={model})")
    
    tools: list[AgentTool] = []
    
    # Add all static tools first
    logger.debug(f"Adding static tools: {list(AVAILABLE_TOOLS.keys())}")
    tools.extend(AVAILABLE_TOOLS.values())
    
    # For the /bot/new/agent/available-tools endpoint, always return all possible tools
    if bot is None:
        logger.debug("No bot provided - new bot flow, adding all possible tools")
        dummy_bot = create_dummy_bot()
    else:
        dummy_bot = bot  # Use provided bot

    effective_model = model or DEFAULT_AGENT_MODEL  # Default model if none provided

    # Add bot-specific tools only once
    logger.info(f"Adding core bot tools (quiz and knowledge base) using model: {effective_model}")
    for tool_name, creator in BOT_TOOL_CREATORS.items():
        try:
            tools.append(creator(dummy_bot, effective_model))
            logger.debug(f"Successfully added {tool_name} tool")
        except Exception as e:
            logger.error(f"Error creating tool {tool_name}: {str(e)}")
    
    # Log details of each tool being returned
    for tool in tools:
        logger.info(f"Tool: {tool.__class__.__name__}, Description: {tool.description}, Required Args: {tool.required_args if hasattr(tool, 'required_args') else 'None'}")
    
    logger.info(f"Returning {len(tools)} tools")
    return tools