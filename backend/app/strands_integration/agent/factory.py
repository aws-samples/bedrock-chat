"""
Agent factory for Strands integration.
"""

import logging
import os

from app.repositories.models.conversation import type_model_name
from app.repositories.models.custom_bot import BotModel, GenerationParamsModel
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.strands_integration.utils import get_strands_tools
from strands import Agent
from strands.hooks import HookProvider
from strands.models import BedrockModel

from app.strands_integration.agent.config import get_bedrock_model_config

logger = logging.getLogger(__name__)

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")


def create_strands_agent(
    bot: BotModel | None,
    instructions: list[str],
    model_name: type_model_name,
    generation_params: GenerationParamsModel | None = None,
    guardrail: BedrockGuardrailsModel | None = None,
    enable_reasoning: bool = False,
    prompt_caching_enabled: bool = False,
    has_tools: bool = False,
    hooks: list[HookProvider] | None = None,
) -> Agent:
    model_config = get_bedrock_model_config(
        model_name=model_name,
        instructions=instructions,
        generation_params=generation_params,
        guardrail=guardrail,
        enable_reasoning=enable_reasoning,
        prompt_caching_enabled=prompt_caching_enabled,
        has_tools=has_tools,
    )
    logger.debug(f"[AGENT_FACTORY] Model config: {model_config}")
    model = BedrockModel(
        region_name=BEDROCK_REGION,
        **model_config,
    )

    # Strands does not support list of instructions, so we join them into a single string.
    system_prompt = "\n\n".join(instructions).strip() if instructions else None

    agent = Agent(
        model=model,
        tools=get_strands_tools(bot, model_name),  # type: ignore
        hooks=hooks or [],
        system_prompt=system_prompt,
    )
    return agent
