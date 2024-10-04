import sys

sys.path.append(".")
import json
import unittest
from pprint import pprint

from app.agents.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field


class TestArg(BaseModel):
    arg1: str = Field(..., description="test string")
    arg2: float = Field(..., description="test float")
    arg3: int = Field(..., description="test int")
    arg4: list[str] = Field(..., description="test list")


def test_function(arg: TestArg) -> str:
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

    def test_to_converse_spec(self):

        spec = self.tool.to_converse_spec()
        pprint(spec)

        # Output must be a JSON schema
        # https://json-schema.org/
        expected_spec = {
            "name": "test",
            "description": "test",
            "inputSchema": {
                "json": {
                    "properties": {
                        "arg1": {
                            "title": "Arg1",
                            "type": "string",
                            "description": "test string",
                        },
                        "arg2": {
                            "title": "Arg2",
                            "type": "number",
                            "description": "test float",
                        },
                        "arg3": {
                            "title": "Arg3",
                            "type": "integer",
                            "description": "test int",
                        },
                        "arg4": {
                            "title": "Arg4",
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "test list",
                        },
                    },
                    "required": ["arg1", "arg2", "arg3", "arg4"],
                    "type": "object",
                    "title": "TestArg",
                }
            },
        }
        self.assertDictEqual(spec, expected_spec)

    def test_run(self):
        arg = TestArg(
            arg1="test",
            arg2=1.0,
            arg3=1,
            arg4=["test"],
        )
        result = self.tool.run(arg)
        self.assertEqual(result.body, "test")
        self.assertEqual(result.succeeded, True)


if __name__ == "__main__":
    unittest.main()
