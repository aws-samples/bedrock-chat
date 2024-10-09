import logging
from typing import Any, Callable

from app.bedrock import ConverseApiRequest, calculate_price, get_model_id
from app.routes.schemas.conversation import type_model_name
from app.utils import get_bedrock_runtime_client
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OnStopInput(BaseModel):
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
        on_stream: Callable[[str], None],
        on_stop: Callable[[OnStopInput], None],
    ):
        """Base class for stream handlers.
        :param model: Model name.
        :param on_stream: Callback function for streaming.
        :param on_stop: Callback function for stopping the stream.
        """
        self.model: type_model_name = model
        self.on_stream = on_stream
        self.on_stop = on_stop

    @classmethod
    def from_model(cls, model: type_model_name):
        return ConverseApiStreamHandler(
            model=model, on_stream=lambda x: None, on_stop=lambda x: None
        )

    def bind(
        self, on_stream: Callable[[str], Any], on_stop: Callable[[OnStopInput], Any]
    ):
        self.on_stream = on_stream
        self.on_stop = on_stop
        return self

    def run(self, args: ConverseApiRequest):
        client = get_bedrock_runtime_client()
        response = None
        try:
            base_args = {
                "modelId": args["model_id"],
                "messages": args["messages"],
                "inferenceConfig": args["inference_config"],
                "system": args["system"],
                # for topK
                "additionalModelRequestFields": args["additional_model_request_fields"],
            }

            if "guardrailConfig" in args:
                base_args["guardrailConfig"] = args["guardrailConfig"]  # type: ignore

            logger.info(f"args for converse_stream: {args}")
            response = client.converse_stream(**base_args)
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e

        completions = []
        stop_reason = ""
        for event in response["stream"]:
            if "contentBlockDelta" in event:
                logger.debug(f"event: {event}")
                text = event["contentBlockDelta"]["delta"]["text"]
                completions.append(text)
                response = self.on_stream(text)
                yield response
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
                response = self.on_stop(
                    OnStopInput(
                        full_token=concatenated.rstrip(),
                        stop_reason=stop_reason,
                        input_token_count=input_token_count,
                        output_token_count=output_token_count,
                        price=price,
                    )
                )
                logger.info(f"event of converse_stream: {event}")
                yield response
