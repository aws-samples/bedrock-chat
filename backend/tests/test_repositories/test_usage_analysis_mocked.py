import sys
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import date, datetime, timedelta

sys.path.append(".")

from app.repositories.usage_analysis import (
    run_athena_query,
    get_analytics_dashboard_fast,
    get_topics_analysis,
    _count_total_bots,
)

class TestUsageAnalysisMocked(unittest.IsolatedAsyncioTestCase):
    """Test suite for usage analysis with mocked AWS services."""
    
    async def test_run_athena_query(self):
        """Test the core run_athena_query function."""
        # Mock response data
        mock_response = {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "col1"}, {"VarCharValue": "col2"}]},
                    {"Data": [{"VarCharValue": "val1"}, {"VarCharValue": "val2"}]}
                ]
            }
        }

        # Mock the boto3 client
        with patch("app.repositories.usage_analysis.athena") as mock_athena:
            # Set up query execution mock
            mock_athena.start_query_execution.return_value = {
                "QueryExecutionId": "test-query-id"
            }
            
            # Set up query execution status mock sequence
            mock_athena.get_query_execution.side_effect = [
                {"QueryExecution": {"Status": {"State": "RUNNING"}}},
                {"QueryExecution": {"Status": {"State": "SUCCEEDED"}}}
            ]
            
            # Set up query results mock
            mock_athena.get_query_results.return_value = mock_response
            
            # Call the function with a test query and required parameters
            result = await run_athena_query(
                "SELECT * FROM test_table",
                database="test_database",
                workgroup="test_workgroup",
                output_location="s3://test-bucket/test-output/"
            )
            
            # Verify AWS API calls
            mock_athena.start_query_execution.assert_called_once()
            self.assertEqual(mock_athena.get_query_execution.call_count, 2)
            mock_athena.get_query_results.assert_called_once()
            
            # Assertions
            self.assertEqual(result, mock_response)

    async def test_get_analytics_dashboard_fast(self):
        """Test getting the analytics dashboard fast endpoint."""
        # Set up mock for run_athena_query
        with patch("app.repositories.usage_analysis.run_athena_query", new_callable=AsyncMock) as mock_run_query:
            # Set up mock response
            mock_run_query.return_value = {
                "ResultSet": {
                    "Rows": [
                        {"Data": [{"VarCharValue": "date"}, {"VarCharValue": "num_sessions"}, {"VarCharValue": "num_messages"}, {"VarCharValue": "input_tokens"}, {"VarCharValue": "output_tokens"}, {"VarCharValue": "cost"}]},
                        {"Data": [{"VarCharValue": "2023-01-01"}, {"VarCharValue": "10"}, {"VarCharValue": "100"}, {"VarCharValue": "1000"}, {"VarCharValue": "800"}, {"VarCharValue": "1.5"}]}
                    ]
                }
            }
            
            # Set up mocks for count functions
            with patch("app.repositories.usage_analysis._count_total_bots", new_callable=AsyncMock, return_value=5) as mock_count_bots:
                with patch("app.repositories.usage_analysis._count_total_users", new_callable=AsyncMock, return_value=20) as mock_count_users:
                    # Call the function with proper date format
                    result = await get_analytics_dashboard_fast(from_="2024-01-01", to_="2024-12-01")
                    
                    # Verify mocks were called
                    mock_count_bots.assert_called_once()
                    mock_count_users.assert_called_once()
                    mock_run_query.assert_called_once()
                    
                    # Verify results
                    self.assertIn("summary", result)
                    self.assertIn("daily_usage", result)
                    self.assertEqual(result["summary"]["total_bots"], 5)
                    self.assertEqual(result["summary"]["total_users"], 20)
                    self.assertEqual(len(result["daily_usage"]), 1)
    
    async def test_count_total_bots(self):
        """Test counting total bots."""
        # Set up mock for run_athena_query
        with patch("app.repositories.usage_analysis.run_athena_query", new_callable=AsyncMock) as mock_run_query:
            # Set up mock response
            mock_run_query.return_value = {
                "ResultSet": {
                    "Rows": [
                        {"Data": [{"VarCharValue": "count"}]},
                        {"Data": [{"VarCharValue": "5"}]}
                    ]
                }
            }
            
            # Call the function
            result = await _count_total_bots()
            
            # Verify results
            self.assertEqual(result, 5)
    
    async def test_get_topics_analysis(self):
        """Test getting topics analysis."""
        # Set up mock for run_athena_query
        with patch("app.repositories.usage_analysis.run_athena_query", new_callable=AsyncMock) as mock_run_query:
            # Set up mock response
            mock_run_query.return_value = {
                "ResultSet": {
                    "Rows": [
                        {"Data": [{"VarCharValue": "topic"}, {"VarCharValue": "message_count"}]},
                        {"Data": [{"VarCharValue": "Feature Requests"}, {"VarCharValue": "150"}]},
                        {"Data": [{"VarCharValue": "Bug Reports"}, {"VarCharValue": "120"}]}
                    ]
                }
            }
            
            # Call the function with proper date format
            result = await get_topics_analysis(from_="2024-01-01", to_="2024-12-01", limit=10)
            
            # Verify results
            self.assertIn("topics", result)
            self.assertIn("total_count", result)
            self.assertEqual(len(result["topics"]), 2)
            self.assertEqual(result["total_count"], 270)
            self.assertEqual(result["topics"][0]["topic"], "Feature Requests")
            self.assertEqual(result["topics"][0]["message_count"], 150)

if __name__ == "__main__":
    unittest.main()
