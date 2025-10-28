"""
Simple list tool. For testing purposes only.
"""

import json
import logging
import random

from strands import tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@tool
def simple_list(topic: str, count: int = 5) -> dict:
    """
    Generate a simple list of items for a given topic.

    Args:
        topic: Topic to generate list about (e.g., 'colors', 'fruits', 'countries')
        count: Number of items to return in the list (default: 5, max: 20)

    Returns:
        dict: ToolResult format with list data in json field
    """
    logger.debug(f"[SIMPLE_LIST_V3] Generating list for topic: {topic}, count: {count}")

    # Limit count to reasonable bounds
    count = max(1, min(count, 20))

    try:
        # Get predefined lists or generate based on topic
        items = _generate_items_for_topic(topic.lower().strip(), count)

        # Format as list of dictionaries with source info (same as internet search)
        result_list = []
        for item in items:
            result_list.append(
                {
                    "content": f"Item: {item}",
                    "source_name": f"Simple List Generator - {topic}",
                    "source_link": None,
                }
            )

        logger.debug(
            f"[SIMPLE_LIST_V3] Generated {len(items)} items for topic: {topic}"
        )

        # Return in ToolResult format to prevent Strands from converting to string
        return {
            "status": "success",
            "content": [{"json": result} for result in result_list],
        }

    except Exception as e:
        error_msg = f"Error generating list for topic '{topic}': {str(e)}"
        logger.error(f"[SIMPLE_LIST_V3] {error_msg}")
        return {
            "status": "error",
            "content": [{"text": error_msg}],
        }


def _generate_items_for_topic(topic: str, count: int) -> list[str]:
    """Generate items for a specific topic."""

    # Predefined lists for common topics
    predefined_lists = {
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
            "Gray",
            "Cyan",
            "Magenta",
            "Lime",
            "Indigo",
        ],
        "fruits": [
            "Apple",
            "Banana",
            "Orange",
            "Grape",
            "Strawberry",
            "Pineapple",
            "Mango",
            "Peach",
            "Pear",
            "Cherry",
            "Watermelon",
            "Kiwi",
            "Lemon",
            "Lime",
            "Blueberry",
        ],
        "countries": [
            "Japan",
            "United States",
            "Germany",
            "France",
            "Italy",
            "Spain",
            "Canada",
            "Australia",
            "Brazil",
            "India",
            "China",
            "South Korea",
            "United Kingdom",
            "Mexico",
            "Russia",
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
            "Pig",
            "Sheep",
            "Goat",
            "Chicken",
            "Duck",
            "Fish",
        ],
        "foods": [
            "Pizza",
            "Sushi",
            "Hamburger",
            "Pasta",
            "Rice",
            "Bread",
            "Salad",
            "Soup",
            "Sandwich",
            "Steak",
            "Chicken",
            "Fish",
            "Vegetables",
            "Fruit",
            "Dessert",
        ],
        "sports": [
            "Soccer",
            "Basketball",
            "Tennis",
            "Baseball",
            "Swimming",
            "Running",
            "Cycling",
            "Golf",
            "Volleyball",
            "Badminton",
            "Table Tennis",
            "Boxing",
            "Wrestling",
            "Skiing",
            "Surfing",
        ],
        "programming": [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "C#",
            "Go",
            "Rust",
            "TypeScript",
            "PHP",
            "Ruby",
            "Swift",
            "Kotlin",
            "Scala",
            "R",
            "MATLAB",
        ],
        "cities": [
            "Tokyo",
            "New York",
            "London",
            "Paris",
            "Berlin",
            "Rome",
            "Madrid",
            "Toronto",
            "Sydney",
            "São Paulo",
            "Mumbai",
            "Seoul",
            "Mexico City",
            "Moscow",
            "Cairo",
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
        "months": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        "days": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        "numbers": [
            "One",
            "Two",
            "Three",
            "Four",
            "Five",
            "Six",
            "Seven",
            "Eight",
            "Nine",
            "Ten",
            "Eleven",
            "Twelve",
            "Thirteen",
            "Fourteen",
            "Fifteen",
        ],
    }

    # Check if we have a predefined list
    if topic in predefined_lists:
        available_items = predefined_lists[topic]
        if len(available_items) <= count:
            return available_items
        else:
            # Randomly sample from available items
            return random.sample(available_items, count)

    # For unknown topics, try to generate based on patterns
    return _generate_generic_items(topic, count)


def _generate_generic_items(topic: str, count: int) -> list[str]:
    """Generate generic items when no predefined list exists."""

    # Try to generate based on common patterns
    if "color" in topic:
        base_colors = [
            "Red",
            "Blue",
            "Green",
            "Yellow",
            "Purple",
            "Orange",
            "Pink",
            "Brown",
        ]
        return random.sample(base_colors, min(count, len(base_colors)))

    elif "number" in topic:
        return [str(i) for i in range(1, count + 1)]

    elif "letter" in topic:
        import string

        letters = list(string.ascii_uppercase)
        return letters[:count] if count <= 26 else letters

    elif any(word in topic for word in ["food", "dish", "meal"]):
        foods = [
            "Rice",
            "Bread",
            "Pasta",
            "Salad",
            "Soup",
            "Sandwich",
            "Pizza",
            "Burger",
            "Noodles",
            "Curry",
        ]
        return random.sample(foods, min(count, len(foods)))

    elif any(word in topic for word in ["animal", "pet"]):
        animals = [
            "Dog",
            "Cat",
            "Bird",
            "Fish",
            "Rabbit",
            "Hamster",
            "Horse",
            "Cow",
            "Pig",
            "Sheep",
        ]
        return random.sample(animals, min(count, len(animals)))

    else:
        # Generate generic numbered items
        return [f"{topic.title()} {i+1}" for i in range(count)]


# Additional tool for more structured lists
@tool
def structured_list(
    topic: str, count: int = 5, include_description: bool = False
) -> list[dict]:
    """
    Generate a structured list with optional descriptions.

    Args:
        topic: Topic to generate list about
        count: Number of items to return (default: 5, max: 15)
        include_description: Whether to include brief descriptions (default: False)

    Returns:
        list[dict]: List of structured items with content, source_name, and source_link
    """
    logger.debug(
        f"[STRUCTURED_LIST_V3] Topic: {topic}, count: {count}, descriptions: {include_description}"
    )

    # Limit count for structured lists
    count = max(1, min(count, 15))

    try:
        # Get basic items
        items = _generate_items_for_topic(topic.lower().strip(), count)

        # Format as list of dictionaries with source info (same as internet search)
        result = []
        for item in items:
            if include_description:
                description = _generate_description(item, topic)
                content = f"Item: {item}\nDescription: {description}"
            else:
                content = f"Item: {item}"

            result.append(
                {
                    "content": content,
                    "source_name": f"Structured List Generator - {topic}",
                    "source_link": None,
                }
            )

        logger.debug(
            f"[STRUCTURED_LIST_V3] Generated structured list with {len(items)} items"
        )

        return result

    except Exception as e:
        error_msg = f"Error generating structured list for topic '{topic}': {str(e)}"
        logger.error(f"[STRUCTURED_LIST_V3] {error_msg}")
        return [{"content": error_msg, "source_name": "Error", "source_link": None}]


def _generate_description(item: str, topic: str) -> str:
    """Generate a brief description for an item."""

    # Simple description patterns
    descriptions = {
        # Colors
        "Red": "A warm, vibrant color often associated with passion and energy",
        "Blue": "A cool, calming color often associated with sky and water",
        "Green": "A natural color associated with plants and growth",
        "Yellow": "A bright, cheerful color associated with sunshine",
        # Fruits
        "Apple": "A popular fruit that's crunchy and sweet, available in many varieties",
        "Banana": "A yellow tropical fruit that's soft and sweet when ripe",
        "Orange": "A citrus fruit that's juicy and rich in vitamin C",
        # Animals
        "Dog": "A loyal domestic animal known as man's best friend",
        "Cat": "An independent domestic animal known for being graceful and curious",
        "Elephant": "A large mammal known for its intelligence and memory",
        # Programming languages
        "Python": "A versatile, easy-to-learn programming language popular for data science",
        "JavaScript": "A dynamic programming language essential for web development",
        "Java": "A robust, object-oriented programming language used in enterprise applications",
    }

    # Return specific description if available, otherwise generate generic one
    if item in descriptions:
        return descriptions[item]
    else:
        return f"An item in the {topic} category"
