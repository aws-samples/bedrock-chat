from typing import Callable, Literal, Optional, no_type_check

from app.agents.tools.agent_tool import AgentTool, RunResult
from app.bedrock import (
    DEFAULT_GENERATION_CONFIG,
    ConverseApiRequest,
    ConverseApiResponse,
    ConverseApiToolConfig,
    ConverseApiToolResult,
    ConverseApiToolUseContent,
    calculate_price,
    get_bedrock_runtime_client,
    get_model_id,
)
from app.repositories.models.conversation import (
    AgentContentModel,
    AgentMessageModel,
    AgentToolResultModel,
    AgentToolUseContentModel,
    MessageModel,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from app.utils import convert_dict_keys_to_camel_case
from pydantic import BaseModel


class OnStopInput(BaseModel):
    thinking_conversation: list[AgentMessageModel]
    last_response: ConverseApiResponse
    stop_reason: str
    input_token_count: int
    output_token_count: int
    price: float


class AgentRunner:
    def __init__(
        self,
        bot: BotModel,
        tools: list[AgentTool],
        model: type_model_name,
        on_thinking: Optional[Callable[[list[AgentMessageModel]], None]] = None,
        on_tool_result: Optional[Callable[[ConverseApiToolResult], None]] = None,
        on_stop: Optional[Callable[[OnStopInput], None]] = None,
    ):
        self.bot = bot
        self.tools = {tool.name: tool for tool in tools}
        self.client = get_bedrock_runtime_client()
        self.model: type_model_name = model
        self.model_id = get_model_id(model)
        self.on_thinking = on_thinking
        self.on_tool_result = on_tool_result
        self.on_stop = on_stop
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def run(self, messages: list[MessageModel]) -> OnStopInput:
        print(f"Running agent with messages: {messages}")
        conv = [
            AgentMessageModel.from_message_model(message)
            for message in messages
            if message.role in ["user", "assistant"]
        ]
        response = self._call_converse_api(conv)

        while any(
            "toolUse" in content
            for content in response["output"]["message"]["content"][-1]
        ):
            tool_uses = [
                content["toolUse"]
                for content in response["output"]["message"]["content"]
                if "toolUse" in content
            ]

            assistant_message = AgentMessageModel(
                role="assistant",
                content=[
                    AgentContentModel(
                        content_type="toolUse",
                        body=AgentToolUseContentModel.from_tool_use_content(tool_use),
                    )
                    for tool_use in tool_uses
                ],
            )
            conv.append(assistant_message)

            if self.on_thinking:
                self.on_thinking(conv)

            tool_results = self._invoke_tools(tool_uses)

            user_message = AgentMessageModel(
                role="user",
                content=[
                    AgentContentModel(
                        content_type="toolResult",
                        body=AgentToolResultModel.from_tool_result(result),
                    )
                    for result in tool_results
                ],
            )
            conv.append(user_message)

            response = self._call_converse_api(conv)

            # Update token counts
            self.total_input_tokens += response["usage"]["inputTokens"]
            self.total_output_tokens += response["usage"]["outputTokens"]

        stop_input = OnStopInput(
            thinking_conversation=conv,
            last_response=response,
            stop_reason=response["stopReason"],
            input_token_count=self.total_input_tokens,
            output_token_count=self.total_output_tokens,
            price=calculate_price(
                self.model, self.total_input_tokens, self.total_output_tokens
            ),
        )

        if self.on_stop:
            self.on_stop(stop_input)

        return stop_input

    def _call_converse_api(
        self, messages: list[AgentMessageModel]
    ) -> ConverseApiResponse:
        args = self._compose_args(messages)

        messages = args["messages"]  # type: ignore
        inference_config = args["inference_config"]
        additional_model_request_fields = args["additional_model_request_fields"]
        model_id = args["model_id"]
        system = args["system"]
        tool_config = args["tool_config"]  # type: ignore

        return self.client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig=inference_config,
            additionalModelRequestFields=additional_model_request_fields,
            system=system,
            toolConfig=tool_config,
        )

    @no_type_check
    def _compose_args(self, messages: list[AgentMessageModel]) -> ConverseApiRequest:
        arg_messages = [
            {
                "role": message.role,
                "content": [
                    (
                        {"text": c.body}
                        if c.content_type == "text"
                        else (
                            {
                                "toolUse": {
                                    "toolUseId": c.body.tool_use_id,
                                    "name": c.body.name,
                                    "input": c.body.input,
                                }
                            }
                            if c.content_type == "toolUse"
                            else {
                                "toolResult": {
                                    "toolUseId": c.body.tool_use_id,
                                    "status": c.body.status,
                                    "content": [
                                        (
                                            {"json": c.body.content.json_}
                                            if c.body.content.json_
                                            else {"text": c.body.content.text}
                                        )
                                    ],
                                }
                            }
                        )
                    )
                    for c in message.content
                ],
            }
            for message in messages
        ]

        generation_params = self.bot.generation_params
        inference_config = {
            **DEFAULT_GENERATION_CONFIG,
            **(
                {
                    "maxTokens": generation_params.max_tokens,
                    "temperature": generation_params.temperature,
                    "topP": generation_params.top_p,
                    "stopSequences": generation_params.stop_sequences,
                }
                if generation_params
                else {}
            ),
        }

        additional_model_request_fields = {"top_k": inference_config["top_k"]}
        del inference_config["top_k"]

        args: ConverseApiRequest = {
            "inference_config": convert_dict_keys_to_camel_case(inference_config),
            "additional_model_request_fields": additional_model_request_fields,
            "model_id": self.model_id,
            "messages": arg_messages,
            "system": [],
            "tool_config": self._get_tool_config(),
        }
        if self.bot.instruction:
            args["system"] = [{"text": self.bot.instruction}]
        return args

    def _get_tool_config(self) -> ConverseApiToolConfig:
        tool_config: ConverseApiToolConfig = {
            "tools": [  # type: ignore
                {"toolSpec": tool.to_converse_spec()} for tool in self.tools.values()
            ]
        }
        return tool_config

    def _invoke_tools(
        self, tool_uses: list[ConverseApiToolUseContent]
    ) -> list[ConverseApiToolResult]:
        results = []
        for tool_use in tool_uses:
            tool_name = tool_use["name"]
            if tool_name in self.tools:
                tool = self.tools[tool_name]
                args = tool.args_schema(**tool_use["input"])
                result = tool.run(args)
                tool_result: ConverseApiToolResult = {
                    "toolUseId": tool_use["toolUseId"],
                    "content": {"text": result.body},
                }
                if not result.succeeded:
                    tool_result["status"] = "error"
                else:
                    tool_result["status"] = "success"

                if self.on_tool_result:
                    self.on_tool_result(tool_result)

                results.append(tool_result)
            else:
                raise ValueError(f"Tool {tool_name} not found.")
        return results
