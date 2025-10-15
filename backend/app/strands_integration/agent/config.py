"""
Agent configuration utilities for Strands integration.
"""

import logging

from app.bedrock import (
    get_model_id,
    generation_params_to_converse_configuration,
    is_prompt_caching_supported,
)
from app.repositories.models.conversation import type_model_name
from app.repositories.models.custom_bot import GenerationParamsModel
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel

from strands.models import BedrockModel

logger = logging.getLogger(__name__)


def get_bedrock_model_config(
    model_name: type_model_name = "claude-v3.5-sonnet",
    instructions: list[str] = [],
    generation_params: GenerationParamsModel | None = None,
    guardrail: BedrockGuardrailsModel | None = None,
    enable_reasoning: bool = False,
    prompt_caching_enabled: bool = False,
    has_tools: bool = False,
) -> BedrockModel.BedrockConfig:
    """Get Bedrock model configuration."""

    model_id = get_model_id(model_name)

    config: BedrockModel.BedrockConfig = {
        "model_id": model_id,
    }

    # Prepare model-specific parameters
    converse_config = generation_params_to_converse_configuration(
        model=model_name,
        generation_params=generation_params,
        guardrail=guardrail,
        enable_reasoning=enable_reasoning,
    )

    # Add model parameters if available
    inference_config = converse_config["inferenceConfig"]
    if "temperature" in inference_config:
        config["temperature"] = inference_config["temperature"]

    if "topP" in inference_config:
        config["top_p"] = inference_config["topP"]

    if "maxTokens" in inference_config:
        config["max_tokens"] = inference_config["maxTokens"]

    if "stopSequences" in inference_config:
        config["stop_sequences"] = inference_config["stopSequences"]

    # Add Guardrails configuration (Strands way)
    if "guardrailConfig" in converse_config:
        guardrail_config = converse_config["guardrailConfig"]
        config["guardrail_id"] = guardrail_config["guardrailIdentifier"]
        config["guardrail_version"] = guardrail_config["guardrailVersion"]

        if "trace" in guardrail_config:
            config["guardrail_trace"] = guardrail_config["trace"]

        if "streamProcessingMode" in guardrail_config:
            config["guardrail_stream_processing_mode"] = guardrail_config[
                "streamProcessingMode"
            ]

        logger.info(f"Enabled Guardrails: {guardrail_config["guardrailIdentifier"]}")

    # Add prompt caching configuration
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

    if "additionalModelRequestFields" in converse_config:
        config["additional_request_fields"] = converse_config[
            "additionalModelRequestFields"
        ]

    return config
