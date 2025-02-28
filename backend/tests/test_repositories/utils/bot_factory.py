import sys
import unittest

sys.path.append(".")


from app.repositories.models.custom_bot import (
    ActiveModelsModel,
    AgentModel,
    BedrockGuardrailsModel,
    BedrockKnowledgeBaseModel,
    BotAliasModel,
    BotModel,
    ConversationQuickStarterModel,
    GenerationParamsModel,
    InternetToolModel,
    KnowledgeModel,
    PlainToolModel,
    ReasoningParamsModel,
)
from app.routes.schemas.bot import type_sync_status


def create_test_private_bot(
    id,
    is_pinned: bool,
    owner_user_id: str,
    instruction: str = "Test Bot Prompt",
    sync_status: type_sync_status = "RUNNING",
    published_api_stack_name: str | None = None,
    published_api_datetime: int | None = None,
    published_api_codebuild_id: str | None = None,
    display_retrieved_chunks: bool = True,
    conversation_quick_starters: list[ConversationQuickStarterModel] | None = None,
    bedrock_knowledge_base: BedrockKnowledgeBaseModel | None = None,
    bedrock_guardrails: BedrockGuardrailsModel | None = None,
):
    return BotModel(
        id=id,
        title="Test Bot",
        description="Test Bot Description",
        instruction=instruction,
        create_time=1627984879.9,
        last_used_time=1627984879.9,
        is_pinned=is_pinned,
        public_bot_id=None,
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
            tools=[
                PlainToolModel(
                    tool_type="plain", name="tool1", description="tool1 description"
                ),
                PlainToolModel(
                    tool_type="plain", name="tool2", description="tool2 description"
                ),
            ]
        ),
        knowledge=KnowledgeModel(
            source_urls=["https://aws.amazon.com/"],
            sitemap_urls=["https://aws.amazon.sitemap.xml"],
            filenames=["test.txt"],
            s3_urls=["s3://test-user/test-bot/"],
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
        bedrock_knowledge_base=bedrock_knowledge_base,
        bedrock_guardrails=bedrock_guardrails,
        active_models=ActiveModelsModel(),
    )


def create_test_public_bot(
    id,
    is_pinned,
    owner_user_id,
    public_bot_id=None,
    instruction="Test Public Bot Prompt",
    conversation_quick_starters: list[ConversationQuickStarterModel] | None = None,
    bedrock_knowledge_base: BedrockKnowledgeBaseModel | None = None,
    bedrock_guardrails: BedrockGuardrailsModel | None = None,
):
    return BotModel(
        id=id,
        title="Test Public Bot",
        description="Test Public Bot Description",
        instruction=instruction,
        create_time=1627984879.9,
        last_used_time=1627984879.9,
        is_pinned=is_pinned,
        public_bot_id=public_bot_id,
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
            tools=[
                PlainToolModel(
                    tool_type="plain", name="tool1", description="tool1 description"
                ),
                PlainToolModel(
                    tool_type="plain", name="tool2", description="tool2 description"
                ),
            ]
        ),
        knowledge=KnowledgeModel(
            source_urls=["https://aws.amazon.com/"],
            sitemap_urls=["https://aws.amazon.sitemap.xml"],
            filenames=["test.txt"],
            s3_urls=["s3://test-user/test-bot/"],
        ),
        sync_status="RUNNING",
        sync_status_reason="reason",
        sync_last_exec_id="",
        published_api_stack_name=None,
        published_api_datetime=None,
        published_api_codebuild_id=None,
        display_retrieved_chunks=True,
        conversation_quick_starters=(
            conversation_quick_starters if conversation_quick_starters else []
        ),
        bedrock_knowledge_base=bedrock_knowledge_base,
        bedrock_guardrails=bedrock_guardrails,
        active_models=ActiveModelsModel(),
    )
