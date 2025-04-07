import sys

sys.path.append(".")
import unittest
from pprint import pprint

from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.conversation import (
    RelatedDocumentModel,
    TextToolResultModel,
)
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, Field


class TestArg(BaseModel):
    arg1: str = Field(..., description="test string")
    arg2: float = Field(..., description="test float")
    arg3: int = Field(..., description="test int")
    arg4: list[str] = Field(..., description="test list")


def test_function(
    arg: TestArg,
    bot: BotModel | None,
    model: type_model_name | None,
) -> str:
    print(arg)
    return "test"


class TestAgentTool(unittest.TestCase):
    def setUp(self) -> None:
        self.tool = AgentTool(
            name="test",
            description="test",
            args_schema=TestArg,
            function=test_function,
        )

    def test_run(self):
        arg = TestArg(
            arg1="test",
            arg2=1.0,
            arg3=1,
            arg4=["test"],
        )
        result = self.tool.run(
            tool_use_id="dummy",
            input=arg.model_dump(),
            model="claude-v3.5-sonnet-v2",
        )
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main()
