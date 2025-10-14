"""
Tool result conversion utilities for Strands integration.
"""

import logging

from app.agents.tools.agent_tool import ToolRunResult
from app.repositories.models.conversation import (
    DocumentToolResultModel,
    ImageToolResultModel,
    JsonToolResultModel,
    RelatedDocumentModel,
    TextToolResultModel,
    ToolResultModel,
)
from strands.types.tools import ToolResult, ToolResultContent

logger = logging.getLogger(__name__)


def _text_tool_result_model_to_strands_tool_result_content(
    result: TextToolResultModel,
) -> ToolResultContent:
    return {
        "text": result.text,
    }


def _json_tool_result_model_to_strands_tool_result_content(
    result: JsonToolResultModel,
) -> ToolResultContent:
    return {
        "json": result.json_,
    }


def _image_tool_result_model_to_strands_tool_result_content(
    result: ImageToolResultModel,
) -> ToolResultContent:
    return {
        "image": {
            "format": result.format,
            "source": {
                "bytes": result.image,
            },
        }
    }


def _document_tool_result_model_to_strands_tool_result_content(
    result: DocumentToolResultModel,
) -> ToolResultContent:
    return {
        "document": (
            {
                "format": result.format,
                "name": result.name,
                "source": {
                    "bytes": result.document,
                },
            }
            if result.format
            else {
                "name": result.name,
                "source": {
                    "bytes": result.document,
                },
            }
        )
    }


def tool_result_model_to_strands_tool_result_content(
    result: ToolResultModel,
) -> ToolResultContent:
    """Convert our ToolResultModel to Strands ToolResultContent format."""

    if isinstance(result, TextToolResultModel):
        return _text_tool_result_model_to_strands_tool_result_content(result)

    elif isinstance(result, JsonToolResultModel):
        return _json_tool_result_model_to_strands_tool_result_content(result)

    elif isinstance(result, ImageToolResultModel):
        return _image_tool_result_model_to_strands_tool_result_content(result)

    elif isinstance(result, DocumentToolResultModel):
        return _document_tool_result_model_to_strands_tool_result_content(result)

    else:
        raise ValueError(f"Unknown tool result type")


def strands_tool_result_content_to_tool_result_model(
    content: ToolResultContent,
) -> ToolResultModel:
    """Convert Strands ToolResultContent to our ToolResultModel format."""

    if "text" in content:
        return TextToolResultModel(
            text=content["text"],
        )

    elif "json" in content:
        return JsonToolResultModel(
            json=content["json"],
        )

    elif "image" in content:
        image = content["image"]
        return ImageToolResultModel(
            format=image["format"],
            image=image["source"]["bytes"],
        )

    elif "document" in content:
        document = content["document"]
        if "name" in document and "format" in document and "source" in document:
            return DocumentToolResultModel(
                format=document["format"],
                name=document["name"],
                document=document["source"]["bytes"],
            )

    raise ValueError(f"Unknown tool result content type")


def tool_run_result_to_strands_tool_result(
    result: ToolRunResult,
    display_citation: bool,
) -> ToolResult:
    """Convert our ToolRunResult back to Strands ToolResult format with source_id included."""

    return {
        "toolUseId": result["tool_use_id"],
        "status": result["status"],
        "content": [
            tool_result_model_to_strands_tool_result_content(
                related_document.to_tool_result_model(
                    display_citation=display_citation,
                )
            )
            for related_document in result["related_documents"]
        ],
    }


def _strands_tool_result_content_to_related_document(
    tool_name: str,
    result_content: ToolResultContent,
    source_id_base: str,
    rank: int | None = None,
) -> RelatedDocumentModel:
    """Convert ToolResultContent to RelatedDocumentModel."""

    if rank is not None:
        source_id = f"{source_id_base}@{rank}"

    else:
        source_id = source_id_base

    if "text" in result_content:
        return RelatedDocumentModel(
            content=TextToolResultModel(text=result_content["text"]),
            source_id=source_id,
            source_name=tool_name,
            page_number=None,
        )

    elif "json" in result_content:
        json = result_content["json"]
        if isinstance(json, dict):
            content = json.get("content")
            source_id_from_result = json.get("source_id")
            source_name = json.get("source_name")
            source_link = json.get("source_link")
            page_number = json.get("page_number")

            return RelatedDocumentModel(
                content=(
                    TextToolResultModel(
                        text=content,
                    )
                    if isinstance(content, str)
                    else JsonToolResultModel(
                        json=content if isinstance(content, dict) else json,
                    )
                ),
                source_id=(
                    str(source_id_from_result)
                    if source_id_from_result is not None
                    else source_id
                ),
                source_name=str(source_name) if source_name is not None else tool_name,
                source_link=str(source_link) if source_link is not None else None,
                page_number=int(page_number) if page_number is not None else None,
            )

    elif "image" in result_content:
        image = result_content["image"]
        return RelatedDocumentModel(
            content=ImageToolResultModel(
                format=image["format"],
                image=image["source"]["bytes"],
            ),
            source_id=source_id,
            source_name=tool_name,
            page_number=None,
        )

    elif "document" in result_content:
        document = result_content["document"]
        if "name" in document and "format" in document and "source" in document:
            return RelatedDocumentModel(
                content=DocumentToolResultModel(
                    format=document["format"],
                    name=document["name"],
                    document=document["source"]["bytes"],
                ),
                source_id=source_id,
                source_name=tool_name,
                page_number=None,
            )

    raise ValueError(f"Unknown tool result content type")


def strands_tool_result_to_tool_run_result(
    tool_name: str,
    result: ToolResult,
) -> ToolRunResult:
    """Convert ToolResult to our ToolRunResult format."""

    tool_use_id = result["toolUseId"]
    contents = result["content"]

    if len(contents) == 1:
        # Single result
        return ToolRunResult(
            tool_use_id=tool_use_id,
            status=result["status"],
            related_documents=[
                _strands_tool_result_content_to_related_document(
                    tool_name=tool_name,
                    result_content=contents[0],
                    source_id_base=tool_use_id,
                )
            ],
        )

    else:
        # Multiple results
        return ToolRunResult(
            tool_use_id=tool_use_id,
            status=result["status"],
            related_documents=[
                _strands_tool_result_content_to_related_document(
                    tool_name=tool_name,
                    result_content=content,
                    source_id_base=tool_use_id,
                    rank=rank,
                )
                for rank, content in enumerate(result["content"])
            ],
        )
