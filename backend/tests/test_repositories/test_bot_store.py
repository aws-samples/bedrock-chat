"""Tests for bot_store repository using mocked AWS clients."""

import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, ".")

import logging

from app.repositories.bot_store import (
    _is_bot_accessible,
    find_bots_by_query,
    find_bots_sorted_by_usage_count,
    find_random_bots,
)
from app.user import User


class TestIsBotAccessible(unittest.TestCase):
    def setUp(self):
        self.user1 = User(
            id="user1", name="user1", groups=["group1"], email="u1@example.com"
        )
        self.admin = User(
            id="admin", name="admin", groups=["Admin"], email="admin@example.com"
        )

    def test_public_bot_accessible_by_anyone(self):
        meta = {"SharedScope": "all", "PK": "other-user"}
        self.assertTrue(_is_bot_accessible(meta, self.user1))

    def test_private_bot_accessible_by_owner(self):
        meta = {"SharedScope": "private", "PK": "user1"}
        self.assertTrue(_is_bot_accessible(meta, self.user1))

    def test_private_bot_not_accessible_by_other(self):
        meta = {"SharedScope": "private", "PK": "other-user"}
        self.assertFalse(_is_bot_accessible(meta, self.user1))

    def test_partial_bot_accessible_by_admin(self):
        meta = {"SharedScope": "partial", "PK": "other-user", "AllowedCognitoUsers": [], "AllowedCognitoGroups": []}
        self.assertTrue(_is_bot_accessible(meta, self.admin))

    def test_partial_bot_accessible_by_allowed_user(self):
        meta = {"SharedScope": "partial", "PK": "other-user", "AllowedCognitoUsers": ["user1"], "AllowedCognitoGroups": []}
        self.assertTrue(_is_bot_accessible(meta, self.user1))

    def test_partial_bot_accessible_by_group(self):
        meta = {"SharedScope": "partial", "PK": "other-user", "AllowedCognitoUsers": [], "AllowedCognitoGroups": ["group1"]}
        self.assertTrue(_is_bot_accessible(meta, self.user1))

    def test_partial_bot_not_accessible_by_other(self):
        meta = {"SharedScope": "partial", "PK": "other-user", "AllowedCognitoUsers": ["user2"], "AllowedCognitoGroups": ["group2"]}
        self.assertFalse(_is_bot_accessible(meta, self.user1))


class TestFindBotsByQuery(unittest.TestCase):
    def setUp(self):
        self.user = User(id="user1", name="user1", groups=[], email="u1@example.com")

    @patch("app.repositories.bot_store.S3_VECTORS_BOT_BUCKET_NAME", "")
    def test_returns_empty_when_bucket_not_configured(self):
        result = find_bots_by_query("test", self.user)
        self.assertEqual(result, [])

    @patch("app.repositories.bot_store.S3_VECTORS_BOT_BUCKET_NAME", "test-bucket")
    @patch("app.repositories.bot_store._embed")
    @patch("app.repositories.bot_store._get_s3vectors")
    def test_filters_by_access_control(self, mock_get_s3vectors, mock_embed):
        mock_embed.return_value = [0.1] * 1024
        mock_client = MagicMock()
        mock_get_s3vectors.return_value = mock_client
        mock_client.query_vectors.return_value = {
            "vectors": [
                {
                    "key": "bot1",
                    "metadata": {
                        "BotId": "bot1",
                        "Title": "Public Bot",
                        "Description": "",
                        "SharedScope": "all",
                        "SharedStatus": "shared",
                        "SyncStatus": "RUNNING",
                        "PK": "other-user",
                        "CreateTime": 1000.0,
                        "LastUsedTime": 1000.0,
                    },
                },
                {
                    "key": "bot2",
                    "metadata": {
                        "BotId": "bot2",
                        "Title": "Private Bot",
                        "Description": "",
                        "SharedScope": "private",
                        "SharedStatus": "unshared",
                        "SyncStatus": "RUNNING",
                        "PK": "other-user",
                        "CreateTime": 1000.0,
                        "LastUsedTime": 1000.0,
                    },
                },
            ]
        }
        result = find_bots_by_query("test", self.user)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "bot1")


class TestFindBotsSortedByUsageCount(unittest.TestCase):
    def setUp(self):
        self.user = User(id="user1", name="user1", groups=[], email="u1@example.com")

    @patch("app.repositories.bot_store.get_bot_table_client")
    def test_sorts_by_usage_count(self, mock_get_table):
        mock_table = MagicMock()
        mock_get_table.return_value = mock_table
        mock_table.query.return_value = {
            "Items": [
                {
                    "BotId": "bot-low",
                    "PK": "user1",
                    "SK": "BOT#bot-low",
                    "ItemType": "BOT",
                    "Title": "Low",
                    "Description": "",
                    "CreateTime": 1000.0,
                    "SharedScope": "all",
                    "SharedStatus": "shared",
                    "SyncStatus": "RUNNING",
                    "UsageStats": {"usage_count": 5},
                },
                {
                    "BotId": "bot-high",
                    "PK": "user1",
                    "SK": "BOT#bot-high",
                    "ItemType": "BOT",
                    "Title": "High",
                    "Description": "",
                    "CreateTime": 1000.0,
                    "SharedScope": "all",
                    "SharedStatus": "shared",
                    "SyncStatus": "RUNNING",
                    "UsageStats": {"usage_count": 50},
                },
            ]
        }
        result = find_bots_sorted_by_usage_count(self.user, limit=10)
        self.assertEqual(result[0].id, "bot-high")
        self.assertEqual(result[1].id, "bot-low")


if __name__ == "__main__":
    unittest.main()
