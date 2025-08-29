"""
Agent factory for Strands integration.
"""

import logging

from app.repositories.models.conversation import type_model_name
from app.repositories.models.custom_bot import BotModel
from app.strands_integration.utils import get_strands_tools
from strands import Agent
from strands.hooks import HookProvider
from strands.models import BedrockModel

from .config import get_bedrock_model_config

logger = logging.getLogger(__name__)


def create_strands_agent(
    bot: BotModel | None,
    instructions: list[str],
    model_name: type_model_name,
    enable_reasoning: bool = False,
    hooks: list[HookProvider] | None = None,
) -> Agent:
    model_config = get_bedrock_model_config(
        bot, model_name, enable_reasoning, instructions
    )
    logger.debug(f"[AGENT_FACTORY] Model config: {model_config}")
    model = BedrockModel(**model_config)

    # Strands does not support list of instructions, so we join them into a single string.
    system_prompt = "\n\n".join(instructions).strip() if instructions else None

    agent = Agent(
        model=model,
        tools=get_strands_tools(bot, model_name),  # type: ignore
        hooks=hooks or [],
        system_prompt=system_prompt,
    )
    return agent
