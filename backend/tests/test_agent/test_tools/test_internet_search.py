import sys

sys.path.append(".")
import unittest

from app.agents.tools.internet_search import InternetSearchInput, internet_search_tool


class TestInternetSearchTool(unittest.TestCase):
    def test_internet_search(self):
        # query = "Amazon Stock Price Today"
        query = "東京 焼肉"
        time_limit = "d"
        country = "jp-jp"
        arg = InternetSearchInput(query=query, time_limit=time_limit, country=country)
        response = internet_search_tool.run(
            tool_use_id="dummy",
            input=arg.model_dump(),
            model="claude-v3.5-sonnet-v2",
        )
        self.assertIsInstance(response["related_documents"], list)
        self.assertEqual(response["status"], "success")
        print(response)


if __name__ == "__main__":
    unittest.main()
