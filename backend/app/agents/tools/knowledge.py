import logging

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from app.vector_search import SearchResult, search_related_docs

from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)

# For testing purpose
dummy_search_results = [
    SearchResult(
        bot_id="dummy",
        content=r["chunkBody"],  # type: ignore
        source=r["sourceLink"],  # type: ignore
        rank=r["rank"],  # type: ignore
    )
    for r in [
        {
            "chunkBody": "Sushi is one of the most representative dishes of Japan, consisting of vinegared rice topped with raw fish, vegetables, or other ingredients. Originating in the Edo period, it is now enjoyed worldwide.",
            "contentType": "s3",
            "sourceLink": "",
            "rank": 0,
        },
        {
            "chunkBody": "Ramen is a popular Japanese noodle dish that originated in China. There are various types of broth, such as pork bone, soy sauce, miso, and salt, each with regional characteristics.",
            "contentType": "s3",
            "sourceLink": "",
            "rank": 1,
        },
        {
            "chunkBody": "Curry rice is a dish that combines Indian curry with Japanese rice and is considered one of Japan's national dishes. There are many variations in the roux and toppings used.",
            "contentType": "s3",
            "sourceLink": "",
            "rank": 2,
        },
        {
            "chunkBody": "Tempura is a Japanese dish consisting of battered and deep-fried ingredients such as shrimp, vegetables, and fish. It is characterized by its crispy texture and the flavor of the batter.",
            "contentType": "s3",
            "sourceLink": "",
            "rank": 3,
        },
        {
            "chunkBody": "Okonomiyaki is a popular Japanese savory pancake made with a batter of wheat flour and water, mixed with ingredients such as cabbage, meat, and seafood, and cooked on a griddle. The Kansai and Hiroshima styles are famous.",
            "contentType": "s3",
            "sourceLink": "",
            "rank": 4,
        },
    ]
]


class KnowledgeToolInput(BaseModel):
    query: str = Field(description="User's original question string.")


def search_knowledge(
    tool_input: KnowledgeToolInput, bot: BotModel | None, model: type_model_name | None
) -> list:
    assert bot is not None

    query = tool_input.query
    logger.info(f"Running AnswerWithKnowledgeTool with query: {query}")

    try:
        search_results = search_related_docs(
            bot,
            query=query,
        )

        # # For testing purpose
        # search_results = dummy_search_results

        return [
            {
                "content": r.content,
                "source": r.source,
                "rank": r.rank,
            }
            for r in search_results
        ]

    except Exception as e:
        logger.error(f"Failed to run AnswerWithKnowledgeTool: {e}")
        raise e


def create_knowledge_tool(bot: BotModel, model: type_model_name) -> AgentTool:
    description = (
        "Answer a user's question using information. The description is: {}".format(
            bot.knowledge.__str_in_claude_format__()
        )
    )
    logger.info(f"Creating knowledge base tool with description: {description}")
    return AgentTool(
        name=f"knowledge_base_tool",
        description=description,
        args_schema=KnowledgeToolInput,
        function=search_knowledge,
        bot=bot,
        model=model,
    )
