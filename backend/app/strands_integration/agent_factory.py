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

from .citation_prompt import get_citation_system_prompt
from .tool_registry import get_tools_for_bot as _get_tools_for_bot

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_strands_agent(
    bot: Optional[BotModel],
    user: User,
    model_name: str = "claude-v3.5-sonnet",
    enable_reasoning: bool = False,
    display_citation: bool = False,
) -> tuple[Agent, list]:
    """
    Create a Strands agent from bot configuration.

    Args:
        bot: Optional bot configuration
        user: User making the request
        model_name: Model name to use
        enable_reasoning: Whether to enable reasoning functionality
        display_citation: Whether to enable citation support for tools

    Returns:
        Tuple of (configured Strands agent, list of tools)
    """
    logger.debug(
        f"[AGENT_FACTORY] Creating Strands agent - user: {user.id}, model: {model_name}, reasoning: {enable_reasoning}, citation: {display_citation}"
    )
    logger.debug(f"[AGENT_FACTORY] Bot: {bot.id if bot else None}")
    # Bedrock model configuration
    logger.debug(f"[AGENT_FACTORY] Getting Bedrock model configuration...")
    model_config = _get_bedrock_model_config(bot, model_name, enable_reasoning)
    logger.debug(f"[AGENT_FACTORY] Model config: {model_config}")
    model = BedrockModel(**model_config)

    # Get tools for bot before creating agent
    logger.debug(f"[AGENT_FACTORY] Getting tools for bot...")
    tools = _get_tools_for_bot(bot, display_citation)
    logger.debug(f"[AGENT_FACTORY] Tools configured: {len(tools)}")

    # Debug: Log detailed tool information before passing to Strands
    logger.debug(f"[AGENT_FACTORY] About to pass tools to Strands Agent:")
    for i, tool in enumerate(tools):
        logger.debug(f"[AGENT_FACTORY] Tool {i}: type={type(tool)}")
        logger.debug(f"[AGENT_FACTORY] Tool {i}: repr={repr(tool)}")
        if hasattr(tool, "__name__"):
            logger.debug(f"[AGENT_FACTORY] Tool {i}: __name__={tool.__name__}")
        if hasattr(tool, "tool_name"):
            logger.debug(f"[AGENT_FACTORY] Tool {i}: tool_name={tool.tool_name}")
        if callable(tool):
            logger.debug(f"[AGENT_FACTORY] Tool {i}: is callable")
        else:
            logger.debug(f"[AGENT_FACTORY] Tool {i}: is NOT callable")
            logger.debug(f"[AGENT_FACTORY] Tool {i}: value={tool}")

    # Debug: Log detailed tool information
    for i, tool in enumerate(tools):
        logger.debug(f"[AGENT_FACTORY] Tool {i}: type={type(tool)}")
        if hasattr(tool, "name"):
            logger.debug(f"[AGENT_FACTORY] Tool {i}: name={tool.name}")
        if hasattr(tool, "__name__"):
            logger.debug(f"[AGENT_FACTORY] Tool {i}: __name__={tool.__name__}")
        if callable(tool):
            logger.debug(f"[AGENT_FACTORY] Tool {i}: is callable")
        else:
            logger.debug(f"[AGENT_FACTORY] Tool {i}: is NOT callable")

    # Create system prompt with optional citation instructions
    base_system_prompt = bot.instruction if bot and bot.instruction else ""

    if display_citation and tools:
        # Add citation instructions when citation is enabled and tools are available
        citation_prompt = get_citation_system_prompt(model_name)
        system_prompt = f"{base_system_prompt}\n\n{citation_prompt}".strip()
        logger.debug(f"[AGENT_FACTORY] Citation prompt added to system prompt")
    else:
        system_prompt = base_system_prompt if base_system_prompt else None
        logger.debug(f"[AGENT_FACTORY] Using base system prompt only")

    logger.debug(
        f"[AGENT_FACTORY] System prompt: {len(system_prompt) if system_prompt else 0} chars"
    )

    # Create agent with tools and system prompt
    logger.debug(f"[AGENT_FACTORY] Creating Agent instance...")
    agent = Agent(model=model, tools=tools, system_prompt=system_prompt)

    logger.debug(f"[AGENT_FACTORY] Agent created successfully")
    return agent, tools


def _get_bedrock_model_config(
    bot: Optional[BotModel],
    model_name: str = "claude-v3.5-sonnet",
    enable_reasoning: bool = False,
) -> dict:
    """Get Bedrock model configuration."""
    from app.bedrock import get_model_id

    # Use provided model name (BotModel doesn't have a direct model attribute)
    # Get proper Bedrock model ID
    bedrock_region = os.environ.get("BEDROCK_REGION", "us-east-1")
    enable_cross_region = (
        os.environ.get("ENABLE_BEDROCK_CROSS_REGION_INFERENCE", "false").lower()
        == "true"
    )

    model_id = get_model_id(
        model_name,
        bedrock_region=bedrock_region,
        enable_cross_region=enable_cross_region,
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
    if enable_reasoning:
        # Import config for default values
        from app.config import DEFAULT_GENERATION_CONFIG

        # Enable thinking/reasoning functionality
        budget_tokens = DEFAULT_GENERATION_CONFIG["reasoning_params"][
            "budget_tokens"
        ]  # Use config default (1024)

        # Use bot's reasoning params if available
        if bot and bot.generation_params and bot.generation_params.reasoning_params:
            budget_tokens = bot.generation_params.reasoning_params.budget_tokens

        additional_request_fields["thinking"] = {
            "type": "enabled",
            "budget_tokens": budget_tokens,
        }
        # When thinking is enabled, temperature must be 1
        config["temperature"] = 1.0
        logger.debug(
            f"[AGENT_FACTORY] Reasoning enabled with budget_tokens: {budget_tokens}"
        )

    if additional_request_fields:
        config["additional_request_fields"] = additional_request_fields

    return config
