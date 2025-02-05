import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(".")

from app.agents.tools.internet_search import (
    InternetSearchInput, 
    internet_search_tool,
    search_bing,
    search_duckduckgo
)


class TestInternetSearchTool(unittest.TestCase):
    def setUp(self):
        os.environ['BING_API_SECRET_ARN'] = 'dummy-arn'
        self.query = "Best restaurants in San Diego"
        self.time_limit = "d"
        self.country = "us-en"
        self.input_args = InternetSearchInput(
            query=self.query,
            time_limit=self.time_limit,
            country=self.country
        )
        # Mock DuckDuckGo API
        self.ddg_results = [{"body": "test", "title": "test", "href": "test"}]

    @patch('app.agents.tools.internet_search.DDGS')
    def test_duckduckgo_search(self, mock_ddgs):
        # Mock the DDGS instance
        mock_instance = MagicMock()
        mock_ddgs.return_value.__enter__.return_value = mock_instance
        mock_instance.text.return_value = [{"body": "test", "title": "test", "href": "test"}]
        
        response = internet_search_tool.run(
            tool_use_id="dummy",
            input=self.input_args.model_dump(),
            model="claude-v3.5-sonnet-v2",
        )
        
        self.assertIsInstance(response["related_documents"], list)
        self.assertEqual(response["status"], "success")

    @patch('app.agents.tools.internet_search.get_bing_api_key')
    def test_bing_search_fallback(self, mock_get_key):
        mock_get_key.return_value = "dummy_api_key"
        
        with patch('app.agents.tools.internet_search.search_duckduckgo') as mock_ddg:
            mock_ddg.side_effect = Exception("DuckDuckGo failed")
            
            with patch('app.agents.tools.internet_search.search_bing') as mock_bing:
                mock_bing.return_value = [{"content": "test", "source_name": "test", "source_link": "test"}]
                
                response = internet_search_tool.run(
                    tool_use_id="dummy",
                    input=self.input_args.model_dump(),
                    model="claude-v3.5-sonnet-v2",
                )
                
                self.assertTrue(mock_bing.called)
                self.assertIsInstance(response["related_documents"], list)
                self.assertEqual(response["status"], "success")


if __name__ == "__main__":
    unittest.main()
