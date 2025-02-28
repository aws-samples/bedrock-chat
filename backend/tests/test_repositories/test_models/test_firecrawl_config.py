import json
import sys
import unittest

sys.path.insert(0, ".")
from uuid import uuid4

import boto3
from app.repositories.models.custom_bot import FirecrawlConfigModel
from app.routes.schemas.bot import FirecrawlConfig

API_KEY = "test-api-key"


class TestFirecrawlConfigModel(unittest.TestCase):
    def tearDown(self) -> None:
        # Delete the secret after each test
        client = boto3.client("secretsmanager")
        client.delete_secret(SecretId=self.secret_arn)

    def test_lifecycle(self):
        # Create the model from input
        bot_id = str(uuid4())
        input_config = FirecrawlConfig(api_key=API_KEY, max_results=15)
        model = FirecrawlConfigModel.from_firecrawl_config(
            input_config, "user123", bot_id
        )

        # Secret ARN should not be empty
        self.assertNotEqual(model.secret_arn, "")
        self.secret_arn = model.secret_arn
        self.assertEqual(model.api_key, API_KEY)
        self.assertEqual(model.max_results, 15)

        serialized = model.model_dump()
        # API key should be empty
        self.assertEqual(serialized["api_key"], "")
        deserialized = FirecrawlConfigModel.model_validate(serialized)

        # API key should be loaded from Secrets Manager
        self.assertEqual(deserialized.api_key, API_KEY)
        self.assertEqual(deserialized.secret_arn, model.secret_arn)
        self.assertEqual(deserialized.max_results, 15)


if __name__ == "__main__":
    unittest.main()
