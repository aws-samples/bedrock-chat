import logging
import os
from typing import Literal

from app.agents.utils import get_available_tools, get_tool_by_name
from app.config import DEFAULT_GENERATION_CONFIG as DEFAULT_CLAUDE_GENERATION_CONFIG
from app.config import DEFAULT_MISTRAL_GENERATION_CONFIG
from app.config import GenerationParams as GenerationParamsDict
from app.usecases.group import get_user_name, fetch_all_groups_by_user_id
from app.repositories.common import (
    RecordNotFoundError,
    _get_table_client,
    decompose_bot_alias_id,
    decompose_bot_id,
)
from app.repositories.custom_bot import (
    delete_alias_by_id,
    delete_bot_by_id,
    find_alias_by_id,
    find_private_bot_by_id,
    find_private_bots_by_user_id,
    find_public_bot_by_id,
    store_alias,
    store_bot,
    update_alias_last_used_time,
    update_alias_pin_status,
    update_bot,
    update_bot_last_used_time,
    update_bot_pin_status,
    find_all_bots_by_group_id,
    fetch_bots_by_group_id_and_type,
)
from app.repositories.models.custom_bot import (
    ActiveModelsModel,
    AgentModel,
    AgentToolModel,
    BotAliasModel,
    BotMeta,
    BotModel,
    ConversationQuickStarterModel,
    GenerationParamsModel,
    KnowledgeModel,
    CreatorConfigModel,
    AssistantConfigModel
)
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.repositories.models.custom_bot_kb import BedrockKnowledgeBaseModel
from app.routes.schemas.bot import (
    ActiveModelsInput,
    ActiveModelsOutput,
    Agent,
    AgentTool,
    BotInput,
    BotMetaOutput,
    BotModifyInput,
    BotModifyOutput,
    BotOutput,
    AssistantConfig,
    CreatorConfig,
    BotSummaryOutput,
    ConversationQuickStarter,
    GenerationParams,
    Knowledge,
    type_sync_status,
)
from app.routes.schemas.bot_guardrails import BedrockGuardrailsOutput
from app.routes.schemas.bot_kb import BedrockKnowledgeBaseOutput
from app.utils import (
    compose_upload_document_s3_path,
    compose_upload_temp_s3_path,
    compose_upload_temp_s3_prefix,
    delete_file_from_s3,
    delete_files_with_prefix_from_s3,
    generate_presigned_url,
    get_bedrock_agent_client,
    get_current_time,
    move_file_in_s3,
)
from app.usecases.group import (
    validate_user_access_to_bot
)
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

DOCUMENT_BUCKET = os.environ.get("DOCUMENT_BUCKET", "bedrock-documents")
ENABLE_MISTRAL = os.environ.get("ENABLE_MISTRAL", "") == "true"

DEFAULT_GENERATION_CONFIG = (
    DEFAULT_MISTRAL_GENERATION_CONFIG
    if ENABLE_MISTRAL
    else DEFAULT_CLAUDE_GENERATION_CONFIG
)


def _update_s3_documents_by_diff(
    user_id: str,
    bot_id: str,
    added_filenames: list[str],
    deleted_filenames: list[str],
):
    for filename in added_filenames:
        tmp_path = compose_upload_temp_s3_path(user_id, bot_id, filename)
        document_path = compose_upload_document_s3_path(user_id, bot_id, filename)
        move_file_in_s3(DOCUMENT_BUCKET, tmp_path, document_path)

    for filename in deleted_filenames:
        document_path = compose_upload_document_s3_path(user_id, bot_id, filename)

        # Ignore errors when deleting a non-existent file from the S3 bucket used in knowledge bases.
        # This allows users to update bot if the uploaded file is missing after the bot is created.
        delete_file_from_s3(DOCUMENT_BUCKET, document_path, ignore_not_exist=True)


def create_new_bot(user_id: str, bot_input: BotInput) -> BotOutput:
    """Create a new bot.
    Bot is created as private and not pinned.
    """
    current_time = get_current_time()
    has_knowledge = bot_input.knowledge and (
        len(bot_input.knowledge.source_urls) > 0
        or len(bot_input.knowledge.sitemap_urls) > 0
        or len(bot_input.knowledge.filenames) > 0
        or len(bot_input.knowledge.s3_urls) > 0
        # This is a condition for running Sfn to register existing KB information in DynamoDB when an existing KB is specified.
        or (
            bot_input.bedrock_knowledge_base is not None
            and bot_input.bedrock_knowledge_base.exist_knowledge_base_id is not None
        )
    )

    has_guardrails = (
        bot_input.bedrock_guardrails
        and bot_input.bedrock_guardrails.is_guardrail_enabled == True
    )

    sync_status: type_sync_status = (
        "QUEUED" if has_knowledge or has_guardrails else "SUCCEEDED"
    )

    # Prepare knowledge fields
    source_urls = bot_input.knowledge.source_urls if bot_input.knowledge else []
    sitemap_urls = bot_input.knowledge.sitemap_urls if bot_input.knowledge else []
    s3_urls = bot_input.knowledge.s3_urls if bot_input.knowledge else []
    filenames = bot_input.knowledge.filenames if bot_input.knowledge else []

    if filenames:
        try:
            # Move files from temp to final S3 path
            _update_s3_documents_by_diff(user_id, bot_input.id, filenames, [])
            # Clean up any leftover temp uploads
            delete_files_with_prefix_from_s3(
                DOCUMENT_BUCKET, compose_upload_temp_s3_prefix(user_id, bot_input.id)
            )
        except FileNotFoundError:
            logger.warning(f"No files found in temp S3 location for bot {bot_input.id}")
            filenames = []  # Reset if we couldn't move them

    # Build generation params
    generation_params: GenerationParamsDict = (
        {
            "max_tokens": bot_input.generation_params.max_tokens,
            "top_k": bot_input.generation_params.top_k,
            "top_p": bot_input.generation_params.top_p,
            "temperature": bot_input.generation_params.temperature,
            "stop_sequences": bot_input.generation_params.stop_sequences,
        }
        if bot_input.generation_params
        else DEFAULT_GENERATION_CONFIG
    )

    # ===== Construct the AgentModel (never None!) =====
    tool_instances = []
    if bot_input.agent and bot_input.agent.tools:
        for tool_name in bot_input.agent.tools:
            try:
                the_tool = get_tool_by_name(tool_name)
                tool_instances.append(
                    AgentToolModel(
                        name=the_tool.name,
                        description=the_tool.description
                    )
                )
            except Exception as e:
                logger.error(f"Failed to create tool {tool_name}: {e}")

    # If user didn't provide any agent or agent.tools, we default to empty
    agent_model = AgentModel(tools=tool_instances)

    logger.info(f"Get user_name for user_id: {user_id}")
    userName = get_user_name(user_id)
    logger.warning(f"user_name {userName}")

    creatorConfigModel = CreatorConfigModel(user_id=user_id, user_name=userName)

    # Step 1: Construct the BotModel object
    new_bot = BotModel(
        id=bot_input.id,
        title=bot_input.title,
        description=bot_input.description or "",
        instruction=bot_input.instruction,
        create_time=current_time,
        last_used_time=current_time,
        public_bot_id=None,
        is_pinned=False,
        owner_user_id=user_id,
        generation_params=GenerationParamsModel(**generation_params),
        agent=agent_model,
        knowledge=KnowledgeModel(
            source_urls=source_urls,
            sitemap_urls=sitemap_urls,
            filenames=filenames,
            s3_urls=s3_urls,
        ),
        sync_status=sync_status,
        sync_status_reason="",
        sync_last_exec_id="",
        published_api_stack_name=None,
        published_api_datetime=None,
        published_api_codebuild_id=None,
        display_retrieved_chunks=bot_input.display_retrieved_chunks,
        conversation_quick_starters=(
            []
            if not bot_input.conversation_quick_starters
            else [
                ConversationQuickStarterModel(
                    title=starter.title,
                    example=starter.example,
                )
                for starter in bot_input.conversation_quick_starters
            ]
        ),
        bedrock_knowledge_base=(
            BedrockKnowledgeBaseModel(**bot_input.bedrock_knowledge_base.model_dump())
            if bot_input.bedrock_knowledge_base
            else None
        ),
        bedrock_guardrails=(
            BedrockGuardrailsModel(**bot_input.bedrock_guardrails.model_dump())
            if bot_input.bedrock_guardrails
            else None
        ),
        active_models=ActiveModelsModel.model_validate(
            dict(bot_input.active_models) if bot_input.active_models else {}
        ),
        version=bot_input.version or None,
        group_id=bot_input.group_id or None,
        assistant_config=(
            AssistantConfigModel(**bot_input.assistant_config.model_dump())
            if bot_input.assistant_config
            else None
        ),
        creator_config=creatorConfigModel
    )

    # Step 2: Store the newly created bot in DB
    store_bot(user_id, new_bot)

    # Step 3: Return BotOutput
    return BotOutput(
        id=new_bot.id,
        title=new_bot.title,
        instruction=new_bot.instruction,
        description=new_bot.description,
        create_time=new_bot.create_time,
        last_used_time=new_bot.last_used_time,
        is_public=False,
        is_pinned=False,
        owned=True,
        generation_params=GenerationParams(**generation_params),
        agent=Agent(
            tools=[
                AgentTool(name=tool.name, description=tool.description)
                for tool in new_bot.agent.tools
            ]
        ),
        knowledge=Knowledge(
            source_urls=source_urls,
            sitemap_urls=sitemap_urls,
            filenames=filenames,
            s3_urls=s3_urls,
        ),
        sync_status=sync_status,
        sync_status_reason="",
        sync_last_exec_id="",
        display_retrieved_chunks=new_bot.display_retrieved_chunks,
        conversation_quick_starters=[
            ConversationQuickStarter(title=starter.title, example=starter.example)
            for starter in new_bot.conversation_quick_starters
        ]
        if new_bot.conversation_quick_starters
        else [],
        bedrock_knowledge_base=(
            BedrockKnowledgeBaseOutput(**bot_input.bedrock_knowledge_base.model_dump())
            if bot_input.bedrock_knowledge_base
            else None
        ),
        bedrock_guardrails=(
            BedrockGuardrailsOutput(**bot_input.bedrock_guardrails.model_dump())
            if bot_input.bedrock_guardrails
            else None
        ),
        active_models=ActiveModelsOutput.model_validate(
            dict(bot_input.active_models) if bot_input.active_models else {}
        ),
        version=bot_input.version or None,
        group_id=bot_input.group_id or None,
        assistant_config=(
            AssistantConfig(**new_bot.assistant_config.model_dump())
            if new_bot.assistant_config
            else None
        ),
        creator_config=(
            CreatorConfig(**new_bot.creator_config.model_dump())
            if new_bot.creator_config
            else None
        ),
    )


def modify_owned_bot(
    user_id: str, bot_id: str, modify_input: BotModifyInput
) -> BotModifyOutput:
    """
    Modify an owned bot. 
    """

     # Get existing bot and model first
    bot = find_private_bot_by_id(user_id, bot_id)

    if not hasattr(bot, "creator_config") or not getattr(bot.creator_config, "user_id", None):
        raise RecordNotFoundError(f"Failed to get the creator id for bot: {bot_id}")
    # get the creator_id to ensure the existing bot record is updated
    creator_id = bot.creator_config.user_id

    source_urls = []
    sitemap_urls = []
    filenames = []
    s3_urls = []
    sync_status: type_sync_status = "QUEUED"

    if modify_input.knowledge:
        source_urls = modify_input.knowledge.source_urls
        sitemap_urls = modify_input.knowledge.sitemap_urls
        s3_urls = modify_input.knowledge.s3_urls

        # Commit changes to S3
        _update_s3_documents_by_diff(
            creator_id,
            bot_id,
            modify_input.knowledge.added_filenames,
            modify_input.knowledge.deleted_filenames,
        )
        # Delete files from upload temp directory
        delete_files_with_prefix_from_s3(
            DOCUMENT_BUCKET, compose_upload_temp_s3_prefix(creator_id, bot_id)
        )

        filenames = (
            modify_input.knowledge.added_filenames
            + modify_input.knowledge.unchanged_filenames
        )

    generation_params: GenerationParamsDict = (
        {
            "max_tokens": modify_input.generation_params.max_tokens,
            "top_k": modify_input.generation_params.top_k,
            "top_p": modify_input.generation_params.top_p,
            "temperature": modify_input.generation_params.temperature,
            "stop_sequences": modify_input.generation_params.stop_sequences,
        }
        if modify_input.generation_params
        else DEFAULT_GENERATION_CONFIG
    )
   
    # Build or update the agent if needed
    tool_dict = {}

    if modify_input.agent:        
        # Create or update AgentToolModel entries
        for tool_name in modify_input.agent.tools:
            try:
                the_tool = get_tool_by_name(tool_name)
                # Update existing or add new tool
                tool_dict[tool_name] = AgentToolModel(
                    name=the_tool.name,
                    description=the_tool.description,
                )
            except Exception as e:
                logger.error(f"Failed to create/update tool {tool_name}: {e}")

    # Convert dictionary values back to list
    new_tools = list(tool_dict.values())
    agent = AgentModel(tools=new_tools)

    # if knowledge is not updated, skip embeding process.
    # 'sync_status = "QUEUED"' will execute embeding process and update dynamodb record.
    # 'sync_status= "SUCCEEDED"' will update only dynamodb record.
    sync_status = (
        "QUEUED"
        if modify_input.is_embedding_required(bot)
        or modify_input.is_guardrails_update_required(bot)
        else "SUCCEEDED"
    )

    # Use the existing knowledge base (KB) configuration if available, as it may have been set externally
    # by a Step Functions state machine for embedding processes e.g. data source id. If a new KB configuration is provided,
    # merge it with the existing one; otherwise, retain the current KB settings.
    current_bot_kb = bot.bedrock_knowledge_base
    updated_kb: BedrockKnowledgeBaseModel | None = None
    if modify_input.bedrock_knowledge_base:
        updated_kb = (
            current_bot_kb.model_copy(
                update=modify_input.bedrock_knowledge_base.model_dump()
            )
            if current_bot_kb
            else BedrockKnowledgeBaseModel(
                **modify_input.bedrock_knowledge_base.model_dump()
            )
        )
    else:
        updated_kb = current_bot_kb

    update_bot(
        creator_id,
        bot_id,
        title=modify_input.title,
        instruction=modify_input.instruction,
        description=modify_input.description if modify_input.description else "",
        generation_params=GenerationParamsModel(**generation_params),
        agent=agent,
        knowledge=KnowledgeModel(
            source_urls=source_urls,
            sitemap_urls=sitemap_urls,
            filenames=filenames,
            s3_urls=s3_urls,
        ),
        sync_status=sync_status,
        sync_status_reason="",
        display_retrieved_chunks=modify_input.display_retrieved_chunks,
        conversation_quick_starters=(
            []
            if modify_input.conversation_quick_starters is None
            else [
                ConversationQuickStarterModel(
                    title=starter.title,
                    example=starter.example,
                )
                for starter in modify_input.conversation_quick_starters
            ]
        ),
        bedrock_knowledge_base=updated_kb,
        bedrock_guardrails=(
            BedrockGuardrailsModel(**modify_input.bedrock_guardrails.model_dump())
            if modify_input.bedrock_guardrails
            else None
        ),
        active_models=ActiveModelsModel.model_validate(
            dict(modify_input.active_models) if modify_input.active_models else {}
        ),
        group_id=modify_input.group_id if modify_input.group_id else None,
        assistant_config=(
            AssistantConfigModel(**modify_input.assistant_config.model_dump())
            if modify_input.assistant_config
            else None
        )
    )

    return BotModifyOutput(
        id=bot_id,
        title=modify_input.title,
        instruction=modify_input.instruction,
        description=modify_input.description if modify_input.description else "",
        generation_params=GenerationParams(**generation_params),
        agent=Agent(
            tools=[
                AgentTool(name=tool.name, description=tool.description)
                for tool in agent.tools
            ]
        ),
        knowledge=Knowledge(
            source_urls=source_urls,
            sitemap_urls=sitemap_urls,
            filenames=filenames,
            s3_urls=s3_urls,
        ),
        conversation_quick_starters=(
            []
            if modify_input.conversation_quick_starters is None
            else [
                ConversationQuickStarter(
                    title=starter.title,
                    example=starter.example,
                )
                for starter in modify_input.conversation_quick_starters
            ]
        ),
        bedrock_knowledge_base=(
            BedrockKnowledgeBaseOutput(
                **(modify_input.bedrock_knowledge_base.model_dump())
            )
            if modify_input.bedrock_knowledge_base
            else None
        ),
        bedrock_guardrails=(
            BedrockGuardrailsOutput(**modify_input.bedrock_guardrails.model_dump())
            if modify_input.bedrock_guardrails
            else None
        ),
        active_models=ActiveModelsOutput.model_validate(
            dict(modify_input.active_models) if modify_input.active_models else {}
        ),
        group_id=modify_input.group_id if modify_input.group_id else None,
        assistant_config=(
            AssistantConfig(**modify_input.assistant_config.model_dump())
            if modify_input.assistant_config
            else None
        )
    )


def fetch_bot(user_id: str, bot_id: str) -> tuple[bool, BotModel]:
    """Fetch bot by id.
    The first element of the returned tuple is whether the bot is owned or not.
    `True` means the bot is owned by the user.
    `False` means the bot is shared by another user.
    """
    try:
        return True, find_private_bot_by_id(user_id, bot_id)
    except RecordNotFoundError:
        pass  #

    try:
        return False, find_public_bot_by_id(bot_id)
    except RecordNotFoundError:
        raise RecordNotFoundError(
            f"Bot with ID {bot_id} not found in both private (for user {user_id}) and public items."
        )


def fetch_all_bots_by_user_id(
    user_id: str, limit: int | None = None, only_pinned: bool = False
) -> list[BotMeta]:
    """Find all private & shared bots of a user.
    The order is descending by `last_used_time`.
    """
    if not only_pinned and not limit:
        raise ValueError("Must specify either `limit` or `only_pinned`")
    if limit and only_pinned:
        raise ValueError("Cannot specify both `limit` and `only_pinned`")
    if limit and (limit < 0 or limit > 100):
        raise ValueError("Limit must be between 0 and 100")

    table = _get_table_client(user_id)
    logger.info(f"Finding pinned bots for user: {user_id}")

    # Fetch all pinned bots
    query_params = {
        "IndexName": "LastBotUsedIndex",
        "KeyConditionExpression": Key("PK").eq(user_id),
        "ScanIndexForward": False,
    }
    if limit:
        query_params["Limit"] = limit
    if only_pinned:
        query_params["FilterExpression"] = Attr("IsPinned").eq(True)

    response = table.query(**query_params)

    bots = []
    for item in response["Items"]:
        if "OriginalBotId" in item:
            # Fetch original bots of alias bots
            is_original_available = True
            try:
                bot = find_public_bot_by_id(item["OriginalBotId"])
                logger.info(f"Found original bot: {bot.id}")
                meta = BotMeta(
                    id=bot.id,
                    title=bot.title,
                    create_time=float(bot.create_time),
                    last_used_time=float(bot.last_used_time),
                    is_pinned=item["IsPinned"],
                    owned=False,
                    available=True,
                    description=bot.description,
                    is_public=True,
                    sync_status=bot.sync_status,
                    has_bedrock_knowledge_base=bot.has_bedrock_knowledge_base(),
                    version=(
                        None if "Version" not in item else item["Version"]
                    ),
                    group_id=(
                        None if "GroupId" not in item else item["GroupId"]
                    ),
                    assistant_config=(
                        AssistantConfigModel(**item["AssistantConfig"])
                        if "AssistantConfig" in item
                        else None
                    ),
                    creator_config=(
                        CreatorConfigModel(**item["CreatorConfig"])
                        if "CreatorConfig" in item
                        else None
                    )
                )
            except RecordNotFoundError:
                # Original bot is removed
                is_original_available = False
                logger.info(f"Original bot {item['OriginalBotId']} has been removed")
                meta = BotMeta(
                    id=item["OriginalBotId"],
                    title=item["Title"],
                    create_time=float(item["CreateTime"]),
                    last_used_time=float(item["LastBotUsed"]),
                    is_pinned=item["IsPinned"],
                    owned=False,
                    # NOTE: Original bot is removed
                    available=False,
                    description="This item is no longer available",
                    is_public=False,
                    sync_status="ORIGINAL_NOT_FOUND",
                    has_bedrock_knowledge_base=False,
                    version=(
                        None if "Version" not in item else item["Version"]
                    ),
                    group_id=(
                        None if "GroupId" not in item else item["GroupId"]
                    ),
                    assistant_config=(
                        AssistantConfigModel(**item["AssistantConfig"])
                        if "AssistantConfig" in item
                        else None
                    ),
                    creator_config=(
                        CreatorConfigModel(**item["CreatorConfig"])
                        if "CreatorConfig" in item
                        else None
                    )
                )

            if is_original_available and (
                bot.title != item["Title"]
                or bot.description != item["Description"]
                or bot.sync_status != item["SyncStatus"]
                or bot.has_knowledge() != item["HasKnowledge"]
                or bot.conversation_quick_starters
                != [
                    ConversationQuickStarter(**starter)
                    for starter in item.get("ConversationQuickStarters", [])
                ]
                or bot.active_models
                != ActiveModelsModel.model_validate(dict(item.get("ActiveModels", {})))
            ):
                # Update alias to the latest original bot
                store_alias(
                    user_id,
                    BotAliasModel(
                        id=decompose_bot_alias_id(item["SK"]),
                        # Update title and description
                        title=bot.title,
                        description=bot.description,
                        original_bot_id=item["OriginalBotId"],
                        create_time=float(item["CreateTime"]),
                        last_used_time=float(item["LastBotUsed"]),
                        is_pinned=item["IsPinned"],
                        sync_status=bot.sync_status,
                        has_knowledge=bot.has_knowledge(),
                        has_agent=bot.is_agent_enabled(),
                        conversation_quick_starters=bot.conversation_quick_starters,
                        active_models=ActiveModelsModel.model_validate(
                            dict(bot.active_models) if bot.active_models else {}
                        ),
                    ),
                )

            bots.append(meta)
        else:
            # Private bots
            bots.append(
                BotMeta(
                    id=decompose_bot_id(item["SK"]),
                    title=item["Title"],
                    create_time=float(item["CreateTime"]),
                    last_used_time=float(item["LastBotUsed"]),
                    is_pinned=item["IsPinned"],
                    owned=True,
                    available=True,
                    description=item["Description"],
                    is_public="PublicBotId" in item,
                    sync_status=item["SyncStatus"],
                    has_bedrock_knowledge_base=(
                        True if item.get("BedrockKnowledgeBase", None) else False
                    ),
                    version=(
                        None if "Version" not in item else item["Version"]
                    ),
                    group_id=(
                        None if "GroupId" not in item else item["GroupId"]
                    ),
                    assistant_config=(
                        AssistantConfigModel(**item["AssistantConfig"])
                        if "AssistantConfig" in item
                        else None
                    ),
                    creator_config=(
                        CreatorConfigModel(**item["CreatorConfig"])
                        if "CreatorConfig" in item
                        else None
                    )
                )
            )

    return bots

def fetch_all_bots_from_groups(user_id: str) -> list[BotMeta]:

    logger.info(f"Find all bots from groups. user_id: {user_id}")
    groupList = fetch_all_groups_by_user_id(user_id)

    if not groupList:
        return []

    assistantList =[]
    for group in groupList:
        groupId = group.group_id
        bots = find_all_bots_by_group_id(groupId)
        assistantList.extend(bots)
    return assistantList


def fetch_all_bots(
    user_id: str,
    limit: int | None = None,
    pinned: bool = False,
    kind: Literal["private", "mixed", "groups"] = "private",
    group_id: str | None = None,
) -> list[BotMetaOutput]:
    """Fetch all bots.
    The order is descending by `last_used_time`.
    - If `kind` is `private`, only private bots will be returned.
        - If `mixed` must give either `pinned` or `limit`.
    - If `pinned` is True, only pinned bots will be returned.
        - When kind is `private`, this will be ignored.
    - If `limit` is specified, only the first n bots will be returned.
        - Cannot specify both `pinned` and `limit`.
    """
    bots = []
    if group_id:
        # get public, available, learning assistants
        bots = fetch_bots_by_group_id_and_type(user_id, group_id)
    elif kind == "private":
        bots = find_private_bots_by_user_id(user_id, limit=limit)
    elif kind == "mixed":
        bots = fetch_all_bots_by_user_id(user_id, limit=limit, only_pinned=pinned)
    elif kind == "groups":
        bots = fetch_all_bots_from_groups(user_id)
    else:
        raise ValueError(f"Invalid kind: {kind}")

    bot_metas = []
    for bot in bots:
        bot_metas.append(
            BotMetaOutput(
                id=bot.id,
                title=bot.title,
                create_time=bot.create_time,
                last_used_time=bot.last_used_time,
                is_pinned=bot.is_pinned,
                owned=bot.owned,
                available=bot.available,
                description=bot.description,
                is_public=bot.is_public,
                sync_status=bot.sync_status,
                version=bot.version or None,
                group_id=bot.group_id or None,
                assistant_config=(
                    AssistantConfig(**bot.assistant_config.model_dump())
                    if bot.assistant_config
                    else None
                ),
                creator_config=(
                    CreatorConfig(**bot.creator_config.model_dump())
                    if bot.creator_config
                    else None
                ),
            )
        )
    return bot_metas


def fetch_bot_summary(user_id: str, bot_id: str) -> BotSummaryOutput:
    try:
        bot = find_private_bot_by_id(user_id, bot_id)
        return BotSummaryOutput(
            id=bot_id,
            title=bot.title,
            description=bot.description,
            create_time=bot.create_time,
            last_used_time=bot.last_used_time,
            is_pinned=bot.is_pinned,
            is_public=True if bot.public_bot_id else False,
            has_agent=bot.is_agent_enabled(),
            owned=True,
            sync_status=bot.sync_status,
            has_knowledge=bot.has_knowledge(),
            conversation_quick_starters=[
                ConversationQuickStarter(
                    title=starter.title,
                    example=starter.example,
                )
                for starter in bot.conversation_quick_starters
            ],
            active_models=ActiveModelsOutput.model_validate(
                dict(bot.active_models) if bot.active_models else {}
            ),
        )

    except RecordNotFoundError:
        pass

    try:
        # NOTE: At the first time using shared bot, alias is not created yet.
        bot = find_public_bot_by_id(bot_id)
        return BotSummaryOutput(
            id=bot_id,
            title=bot.title,
            description=bot.description,
            create_time=bot.create_time,
            last_used_time=bot.last_used_time,
            is_pinned=False,  # NOTE: Shared bot is not pinned by default.
            is_public=True,
            has_agent=bot.is_agent_enabled(),
            owned=False,
            sync_status=bot.sync_status,
            has_knowledge=bot.has_knowledge(),
            conversation_quick_starters=[
                ConversationQuickStarter(
                    title=starter.title,
                    example=starter.example,
                )
                for starter in bot.conversation_quick_starters
            ],
            active_models=ActiveModelsOutput.model_validate(
                dict(bot.active_models) if bot.active_models else {}
            ),
        )
    except RecordNotFoundError:
        raise RecordNotFoundError(
            f"Bot with ID {bot_id} not found in both private (for user {user_id}) and alias, shared items."
        )


def modify_pin_status(user_id: str, bot_id: str, pinned: bool):
    """Modify bot pin status."""
    creator_id = validate_user_access_to_bot(user_id, bot_id).user_id
    try:
        return update_bot_pin_status(creator_id, bot_id, pinned)
    except RecordNotFoundError:
        pass

    try:
        return update_alias_pin_status(creator_id, bot_id, pinned)
    except RecordNotFoundError:
        raise RecordNotFoundError(f"Bot {bot_id} is neither owned nor alias.")


def remove_bot_by_id(user_id: str, bot_id: str):
    """Remove bot by id."""
    creator_id = validate_user_access_to_bot(user_id, bot_id).user_id
    try:
        return delete_bot_by_id(creator_id, bot_id)
    except RecordNotFoundError:
        pass

    try:
        return delete_alias_by_id(creator_id, bot_id)
    except RecordNotFoundError:
        raise RecordNotFoundError(f"Bot {bot_id} is neither owned nor alias.")


def modify_bot_last_used_time(user_id: str, bot_id: str):
    """Modify bot last used time."""
    creator_id = validate_user_access_to_bot(user_id, bot_id).user_id
    try:
        return update_bot_last_used_time(creator_id, bot_id)
    except RecordNotFoundError:
        pass

    try:
        return update_alias_last_used_time(creator_id, bot_id)
    except RecordNotFoundError:
        raise RecordNotFoundError(f"Bot {bot_id} is neither owned nor alias.")


def issue_presigned_url(
    user_id: str, bot_id: str, filename: str, content_type: str
) -> str:
    response = generate_presigned_url(
        DOCUMENT_BUCKET,
        compose_upload_temp_s3_path(user_id, bot_id, filename),
        content_type=content_type,
        expiration=3600,
        client_method="put_object",
    )
    return response


def remove_uploaded_file(user_id: str, bot_id: str, filename: str):
    # Ignore errors when deleting a non-existent file from the S3 bucket used in knowledge bases.
    # This allows users to update bot if the uploaded file is missing after the bot is created.
    creator_id = validate_user_access_to_bot(user_id, bot_id).user_id
    delete_file_from_s3(
        DOCUMENT_BUCKET,
        compose_upload_temp_s3_path(creator_id, bot_id, filename),
        ignore_not_exist=True,
    )
    return


def fetch_available_agent_tools():
    """Fetch available tools for bot."""
    return get_available_tools()
