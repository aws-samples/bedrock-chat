from typing import Any, Dict, List, Literal, Type, get_args

from app.repositories.models.common import DynamicBaseModel, Float
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.repositories.models.custom_bot_kb import BedrockKnowledgeBaseModel
from app.routes.schemas.bot import type_sync_status
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, ConfigDict, create_model


def _create_model_activate_model(model_names: List[str]) -> Type[DynamicBaseModel]:
    fields: Dict[str, Any] = {
        name.replace("-", "_").replace(".", "_"): (bool, True) for name in model_names
    }
    return create_model("ActiveModelsModel", __base__=DynamicBaseModel, **fields)


ActiveModelsModel: Type[BaseModel] = _create_model_activate_model(
    list(get_args(type_model_name))
)


class KnowledgeModel(BaseModel):
    source_urls: list[str]
    sitemap_urls: list[str]
    filenames: list[str]
    s3_urls: list[str]

    def __str_in_claude_format__(self) -> str:
        """Description of the knowledge in Claude format."""
        _source_urls = "<source_urls>"
        for url in self.source_urls:
            _source_urls += f"<url>{url}</url>"
        _source_urls += "</source_urls>"
        _sitemap_urls = "<sitemap_urls>"
        for url in self.sitemap_urls:
            _sitemap_urls += f"<url>{url}</url>"
        _sitemap_urls += "</sitemap_urls>"
        _filenames = "<filenames>"
        for filename in self.filenames:
            _filenames += f"<filename>{filename}</filename>"
        _filenames += "</filenames>"
        _s3_urls = "<s3_urls>"
        for url in self.s3_urls:
            _s3_urls += f"<url>{url}</url>"
        _s3_urls += "</s3_urls>"
        return f"{_source_urls}{_sitemap_urls}{_filenames}{_s3_urls}"


class GenerationParamsModel(BaseModel):
    max_tokens: int
    top_k: int
    top_p: Float
    temperature: Float
    stop_sequences: list[str]


class AgentToolModel(BaseModel):
    name: str
    description: str


class AgentModel(BaseModel):
    tools: list[AgentToolModel]


class ConversationQuickStarterModel(BaseModel):
    title: str
    example: str


class BotModel(BaseModel):
    id: str
    title: str
    description: str
    instruction: str
    create_time: float
    last_used_time: float
    # This can be used as the bot is public or not. Also used for GSI PK
    public_bot_id: str | None
    owner_user_id: str
    is_pinned: bool
    generation_params: GenerationParamsModel
    agent: AgentModel
    knowledge: KnowledgeModel
    sync_status: type_sync_status
    sync_status_reason: str
    sync_last_exec_id: str
    published_api_stack_name: str | None
    published_api_datetime: int | None
    published_api_codebuild_id: str | None
    display_retrieved_chunks: bool
    conversation_quick_starters: list[ConversationQuickStarterModel]
    bedrock_knowledge_base: BedrockKnowledgeBaseModel | None
    bedrock_guardrails: BedrockGuardrailsModel | None
    active_models: ActiveModelsModel  # type: ignore

    def has_knowledge(self) -> bool:
        return (
            len(self.knowledge.source_urls) > 0
            or len(self.knowledge.sitemap_urls) > 0
            or len(self.knowledge.filenames) > 0
            or len(self.knowledge.s3_urls) > 0
        )

    def is_agent_enabled(self) -> bool:
        return len(self.agent.tools) > 0

    def has_bedrock_knowledge_base(self) -> bool:
        return (
            self.bedrock_knowledge_base is not None
            and self.bedrock_knowledge_base.knowledge_base_id is not None
        )


class BotAliasModel(BaseModel):
    id: str
    title: str
    description: str
    original_bot_id: str
    create_time: float
    last_used_time: float
    is_pinned: bool
    sync_status: type_sync_status
    has_knowledge: bool
    has_agent: bool
    conversation_quick_starters: list[ConversationQuickStarterModel]
    active_models: ActiveModelsModel  # type: ignore


class BotMeta(BaseModel):
    id: str
    title: str
    description: str
    create_time: float
    last_used_time: float
    is_pinned: bool
    is_public: bool
    # Whether the bot is owned by the user
    owned: bool
    # Whether the bot is available or not.
    # This can be `False` if the bot is not owned by the user and original bot is removed.
    available: bool
    sync_status: type_sync_status
    has_bedrock_knowledge_base: bool


class BotMetaWithStackInfo(BotMeta):
    owner_user_id: str
    published_api_stack_name: str | None
    published_api_datetime: int | None
