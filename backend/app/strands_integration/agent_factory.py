"""
Agent factory for creating Strands agents from bot configurations.
"""

import logging
import os
from typing import Optional

from app.repositories.models.custom_bot import BotModel
from app.user import User
from strands import Agent
from strands.models import BedrockModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_strands_agent(bot: Optional[BotModel], user: User, model_name: str = "claude-v3.5-sonnet", enable_reasoning: bool = False) -> Agent:
    """
    Create a Strands agent from bot configuration.
    
    Args:
        bot: Optional bot configuration
        user: User making the request
        model_name: Model name to use
        enable_reasoning: Whether to enable reasoning functionality
        
    Returns:
        Configured Strands agent
    """
    logger.debug(f"[AGENT_FACTORY] Creating Strands agent - user: {user.id}, model: {model_name}, reasoning: {enable_reasoning}")
    logger.debug(f"[AGENT_FACTORY] Bot: {bot.id if bot else None}")
    # Bedrock model configuration
    logger.debug(f"[AGENT_FACTORY] Getting Bedrock model configuration...")
    model_config = _get_bedrock_model_config(bot, model_name, enable_reasoning)
    logger.debug(f"[AGENT_FACTORY] Model config: {model_config}")
    model = BedrockModel(**model_config)
    
    # Get tools for bot before creating agent
    logger.debug(f"[AGENT_FACTORY] Getting tools for bot...")
    tools = _get_tools_for_bot(bot)
    logger.debug(f"[AGENT_FACTORY] Tools configured: {len(tools)}")
    
    # Get system prompt
    system_prompt = bot.instruction if bot and bot.instruction else None
    logger.debug(f"[AGENT_FACTORY] System prompt: {len(system_prompt) if system_prompt else 0} chars")
    
    # Create agent with tools and system prompt
    logger.debug(f"[AGENT_FACTORY] Creating Agent instance...")
    agent = Agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt
    )
    
    logger.debug(f"[AGENT_FACTORY] Agent created successfully")
    return agent


def _get_bedrock_model_config(bot: Optional[BotModel], model_name: str = "claude-v3.5-sonnet", enable_reasoning: bool = False) -> dict:
    """Get Bedrock model configuration."""
    from app.bedrock import get_model_id
    
    # Use provided model name (BotModel doesn't have a direct model attribute)
    
    # Get proper Bedrock model ID
    bedrock_region = os.environ.get("BEDROCK_REGION", "us-east-1")
    enable_cross_region = os.environ.get("ENABLE_BEDROCK_CROSS_REGION_INFERENCE", "false").lower() == "true"
    
    model_id = get_model_id(
        model_name,
        bedrock_region=bedrock_region,
        enable_cross_region=enable_cross_region
    )
    
    config = {
        "model_id": model_id,
        "region_name": bedrock_region,
    }
    
    # Add model parameters if available
    if bot and bot.generation_params:
        if bot.generation_params.temperature is not None:
            config["temperature"] = bot.generation_params.temperature
        if bot.generation_params.top_p is not None:
            config["top_p"] = bot.generation_params.top_p
        if bot.generation_params.max_tokens is not None:
            config["max_tokens"] = bot.generation_params.max_tokens
    
    # Add Guardrails configuration (Strands way)
    if bot and bot.bedrock_guardrails:
        guardrails = bot.bedrock_guardrails
        config["guardrail_id"] = guardrails.guardrail_arn
        config["guardrail_version"] = guardrails.guardrail_version
        config["guardrail_trace"] = "enabled"  # Enable trace for debugging
        logger.info(f"Enabled Guardrails: {guardrails.guardrail_arn}")
    
    # Add reasoning functionality if explicitly enabled
    additional_request_fields = {}
    if enable_reasoning and bot and bot.generation_params and bot.generation_params.reasoning_params:
        additional_request_fields["thinking"] = {
            "type": "enabled",
            "budget_tokens": bot.generation_params.reasoning_params.budget_tokens
        }
        # When thinking is enabled, temperature must be 1
        config["temperature"] = 1.0
    
    if additional_request_fields:
        config["additional_request_fields"] = additional_request_fields
    
    return config


def _get_tools_for_bot(bot: Optional[BotModel]) -> list:
    """Get tools list for bot configuration."""
    tools = []
    
    # Check if bot has agent tools configured
    if not (bot and bot.agent and bot.agent.tools):
        return tools
    
    # Knowledge search tool
    if bot.knowledge and bot.knowledge.source_urls:
        try:
            from app.strands_integration.tools.knowledge_tool_strands import knowledge_search
            tools.append(knowledge_search)
            logger.info("Added knowledge search tool")
        except ImportError:
            logger.warning("Knowledge search tool not available")
    
    # Internet search tool - check if internet search is enabled in agent tools
    for tool in bot.agent.tools:
        if hasattr(tool, 'name') and 'internet' in tool.name.lower():
            try:
                from app.strands_integration.tools.internet_search_tool_strands import internet_search
                tools.append(internet_search)
                logger.info("Added internet search tool")
                break
            except ImportError:
                logger.warning("Internet search tool not available")
    
    # Bedrock agent tool
    if hasattr(bot, 'bedrock_agent_id') and bot.bedrock_agent_id:
        try:
            from app.strands_integration.tools.bedrock_agent_tool_strands import bedrock_agent_invoke
            tools.append(bedrock_agent_invoke)
            logger.info("Added bedrock agent tool")
        except ImportError:
            logger.warning("Bedrock agent tool not available")
    
    logger.info(f"Total tools configured: {len(tools)}")
    return tools