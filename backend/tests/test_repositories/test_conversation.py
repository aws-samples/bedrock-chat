import base64
import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(".")


from app.repositories.conversation import (
    ConversationModel,
    MessageModel,
    RecordNotFoundError,
    change_conversation_title,
    delete_conversation_by_id,
    delete_conversation_by_user_id,
    find_conversation_by_id,
    find_conversation_by_user_id,
    store_conversation,
    update_feedback,
)
from app.repositories.custom_bot import (
    delete_bot_by_id,
    find_private_bots_by_user_id,
    store_bot,
)
from app.repositories.models.conversation import (
    ChunkModel,
    FeedbackModel,
    ImageContentModel,
    SimpleMessageModel,
    TextContentModel,
    ToolUseContentModel,
    ToolUseContentModelBody,
)
from app.repositories.models.custom_bot import (
    ActiveModelsModel,
    AgentModel,
    BotModel,
    ConversationQuickStarterModel,
    GenerationParamsModel,
    KnowledgeModel,
    ToolModel,
)
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# class TestRowLevelAccess(unittest.TestCase):
#     def setUp(self) -> None:
#         self.conversation_user_1 = ConversationModel(
#             id="1",
#             create_time=1627984879.9,
#             title="Test Conversation",
#             message_map={
#                 "a": MessageModel(
#                     role="user",
#                     content=TextContentModel(content_type="text", body="Hello"),
#                     model="model",
#                     children=["x", "y"],
#                     parent="z",
#                     create_time=1627984879.9,
#                 )
#             },
#             last_message_id="x",
#         )
#         store_conversation("user1", self.conversation_user_1)

#         self.conversation_user_2 = ConversationModel(
#             id="2",
#             create_time=1627984879.9,
#             title="Test Conversation",
#             message_map={
#                 "a": MessageModel(
#                     role="user",
#                     content=TextContentModel(content_type="text", body="Hello"),
#                     model="model",
#                     children=["x", "y"],
#                     parent="z",
#                     create_time=1627984879.9,
#                 )
#             },
#             last_message_id="x",
#         )
#         store_conversation("user2", self.conversation_user_2)

#     def test_find_conversation_by_user_id(self):
#         # Create table client for user1
#         table = _get_table_client("user1")

#         table.query(
#             KeyConditionExpression=Key("PK").eq(
#                 compose_conv_id("user1", self.conversation_user_1.id)
#             )
#         )

#         with self.assertRaises(ClientError):
#             # Raise `AccessDeniedException` because user1 cannot access user2's data
#             table.query(
#                 KeyConditionExpression=Key("PK").eq(
#                     compose_conv_id("user2", self.conversation_user_2.id)
#                 )
#             )

#     def test_find_conversation_by_id(self):
#         # Create table client for user1
#         table = _get_table_client("user1")

#         table.query(
#             IndexName="SKIndex",
#             KeyConditionExpression=Key("SK").eq(
#                 compose_conv_id("user1", self.conversation_user_1.id)
#             ),
#         )
#         with self.assertRaises(ClientError):
#             # Raise `AccessDeniedException` because user1 cannot access user2's data
#             table.query(
#                 IndexName="SKIndex",
#                 KeyConditionExpression=Key("SK").eq(
#                     compose_conv_id("user2", self.conversation_user_2.id)
#                 ),
#             )

#     def tearDown(self) -> None:
#         delete_conversation_by_user_id("user1")
#         delete_conversation_by_user_id("user2")


class TestConversationRepository(unittest.TestCase):
    def setUp(self):
        self.patcher1 = patch("boto3.resource")
        self.patcher2 = patch("app.repositories.conversation.s3_client")
        self.mock_boto3_resource = self.patcher1.start()
        self.mock_s3_client = self.patcher2.start()

        self.mock_table = MagicMock()
        self.mock_boto3_resource.return_value.Table.return_value = self.mock_table

        # Set up environment variables
        os.environ["CONVERSATION_TABLE_NAME"] = "test-table"
        os.environ["CONVERSATION_BUCKET_NAME"] = "test-bucket"
        os.environ["LARGE_MESSAGE_BUCKET"] = "test-large-message-bucket"
        os.environ["BEDROCK_REGION"] = "us-east-1"

        self.title_updated = False
        self.feedback_updated = False
        self.conversation_deleted = False

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        os.environ.pop("CONVERSATION_TABLE_NAME", None)
        os.environ.pop("CONVERSATION_BUCKET_NAME", None)
        os.environ.pop("LARGE_MESSAGE_BUCKET", None)
        os.environ.pop("BEDROCK_REGION", None)

    def test_store_and_find_conversation(self):
        conversation = ConversationModel(
            id="1",
            create_time=1627984879.9,
            title="Test Conversation",
            total_price=100,
            message_map={
                "a": MessageModel(
                    role="user",
                    content=[
                        TextContentModel(
                            content_type="text",
                            body="Hello",
                        ),
                        ImageContentModel(
                            content_type="image",
                            body=base64.b64decode(
                                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
                            ),
                            media_type="image/png",
                        ),
                    ],
                    model="claude-instant-v1",
                    children=["x", "y"],
                    parent="z",
                    create_time=1627984879.9,
                    feedback=None,
                    used_chunks=[
                        ChunkModel(
                            content="chunk1",
                            source="source1",
                            rank=1,
                            content_type="url",
                        ),
                    ],
                    thinking_log=[
                        SimpleMessageModel(
                            role="agent",
                            content=[
                                ToolUseContentModel(
                                    content_type="toolUse",
                                    body=ToolUseContentModelBody(
                                        tool_use_id="xyz1234",
                                        name="internet_search",
                                        input={
                                            "query": "Google news",
                                            "country": "us-en",
                                            "time_limit": "d",
                                        },
                                    ),
                                )
                            ],
                        )
                    ],
                )
            },
            last_message_id="x",
            bot_id=None,
            should_continue=False,
        )

        # Mock the responses
        self.mock_table.put_item.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        def mock_query_side_effect(**kwargs):
            if self.conversation_deleted:
                return {"Items": []}

            if "IndexName" in kwargs and kwargs["IndexName"] == "SKIndex":
                message_map = conversation.model_dump()["message_map"]
                if self.feedback_updated:
                    message_map["a"]["feedback"] = {
                        "thumbs_up": True,
                        "category": "Good",
                        "comment": "The response is pretty good.",
                    }
                return {
                    "Items": [
                        {
                            "PK": "user",
                            "SK": "user#CONV#1",
                            "Title": (
                                "Updated title"
                                if self.title_updated
                                else "Test Conversation"
                            ),
                            "CreateTime": 1627984879.9,
                            "TotalPrice": 100,
                            "LastMessageId": "x",
                            "MessageMap": json.dumps(message_map),
                            "IsLargeMessage": False,
                            "ShouldContinue": False,
                        }
                    ]
                }
            return {
                "Items": (
                    []
                    if self.conversation_deleted
                    else [
                        {
                            "PK": "user",
                            "SK": "user#CONV#1",
                            "Title": "Test Conversation",
                            "CreateTime": 1627984879.9,
                            "TotalPrice": 100,
                            "LastMessageId": "x",
                            "MessageMap": json.dumps(
                                conversation.model_dump()["message_map"]
                            ),
                            "IsLargeMessage": False,
                            "ShouldContinue": False,
                        }
                    ]
                )
            }

        self.mock_table.query.side_effect = mock_query_side_effect

        # Test storing conversation
        response = store_conversation("user", conversation)
        self.assertIsNotNone(response)

        # Test finding conversation by user_id
        conversations = find_conversation_by_user_id(user_id="user")
        self.assertEqual(len(conversations), 1)

        # Test finding conversation by id
        found_conversation = find_conversation_by_id(
            user_id="user", conversation_id="1"
        )
        self.assertEqual(found_conversation.id, "1")
        self.assertEqual(found_conversation.title, "Test Conversation")

        message_map = found_conversation.message_map
        # Assert whether the message map is correctly reconstructed
        self.assertEqual(message_map["a"].role, "user")
        content = message_map["a"].content
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0].content_type, "text")
        self.assertEqual(content[0].body, "Hello")
        self.assertEqual(content[1].content_type, "image")
        # Convert the raw bytes to base64 for comparison
        self.assertEqual(
            base64.b64encode(content[1].body).decode(),
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
        )
        self.assertEqual(message_map["a"].model, "claude-instant-v1")
        self.assertEqual(message_map["a"].children, ["x", "y"])
        self.assertEqual(message_map["a"].parent, "z")
        self.assertEqual(message_map["a"].create_time, 1627984879.9)
        self.assertEqual(len(message_map["a"].used_chunks), 1)  # type: ignore
        self.assertEqual(found_conversation.last_message_id, "x")
        self.assertEqual(found_conversation.total_price, 100)
        self.assertEqual(found_conversation.bot_id, None)
        self.assertEqual(found_conversation.should_continue, False)

        # Agent thinking log
        assert message_map["a"].thinking_log is not None
        self.assertEqual(message_map["a"].thinking_log[0].role, "agent")
        self.assertEqual(
            message_map["a"].thinking_log[0].content[0].content_type, "toolUse"
        )
        self.assertEqual(
            message_map["a"].thinking_log[0].content[0].body.name, "internet_search"  # type: ignore
        )
        self.assertEqual(found_conversation.message_map["a"].content[0].body, "Hello")
        self.assertEqual(
            message_map["a"].thinking_log[0].content[0].body.input["query"], "Google news"  # type: ignore
        )

        # Test update title
        self.title_updated = True
        self.mock_table.update_item.return_value = {
            "Attributes": {"Title": "Updated title"},
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        response = change_conversation_title(
            user_id="user",
            conversation_id="1",
            new_title="Updated title",
        )
        found_conversation = find_conversation_by_id(
            user_id="user", conversation_id="1"
        )
        self.assertEqual(found_conversation.title, "Updated title")

        # Test give a feedback
        self.assertIsNone(found_conversation.message_map["a"].feedback)
        self.feedback_updated = True
        response = update_feedback(
            user_id="user",
            conversation_id="1",
            message_id="a",
            feedback=FeedbackModel(
                thumbs_up=True, category="Good", comment="The response is pretty good."
            ),
        )
        found_conversation = find_conversation_by_id(
            user_id="user", conversation_id="1"
        )
        feedback = found_conversation.message_map["a"].feedback
        self.assertIsNotNone(feedback)
        self.assertEqual(feedback.thumbs_up, True)  # type: ignore
        self.assertEqual(feedback.category, "Good")  # type: ignore
        self.assertEqual(feedback.comment, "The response is pretty good.")  # type: ignore

        # Test deleting conversation by id
        self.conversation_deleted = True
        delete_conversation_by_id(user_id="user", conversation_id="1")
        with self.assertRaises(RecordNotFoundError):
            find_conversation_by_id("user", "1")

        response = store_conversation(user_id="user", conversation=conversation)

        # Test deleting conversation by user_id
        delete_conversation_by_user_id(user_id="user")
        conversations = find_conversation_by_user_id(user_id="user")
        self.assertEqual(len(conversations), 0)

    def test_store_and_find_large_conversation(self):
        large_message_map = {
            f"msg_{i}": MessageModel(
                role="user",
                content=[
                    TextContentModel(
                        content_type="text",
                        body="This is a large message."
                        * 1000,  # Repeating to make it large
                    )
                ],
                model="claude-instant-v1",
                children=[],
                parent=None,
                create_time=1627984879.9,
                feedback=None,
                used_chunks=None,
                thinking_log=None,
            )
            for i in range(10)
        }

        large_conversation = ConversationModel(
            id="2",
            create_time=1627984879.9,
            title="Large Conversation",
            total_price=200,
            message_map=large_message_map,
            last_message_id="msg_9",
            bot_id=None,
            should_continue=False,
        )

        # Mock responses
        self.mock_table.put_item.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }
        self.mock_s3_client.put_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        def mock_query_side_effect(**kwargs):
            if self.conversation_deleted:
                return {"Items": []}

            if "IndexName" in kwargs and kwargs["IndexName"] == "SKIndex":
                return {
                    "Items": [
                        {
                            "PK": "user",
                            "SK": "user#CONV#2",
                            "Title": "Large Conversation",
                            "CreateTime": 1627984879.9,
                            "TotalPrice": 200,
                            "LastMessageId": "msg_9",
                            "IsLargeMessage": True,
                            "LargeMessagePath": "user/2/message_map.json",
                            "MessageMap": json.dumps(
                                {
                                    "system": {
                                        "role": "system",
                                        "content": [
                                            {
                                                "content_type": "text",
                                                "body": "Hello",
                                                "media_type": None,
                                            }
                                        ],
                                        "model": "claude-instant-v1",
                                        "children": [],
                                        "parent": None,
                                        "create_time": 1627984879.9,
                                        "feedback": None,
                                        "used_chunks": None,
                                        "thinking_log": None,
                                    }
                                }
                            ),
                            "ShouldContinue": False,
                        }
                    ]
                }
            return {"Items": []}

        self.mock_table.query.side_effect = mock_query_side_effect

        message_map_json = json.dumps(
            {
                k: {
                    "role": v.role,
                    "content": [c.model_dump() for c in v.content],
                    "model": v.model,
                    "children": v.children,
                    "parent": v.parent,
                    "create_time": v.create_time,
                    "feedback": v.feedback,
                    "used_chunks": v.used_chunks,
                    "thinking_log": v.thinking_log,
                }
                for k, v in large_message_map.items()
            }
        )
        self.mock_s3_client.get_object.return_value = {
            "Body": MagicMock(read=lambda: message_map_json.encode())
        }

        # Test storing large conversation
        response = store_conversation("user", large_conversation, threshold=1)
        self.assertIsNotNone(response)

        # Test finding large conversation by id
        found_conversation = find_conversation_by_id(
            user_id="user", conversation_id="2"
        )
        self.assertEqual(found_conversation.id, "2")
        self.assertEqual(found_conversation.title, "Large Conversation")
        self.assertEqual(found_conversation.total_price, 200)
        self.assertEqual(found_conversation.last_message_id, "msg_9")
        self.assertEqual(found_conversation.bot_id, None)
        self.assertEqual(found_conversation.should_continue, False)
        self.assertEqual(len(found_conversation.message_map), 10)

        for i in range(10):
            message_id = f"msg_{i}"
            self.assertIn(message_id, found_conversation.message_map)
            message = found_conversation.message_map[message_id]
            self.assertEqual(message.role, "user")
            self.assertEqual(len(message.content), 1)
            self.assertEqual(message.content[0].content_type, "text")
            self.assertEqual(message.content[0].body, "This is a large message." * 1000)
            self.assertEqual(message.model, "claude-instant-v1")
            self.assertEqual(message.children, [])
            self.assertEqual(message.parent, None)
            self.assertEqual(message.create_time, 1627984879.9)

        # Test deleting large conversation
        self.conversation_deleted = True
        delete_conversation_by_id(user_id="user", conversation_id="2")
        with self.assertRaises(RecordNotFoundError):
            find_conversation_by_id("user", "2")

        store_conversation(user_id="user", conversation=large_conversation)
        delete_conversation_by_user_id(user_id="user")
        conversations = find_conversation_by_user_id(user_id="user")
        self.assertEqual(len(conversations), 0)


class TestConversationBotRepository(unittest.TestCase):
    def setUp(self):
        self.patcher = patch("boto3.resource")
        self.mock_boto3_resource = self.patcher.start()

        self.mock_table = MagicMock()
        self.mock_boto3_resource.return_value.Table.return_value = self.mock_table

        # Set up environment variables
        os.environ["CONVERSATION_TABLE_NAME"] = "test-table"
        os.environ["CONVERSATION_BUCKET_NAME"] = "test-bucket"

        self.active_models = ActiveModelsModel(
            claude3_sonnet_v1=True,
            claude3_haiku_v1=True,
            claude3_opus_v1=True,
            claude3_5_sonnet_v1=True,
            claude3_5_sonnet_v2=True,
            claude3_5_haiku_v1=True,
        )

        self.conversation1 = ConversationModel(
            id="1",
            create_time=1627984879.9,
            title="Test Conversation",
            total_price=100,
            message_map={
                "a": MessageModel(
                    role="user",
                    content=[
                        TextContentModel(
                            content_type="text",
                            body="Hello",
                        ),
                        ImageContentModel(
                            content_type="image",
                            body=base64.b64decode(
                                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
                            ),
                            media_type="image/png",
                        ),
                    ],
                    model="claude-instant-v1",
                    children=["x", "y"],
                    parent="z",
                    create_time=1627984879.9,
                    feedback=None,
                    used_chunks=None,
                    thinking_log=None,
                )
            },
            last_message_id="x",
            bot_id=None,
            should_continue=False,
        )

        self.conversation2 = ConversationModel(
            id="2",
            create_time=1627984879.9,
            title="Test Conversation",
            total_price=100,
            message_map={
                "a": MessageModel(
                    role="user",
                    content=[
                        TextContentModel(
                            content_type="text",
                            body="Hello",
                        ),
                        ImageContentModel(
                            content_type="image",
                            body=base64.b64decode(
                                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
                            ),
                            media_type="image/png",
                        ),
                    ],
                    model="claude-instant-v1",
                    children=["x", "y"],
                    parent="z",
                    create_time=1627984879.9,
                    feedback=None,
                    used_chunks=None,
                    thinking_log=None,
                )
            },
            last_message_id="x",
            bot_id="1",
            should_continue=False,
        )

        self.bot1 = BotModel(
            id="1",
            title="Test Bot",
            instruction="Test Bot Prompt",
            description="Test Bot Description",
            create_time=1627984879.9,
            last_used_time=1627984879.9,
            public_bot_id="1",
            is_pinned=False,
            owner_user_id="user",
            generation_params=GenerationParamsModel(
                max_tokens=2000,
                top_k=250,
                top_p=0.999,
                temperature=0.6,
                stop_sequences=["Human: ", "Assistant: "],
            ),
            agent=AgentModel(
                tools=[
                    ToolModel(name="tool1", description="tool1 description"),
                    ToolModel(name="tool2", description="tool2 description"),
                ]
            ),
            knowledge=KnowledgeModel(
                source_urls=["https://aws.amazon.com/"],
                sitemap_urls=["https://aws.amazon.sitemap.xml"],
                filenames=["aws.pdf"],
                s3_urls=["s3://example/path/"],
            ),
            sync_status="RUNNING",
            sync_status_reason="reason",
            sync_last_exec_id="",
            published_api_codebuild_id="",
            published_api_datetime=0,
            published_api_stack_name="",
            display_retrieved_chunks=True,
            conversation_quick_starters=[
                ConversationQuickStarterModel(title="QS title", example="QS example")
            ],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
            active_models=self.active_models,
        )

        self.bot2 = BotModel(
            id="2",
            title="Test Bot",
            instruction="Test Bot Prompt",
            description="Test Bot Description",
            create_time=1627984879.9,
            last_used_time=1627984879.9,
            public_bot_id="2",
            is_pinned=False,
            owner_user_id="user",
            generation_params=GenerationParamsModel(
                max_tokens=2000,
                top_k=250,
                top_p=0.999,
                temperature=0.6,
                stop_sequences=["Human: ", "Assistant: "],
            ),
            agent=AgentModel(
                tools=[
                    ToolModel(name="tool1", description="tool1 description"),
                    ToolModel(name="tool2", description="tool2 description"),
                ]
            ),
            knowledge=KnowledgeModel(
                source_urls=["https://aws.amazon.com/"],
                sitemap_urls=["https://aws.amazon.sitemap.xml"],
                filenames=["aws.pdf"],
                s3_urls=[],
            ),
            sync_status="RUNNING",
            sync_status_reason="reason",
            sync_last_exec_id="",
            published_api_codebuild_id="",
            published_api_datetime=0,
            published_api_stack_name="",
            display_retrieved_chunks=True,
            conversation_quick_starters=[
                ConversationQuickStarterModel(title="QS title", example="QS example")
            ],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
            active_models=self.active_models,  # Added the missing field
        )

        store_conversation("user", self.conversation1)
        store_bot("user", self.bot1)
        store_bot("user", self.bot2)
        store_conversation("user", self.conversation2)

    def tearDown(self):
        self.patcher.stop()
        os.environ.pop("CONVERSATION_TABLE_NAME", None)
        os.environ.pop("CONVERSATION_BUCKET_NAME", None)

    def test_only_conversation_is_fetched(self):
        self.mock_table.query.return_value = {
            "Items": [
                {
                    "PK": "user",
                    "SK": "user#CONV#1",
                    "Title": "Test Conversation",
                    "CreateTime": 1627984879.9,
                    "MessageMap": json.dumps(
                        {
                            "system": {
                                "role": "system",
                                "content": [
                                    {
                                        "content_type": "text",
                                        "body": "Hello",
                                        "media_type": None,
                                    }
                                ],
                                "model": "claude-instant-v1",
                                "children": [],
                                "parent": None,
                                "create_time": 1627984879.9,
                                "feedback": None,
                                "used_chunks": None,
                                "thinking_log": None,
                            }
                        }
                    ),
                    "BotId": None,
                }
            ]
        }
        conversations = find_conversation_by_user_id("user")
        self.assertEqual(len(conversations), 1)

    def test_only_bot_is_fetched(self):
        self.mock_table.query.return_value = {
            "Items": [
                {
                    "PK": "user",
                    "SK": "user#BOT#1",
                    "Title": "Test Bot",
                    "Description": "Test Bot Description",
                    "CreateTime": 1627984879.9,
                    "LastBotUsed": 1627984879.9,
                    "IsPinned": False,
                    "SyncStatus": "RUNNING",
                    "BedrockKnowledgeBase": None,
                }
            ]
        }
        bots = find_private_bots_by_user_id("user")
        self.assertEqual(len(bots), 1)


def tearDown(self) -> None:
    delete_conversation_by_user_id("user")
    delete_bot_by_id("user", "1")
    delete_bot_by_id("user", "2")


if __name__ == "__main__":
    unittest.main()
