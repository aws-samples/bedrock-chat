import json
import logging
import os
import sys
import time
import unittest
from typing import Dict, List

from app.agents.tools.agent_tool import AgentTool, ToolRunResult
from app.strands_integration.chat_strands_v4 import (
    ToolResultCapture,
    _create_callback_handler,
    chat_with_strands,
)
from app.strands_integration.tools.calculator_v3 import calculator
from strands import Agent
from strands.models import BedrockModel

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from app.stream import OnThinking
from tests.test_repositories.utils.bot_factory import create_test_private_bot

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def on_tool_result(tool_result: ToolRunResult) -> None:
    logger.info("====================================")
    logger.info(f"Tool result captured: {tool_result}")
    logger.info("====================================")


def on_thinking(thinking: OnThinking) -> None:
    logger.info("====================================")
    logger.info(f"Thinking captured: {thinking}")
    logger.info("====================================")


def on_stream(stream: str) -> None:
    logger.info("====================================")
    logger.info(f"Stream captured: {stream}")
    logger.info("====================================")


def on_reasoning(reasoning: str) -> None:
    logger.info("====================================")
    logger.info(f"Reasoning captured: {reasoning}")
    logger.info("====================================")


class TestChatStrandsV4(unittest.TestCase):
    def setUp(self):
        self.bot = create_test_private_bot(
            id="test-bot",
            is_starred=False,
            owner_user_id="test-user",
            include_calculator_tool=True,
            include_simple_list_tool=True,
        )

    def test_capture(self):
        tool_capture = ToolResultCapture(
            on_thinking=on_thinking,
            on_tool_result=on_tool_result,
        )
        agent = Agent(
            model=BedrockModel(
                region_name="us-west-2",
                # model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                additional_request_fields={
                    "thinking": {
                        "type": "enabled",
                        "budget_tokens": 1024,
                    }
                },
            ),
            tools=[calculator],
            hooks=[tool_capture],
        )
        agent.callback_handler = _create_callback_handler(
            on_stream=on_stream,
            on_thinking=on_thinking,
            on_tool_result=on_tool_result,
            on_reasoning=on_reasoning,
        )
        result = agent("What is 2 + 2? When answer, output with the source_id")

        logger.debug(f"Agent result: {result}")


if __name__ == "__main__":
    unittest.main()
