from typing import Any, Callable, Generic, TypeVar, TypedDict

from app.repositories.models.conversation import ToolResultModel
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, JsonValue
from mypy_boto3_bedrock_runtime.type_defs import (
    ToolSpecificationTypeDef,
    ToolResultContentBlockOutputTypeDef,
)

T = TypeVar("T", bound=BaseModel)


class RunResult(TypedDict):
    tool_use_id: str
    succeeded: bool
    body: list[ToolResultContentBlockOutputTypeDef]


class InvalidToolError(Exception):
    pass


AgentResultType = str | dict | ToolResultModel | list[str | dict | ToolResultModel]


class AgentTool(Generic[T]):
    def __init__(
        self,
        name: str,
        description: str,
        args_schema: type[T],
        function: Callable[[T, BotModel | None, type_model_name | None], AgentResultType],
        bot: BotModel | None = None,
        model: type_model_name | None = None,
    ):
        self.name = name
        self.description = description
        self.args_schema = args_schema
        self.function = function
        self.bot = bot
        self.model: type_model_name | None = model

    def _generate_input_schema(self) -> dict[str, Any]:
        """Converts the Pydantic model to a JSON schema."""
        return self.args_schema.model_json_schema()

    def to_converse_spec(self) -> ToolSpecificationTypeDef:
        return ToolSpecificationTypeDef(
            name=self.name,
            description=self.description,
            inputSchema={
                "json": self._generate_input_schema()
            },
        )

    def run(self, tool_use_id: str, input: dict[str, JsonValue]) -> RunResult:
        try:
            arg = self.args_schema.model_validate(input)
            res = self.function(arg, self.bot, self.model)
            if isinstance(res, str):
                return RunResult(
                    tool_use_id=tool_use_id,
                    succeeded=True,
                    body=[{"text": res}],
                )

            elif isinstance(res, dict):
                return RunResult(
                    tool_use_id=tool_use_id,
                    succeeded=True,
                    body=[{"json": res}],
                )

            elif isinstance(res, list):
                return RunResult(
                    tool_use_id=tool_use_id,
                    succeeded=True,
                    body=[
                        {
                            "text": result,
                        }
                        if isinstance(result, str) else
                        {
                            "json": result
                        }
                        if isinstance(result, dict) else
                        result.to_content_for_converse()
                        for result in res
                    ],
                )

            else:
                return RunResult(
                    tool_use_id=tool_use_id,
                    succeeded=True,
                    body=[res.to_content_for_converse()],
                )

        except Exception as e:
            return RunResult(
                tool_use_id=tool_use_id,
                succeeded=False,
                body=[{"text": str(e)}],
            )
