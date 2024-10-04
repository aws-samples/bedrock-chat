from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from app.bedrock import (
        ConverseApiToolResult,
        ConverseApiToolResultContent,
        ConverseApiToolUseContent,
    )

from app.routes.schemas.conversation import MessageInput, type_model_name
from pydantic import BaseModel, Field


class ContentModel(BaseModel):
    content_type: Literal["text", "image", "attachment"]
    media_type: str | None
    body: str = Field(
        ...,
        description="Body string. If content_type is image or attachment, it should be base64 encoded.",
    )
    file_name: str | None = Field(None)

    model_config = {
        "json_encoders": {
            bytes: lambda v: base64.b64encode(v).decode(),
        }
    }


class FeedbackModel(BaseModel):
    thumbs_up: bool
    category: str
    comment: str


class ChunkModel(BaseModel):
    content: str
    content_type: str
    source: str
    rank: int


class AgentToolUseContentModel(BaseModel):
    tool_use_id: str
    name: str
    input: dict

    @classmethod
    def from_tool_use_content(cls, tool_use_content: "ConverseApiToolUseContent"):
        return AgentToolUseContentModel(
            tool_use_id=tool_use_content["toolUseId"],
            name=tool_use_content["name"],
            input=tool_use_content["input"],
        )


class AgentToolResultModelContentModel(BaseModel):
    json_: dict | None  # `json` is a reserved keyword on pydantic
    text: str | None

    @classmethod
    def from_tool_result_content(
        cls, tool_result_content: "ConverseApiToolResultContent"
    ):
        return AgentToolResultModelContentModel(
            json_=(
                tool_result_content["json"] if "json" in tool_result_content else None
            ),
            text=tool_result_content["text"] if "text" in tool_result_content else None,
        )


class AgentToolResultModel(BaseModel):
    tool_use_id: str
    content: AgentToolResultModelContentModel
    status: str

    @classmethod
    def from_tool_result(cls, tool_result: "ConverseApiToolResult"):
        return AgentToolResultModel(
            tool_use_id=tool_result["toolUseId"],
            content=AgentToolResultModelContentModel.from_tool_result_content(
                tool_result["content"]
            ),
            status=tool_result["status"] if "status" in tool_result else "",
        )


class AgentContentModel(BaseModel):
    content_type: Literal["text", "toolUse", "toolResult"]
    body: str | AgentToolUseContentModel | AgentToolResultModel


class AgentMessageModel(BaseModel):
    role: str
    content: list[AgentContentModel]

    @classmethod
    def from_message_model(cls, message: "MessageModel"):
        return AgentMessageModel(
            role=message.role,  # type: ignore
            content=[
                AgentContentModel(
                    content_type=content.content_type,  # type: ignore
                    body=content.body,
                )
                for content in message.content
            ],
        )


class MessageModel(BaseModel):
    role: str
    content: list[ContentModel]
    model: type_model_name
    children: list[str]
    parent: str | None
    create_time: float
    feedback: FeedbackModel | None
    used_chunks: list[ChunkModel] | None
    thinking_log: list[AgentMessageModel] | None = Field(
        None, description="Only available for agent."
    )

    @classmethod
    def from_message_input(cls, message_input: MessageInput):
        return MessageModel(
            role=message_input.role,
            content=[
                ContentModel(
                    content_type=content.content_type,
                    media_type=content.media_type,
                    body=content.body,
                    file_name=content.file_name,
                )
                for content in message_input.content
            ],
            model=message_input.model,
            children=[],
            parent=message_input.parent_message_id,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )


class ConversationModel(BaseModel):
    id: str
    create_time: float
    title: str
    total_price: float
    message_map: dict[str, MessageModel]
    last_message_id: str
    bot_id: str | None
    should_continue: bool


class ConversationMeta(BaseModel):
    id: str
    title: str
    create_time: float
    model: str
    bot_id: str | None
