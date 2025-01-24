import sys

sys.path.append(".")
import unittest

from app.agents.tools.bmi import bmi_tool


class TestBmiTool(unittest.TestCase):
    def test_bmi(self):
        result = bmi_tool.run(
            tool_use_id="dummy",
            input={
                "height": 170,
                "weight": 70,
            },
            model="claude-v3.5-sonnet-v2",
        )
        print(result)
        self.assertEqual(type(result), str)


if __name__ == "__main__":
    unittest.main()
