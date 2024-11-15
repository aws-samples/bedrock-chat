from typing import Any, Callable, Generic, TypeVar, TypedDict

from app.repositories.models.conversation import (
    ToolResultModel,
    TextToolResultModel,
    JsonToolResultModel,
    RelatedDocumentModel,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, JsonValue
from mypy_boto3_bedrock_runtime.type_defs import (
    ToolSpecificationTypeDef,
)

T = TypeVar("T", bound=BaseModel)


AgentResultType = str | dict | ToolResultModel


class RunResult(TypedDict):
    tool_use_id: str
    succeeded: bool
    result: AgentResultType | list[AgentResultType]


class InvalidToolError(Exception):
    pass


class AgentTool(Generic[T]):
    def __init__(
        self,
        name: str,
        description: str,
        args_schema: type[T],
        function: Callable[
            [T, BotModel | None, type_model_name | None],
            AgentResultType | list[AgentResultType],
        ],
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
            inputSchema={"json": self._generate_input_schema()},
        )

    def run(self, tool_use_id: str, input: dict[str, JsonValue]) -> RunResult:
        try:
            arg = self.args_schema.model_validate(input)
            res = self.function(arg, self.bot, self.model)
            return RunResult(
                tool_use_id=tool_use_id,
                succeeded=True,
                result=res,
            )

        except Exception as e:
            return RunResult(
                tool_use_id=tool_use_id,
                succeeded=False,
                result=str(e),
            )


def agent_result_to_related_document(
    tool_name: str,
    res: AgentResultType,
    source_id_base: str,
    rank: int | None = None,
) -> RelatedDocumentModel:
    if rank is not None:
        source_id = f"{source_id_base}@{rank}"

    else:
        source_id = source_id_base

    if isinstance(res, str):
        return RelatedDocumentModel(
            content=TextToolResultModel(text=res),
            source_id=source_id,
            source_name=tool_name,
        )

    elif isinstance(res, dict):
        content = res.get("content")
        source_name = res.get("source_name")
        source_link = res.get("source_link")
        return RelatedDocumentModel(
            content=(
                TextToolResultModel(
                    text=content,
                )
                if isinstance(content, str)
                else JsonToolResultModel(
                    json=content if isinstance(content, dict) else res,
                )
            ),
            source_id=source_id,
            source_name=str(source_name) if source_name is not None else tool_name,
            source_link=str(source_link) if source_link is not None else None,
        )

    elif isinstance(res, JsonToolResultModel):
        return agent_result_to_related_document(
            tool_name=tool_name,
            res=res.json_,
            source_id_base=source_id_base,
            rank=rank,
        )

    else:
        return RelatedDocumentModel(
            content=res,
            source_id=source_id,
            source_name=tool_name,
        )
