"""
Cost calculation utilities for Strands integration.
"""

import logging
from typing import cast

from app.bedrock import calculate_price
from app.repositories.models.conversation import type_model_name
from strands.telemetry.metrics import EventLoopMetrics

logger = logging.getLogger(__name__)


def calculate_conversation_cost(
    metrics: EventLoopMetrics, model_name: type_model_name
) -> float:
    """Calculate conversation cost from AgentResult metrics."""
    # Extract token usage from metrics
    input_tokens = metrics.accumulated_usage.get("inputTokens", 0)
    output_tokens = metrics.accumulated_usage.get("outputTokens", 0)

    # Cache token metrics are not yet supported in strands-agents 1.3.0
    # See: https://github.com/strands-agents/sdk-python/pull/641
    # This will be supported in future versions based on the issue discussion / PR
    cache_read_input_tokens = metrics.accumulated_usage.get("cacheReadInputTokens", 0)
    cache_write_input_tokens = metrics.accumulated_usage.get("cacheWriteInputTokens", 0)

    # Calculate price using the same function as chat_legacy
    price = calculate_price(
        model=model_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_read_input_tokens=cast(int, cache_read_input_tokens),
        cache_write_input_tokens=cast(int, cache_write_input_tokens),
    )

    logger.info(
        f"Token usage: input={input_tokens}, output={output_tokens}, price={price}"
    )

    # Only warn if caching might be active but tokens are zero (indicating strands limitation)
    if cache_read_input_tokens == 0 and cache_write_input_tokens == 0:
        logger.debug(
            "Cache tokens are zero - may be due to strands not yet supporting cache token metrics (see https://github.com/strands-agents/sdk-python/issues/529)"
        )

    return price
