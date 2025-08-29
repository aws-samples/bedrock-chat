"""
Tool result conversion utilities for Strands integration.
"""
import logging

from app.agents.tools.agent_tool import (
    ToolFunctionResult,
    ToolRunResult,
    _function_result_to_related_document,
)
from app.repositories.models.conversation import (
    JsonToolResultModel,
    TextToolResultModel,
)
from strands.experimental.hooks import AfterToolInvocationEvent
from strands.types.tools import ToolResult, ToolResultContent

logger = logging.getLogger(__name__)


def convert_tool_result_content_to_function_result(
    content_item: ToolResultContent,
) -> ToolFunctionResult:
    """Convert ToolResultContent to ToolFunctionResult format."""
    if "text" in content_item:
        return content_item["text"]
    elif "json" in content_item:
        # Return json content directly without wrapping in {"data": ...}
        return content_item["json"]
    elif "document" in content_item:
        # Convert document to string
        doc_content = content_item["document"]
        if isinstance(doc_content, dict) and "source" in doc_content:
            # DocumentSource has bytes field according to Strands type definition
            doc_source = doc_content["source"]
            if isinstance(doc_source, dict) and "bytes" in doc_source:
                try:
                    # Try to decode bytes as UTF-8 text
                    return doc_source["bytes"].decode("utf-8")
                except (UnicodeDecodeError, AttributeError):
                    # If decoding fails, return a description
                    doc_name = doc_content.get("name", "document")
                    doc_format = doc_content.get("format", "unknown")
                    return f"[Document: {doc_name} ({doc_format})]"
            else:
                return str(doc_source)
        else:
            return str(doc_content)
    elif "image" in content_item:
        # Convert image to text description
        img_content = content_item["image"]
        if isinstance(img_content, dict):
            img_format = img_content.get("format", "unknown")
            return f"[Image content ({img_format})]"
        else:
            return "[Image content]"
    else:
        # Empty content
        return ""


def convert_raw_tool_result_to_tool_result(event: AfterToolInvocationEvent) -> dict:
    """Convert raw tool result to proper ToolResult format."""

    tool_use_id = event.tool_use["toolUseId"]
    raw_result = event.result

    # DEBUG: Log the raw result before conversion
    logger.debug(f"[RAW_TOOL_RESULT_DEBUG] Tool: {event.tool_use['name']}")
    logger.debug(f"[RAW_TOOL_RESULT_DEBUG] Raw result type: {type(raw_result)}")
    logger.debug(f"[RAW_TOOL_RESULT_DEBUG] Raw result: {raw_result}")

    # If already in ToolResult format, return as is
    if (
        isinstance(raw_result, dict)
        and "content" in raw_result
        and "status" in raw_result
    ):
        logger.debug("[RAW_TOOL_RESULT_DEBUG] Already in ToolResult format")
        return raw_result

    # Convert raw result to ToolResult format
    content_list = []

    if isinstance(raw_result, list):
        # Handle list results (like simple_list tool)
        logger.debug("[RAW_TOOL_RESULT_DEBUG] Converting list result to ToolResult")
        content_list.append({"json": raw_result})
    elif isinstance(raw_result, dict):
        # Handle dict results
        logger.debug("[RAW_TOOL_RESULT_DEBUG] Converting dict result to ToolResult")
        content_list.append({"json": raw_result})
    elif isinstance(raw_result, str):
        # Handle string results
        logger.debug("[RAW_TOOL_RESULT_DEBUG] Converting string result to ToolResult")
        content_list.append({"text": raw_result})
    else:
        # Handle other types by converting to JSON
        logger.debug(
            f"[RAW_TOOL_RESULT_DEBUG] Converting {type(raw_result)} result to ToolResult"
        )
        content_list.append({"json": raw_result})

    result = {
        "content": content_list,
        "status": "success",
        "toolUseId": tool_use_id,
    }

    logger.debug(f"[RAW_TOOL_RESULT_DEBUG] Final ToolResult: {result}")
    return result


def convert_tool_run_result_to_strands_tool_result(
    tool_run_result: ToolRunResult,
) -> dict:
    """Convert our ToolRunResult back to Strands ToolResult format with source_id included."""
    # Convert related documents back to ToolResultContent
    content_list = []
    for related_doc in tool_run_result["related_documents"]:
        content = related_doc.content
        source_id = related_doc.source_id

        # Always return as JSON with source_id included
        if isinstance(content, TextToolResultModel):
            # Convert text content to JSON with source_id
            original_content = {"text": content.text}
            enhanced_content = {**original_content, "source_id": source_id}
            tool_result_content: ToolResultContent = {"json": enhanced_content}
        elif isinstance(content, JsonToolResultModel):
            # Convert JSON content with source_id
            original_content = (
                content.json_
                if isinstance(content.json_, dict)
                else {"data": content.json_}
            )
            enhanced_content = {**original_content, "source_id": source_id}
            tool_result_content = {"json": enhanced_content}
        else:
            # Fallback to text converted to JSON with source_id
            original_content = {"text": str(content)}
            enhanced_content = {**original_content, "source_id": source_id}
            tool_result_content = {"json": enhanced_content}

        content_list.append(tool_result_content)

    # If no content, add empty JSON content with source_id
    if not content_list:
        content_list.append({"json": {"text": "", "source_id": "unknown"}})

    return {
        "content": content_list,
        "status": tool_run_result["status"],
        "toolUseId": tool_run_result["tool_use_id"],
    }


def convert_after_tool_event_to_tool_run_result(
    event: AfterToolInvocationEvent,
) -> ToolRunResult:
    """Convert AfterToolInvocationEvent to our ToolRunResult format."""
    tool_input = event.tool_use["input"]
    tool_name = event.tool_use["name"]

    result = event.result
    tool_use_id = result["toolUseId"]
    tool_result_status = result["status"]
    tool_result_content = result["content"]

    # DEBUG: Log the raw result content
    logger.debug(f"[TOOL_RESULT_DEBUG] Tool: {tool_name}")
    logger.debug(f"[TOOL_RESULT_DEBUG] Raw result content: {tool_result_content}")
    logger.debug(f"[TOOL_RESULT_DEBUG] Content type: {type(tool_result_content)}")
    if tool_result_content:
        logger.debug(f"[TOOL_RESULT_DEBUG] First content item: {tool_result_content[0]}")
        logger.debug(
            f"[TOOL_RESULT_DEBUG] First content item type: {type(tool_result_content[0])}"
        )

    # Convert content items to function results first
    function_results = []
    for content_item in tool_result_content:
        function_result = convert_tool_result_content_to_function_result(content_item)
        function_results.append(function_result)

    # Special handling for tools that return lists (like simple_list)
    if len(function_results) == 1 and isinstance(function_results[0], list):
        # Tool returned a list - treat each item as a separate result
        list_items = function_results[0]
        related_documents = [
            _function_result_to_related_document(
                tool_name=tool_name,
                res=item,
                source_id_base=tool_use_id,
                rank=rank,
            )
            for rank, item in enumerate(list_items)
        ]
    elif len(function_results) > 1:
        # Multiple results - treat as list
        related_documents = [
            _function_result_to_related_document(
                tool_name=tool_name,
                res=result,
                source_id_base=tool_use_id,
                rank=rank,
            )
            for rank, result in enumerate(function_results)
        ]
    else:
        # Single result
        single_result = function_results[0] if function_results else ""
        related_documents = [
            _function_result_to_related_document(
                tool_name=tool_name,
                res=single_result,
                source_id_base=tool_use_id,
            )
        ]

    return ToolRunResult(
        tool_use_id=tool_use_id,
        status=tool_result_status,
        related_documents=related_documents,
    )
