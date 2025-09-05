"""
Calculator tool. For testing and demonstration purposes only.
"""

import logging
import math
import operator
import re

from app.repositories.models.custom_bot import BotModel
from strands import tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_calculator_tool(bot: BotModel | None = None):
    """Create calculator tool with bot context closure."""

    @tool
    def calculator(expression: str) -> str:
        """
        Perform mathematical calculations safely.

        Args:
            expression: Mathematical expression to evaluate (e.g., "2+2", "10*5", "sqrt(16)", "sin(30)")

        Returns:
            str: Result of the calculation or error message
        """
        logger.debug(f"[CALCULATOR_V3] Bot context: {bot.id if bot else 'None'}")
        logger.debug(f"[CALCULATOR_V3] Evaluating expression: {expression}")

        try:
            # Clean the expression
            expression = expression.strip()

            # Replace common mathematical functions and constants
            expression = _prepare_expression(expression)

            # Define safe operations
            safe_dict = {
                "__builtins__": {},
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum,
                "pow": pow,
                # Math functions
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "asin": math.asin,
                "acos": math.acos,
                "atan": math.atan,
                "log": math.log,
                "log10": math.log10,
                "exp": math.exp,
                "floor": math.floor,
                "ceil": math.ceil,
                # Constants
                "pi": math.pi,
                "e": math.e,
            }

            # Validate expression for safety
            if not _is_safe_expression(expression):
                logger.warning(
                    f"[CALCULATOR_V3] Unsafe expression detected: {expression}"
                )
                return f"Error: Expression contains unsafe operations: {expression}"

            # Evaluate the expression
            result = eval(expression, safe_dict, {})

            # Format the result
            if isinstance(result, float):
                # Remove unnecessary decimal places
                if result.is_integer():
                    formatted_result = str(int(result))
                else:
                    # Round to 10 decimal places to avoid floating point precision issues
                    formatted_result = f"{result:.10f}".rstrip("0").rstrip(".")
            else:
                formatted_result = str(result)

            logger.debug(f"[CALCULATOR_V3] Result: {formatted_result}")
            return formatted_result

        except ZeroDivisionError:
            error_msg = "Error: Division by zero"
            logger.warning(f"[CALCULATOR_V3] {error_msg}")
            return error_msg
        except ValueError as e:
            error_msg = f"Error: Invalid value - {str(e)}"
            logger.warning(f"[CALCULATOR_V3] {error_msg}")
            return error_msg
        except SyntaxError as e:
            error_msg = f"Error: Invalid syntax - {str(e)}"
            logger.warning(f"[CALCULATOR_V3] {error_msg}")
            return error_msg
        except Exception as e:
            error_msg = f"Error: Calculation failed - {str(e)}"
            logger.error(f"[CALCULATOR_V3] {error_msg}")
            return error_msg

    return calculator


def create_advanced_calculator_tool(bot: BotModel | None = None):
    """Create advanced calculator tool with bot context closure."""

    @tool
    def advanced_calculator(expression: str, precision: int = 6) -> str:
        """
        Perform advanced mathematical calculations with custom precision.

        Args:
            expression: Mathematical expression to evaluate
            precision: Number of decimal places for the result (default: 6, max: 15)

        Returns:
            str: Result of the calculation with specified precision
        """
        logger.debug(
            f"[ADVANCED_CALCULATOR_V3] Bot context: {bot.id if bot else 'None'}"
        )
        logger.debug(
            f"[ADVANCED_CALCULATOR_V3] Expression: {expression}, Precision: {precision}"
        )

        # Limit precision to reasonable bounds
        precision = max(0, min(precision, 15))

        # Use the basic calculator first
        basic_calc = create_calculator_tool(bot)
        result = basic_calc(expression)

        # If it's an error, return as-is
        if result.startswith("Error:"):
            return result

        try:
            # Try to apply custom precision
            numeric_result = float(result)

            if numeric_result.is_integer():
                formatted_result = str(int(numeric_result))
            else:
                formatted_result = f"{numeric_result:.{precision}f}".rstrip("0").rstrip(
                    "."
                )

            logger.debug(
                f"[ADVANCED_CALCULATOR_V3] Formatted result: {formatted_result}"
            )
            return formatted_result

        except ValueError:
            # If we can't parse as float, return the original result
            return result

    return advanced_calculator


def _prepare_expression(expression: str) -> str:
    """Prepare expression by replacing common mathematical notations."""
    # Replace common mathematical notations
    replacements = {
        "×": "*",
        "÷": "/",
        "^": "**",
        "π": "pi",
        # Handle implicit multiplication (e.g., "2pi" -> "2*pi")
        r"(\d+)(pi|e)": r"\1*\2",
        r"(\d+)(\w+)": r"\1*\2",  # 2x -> 2*x (but be careful with function names)
    }

    for pattern, replacement in replacements.items():
        if pattern.startswith("r"):
            # Regex replacement
            expression = re.sub(pattern[1:], replacement, expression)
        else:
            # Simple string replacement
            expression = expression.replace(pattern, replacement)

    return expression


def _is_safe_expression(expression: str) -> bool:
    """Check if expression is safe to evaluate."""
    # List of dangerous patterns
    dangerous_patterns = [
        "__",  # Dunder methods
        "import",
        "exec",
        "eval",
        "open",
        "file",
        "input",
        "raw_input",
        "compile",
        "globals",
        "locals",
        "vars",
        "dir",
        "hasattr",
        "getattr",
        "setattr",
        "delattr",
        "callable",
    ]

    expression_lower = expression.lower()
    for pattern in dangerous_patterns:
        if pattern in expression_lower:
            return False

    return True
