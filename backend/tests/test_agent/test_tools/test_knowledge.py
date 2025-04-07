import sys

sys.path.append(".")
import unittest

from app.agents.tools.knowledge import KnowledgeToolInput, create_knowledge_tool
from app.repositories.models.custom_bot import (
    ActiveModelsModel,
    AgentModel,
    BotModel,
    GenerationParamsModel,
    KnowledgeModel,
    ReasoningParamsModel,
)


class TestKnowledgeTool(unittest.TestCase):
    def test_knowledge_tool(self):
        bot = BotModel(
            id="dummy",
            title="Japanese Dishes",
            description="Japanese Delicious Dishes",
            instruction="",
            create_time=1627984879.9,
            last_used_time=1627984879.9,
            # Pinned
            is_starred=True,
            owner_user_id="dummy",
            generation_params=GenerationParamsModel(
                max_tokens=2000,
                top_k=250,
                top_p=0.999,
                temperature=0.6,
                stop_sequences=["Human: ", "Assistant: "],
                reasoning_params=ReasoningParamsModel(
                    budget_tokens=2000,
                ),
            ),
            agent=AgentModel(tools=[]),
            knowledge=KnowledgeModel(
                source_urls=[""],
                sitemap_urls=[""],
                filenames=[
                    "Ramen.pdf",
                    "Sushi.pdf",
                    "Yakiniku.pdf",
                ],
                s3_urls=[],
            ),
            display_retrieved_chunks=True,
            sync_status="RUNNING",
            sync_status_reason="reason",
            sync_last_exec_id="",
            published_api_stack_name=None,
            published_api_datetime=None,
            published_api_codebuild_id=None,
            conversation_quick_starters=[],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
            active_models=ActiveModelsModel(),
            shared_scope="private",
            shared_status="private",
            allowed_cognito_groups=[],
            allowed_cognito_users=[],
            usage_stats=None,
        )
        arg = KnowledgeToolInput(query="What are delicious Japanese dishes?")
        tool = create_knowledge_tool(bot=bot)
        response = tool.run(
            tool_use_id="dummy",
            input=arg.model_dump(),
            model="claude-v3.5-sonnet-v2",
        )
        self.assertIsInstance(response["related_documents"], list)
        self.assertEqual(response["status"], "success")
        print(response)


if __name__ == "__main__":
    unittest.main()
