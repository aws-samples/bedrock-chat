import logging
from typing import Optional

from app.repositories.common import get_opensearch_client
from app.repositories.models.conversation import ConversationMeta
from app.user import User
from opensearchpy import OpenSearch

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # More detailed logging


def find_conversations_by_query(
    query: str,
    user: User,
    limit: int = 20,
    client: OpenSearch | None = None,
    index_name: str = "conversation",
) -> list[ConversationMeta]:
    """Search conversations by query string.
    This method searches through both the conversation title and message content.
    """
    client = client or get_opensearch_client(collection_type="conversation")
    logger.info(f"Searching conversations with query: {query}")

    # Only search conversations belonging to the user
    # Combining both filtering conditions for more restrictive search
    filter_must = [
        {"term": {"PK.keyword": user.id}},
        {"prefix": {"SK.keyword": f"{user.id}#CONV#"}}
    ]

    search_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title^2", "messages.content"],
                            "type": "best_fields",
                            "operator": "or",
                            "minimum_should_match": "30%",
                            "fuzziness": "AUTO",
                        }
                    }
                ],
                "filter": {"bool": {"must": filter_must}}
            }
        },
        "size": limit,
        "sort": [
            {"_score": {"order": "desc"}},  # 1. Primary sort by relevance score
            {"createTime": {"order": "desc"}}  # 2. Secondary sort by recency
        ]
    }

    try:
        response = client.search(index=index_name, body=search_body)
        logger.debug(f"Search response: {response}")

        conversations = [
            ConversationMeta.from_opensearch_response(hit)
            for hit in response["hits"]["hits"]
        ]
        logger.info(f"Found {len(conversations)} conversations matching query: {query}")
        return conversations
    except Exception as e:
        logger.error(f"Error searching conversations: {e}")
        raise
