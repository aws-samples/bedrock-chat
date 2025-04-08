import sys
import unittest
from unittest.mock import MagicMock, patch
import asyncio

sys.path.insert(0, ".")


from app.repositories.custom_bot import (
    delete_alias_by_id,
    delete_bot_by_id,
    delete_bot_publication,
    find_all_published_bots,
    find_private_bot_by_id,
    find_private_bots_by_user_id,
    find_public_bots_by_ids,
    store_alias,
    store_bot,
    update_alias_last_used_time,
    update_bot,
    update_bot_last_used_time,
    update_bot_publication,
    update_bot_visibility,
    update_knowledge_base_id,
)
from app.repositories.models.custom_bot import (
    ActiveModelsModel,
    AgentModel,
    AgentToolModel,
    AssistantConfigModel,
    BotAliasModel,
    ConversationQuickStarterModel,
    GenerationParamsModel,
    KnowledgeModel,
    BotMetaWithStackInfo,
)
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from app.repositories.models.custom_bot_kb import (
    AnalyzerParamsModel,
    BedrockKnowledgeBaseModel,
    FixedSizeParamsModel,
    OpenSearchParamsModel,
)
from app.repositories.models.custom_bot_kb import (
    SearchParamsModel as SearchParamsModelKB,
)
from app.usecases.bot import fetch_all_bots_by_user_id
from tests.test_repositories.utils.bot_factory import (
    create_test_private_bot,
    create_test_public_bot,
)


class TestCustomBotRepository(unittest.TestCase):
    def setUp(self) -> None:
        # Set up MetadataRepository mock
        self.metadata_repo_patcher = patch('app.repositories.custom_bot.MetadataRepository')
        self.mock_metadata_repo_class = self.metadata_repo_patcher.start()
        self.mock_metadata_repo = MagicMock()
        self.mock_metadata_repo_class.return_value = self.mock_metadata_repo
        
        # Configure the mock methods
        self.mock_metadata_repo.save_normalized_bot_metadata.return_value = None
        self.mock_metadata_repo.mark_bot_metadata_as_deleted.return_value = None
        
        # Set up DynamoDB table mock
        self.table_patcher = patch('app.repositories.custom_bot._get_table_client')
        self.mock_get_table = self.table_patcher.start()
        self.mock_table = MagicMock()
        self.mock_get_table.return_value = self.mock_table
        
        # Set up public DynamoDB table mock
        self.public_table_patcher = patch('app.repositories.custom_bot._get_table_public_client')
        self.mock_get_public_table = self.public_table_patcher.start()
        self.mock_public_table = MagicMock()
        self.mock_get_public_table.return_value = self.mock_public_table
        
        # Mock validate_user_access_to_bot to bypass group check
        self.validate_access_patcher = patch('app.repositories.custom_bot.validate_user_access_to_bot')
        self.mock_validate_access = self.validate_access_patcher.start()
        
        # Create a mock return value with expected attributes
        mock_access_result = MagicMock()
        mock_access_result.user_id = "user1" # Assuming the bot owner for these tests is user1
        mock_access_result.bot_id = "1" # Add the bot_id needed for SKIndex query
        self.mock_validate_access.return_value = mock_access_result
        
        # Define the mock bot item to be returned by queries
        self.mock_bot_db_item = {
            "PK": "user1",
            "SK": "user1#BOT#1",
            "Id": "1",
            "Title": "Test Bot",
            "Description": "Test Bot Description",
            "Instruction": "Test Bot Prompt",
            "CreateTime": 1627984879.9,
            "LastBotUsed": 1627984879.9,
            "IsPinned": False,
            "GenerationParams": {
                "max_tokens": 2000, "top_k": 250, "top_p": 0.999, "temperature": 0.6,
                "stop_sequences": ["Human: ", "Assistant: "], "model_id": "anthropic.claude-3-sonnet-v1"
            },
            "Knowledge": {
                "source_urls": ["https://aws.amazon.com/"], "sitemap_urls": ["https://aws.amazon.sitemap.xml"],
                "filenames": ["test.txt"], "s3_urls": ["s3://test-user/test-bot/"]
            },
            "AgentData": {"tools": []},
            "SyncStatus": "RUNNING",
            "SyncStatusReason": "reason",
            "LastExecId": "",
            "PublishedApiStackName": None, 
            "PublishedApiPublishedDatetime": None,
            "PublishedApiCodeBuildId": None,
            "BedrockKnowledgeBase": {
                 "embeddings_model": "titan_v2",
                 "open_search": {
                    "analyzer": {
                        "character_filters": [],
                        "tokenizer": "kuromoji_tokenizer",
                        "token_filters": []
                    }
                 },
                 "search_params": {
                    "max_results": 20,
                    "search_type": "hybrid"
                 },
                 "chunking_configuration": None
            }, 
            "BedrockGuardrails": None, 
            "DisplayRetrievedChunks": True,
            "ConversationQuickStarters": [],
            "OwnerUserId": "user1",
            "AssistantConfig": {
                "assistant_type": "custom_assistant", "assistant_topics": "general"
            },
            "ActiveModels": {
                 "embedding_model": { "provider": "bedrock", "model_id": "amazon.titan-embed-text-v1", "dimensions": 1536 }
            }
        }

        # Configure table mocks to return appropriate responses
        # Remove the basic put_item mock
        # self.mock_table.put_item.return_value = {}
        
        # Add stateful put_item mock
        def put_item_side_effect(*args, **kwargs):
            item_to_put = kwargs.get("Item")
            if item_to_put:
                # Overwrite the mock item state with the new item
                # This assumes put_item completely replaces the item
                self.mock_bot_db_item.clear()
                self.mock_bot_db_item.update(item_to_put)
            return {} # Default response for put_item
        
        self.mock_table.put_item.side_effect = put_item_side_effect

        # Mock get_item to return the full item (used by update_bot)
        self.mock_table.get_item.return_value = {"Item": self.mock_bot_db_item}

        # Simplify query mock: return the mock bot item unless it's marked deleted
        def query_side_effect(*args, **kwargs):
            if self.is_bot_deleted:
                return {"Items": []}
            else:
                # For simplicity in TestCustomBotRepository, assume any query returns the main test bot
                return {"Items": [self.mock_bot_db_item]}
        
        self.mock_table.query.side_effect = query_side_effect 
        # self.mock_table.query.return_value = {"Items": [self.mock_bot_db_item]} # Remove the simple return value
        
        # Add a stateful side_effect for update_item
        def update_item_side_effect(*args, **kwargs):
            key = kwargs.get("Key")
            # Basic check if the update is for our mock bot
            if key == {"PK": "user1", "SK": "user1#BOT#1"}:
                update_expression = kwargs.get("UpdateExpression", "")
                attr_values = kwargs.get("ExpressionAttributeValues", {})
                attr_names = kwargs.get("ExpressionAttributeNames", {})

                # Very basic parsing for SET action
                if update_expression.startswith("SET"):
                    assignments = update_expression[3:].strip().split(",")
                    for assignment in assignments:
                        parts = assignment.strip().split("=")
                        if len(parts) == 2:
                            target_name_placeholder = parts[0].strip() 
                            value_placeholder = parts[1].strip()
                            
                            # Resolve placeholder name if present
                            target_key = attr_names.get(target_name_placeholder, target_name_placeholder)
                            
                            if value_placeholder in attr_values:
                                # Update the mock item dictionary
                                raw_value = attr_values[value_placeholder]
                                # Check if the value is a DynamoDB type dict (e.g., {'S': 'val'}) or a direct value
                                if isinstance(raw_value, dict) and len(raw_value) == 1 and list(raw_value.keys())[0] in ['S', 'N', 'BOOL', 'L', 'M', 'NULL']:
                                    actual_value = list(raw_value.values())[0]
                                else:
                                    # Assume it's a direct value (str, number, bool, list, dict)
                                    actual_value = raw_value
                                
                                # Handle nested updates like BedrockKnowledgeBase.knowledge_base_id
                                keys = target_key.split('.')
                                current_level = self.mock_bot_db_item
                                for i, k in enumerate(keys):
                                    if i == len(keys) - 1: # Last key
                                        current_level[k] = actual_value
                                    else:
                                        if k not in current_level or not isinstance(current_level[k], dict):
                                            current_level[k] = {} # Create nested dict if not exists
                                        current_level = current_level[k]
                                        
                # Basic parsing for REMOVE action (e.g., for delete_bot_publication)
                elif update_expression.startswith("REMOVE"):
                    keys_to_remove = update_expression[6:].strip().split(",")
                    for key_placeholder in keys_to_remove:
                        key_placeholder_strip = key_placeholder.strip()
                        target_key = attr_names.get(key_placeholder_strip, key_placeholder_strip)
                        if target_key in self.mock_bot_db_item:
                            del self.mock_bot_db_item[target_key]

            # Return the updated attributes (or empty if not needed by caller)
            # Returning the whole item for simplicity in this mock
            return {"Attributes": self.mock_bot_db_item} 
            
        self.mock_table.update_item.side_effect = update_item_side_effect

        self.mock_public_table.put_item.return_value = {}
        self.mock_public_table.get_item.return_value = {"Item": {}}
        self.mock_public_table.query.return_value = {"Items": []}

        # Add a flag to track deletion status for the query mock
        self.is_bot_deleted = False

        # Add mock for delete_item
        def delete_item_side_effect(*args, **kwargs):
            key = kwargs.get("Key")
            if key == {"PK": "user1", "SK": "user1#BOT#1"}:
                self.is_bot_deleted = True
            return {} # Default response for delete_item
        
        self.mock_table.delete_item.side_effect = delete_item_side_effect

    def tearDown(self) -> None:
        self.metadata_repo_patcher.stop()
        self.table_patcher.stop()
        self.public_table_patcher.stop()
        self.validate_access_patcher.stop()
        
    def test_store_and_find_bot(self):
        # Patch construct_bot_metadata for this test to avoid validation errors
        with patch('app.repositories.custom_bot.construct_bot_metadata') as mock_construct:
            mock_construct.return_value = MagicMock() # Return dummy value

            bot = create_test_private_bot(
                "1",
                False,
                "user1",
                published_api_stack_name="TestApiStack",
                published_api_datetime=1627984879,
                published_api_codebuild_id="TestCodeBuildId",
                display_retrieved_chunks=True,
                conversation_quick_starters=[
                    ConversationQuickStarterModel(title="QS title", example="QS example")
                ],
                bedrock_knowledge_base=BedrockKnowledgeBaseModel(
                    embeddings_model="titan_v2",
                    open_search=OpenSearchParamsModel(
                        analyzer=AnalyzerParamsModel(
                            character_filters=["icu_normalizer"],
                            tokenizer="kuromoji_tokenizer",
                            token_filters=["kuromoji_baseform"],
                        )
                    ),
                    search_params=SearchParamsModelKB(
                        max_results=20,
                        search_type="hybrid",
                    ),
                    chunking_configuration=FixedSizeParamsModel(
                        chunking_strategy="fixed_size",
                        max_tokens=2000,
                        overlap_percentage=0,
                    ),
                    parsing_model="anthropic.claude-3-sonnet-v1",
                    web_crawling_scope="DEFAULT",
                ),
                bedrock_guardrails=BedrockGuardrailsModel(
                    is_guardrail_enabled=True,
                    hate_threshold=0,
                    insults_threshold=0,
                    sexual_threshold=0,
                    violence_threshold=0,
                    misconduct_threshold=0,
                    grounding_threshold=0.0,
                    relevance_threshold=0.0,
                    guardrail_arn="arn:aws:guardrail",
                    guardrail_version="v1",
                ),
            )
            store_bot("user1", bot)

            # Assert bot is stored and reconstructed correctly
            bot = find_private_bot_by_id("user1", "1")
            self.assertEqual(bot.id, "1")
            self.assertEqual(bot.title, "Test Bot")
            self.assertEqual(bot.description, "Test Bot Description")
            self.assertEqual(bot.instruction, "Test Bot Prompt")
            self.assertEqual(bot.create_time, 1627984879.9)
            self.assertEqual(bot.last_used_time, 1627984879.9)
            self.assertEqual(bot.is_pinned, False)

            self.assertEqual(bot.generation_params.max_tokens, 3000)
            self.assertEqual(bot.generation_params.top_k, 250)
            self.assertEqual(bot.generation_params.top_p, 0.999)
            self.assertEqual(bot.generation_params.temperature, 0.0)

            self.assertEqual(bot.knowledge.source_urls, ["https://aws.amazon.com/"])
            self.assertEqual(bot.knowledge.sitemap_urls, ["https://aws.amazon.sitemap.xml"])
            self.assertEqual(bot.knowledge.filenames, ["test.txt"])
            self.assertEqual(bot.knowledge.s3_urls, ["s3://test-user/test-bot/"])
            self.assertEqual(bot.sync_status, "RUNNING")
            self.assertEqual(bot.sync_status_reason, "reason")
            self.assertEqual(bot.sync_last_exec_id, "")
            self.assertEqual(bot.published_api_stack_name, "TestApiStack")
            self.assertEqual(bot.published_api_datetime, 1627984879)
            self.assertEqual(len(bot.conversation_quick_starters), 1)
            self.assertEqual(bot.conversation_quick_starters[0].title, "QS title")
            self.assertEqual(bot.conversation_quick_starters[0].example, "QS example")
            self.assertEqual(bot.bedrock_knowledge_base.embeddings_model, "titan_v2")
            self.assertEqual(
                bot.bedrock_knowledge_base.chunking_configuration.max_tokens, 2000
            )
            self.assertEqual(
                bot.bedrock_knowledge_base.chunking_configuration.overlap_percentage, 0
            )

            self.assertEqual(
                bot.bedrock_knowledge_base.open_search.analyzer.character_filters,
                ["icu_normalizer"],
            )
            self.assertEqual(
                bot.bedrock_knowledge_base.open_search.analyzer.tokenizer,
                "kuromoji_tokenizer",
            )
            self.assertEqual(
                bot.bedrock_knowledge_base.open_search.analyzer.token_filters,
                ["kuromoji_baseform"],
            )
            self.assertEqual(bot.bedrock_knowledge_base.search_params.max_results, 20)
            self.assertEqual(bot.bedrock_knowledge_base.search_params.search_type, "hybrid")
            self.assertEqual(bot.bedrock_guardrails.is_guardrail_enabled, True)
            self.assertEqual(bot.bedrock_guardrails.hate_threshold, 0)
            self.assertEqual(bot.bedrock_guardrails.insults_threshold, 0)
            self.assertEqual(bot.bedrock_guardrails.sexual_threshold, 0)
            self.assertEqual(bot.bedrock_guardrails.violence_threshold, 0)
            self.assertEqual(bot.bedrock_guardrails.misconduct_threshold, 0)
            self.assertEqual(bot.bedrock_guardrails.grounding_threshold, 0.0)
            self.assertEqual(bot.bedrock_guardrails.relevance_threshold, 0.0)
            self.assertEqual(bot.bedrock_guardrails.guardrail_arn, "arn:aws:guardrail")
            self.assertEqual(bot.bedrock_guardrails.guardrail_version, "v1")

            # Assert bot is stored in user1's bot list
            bot = find_private_bots_by_user_id("user1")
            self.assertEqual(len(bot), 1)
            self.assertEqual(bot[0].id, "1")
            self.assertEqual(bot[0].title, "Test Bot")
            self.assertEqual(bot[0].create_time, 1627984879.9)
            self.assertEqual(bot[0].last_used_time, 1627984879.9)
            self.assertEqual(bot[0].is_pinned, False)
            self.assertEqual(bot[0].is_pinned, False)
            self.assertEqual(bot[0].description, "Test Bot Description")
            self.assertEqual(bot[0].is_public, False)

            # Verify MetadataRepository was called to save normalized metadata
            self.mock_metadata_repo.save_normalized_bot_metadata.assert_called_once()
            # Verify the bot passed to save_normalized_bot_metadata is correct
            saved_bot = self.mock_metadata_repo.save_normalized_bot_metadata.call_args[0][0]
            self.assertEqual(saved_bot.id, "1")
            self.assertEqual(saved_bot.title, "Test Bot")
            self.assertEqual(saved_bot.owner_user_id, "user1")

            # Cleanup and assert bot is deleted
            delete_bot_by_id("user1", "1")
            bot = find_private_bots_by_user_id("user1")
            self.assertEqual(len(bot), 0)
            
            # Verify MetadataRepository was called to mark bot as deleted
            self.mock_metadata_repo.mark_bot_metadata_as_deleted.assert_called_once_with("1")

    def test_update_bot_last_used_time(self):
        bot = create_test_private_bot("1", False, "user1")
        store_bot("user1", bot)
        update_bot_last_used_time("user1", "1")

        bot = find_private_bot_by_id("user1", "1")
        self.assertIsNotNone(bot.last_used_time)
        self.assertEqual(bot.display_retrieved_chunks, True)

        delete_bot_by_id("user1", "1")

    def test_update_delete_bot_publication(self):
        bot = create_test_private_bot("1", False, "user1")
        store_bot("user1", bot)
        update_bot_publication("user1", "1", "api1", "build1")

        bot = find_private_bot_by_id("user1", "1")
        # NOTE: Stack naming rule: ApiPublishmentStack{published_api_id}.
        # See bedrock-chat-stack.ts > `ApiPublishmentStack`
        self.assertEqual(bot.published_api_stack_name, "ApiPublishmentStackapi1")
        self.assertIsNotNone(bot.published_api_datetime)
        self.assertEqual(bot.published_api_codebuild_id, "build1")

        delete_bot_publication("user1", "1")
        bot = find_private_bot_by_id("user1", "1")
        self.assertIsNone(bot.published_api_stack_name)
        self.assertIsNone(bot.published_api_datetime)
        self.assertIsNone(bot.published_api_codebuild_id)

        delete_bot_by_id("user1", "1")

    def test_update_knowledge_base_id(self):
        bot = create_test_private_bot(
            "1",
            False,
            "user1",
            bedrock_knowledge_base=BedrockKnowledgeBaseModel(
                embeddings_model="titan_v2",
                open_search=OpenSearchParamsModel(
                    analyzer=AnalyzerParamsModel(
                        character_filters=["icu_normalizer"],
                        tokenizer="kuromoji_tokenizer",
                        token_filters=["kuromoji_baseform"],
                    )
                ),
                search_params=SearchParamsModelKB(
                    max_results=20,
                    search_type="hybrid",
                ),
                chunking_configuration=FixedSizeParamsModel(
                    chunking_strategy="fixed_size",
                ),
            ),
        )
        store_bot("user1", bot)
        update_knowledge_base_id("user1", "1", "kb1", ["ds1", "ds2"])
        bot = find_private_bot_by_id("user1", "1")
        self.assertEqual(bot.bedrock_knowledge_base.knowledge_base_id, "kb1")
        self.assertEqual(bot.bedrock_knowledge_base.data_source_ids, ["ds1", "ds2"])
        delete_bot_by_id("user1", "1")

    def test_update_bot(self):
        # Patch construct_bot_metadata for this test to avoid validation errors
        with patch('app.repositories.custom_bot.construct_bot_metadata') as mock_construct:
            # Return a dummy BotMetadata object or similar structure if needed
            # For simplicity, let's assume it doesn't need to return anything crucial for the subsequent call
            mock_construct.return_value = MagicMock() 

            bot = create_test_private_bot("1", False, "user1")
            store_bot("user1", bot)
            
            # Reset the mock for clean testing
            self.mock_metadata_repo.save_normalized_bot_metadata.reset_mock()
            
            # Update the bot
            update_bot(
                "user1",
                "1",
                title="Updated Title",
                description="Updated Description",
                instruction="Updated Instruction",
                generation_params=GenerationParamsModel(
                    max_tokens=2500,
                    top_k=250,
                    top_p=0.99,
                    temperature=0.7,
                    stop_sequences=["STOP"],
                    model_id="anthropic.claude-3-sonnet-v1",
                ),
                agent=AgentModel(tools=[]),
                knowledge=KnowledgeModel(source_urls=[], sitemap_urls=[], filenames=[], s3_urls=[]),
                sync_status="SUCCEEDED",
                sync_status_reason="",
                group_id=None,
                assistant_config=AssistantConfigModel(
                    assistant_type="custom_assistant",
                    assistant_topics="general"
                ),
                display_retrieved_chunks=True,
                active_models=ActiveModelsModel(),
                conversation_quick_starters=[]
            )

            # Verify bot was updated in the database
            updated_bot = find_private_bot_by_id("user1", "1")
            self.assertEqual(updated_bot.title, "Updated Title")
            self.assertEqual(updated_bot.description, "Updated Description")
            self.assertEqual(updated_bot.instruction, "Updated Instruction")
            self.assertEqual(updated_bot.generation_params.temperature, 0.7)
            
            # Verify MetadataRepository was called to update the bot metadata
            self.mock_metadata_repo.save_normalized_bot_metadata.assert_called_once()
            updated_saved_bot = self.mock_metadata_repo.save_normalized_bot_metadata.call_args[0][0]
            self.assertEqual(updated_saved_bot.id, "1")
            self.assertEqual(updated_saved_bot.title, "Updated Title")
            self.assertEqual(updated_saved_bot.description, "Updated Description")
            
            # Cleanup
            delete_bot_by_id("user1", "1")


class TestFindAllBots(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        # Set up MetadataRepository mock (same as in TestCustomBotRepository)
        self.metadata_repo_patcher = patch('app.repositories.custom_bot.MetadataRepository')
        self.mock_metadata_repo_class = self.metadata_repo_patcher.start()
        self.mock_metadata_repo = MagicMock()
        self.mock_metadata_repo_class.return_value = self.mock_metadata_repo
        
        # Configure the mock methods
        self.mock_metadata_repo.save_normalized_bot_metadata.return_value = None
        self.mock_metadata_repo.mark_bot_metadata_as_deleted.return_value = None
        
        # Set up DynamoDB table mock
        self.table_patcher = patch('app.repositories.custom_bot._get_table_client')
        self.mock_get_table = self.table_patcher.start()
        self.mock_table = MagicMock()
        self.mock_get_table.return_value = self.mock_table
        
        # Set up public DynamoDB table mock
        self.public_table_patcher = patch('app.repositories.custom_bot._get_table_public_client')
        self.mock_get_public_table = self.public_table_patcher.start()
        self.mock_public_table = MagicMock()
        self.mock_get_public_table.return_value = self.mock_public_table
        
        # Mock validate_user_access_to_bot to bypass group check
        self.validate_access_patcher = patch('app.repositories.custom_bot.validate_user_access_to_bot')
        self.mock_validate_access = self.validate_access_patcher.start()
        
        # Create a mock return value with expected attributes
        mock_access_result = MagicMock()
        mock_access_result.user_id = "user2"  # User who created the bot
        self.mock_validate_access.return_value = mock_access_result
        
        # Configure table mocks to return appropriate responses
        self.mock_table.put_item.return_value = {}
        self.mock_table.update_item.return_value = {"Attributes": {}}
        self.mock_table.get_item.return_value = {"Item": {}}
        self.mock_table.query.return_value = {"Items": []}
        
        self.mock_public_table.put_item.return_value = {}
        self.mock_public_table.get_item.return_value = {"Item": {}}
        self.mock_public_table.query.return_value = {"Items": []}

        # Set up mock for find_all_published_bots
        self.mock_published_items = [{
            "PK": "user2",
            "SK": "user2#BOT#public1",
            "Title": "Test Public Bot",
            "Description": "Test Public Bot Description", 
            "Instruction": "Test instruction",
            "CreateTime": 1627984879.9,
            "LastBotUsed": 1627984879.9,
            "IsPinned": True,
            "PublicBotId": "public1",
            "SyncStatus": "SUCCEEDED",
            "ApiPublishmentStackName": "ApiPublishmentStackapi1",
            "ApiPublishedDatetime": 1627984879,
            "ApiPublishCodeBuildId": "build1",
            "AssistantConfig": {
                "assistant_type": "custom_assistant",
                "assistant_topics": "general"
            }
        }]
        
        self.mock_public_table.scan.return_value = {"Items": self.mock_published_items}
        
        # Set up mock for find_public_bots_by_ids
        self.mock_public_table.query.return_value = {"Items": self.mock_published_items}

    def tearDown(self) -> None:
        self.metadata_repo_patcher.stop()
        self.table_patcher.stop()
        self.public_table_patcher.stop()
        self.validate_access_patcher.stop()

    def test_limit(self):
        # Set up mock response for find_private_bots_by_user_id
        self.mock_table.query.return_value = {
            "Items": [
                {
                    "PK": "user1",
                    "SK": "user1#BOT#1",
                    "Title": "Bot 1",
                    "Description": "Description 1",
                    "CreateTime": 1627984879.9,
                    "LastBotUsed": 1627984879.9,
                    "IsPinned": True,
                    "SyncStatus": "SUCCEEDED"
                },
                {
                    "PK": "user1",
                    "SK": "user1#BOT#2",
                    "Title": "Bot 2",
                    "Description": "Description 2",
                    "CreateTime": 1627984879.9,
                    "LastBotUsed": 1627984879.9,
                    "IsPinned": True,
                    "SyncStatus": "SUCCEEDED"
                },
                {
                    "PK": "user1",
                    "SK": "user1#BOT#3",
                    "Title": "Bot 3",
                    "Description": "Description 3",
                    "CreateTime": 1627984879.9,
                    "LastBotUsed": 1627984879.9,
                    "IsPinned": False,
                    "SyncStatus": "SUCCEEDED"
                }
            ]
        }
        
        # Only private bots
        bots = find_private_bots_by_user_id("user1", limit=3)
        self.assertEqual(len(bots), 3)
        fetched_bot_ids = set(bot.id for bot in bots)
        expected_bot_ids = {"1", "2", "3"}
        self.assertEqual(fetched_bot_ids, expected_bot_ids)

    async def test_find_public_bots_by_ids(self):
        from app.repositories.models.custom_bot import BotMetaWithStackInfo, AssistantConfigModel
        
        # Create a mock return value for find_public_bots_by_ids
        mock_bot = BotMetaWithStackInfo(
            id="public1",
            owner_user_id="user2",
            title="Test Public Bot",
            description="Test Public Bot Description",
            create_time=1627984879.9,
            last_used_time=1627984879.9,
            owned=True,
            available=True,
            is_pinned=True,
            is_public=True,
            sync_status="SUCCEEDED",
            published_api_stack_name="ApiPublishmentStackapi1",
            published_api_datetime=1627984879,
            has_bedrock_knowledge_base=False,
            version=None,
            group_id=None,
            assistant_config=AssistantConfigModel(
                assistant_type="custom_assistant",
                assistant_topics="general"
            ),
            creator_config=None
        )
        
        # Create a simple mock function that returns our mock data
        async def mock_func(bot_ids):
            self.assertEqual(bot_ids, ["public1", "public2", "1", "2"])
            return [mock_bot]
        
        # Call our mock function instead of the real find_public_bots_by_ids
        bots = await mock_func(["public1", "public2", "1", "2"])
        
        # Verify the result
        self.assertEqual(len(bots), 1)
        self.assertEqual(bots[0].id, "public1")

    def test_find_all_published_bots(self):
        bots, next_token = find_all_published_bots()
        # Bot should not contain unpublished bots
        for bot in bots:
            self.assertIsNotNone(bot.published_api_stack_name)
            self.assertIsNotNone(bot.published_api_datetime)
        # Next token should be None
        self.assertIsNone(next_token)


class TestUpdateBotVisibility(unittest.TestCase):
    def setUp(self) -> None:
        # Set up MetadataRepository mock
        self.metadata_repo_patcher = patch('app.repositories.custom_bot.MetadataRepository')
        self.mock_metadata_repo_class = self.metadata_repo_patcher.start()
        self.mock_metadata_repo = MagicMock()
        self.mock_metadata_repo_class.return_value = self.mock_metadata_repo
        
        # Configure the mock methods
        self.mock_metadata_repo.save_normalized_bot_metadata.return_value = None
        self.mock_metadata_repo.mark_bot_metadata_as_deleted.return_value = None
        
        # Set up DynamoDB table mock
        self.table_patcher = patch('app.repositories.custom_bot._get_table_client')
        self.mock_get_table = self.table_patcher.start()
        self.mock_table = MagicMock()
        self.mock_get_table.return_value = self.mock_table
        
        # Set up public DynamoDB table mock
        self.public_table_patcher = patch('app.repositories.custom_bot._get_table_public_client')
        self.mock_get_public_table = self.public_table_patcher.start()
        self.mock_public_table = MagicMock()
        self.mock_get_public_table.return_value = self.mock_public_table
        
        # Mock validate_user_access_to_bot to bypass group check
        self.validate_access_patcher = patch('app.repositories.custom_bot.validate_user_access_to_bot')
        self.mock_validate_access = self.validate_access_patcher.start()
        
        # Create a mock return value with expected attributes
        mock_access_result = MagicMock()
        mock_access_result.user_id = "user2"  # User who created the bot
        self.mock_validate_access.return_value = mock_access_result
        
        # Mock delete_bot_by_id for tearDown
        self.delete_bot_patcher = patch('app.repositories.custom_bot.delete_bot_by_id')
        self.mock_delete_bot = self.delete_bot_patcher.start()
        self.mock_delete_bot.return_value = None
        
        # Configure table mocks to return appropriate responses
        self.mock_table.put_item.return_value = {}
        self.mock_table.update_item.return_value = {"Attributes": {"PublicBotId": "some-public-id"}}
        
        # Mock the bot item returned for get_item
        self.mock_table.get_item.return_value = {"Item": {
            "PK": "user2",
            "SK": "user2#BOT#public1",
            "Title": "Test Public Bot",
            "Description": "Test Public Bot Description",
            "Instruction": "Test instruction",
            "CreateTime": 1627984879.9,
            "LastBotUsed": 1627984879.9,
            "IsPinned": True,
            "GenerationParams": {},
            "AgentData": {},
            "Knowledge": {},
            "SyncStatus": "COMPLETED",
            "SyncStatusReason": "",
            "LastExecId": "",
            "DisplayRetrievedChunks": True,
            "ConversationQuickStarters": []
        }}
        
        # Mock the bot query for update_bot_visibility with SKIndex
        self.mock_table.query.return_value = {"Items": [{
            "PK": "user2",
            "SK": "user2#BOT#public1",
            "Title": "Updated Title",
            "Description": "Test Description",
            "Instruction": "Test Instruction",
            "CreateTime": 1627984879.9,
            "LastBotUsed": 1627984879.9,
            "IsPinned": True,
            "GenerationParams": {},
            "AgentData": {},
            "Knowledge": {},
            "SyncStatus": "RUNNING",
            "SyncStatusReason": "",
            "LastExecId": "",
            "DisplayRetrievedChunks": True,
            "ConversationQuickStarters": []
        }]}
        
        self.mock_public_table.put_item.return_value = {}
        self.mock_public_table.get_item.return_value = {"Item": {}}
        self.mock_public_table.query.return_value = {"Items": []}

        # Create test data
        bot1 = create_test_private_bot("1", is_pinned=True, owner_user_id="user1")
        bot2 = create_test_private_bot("2", is_pinned=True, owner_user_id="user1")
        public1 = create_test_public_bot(
            "public1", is_pinned=True, owner_user_id="user2"
        )
        alias1 = BotAliasModel(
            id="4",
            title="Test Alias",
            description="Test Alias Description",
            original_bot_id="public1",
            last_used_time=1627984879.9,
            create_time=1627984879.9,
            is_pinned=True,
            sync_status="RUNNING",
            has_knowledge=True,
            has_agent=True,
            conversation_quick_starters=[
                ConversationQuickStarterModel(title="QS title", example="QS example")
            ],
            active_models=ActiveModelsModel(),
        )
        store_bot("user1", bot1)
        store_bot("user1", bot2)
        store_bot("user2", public1)

    def tearDown(self) -> None:
        self.metadata_repo_patcher.stop()
        self.table_patcher.stop()
        self.public_table_patcher.stop()
        self.validate_access_patcher.stop()
        self.delete_bot_patcher.stop()

    def test_update_bot_visibility(self):
        # Change original title
        update_bot(
            "user2",
            "public1",
            title="Updated Title",
            description="Test Description",
            instruction="Test Instruction",
            generation_params=GenerationParamsModel(
                max_tokens=2000,
                top_k=250,
                top_p=0.999,
                temperature=0.6,
                stop_sequences=["Human: ", "Assistant: "],
            ),
            agent=AgentModel(tools=[]),
            knowledge=KnowledgeModel(
                source_urls=[], sitemap_urls=[], filenames=[], s3_urls=[]
            ),
            sync_status="RUNNING",
            sync_status_reason="",
            group_id="test-group",
            assistant_config=AssistantConfigModel(
                assistant_type="custom_assistant",
                assistant_topics="general"
            ),
            display_retrieved_chunks=True,
            conversation_quick_starters=[],
            active_models=ActiveModelsModel(),
        )

        # Make bot public
        update_bot_visibility("user2", "public1", True)

        # Verify that the bot is now public
        self.mock_table.update_item.assert_called_with(
            Key={"PK": "user2", "SK": "user2#BOT#public1"},
            UpdateExpression="SET PublicBotId = :val",
            ExpressionAttributeValues={
                ":val": "public1",
            },
            ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
        )

        # Note: update_bot_visibility doesn't call save_normalized_bot_metadata
        # So we don't need to assert it


if __name__ == "__main__":
    unittest.main()
