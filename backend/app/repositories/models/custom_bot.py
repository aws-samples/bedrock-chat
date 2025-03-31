import logging
from typing import Annotated, Any, Dict, List, Literal, Optional, Self, Type, get_args

from app.repositories.models.common import DynamicBaseModel, Float, SecureString
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.repositories.models.custom_bot_kb import BedrockKnowledgeBaseModel
from app.routes.schemas.bot import (
    Agent,
    AgentInput,
    AgentToolInput,
    BedrockAgentConfig,
    BedrockAgentTool,
    FirecrawlConfig,
    InternetTool,
    PlainTool,
    Tool,
    type_sync_status,
)
from app.routes.schemas.conversation import type_model_name
from app.utils import get_api_key_from_secret_manager, store_api_key_to_secret_manager
from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    create_model,
    field_validator,
    model_validator,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _create_model_activate_model(model_names: List[str]) -> Type[DynamicBaseModel]:
    fields: Dict[str, Any] = {
        name.replace("-", "_").replace(".", "_"): (bool, True) for name in model_names
    }
    return create_model("ActiveModelsModel", __base__=DynamicBaseModel, **fields)


ActiveModelsModel: Type[BaseModel] = _create_model_activate_model(
    list(get_args(type_model_name))
)


default_active_models = ActiveModelsModel.model_validate(
    {field_name: True for field_name in ActiveModelsModel.model_fields.keys()}
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


class ReasoningParamsModel(BaseModel):
    budget_tokens: int

    @field_validator("budget_tokens")
    def validate_budget_tokens(cls, v: int) -> int:
        if v < 1024:
            raise ValueError("budget_tokens must be greater than or equal to 1024")
        return v


class GenerationParamsModel(BaseModel):
    max_tokens: int
    top_k: int
    top_p: Float
    temperature: Float
    stop_sequences: list[str]
    reasoning_params: ReasoningParamsModel


class FirecrawlConfigModel(BaseModel):
    secret_arn: str
    api_key: SecureString
    max_results: int = 10

    @classmethod
    def from_firecrawl_config(
        cls, config: FirecrawlConfig, user_id: str, bot_id: str
    ) -> Self:
        """Create a configuration model from the input and save the API key to Secrets Manager"""
        secret_arn = store_api_key_to_secret_manager(
            user_id, bot_id, "firecrawl", config.api_key
        )

        return cls(
            secret_arn=secret_arn,
            api_key=config.api_key,
            max_results=config.max_results,
        )

    @model_validator(mode="before")
    @classmethod
    def load_secret_from_arn(cls, data):
        """Load the API key from Secrets Manager when the API key is empty"""
        if (
            isinstance(data, dict)
            and "api_key" in data
            and data["api_key"] == ""  # API key is empty
            and "secret_arn" in data
        ):
            try:
                api_key = get_api_key_from_secret_manager(data["secret_arn"])
                data["api_key"] = api_key
            except Exception as e:
                logger.error(f"Failed to retrieve secret from ARN: {e}")
                raise ValueError(
                    f"Failed to retrieve secret from ARN: {data['secret_arn']}"
                )

        return data


class PlainToolModel(BaseModel):
    tool_type: Literal["plain"] = Field(
        "plain",
        description="Type of tool. It does not need additional settings for the plain.",
    )
    name: str
    description: str

    @classmethod
    def from_tool_input(cls, tool: AgentToolInput) -> Self:
        return cls(tool_type="plain", name=tool.name, description=tool.description)


class InternetToolModel(BaseModel):
    tool_type: Literal["internet"] = Field(
        "internet",
        description="Type of tool. It does need additional settings for the internet search.",
    )
    name: str
    description: str
    search_engine: Optional[Literal["duckduckgo", "firecrawl"]]
    firecrawl_config: Optional[FirecrawlConfigModel] | None = None

    @model_validator(mode="before")
    @classmethod
    def load_firecrawl_secret(cls, data):
        """Ensures validation of nested `FirecrawlConfigModel` with secret loading.

        This validator is specifically for InternetToolModel and handles the nested `FirecrawlConfigModel` validation.
        Without this explicit validation, the `load_secret_from_arn` validator in `FirecrawlConfigModel`
        would not be triggered during the normal nested model validation process and
        `model_validate` would not load the API key from Secrets Manager.
        """
        if (
            isinstance(data, dict)
            and data.get("firecrawl_config")
            and isinstance(data["firecrawl_config"], dict)
        ):
            data["firecrawl_config"] = FirecrawlConfigModel.model_validate(
                data["firecrawl_config"]
            )
        return data

    @classmethod
    def from_tool_input(cls, tool: AgentToolInput, user_id: str, bot_id: str) -> Self:
        firecrawl_config = None
        if tool.search_engine == "firecrawl" and tool.firecrawl_config:
            firecrawl_config = FirecrawlConfigModel.from_firecrawl_config(
                tool.firecrawl_config, user_id, bot_id
            )

        return cls(
            tool_type="internet",
            name=tool.name,
            description=tool.description,
            search_engine=tool.search_engine,
            firecrawl_config=firecrawl_config,
        )


class BedrockAgentConfigModel(BaseModel):
    agent_id: str
    alias_id: str


class BedrockAgentToolModel(BaseModel):
    tool_type: Literal["bedrock_agent"] = Field(
        "bedrock_agent",
        description="Type of tool. It does need additional settings for the bedrock agent.",
    )
    name: str
    description: str
    bedrockAgentConfig: Optional[BedrockAgentConfigModel] | None = None

    @classmethod
    def from_tool_input(cls, tool: AgentToolInput) -> Self:
        return cls(
            tool_type="bedrock_agent",
            name=tool.name,
            description=tool.description,
            bedrockAgentConfig=(
                BedrockAgentConfigModel(
                    agent_id=tool.bedrock_agent_config.agent_id,
                    alias_id=tool.bedrock_agent_config.alias_id,
                )
                if tool.bedrock_agent_config
                else None
            ),
        )


ToolModel = Annotated[
    PlainToolModel | InternetToolModel | BedrockAgentToolModel,
    Discriminator("tool_type"),
]


class AgentModel(BaseModel):
    tools: list[ToolModel]

    @field_validator("tools", mode="before")
    def handle_legacy_tools(cls, v):
        """For backward compatibility, convert legacy tools to the new format.
        If the tool is legacy such that it does not have a `tool_type` field,
        it will be converted to a `plain` tool.
        """
        if isinstance(v, list):
            converted_tools = []
            for tool in v:
                if isinstance(tool, dict) and "tool_type" not in tool:
                    tool["tool_type"] = "plain"
                converted_tools.append(tool)
            return converted_tools
        return v

    @classmethod
    def from_agent_input(
        cls, agent_input: Optional[AgentInput], user_id: str, bot_id: str
    ) -> Self:
        if not agent_input or not hasattr(agent_input, "tools"):
            return cls(tools=[])

        tools: List[ToolModel] = []
        for tool_input in agent_input.tools:
            if tool_input.tool_type == "plain":
                tools.append(PlainToolModel.from_tool_input(tool_input))
            elif tool_input.tool_type == "internet":
                tools.append(
                    InternetToolModel.from_tool_input(tool_input, user_id, bot_id)
                )
            elif tool_input.tool_type == "bedrock_agent":
                tools.append(BedrockAgentToolModel.from_tool_input(tool_input))

        return cls(tools=tools)

    def to_agent(self) -> Agent:
        """Convert to Agent schema while preserving secure strings."""

        tools: List[Tool] = []
        for tool in self.tools:
            if isinstance(tool, InternetToolModel):
                # Special handling for FirecrawlConfigModel
                firecrawl_config = None
                if tool.firecrawl_config:
                    firecrawl_config = FirecrawlConfig(
                        # return the secret ARN as the API key
                        api_key=tool.firecrawl_config.api_key,
                        max_results=tool.firecrawl_config.max_results,
                    )

                tools.append(
                    InternetTool(
                        tool_type="internet",
                        name=tool.name,
                        description=tool.description,
                        search_engine=tool.search_engine,
                        firecrawl_config=firecrawl_config,
                    )
                )
            elif isinstance(tool, BedrockAgentToolModel):
                tools.append(
                    BedrockAgentTool(
                        tool_type="bedrock_agent",
                        name=tool.name,
                        description=tool.description,
                        bedrockAgentConfig=(
                            BedrockAgentConfig(**tool.bedrockAgentConfig.model_dump())
                            if tool.bedrockAgentConfig
                            else None
                        ),
                    )
                )
            else:
                tools.append(
                    PlainTool(
                        tool_type="plain", name=tool.name, description=tool.description
                    )
                )

        return Agent(tools=tools)


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
            or self.has_bedrock_knowledge_base()
        )

    def is_agent_enabled(self) -> bool:
        # Always consider agents active, even if they have a knowledge base
        return len(self.agent.tools) > 0 or self.has_knowledge()

    def has_bedrock_knowledge_base(self) -> bool:
        return self.bedrock_knowledge_base is not None and (
            self.bedrock_knowledge_base.knowledge_base_id is not None
            or self.bedrock_knowledge_base.exist_knowledge_base_id is not None
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
    has_knowledge: bool
    has_bedrock_knowledge_base: bool


class BotMetaWithStackInfo(BotMeta):
    owner_user_id: str
    published_api_stack_name: str | None
    published_api_datetime: int | None
