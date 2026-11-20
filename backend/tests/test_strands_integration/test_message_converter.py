import os
import sys

os.environ["BEDROCK_REGION"] = "us-east-1"
sys.path.append(".")

import unittest

from app.bedrock import simple_message_models_to_bedrock_messages
from app.repositories.models.conversation import SimpleMessageModel, TextContentModel
from app.strands_integration.converters.message_converter import (
    simple_message_models_to_strands_messages,
)


class TestMessageConverter(unittest.TestCase):
    def test_blank_assistant_turn_merges_surrounding_user_messages(self):
        history = [
            SimpleMessageModel(
                role=role, content=[TextContentModel(content_type="text", body=text)]
            )
            for role, text in [("user", "hello"), ("assistant", ""), ("user", "again")]
        ]
        for convert in (
            simple_message_models_to_bedrock_messages,
            simple_message_models_to_strands_messages,
        ):
            with self.subTest(converter=convert.__name__):
                self.assertEqual(
                    convert(history, "claude-v4-sonnet", prompt_caching_enabled=False),
                    [{"role": "user", "content": [{"text": "hello"}, {"text": "again"}]}],
                )


if __name__ == "__main__":
    unittest.main()
