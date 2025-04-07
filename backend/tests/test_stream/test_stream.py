import base64
import os
import sys

os.environ["REGION"] = "us-west-2"
os.environ["BEDROCK_REGION"] = "us-west-2"
os.environ["ENABLE_BEDROCK_CROSS_REGION_INFERENCE"] = "true"
sys.path.append(".")

import unittest
from pprint import pprint

import boto3
from app.repositories.models.conversation import (
    AttachmentContentModel,
    ImageContentModel,
    MessageModel,
    TextContentModel,
)
from app.repositories.models.custom_bot import (
    GenerationParamsModel,
    ReasoningParamsModel,
)
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.stream import ConverseApiStreamHandler, OnStopInput
from get_aws_logo import get_aws_logo, get_cdk_logo
from get_pdf import get_aws_overview, get_test_markdown
from ulid import ULID


def on_stream(x: str) -> None:
    print(f"Stream: {x}")


def on_stop(x: OnStopInput) -> None:
    print(f"Stop reason: {x['stop_reason']}")
    print(f"Price: {x['price']}")
    print(f"Input token count: {x['input_token_count']}")
    print(f"Output token count: {x['output_token_count']}")
    pprint(x["message"])


def on_reasoning(x: str) -> None:
    print(f"Reasoning: {x}")


class TestConverseApiStreamHandler(unittest.TestCase):
    # MODEL = "claude-v3.5-haiku"
    MODEL = "claude-v3.5-sonnet"
    MODEL_REASONING = "claude-v3.7-sonnet"

    def _run(
        self,
        message,
        instructions=[],
        generation_params=None,
        guardrail=None,
        reasoning=False,
    ):
        self.stream_handler = ConverseApiStreamHandler(
            model=self.MODEL if not reasoning else self.MODEL_REASONING,
            instructions=instructions,
            generation_params=generation_params,
            guardrail=guardrail,
            on_stream=on_stream,
            on_reasoning=on_reasoning,
        )
        result = self.stream_handler.run(
            messages=[message],
        )
        on_stop(result)

    def test_run(self):
        message = MessageModel(
            role="user",
            content=[
                TextContentModel(
                    content_type="text",
                    body="Hello, World!",
                )
            ],
            model=self.MODEL,
            children=[],
            parent=None,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )
        self._run(message)

    def test_run_with_reasoning(self):
        message = MessageModel(
            role="user",
            content=[
                TextContentModel(
                    content_type="text",
                    body="「本日のお買い得品はこれさ。」「山がアリ地獄になったとき、新しい山は高くなっていく。全てはガラスの向こうの出来事」「何かが分かったら、更に半額で売ってあげるよ。ひらがな5文字で答えられるかな。」",
                )
            ],
            model=self.MODEL,
            children=[],
            parent=None,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )
        self._run(
            message,
            generation_params=GenerationParamsModel(
                max_tokens=2000,
                top_k=50,
                top_p=0.999,
                temperature=0.6,
                stop_sequences=["Human: ", "Assistant: "],
                reasoning_params=ReasoningParamsModel(
                    budget_tokens=1024,
                ),
            ),
            reasoning=True,
        )

    def test_run_with_instruction(self):
        message = MessageModel(
            role="user",
            content=[
                TextContentModel(
                    content_type="text",
                    body="Hello!",
                )
            ],
            model=self.MODEL,
            children=[],
            parent=None,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )

        instruction = "いかなる状況でも、大阪弁で回答してください"
        self._run(message, instruction)

    def test_run_with_generation_params(self):
        message = MessageModel(
            role="user",
            content=[
                TextContentModel(
                    content_type="text",
                    body="Hello!",
                )
            ],
            model=self.MODEL,
            children=[],
            parent=None,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )

        generation_params = GenerationParamsModel(
            max_tokens=2000,
            top_k=50,
            top_p=0.999,
            temperature=0.6,
            stop_sequences=["Human: ", "Assistant: "],
            reasoning_params=ReasoningParamsModel(
                budget_tokens=1024,
            ),
        )
        self._run(message, generation_params=generation_params)

    def test_run_with_image(self):
        message = MessageModel(
            role="user",
            content=[
                ImageContentModel(
                    content_type="image",
                    media_type="image/png",
                    body=get_aws_logo(),
                ),
                ImageContentModel(
                    content_type="image",
                    media_type="image/png",
                    body=get_cdk_logo(),
                ),
                TextContentModel(
                    content_type="text",
                    body="Explain the images.",
                ),
            ],
            model=self.MODEL,
            children=[],
            parent=None,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )
        self._run(message)

    def test_run_with_attachment(self):
        file_name, body = get_aws_overview()

        message = MessageModel(
            role="user",
            content=[
                AttachmentContentModel(
                    content_type="attachment",
                    body=body,
                    file_name=file_name,
                ),
                TextContentModel(
                    content_type="text",
                    body="要約して",
                ),
            ],
            model=self.MODEL,
            children=[],
            parent=None,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )
        self._run(message)


class TestConverseApiStreamHandlerGuardrail(unittest.TestCase):
    MODEL = "claude-v3.5-haiku"

    def setUp(self) -> None:
        # Note that the region must be the same as the one used in the bedrock client
        # https://github.com/aws/aws-sdk-js-v3/issues/6482
        self.bedrock_client = boto3.client("bedrock", region_name="us-east-1")
        self.guardrail_name = f"test-guardrail-{ULID()}"

        # Create dummy guardrail
        guardrail_res = self.bedrock_client.create_guardrail(
            name=self.guardrail_name,
            description="Test guardrail for unit tests",
            contentPolicyConfig={
                "filtersConfig": [
                    {"type": "SEXUAL", "inputStrength": "LOW", "outputStrength": "LOW"},
                ]
            },
            blockedInputMessaging="blocked",
            blockedOutputsMessaging="blocked",
        )

        self.guardrail_arn = guardrail_res["guardrailArn"]

    def tearDown(self):
        print("Cleaning up...")
        # Delete dummy guardrail
        try:
            self.bedrock_client.delete_guardrail(guardrailIdentifier=self.guardrail_arn)

        except Exception as e:
            print(f"Error deleting guardrail: {e}")

    def _run(self, message, instructions=[], generation_params=None, guardrail=None):
        self.stream_handler = ConverseApiStreamHandler(
            model=self.MODEL,
            instructions=instructions,
            generation_params=generation_params,
            guardrail=guardrail,
            on_stream=on_stream,
        )
        result = self.stream_handler.run(
            messages=[message],
        )
        on_stop(result)

    def test_run_with_guardrail(self):
        message = MessageModel(
            role="user",
            content=[
                TextContentModel(
                    content_type="text",
                    body="Hello, World!",
                )
            ],
            model=self.MODEL,
            children=[],
            parent=None,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )
        guardrail = BedrockGuardrailsModel(
            is_guardrail_enabled=True,
            hate_threshold=0,
            insults_threshold=0,
            sexual_threshold=1,
            violence_threshold=0,
            misconduct_threshold=0,
            grounding_threshold=0,
            relevance_threshold=0,
            guardrail_arn=self.guardrail_arn,
            guardrail_version="DRAFT",
        )
        self._run(message, guardrail=guardrail)


if __name__ == "__main__":
    unittest.main()
