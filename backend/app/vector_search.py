import json
import logging
import re
from typing import Any, Literal

from app.bedrock import calculate_query_embedding
from app.repositories.custom_bot import find_public_bot_by_id
from app.repositories.models.custom_bot import BotModel
from app.utils import generate_presigned_url, get_bedrock_agent_client, query_postgres
from botocore.exceptions import ClientError
from pydantic import BaseModel

logger = logging.getLogger(__name__)
agent_client = get_bedrock_agent_client()


class SearchResult(BaseModel):
    bot_id: str
    content: str
    source: str
    rank: int


def to_guardrails_grounding_source(
    search_results: list[SearchResult],
) -> dict:
    """Convert search results to Guardrails Grounding source format."""
    grounding_source = {
        "text": {
            "text": "\n\n".join(x.content for x in search_results),
            "qualifiers": ["grounding_source"],
        }
    }
    return grounding_source


def filter_used_results(
    generated_text: str, search_results: list[SearchResult]
) -> list[SearchResult]:
    """Filter the search results based on the citations in the generated text.
    Note that the citations in the generated text are in the format of [^rank].
    """
    used_results: list[SearchResult] = []

    try:
        # Extract citations from the generated text
        citations = [
            citation.strip("[]^")
            for citation in re.findall(r"\[\^(\d+)\]", generated_text)
        ]
    except Exception as e:
        logger.error(f"Error extracting citations from the generated text: {e}")
        return used_results

    for result in search_results:
        if str(result.rank) in citations:
            used_results.append(result)

    return used_results


def get_source_link(source: str) -> tuple[Literal["s3", "url"], str]:
    if source.startswith("s3://"):
        s3_path = source[5:]  # Remove "s3://" prefix
        path_parts = s3_path.split("/", 1)
        bucket_name = path_parts[0]
        object_key = path_parts[1] if len(path_parts) > 1 else ""

        source_link = generate_presigned_url(
            bucket=bucket_name,
            key=object_key,
            client_method="get_object",
        )
        return "s3", source_link
    elif source.startswith("http://") or source.startswith("https://"):
        return "url", source
    else:
        # Assume source is a youtube video id
        return "url", f"https://www.youtube.com/watch?v={source}"


def _pgvector_search(bot_id: str, limit: int, query: str) -> list[SearchResult]:
    """Search to fetch top n most related documents from pgvector.
    Args:
        bot_id (str): bot id
        limit (int): number of results to return
        query (str): query string
    Returns:
        list[SearchResult]: list of search results
    """
    query_embedding = calculate_query_embedding(query)
    logger.info(f"query_embedding: {query_embedding}")

    search_query = """
SELECT id, botid, content, source, embedding 
FROM items 
WHERE botid = %s 
ORDER BY embedding <-> %s 
LIMIT %s
"""

    results = query_postgres(search_query, (bot_id, json.dumps(query_embedding), limit))
    # NOTE: results should be:
    # [
    #     ('123', 'bot_1', 'content_1', 'source_1', [0.123, 0.456, 0.789]),
    #     ('124', 'bot_1', 'content_2', 'source_2', [0.234, 0.567, 0.890]),
    #     ...
    # ]
    return [
        SearchResult(rank=i, bot_id=r[1], content=r[2], source=r[3])
        for i, r in enumerate(results)
    ]


def _bedrock_knowledge_base_search(bot: BotModel, query: str) -> list[SearchResult]:
    assert bot.bedrock_knowledge_base is not None
    if bot.bedrock_knowledge_base.search_params.search_type == "semantic":
        search_type = "SEMANTIC"
    elif bot.bedrock_knowledge_base.search_params.search_type == "hybrid":
        search_type = "HYBRID"
    else:
        raise ValueError("Invalid search type")

    limit = bot.bedrock_knowledge_base.search_params.max_results
    knowledge_base_id = bot.bedrock_knowledge_base.knowledge_base_id

    try:
        response = agent_client.retrieve(
            knowledgeBaseId=knowledge_base_id,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": limit,
                    "overrideSearchType": search_type,
                }
            },
        )

        search_results = []
        for i, retrieval_result in enumerate(response.get("retrievalResults", [])):
            content = retrieval_result.get("content", {}).get("text", "")
            source = (
                retrieval_result.get("location", {})
                .get("s3Location", {})
                .get("uri", "")
            )

            search_results.append(
                SearchResult(rank=i, bot_id=bot.id, content=content, source=source)
            )

        return search_results

    except ClientError as e:
        logger.error(f"Error querying Bedrock Knowledge Base: {e}")
        raise e


def search_related_docs(bot: BotModel, query: str) -> list[SearchResult]:
    if bot.has_bedrock_knowledge_base():
        logger.info("Searching related documents using Bedrock Knowledge Base.")
        return _bedrock_knowledge_base_search(bot, query)
    logger.info("Searching related documents using pgvector.")
    return _pgvector_search(bot.id, bot.search_params.max_results, query)
