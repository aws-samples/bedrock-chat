"""
Agent configuration utilities for Strands integration.
"""
import logging
import os

from app.bedrock import get_model_id, is_prompt_caching_supported
from app.repositories.models.conversation import type_model_name
from app.repositories.models.custom_bot import BotModel

logger = logging.getLogger(__name__)

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")


def get_bedrock_model_config(
    bot: BotModel | None,
    model_name: type_model_name = "claude-v3.5-sonnet",
    enable_reasoning: bool = False,
    instructions: list[str] = [],
) -> dict:
    """Get Bedrock model configuration."""
    model_id = get_model_id(model_name)

    config = {
        "model_id": model_id,
        "region_name": BEDROCK_REGION,
    }

    # Add model parameters if available
    if bot and bot.generation_params:
        if bot.generation_params.temperature is not None:
            config["temperature"] = bot.generation_params.temperature  # type: ignore
        if bot.generation_params.top_p is not None:
            config["top_p"] = bot.generation_params.top_p  # type: ignore
        if bot.generation_params.max_tokens is not None:
            config["max_tokens"] = bot.generation_params.max_tokens  # type: ignore

    # Add Guardrails configuration (Strands way)
    if bot and bot.bedrock_guardrails:
        guardrails = bot.bedrock_guardrails
        config["guardrail_id"] = guardrails.guardrail_arn
        config["guardrail_version"] = guardrails.guardrail_version
        config["guardrail_trace"] = "enabled"  # Enable trace for debugging
        logger.info(f"Enabled Guardrails: {guardrails.guardrail_arn}")

    # Add prompt caching configuration
    prompt_caching_enabled = bot.prompt_caching_enabled if bot is not None else True
    has_tools = bot is not None and bot.is_agent_enabled()
    if prompt_caching_enabled and not (
        has_tools and not is_prompt_caching_supported(model_name, target="tool")
    ):
        # Only enable system prompt caching if there are instructions
        if is_prompt_caching_supported(model_name, "system") and len(instructions) > 0:
            config["cache_prompt"] = "default"
            logger.debug(f"Enabled system prompt caching for model {model_name}")

        # Only enable tool caching if model supports it and tools are available
        if is_prompt_caching_supported(model_name, target="tool") and has_tools:
            config["cache_tools"] = "default"
            logger.debug(f"Enabled tool caching for model {model_name}")
    else:
        logger.info(
            f"Prompt caching disabled for model {model_name} (enabled={prompt_caching_enabled}, has_tools={has_tools})"
        )

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
        config["temperature"] = 1.0  # type: ignore
        logger.debug(
            f"[AGENT_FACTORY] Reasoning enabled with budget_tokens: {budget_tokens}"
        )

    if additional_request_fields:
        config["additional_request_fields"] = additional_request_fields  # type: ignore

    return config
