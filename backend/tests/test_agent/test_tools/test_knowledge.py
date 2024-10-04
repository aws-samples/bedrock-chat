import sys

sys.path.append(".")
import unittest

from app.agents.tools.knowledge import KnowledgeToolInput, create_knowledge_tool
from app.config import DEFAULT_EMBEDDING_CONFIG
from app.repositories.models.custom_bot import (
    AgentModel,
    BotModel,
    EmbeddingParamsModel,
    GenerationParamsModel,
    KnowledgeModel,
    SearchParamsModel,
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
            is_pinned=True,
            public_bot_id=None,
            owner_user_id="dummy",
            embedding_params=EmbeddingParamsModel(
                chunk_size=DEFAULT_EMBEDDING_CONFIG["chunk_size"],
                chunk_overlap=DEFAULT_EMBEDDING_CONFIG["chunk_overlap"],
                enable_partition_pdf=False,
            ),
            generation_params=GenerationParamsModel(
                max_tokens=2000,
                top_k=250,
                top_p=0.999,
                temperature=0.6,
                stop_sequences=["Human: ", "Assistant: "],
            ),
            search_params=SearchParamsModel(
                max_results=20,
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
        )
        tool = create_knowledge_tool(bot, model="claude-v3-sonnet")
        response = tool.run(
            KnowledgeToolInput(query="What are delicious Japanese dishes?")
        )
        self.assertIsInstance(response.body, str)
        self.assertTrue(response.succeeded)
        print(response)


if __name__ == "__main__":
    unittest.main()
