from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, TypeGuard

from app.config import BEDROCK_PRICING
from app.config import DEFAULT_GENERATION_CONFIG as DEFAULT_CLAUDE_GENERATION_CONFIG
from app.config import DEFAULT_MISTRAL_GENERATION_CONFIG
from app.repositories.models.custom_bot import GenerationParamsModel
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.routes.schemas.conversation import type_model_name
from app.utils import get_bedrock_runtime_client
from botocore.exceptions import ClientError
from retry import retry

if TYPE_CHECKING:
    from app.agents.tools.agent_tool import AgentTool
    from app.repositories.models.conversation import ContentModel, SimpleMessageModel
    from mypy_boto3_bedrock_runtime.literals import ConversationRoleType
    from mypy_boto3_bedrock_runtime.type_defs import (
        ContentBlockTypeDef,
        ConverseResponseTypeDef,
        ConverseStreamRequestTypeDef,
        GuardrailConverseContentBlockTypeDef,
        InferenceConfigurationTypeDef,
        MessageTypeDef,
        SystemContentBlockTypeDef,
    )


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")
ENABLE_MISTRAL = os.environ.get("ENABLE_MISTRAL", "false") == "true"
DEFAULT_GENERATION_CONFIG = (
    DEFAULT_MISTRAL_GENERATION_CONFIG
    if ENABLE_MISTRAL
    else DEFAULT_CLAUDE_GENERATION_CONFIG
)
ENABLE_BEDROCK_CROSS_REGION_INFERENCE = (
    os.environ.get("ENABLE_BEDROCK_CROSS_REGION_INFERENCE", "false") == "true"
)

client = get_bedrock_runtime_client()


class BedrockThrottlingException(Exception): ...


def _is_conversation_role(role: str) -> TypeGuard[ConversationRoleType]:
    return role in ["user", "assistant"]


def is_nova_model(model: type_model_name) -> bool:
    """Check if the model is an Amazon Nova model"""
    return model in ["amazon-nova-pro", "amazon-nova-lite", "amazon-nova-micro"]


def _prepare_nova_model_params(
    model: type_model_name, generation_params: Optional[GenerationParamsModel] = None
) -> Tuple[InferenceConfigurationTypeDef, Dict[str, Any]]:
    """
    Prepare inference configuration and additional model request fields for Nova models
    > Note that Amazon Nova expects inference parameters as a JSON object under a inferenceConfig attribute. Amazon Nova also has an additional parameter "topK" that can be passed as an additional inference parameters. This parameter follows the same structure and is passed through the additionalModelRequestFields, as shown below.
    https://docs.aws.amazon.com/nova/latest/userguide/getting-started-converse.html
    """
    # Base inference configuration
    inference_config: InferenceConfigurationTypeDef = {
        "maxTokens": (
            generation_params.max_tokens
            if generation_params
            else DEFAULT_GENERATION_CONFIG["max_tokens"]
        ),
        "temperature": (
            generation_params.temperature
            if generation_params
            else DEFAULT_GENERATION_CONFIG["temperature"]
        ),
        "topP": (
            generation_params.top_p
            if generation_params
            else DEFAULT_GENERATION_CONFIG["top_p"]
        ),
    }

    # Additional model request fields specific to Nova models
    additional_fields: Dict[str, Any] = {"inferenceConfig": {}}

    # Add top_k if specified in generation params
    if generation_params and generation_params.top_k is not None:
        top_k = generation_params.top_k
        if top_k > 128:
            logger.warning(
                "In Amazon Nova, an 'unexpected error' occurs if topK exceeds 128. To avoid errors, the upper limit of A is set to 128."
            )
            top_k = 128

        additional_fields["inferenceConfig"]["topK"] = top_k

    return inference_config, additional_fields


def compose_args_for_converse_api(
    messages: list[SimpleMessageModel],
    model: type_model_name,
    instructions: list[str] = [],
    generation_params: GenerationParamsModel | None = None,
    guardrail: BedrockGuardrailsModel | None = None,
    grounding_source: GuardrailConverseContentBlockTypeDef | None = None,
    tools: dict[str, AgentTool] | None = None,
    stream: bool = True,
    enable_reasoning: bool = False,
) -> ConverseStreamRequestTypeDef:
    def process_content(c: ContentModel, role: str) -> list[ContentBlockTypeDef]:
        if c.content_type == "text":
            if (
                role == "user"
                and guardrail
                and guardrail.grounding_threshold > 0
                and grounding_source
            ):
                return [
                    {"guardContent": grounding_source},
                    {
                        "guardContent": {
                            "text": {"text": c.body, "qualifiers": ["query"]}
                        }
                    },
                ]

        return c.to_contents_for_converse()

    arg_messages: list[MessageTypeDef] = [
        {
            "role": message.role,
            "content": [
                block
                for c in message.content
                for block in process_content(c, message.role)
            ],
        }
        for message in messages
        if _is_conversation_role(message.role)
    ]

    # Prepare model-specific parameters
    inference_config: InferenceConfigurationTypeDef
    additional_model_request_fields: dict[str, Any]
    system_prompts: list[SystemContentBlockTypeDef]

    if is_nova_model(model):
        # Special handling for Nova models
        inference_config, additional_model_request_fields = _prepare_nova_model_params(
            model, generation_params
        )
        system_prompts = (
            [
                {
                    "text": "\n\n".join(instructions),
                }
            ]
            if len(instructions) > 0
            else []
        )

    else:
        # Standard handling for non-Nova models
        if enable_reasoning:
            budget_tokens = (
                generation_params.reasoning_params.budget_tokens
                if generation_params and generation_params.reasoning_params
                else DEFAULT_GENERATION_CONFIG["reasoning_params"]["budget_tokens"]  # type: ignore
            )
            max_tokens = (
                generation_params.max_tokens
                if generation_params
                else DEFAULT_GENERATION_CONFIG["max_tokens"]
            )

            if max_tokens <= budget_tokens:
                logger.warning(
                    f"max_tokens ({max_tokens}) must be greater than budget_tokens ({budget_tokens}). "
                    f"Setting max_tokens to {budget_tokens + 1024}"
                )
                max_tokens = budget_tokens + 1024

            inference_config = {
                "maxTokens": max_tokens,
                "temperature": 1.0,  # Force temperature to 1.0 when reasoning is enabled
                "topP": (
                    generation_params.top_p
                    if generation_params
                    else DEFAULT_GENERATION_CONFIG["top_p"]
                ),
                "stopSequences": (
                    generation_params.stop_sequences
                    if generation_params
                    else DEFAULT_GENERATION_CONFIG.get("stop_sequences", [])
                ),
            }
            additional_model_request_fields = {
                # top_k cannot be used with reasoning
                "thinking": {
                    "type": "enabled",
                    "budget_tokens": budget_tokens,
                },
            }
        else:
            inference_config = {
                "maxTokens": (
                    generation_params.max_tokens
                    if generation_params
                    else DEFAULT_GENERATION_CONFIG["max_tokens"]
                ),
                "temperature": (
                    generation_params.temperature
                    if generation_params
                    else DEFAULT_GENERATION_CONFIG["temperature"]
                ),
                "topP": (
                    generation_params.top_p
                    if generation_params
                    else DEFAULT_GENERATION_CONFIG["top_p"]
                ),
                "stopSequences": (
                    generation_params.stop_sequences
                    if generation_params
                    else DEFAULT_GENERATION_CONFIG.get("stop_sequences", [])
                ),
            }
            additional_model_request_fields = {
                "top_k": (
                    generation_params.top_k
                    if generation_params
                    else DEFAULT_GENERATION_CONFIG["top_k"]
                ),
            }
        system_prompts = [
            {
                "text": instruction,
            }
            for instruction in instructions
            if len(instruction) > 0
        ]

    # Construct the base arguments
    args: ConverseStreamRequestTypeDef = {
        "inferenceConfig": inference_config,
        "modelId": get_model_id(model),
        "messages": arg_messages,
        "system": system_prompts,
        "additionalModelRequestFields": additional_model_request_fields,
    }

    if guardrail and guardrail.guardrail_arn and guardrail.guardrail_version:
        args["guardrailConfig"] = {
            "guardrailIdentifier": guardrail.guardrail_arn,
            "guardrailVersion": guardrail.guardrail_version,
            "trace": "enabled",
        }

        if stream:
            # https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-streaming.html
            args["guardrailConfig"]["streamProcessingMode"] = "async"

    if tools:
        args["toolConfig"] = {
            "tools": [
                {
                    "toolSpec": tool.to_converse_spec(),
                }
                for tool in tools.values()
            ],
        }

    return args


@retry(
    exceptions=(BedrockThrottlingException,),
    tries=3,
    delay=60,
    backoff=2,
    jitter=(0, 2),
    logger=logger,
)
def call_converse_api(
    args: ConverseStreamRequestTypeDef,
) -> ConverseResponseTypeDef:
    client = get_bedrock_runtime_client()
    try:
        return client.converse(**args)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ThrottlingException":
            raise BedrockThrottlingException(
                "Bedrock API is throttling requests"
            ) from e
        raise


def calculate_price(
    model: type_model_name,
    input_tokens: int,
    output_tokens: int,
    region: str = BEDROCK_REGION,
) -> float:
    input_price = (
        BEDROCK_PRICING.get(region, {})
        .get(model, {})
        .get("input", BEDROCK_PRICING["default"][model]["input"])
    )
    output_price = (
        BEDROCK_PRICING.get(region, {})
        .get(model, {})
        .get("output", BEDROCK_PRICING["default"][model]["output"])
    )

    return input_price * input_tokens / 1000.0 + output_price * output_tokens / 1000.0


def get_model_id(
    model: type_model_name,
    enable_cross_region: bool = ENABLE_BEDROCK_CROSS_REGION_INFERENCE,
    bedrock_region: str = BEDROCK_REGION,
) -> str:
    # Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html
    base_model_ids = {
        "claude-v2": "anthropic.claude-v2:1",
        "claude-instant-v1": "anthropic.claude-instant-v1",
        "claude-v3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
        "claude-v3-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
        "claude-v3-opus": "anthropic.claude-3-opus-20240229-v1:0",
        "claude-v3.5-sonnet": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "claude-v3.5-sonnet-v2": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "claude-v3.7-sonnet": "anthropic.claude-3-7-sonnet-20250219-v1:0",
        "claude-v3.5-haiku": "anthropic.claude-3-5-haiku-20241022-v1:0",
        "mistral-7b-instruct": "mistral.mistral-7b-instruct-v0:2",
        "mixtral-8x7b-instruct": "mistral.mixtral-8x7b-instruct-v0:1",
        "mistral-large": "mistral.mistral-large-2402-v1:0",
        # New Amazon Nova models
        "amazon-nova-pro": "amazon.nova-pro-v1:0",
        "amazon-nova-lite": "amazon.nova-lite-v1:0",
        "amazon-nova-micro": "amazon.nova-micro-v1:0",
        # Llama Model
        "llama-3-2-1b-instruct": "meta.llama3-2-1b-instruct-v1:0",
        "llama-3-2-11b-instruct": "meta.llama3-2-11b-instruct-v1:0",
        "llama-3-3-70b-instruct": "meta.llama3-3-70b-instruct-v1:0",

    }

    # Made this list by scripts/cross_region_inference/get_supported_cross_region_inferences.py
    # Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference-support.html
    supported_regions = {
        "us-east-1": {
            "area": "us",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-opus",
                "claude-v3-sonnet",
                "claude-v3.5-haiku",
                "claude-v3.5-sonnet",
                "claude-v3.5-sonnet-v2",
                "claude-v3.7-sonnet",
                "llama-3-2-1b-instruct",
                "llama-3-2-11b-instruct",
                "llama-3-3-70b-instruct",
            ],
        },
        "us-east-2": {
            "area": "us",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3.5-haiku",
                "claude-v3.5-sonnet",
                "claude-v3.5-sonnet-v2",
                "claude-v3.7-sonnet",
                "llama-3-2-1b-instruct",
                "llama-3-2-11b-instruct"
                "llama-3-3-70b-instruct",
            ],
        },
        "us-west-2": {
            "area": "us",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-opus",
                "claude-v3-sonnet",
                "claude-v3.5-haiku",
                "claude-v3.5-sonnet",
                "claude-v3.5-sonnet-v2",
                "claude-v3.7-sonnet",
                "llama-3-2-1b-instruct",
                "llama-3-2-11b-instruct",
                "llama-3-3-70b-instruct",
            ],
        },
        "eu-central-1": {
            "area": "eu",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-sonnet",
                "claude-v3.5-sonnet",
                "llama-3-2-1b-instruct",
            ],
        },
        "eu-west-1": {
            "area": "eu",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-sonnet",
                "claude-v3.5-sonnet",
                "llama-3-2-1b-instruct",
            ],
        },
        "eu-west-2": {"area": "eu", "models": []},
        "eu-west-3": {
            "area": "eu",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-sonnet",
                "claude-v3.5-sonnet",
                "llama-3-2-1b-instruct",
            ],
        },
        "eu-north-1": {
            "area": "eu",
            "models": ["amazon-nova-lite", "amazon-nova-micro", "amazon-nova-pro"],
        },
        "ap-south-1": {
            "area": "apac",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-sonnet",
                "claude-v3.5-sonnet",
                "claude-v3.5-sonnet-v2",
            ],
        },
        "ap-northeast-1": {
            "area": "apac",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-sonnet",
                "claude-v3.5-sonnet",
                "claude-v3.5-sonnet-v2",
            ],
        },
        "ap-northeast-2": {
            "area": "apac",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-sonnet",
                "claude-v3.5-sonnet",
                "claude-v3.5-sonnet-v2",
            ],
        },
        "ap-northeast-3": {"area": "apac", "models": ["claude-v3.5-sonnet-v2"]},
        "ap-southeast-1": {
            "area": "apac",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-sonnet",
                "claude-v3.5-sonnet",
                "claude-v3.5-sonnet-v2",
            ],
        },
        "ap-southeast-2": {
            "area": "apac",
            "models": [
                "amazon-nova-lite",
                "amazon-nova-micro",
                "amazon-nova-pro",
                "claude-v3-haiku",
                "claude-v3-sonnet",
                "claude-v3.5-sonnet",
                "claude-v3.5-sonnet-v2",
            ],
        },
    }

    base_model_id = base_model_ids.get(model)
    if not base_model_id:
        raise ValueError(f"Unsupported model: {model}")

    model_id = base_model_id

    if enable_cross_region:
        if (
            bedrock_region in supported_regions
            and model in supported_regions[bedrock_region]["models"]
        ):
            region_prefix = supported_regions[bedrock_region]["area"]
            model_id = f"{region_prefix}.{base_model_id}"
            logger.info(
                f"Using cross-region model ID: {model_id} for model '{model}' in region '{BEDROCK_REGION}'"
            )
        else:
            logger.warning(
                f"Region '{bedrock_region}' does not support cross-region inference for model '{model}'."
            )
    else:
        logger.info(f"Using local model ID: {model_id} for model '{model}'")

    return model_id
