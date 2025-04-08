import sys
import unittest
from unittest.mock import MagicMock, patch

from app.repositories.usage_analysis import (
    get_metadata_analytics,
    get_feedback_analytics,
    get_token_analytics,
    get_bot_analytics,
    get_analytics_dashboard
)


class TestEnhancedUsageAnalytics(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Setup mocks
        self.mock_athena = MagicMock()
        self.athena_patcher = patch('app.repositories.usage_analysis.athena', self.mock_athena)
        self.mock_athena_client = self.athena_patcher.start()
        
        # Mock the boto3 client for DynamoDB
        self.mock_dynamodb = MagicMock()
        self.dynamodb_patcher = patch('app.repositories.custom_bot.boto3.resource', return_value=self.mock_dynamodb)
        self.mock_dynamodb_resource = self.dynamodb_patcher.start()
        
        # Mock the table
        self.mock_table = MagicMock()
        self.mock_dynamodb.Table.return_value = self.mock_table
        
        # Mock find_public_bot_by_id
        self.bot_patcher = patch('app.repositories.usage_analysis.find_public_bot_by_id')
        self.mock_find_bot = self.bot_patcher.start()
        self.mock_find_bot.return_value = {
            'id': 'test-bot',
            'title': 'Test Bot',
            'description': 'A test bot'
        }
        
    def tearDown(self):
        self.athena_patcher.stop()
        self.dynamodb_patcher.stop()
        self.bot_patcher.stop()
        
    def _setup_athena_mock_response(self, rows):
        """Helper to set up mock Athena responses"""
        self.mock_athena.start_query_execution.return_value = {'QueryExecutionId': 'test-query-id'}
        self.mock_athena.get_query_execution.return_value = {
            'QueryExecution': {
                'Status': {'State': 'SUCCEEDED'}
            }
        }
        self.mock_athena.get_query_results.return_value = {
            'ResultSet': {
                'Rows': rows
            }
        }
    
    async def test_get_metadata_analytics(self):
        # Arrange
        self._setup_athena_mock_response([
            {'Data': [{'VarCharValue': 'metadata_type'}, {'VarCharValue': 'metadata_key'}, {'VarCharValue': 'count'}]},
            {'Data': [{'VarCharValue': 'hierarchy'}, {'VarCharValue': 'school'}, {'VarCharValue': '5'}]},
            {'Data': [{'VarCharValue': 'tag'}, {'VarCharValue': 'subject'}, {'VarCharValue': '10'}]}
        ])
        
        # Patch the run_athena_query function to return mock data
        with patch('app.repositories.usage_analysis.run_athena_query') as mock_run_query:
            mock_run_query.return_value = [
                {'metadata_type': 'hierarchy', 'metadata_key': 'school', 'count': 5},
                {'metadata_type': 'tag', 'metadata_key': 'subject', 'count': 10}
            ]
            
            # Act
            result = await get_metadata_analytics(bot_id=None)
            
            # Assert
            self.assertIn('hierarchy', result)
            self.assertIn('tags', result)
            self.assertEqual(result['hierarchy'].get('school', 0), 5)
            self.assertEqual(result['tags'].get('subject', 0), 10)
        
    async def test_get_metadata_analytics_with_bot_id(self):
        # Arrange
        self._setup_athena_mock_response([
            {'Data': [{'VarCharValue': 'metadata_type'}, {'VarCharValue': 'metadata_key'}, {'VarCharValue': 'count'}]},
            {'Data': [{'VarCharValue': 'hierarchy'}, {'VarCharValue': 'school'}, {'VarCharValue': '1'}]}
        ])
        
        # Patch the run_athena_query function to return mock data
        with patch('app.repositories.usage_analysis.run_athena_query') as mock_run_query:
            mock_run_query.return_value = [
                {'metadata_type': 'hierarchy', 'metadata_key': 'school', 'count': 1}
            ]
            
            # Act
            result = await get_metadata_analytics(bot_id='test-bot')
            
            # Assert
            self.assertIn('hierarchy', result)
            self.assertEqual(result['hierarchy'].get('school', 0), 1)
        
    async def test_get_feedback_analytics(self):
        # Arrange
        self._setup_athena_mock_response([
            {'Data': [{'VarCharValue': 'metric'}, {'VarCharValue': 'value'}]},
            {'Data': [{'VarCharValue': 'average_rating'}, {'VarCharValue': '4.5'}]},
            {'Data': [{'VarCharValue': 'total_feedback'}, {'VarCharValue': '20'}]},
            {'Data': [{'VarCharValue': 'category_distribution'}, {'VarCharValue': '{"helpful": 15, "not_helpful": 5}'}]}
        ])
        
        # Patch the run_athena_query function to return mock data
        with patch('app.repositories.usage_analysis.run_athena_query') as mock_run_query:
            mock_run_query.return_value = [
                {'metric': 'average_rating', 'value': '4.5'},
                {'metric': 'total_feedback', 'value': '20'},
                {'metric': 'category_distribution', 'value': '{"helpful": 15, "not_helpful": 5}'}
            ]
            
            # Act
            result = await get_feedback_analytics()
            
            # Assert
            self.assertIn('average_rating', result)
            self.assertIn('total_feedback', result)
            self.assertIn('categories', result)
            self.assertEqual(result['average_rating'], 4.5)
            self.assertEqual(result['total_feedback'], 20)
            self.assertEqual(result['categories']['helpful'], 15)
        
    async def test_get_token_analytics(self):
        # Arrange
        self._setup_athena_mock_response([
            {'Data': [{'VarCharValue': 'metric'}, {'VarCharValue': 'value'}]},
            {'Data': [{'VarCharValue': 'total_input_tokens'}, {'VarCharValue': '1000'}]},
            {'Data': [{'VarCharValue': 'total_output_tokens'}, {'VarCharValue': '500'}]},
            {'Data': [{'VarCharValue': 'total_cost'}, {'VarCharValue': '0.12'}]},
            {'Data': [{'VarCharValue': 'models'}, {'VarCharValue': '{"claude-3": {"input_tokens": 1000, "output_tokens": 500, "cost": 0.12}}'}]}
        ])
        
        # Patch the run_athena_query function to return mock data
        with patch('app.repositories.usage_analysis.run_athena_query') as mock_run_query:
            mock_run_query.return_value = [
                {'metric': 'total_input_tokens', 'value': '1000'},
                {'metric': 'total_output_tokens', 'value': '500'},
                {'metric': 'total_cost', 'value': '0.12'},
                {'metric': 'models', 'value': '{"claude-3": {"input_tokens": 1000, "output_tokens": 500, "cost": 0.12}}'}
            ]
            
            # Act
            result = await get_token_analytics()
            
            # Assert
            self.assertIn('total_input_tokens', result)
            self.assertIn('total_output_tokens', result)
            self.assertIn('total_cost', result)
            self.assertIn('models', result)
            self.assertEqual(result['total_input_tokens'], 1000)
            self.assertEqual(result['total_output_tokens'], 500)
            self.assertEqual(result['total_cost'], 0.12)
            self.assertEqual(result['models']['claude-3']['input_tokens'], 1000)
        
    async def test_get_bot_analytics(self):
        # Arrange
        bot_id = 'test-bot'
        self._setup_athena_mock_response([
            {'Data': [{'VarCharValue': 'metric'}, {'VarCharValue': 'value'}]},
            {'Data': [{'VarCharValue': 'total_users'}, {'VarCharValue': '10'}]},
            {'Data': [{'VarCharValue': 'total_sessions'}, {'VarCharValue': '100'}]},
            {'Data': [{'VarCharValue': 'total_messages'}, {'VarCharValue': '500'}]},
            {'Data': [{'VarCharValue': 'total_cost'}, {'VarCharValue': '1.25'}]},
            {'Data': [{'VarCharValue': 'daily_usage'}, {'VarCharValue': '[{"date": "2025-03-01", "num_sessions": 5, "num_messages": 25}]'}]}
        ])
        
        # Patch the run_athena_query function to return mock data
        with patch('app.repositories.usage_analysis.run_athena_query') as mock_run_query:
            mock_run_query.return_value = [
                {'metric': 'total_users', 'value': '10'},
                {'metric': 'total_sessions', 'value': '100'},
                {'metric': 'total_messages', 'value': '500'},
                {'metric': 'total_cost', 'value': '1.25'},
                {'metric': 'daily_usage', 'value': '[{"date": "2025-03-01", "num_sessions": 5, "num_messages": 25}]'}
            ]
            
            # Act
            result = await get_bot_analytics(bot_id=bot_id)
            
            # Assert
            self.assertEqual(result.bot_id, bot_id)
            self.assertEqual(result.total_users, 10)
            self.assertEqual(result.total_sessions, 100)
            self.assertEqual(result.total_messages, 500)
            self.assertEqual(result.total_cost, 1.25)
            self.assertEqual(len(result.daily_usage), 1)
        
    async def test_get_analytics_dashboard(self):
        # Arrange
        self._setup_athena_mock_response([
            {'Data': [{'VarCharValue': 'metric'}, {'VarCharValue': 'value'}]},
            {'Data': [{'VarCharValue': 'total_bots'}, {'VarCharValue': '5'}]},
            {'Data': [{'VarCharValue': 'total_users'}, {'VarCharValue': '50'}]},
            {'Data': [{'VarCharValue': 'total_sessions'}, {'VarCharValue': '500'}]},
            {'Data': [{'VarCharValue': 'total_cost'}, {'VarCharValue': '10.0'}]},
            {'Data': [{'VarCharValue': 'top_bots'}, {'VarCharValue': '[{"id": "bot-1", "title": "Math Bot", "total_price": 5.0}]'}]},
            {'Data': [{'VarCharValue': 'top_users'}, {'VarCharValue': '[{"id": "user-1", "email": "test@example.com", "total_price": 3.0}]'}]}
        ])
        
        # Patch the run_athena_query function to return mock data
        with patch('app.repositories.usage_analysis.run_athena_query') as mock_run_query:
            mock_run_query.return_value = [
                {'metric': 'total_bots', 'value': '5'},
                {'metric': 'total_users', 'value': '50'},
                {'metric': 'total_sessions', 'value': '500'},
                {'metric': 'total_cost', 'value': '10.0'},
                {'metric': 'top_bots', 'value': '[{"id": "bot-1", "title": "Math Bot", "total_price": 5.0}]'},
                {'metric': 'top_users', 'value': '[{"id": "user-1", "email": "test@example.com", "total_price": 3.0}]'}
            ]
            
            # Act
            result = await get_analytics_dashboard()
            
            # Assert
            self.assertEqual(result.total_bots, 5)
            self.assertEqual(result.total_users, 50)
            self.assertEqual(result.total_sessions, 500)
            self.assertEqual(result.total_cost, 10.0)
            self.assertEqual(len(result.top_bots), 1)
            self.assertEqual(len(result.top_users), 1)
            self.assertEqual(result.top_bots[0].id, "bot-1")
            self.assertEqual(result.top_users[0].id, "user-1")


if __name__ == "__main__":
    unittest.main() 