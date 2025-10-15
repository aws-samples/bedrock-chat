"""
Content conversion utilities for Strands integration.
"""

from app.repositories.models.conversation import (
    AttachmentContentModel,
    ContentModel,
    ImageContentModel,
    ReasoningContentModel,
    TextContentModel,
    ToolResultContentModel,
    ToolResultContentModelBody,
    ToolUseContentModel,
    ToolUseContentModelBody,
)
from app.strands_integration.converters.tool_converter import (
    strands_tool_result_content_to_tool_result_model,
    tool_result_model_to_strands_tool_result_content,
)
from strands.types.content import ContentBlock


def _text_content_model_to_strands_content_blocks(
    content: TextContentModel,
) -> list[ContentBlock]:
    """Convert TextContentModel to Strands ContentBlock format."""

    return [
        {
            "text": content.body,
        },
    ]


def _image_content_model_to_strands_content_blocks(
    content: ImageContentModel,
) -> list[ContentBlock]:
    """Convert ImageContentModel to Strands ContentBlock format."""

    format = content.format
    if format is None:
        raise ValueError("Missing image format")

    return [
        {
            "image": {
                "format": format,
                "source": {
                    "bytes": content.body,
                },
            },
        },
    ]


def _attachment_content_model_to_strands_content_blocks(
    content: AttachmentContentModel,
) -> list[ContentBlock]:
    """Convert AttachmentContentModel to Strands ContentBlock format."""

    format, name = content.format_and_name
    return [
        {
            "document": (
                {
                    "format": format,
                    "name": name,
                    "source": {
                        "bytes": content.body,
                    },  # Use body directly (already base64)
                }
                if format is not None
                else {
                    "name": name,
                    "source": {
                        "bytes": content.body,
                    },
                }
            ),
        },
    ]


def _tool_use_content_model_to_strands_content_blocks(
    content: ToolUseContentModel,
) -> list[ContentBlock]:
    """Convert ToolUseContentModel to Strands ContentBlock format."""

    return [
        {
            "toolUse": {
                "toolUseId": content.body.tool_use_id,
                "name": content.body.name,
                "input": content.body.input,
            },
        },
    ]


def _tool_result_content_model_to_strands_content_blocks(
    content: ToolResultContentModel,
) -> list[ContentBlock]:
    """Convert ToolResultContentModel to Strands ContentBlock format."""

    return [
        {
            "toolResult": {
                "toolUseId": content.body.tool_use_id,
                "status": content.body.status,
                "content": [
                    tool_result_model_to_strands_tool_result_content(content)
                    for content in content.body.content
                ],
            },
        },
    ]


def _reasoning_content_model_to_strands_content_blocks(
    content: ReasoningContentModel,
) -> list[ContentBlock]:
    """Convert ReasoningContentModel to Strands ContentBlock format."""

    return (
        [
            {
                "reasoningContent": (
                    {
                        "reasoningText": (
                            {
                                "text": content.text,
                                "signature": content.signature,
                            }
                            if content.signature
                            else {
                                "text": content.text,
                            }
                        ),
                    }
                    if content.text
                    else (
                        {
                            "redactedContent": content.redacted_content,
                        }
                        if content.redacted_content
                        else {}
                    )
                ),
            },
        ]
        if content.text or content.redacted_content
        else []
    )


def content_model_to_strands_content_blocks(
    content: ContentModel,
) -> list[ContentBlock]:
    """Convert ContentModel to Strands ContentBlock format."""

    if isinstance(content, TextContentModel):
        return _text_content_model_to_strands_content_blocks(content)

    elif isinstance(content, ImageContentModel):
        return _image_content_model_to_strands_content_blocks(content)

    elif isinstance(content, AttachmentContentModel):
        return _attachment_content_model_to_strands_content_blocks(content)

    elif isinstance(content, ToolUseContentModel):
        return _tool_use_content_model_to_strands_content_blocks(content)

    elif isinstance(content, ToolResultContentModel):
        return _tool_result_content_model_to_strands_content_blocks(content)

    elif isinstance(content, ReasoningContentModel):
        return _reasoning_content_model_to_strands_content_blocks(content)

    else:
        raise ValueError(f"Unknown content type")


def strands_content_block_to_content_model(content: ContentBlock) -> ContentModel:
    if "text" in content:
        return TextContentModel(
            content_type="text",
            body=content["text"],
        )

    elif "image" in content:
        image = content["image"]
        return ImageContentModel(
            content_type="image",
            media_type=f"image/{image["format"]}",
            body=image["source"]["bytes"],
        )

    elif "document" in content:
        document = content["document"]
        if "name" in document and "source" in document:
            return AttachmentContentModel(
                content_type="attachment",
                file_name=(
                    f"{document["name"]}.{document["format"]}"
                    if "format" in document
                    else document["name"]
                ),
                body=document["source"]["bytes"],
            )

    elif "toolUse" in content:
        tool_use = content["toolUse"]
        return ToolUseContentModel(
            content_type="toolUse",
            body=ToolUseContentModelBody(
                tool_use_id=tool_use["toolUseId"],
                name=tool_use["name"],
                input=tool_use["input"],
            ),
        )

    elif "toolResult" in content:
        tool_result = content["toolResult"]
        return ToolResultContentModel(
            content_type="toolResult",
            body=ToolResultContentModelBody(
                tool_use_id=tool_result["toolUseId"],
                status=tool_result["status"],
                content=[
                    strands_tool_result_content_to_tool_result_model(content)
                    for content in tool_result["content"]
                ],
            ),
        )

    elif "reasoningContent" in content:
        reasoning_content = content["reasoningContent"]
        if "reasoningText" in reasoning_content:
            reasoning_text = reasoning_content["reasoningText"]
            if "text" in reasoning_text:
                return ReasoningContentModel(
                    content_type="reasoning",
                    text=reasoning_text["text"],
                    signature=reasoning_text.get("signature") or "",
                    redacted_content=b"",  # Default empty
                )

        elif "redactedContent" in reasoning_content:
            return ReasoningContentModel(
                content_type="reasoning",
                text="",
                signature="",
                redacted_content=reasoning_content["redactedContent"],
            )

    raise ValueError(f"Unknown content type")
