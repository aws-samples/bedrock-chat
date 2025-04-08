import sys
import unittest
from datetime import datetime

from app.routes.schemas.analytics import (
    DailyUsage,
    TopUser,
    TopicAnalysis,
    UsagePerBot,
    UsagePerUser,
    BotAnalytics,
    MetadataAnalytics,
    FeedbackAnalytics,
    TokenAnalytics,
    AnalyticsDashboard
)


class TestAnalyticsSchemas(unittest.TestCase):
    def test_daily_usage_schema(self):
        """Test the DailyUsage schema validation."""
        # Test valid initialization
        daily = DailyUsage(
            date="2023-01-01",
            num_sessions=10,
            num_messages=50,
            input_tokens=1000,
            output_tokens=500,
            cost=0.25
        )
        
        self.assertEqual(daily.date, "2023-01-01")
        self.assertEqual(daily.num_sessions, 10)
        self.assertEqual(daily.num_messages, 50)
        self.assertEqual(daily.input_tokens, 1000)
        self.assertEqual(daily.output_tokens, 500)
        self.assertEqual(daily.cost, 0.25)
        
        # Test schema validation
        daily_dict = daily.model_dump()
        self.assertIn("date", daily_dict)
        self.assertIn("num_sessions", daily_dict)
        self.assertIn("num_messages", daily_dict)
        self.assertIn("input_tokens", daily_dict)
        self.assertIn("output_tokens", daily_dict)
        self.assertIn("cost", daily_dict)
        
    def test_top_user_schema(self):
        """Test the TopUser schema validation."""
        # Test valid initialization
        user = TopUser(
            user_id="user-1",
            email="user@example.com",
            num_sessions=10,
            num_messages=50,
            total_cost=1.25
        )
        
        self.assertEqual(user.user_id, "user-1")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.num_sessions, 10)
        self.assertEqual(user.num_messages, 50)
        self.assertEqual(user.total_cost, 1.25)
        
        # Test schema validation
        user_dict = user.model_dump()
        self.assertIn("user_id", user_dict)
        self.assertIn("email", user_dict)
        self.assertIn("num_sessions", user_dict)
        self.assertIn("num_messages", user_dict)
        self.assertIn("total_cost", user_dict)
        
    def test_topic_analysis_schema(self):
        """Test the TopicAnalysis schema validation."""
        # Test valid initialization
        topic = TopicAnalysis(
            topic="Science",
            message_count=30,
            percentage=0.3
        )
        
        self.assertEqual(topic.topic, "Science")
        self.assertEqual(topic.message_count, 30)
        self.assertEqual(topic.percentage, 0.3)
        
        # Test schema validation
        topic_dict = topic.model_dump()
        self.assertIn("topic", topic_dict)
        self.assertIn("message_count", topic_dict)
        self.assertIn("percentage", topic_dict)
        
    def test_usage_per_bot_schema(self):
        """Test the UsagePerBot schema validation."""
        # Test valid initialization
        bot_usage = UsagePerBot(
            id="bot-1",
            title="Math Bot",
            description="A bot for math help",
            owner_user_id="user-1",
            total_price=5.0,
            num_of_users=10,
            num_of_convos=50,
            assistant_config={"model": "claude-3"},
            creator_config={"template_id": "math-template"},
            group_id="group-1"
        )
        
        self.assertEqual(bot_usage.id, "bot-1")
        self.assertEqual(bot_usage.title, "Math Bot")
        self.assertEqual(bot_usage.owner_user_id, "user-1")
        self.assertEqual(bot_usage.total_price, 5.0)
        self.assertEqual(bot_usage.num_of_users, 10)
        self.assertEqual(bot_usage.assistant_config["model"], "claude-3")
        
        # Test schema validation
        bot_usage_dict = bot_usage.model_dump()
        self.assertIn("id", bot_usage_dict)
        self.assertIn("title", bot_usage_dict)
        self.assertIn("owner_user_id", bot_usage_dict)
        self.assertIn("total_price", bot_usage_dict)
        self.assertIn("num_of_users", bot_usage_dict)
        self.assertIn("assistant_config", bot_usage_dict)
        
    def test_usage_per_user_schema(self):
        """Test the UsagePerUser schema validation."""
        # Test valid initialization
        user_usage = UsagePerUser(
            id="user-1",
            email="test@example.com",
            total_price=2.5
        )
        
        self.assertEqual(user_usage.id, "user-1")
        self.assertEqual(user_usage.email, "test@example.com")
        self.assertEqual(user_usage.total_price, 2.5)
        
        # Test schema validation
        user_usage_dict = user_usage.model_dump()
        self.assertIn("id", user_usage_dict)
        self.assertIn("email", user_usage_dict)
        self.assertIn("total_price", user_usage_dict)
        
    def test_bot_analytics_schema(self):
        """Test the BotAnalytics schema validation."""
        # Test valid initialization
        analytics = BotAnalytics(
            bot_id="bot-1",
            title="Math Bot", 
            description="A bot for math help",
            owner_user_id="user-1",
            total_users=10,
            total_sessions=50,
            total_messages=250,
            total_input_tokens=5000,
            total_output_tokens=2500,
            total_cost=5.0,
            daily_usage=[
                {"date": "2023-01-01", "num_sessions": 5, "num_messages": 25}
            ],
            top_users=[
                {"user_id": "user-2", "email": "user2@example.com", "num_sessions": 10}
            ],
            top_topics=[
                {"topic": "Algebra", "message_count": 50, "percentage": 20.0}
            ]
        )
        
        self.assertEqual(analytics.bot_id, "bot-1")
        self.assertEqual(analytics.title, "Math Bot")
        self.assertEqual(analytics.total_users, 10)
        self.assertEqual(analytics.total_cost, 5.0)
        self.assertEqual(len(analytics.daily_usage), 1)
        self.assertEqual(len(analytics.top_users), 1)
        self.assertEqual(len(analytics.top_topics), 1)
        
        # Test schema validation
        analytics_dict = analytics.model_dump()
        self.assertIn("bot_id", analytics_dict)
        self.assertIn("title", analytics_dict)
        self.assertIn("total_users", analytics_dict)
        self.assertIn("total_cost", analytics_dict)
        self.assertIn("daily_usage", analytics_dict)
        self.assertIn("top_users", analytics_dict)
        self.assertIn("top_topics", analytics_dict)
        
    def test_analytics_dashboard_schema(self):
        """Test the AnalyticsDashboard schema validation."""
        # Test valid initialization
        # We need to use complete UsagePerBot and UsagePerUser objects due to validation
        dashboard = AnalyticsDashboard(
            total_bots=5,
            total_users=20,
            total_sessions=100,
            total_messages=500,
            total_input_tokens=10000,
            total_output_tokens=5000,
            total_cost=15.0,
            top_bots=[
                UsagePerBot(
                    id="bot-1", 
                    title="Math Bot", 
                    description="A bot for math help",
                    owner_user_id="user-1",
                    total_price=5.0,
                    num_of_users=10,
                    num_of_convos=50
                )
            ],
            top_users=[
                UsagePerUser(
                    id="user-1",
                    email="test@example.com",
                    total_price=3.0
                )
            ],
            daily_usage=[
                DailyUsage(
                    date="2023-01-01",
                    num_sessions=10,
                    num_messages=50
                )
            ]
        )
        
        self.assertEqual(dashboard.total_bots, 5)
        self.assertEqual(dashboard.total_users, 20)
        self.assertEqual(dashboard.total_cost, 15.0)
        self.assertEqual(len(dashboard.top_bots), 1)
        self.assertEqual(len(dashboard.top_users), 1)
        self.assertEqual(len(dashboard.daily_usage), 1)
        
        # Test schema validation
        dashboard_dict = dashboard.model_dump()
        self.assertIn("total_bots", dashboard_dict)
        self.assertIn("total_users", dashboard_dict)
        self.assertIn("total_cost", dashboard_dict)
        self.assertIn("top_bots", dashboard_dict)
        self.assertIn("top_users", dashboard_dict)
        self.assertIn("daily_usage", dashboard_dict)
        
    def test_metadata_analytics_schema(self):
        """Test the MetadataAnalytics schema validation."""
        # Test valid initialization
        metadata_analytics = MetadataAnalytics(
            hierarchies={
                "school": {"count": "5", "names": ["School 1", "School 2"]}
            },
            usage_count=15
        )
        
        self.assertEqual(metadata_analytics.usage_count, 15)
        self.assertEqual(len(metadata_analytics.hierarchies), 1)
        self.assertEqual(metadata_analytics.hierarchies["school"]["count"], "5")
        
        # Test schema validation
        analytics_dict = metadata_analytics.model_dump()
        self.assertIn("hierarchies", analytics_dict)
        self.assertIn("usage_count", analytics_dict)
        
    def test_feedback_analytics_schema(self):
        """Test the FeedbackAnalytics schema validation."""
        # Test valid initialization
        feedback_analytics = FeedbackAnalytics(
            average_rating=4.5,
            total_feedback=20,
            categories={
                "helpful": {"count": 15, "average": 4.8},
                "not_helpful": {"count": 5, "average": 3.5}
            },
            sentiments={"positive": 15, "negative": 5},
            topics={"math": 10, "science": 10},
            tags=["helpful", "clear", "concise"]
        )
        
        self.assertEqual(feedback_analytics.average_rating, 4.5)
        self.assertEqual(feedback_analytics.total_feedback, 20)
        self.assertEqual(len(feedback_analytics.categories), 2)
        self.assertEqual(len(feedback_analytics.sentiments), 2)
        self.assertEqual(len(feedback_analytics.topics), 2)
        self.assertEqual(len(feedback_analytics.tags), 3)
        
        # Test schema validation
        analytics_dict = feedback_analytics.model_dump()
        self.assertIn("average_rating", analytics_dict)
        self.assertIn("total_feedback", analytics_dict)
        self.assertIn("categories", analytics_dict)
        self.assertIn("sentiments", analytics_dict)
        self.assertIn("topics", analytics_dict)
        self.assertIn("tags", analytics_dict)
        
    def test_token_analytics_schema(self):
        """Test the TokenAnalytics schema validation."""
        # Test valid initialization
        token_analytics = TokenAnalytics(
            total_input_tokens=10000,
            total_output_tokens=5000,
            total_cost=5.0,
            models={
                "claude-3": {
                    "input_tokens": 10000,
                    "output_tokens": 5000,
                    "cost": 5.0,
                    "cost_per_token": 0.0003
                }
            }
        )
        
        self.assertEqual(token_analytics.total_input_tokens, 10000)
        self.assertEqual(token_analytics.total_output_tokens, 5000)
        self.assertEqual(token_analytics.total_cost, 5.0)
        self.assertEqual(len(token_analytics.models), 1)
        self.assertEqual(token_analytics.models["claude-3"]["cost"], 5.0)
        
        # Test schema validation
        analytics_dict = token_analytics.model_dump()
        self.assertIn("total_input_tokens", analytics_dict)
        self.assertIn("total_output_tokens", analytics_dict)
        self.assertIn("total_cost", analytics_dict)
        self.assertIn("models", analytics_dict)


if __name__ == "__main__":
    unittest.main() 