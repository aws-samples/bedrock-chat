import base64
import sys

sys.path.append(".")

import unittest

import boto3
from app.repositories.models.conversation import (
    TextContentModel,
    ImageContentModel,
    AttachmentContentModel,
    MessageModel,
)
from app.repositories.models.custom_bot import GenerationParamsModel
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.stream import ConverseApiStreamHandler, OnStopInput
from get_aws_logo import get_aws_logo, get_cdk_logo
from get_pdf import get_aws_overview, get_test_markdown
from ulid import ULID


def on_stream(x: str) -> None:
    print(x)


def on_stop(x: OnStopInput) -> None:
    print(f"Stop reason: {x['stop_reason']}")
    print(f"Price: {x['price']}")
    print(f"Input token count: {x['input_token_count']}")
    print(f"Output token count: {x['output_token_count']}")


class TestConverseApiStreamHandler(unittest.TestCase):
    MODEL = "claude-v3-sonnet"
    # MODEL = "mistral-7b-instruct"

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
    MODEL = "claude-v3-sonnet"
    # MODEL = "mistral-7b-instruct"

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
