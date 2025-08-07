"""
Message converter for converting between Strands and existing message formats.
"""

import logging
from typing import Any, List

from app.repositories.models.conversation import (
    MessageModel,
    ReasoningContentModel,
    SimpleMessageModel,
    TextContentModel,
    TextToolResultModel,
    ToolResultContentModel,
    ToolResultContentModelBody,
    ToolUseContentModel,
    ToolUseContentModelBody,
)
from app.utils import get_current_time
from ulid import ULID

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def strands_result_to_message_model(
    result: Any,
    parent_message_id: str,
    bot: Any = None,
    model_name: str = None,
    collected_tool_usage: list = None,
    collected_reasoning: list = None,
    display_citation: bool = False,
) -> tuple[MessageModel, list]:
    """
    Convert Strands AgentResult to MessageModel with citation support.

    Args:
        result: Strands AgentResult - The result from calling agent(prompt)
        parent_message_id: Parent message ID
        bot: Optional bot configuration for tool detection
        model_name: Optional model name to use (if not provided, will be extracted from result)
        collected_tool_usage: Pre-collected tool usage data
        collected_reasoning: Pre-collected reasoning data
        display_citation: Whether to extract related documents for citation

    Returns:
        Tuple of (MessageModel, list of RelatedDocumentModel)
    """
    logger.debug(f"[MESSAGE_CONVERTER] Starting conversion - result type: {type(result)}")
    logger.debug(
        f"[MESSAGE_CONVERTER] Result attributes: {[attr for attr in dir(result) if not attr.startswith('_')]}"
    )

    message_id = str(ULID())

    # Extract text content from AgentResult
    # According to Strands docs, AgentResult has a message attribute with content array
    logger.debug(f"[MESSAGE_CONVERTER] Extracting text content...")
    text_content = _extract_text_content_from_agent_result(result)
    logger.debug(f"[MESSAGE_CONVERTER] Text content extracted: {len(text_content)} chars")
    content = [TextContentModel(content_type="text", body=text_content)]

    # Extract reasoning content if available (only when reasoning is enabled)
    logger.debug(f"[MESSAGE_CONVERTER] Extracting reasoning content...")
    reasoning_content = _extract_reasoning_content_from_agent_result(result)

    # Create thinking log from tool usage in the message
    logger.debug(f"[MESSAGE_CONVERTER] Creating thinking log...")
    thinking_log = _create_thinking_log_from_agent_result(
        result, bot, collected_tool_usage, collected_reasoning
    )

    # Apply chat_legacy logic: if reasoning found in thinking_log, add to message content
    if thinking_log:
        reasoning_log = next(
            (
                log
                for log in thinking_log
                if any(
                    isinstance(content_item, ReasoningContentModel)
                    for content_item in log.content
                )
            ),
            None,
        )
        if reasoning_log:
            reasoning_content_from_log = next(
                content_item
                for content_item in reasoning_log.content
                if isinstance(content_item, ReasoningContentModel)
            )
            content.insert(
                0, reasoning_content_from_log
            )  # Insert at beginning like chat_legacy
            logger.debug(
                f"[MESSAGE_CONVERTER] Reasoning content from thinking_log added: {len(reasoning_content_from_log.text)} chars"
            )
        else:
            logger.debug(
                f"[MESSAGE_CONVERTER] No reasoning content found in thinking_log"
            )

    # Fallback: if direct reasoning extraction found something, add it
    elif reasoning_content:
        logger.debug(
            f"[MESSAGE_CONVERTER] Direct reasoning content found: {len(reasoning_content.text)} chars"
        )
        content.insert(0, reasoning_content)  # Insert at beginning like chat_legacy
    else:
        logger.debug(f"[MESSAGE_CONVERTER] No reasoning content found")

    # thinking_log is already created above, so remove duplicate creation
    if thinking_log:
        logger.debug(
            f"[MESSAGE_CONVERTER] Thinking log created with {len(thinking_log)} entries"
        )
    else:
        logger.debug(f"[MESSAGE_CONVERTER] No thinking log created")

    # Use provided model name or extract from result
    if model_name:
        logger.debug(f"[MESSAGE_CONVERTER] Using provided model name: {model_name}")
        final_model_name = model_name
    else:
        final_model_name = _get_model_name_from_agent_result(result)
        logger.debug(f"[MESSAGE_CONVERTER] Extracted model name: {final_model_name}")

    logger.debug(f"[MESSAGE_CONVERTER] Final model name: {final_model_name}")

    # Extract related documents for citation if enabled
    related_documents = []
    if display_citation:
        logger.debug(f"[MESSAGE_CONVERTER] Extracting related documents for citation...")
        related_documents = _extract_related_documents_from_collected_tool_usage(
            collected_tool_usage
        )
        logger.debug(
            f"[MESSAGE_CONVERTER] Extracted {len(related_documents)} related documents"
        )

    final_message = MessageModel(
        role="assistant",
        content=content,
        model=final_model_name,
        children=[],
        parent=parent_message_id,
        create_time=get_current_time(),
        thinking_log=thinking_log,
        used_chunks=None,
        feedback=None,
    )

    logger.debug(
        f"[MESSAGE_CONVERTER] Conversion completed - content items: {len(final_message.content)}, thinking_log: {len(thinking_log) if thinking_log else 0}, related_docs: {len(related_documents)}"
    )
    logger.debug(
        f"[MESSAGE_CONVERTER] Final message content types: {[c.content_type for c in final_message.content]}"
    )

    # Log content sizes
    for i, content_item in enumerate(final_message.content):
        if hasattr(content_item, "body"):
            size = len(str(content_item.body))
        elif hasattr(content_item, "text"):
            size = len(str(content_item.text))
        else:
            size = 0
        logger.debug(
            f"[MESSAGE_CONVERTER] Content {i} ({content_item.content_type}): {size} chars"
        )

    return final_message, related_documents

    return final_message


def _extract_related_documents_from_collected_tool_usage(
    collected_tool_usage: list,
) -> list:
    """
    Extract RelatedDocumentModel instances from collected tool usage for citation.

    This function processes the collected_tool_usage data from Strands callbacks
    to create RelatedDocumentModel instances for citation display.

    Args:
        collected_tool_usage: List of tool usage data collected from Strands callbacks

    Returns:
        List of RelatedDocumentModel instances
    """
    from app.repositories.models.conversation import (
        RelatedDocumentModel,
        TextToolResultModel,
    )

    logger.debug(
        f"[MESSAGE_CONVERTER] Extracting related documents from collected tool usage"
    )
    related_documents = []

    if not collected_tool_usage:
        logger.debug(f"[MESSAGE_CONVERTER] No collected tool usage provided")
        return related_documents

    try:
        logger.debug(
            f"[MESSAGE_CONVERTER] Processing {len(collected_tool_usage)} collected tool usage items"
        )

        # Group tool usage by toolUseId to match tool results with their usage
        tool_usage_by_id = {}
        for item in collected_tool_usage:
            item_type = item.get("type")
            data = item.get("data", {})
            tool_use_id = data.get("toolUseId", "unknown")

            if tool_use_id not in tool_usage_by_id:
                tool_usage_by_id[tool_use_id] = {"toolUse": None, "toolResult": None}

            if item_type == "toolUse":
                tool_usage_by_id[tool_use_id]["toolUse"] = data
            elif item_type == "toolResult":
                tool_usage_by_id[tool_use_id]["toolResult"] = data

        logger.debug(
            f"[MESSAGE_CONVERTER] Grouped into {len(tool_usage_by_id)} tool usage pairs"
        )

        # Process each tool usage pair
        for tool_use_id, tool_data in tool_usage_by_id.items():
            tool_use = tool_data.get("toolUse")
            tool_result = tool_data.get("toolResult")

            if not tool_result:
                logger.debug(
                    f"[MESSAGE_CONVERTER] No tool result for {tool_use_id}, skipping"
                )
                continue

            tool_name = (
                tool_use.get("name", "unknown_tool") if tool_use else "unknown_tool"
            )
            logger.debug(
                f"[MESSAGE_CONVERTER] Processing tool result for {tool_name} ({tool_use_id})"
            )

            # Extract content from tool result
            tool_content = tool_result.get("content", [])
            if isinstance(tool_content, list):
                for i, content_item in enumerate(tool_content):
                    if isinstance(content_item, dict):
                        # Extract text content
                        content_text = content_item.get("text", "")

                        # Check if the text content is a JSON string representing a list
                        # This handles the case where tools return lists that get serialized
                        try:
                            import json
                            import ast
                            
                            # First try JSON parsing
                            try:
                                parsed_content = json.loads(content_text)
                            except json.JSONDecodeError:
                                # If JSON fails, try ast.literal_eval for Python literal strings
                                parsed_content = ast.literal_eval(content_text)
                            
                            # Handle citation-enhanced results (dict with 'content' and 'source_id')
                            if isinstance(parsed_content, dict) and 'content' in parsed_content and 'source_id' in parsed_content:
                                logger.debug(
                                    f"[MESSAGE_CONVERTER] Found citation-enhanced result with source_id: {parsed_content['source_id']}"
                                )
                                # Extract the actual content and try to parse it
                                actual_content = parsed_content['content']
                                citation_source_id = parsed_content['source_id']
                                
                                try:
                                    # Try to parse the actual content as JSON
                                    actual_parsed = json.loads(actual_content)
                                    
                                    # Check if it's a dict with list (like simple_list_tool)
                                    if isinstance(actual_parsed, dict):
                                        list_keys = ["items", "results", "data", "list", "entries"]
                                        found_list = None
                                        found_key = None
                                        
                                        for key in list_keys:
                                            if key in actual_parsed and isinstance(actual_parsed[key], list):
                                                found_list = actual_parsed[key]
                                                found_key = key
                                                break
                                        
                                        if found_list:
                                            logger.debug(
                                                f"[MESSAGE_CONVERTER] Citation-enhanced result contains dict with list in '{found_key}' key with {len(found_list)} items, splitting into individual documents"
                                            )
                                            # Split list into individual RelatedDocuments using citation source_id as base
                                            for rank, item in enumerate(found_list):
                                                if isinstance(item, dict):
                                                    # Extract content from the item
                                                    item_text = (
                                                        item.get("content") or 
                                                        item.get("description") or 
                                                        item.get("text") or 
                                                        item.get("name") or 
                                                        str(item)
                                                    )
                                                    # Use citation source_id with rank suffix
                                                    source_id = f"{citation_source_id}@{rank}"
                                                    
                                                    logger.debug(
                                                        f"[MESSAGE_CONVERTER] Creating related document from citation-enhanced list item: {source_id}"
                                                    )

                                                    # Create RelatedDocumentModel for each list item
                                                    related_doc = RelatedDocumentModel(
                                                        content=TextToolResultModel(text=str(item_text)),
                                                        source_id=source_id,
                                                        source_name=item.get("source_name") or item.get("name") or tool_name,
                                                        source_link=item.get("source_link"),
                                                        page_number=item.get("page_number"),
                                                    )
                                                    related_documents.append(related_doc)
                                                    logger.debug(
                                                        f"[MESSAGE_CONVERTER] Added related document from citation-enhanced list: {source_id} ({len(str(item_text))} chars)"
                                                    )
                                            continue  # Skip the regular processing for this content_item
                                        else:
                                            # Single item with citation source_id
                                            logger.debug(
                                                f"[MESSAGE_CONVERTER] Citation-enhanced single item, using source_id: {citation_source_id}"
                                            )
                                            related_doc = RelatedDocumentModel(
                                                content=TextToolResultModel(text=str(actual_content)),
                                                source_id=citation_source_id,
                                                source_name=tool_name,
                                                source_link=None,
                                                page_number=None,
                                            )
                                            related_documents.append(related_doc)
                                            logger.debug(
                                                f"[MESSAGE_CONVERTER] Added citation-enhanced single document: {citation_source_id}"
                                            )
                                            continue
                                    elif isinstance(actual_parsed, list):
                                        # Direct list with citation source_id
                                        logger.debug(
                                            f"[MESSAGE_CONVERTER] Citation-enhanced direct list with {len(actual_parsed)} items, splitting into individual documents"
                                        )
                                        for rank, item in enumerate(actual_parsed):
                                            if isinstance(item, dict):
                                                item_text = item.get("content", str(item))
                                                source_id = f"{citation_source_id}@{rank}"
                                                
                                                related_doc = RelatedDocumentModel(
                                                    content=TextToolResultModel(text=str(item_text)),
                                                    source_id=source_id,
                                                    source_name=item.get("source_name", tool_name),
                                                    source_link=item.get("source_link"),
                                                    page_number=item.get("page_number"),
                                                )
                                                related_documents.append(related_doc)
                                                logger.debug(
                                                    f"[MESSAGE_CONVERTER] Added related document from citation-enhanced direct list: {source_id}"
                                                )
                                        continue
                                except (json.JSONDecodeError, TypeError, ValueError) as e:
                                    # Actual content is not JSON, treat as single item
                                    logger.debug(f"[MESSAGE_CONVERTER] Citation-enhanced content is not JSON: {e}")
                                    related_doc = RelatedDocumentModel(
                                        content=TextToolResultModel(text=str(actual_content)),
                                        source_id=citation_source_id,
                                        source_name=tool_name,
                                        source_link=None,
                                        page_number=None,
                                    )
                                    related_documents.append(related_doc)
                                    logger.debug(
                                        f"[MESSAGE_CONVERTER] Added citation-enhanced non-JSON document: {citation_source_id}"
                                    )
                                    continue
                            
                            # Handle regular list case (for backward compatibility)
                            elif isinstance(parsed_content, list):
                                logger.debug(
                                    f"[MESSAGE_CONVERTER] Tool result contains list with {len(parsed_content)} items, splitting into individual documents"
                                )
                                # Split list into individual RelatedDocuments
                                for rank, item in enumerate(parsed_content):
                                    if isinstance(item, dict):
                                        # Extract content from the item (use 'content' field, not 'text')
                                        item_text = item.get("content", str(item))
                                        source_id = f"{tool_use_id}@{rank}"
                                        
                                        logger.debug(
                                            f"[MESSAGE_CONVERTER] Creating related document from list item: {source_id}"
                                        )

                                        # Create RelatedDocumentModel for each list item
                                        related_doc = RelatedDocumentModel(
                                            content=TextToolResultModel(text=str(item_text)),
                                            source_id=source_id,
                                            source_name=item.get("source_name", tool_name),
                                            source_link=item.get("source_link"),
                                            page_number=item.get("page_number"),
                                        )
                                        related_documents.append(related_doc)
                                        logger.debug(
                                            f"[MESSAGE_CONVERTER] Added related document from list: {source_id} ({len(item_text)} chars)"
                                        )
                                continue  # Skip the regular processing for this content_item
                        except (json.JSONDecodeError, TypeError, ValueError, SyntaxError) as e:
                            # Not a JSON list or Python literal, continue with regular processing
                            logger.debug(f"[MESSAGE_CONVERTER] Content is not a parseable list: {e}")
                            pass

                        # Check if content contains multiple source_id markers (citation-enhanced text)
                        import re
                        
                        # Updated pattern to handle multiple markers on the same line
                        source_id_pattern = r'(.*?)\s*\[source_id:\s*([^\]]+)\](?:\s*\[source_name:\s*([^\]]+)\])?\s*(?:\s*\[source_link:\s*([^\]]+)\])?'
                        source_id_matches = re.findall(source_id_pattern, content_text, re.MULTILINE)
                        
                        if len(source_id_matches) > 1:
                            # Multiple source_ids found - split into individual RelatedDocuments
                            logger.debug(
                                f"[MESSAGE_CONVERTER] Found {len(source_id_matches)} source_id markers, splitting into individual documents"
                            )
                            
                            for match in source_id_matches:
                                segment_content = match[0].strip() if match[0] else ""
                                segment_source_id = match[1].strip() if match[1] else ""
                                source_name = match[2].strip() if len(match) > 2 and match[2] else None
                                source_link = match[3].strip() if len(match) > 3 and match[3] else None
                                
                                if segment_content:  # Only create document if content is not empty
                                    logger.debug(
                                        f"[MESSAGE_CONVERTER] Creating related document from text segment: {segment_source_id}"
                                    )
                                    
                                    related_doc = RelatedDocumentModel(
                                        content=TextToolResultModel(text=segment_content),
                                        source_id=segment_source_id,
                                        source_name=source_name or tool_name,
                                        source_link=source_link,
                                        page_number=None,
                                    )
                                    related_documents.append(related_doc)
                                    logger.debug(
                                        f"[MESSAGE_CONVERTER] Added related document from text segment: {segment_source_id} ({len(segment_content)} chars, source_name: {source_name}, source_link: {source_link})"
                                    )
                            continue  # Skip the regular processing for this content_item

                        # Regular processing for single or no source_id content
                        # Look for source_id in the content text (format: "[source_id: xxx]")
                        source_id = None
                        if "[source_id:" in content_text:
                            match = re.search(r"\[source_id:\s*([^\]]+)\]", content_text)
                            if match:
                                source_id = match.group(1).strip()
                                # Remove the source_id from display text
                                content_text = re.sub(
                                    r"\s*\[source_id:[^\]]+\]", "", content_text
                                )

                        if not source_id:
                            source_id = f"{tool_use_id}@{i}"

                        logger.debug(
                            f"[MESSAGE_CONVERTER] Creating related document: {source_id}"
                        )

                        # Create RelatedDocumentModel
                        related_doc = RelatedDocumentModel(
                            content=TextToolResultModel(text=str(content_text)),
                            source_id=source_id,
                            source_name=content_item.get("source_name", tool_name),
                            source_link=content_item.get("source_link"),
                            page_number=content_item.get("page_number"),
                        )
                        related_documents.append(related_doc)
                        logger.debug(
                            f"[MESSAGE_CONVERTER] Added related document: {source_id} ({len(content_text)} chars)"
                        )
            else:
                logger.debug(
                    f"[MESSAGE_CONVERTER] Tool result content is not a list: {type(tool_content)}"
                )

        logger.debug(
            f"[MESSAGE_CONVERTER] Extracted {len(related_documents)} related documents from collected tool usage"
        )

    except Exception as e:
        logger.error(
            f"[MESSAGE_CONVERTER] Error extracting related documents from collected tool usage: {e}"
        )
        logger.error(
            f"[MESSAGE_CONVERTER] collected_tool_usage type: {type(collected_tool_usage)}"
        )
        if collected_tool_usage:
            logger.error(
                f"[MESSAGE_CONVERTER] First item: {collected_tool_usage[0] if collected_tool_usage else 'None'}"
            )

    return related_documents


def _extract_text_content_from_agent_result(result: Any) -> str:
    """
    Extract text content from Strands AgentResult.

    According to Strands documentation, AgentResult has:
    - message: Message (the final message from the model)
    - stop_reason: StopReason
    - metrics: EventLoopMetrics
    - state: Any

    The AgentResult.__str__() method extracts text from message.content array.
    """
    # Use AgentResult's built-in __str__ method if available
    if hasattr(result, "__str__"):
        try:
            text = str(result).strip()
            # Check if it's not just the object representation
            if (
                text
                and text != ""
                and not text.startswith("<")
                and not text.endswith(">")
            ):
                return text
        except Exception:
            pass

    # Fallback: Extract from message.content manually
    if hasattr(result, "message") and result.message:
        message = result.message
        if isinstance(message, dict) and "content" in message:
            content_array = message["content"]
            if isinstance(content_array, list):
                for item in content_array:
                    if isinstance(item, dict):
                        # Check for text content
                        if "text" in item:
                            return str(item["text"])
                        # Check for type-based text content (Anthropic format)
                        elif item.get("type") == "text" and "text" in item:
                            return str(item["text"])
        # Handle case where message is a string
        elif isinstance(message, str):
            return message

    return "応答を生成できませんでした。"


def _extract_reasoning_content_from_agent_result(
    result: Any,
) -> ReasoningContentModel | None:
    """
    Extract reasoning content from Strands AgentResult.

    Reasoning content might be in the message content array or as separate attributes.
    """
    logger.debug(
        f"[MESSAGE_CONVERTER] Extracting reasoning - result has message: {hasattr(result, 'message')}"
    )

    # Check if the message contains reasoning content
    if hasattr(result, "message") and result.message:
        message = result.message
        logger.debug(f"[MESSAGE_CONVERTER] Message type: {type(message)}")
        logger.debug(f"[MESSAGE_CONVERTER] Message content: {message}")

        if isinstance(message, dict) and "content" in message:
            content_array = message["content"]
            logger.debug(f"[MESSAGE_CONVERTER] Content array: {content_array}")

            if isinstance(content_array, list):
                for i, item in enumerate(content_array):
                    logger.debug(f"[MESSAGE_CONVERTER] Content item {i}: {item}")
                    if isinstance(item, dict):
                        # Check for Strands reasoning content structure
                        if "reasoningContent" in item:
                            reasoning_data = item["reasoningContent"]
                            if "reasoningText" in reasoning_data:
                                reasoning_text_data = reasoning_data["reasoningText"]
                                reasoning_text = reasoning_text_data.get("text", "")
                                signature = reasoning_text_data.get(
                                    "signature", "strands-reasoning"
                                )

                                logger.debug(
                                    f"[MESSAGE_CONVERTER] Found Strands reasoning content: {len(reasoning_text)} chars"
                                )
                                if reasoning_text:
                                    # Convert signature to bytes if it's a string
                                    signature_bytes = (
                                        signature.encode("utf-8")
                                        if isinstance(signature, str)
                                        else signature
                                    )
                                    return ReasoningContentModel(
                                        content_type="reasoning",
                                        text=str(reasoning_text),
                                        signature=signature,
                                        redacted_content=signature_bytes,
                                    )

    # Check if reasoning should be extracted based on model capabilities
    logger.debug(f"[MESSAGE_CONVERTER] No reasoning content found in message")

    # Return None when no reasoning content is found
    # This prevents unnecessary reasoning content from being added
    logger.debug(f"[MESSAGE_CONVERTER] No reasoning content to extract, returning None")
    return None


def _create_thinking_log_from_agent_result(
    result: Any,
    bot: Any = None,
    collected_tool_usage: list = None,
    collected_reasoning: list = None,
) -> List[SimpleMessageModel] | None:
    """
    Create thinking log from Strands AgentResult.

    The thinking log should contain tool usage information extracted from the agent's execution.
    According to Strands docs, tool usage is recorded in the agent's message history.
    """
    thinking_log = []

    # First, check if there's collected reasoning from callbacks to add to thinking_log
    if collected_reasoning and len(collected_reasoning) > 0:
        # Join all reasoning chunks into a single text
        full_reasoning_text = "".join(collected_reasoning)
        logger.debug(
            f"[MESSAGE_CONVERTER] Adding collected reasoning to thinking_log: {len(full_reasoning_text)} chars from {len(collected_reasoning)} chunks"
        )

        # Create reasoning content model
        reasoning_content = ReasoningContentModel(
            content_type="reasoning",
            text=full_reasoning_text,
            signature="strands-collected-reasoning",
            redacted_content=b"",  # Empty for collected reasoning
        )

        thinking_log.append(
            SimpleMessageModel(role="assistant", content=[reasoning_content])
        )
    else:
        # Fallback: check if there's reasoning content in the result itself
        reasoning_content = _extract_reasoning_content_from_agent_result(result)
        if reasoning_content:
            logger.debug(
                f"[MESSAGE_CONVERTER] Adding extracted reasoning to thinking_log: {len(reasoning_content.text)} chars"
            )
            thinking_log.append(
                SimpleMessageModel(role="assistant", content=[reasoning_content])
            )

    # Check if the final message contains tool usage
    tool_usage_found = False
    if hasattr(result, "message") and result.message:
        message = result.message
        if isinstance(message, dict) and "content" in message:
            content_array = message["content"]
            if isinstance(content_array, list):
                for item in content_array:
                    if isinstance(item, dict):
                        # Check for tool use content
                        if "toolUse" in item:
                            tool_use = item["toolUse"]
                            _add_strands_tool_use_to_thinking_log(thinking_log, tool_use)
                            tool_usage_found = True
                        # Check for tool result content
                        elif "toolResult" in item:
                            tool_result = item["toolResult"]
                            _add_strands_tool_result_to_thinking_log(
                                thinking_log, tool_result
                            )
                            tool_usage_found = True

    # If no tool usage found in message but we have collected tool usage from callbacks,
    # add it to thinking_log
    logger.debug(f"[MESSAGE_CONVERTER] Tool usage found in message: {tool_usage_found}")
    logger.debug(f"[MESSAGE_CONVERTER] Collected tool usage: {collected_tool_usage}")

    if not tool_usage_found and collected_tool_usage:
        logger.debug(
            f"[MESSAGE_CONVERTER] Adding collected tool usage to thinking_log: {len(collected_tool_usage)} items"
        )

        # Group tool usage by toolUseId to ensure proper pairing
        tool_usage_by_id = {}
        for tool_usage_item in collected_tool_usage:
            item_type = tool_usage_item.get("type")
            data = tool_usage_item.get("data", {})
            tool_use_id = data.get("toolUseId", "unknown")

            if tool_use_id not in tool_usage_by_id:
                tool_usage_by_id[tool_use_id] = {"toolUse": None, "toolResult": None}

            tool_usage_by_id[tool_use_id][item_type] = data

        # Add tool usage pairs to thinking_log in correct order
        for tool_use_id, tool_data in tool_usage_by_id.items():
            # Add tool use first
            if tool_data["toolUse"]:
                _add_strands_tool_use_to_thinking_log(thinking_log, tool_data["toolUse"])
                tool_usage_found = True
                logger.debug(
                    f"[MESSAGE_CONVERTER] Added tool use to thinking_log: {tool_data['toolUse'].get('name')}"
                )

            # Then add tool result
            if tool_data["toolResult"]:
                _add_strands_tool_result_to_thinking_log(
                    thinking_log, tool_data["toolResult"]
                )
                logger.debug(
                    f"[MESSAGE_CONVERTER] Added tool result to thinking_log: {tool_use_id}"
                )
    elif not tool_usage_found:
        logger.debug(
            f"[MESSAGE_CONVERTER] No tool usage found in message and no collected tool usage"
        )

    # Note: Removed dummy tool creation as it was causing corruption
    # Tool usage should only be added when actually present in the agent result

    return thinking_log if thinking_log else None


def _add_strands_tool_use_to_thinking_log(
    thinking_log: List[SimpleMessageModel], tool_use: dict
):
    """Add a Strands tool use to thinking log."""
    tool_use_id = tool_use.get("toolUseId", str(ULID()))
    tool_use_content = ToolUseContentModel(
        content_type="toolUse",
        body=ToolUseContentModelBody(
            tool_use_id=tool_use_id,
            name=tool_use.get("name", "unknown_tool"),
            input=tool_use.get("input", {}),
        ),
    )
    thinking_log.append(SimpleMessageModel(role="assistant", content=[tool_use_content]))


def _add_strands_tool_result_to_thinking_log(
    thinking_log: List[SimpleMessageModel], tool_result: dict
):
    """Add a Strands tool result to thinking log."""
    tool_use_id = tool_result.get("toolUseId", str(ULID()))

    # Extract content from tool result
    content_list = []
    if "content" in tool_result:
        for content_item in tool_result["content"]:
            if "text" in content_item:
                content_list.append(TextToolResultModel(text=content_item["text"]))

    if not content_list:
        content_list.append(TextToolResultModel(text="Tool execution completed"))

    tool_result_content = ToolResultContentModel(
        content_type="toolResult",
        body=ToolResultContentModelBody(
            tool_use_id=tool_use_id,
            content=content_list,
            status=tool_result.get("status", "success"),
        ),
    )
    thinking_log.append(SimpleMessageModel(role="user", content=[tool_result_content]))

    # Note: tool_result already processed above, no need for additional processing


def _bot_has_tools(bot: Any) -> bool:
    """Check if bot has tools configured."""
    if not bot:
        return False

    # Check if bot has agent tools configured
    if (
        hasattr(bot, "agent")
        and bot.agent
        and hasattr(bot.agent, "tools")
        and bot.agent.tools
    ):
        return True

    # Check if bot has knowledge sources (knowledge tool)
    if (
        hasattr(bot, "knowledge")
        and bot.knowledge
        and hasattr(bot.knowledge, "source_urls")
        and bot.knowledge.source_urls
    ):
        return True

    # Check if bot has bedrock agent
    if hasattr(bot, "bedrock_agent_id") and bot.bedrock_agent_id:
        return True

    return False


def _get_model_name_from_agent_result(result: Any) -> str:
    """Get model name from Strands AgentResult."""
    logger.debug(f"[MESSAGE_CONVERTER] Getting model name from result")
    logger.debug(
        f"[MESSAGE_CONVERTER] Result attributes: {[attr for attr in dir(result) if not attr.startswith('_')]}"
    )

    # Try to extract model name from various locations
    if hasattr(result, "model_name"):
        logger.debug(f"[MESSAGE_CONVERTER] Found model_name: {result.model_name}")
        return result.model_name

    if hasattr(result, "message") and result.message:
        if isinstance(result.message, dict) and "model" in result.message:
            logger.debug(
                f"[MESSAGE_CONVERTER] Found model in message: {result.message['model']}"
            )
            return result.message["model"]

    if hasattr(result, "metrics") and result.metrics:
        logger.debug(f"[MESSAGE_CONVERTER] Checking metrics for model info")
        # Check if metrics contains model information

    # AgentResult doesn't directly contain model info, use default
    logger.debug(
        f"[MESSAGE_CONVERTER] No model info found, using default: claude-v3.5-sonnet"
    )
    return "claude-v3.5-sonnet"
