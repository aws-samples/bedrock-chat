import logging
from typing import List, Optional, ClassVar
from pydantic import BaseModel, Field
from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from app.vector_search import search_related_docs

logger = logging.getLogger(__name__)

class SimpleQuizInput(BaseModel):
    """Simple quiz generation parameters"""
    topic: str = Field(
        description="Topic or subject area to create quiz about"
    )
    num_questions: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of questions to generate (1-10)"
    )
    # Add documents field for specific source documents
    documents: Optional[List[str]] = Field(
        default=None,
        description="List of source document names to search in knowledge base"
    )

class SimpleQuizTool(AgentTool):
    """Quiz generation tool with class-level description"""
    DESCRIPTION: ClassVar[str] = (
        "Generate a multiple choice quiz based on information in the knowledge base. "
        "Specify a topic and number of questions (default 5)."
    )
    
    @classmethod
    def get_description(cls) -> str:
        """Get tool description for schema generation"""
        return cls.DESCRIPTION

    def __init__(self, bot: BotModel, model: type_model_name):
        super().__init__(
            name="quiz_generator",
            description=self.DESCRIPTION,
            args_schema=SimpleQuizInput,
            function=self.generate_quiz,
            bot=bot,
            model=model
        )
    
    def _build_search_query(
        self,
        tool_input: SimpleQuizInput
    ) -> str:
        """
        Build context-appropriate search query for knowledge base search
        """
        # Base components for search query
        topic_term = tool_input.topic

        query = (
            f"Find detailed information about {topic_term}"
        )

        # Add any documents if specified
        if hasattr(tool_input, 'documents') and tool_input.documents:
            documents_list = " ".join(tool_input.documents)
            query += f" sources: {documents_list}"

        logger.info(f"Built search query: {query}")
        return query

    def generate_quiz(
        self,
        tool_input: SimpleQuizInput,
        bot: BotModel | None,
        model: type_model_name | None
    ) -> list:
        """Generate quiz based on knowledge base content"""
        if bot is None:
            raise ValueError("Bot instance required for quiz generation")

        logger.info(f"Generating quiz about: {tool_input.topic}")

        try:
            # Search knowledge base for relevant content
            search_results = search_related_docs(
                bot=bot,
                query=self._build_search_query(tool_input)
            )

            if not search_results:
                return [{
                    "content": f"No information found about {tool_input.topic} in the knowledge base.",
                    "source_name": "Quiz Generator"
                }]

            # Create quiz generation prompt
            content_text = "\n\n".join(result["content"] for result in search_results)
            sources = [f"- {result['source_name']}" for result in search_results]
            
            quiz_prompt = f"""You are a quiz generation assistant. Your task is to create {tool_input.num_questions} high-quality multiple-choice questions about {tool_input.topic} using the provided content.

CONTENT TO USE:
{content_text}

REFERENCE MATERIALS:
{chr(10).join(sources)}

VALIDATION REQUIREMENTS:
1. Every question must be based on specific content from the provided materials
2. All correct answers must be directly verifiable from the source content
3. Keep track of content coverage to avoid duplicates
4. Each question must include a citation to the source material

FORMAT EACH QUESTION AS FOLLOWS:
Question [X of {tool_input.num_questions}]
Source: [source document name]
Retrieved Content: [brief relevant quote from source]

[Question text]
Options:
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

Correct Answer: [Letter]
Explanation: [Explanation referencing the source content]
Validation: [Brief statement confirming answer can be verified in source]

---

Begin quiz generation:"""

            # Return the quiz prompt as content to be processed by the bot
            return [{
                "content": quiz_prompt,
                "source_name": "Quiz Generator",
                "metadata": {
                    "topic": tool_input.topic,
                    "num_questions": tool_input.num_questions,
                    "sources": sources
                }
            }]

        except Exception as e:
            logger.error(f"Failed to generate quiz: {e}")
            return [{
                "content": f"Error generating quiz: {str(e)}",
                "source_name": "Quiz Generator"
            }]

def create_simple_quiz_tool(bot: BotModel, model: type_model_name) -> AgentTool:
    """Create a quiz tool instance for the given bot."""
    return SimpleQuizTool(bot, model)