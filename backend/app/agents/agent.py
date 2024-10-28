from typing import Callable, Optional, TypedDict

from app.agents.tools.agent_tool import AgentTool
from app.bedrock import (
    DEFAULT_GENERATION_CONFIG,
    ConverseApiToolResult,
    calculate_price,
    get_bedrock_runtime_client,
    get_model_id,
    _is_conversation_role,
)
from app.repositories.models.conversation import (
    ToolUseContentModel,
    ToolUseContentModelBody,
    ToolResultContentModel,
    ToolResultContentModelBody,
    AgentMessageModel,
    MessageModel,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import JsonValue
from mypy_boto3_bedrock_runtime.type_defs import (
    ConverseRequestRequestTypeDef,
    ConverseResponseTypeDef,
    MessageTypeDef,
    ToolConfigurationTypeDef,
    ToolUseBlockOutputTypeDef,
)


class OnStopInput(TypedDict):
    thinking_conversation: list[AgentMessageModel]
    full_token: str
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
    ):
        self.bot = bot
        self.tools = {tool.name: tool for tool in tools}
        self.client = get_bedrock_runtime_client()
        self.model: type_model_name = model
        self.model_id = get_model_id(model)
        self.on_thinking = on_thinking
        self.on_tool_result = on_tool_result
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

        while "toolUse" in (
            response["output"]["message"]["content"][-1]
            if "message" in response["output"] and len(response["output"]["message"]["content"]) > 0
            else dict[str, JsonValue]()
        ):
            tool_uses: list[ToolUseBlockOutputTypeDef] = [
                content["toolUse"]
                for content in (
                    response["output"]["message"]["content"]
                    if "message" in response["output"] else []
                )
                if "toolUse" in content
            ]

            assistant_message = AgentMessageModel(
                role="assistant",
                content=[
                    ToolUseContentModel(
                        content_type="toolUse",
                        body=ToolUseContentModelBody.from_tool_use_content(tool_use),
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
                    ToolResultContentModel(
                        content_type="toolResult",
                        body=ToolResultContentModelBody.from_tool_result(result),
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
            full_token=response["output"]["message"]["content"][0]["text"] \
                if "message" in response["output"] \
                    and len(response["output"]["message"]["content"]) > 0 \
                    and "text" in response["output"]["message"]["content"][0] \
                else "",
            stop_reason=response["stopReason"],
            input_token_count=self.total_input_tokens,
            output_token_count=self.total_output_tokens,
            price=calculate_price(
                self.model, self.total_input_tokens, self.total_output_tokens
            ),
        )
        return stop_input

    def _call_converse_api(
        self, messages: list[AgentMessageModel]
    ) -> ConverseResponseTypeDef:
        args = self._compose_args(messages)
        return self.client.converse(**args)

    def _compose_args(self, messages: list[AgentMessageModel]) -> ConverseRequestRequestTypeDef:
        arg_messages: list[MessageTypeDef] = [
            {
                "role": message.role,
                "content": [
                    content
                    for c in message.content
                    for content in c.to_contents_for_converse()
                ],
            }
            for message in messages
            if _is_conversation_role(message.role)
        ]

        generation_params = self.bot.generation_params
        inference_config = {
            **DEFAULT_GENERATION_CONFIG,
            **(
                {
                    "max_tokens": generation_params.max_tokens,
                    "temperature": generation_params.temperature,
                    "top_p": generation_params.top_p,
                    "stop_sequences": generation_params.stop_sequences,
                }
                if generation_params
                else {}
            ),
        }

        additional_model_request_fields = {"top_k": inference_config["top_k"]}
        del inference_config["top_k"]

        args: ConverseRequestRequestTypeDef = {
            "inferenceConfig": {
                'maxTokens': inference_config['max_tokens'],
                'temperature': inference_config['temperature'],
                'topP': inference_config['top_p'],
                'stopSequences': inference_config['stop_sequences'],
            },
            "additionalModelRequestFields": additional_model_request_fields,
            "modelId": self.model_id,
            "messages": arg_messages,
            "system": [],
            "toolConfig": self._get_tool_config(),
        }
        if self.bot.instruction:
            args["system"] = [{"text": self.bot.instruction}]
        return args

    def _get_tool_config(self) -> ToolConfigurationTypeDef:
        tool_config: ToolConfigurationTypeDef = {
            "tools": [
                {"toolSpec": tool.to_converse_spec()} for tool in self.tools.values()
            ]
        }
        return tool_config

    def _invoke_tools(
        self, tool_uses: list[ToolUseBlockOutputTypeDef]
    ) -> list[ConverseApiToolResult]:
        results: list[ConverseApiToolResult] = []
        for tool_use in tool_uses:
            tool_name = tool_use["name"]
            if tool_name in self.tools:
                tool = self.tools[tool_name]
                args = tool.args_schema(**tool_use["input"])
                result = tool.run(args)
                tool_result: ConverseApiToolResult = {
                    "toolUseId": tool_use["toolUseId"],
                    "content": result["body"],
                    "status": "success" if result["succeeded"] else "error"
                }

                if self.on_tool_result:
                    self.on_tool_result(tool_result)

                results.append(tool_result)
            else:
                raise ValueError(f"Tool {tool_name} not found.")
        return results
