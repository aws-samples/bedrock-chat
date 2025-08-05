"""
Calculator tool for mathematical calculations.
The purpose of this tool is for testing.
"""

import logging
import re
from typing import Any

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CalculatorInput(BaseModel):
    expression: str = Field(
        description="Mathematical expression to evaluate (e.g., '2+2', '10*5', '100/4')"
    )


def calculate_expression(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        str: Result of the calculation or error message
    """
    logger.info(f"[CALCULATOR_TOOL] Calculating expression: {expression}")

    try:
        # Clean the expression - remove spaces
        cleaned_expression = expression.replace(" ", "")
        logger.debug(f"[CALCULATOR_TOOL] Cleaned expression: {cleaned_expression}")

        # Validate expression contains only allowed characters
        if not re.match(r"^[0-9+\-*/().]+$", cleaned_expression):
            logger.warning(
                f"[CALCULATOR_TOOL] Invalid characters in expression: {expression}"
            )
            return "Error: Invalid characters in expression. Only numbers and basic operators (+, -, *, /, parentheses) are allowed."

        # Check for division by zero
        if "/0" in cleaned_expression:
            logger.error(
                f"[CALCULATOR_TOOL] Division by zero in expression: {expression}"
            )
            return "Error: Division by zero is not allowed."

        # Safely evaluate the expression
        result = eval(cleaned_expression)
        logger.debug(f"[CALCULATOR_TOOL] Calculation result: {result}")

        # Format the result
        if isinstance(result, float) and result.is_integer():
            formatted_result = str(int(result))
        else:
            formatted_result = str(result)

        logger.debug(f"[CALCULATOR_TOOL] Formatted result: {formatted_result}")
        return formatted_result

    except ZeroDivisionError:
        logger.error(f"[CALCULATOR_TOOL] Division by zero in expression: {expression}")
        return "Error: Division by zero is not allowed."
    except Exception as e:
        logger.error(
            f"[CALCULATOR_TOOL] Error calculating expression '{expression}': {e}"
        )
        return f"Error: Unable to calculate the expression. Please check the syntax."


def _calculator_function(
    input_data: CalculatorInput,
    bot: BotModel | None,
    model: type_model_name | None,
) -> str:
    """
    Calculator tool function for AgentTool.

    Args:
        input_data: Calculator input containing the expression
        bot: Bot model (not used for calculator)
        model: Model name (not used for calculator)

    Returns:
        str: Calculation result
    """
    return calculate_expression(input_data.expression)


# Backward compatibility alias
_calculate_expression = calculate_expression


# Create the calculator tool instance
calculator_tool = AgentTool(
    name="calculator",
    description="Perform mathematical calculations like addition, subtraction, multiplication, and division",
    args_schema=CalculatorInput,
    function=_calculator_function,
)
