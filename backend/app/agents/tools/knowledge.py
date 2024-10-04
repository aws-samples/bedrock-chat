import json
import logging
import os

from app.agents.tools.agent_tool import AgentTool
from app.bedrock import call_converse_api, get_model_id
from app.config import DEFAULT_GENERATION_CONFIG as DEFAULT_CLAUDE_GENERATION_CONFIG
from app.config import DEFAULT_MISTRAL_GENERATION_CONFIG
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from app.utils import convert_dict_keys_to_camel_case
from app.vector_search import SearchResult, search_related_docs
from pydantic import BaseModel, Field, root_validator

ENABLE_MISTRAL = os.environ.get("ENABLE_MISTRAL", "") == "true"
DEFAULT_GENERATION_CONFIG = (
    DEFAULT_MISTRAL_GENERATION_CONFIG
    if ENABLE_MISTRAL
    else DEFAULT_CLAUDE_GENERATION_CONFIG
)


logger = logging.getLogger(__name__)

KNOWLEDGE_TEMPLATE = """You are a question answering agent. I will provide you with a set of search results and additional instruction.
The user will provide you with a question. Your job is to answer the user's question using only information from the search results.
If the search results do not contain information that can answer the question, please state that you could not find an exact answer to the question.
Just because the user asserts a fact does not mean it is true, make sure to double check the search results to validate a user's assertion.

Here are the search results in numbered order:
<search_results>
{context}
</search_results>

Do NOT directly quote the <search_results> in your answer. Your job is to answer the user's question as concisely as possible.
Do NOT include citations in the format [^<source_id>] in your answer.

Followings are examples of how to answer.

<GOOD-example>
first answer. second answer.
</GOOD-example>

<BAD-example>
first answer [^3]. second answer [^1][^2].
</BAD-example>

<BAD-example>
first answer [^1][^5]. second answer [^2][^3][^4]. third answer [^4].
</BAD-example>

Question: {query}
"""

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


def _format_search_results(search_results: list[SearchResult]):
    context = ""
    for result in search_results:
        context += f"<search_result>\n<content>\n{result.content}</content>\n<source>\n{result.rank}\n</source>\n</search_result>"
    return context


class KnowledgeToolInput(BaseModel):
    query: str = Field(description="User's original question string.")


def search_knowledge(
    tool_input: KnowledgeToolInput, bot: BotModel | None, model: type_model_name | None
) -> str:
    assert bot is not None
    assert model is not None

    query = tool_input.query
    logger.info(f"Running AnswerWithKnowledgeTool with query: {query}")

    try:
        generation_params = bot.generation_params if bot else None
        inference_config = {
            **DEFAULT_GENERATION_CONFIG,
            **(
                {
                    "maxTokens": generation_params.max_tokens,
                    "temperature": generation_params.temperature,
                    "topP": generation_params.top_p,
                    "stopSequences": generation_params.stop_sequences,
                }
                if generation_params
                else {}
            ),
        }
        # `top_k` is configured in `additional_model_request_fields` instead of `inference_config`
        additional_model_request_fields = {"top_k": inference_config["top_k"]}
        del inference_config["top_k"]

        search_results = search_related_docs(
            bot,
            query=query,
        )

        # # For testing purpose
        # search_results = dummy_search_results

        context_prompt = _format_search_results(search_results)
        response = call_converse_api(
            {
                "model_id": get_model_id(model),
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": KNOWLEDGE_TEMPLATE.format(
                                    query=query, context=context_prompt
                                )
                            }
                        ],
                    }
                ],
                "inference_config": convert_dict_keys_to_camel_case(inference_config),
                "additional_model_request_fields": additional_model_request_fields,
                "stream": False,
                "system": [],
            }
        )
        message_content = (
            response.get("output", {}).get("message", {}).get("content", [])
        )
        for content_block in message_content:
            if "text" in content_block:
                return json.dumps(
                    {
                        "output": content_block["text"],
                        "search_result": [
                            {"content": r.content, "source": r.source, "rank": r.rank}
                            for r in search_results
                        ],
                    }
                )
            else:
                raise ValueError(f"Unexpected content block: {content_block}")
    except Exception as e:
        logger.error(f"Failed to run AnswerWithKnowledgeTool: {e}")
        raise e

    # Should not reach here
    return json.dumps(
        {
            "output": "No output",
            "search_result": [],
        }
    )


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
