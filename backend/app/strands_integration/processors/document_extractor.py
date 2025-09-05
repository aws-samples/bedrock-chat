"""
Document extraction utilities for Strands integration.
"""

from app.repositories.models.conversation import (
    ReasoningContentModel,
    RelatedDocumentModel,
    SimpleMessageModel,
    ToolResultContentModel,
    ToolResultContentModelBody,
    ToolUseContentModel,
    ToolUseContentModelBody,
)
from strands.types.content import Message

from app.strands_integration.handlers.tool_result_capture import ToolResultCapture


def extract_related_documents_from_tool_capture(
    tool_capture: ToolResultCapture, assistant_msg_id: str
) -> list[RelatedDocumentModel]:
    """Extract related documents from ToolResultCapture."""
    related_documents = []

    for tool_use_id, tool_result in tool_capture.captured_tool_results.items():
        for related_doc in tool_result["related_documents"]:
            # Keep original source_id format for compatibility with frontend citation matching
            updated_doc = RelatedDocumentModel(
                content=related_doc.content,
                source_id=related_doc.source_id,
                source_name=related_doc.source_name,
                source_link=related_doc.source_link,
                page_number=related_doc.page_number,
            )
            related_documents.append(updated_doc)

    return related_documents


def build_thinking_log_from_tool_capture(
    tool_capture: ToolResultCapture,
) -> list[SimpleMessageModel] | None:
    """Build thinking_log from ToolResultCapture for tool use/result pairs."""
    if not tool_capture.captured_tool_results:
        return None

    thinking_log = []

    for tool_use_id, tool_result in tool_capture.captured_tool_results.items():
        # Get tool use info from captured data
        tool_use_info = tool_capture.captured_tool_uses.get(tool_use_id, {})

        # Create tool use message
        tool_use_content = ToolUseContentModel(
            content_type="toolUse",
            body=ToolUseContentModelBody(
                tool_use_id=tool_use_id,
                name=tool_use_info.get("name", "unknown"),
                input=tool_use_info.get("input", {}),
            ),
        )

        tool_use_message = SimpleMessageModel(
            role="assistant", content=[tool_use_content]
        )
        thinking_log.append(tool_use_message)

        # Create tool result message
        from app.repositories.models.conversation import ToolResultModel

        result_models: list[ToolResultModel] = []
        for related_doc in tool_result["related_documents"]:
            result_models.append(related_doc.content)

        tool_result_content = ToolResultContentModel(
            content_type="toolResult",
            body=ToolResultContentModelBody(
                tool_use_id=tool_use_id,
                content=result_models,
                status=tool_result["status"],
            ),
        )

        tool_result_message = SimpleMessageModel(
            role="user", content=[tool_result_content]
        )
        thinking_log.append(tool_result_message)

    return thinking_log if thinking_log else None


def extract_reasoning_from_message(message: Message) -> ReasoningContentModel | None:
    """Extract reasoning content from Strands Message."""
    for content_block in message["content"]:
        if "reasoningContent" in content_block:
            reasoning_content = content_block["reasoningContent"]
            if "reasoningText" in reasoning_content:
                reasoning_text = reasoning_content["reasoningText"]
                return ReasoningContentModel(
                    content_type="reasoning",
                    text=reasoning_text.get("text", ""),
                    signature=reasoning_text.get("signature", "")
                    or "",  # Ensure not None
                    redacted_content=b"",  # Default empty
                )
    return None
