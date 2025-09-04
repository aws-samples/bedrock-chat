# BMI calculation tool

## Overview

The BMI (Body Mass Index) calculation tool is a custom tool designed to compute the BMI of an individual based on their height and weight. This tool helps users quickly determine their BMI and understand which weight category they fall into, such as underweight, normal weight, overweight, or obese.

## How to enable this tool

- Move `bmi_strands.py` under `backend/app/strands_integration/tools/` directory.
- Open `backend/app/strands_integration/utils.py` and modify `get_strands_registered_tools` function:

```py
def get_strands_registered_tools(bot: BotModel | None = None) -> list[StrandsAgentTool]:
    """Get list of available Strands tools."""
    from app.strands_integration.tools.bedrock_agent import create_bedrock_agent_tool
    from app.strands_integration.tools.calculator import create_calculator_tool
    from app.strands_integration.tools.internet_search import (
        create_internet_search_tool,
    )
    from app.strands_integration.tools.simple_list import simple_list, structured_list
+   from app.strands_integration.tools.bmi_strands import create_bmi_tool

    tools: list[StrandsAgentTool] = []
    tools.append(create_internet_search_tool(bot))
    tools.append(create_bedrock_agent_tool(bot))
+   tools.append(create_bmi_tool(bot))
    return tools
```

- Run `npx cdk deploy`.
