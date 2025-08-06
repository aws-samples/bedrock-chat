"""
Citation decorator for Strands integration.
This decorator enhances tool results with source_id information for citation support.
"""

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
    
    This function follows the same logic as agent_tool.py's _function_result_to_related_document
    for source_id generation:
    - str -> dict with source_id
    - dict -> add source_id if not present
    - list -> add source_id with @rank suffix to each item
    - ToolResultModel -> return as-is (already processed)
    
    Args:
        result: Original tool result
        tool_use_id: Tool use ID for source_id generation
        
    Returns:
        Enhanced result with source_id information
    """
    logger.debug(f"[CITATION_DECORATOR] Enhancing result type: {type(result)}")
    
    if isinstance(result, str):
        # Convert string to dict with source_id
        enhanced = {
            "content": result,
            "source_id": tool_use_id,
        }
        logger.debug(f"[CITATION_DECORATOR] Enhanced string result with source_id: {tool_use_id}")
        return enhanced
        
    elif isinstance(result, dict):
        # Add source_id if not already present
        if "source_id" not in result:
            result["source_id"] = tool_use_id
            logger.debug(f"[CITATION_DECORATOR] Added source_id to dict: {tool_use_id}")
        else:
            logger.debug(f"[CITATION_DECORATOR] Dict already has source_id: {result['source_id']}")
        return result
        
    elif isinstance(result, list):
        # Add source_id with @rank suffix to each item
        enhanced_list = []
        for i, item in enumerate(result):
            if isinstance(item, dict):
                if "source_id" not in item:
                    item["source_id"] = f"{tool_use_id}@{i}"
                    logger.debug(f"[CITATION_DECORATOR] Added source_id to list item {i}: {tool_use_id}@{i}")
                enhanced_list.append(item)
            elif isinstance(item, str):
                enhanced_item = {
                    "content": item,
                    "source_id": f"{tool_use_id}@{i}",
                }
                logger.debug(f"[CITATION_DECORATOR] Enhanced list string item {i} with source_id: {tool_use_id}@{i}")
                enhanced_list.append(enhanced_item)
            else:
                # For other types (like ToolResultModel), keep as-is
                enhanced_list.append(item)
        return enhanced_list
        
    else:
        # For ToolResultModel and other types, return as-is
        logger.debug(f"[CITATION_DECORATOR] Returning result as-is for type: {type(result)}")
        return result
