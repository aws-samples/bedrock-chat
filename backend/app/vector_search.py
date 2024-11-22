import logging
from typing import TypedDict
from urllib.parse import urlparse

from app.repositories.models.conversation import (
    RelatedDocumentModel,
    TextToolResultModel,
)
from app.repositories.models.custom_bot import BotModel
from app.utils import get_bedrock_agent_client

from botocore.exceptions import ClientError
from mypy_boto3_bedrock_runtime.type_defs import (
    GuardrailConverseContentBlockTypeDef,
)
from mypy_boto3_bedrock_agent_runtime.type_defs import (
    KnowledgeBaseRetrievalResultTypeDef,
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

        def extract_source_from_retrieval_result(
            retrieval_result: KnowledgeBaseRetrievalResultTypeDef,
        ) -> tuple[str, str] | None:
            """Extract source URL/URI from retrieval result based on location type."""
            location = retrieval_result.get("location", {})
            location_type = location.get("type")

            if location_type == "WEB":
                url = location.get("webLocation", {}).get("url", "")
                return (url, url)

            elif location_type == "S3":
                uri = location.get("s3Location", {}).get("uri", "")
                source_name = urlparse(url=uri).path.split("/")[-1]
                return (source_name, uri)

            return None

        search_results = []
        for i, retrieval_result in enumerate(response.get("retrievalResults", [])):
            content = retrieval_result.get("content", {}).get("text", "")
            source = extract_source_from_retrieval_result(retrieval_result)

            if source is not None:
                search_results.append(
                    SearchResult(
                        rank=i,
                        bot_id=bot.id,
                        content=content,
                        source_name=source[0],
                        source_link=source[1],
                    )
                )

        return search_results

    except ClientError as e:
        logger.error(f"Error querying Bedrock Knowledge Base: {e}")
        raise e


def search_related_docs(bot: BotModel, query: str) -> list[SearchResult]:
    return _bedrock_knowledge_base_search(bot, query)
