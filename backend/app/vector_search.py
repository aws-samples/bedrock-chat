import logging
from typing import TypedDict
from urllib.parse import urlparse

from app.repositories.models.conversation import (
    RelatedDocumentModel,
    TextToolResultModel,
)
from app.repositories.models.custom_bot import BotModel
from app.utils import get_bedrock_agent_runtime_client
from botocore.exceptions import ClientError
from mypy_boto3_bedrock_agent_runtime.type_defs import (
    KnowledgeBaseRetrievalResultTypeDef,
)
from mypy_boto3_bedrock_runtime.type_defs import GuardrailConverseContentBlockTypeDef

logger = logging.getLogger(__name__)
agent_client = get_bedrock_agent_runtime_client()


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
) -> GuardrailConverseContentBlockTypeDef | None:
    """Convert search results to Guardrails Grounding source format."""
    return (
        {
            "text": {
                "text": "\n\n".join(x["content"] for x in search_results),
                "qualifiers": ["grounding_source"],
            }
        }
        if len(search_results) > 0
        else None
    )


def _bedrock_knowledge_base_search(
    bot: BotModel,
    query: str,
    doc_filter: list[str] | None = None
) -> list[SearchResult]:
    # Instead of assert, do an explicit check and log a full stack trace if missing
    if bot.bedrock_knowledge_base is None or bot.bedrock_knowledge_base.knowledge_base_id is None:
        logger.error(
            "Missing bedrock_knowledge_base or knowledge_base_id in _bedrock_knowledge_base_search.\n"
            "Bot ID: %s\n"
            "bedrock_knowledge_base: %s\n",
            bot.id,
            bot.bedrock_knowledge_base,
        )
        # Print the stack to logs:
        logger.exception("Stacktrace below:")
        
        # Then raise an assertion or custom exception:
        raise AssertionError(
            "Cannot perform knowledge base search with a null or missing knowledge_base_id."
        )

    if bot.bedrock_knowledge_base.search_params.search_type == "semantic":
        search_type = "SEMANTIC"
    elif bot.bedrock_knowledge_base.search_params.search_type == "hybrid":
        search_type = "HYBRID"
    else:
        raise ValueError("Invalid search type")

    limit = bot.bedrock_knowledge_base.search_params.max_results
    # Use exist_knowledge_base_id if available, otherwise use knowledge_base_id
    knowledge_base_id = (
        bot.bedrock_knowledge_base.exist_knowledge_base_id
        if bot.bedrock_knowledge_base.exist_knowledge_base_id is not None
        else bot.bedrock_knowledge_base.knowledge_base_id
    )

    try:
        retrieval_config = {
            "vectorSearchConfiguration": {
                "numberOfResults": limit,
                "overrideSearchType": search_type,
            }
        }

        if doc_filter:
            if len(doc_filter) == 1:
                retrieval_config["vectorSearchConfiguration"]["filter"] = {
                    "stringContains": {
                        "key": "x-amz-bedrock-kb-source-uri",
                        "value": doc_filter[0]
                    }
                }
            else:
                retrieval_config["vectorSearchConfiguration"]["filter"] = {
                    "orAll": [
                        {
                            "stringContains": {
                                "key": "x-amz-bedrock-kb-source-uri",
                                "value": doc_name
                            }
                        }
                        for doc_name in doc_filter
                    ]
                }

        logger.info(
            "Executing Knowledge Base Search:\n"
            "- Bot ID: %s\n"
            "- Bedrock_knowledge_base: %s\n"
            "- Bedrock_knowledge_base search: %s\n"
            "- Retrieval Config: %s\n",
            bot.id,
            bot.bedrock_knowledge_base,
            query,
            retrieval_config
        )

        response = agent_client.retrieve(
            knowledgeBaseId=knowledge_base_id,
            retrievalQuery={"text": query},
            retrievalConfiguration=retrieval_config,
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
            logger.debug(f"KB Search Response - source:{source} - content: {content[:100]}...")

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


def search_related_docs(bot: BotModel, query: str, doc_filter: list[str] | None = None) -> list[SearchResult]:
    return _bedrock_knowledge_base_search(bot, query, doc_filter)

