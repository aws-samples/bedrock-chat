"""
Telemetry manager for Strands integration.
"""

import logging

from app.strands_integration.telemetry.processors import ReasoningSpanProcessor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from strands.telemetry import StrandsTelemetry

logger = logging.getLogger(__name__)


class StrandsTelemetryManager:
    """Manages Strands telemetry setup and span processors."""

    def __init__(self):
        self.telemetry = StrandsTelemetry()
        self.reasoning_processor = ReasoningSpanProcessor()

    def setup(self, conversation_id: str, user_id: str):
        """Setup telemetry with custom span processors."""
        # Get the tracer provider and add our custom processors
        tracer_provider = trace.get_tracer_provider()
        if isinstance(tracer_provider, TracerProvider):
            tracer_provider.add_span_processor(self.reasoning_processor)
            logger.debug("Added custom span processors to tracer provider")

        self.reasoning_processor.set_context(conversation_id, user_id)
