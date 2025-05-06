import logging
import time
from typing import TypedDict, Any
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
logger.setLevel(logging.INFO)
agent_client = get_bedrock_agent_runtime_client()


class SearchResult(TypedDict):
    bot_id: str
    content: str
    source_name: str
    source_link: str
    rank: int
    metadata: dict[str, Any]
    page_number: int | None


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
        page_number=search_result["page_number"],
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
        if search_results
        else None
    )


def _bedrock_knowledge_base_search(bot: BotModel, query: str) -> list[SearchResult]:
    assert bot.bedrock_knowledge_base is not None
    assert (
        bot.bedrock_knowledge_base.knowledge_base_id is not None
        or bot.bedrock_knowledge_base.exist_knowledge_base_id is not None
    ), "Either knowledge_base_id or exist_knowledge_base_id must be set"

    if bot.bedrock_knowledge_base.search_params.search_type == "semantic":
        search_type = "SEMANTIC"
    elif bot.bedrock_knowledge_base.search_params.search_type == "hybrid":
        search_type = "HYBRID"
    else:
        raise ValueError("Invalid search type")

    limit = bot.bedrock_knowledge_base.search_params.max_results
    knowledge_base_id = (
        bot.bedrock_knowledge_base.exist_knowledge_base_id
        if bot.bedrock_knowledge_base.exist_knowledge_base_id is not None
        else bot.bedrock_knowledge_base.knowledge_base_id
    )

    # Retry if Aurora is paused
    delays = [15, 45]
    response = None
    last_exc: ClientError | None = None

    for delay in delays + [None]:
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
            break

        except ClientError as e:
            last_exc = e
            msg = str(e)
            if delay is not None and "resuming after auto-pause" in msg.lower():
                logger.warning(f"Aurora paused – retrying retrieve in {delay}s...")
                time.sleep(delay)
                continue

            logger.error(f"Error querying Bedrock Knowledge Base: {e}")
            raise

    if response is None and last_exc:
        # all retries failed
        raise last_exc

    # process successful response
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
            source_name = urlparse(uri).path.split("/")[-1]
            return (source_name, uri)

        elif location_type == "CONFLUENCE":
            url = location.get("confluenceLocation", {}).get("url", "")
            return (url, url) if url else None

        elif location_type == "SALESFORCE":
            url = location.get("salesforceLocation", {}).get("url", "")
            return (url, url) if url else None

        elif location_type == "SHAREPOINT":
            url = location.get("sharePointLocation", {}).get("url", "")
            return (url, url) if url else None

        elif location_type == "KENDRA":
            url = location.get("kendraDocumentLocation", {}).get("uri", "")
            return (url, url) if url else None

        return None

    search_results: list[SearchResult] = []
    for i, retrieval_result in enumerate(response.get("retrievalResults", [])):
        content = retrieval_result.get("content", {}).get("text", "")
        source = extract_source_from_retrieval_result(retrieval_result)

        if source is not None:
            metadata = retrieval_result.get("metadata", {})
            page_number = None
            if "x-amz-bedrock-kb-document-page-number" in metadata:
                try:
                    page_number = int(metadata["x-amz-bedrock-kb-document-page-number"])
                except (ValueError, TypeError):
                    pass

            search_results.append(
                SearchResult(
                    rank=i,
                    bot_id=bot.id,
                    content=content,
                    source_name=source[0],
                    source_link=source[1],
                    metadata=metadata,
                    page_number=page_number,
                )
            )

    return search_results


def search_related_docs(bot: BotModel, query: str) -> list[SearchResult]:
    return _bedrock_knowledge_base_search(bot, query)
