"""
Calculator tool for Strands integration.
This is a thin wrapper around the traditional AgentTool calculator implementation.
"""

import logging

# Import the core calculator function from the traditional AgentTool
from app.agents.tools.calculator import calculate_expression
from strands import tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2+2", "10*5", "100/4")

    Returns:
        str: Result of the calculation
    """
    logger.debug(f"[STRANDS_CALCULATOR_TOOL] Delegating to core calculator: {expression}")

    # Delegate to the core calculator implementation
    result = calculate_expression(expression)

    logger.debug(f"[STRANDS_CALCULATOR_TOOL] Core calculator result: {result}")
    return result


# For testing purposes, also create a more complex calculator
@tool
def advanced_calculator(expression: str, precision: int = 6) -> str:
    """
    Perform advanced mathematical calculations with custom precision.

    Args:
        expression: Mathematical expression to evaluate
        precision: Number of decimal places for the result (default: 6)

    Returns:
        str: Result of the calculation with specified precision
    """
    logger.debug(
        f"[STRANDS_ADVANCED_CALCULATOR_TOOL] Calculating: {expression} with precision: {precision}"
    )

    # Use the core calculator function
    result_str = calculate_expression(expression)

    # If it's an error message, return as-is
    if result_str.startswith("Error:"):
        return result_str

    try:
        # Try to parse the result and apply custom precision
        result = float(result_str)

        # Format with custom precision
        if result.is_integer():
            formatted_result = str(int(result))
        else:
            formatted_result = f"{result:.{precision}f}".rstrip("0").rstrip(".")

        logger.debug(
            f"[STRANDS_ADVANCED_CALCULATOR_TOOL] Formatted result: {formatted_result}"
        )
        return formatted_result

    except ValueError:
        # If parsing fails, return the original result
        logger.debug(
            f"[STRANDS_ADVANCED_CALCULATOR_TOOL] Could not parse result, returning as-is: {result_str}"
        )
        return result_str
