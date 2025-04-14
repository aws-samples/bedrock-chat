import logging
import os
from typing import Optional

from app.repositories.common import get_opensearch_client
from app.repositories.models.conversation import ConversationMeta
from app.user import User
from opensearchpy import OpenSearch

env_prefix = os.environ.get("ENV_PREFIX", "")
INDEX_NAME = f"{env_prefix}conversation"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # More detailed logging


def find_conversations_by_query(
    query: str,
    user: User,
    limit: int = 20,
    client: OpenSearch | None = None,
) -> list[ConversationMeta]:
    """Search conversations by query string.
    This method searches through both the conversation title and message content.
    """
    client = client or get_opensearch_client(collection_type="conversation")

    logger.info(f"Searching conversations with query: {query} in index: {INDEX_NAME}")

    # Only search conversations belonging to the user
    # Combining both filtering conditions for more restrictive search
    filter_must = [
        {"term": {"PK.keyword": user.id}},
        {"prefix": {"SK.keyword": f"{user.id}#CONV#"}},
    ]

    search_body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"Title": {"query": query, "boost": 3.0}}},
                    {"match": {"ParsedMessageMap": {"query": query, "boost": 4.0}}},
                    {
                        "query_string": {
                            "query": f'"{query}"',
                            "fields": [
                                "ParsedMessageMap.*.*content*.body^4.0",
                                "ParsedMessageMap.*.*content*.text^4.0",
                            ],
                            "type": "best_fields",
                            "default_operator": "AND",
                        }
                    },
                ],
                "minimum_should_match": 1,
                "filter": {"bool": {"must": filter_must}},
            }
        },
        "size": limit,
        "sort": [
            {"_score": {"order": "desc"}},  # 1. Primary sort by relevance score
            {
                "CreateTime": {"order": "desc"}
            },  # 2. Secondary sort by recency (DynamoDB field name)
        ],
        "highlight": {
            "fields": {
                "Title": {
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                    "fragment_size": 150,
                    "number_of_fragments": 1,
                },
                "ParsedMessageMap.*.*content*.body": {
                    "fragment_size": 150,
                    "number_of_fragments": 3,
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                },
                "ParsedMessageMap.*.*content*.text": {
                    "fragment_size": 150,
                    "number_of_fragments": 3,
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"],
                },
            },
            "require_field_match": False,
            "order": "score",
        },
    }

    logger.debug(f"Search body: {search_body}")

    try:
        response = client.search(index=INDEX_NAME, body=search_body)
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
