import logging
from typing import Any, Callable, TypedDict

from app.bedrock import calculate_price, get_model_id
from app.routes.schemas.conversation import type_model_name
from app.utils import get_bedrock_runtime_client
from mypy_boto3_bedrock_runtime.type_defs import (
    ConverseStreamRequestRequestTypeDef,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OnStopInput(TypedDict):
    full_token: str
    stop_reason: str
    input_token_count: int
    output_token_count: int
    price: float


class ConverseApiStreamHandler:
    """Stream handler using Converse API.
    Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
    """

    def __init__(
        self,
        model: type_model_name,
        on_stream: Callable[[str], None] | None,
    ):
        """Base class for stream handlers.
        :param model: Model name.
        :param on_stream: Callback function for streaming.
        :param on_stop: Callback function for stopping the stream.
        """
        self.model: type_model_name = model
        self.on_stream = on_stream

    @classmethod
    def from_model(cls, model: type_model_name):
        return ConverseApiStreamHandler(
            model=model, on_stream=lambda x: None,
        )

    def bind(
        self, on_stream: Callable[[str], Any],
    ):
        self.on_stream = on_stream
        return self

    def run(self, args: ConverseStreamRequestRequestTypeDef) -> OnStopInput:
        client = get_bedrock_runtime_client()
        response = None
        try:
            logger.info(f"args for converse_stream: {args}")
            response = client.converse_stream(**args)
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e

        completions = []
        stop_reason = ""
        input_token_count = 0
        output_token_count = 0
        for event in response["stream"]:
            if "contentBlockDelta" in event:
                logger.debug(f"event: {event}")
                text = event["contentBlockDelta"]["delta"]["text"]
                completions.append(text)

                if self.on_stream:
                    self.on_stream(text)

            elif "messageStop" in event:
                logger.debug(f"event: {event}")
                stop_reason = event["messageStop"]["stopReason"]

            elif "metadata" in event:
                logger.debug(f"event: {event}")
                metadata = event["metadata"]
                usage = metadata["usage"]
                input_token_count = usage["inputTokens"]
                output_token_count = usage["outputTokens"]

        price = calculate_price(
            self.model, input_token_count, output_token_count
        )
        concatenated = "".join(completions)

        result = OnStopInput(
            full_token=concatenated.rstrip(),
            stop_reason=stop_reason,
            input_token_count=input_token_count,
            output_token_count=output_token_count,
            price=price,
        )
        return result
