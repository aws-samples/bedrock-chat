from typing_extensions import NotRequired, TypedDict


class GenerationParams(TypedDict):
    max_tokens: int
    top_k: NotRequired[int]
    top_p: float
    temperature: float
    stop_sequences: list[str]
    reasoning_params: NotRequired[dict[str, int]]


class EmbeddingConfig(TypedDict):
    model_id: str
    chunk_size: int
    chunk_overlap: int
    enable_partition_pdf: bool


# Configure generation parameter for Claude chat response.
# Adjust the values according to your application.
# See: https://docs.anthropic.com/claude/reference/complete_post
DEFAULT_GENERATION_CONFIG: GenerationParams = {
    # Minimum (Haiku) is 4096
    # Ref: https://docs.anthropic.com/en/docs/about-claude/models/all-models#model-comparison
    "max_tokens": 4096,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 1.0,
    "stop_sequences": [],
    # Budget tokens must NOT exceeds max_tokens
    "reasoning_params": {"budget_tokens": 1024},
}

# Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-mistral.html#model-parameters-mistral-request-response
DEFAULT_MISTRAL_GENERATION_CONFIG: GenerationParams = {
    "max_tokens": 4096,
    "top_k": 250,
    "top_p": 0.9,
    "temperature": 0.5,
    "stop_sequences": ["[INST]", "[/INST]"],
}

# Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-deepseek.html
DEFAULT_DEEP_SEEK_GENERATION_CONFIG: GenerationParams = {
    "max_tokens": 4096,
    "top_p": 0.9,
    "temperature": 1.0,
    "stop_sequences": [],
}

# Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta.html
DEFAULT_LLAMA_GENERATION_CONFIG: GenerationParams = {
    "max_tokens": 2048,
    "top_p": 0.9,
    "temperature": 0.7,
    "stop_sequences": [],
}


# Used for price estimation, in USD per 1,000 tokens.
# Models without an entry here are priced from the llm-prices package
# (https://github.com/Mattbusel/llm-prices), which carries the us-east-1 on-demand
# prices from the AWS Price List API and the Anthropic list prices that Bedrock
# charges for Claude. See `calculate_price` in app/bedrock.py.
# "default" holds models llm-prices has no row for; a region entry overrides
# "default" and llm-prices for that region.
# See: https://aws.amazon.com/bedrock/pricing/
BEDROCK_PRICING = {
    "default": {
        "claude-v3-haiku": {"input": 0.00025, "output": 0.00125},
        "claude-v3.5-sonnet": {
            "input": 0.00300,
            "output": 0.01500,
            "cache_write_input": 0.00375,
            "cache_read_input": 0.0003,
        },
        "claude-v3.5-sonnet-v2": {
            "input": 0.00300,
            "output": 0.01500,
            "cache_write_input": 0.00375,
            "cache_read_input": 0.0003,
        },
        "claude-v3.7-sonnet": {
            "input": 0.00300,
            "output": 0.01500,
            "cache_write_input": 0.00375,
            "cache_read_input": 0.0003,
        },
        "claude-v3-opus": {"input": 0.01500, "output": 0.07500},
        "mistral-large-2": {"input": 0.002, "output": 0.006},
    },
    # EU regions (eu-central-1, eu-west-1, eu-west-3)
    "eu-central-1": {
        "llama3-2-1b-instruct": {"input": 0.00013, "output": 0.00013},
        "llama3-2-3b-instruct": {"input": 0.00019, "output": 0.00019},
    },
    "eu-west-1": {
        "llama3-2-1b-instruct": {"input": 0.00013, "output": 0.00013},
        "llama3-2-3b-instruct": {"input": 0.00019, "output": 0.00019},
    },
    "eu-west-3": {
        "llama3-2-1b-instruct": {"input": 0.00013, "output": 0.00013},
        "llama3-2-3b-instruct": {"input": 0.00019, "output": 0.00019},
    },
}
