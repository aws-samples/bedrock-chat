import logging
from typing import TypedDict
from urllib.parse import urlparse

from app.repositories.models.conversation import (
    RelatedDocumentModel,
    TextToolResultModel,
)
from app.repositories.models.custom_bot import BotModel
from app.utils import generate_presigned_url, get_bedrock_agent_client

from botocore.exceptions import ClientError
from mypy_boto3_bedrock_runtime.type_defs import (
    GuardrailConverseContentBlockTypeDef,
)

logger = logging.getLogger(__name__)
agent_client = get_bedrock_agent_client()


class SearchResult(TypedDict):
    bot_id: str
    content: str
    source_name: str
    source_link: str
    rank: int


def search_result_to_related_document(
    search_result: SearchResult,
    source_id_base: str,
) -> RelatedDocumentModel:
    return RelatedDocumentModel(
        content=TextToolResultModel(
            text=search_result["content"],
        ),
        source_id=f"{source_id_base}@{search_result['rank']}",
        source_name=search_result["source_name"],
        source_link=search_result["source_link"],
    )


def to_guardrails_grounding_source(
    search_results: list[SearchResult],
) -> GuardrailConverseContentBlockTypeDef:
    """Convert search results to Guardrails Grounding source format."""
    grounding_source: GuardrailConverseContentBlockTypeDef = {
        "text": {
            "text": "\n\n".join(x["content"] for x in search_results),
            "qualifiers": ["grounding_source"],
        }
    }
    return grounding_source


def _bedrock_knowledge_base_search(bot: BotModel, query: str) -> list[SearchResult]:
    assert (
        bot.bedrock_knowledge_base is not None
        and bot.bedrock_knowledge_base.knowledge_base_id is not None
    )
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

            url = urlparse(url=source)
            if url.scheme == "s3":
                source_name = url.path.split("/")[-1]
                source_link = generate_presigned_url(
                    bucket=url.netloc,
                    key=url.path,
                    client_method="get_object",
                )

            elif url.scheme == "http" or url.scheme == "https":
                source_name = source
                source_link = source

            else:
                # Assume source is a youtube video id
                source_name = source
                source_link = f"https://www.youtube.com/watch?v={source}"

            search_results.append(
                SearchResult(
                    rank=i,
                    bot_id=bot.id,
                    content=content,
                    source_name=source_name,
                    source_link=source_link,
                )
            )

        return search_results

    except ClientError as e:
        logger.error(f"Error querying Bedrock Knowledge Base: {e}")
        raise e


def search_related_docs(bot: BotModel, query: str) -> list[SearchResult]:
    return _bedrock_knowledge_base_search(bot, query)
