import sys
import unittest
from unittest.mock import patch, AsyncMock, MagicMock

sys.path.append(".")

# Import base test class
from tests.base_test import ImportTrackingTestCase, async_test

from app.repositories.usage_analysis import (
    _find_cognito_user_by_id,
    _find_cognito_users_by_ids,
    find_bots_sorted_by_price,
    find_users_sorted_by_price,
    run_athena_query,
    get_analytics_dashboard_fast,
    get_top_entities,
    get_topics_analysis,
    _count_total_bots,
    _count_total_users,
)

class TestUsageAnalysisEnhanced(ImportTrackingTestCase):
    """Enhanced test suite for the usage analysis repository."""
    
    @classmethod
    def _import_modules(cls):
        """Import modules needed for this test class."""
        import app.repositories.usage_analysis
        
    def setUp(self):
        """Set up test fixtures."""
        # Mock Athena client
        self.athena_patcher = patch("app.repositories.usage_analysis.athena")
        self.mock_athena = self.athena_patcher.start()
        self.addCleanup(self.athena_patcher.stop)
        
        # Mock boto3 client
        self.boto3_patcher = patch("app.repositories.usage_analysis.boto3")
        self.mock_boto3 = self.boto3_patcher.start()
        self.addCleanup(self.boto3_patcher.stop)
        
        # Sample query response
        self.sample_query_response = {
            "ResultSet": {
                "Rows": [
                    {
                        "Data": [
                            {"VarCharValue": "bot_id"}, 
                            {"VarCharValue": "title"}, 
                            {"VarCharValue": "num_sessions"}, 
                            {"VarCharValue": "num_messages"}, 
                            {"VarCharValue": "input_tokens"}, 
                            {"VarCharValue": "output_tokens"}, 
                            {"VarCharValue": "cost"}
                        ]
                    },
                    {
                        "Data": [
                            {"VarCharValue": "bot-1"}, 
                            {"VarCharValue": "Test Bot"}, 
                            {"VarCharValue": "50"}, 
                            {"VarCharValue": "250"}, 
                            {"VarCharValue": "5000"}, 
                            {"VarCharValue": "4000"}, 
                            {"VarCharValue": "2.5"}
                        ]
                    }
                ]
            }
        }
        
        # Setup mock for run_athena_query to use in tests
        self.run_query_patcher = patch(
            "app.repositories.usage_analysis.run_athena_query", 
            new_callable=AsyncMock
        )
        self.mock_run_query = self.run_query_patcher.start()
        self.addCleanup(self.run_query_patcher.stop)
        
    @async_test
    async def test_run_athena_query(self):
        """Test running an Athena query."""
        # Setup query execution mock
        self.mock_athena.start_query_execution.return_value = {
            "QueryExecutionId": "test-query-id"
        }
        
        # Setup query execution status mock sequence
        self.mock_athena.get_query_execution.side_effect = [
            {"QueryExecution": {"Status": {"State": "RUNNING"}}},
            {"QueryExecution": {"Status": {"State": "SUCCEEDED"}}}
        ]
        
        # Setup query results mock
        self.mock_athena.get_query_results.return_value = self.sample_query_response
        
        # Call the function with a test query
        test_query = "SELECT * FROM test_table"
        result = await run_athena_query(
            test_query, 
            "test_database", 
            "test_workgroup", 
            "s3://test-bucket"
        )
        
        # Assertions
        self.assertEqual(result, self.sample_query_response)
        
    @async_test
    async def test_get_analytics_dashboard_fast(self):
        """Test getting the analytics dashboard data."""
        # Setup mock return values
        self.mock_run_query.return_value = {
            "ResultSet": {
                "Rows": [
                    {
                        "Data": [
                            {"VarCharValue": "date"}, 
                            {"VarCharValue": "num_sessions"}, 
                            {"VarCharValue": "num_messages"}, 
                            {"VarCharValue": "input_tokens"}, 
                            {"VarCharValue": "output_tokens"}, 
                            {"VarCharValue": "cost"}
                        ]
                    },
                    {
                        "Data": [
                            {"VarCharValue": "2023-01-01"}, 
                            {"VarCharValue": "10"}, 
                            {"VarCharValue": "100"}, 
                            {"VarCharValue": "1000"}, 
                            {"VarCharValue": "800"}, 
                            {"VarCharValue": "1.5"}
                        ]
                    }
                ]
            }
        }
        
        # Mock count functions
        with patch(
            "app.repositories.usage_analysis._count_total_bots", 
            new_callable=AsyncMock, 
            return_value=5
        ) as mock_count_bots:
            with patch(
                "app.repositories.usage_analysis._count_total_users", 
                new_callable=AsyncMock, 
                return_value=20
            ) as mock_count_users:
                # Call the function
                result = await get_analytics_dashboard_fast(
                    from_="2024010100", 
                    to_="2024120100"
                )
                
                # Assertions
                self.assertIn("summary", result)
                self.assertIn("daily_usage", result)


    @async_test
    async def test_get_top_entities(self):
        """Test getting top entities."""
        # Setup mock return values for bots and users
        self.mock_run_query.side_effect = [
            self.sample_query_response,     # For bots
            {
                "ResultSet": {
                    "Rows": [
                        {
                            "Data": [
                                {"VarCharValue": "user_id"}, 
                                {"VarCharValue": "email"}, 
                                {"VarCharValue": "num_sessions"}, 
                                {"VarCharValue": "num_messages"}, 
                                {"VarCharValue": "cost"}
                            ]
                        },
                        {
                            "Data": [
                                {"VarCharValue": "user-1"}, 
                                {"VarCharValue": "test@example.com"}, 
                                {"VarCharValue": "40"}, 
                                {"VarCharValue": "200"}, 
                                {"VarCharValue": "2.0"}
                            ]
                        }
                    ]
                }
            }  # For users
        ]
        
        # Create mock for find_public_bots_by_ids
        with patch(
            "app.repositories.usage_analysis.find_public_bots_by_ids",
            new_callable=AsyncMock,
            return_value=[
                MagicMock(id="bot-1", title="Test Bot", description="A test bot")
            ]
        ) as mock_find_bots:
            # Call the function
            result = await get_top_entities(
                from_="2024010100", 
                to_="2024120100",
                limit=5
            )
            
            # Assertions
            self.assertIn("top_bots", result)
            self.assertIn("top_users", result)
            
            # Check bot data
            top_bots = result["top_bots"]
            self.assertEqual(len(top_bots), 1)
            
            # Check user data
            top_users = result["top_users"]
            self.assertEqual(len(top_users), 1)
            
    @async_test
    async def test_get_topics_analysis(self):
        """Test getting topics analysis."""
        # Setup mock return value
        self.mock_run_query.return_value = {
            "ResultSet": {
                "Rows": [
                    {
                        "Data": [
                            {"VarCharValue": "topic"}, 
                            {"VarCharValue": "message_count"}
                        ]
                    },
                    {
                        "Data": [
                            {"VarCharValue": "Feature Requests"}, 
                            {"VarCharValue": "150"}
                        ]
                    },
                    {
                        "Data": [
                            {"VarCharValue": "Bug Reports"}, 
                            {"VarCharValue": "120"}
                        ]
                    }
                ]
            }
        }
        
        # Call the function
        result = await get_topics_analysis(
            from_="2024010100", 
            to_="2024120100",
            limit=10
        )
        
        # Assertions
        self.assertIn("topics", result)
        self.assertIn("total_count", result)
