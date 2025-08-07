"""
Tool registry for Strands integration with citation support.
"""

import logging
import time
import random
import json
import inspect
from typing import Optional

from strands import tool

from app.agents.tools.agent_tool import AgentTool
from app.strands_integration.tools.calculator_tool_strands import calculator
from app.strands_integration.tools.internet_search_tool_strands import create_internet_search_tool
from app.strands_integration.tools.bedrock_agent_tool_strands import bedrock_agent_invoke
from app.strands_integration.tools.knowledge_tool_strands import knowledge_search
from app.strands_integration.citation_decorator import _enhance_result_with_citation
from app.repositories.models.custom_bot import BotModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def convert_strands_args_kwargs_to_tool_params(tool_func, strands_input: dict) -> dict:
    """
    Convert Strands args/kwargs format to proper tool parameters.
    
    This function provides the same conversion logic used in citation wrapper
    but can be reused in other contexts like callback handlers.
    
    Args:
        tool_func: The tool function to get signature from
        strands_input: Input dict with 'args' and 'kwargs' keys
        
    Returns:
        Dict with converted parameters suitable for the tool
    """
    logger.debug(f"[TOOL_REGISTRY] Converting Strands input: {strands_input}")
    
    # Check if this is Strands args/kwargs format
    if 'args' not in strands_input or 'kwargs' not in strands_input:
        # Not Strands format, return as-is
        return strands_input
    
    # Extract the main argument from 'args'
    main_arg_value = strands_input['args']
    
    # Parse the 'kwargs' JSON string
    strands_kwargs_str = strands_input['kwargs']
    try:
        strands_kwargs = json.loads(strands_kwargs_str)
        logger.debug(f"[TOOL_REGISTRY] Parsed Strands kwargs: {strands_kwargs}")
    except json.JSONDecodeError as e:
        logger.error(f"[TOOL_REGISTRY] Failed to parse Strands kwargs JSON: {e}")
        strands_kwargs = {}
    
    # Merge with other parameters (excluding args/kwargs)
    merged_kwargs = {k: v for k, v in strands_input.items() if k not in ['args', 'kwargs']}
    merged_kwargs.update(strands_kwargs)
    
    # Dynamically determine the main parameter name from tool signature
    # If tool has _original_func (citation wrapper), use that for signature inspection
    func_for_signature = getattr(tool_func, '_original_func', tool_func)
    sig = inspect.signature(func_for_signature)
    param_names = list(sig.parameters.keys())
    
    if param_names:
        # Use the first parameter as the main argument
        main_param_name = param_names[0]
        merged_kwargs[main_param_name] = main_arg_value
        logger.debug(f"[TOOL_REGISTRY] Mapped args to '{main_param_name}': {main_arg_value}")
    else:
        logger.warning(f"[TOOL_REGISTRY] Tool has no parameters, cannot map args")
    
    # Filter kwargs to only include parameters that the tool accepts
    valid_param_names = set(param_names)
    filtered_kwargs = {k: v for k, v in merged_kwargs.items() if k in valid_param_names}
    
    if len(filtered_kwargs) != len(merged_kwargs):
        ignored_params = set(merged_kwargs.keys()) - valid_param_names
        logger.debug(f"[TOOL_REGISTRY] Ignored unsupported parameters: {ignored_params}")
    
    logger.debug(f"[TOOL_REGISTRY] Converted parameters: {filtered_kwargs}")
    return filtered_kwargs


def get_tools_for_bot(bot: Optional[BotModel], display_citation: bool = False) -> list:
    """
    Get tools for bot configuration with optional citation support.
    
    Converts AgentTool instances to Strands-compatible DecoratedFunctionTool
    using the @tool decorator. When display_citation=True, tools will embed 
    source_id information in their results.
    
    Args:
        bot: Bot configuration (None for no tools)
        display_citation: Whether to enable citation support
        
    Returns:
        List of Strands-compatible DecoratedFunctionTool objects
    """
    logger.debug(f"[TOOL_REGISTRY] Getting tools for bot: {bot.id if bot else None}")
    logger.debug(f"[TOOL_REGISTRY] Citation enabled: {display_citation}")
    
    tools = []
    
    # Return empty list if no bot or agent not enabled
    if not bot or not bot.is_agent_enabled():
        logger.debug(f"[TOOL_REGISTRY] No bot or agent not enabled, returning empty tools")
        return tools
    
    # Get available Strands tools from agent configuration
    available_tools = {
        "internet_search": lambda bot: create_internet_search_tool(bot),
        "bedrock_agent": lambda bot: bedrock_agent_invoke,  # bedrock_agent is already a tool
        "calculator": lambda bot: calculator,  # calculator doesn't need bot context
    }
    
    # Add configured tools from bot
    for tool_config in bot.agent.tools:
        tool_name = tool_config.name
        if tool_name in available_tools:
            tool_factory = available_tools[tool_name]
            
            # Create Strands tool (some need bot context, some don't)
            if callable(tool_factory):
                strands_tool = tool_factory(bot)
            else:
                strands_tool = tool_factory
            
            # Add citation support if enabled
            if display_citation:
                strands_tool = _add_citation_support(strands_tool, tool_name)
            
            tools.append(strands_tool)
            logger.debug(f"[TOOL_REGISTRY] Added Strands tool: {tool_name} (citation: {display_citation})")
    
    # Add knowledge tool if bot has knowledge base
    if bot.has_knowledge():
        knowledge_tool = knowledge_search
        
        # Add citation support if enabled
        if display_citation:
            knowledge_tool = _add_citation_support(knowledge_tool, "knowledge")
        
        tools.append(knowledge_tool)
        logger.debug(f"[TOOL_REGISTRY] Added Strands knowledge tool (citation: {display_citation})")
    
    logger.debug(f"[TOOL_REGISTRY] Total tools created: {len(tools)}")
    
    # Debug: Log tool types and names
    for i, tool in enumerate(tools):
        logger.debug(f"[TOOL_REGISTRY] Tool {i}: type={type(tool)}")
        if hasattr(tool, 'tool_name'):
            logger.debug(f"[TOOL_REGISTRY] Tool {i}: tool_name={tool.tool_name}")
        logger.debug(f"[TOOL_REGISTRY] Tool {i}: callable={callable(tool)}")
    
    return tools


def _add_citation_support(strands_tool, tool_name: str):
    """
    Add citation support to an existing Strands tool.
    
    This function wraps a Strands tool to add source_id information
    to its results for citation purposes using the proper citation
    enhancement logic from citation_decorator.
    
    Args:
        strands_tool: Existing Strands DecoratedFunctionTool
        tool_name: Name of the tool for source_id generation
        
    Returns:
        Enhanced Strands tool with citation support
    """
    logger.debug(f"[TOOL_REGISTRY] Adding citation support to tool: {tool_name}")
    
    # Get the original function from the Strands tool
    original_func = strands_tool._func if hasattr(strands_tool, '_func') else strands_tool
    
    # Create wrapper function that adds citation
    def citation_wrapper(*args, **kwargs):
        """Wrapper that adds citation information to tool results."""
        logger.debug(f"[TOOL_REGISTRY] Executing citation wrapper for {tool_name}")
        logger.debug(f"[TOOL_REGISTRY] Citation wrapper args: {args}")
        logger.debug(f"[TOOL_REGISTRY] Citation wrapper kwargs: {kwargs}")
        
        try:
            # Handle Strands args/kwargs format conversion
            if 'args' in kwargs and 'kwargs' in kwargs:
                logger.debug(f"[TOOL_REGISTRY] Converting Strands args/kwargs format")
                
                # Use the common conversion function
                converted_kwargs = convert_strands_args_kwargs_to_tool_params(original_func, kwargs)
                
                # Execute with converted parameters
                result = original_func(**converted_kwargs)
            else:
                # Normal execution path
                result = original_func(*args, **kwargs)
                
            logger.debug(f"[TOOL_REGISTRY] Original tool result: {result}")
            
            # Generate unique source_id
            source_id = f"{tool_name}_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Use proper citation enhancement logic from citation_decorator
            enhanced_result = _enhance_result_with_citation(result, source_id)
            
            logger.debug(f"[TOOL_REGISTRY] Enhanced result with citation: {type(enhanced_result)}")
            return enhanced_result
            
        except Exception as e:
            logger.error(f"[TOOL_REGISTRY] Citation wrapper execution failed: {e}")
            return f"Error executing {tool_name}: {str(e)}"
    
    # Copy metadata from original function
    citation_wrapper.__name__ = getattr(original_func, '__name__', tool_name)
    citation_wrapper.__doc__ = getattr(original_func, '__doc__', f"Enhanced {tool_name} with citation support")
    
    # Apply Strands @tool decorator to create new DecoratedFunctionTool
    enhanced_tool = tool(citation_wrapper)
    
    # Store reference to original function for signature inspection
    enhanced_tool._original_func = original_func
    
    logger.debug(f"[TOOL_REGISTRY] Created citation-enhanced tool: {tool_name}")
    return enhanced_tool
