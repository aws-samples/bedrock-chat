"""
Simple list tool for testing citation/reference functionality.
Returns a list of items to test how citations work with array results.
"""

import json
import logging
from typing import Any

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SimpleListInput(BaseModel):
    topic: str = Field(
        description="Topic to generate a simple list about (e.g., 'colors', 'fruits', 'countries')"
    )
    count: int = Field(
        default=5,
        description="Number of items to return in the list (default: 5, max: 10)",
    )


def generate_simple_list(topic: str, count: int = 5) -> str:
    """
    Generate a simple list of items based on the topic.

    Args:
        topic: Topic to generate list about
        count: Number of items to return

    Returns:
        str: JSON string containing list of items
    """
    logger.info(
        f"[SIMPLE_LIST_TOOL] Generating list for topic: {topic}, count: {count}"
    )

    # Limit count to reasonable range
    count = max(1, min(count, 10))

    # Predefined lists for different topics
    topic_data = {
        "colors": [
            "Red",
            "Blue",
            "Green",
            "Yellow",
            "Purple",
            "Orange",
            "Pink",
            "Brown",
            "Black",
            "White",
        ],
        "fruits": [
            "Apple",
            "Banana",
            "Orange",
            "Grape",
            "Strawberry",
            "Pineapple",
            "Mango",
            "Kiwi",
            "Peach",
            "Cherry",
        ],
        "countries": [
            "Japan",
            "United States",
            "Germany",
            "France",
            "Brazil",
            "Australia",
            "Canada",
            "India",
            "China",
            "United Kingdom",
        ],
        "animals": [
            "Dog",
            "Cat",
            "Elephant",
            "Lion",
            "Tiger",
            "Bear",
            "Rabbit",
            "Horse",
            "Cow",
            "Sheep",
        ],
        "programming": [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "Go",
            "Rust",
            "TypeScript",
            "Swift",
            "Kotlin",
            "Ruby",
        ],
        "planets": [
            "Mercury",
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
            "Neptune",
        ],
    }

    # Get items for the topic (case insensitive)
    topic_lower = topic.lower()
    items = topic_data.get(topic_lower, [f"Item {i+1} for {topic}" for i in range(10)])

    # Select the requested number of items
    selected_items = items[:count]

    # Create result as list of dictionaries with metadata
    result_items = []
    for i, item in enumerate(selected_items):
        result_items.append(
            {
                "id": f"{topic_lower}_{i+1}",
                "name": item,
                "description": f"This is {item}, item #{i+1} in the {topic} category",
                "source": f"Simple List Tool - {topic} category",
                "source_name": f"Simple List Source - {item}",
                "source_link": f"https://example.com/{topic_lower}/{item.lower().replace(' ', '-')}",
                "index": i + 1,
            }
        )

    result = {"topic": topic, "count": len(result_items), "items": result_items}

    logger.info(
        f"[SIMPLE_LIST_TOOL] Generated {len(result_items)} items for topic: {topic}"
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


def _simple_list_function(
    input_data: SimpleListInput,
    bot: BotModel | None,
    model: type_model_name | None,
) -> str:
    """
    Simple list tool function for AgentTool.

    Args:
        input_data: Simple list input containing topic and count
        bot: Bot model (not used for simple list)
        model: Model name (not used for simple list)

    Returns:
        str: JSON string containing list of items
    """
    return generate_simple_list(input_data.topic, input_data.count)


# Create the simple list tool instance
simple_list_tool = AgentTool(
    name="simple_list",
    description="Generate a simple list of items for a given topic. Useful for testing citation and reference functionality.",
    args_schema=SimpleListInput,
    function=_simple_list_function,
)
