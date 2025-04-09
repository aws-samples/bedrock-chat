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
    index_name: str = None,  # Will be set based on environment variables
) -> list[ConversationMeta]:
    """Search conversations by query string.
    This method searches through both the conversation title and message content.
    """
    client = client or get_opensearch_client(collection_type="conversation")
    
    # Use environment prefix for index name if not explicitly provided
    if index_name is None:
        import os
        env_prefix = os.environ.get("ENV_PREFIX", "")
        index_name = f"{env_prefix}conversation"
    
    logger.info(f"Searching conversations with query: {query} in index: {index_name}")

    # Only search conversations belonging to the user
    # Combining both filtering conditions for more restrictive search
    filter_must = [
        {"term": {"PK.keyword": user.id}},
        {"prefix": {"SK.keyword": f"{user.id}#CONV#"}}
    ]

    search_body = {
        "query": {
            "bool": {
                "should": [
                    # Title match (high weight)
                    {"match": {"Title": {"query": query, "boost": 3.0}}},
                    # Phrase match (high weight)
                    {"match_phrase": {"MessageMap": {"query": query, "boost": 2.5}}},
                    # MessageMap overall match (medium weight)
                    {"match": {"MessageMap": {"query": query, "boost": 2.0}}},
                    # Wildcard search
                    {"wildcard": {"MessageMap": {"value": f"*{query.lower()}*", "boost": 1.0}}}
                ],
                "minimum_should_match": 1,
                "filter": {"bool": {"must": filter_must}}
            }
        },
        "size": limit,
        "sort": [
            {"_score": {"order": "desc"}},  # 1. Primary sort by relevance score
            {"CreateTime": {"order": "desc"}}  # 2. Secondary sort by recency (DynamoDB field name)
        ]
    }
    
    logger.debug(f"Search body: {search_body}")

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
