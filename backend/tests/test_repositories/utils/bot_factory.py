import sys
import unittest
from decimal import Decimal

sys.path.append(".")
from app.agents.tools.internet_search import internet_search_tool
from app.repositories.models.custom_bot import (
    ActiveModelsModel,
    AgentModel,
    BedrockGuardrailsModel,
    BedrockKnowledgeBaseModel,
    BotModel,
    ConversationQuickStarterModel,
    GenerationParamsModel,
    InternetToolModel,
    KnowledgeModel,
    PlainToolModel,
    ReasoningParamsModel,
    ToolModel,
    UsageStatsModel,
)
from app.repositories.models.custom_bot_kb import (
    AnalyzerParamsModel,
    OpenSearchParamsModel,
    SearchParamsModel,
    WebCrawlingFiltersModel,
)
from app.routes.schemas.bot import type_sync_status


def _create_test_bot_model(
    id,
    title,
    description,
    shared_scope,
    shared_status,
    is_starred,
    owner_user_id,
    allowed_cognito_users=[],
    allowed_cognito_groups=[],
    last_used_time=1627984879.9,
    conversation_quick_starters=None,
    bedrock_guardrails=None,
    sync_status="RUNNING",
    knowledge=None,
    display_retrieved_chunks=True,
    published_api_stack_name=None,
    published_api_datetime=None,
    published_api_codebuild_id=None,
    bedrock_knowledge_base=None,
    include_internet_tool=False,
    set_dummy_knowledge=False,
    usage_count=0,
    **kwargs
):
    tools: list[ToolModel] = [
        PlainToolModel(
            tool_type="plain", name="tool1", description="tool1 description"
        ),
        PlainToolModel(
            tool_type="plain", name="tool2", description="tool2 description"
        ),
    ]
    if include_internet_tool:
        tools.append(
            InternetToolModel(
                tool_type="internet",
                name=internet_search_tool.name,
                description=internet_search_tool.description,
                search_engine="duckduckgo",
            )
        )
    return BotModel(
        id=id,
        title=title,
        description=description,
        instruction=kwargs.get("instruction", ""),
        create_time=1627984879.9,
        last_used_time=last_used_time,
        shared_scope=shared_scope,
        shared_status=shared_status,
        allowed_cognito_users=allowed_cognito_users,
        allowed_cognito_groups=allowed_cognito_groups,
        is_starred=is_starred,
        owner_user_id=owner_user_id,
        generation_params=GenerationParamsModel(
            max_tokens=2000,
            top_k=250,
            top_p=0.999,
            temperature=0.6,
            stop_sequences=["Human: ", "Assistant: "],
            reasoning_params=ReasoningParamsModel(budget_tokens=1024),
        ),
        agent=AgentModel(
            tools=tools,
        ),
        knowledge=(
            KnowledgeModel(
                source_urls=["https://aws.amazon.com/"],
                sitemap_urls=["https://aws.amazon.sitemap.xml"],
                filenames=["test.txt"],
                s3_urls=["s3://test-user/test-bot/"],
            )
            if set_dummy_knowledge
            else (
                knowledge
                if knowledge is not None
                else KnowledgeModel(
                    source_urls=[], sitemap_urls=[], filenames=[], s3_urls=[]
                )
            )
        ),
        sync_status=sync_status,
        sync_status_reason="reason",
        sync_last_exec_id="",
        published_api_stack_name=published_api_stack_name,
        published_api_datetime=published_api_datetime,
        published_api_codebuild_id=published_api_codebuild_id,
        display_retrieved_chunks=display_retrieved_chunks,
        conversation_quick_starters=(
            [] if conversation_quick_starters is None else conversation_quick_starters
        ),
        bedrock_knowledge_base=(
            BedrockKnowledgeBaseModel(
                embeddings_model="titan_v2",
                open_search=OpenSearchParamsModel(analyzer=None),
                chunking_configuration=None,
                search_params=SearchParamsModel(max_results=10, search_type="hybrid"),
                knowledge_base_id="test-knowledge-base-id",
                data_source_ids=["data-source-1", "data-source-2"],
                parsing_model="disabled",
                web_crawling_scope="DEFAULT",
                web_crawling_filters=WebCrawlingFiltersModel(
                    exclude_patterns=["exclude-pattern"],
                    include_patterns=["include-pattern"],
                ),
            )
            if set_dummy_knowledge
            else bedrock_knowledge_base
        ),
        bedrock_guardrails=bedrock_guardrails,
        active_models=ActiveModelsModel(),
        usage_stats=UsageStatsModel(usage_count=usage_count),
    )


def create_test_private_bot(
    id, is_starred, owner_user_id, include_internet_tool=False, **kwargs
):
    return _create_test_bot_model(
        id=id,
        title="Test Bot",
        description="Test Bot Description",
        shared_scope="private",
        shared_status="unshared",
        is_starred=is_starred,
        owner_user_id=owner_user_id,
        include_internet_tool=include_internet_tool,
        **kwargs,
    )


def create_test_public_bot(
    id, is_starred, owner_user_id, include_internet_tool=False, **kwargs
):
    return _create_test_bot_model(
        id=id,
        title="Test Public Bot",
        description="Test Public Bot Description",
        shared_scope="all",
        shared_status="shared",
        is_starred=is_starred,
        owner_user_id=owner_user_id,
        include_internet_tool=include_internet_tool,
        **kwargs,
    )


def create_test_partial_shared_bot(
    id,
    is_starred,
    owner_user_id,
    allowed_cognito_users=[],
    allowed_cognito_groups=[],
    include_internet_tool=False,
    **kwargs
):
    return _create_test_bot_model(
        id=id,
        title="Test Partial Shared Bot",
        description="Test Partial Shared Bot Description",
        shared_scope="partial",
        shared_status="shared",
        allowed_cognito_users=allowed_cognito_users,
        allowed_cognito_groups=allowed_cognito_groups,
        is_starred=is_starred,
        owner_user_id=owner_user_id,
        include_internet_tool=include_internet_tool,
        **kwargs,
    )


def create_test_pinned_public_bot(
    id, is_starred, owner_user_id, include_internet_tool=False, **kwargs
):
    return _create_test_bot_model(
        id=id,
        title="Test Pinned Bot",
        description="Test Pinned Bot Description",
        shared_scope="all",
        shared_status="pinned@001",
        is_starred=is_starred,
        owner_user_id=owner_user_id,
        include_internet_tool=include_internet_tool,
        **kwargs,
    )


def create_test_pinned_partial_share_bot(
    id, is_starred, owner_user_id, include_internet_tool=False, **kwargs
):
    return _create_test_bot_model(
        id=id,
        title="Test Pinned Partial Share Bot",
        description="Test Pinned Partial Share Bot Description",
        shared_scope="partial",
        shared_status="pinned@001",
        allowed_cognito_users=["user1"],
        is_starred=is_starred,
        owner_user_id=owner_user_id,
        include_internet_tool=include_internet_tool,
        **kwargs,
    )


def create_test_published_bot(id, owner_user_id, include_internet_tool=False, **kwargs):
    return _create_test_bot_model(
        id=id,
        title="Test Published Bot",
        description="Test Published Bot Description",
        shared_scope="all",
        shared_status="shared",
        owner_user_id=owner_user_id,
        sync_status="SUCCEEDED",
        published_api_stack_name="test-stack",
        published_api_datetime=1627984879,
        published_api_codebuild_id="test-codebuild-id",
        include_internet_tool=include_internet_tool,
        **kwargs,
    )
