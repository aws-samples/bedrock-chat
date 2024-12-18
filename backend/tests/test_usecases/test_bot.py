import datetime
import logging
import sys

sys.path.insert(0, ".")
import unittest

logger = logging.getLogger()
logger.level = logging.DEBUG

from pydantic import BaseModel

from tests.test_usecases.utils.bot_factory import (
    create_test_bot_alias,
    create_test_private_bot,
    create_test_public_bot,
)

from app.repositories.custom_bot import (
    delete_alias_by_id,
    delete_bot_by_id,
    store_alias,
    store_bot,
    update_alias_last_used_time,
    update_bot_last_used_time,
    update_bot_publication,
    update_bot_visibility,
)

from app.usecases.bot import fetch_all_bots_by_user_id, issue_presigned_url

from app.repositories.common import RecordNotFoundError
from app.repositories.models.custom_bot import BotAliasModel, BotModel, AgentModel, GenerationParamsModel, KnowledgeModel, ActiveModelsModel
from app.routes.schemas.bot import BotSummaryOutput, ConversationQuickStarter, ActiveModelsOutput
from app.usecases.bot import fetch_bot_summary
from unittest.mock import patch, MagicMock


class TestIssuePresignedUrl(unittest.TestCase):
    def test_issue_presigned_url(self):
        url = issue_presigned_url(
            "test_user", "test_bot", "test_file", content_type="image/png"
        )
        self.assertEqual(type(url), str)
        self.assertTrue(url.startswith("https://"))


class TestFindAllBots(unittest.IsolatedAsyncioTestCase):
    first_user_id = "user1"
    second_user_id = "user2"

    first_public_bot_id = "public1"
    second_public_bot_id = "public2"

    first_bot_alias_id = "alias1"
    second_bot_alias_id = "alias2"

    first_bot_id = "1"
    second_bot_id = "2"
    third_bot_id = "3"
    fourth_bot_id = "4"

    def setUp(self) -> None:
        bot1 = create_test_private_bot(self.first_bot_id, True, self.first_user_id)
        bot2 = create_test_private_bot(self.second_bot_id, True, self.first_user_id)
        bot3 = create_test_private_bot(self.third_bot_id, False, self.first_user_id)
        bot4 = create_test_private_bot(self.fourth_bot_id, False, self.first_user_id)

        public_bot1 = create_test_public_bot(
            self.first_public_bot_id, True, self.second_user_id
        )
        public_bot2 = create_test_public_bot(
            self.second_public_bot_id, True, self.second_user_id
        )

        alias1 = create_test_bot_alias(
            self.first_bot_alias_id, self.first_public_bot_id, True
        )
        alias2 = create_test_bot_alias(
            self.second_bot_alias_id, self.second_public_bot_id, False
        )

        store_bot(self.first_user_id, bot1)
        store_bot(self.first_user_id, bot2)
        store_bot(self.first_user_id, bot3)
        store_bot(self.first_user_id, bot4)
        store_bot(self.second_user_id, public_bot1)
        store_bot(self.second_user_id, public_bot2)
        update_bot_visibility(self.second_user_id, self.first_public_bot_id, True)
        update_bot_visibility(self.second_user_id, self.second_public_bot_id, True)
        store_alias(self.first_user_id, alias1)
        store_alias(self.first_user_id, alias2)
        update_bot_publication(
            self.second_user_id, self.first_public_bot_id, "api1", "build1"
        )

    def tearDown(self) -> None:
        delete_bot_by_id(self.first_user_id, self.first_bot_id)
        delete_bot_by_id(self.first_user_id, self.second_bot_id)
        delete_bot_by_id(self.first_user_id, self.third_bot_id)
        delete_bot_by_id(self.first_user_id, self.fourth_bot_id)
        delete_bot_by_id(self.second_user_id, self.first_public_bot_id)
        delete_bot_by_id(self.second_user_id, self.second_public_bot_id)
        delete_alias_by_id(self.first_user_id, self.first_bot_alias_id)
        delete_alias_by_id(self.first_user_id, self.second_bot_alias_id)

    def test_limit(self):
        # Private + public bots
        bots = fetch_all_bots_by_user_id(self.first_user_id, limit=3)
        self.assertEqual(len(bots), 3)
        fetched_bot_ids = set(bot.id for bot in bots)
        expected_bot_ids = {
            self.first_public_bot_id,
            self.second_public_bot_id,
            self.first_bot_id,
            self.second_bot_id,
            self.third_bot_id,
            self.fourth_bot_id,
        }
        self.assertTrue(fetched_bot_ids.issubset(expected_bot_ids))

    def test_find_pinned_bots(self):
        # Only pinned bots fetched
        bots = fetch_all_bots_by_user_id(self.first_user_id, only_pinned=True)
        self.assertEqual(len(bots), 3)

        fetched_bot_ids = set(bot.id for bot in bots)
        expected_bot_ids = {
            self.first_bot_id,
            self.second_bot_id,
            self.first_public_bot_id,
        }

        self.assertTrue(expected_bot_ids.issubset(fetched_bot_ids))

    def test_order_is_descending(self):
        # 1 -> 3 -> alias1 (public1) -> 2 -> 4 -> alias2 (public2)
        update_bot_last_used_time(self.first_user_id, self.first_bot_id)
        update_bot_last_used_time(self.first_user_id, self.third_bot_id)
        update_alias_last_used_time(self.first_user_id, self.first_bot_alias_id)
        update_bot_last_used_time(self.first_user_id, self.second_bot_id)
        update_bot_last_used_time(self.first_user_id, self.fourth_bot_id)
        update_alias_last_used_time(self.first_user_id, self.second_bot_alias_id)

        # Should be alias2 -> 4 -> 2 -> alias1 -> 3 -> 1
        bots = fetch_all_bots_by_user_id(self.first_user_id, limit=6)
        self.assertEqual(len(bots), 6)
        self.assertEqual(bots[0].id, self.second_public_bot_id)
        self.assertEqual(bots[1].id, self.fourth_bot_id)
        self.assertEqual(bots[2].id, self.second_bot_id)
        self.assertEqual(bots[3].id, self.first_public_bot_id)
        self.assertEqual(bots[4].id, self.third_bot_id)
        self.assertEqual(bots[5].id, self.first_bot_id)


class TestFetchBotSummary(unittest.TestCase):

    def setUp(self):
        self._logging_stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(self._logging_stream_handler)
    
    def tearDown(self):
        logger.removeHandler(self._logging_stream_handler)

    @patch('app.usecases.bot.find_private_bot_by_id')
    @patch('app.usecases.bot.find_alias_by_id')  
    @patch('app.usecases.bot.find_public_bot_by_id')
    def test_fetch_bot_summary_alias_bot(self, mock_find_public, mock_find_alias, mock_find_private):
        """Test fetch_bot_summary for an alias bot - where an alias already exists"""

        mock_public_bot = BotModel(
            id="public_bot_id",
            title="Test Public Bot", 
            description="A test public bot",
            instruction="Test instruction",
            create_time=1234567890,
            last_used_time=1234567891,
            is_pinned=True,
            public_bot_id=None,
            owner_user_id="test_owner",
            generation_params=GenerationParamsModel(max_tokens=1,temperature=1,top_k=1,top_p=1,stop_sequences=["Test"]),
            agent=AgentModel(tools=[]),
            knowledge=KnowledgeModel(source_urls=[], sitemap_urls=[], filenames=[], s3_urls=[]),
            sync_status="SUCCEEDED",
            sync_status_reason="",
            sync_last_exec_id="",
            display_retrieved_chunks=True,
            conversation_quick_starters=[],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
            active_models=ActiveModelsModel(chat="claude-v1", embedding="amazon.titan-embed-text-v1"),
            published_api_codebuild_id='test',
            published_api_datetime=1704067200,  # 2024-01-01 00:00:00 UTC
            published_api_stack_name='test'
        )
        mock_find_public.return_value = mock_public_bot

        mock_find_private.side_effect = RecordNotFoundError()
        mock_alias = BotAliasModel(
            id="alias_bot_id",
            title=mock_public_bot.title,
            description=mock_public_bot.description,
            original_bot_id=mock_public_bot.id,
            create_time=1234567890,
            last_used_time=1234567891,
            is_pinned=mock_public_bot.is_pinned,
            sync_status=mock_public_bot.sync_status,
            has_knowledge=mock_public_bot.has_knowledge(),
            has_agent=True,
            conversation_quick_starters=mock_public_bot.conversation_quick_starters,
            active_models=mock_public_bot.active_models
        )
        mock_find_alias.return_value = mock_alias

        result = fetch_bot_summary("valid_user_id", "public_bot_id")
        
        self.assertEqual(result.id, "alias_bot_id") 
        self.assertFalse(result.owned)
        self.assertTrue(result.is_public)
        
    @patch('app.usecases.bot.find_private_bot_by_id')
    @patch('app.usecases.bot.find_alias_by_id')
    @patch('app.usecases.bot.find_public_bot_by_id')
    def test_fetch_bot_summary_incorrect_type(self, mock_find_public, mock_find_alias, mock_find_private):
        """Test fetch_bot_summary with incorrect input types"""
        with self.assertRaises(TypeError):
            fetch_bot_summary(123, "valid_bot_id")
        
        with self.assertRaises(TypeError):
            fetch_bot_summary("valid_user_id", 456)

    @patch('app.usecases.bot.find_private_bot_by_id')
    @patch('app.usecases.bot.find_alias_by_id')
    @patch('app.usecases.bot.find_public_bot_by_id')
    def test_fetch_bot_summary_invalid_input(self, mock_find_public, mock_find_alias, mock_find_private):
        """Test fetch_bot_summary with invalid input"""
        with self.assertRaises(ValueError):
            fetch_bot_summary("", "valid_bot_id")
        
        with self.assertRaises(ValueError):
            fetch_bot_summary("valid_user_id", "")

    @patch('app.usecases.bot.find_private_bot_by_id')
    @patch('app.usecases.bot.find_alias_by_id')
    @patch('app.usecases.bot.find_public_bot_by_id')
    def test_fetch_bot_summary_not_found(self, mock_find_public, mock_find_alias, mock_find_private):
        """Test fetch_bot_summary when bot is not found"""
        mock_find_private.side_effect = RecordNotFoundError()
        mock_find_alias.side_effect = RecordNotFoundError()
        mock_find_public.side_effect = RecordNotFoundError()

        with self.assertRaises(RecordNotFoundError):
            fetch_bot_summary("valid_user_id", "non_existent_bot_id")

    def test_fetch_bot_summary_private_bot(self):
        """Test fetch_bot_summary for a private bot"""
        user_id = "test_user"
        bot_id = "test_bot"
        
        mock_bot = BotModel(
            id=bot_id,
            title="Test Bot",
            description="A test bot",
            instruction="Test instruction",
            create_time=1234567890,
            last_used_time=1234567891,
            is_pinned=True,
            public_bot_id=None,
            owner_user_id=user_id,
            generation_params=None,
            agent=AgentModel(tools=[]),
            knowledge=KnowledgeModel(source_urls=["https://example.com"], sitemap_urls=[], filenames=[], s3_urls=[]),
            sync_status="SUCCEEDED",
            sync_status_reason="",
            sync_last_exec_id="",
            display_retrieved_chunks=True,
            conversation_quick_starters=[
                ConversationQuickStarter(title="Quick Start 1", example="Example 1")
            ],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
            active_models=ActiveModelsModel(chat="claude-v1", embedding="amazon.titan-embed-text-v1")
        )

        with patch('app.usecases.bot.find_private_bot_by_id', return_value=mock_bot):
            result = fetch_bot_summary(user_id, bot_id)

        expected_output = BotSummaryOutput(
            id=bot_id,
            title="Test Bot",
            description="A test bot",
            create_time=1234567890,
            last_used_time=1234567891,
            is_pinned=True,
            is_public=False,
            has_agent=False,
            owned=True,
            sync_status="SUCCEEDED",
            has_knowledge=True,
            conversation_quick_starters=[
                ConversationQuickStarter(title="Quick Start 1", example="Example 1")
            ],
            active_models=ActiveModelsOutput(chat="claude-v1", embedding="amazon.titan-embed-text-v1")
        )

        self.assertEqual(result, expected_output)

    @patch('app.usecases.bot.find_private_bot_by_id')
    @patch('app.usecases.bot.find_alias_by_id')
    @patch('app.usecases.bot.find_public_bot_by_id')
    @patch('app.usecases.bot.store_alias')
    def test_fetch_bot_summary_public_bot_no_alias(self, mock_store_alias, mock_find_public, mock_find_alias, mock_find_private):
        """Test fetch_bot_summary for a public bot without an existing alias"""
        mock_find_private.side_effect = RecordNotFoundError()
        mock_find_alias.side_effect = RecordNotFoundError()
        mock_public_bot = BotModel(
            id="public_bot_id",
            title="Test Public Bot", 
            description="A test public bot",
            instruction="Test instruction",
            create_time=1234567890,
            last_used_time=1234567891,
            is_pinned=True,
            public_bot_id=None,
            owner_user_id="test_owner",
            generation_params=GenerationParamsModel(max_tokens=1,temperature=1,top_k=1,top_p=1,stop_sequences=["Test"]),
            agent=AgentModel(tools=[]),
            knowledge=KnowledgeModel(source_urls=[], sitemap_urls=[], filenames=[], s3_urls=[]),
            sync_status="SUCCEEDED",
            sync_status_reason="",
            sync_last_exec_id="",
            display_retrieved_chunks=True,
            conversation_quick_starters=[],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
            active_models=ActiveModelsModel(chat="claude-v1", embedding="amazon.titan-embed-text-v1"),
            published_api_codebuild_id='test',
            published_api_datetime=1704067200,  # 2024-01-01 00:00:00 UTC
            published_api_stack_name='test'
        )
        mock_public_bot.id = "public_bot_id"
        mock_find_public.return_value = mock_public_bot

        result = fetch_bot_summary("valid_user_id", "public_bot_id")
        
        self.assertEqual(result.id, "public_bot_id")
        self.assertFalse(result.owned)
        self.assertTrue(result.is_public)
        mock_store_alias.assert_called_once()

if __name__ == "__main__":
    unittest.main()