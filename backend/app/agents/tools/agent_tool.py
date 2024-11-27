from typing import Any, Callable, Generic, Literal, TypedDict, TypeVar

from app.repositories.models.conversation import (
    ToolResultModel,
    TextToolResultModel,
    JsonToolResultModel,
    RelatedDocumentModel,
    ToolResultContentModel,
    ToolResultContentModelBody,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, JsonValue
from mypy_boto3_bedrock_runtime.type_defs import (
    ToolSpecificationTypeDef,
)

T = TypeVar("T", bound=BaseModel)


ToolFunctionResult = str | dict | ToolResultModel


class ToolRunResult(TypedDict):
    tool_use_id: str
    status: Literal["success", "error"]
    related_documents: list[RelatedDocumentModel]


def run_result_to_tool_result_content_model(
    run_result: ToolRunResult, display_citation: bool
) -> ToolResultContentModel:
    return ToolResultContentModel(
        content_type="toolResult",
        body=ToolResultContentModelBody(
            tool_use_id=run_result["tool_use_id"],
            content=[
                related_document.to_tool_result_model(
                    display_citation=display_citation,
                )
                for related_document in run_result["related_documents"]
            ],
            status=run_result["status"],
        ),
    )


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
            ToolFunctionResult | list[ToolFunctionResult],
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

    def run(self, tool_use_id: str, input: dict[str, JsonValue]) -> ToolRunResult:
        try:
            arg = self.args_schema.model_validate(input)
            res = self.function(arg, self.bot, self.model)
            if isinstance(res, list):
                related_documents = [
                    _function_result_to_related_document(
                        tool_name=self.name,
                        res=result,
                        source_id_base=tool_use_id,
                        rank=rank,
                    )
                    for rank, result in enumerate(res)
                ]

            else:
                related_documents = [
                    _function_result_to_related_document(
                        tool_name=self.name,
                        res=res,
                        source_id_base=tool_use_id,
                    )
                ]

            return ToolRunResult(
                tool_use_id=tool_use_id,
                status="success",
                related_documents=related_documents,
            )

        except Exception as e:
            return ToolRunResult(
                tool_use_id=tool_use_id,
                status="error",
                related_documents=[
                    _function_result_to_related_document(
                        tool_name=self.name,
                        res=str(e),
                        source_id_base=tool_use_id,
                    )
                ],
            )


def _function_result_to_related_document(
    tool_name: str,
    res: ToolFunctionResult,
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
        source_id_from_result = res.get("source_id")
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
            source_id=(
                str(source_id_from_result)
                if source_id_from_result is not None
                else source_id
            ),
            source_name=str(source_name) if source_name is not None else tool_name,
            source_link=str(source_link) if source_link is not None else None,
        )

    else:
        return RelatedDocumentModel(
            content=res,
            source_id=source_id,
            source_name=tool_name,
        )
