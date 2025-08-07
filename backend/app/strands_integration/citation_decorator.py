"""
Citation decorator for Strands integration.
This decorator enhances tool results with source_id information for citation support.
"""

import json
import logging
from functools import wraps
from typing import Any, Callable, TypeVar, Union

from app.repositories.models.conversation import ToolResultModel
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

F = TypeVar('F', bound=Callable[..., Any])


def with_citation_support(display_citation: bool = False, tool_use_id: str = None) -> Callable[[F], F]:
    """
    Decorator to add citation support to all tools in Strands integration.
    
    This decorator enhances tool results with source_id information when citation is enabled.
    It follows the same source_id format as agent_tool.py:
    - Single result: tool_use_id
    - List result: f"{tool_use_id}@{rank}"
    - Dict with source_id: uses provided source_id
    
    Args:
        display_citation: Whether citation display is enabled
        tool_use_id: The tool use ID for source_id generation
    
    Returns:
        Decorator function that enhances tool results with citation information
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(
            tool_input: Any, 
            bot: BotModel | None, 
            model: type_model_name | None,
        ) -> Union[str, dict, ToolResultModel, list]:
            logger.debug(f"[CITATION_DECORATOR] Executing tool function with citation support")
            logger.debug(f"[CITATION_DECORATOR] display_citation: {display_citation}, tool_use_id: {tool_use_id}")
            
            # Execute original function
            result = func(tool_input, bot, model)
            
            # Enhance result with citation information if enabled
            if display_citation and tool_use_id:
                enhanced_result = _enhance_result_with_citation(result, tool_use_id)
                logger.debug(f"[CITATION_DECORATOR] Enhanced result with citation: {type(enhanced_result)}")
                return enhanced_result
            else:
                logger.debug(f"[CITATION_DECORATOR] Citation not enabled, returning original result")
                return result
                
        return wrapper
    return decorator


def _enhance_result_with_citation(result: Any, tool_use_id: str) -> Any:
    """
    Enhance tool result with citation information.
    
    This function embeds source_id information directly in the text content
    so that LLMs can see and reference them according to the citation prompt.
    
    For complex results like simple_list_tool, it tries to embed individual
    source_ids for each item when possible.
    
    Args:
        result: Original tool result
        tool_use_id: Tool use ID for source_id generation
        
    Returns:
        Enhanced result with source_id information embedded in text
    """
    logger.debug(f"[CITATION_DECORATOR] Enhancing result type: {type(result)}")
    
    if isinstance(result, str):
        # Try to parse as JSON to see if it contains a list structure
        try:
            parsed = json.loads(result)
            
            # Check if it's a dict with a list (like simple_list_tool)
            if isinstance(parsed, dict):
                list_keys = ["items", "results", "data", "list", "entries"]
                found_list = None
                found_key = None
                
                for key in list_keys:
                    if key in parsed and isinstance(parsed[key], list):
                        found_list = parsed[key]
                        found_key = key
                        break
                
                if found_list:
                    logger.debug(f"[CITATION_DECORATOR] Found list in '{found_key}' with {len(found_list)} items")
                    
                    # Create individual source_ids for each item
                    enhanced_items = []
                    for i, item in enumerate(found_list):
                        item_source_id = f"{tool_use_id}@{i}"
                        if isinstance(item, dict):
                            # Extract meaningful content from the item
                            content = (
                                item.get("description") or 
                                item.get("content") or 
                                item.get("name") or 
                                str(item)
                            )
                            
                            # Extract metadata
                            source_name = item.get("source_name", "")
                            source_link = item.get("source_link", "")
                            
                            # Create enhanced item with embedded metadata
                            enhanced_item = f"{content} [source_id: {item_source_id}]"
                            if source_name:
                                enhanced_item += f" [source_name: {source_name}]"
                            if source_link:
                                enhanced_item += f" [source_link: {source_link}]"
                        else:
                            enhanced_item = f"{str(item)} [source_id: {item_source_id}]"
                        enhanced_items.append(enhanced_item)
                        logger.debug(f"[CITATION_DECORATOR] Enhanced item {i} with metadata: {item_source_id}")
                    
                    # Join all items with newlines
                    enhanced_content = "\n".join(enhanced_items)
                    logger.debug(f"[CITATION_DECORATOR] Enhanced JSON with list: {len(enhanced_items)} items")
                    return enhanced_content
                else:
                    # Single dict item
                    enhanced_content = f"{result} [source_id: {tool_use_id}]"
                    logger.debug(f"[CITATION_DECORATOR] Enhanced JSON dict with single source_id: {tool_use_id}")
                    return enhanced_content
            
            elif isinstance(parsed, list):
                # Direct list
                enhanced_items = []
                for i, item in enumerate(parsed):
                    item_source_id = f"{tool_use_id}@{i}"
                    if isinstance(item, dict):
                        item_str = json.dumps(item, ensure_ascii=False)
                        enhanced_item = f"{item_str} [source_id: {item_source_id}]"
                    else:
                        enhanced_item = f"{str(item)} [source_id: {item_source_id}]"
                    enhanced_items.append(enhanced_item)
                    logger.debug(f"[CITATION_DECORATOR] Enhanced list item {i} with source_id: {item_source_id}")
                
                enhanced_content = "\n".join(enhanced_items)
                logger.debug(f"[CITATION_DECORATOR] Enhanced direct list: {len(enhanced_items)} items")
                return enhanced_content
            else:
                # Other JSON types
                enhanced_content = f"{result} [source_id: {tool_use_id}]"
                logger.debug(f"[CITATION_DECORATOR] Enhanced JSON with single source_id: {tool_use_id}")
                return enhanced_content
                
        except (json.JSONDecodeError, TypeError):
            # Not JSON, treat as plain string
            enhanced_content = f"{result} [source_id: {tool_use_id}]"
            logger.debug(f"[CITATION_DECORATOR] Enhanced plain string with source_id: {tool_use_id}")
            return enhanced_content
        
    elif isinstance(result, dict):
        # Convert dict to string with embedded source_id
        result_str = json.dumps(result, ensure_ascii=False, indent=2)
        enhanced_content = f"{result_str} [source_id: {tool_use_id}]"
        logger.debug(f"[CITATION_DECORATOR] Enhanced dict result with embedded source_id: {tool_use_id}")
        return enhanced_content
        
    elif isinstance(result, list):
        # Convert each list item to string with embedded source_id
        enhanced_items = []
        for i, item in enumerate(result):
            item_source_id = f"{tool_use_id}@{i}"
            if isinstance(item, dict):
                item_str = json.dumps(item, ensure_ascii=False)
                enhanced_item = f"{item_str} [source_id: {item_source_id}]"
            elif isinstance(item, str):
                enhanced_item = f"{item} [source_id: {item_source_id}]"
            else:
                enhanced_item = f"{str(item)} [source_id: {item_source_id}]"
            enhanced_items.append(enhanced_item)
            logger.debug(f"[CITATION_DECORATOR] Enhanced list item {i} with embedded source_id: {item_source_id}")
        
        # Join all items with newlines
        enhanced_content = "\n".join(enhanced_items)
        logger.debug(f"[CITATION_DECORATOR] Enhanced list result with {len(enhanced_items)} items")
        return enhanced_content
        
    else:
        # For ToolResultModel and other types, return as-is
        logger.debug(f"[CITATION_DECORATOR] Returning result as-is for type: {type(result)}")
        return result
