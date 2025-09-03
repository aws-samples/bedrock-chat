"""
Data extraction utilities for Strands telemetry.
"""

import logging

from app.repositories.models.conversation import ReasoningContentModel

from app.strands_integration.telemetry.processors import ReasoningSpanProcessor

logger = logging.getLogger(__name__)


class TelemetryDataExtractor:
    """Extracts structured data from telemetry span processors."""

    def __init__(self, reasoning_processor: ReasoningSpanProcessor):
        self.reasoning_processor = reasoning_processor

    def extract_reasoning_content(self) -> list[ReasoningContentModel]:
        """Extract reasoning content from telemetry data."""
        return self.reasoning_processor.get_reasoning_data()
