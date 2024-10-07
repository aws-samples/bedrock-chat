import base64
import sys

sys.path.append(".")

import unittest

import boto3
from app.bedrock import compose_args_for_converse_api
from app.repositories.models.conversation import ContentModel, MessageModel
from app.repositories.models.custom_bot import GenerationParamsModel
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.stream import ConverseApiStreamHandler, OnStopInput
from get_aws_logo import get_aws_logo, get_cdk_logo
from get_pdf import get_aws_overview, get_test_markdown
from ulid import ULID


def on_stream(x: str) -> None:
    print(x)


def on_stop(x: OnStopInput) -> None:
    print(f"Stop reason: {x.stop_reason}")
    print(f"Price: {x.price}")
    print(f"Input token count: {x.input_token_count}")
    print(f"Output token count: {x.output_token_count}")


class TestConverseApiStreamHandler(unittest.TestCase):
    MODEL = "claude-v3-sonnet"
    # MODEL = "mistral-7b-instruct"

    def setUp(self) -> None:
        self.stream_handler = ConverseApiStreamHandler.from_model(model=self.MODEL)  # type: ignore
        self.stream_handler.bind(on_stream=on_stream, on_stop=on_stop)

    def _run(self, message, instruction=None, generation_params=None, guardrail=None):
        args = compose_args_for_converse_api(
            [message],
            self.MODEL,
            instruction=instruction,
            stream=True,
            generation_params=generation_params,
            grounding_source=None,
            guardrail=guardrail,
        )
        for _ in self.stream_handler.run(
            args=args,
        ):
            pass

    def test_run(self):
        message = MessageModel(
            role="user",
            content=[
                ContentModel(
                    content_type="text",
                    media_type=None,
                    body="Hello, World!",
                    file_name=None,
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
                ContentModel(
                    content_type="text",
                    media_type=None,
                    body="Hello!",
                    file_name=None,
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
                ContentModel(
                    content_type="text",
                    media_type=None,
                    body="Hello!",
                    file_name=None,
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
                ContentModel(
                    content_type="image",
                    media_type="image/png",
                    body=get_aws_logo(),
                    file_name="image.png",
                ),
                ContentModel(
                    content_type="image",
                    media_type="image/png",
                    body=get_cdk_logo(),
                    file_name=None,
                ),
                ContentModel(
                    content_type="text",
                    media_type=None,
                    body="Explain the images.",
                    file_name=None,
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
        body = base64.b64encode(body).decode("utf-8")
        # body = get_test_markdown()
        file_name = "test.md"

        message = MessageModel(
            role="user",
            content=[
                ContentModel(
                    content_type="attachment",
                    media_type=None,
                    body=body,
                    file_name=file_name,
                ),
                ContentModel(
                    content_type="text",
                    media_type=None,
                    body="要約して",
                    file_name=None,
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
        self.stream_handler = ConverseApiStreamHandler.from_model(model=self.MODEL)  # type: ignore
        self.stream_handler.bind(on_stream=on_stream, on_stop=on_stop)

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

    def _run(self, message, instruction=None, generation_params=None, guardrail=None):
        args = compose_args_for_converse_api(
            [message],
            self.MODEL,
            instruction=instruction,
            stream=True,
            generation_params=generation_params,
            grounding_source=None,
            guardrail=guardrail,
        )
        for _ in self.stream_handler.run(
            args=args,
        ):
            pass

    def test_run_with_guardrail(self):
        message = MessageModel(
            role="user",
            content=[
                ContentModel(
                    content_type="text",
                    media_type=None,
                    body="Hello, World!",
                    file_name=None,
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
