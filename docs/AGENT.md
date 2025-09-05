# LLM-powered Agent (ReAct)

## What is the Agent (ReAct) ?

An Agent is an advanced AI system that utilizes large language models (LLMs) as its central computational engine. It combines the reasoning capabilities of LLMs with additional functionalities such as planning and tool usage to autonomously perform complex tasks. Agents can break down complicated queries, generate step-by-step solutions, and interact with external tools or APIs to gather information or execute subtasks.

This sample implements an Agent using the [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) approach. ReAct enables the agent to solve complex tasks by combining reasoning and actions in an iterative feedback loop. The agent repeatedly goes through three key steps: Thought, Action, and Observation. It analyzes the current situation using the LLM, decides on the next action to take, executes the action using available tools or APIs, and learns from the observed results. This continuous process allows the agent to adapt to dynamic environments, improve its task-solving accuracy, and provide context-aware solutions.

The implementation is powered by [Strands Agents](https://strandsagents.com/), an open-source SDK that takes a model-driven approach to building AI agents. Strands provides a lightweight, flexible framework for creating custom tools using Python decorators and supports multiple model providers including Amazon Bedrock.

## Example Use Case

An Agent using ReAct can be applied in various scenarios, providing accurate and efficient solutions.

### Text-to-SQL

A user asks for "the total sales for the last quarter." The Agent interprets this request, converts it into a SQL query, executes it against the database, and presents the results.

### Financial Forecasting

A financial analyst needs to forecast next quarter's revenue. The Agent gathers relevant data, performs necessary calculations using financial models, and generates a detailed forecast report, ensuring the accuracy of the projections.

## To use the Agent feature

To enable the Agent functionality for your customized chatbot, follow these steps:

There are two ways to use the Agent feature:

### Using Tool Use

To enable the Agent functionality with Tool Use for your customized chatbot, follow these steps:

1. Navigate to the Agent section in the custom bot screen.

2. In the Agent section, you will find a list of available tools that can be used by the Agent. By default, all tools are disabled.

3. To activate a tool, simply toggle the switch next to the desired tool. Once a tool is enabled, the Agent will have access to it and can utilize it when processing user queries.

![](./imgs/agent_tools.png)

4. For example, "Internet Search" tool allows the Agent to fetch information from the internet to answer user questions.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. You can develop and add your own custom tools to extend the capabilities of the Agent. Refer to the [How to develop your own tools](#how-to-develop-your-own-tools) section for more information on creating and integrating custom tools.

### Using Bedrock Agent

You can utilize a [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) created in Amazon Bedrock.

First, create an Agent in Bedrock (e.g., via the Management Console). Then, specify the Agent ID in the custom bot settings screen. Once set, your chatbot will leverage the Bedrock Agent to process user queries.

![](./imgs/bedrock_agent_tool.png)

## How to develop your own tools

To develop your own custom tools for the Agent using Strands SDK, follow these guidelines:

### About Strands Tools

Strands provides a simple `@tool` decorator that transforms regular Python functions into AI agent tools. The decorator automatically extracts information from your function's docstring and type hints to create tool specifications that the LLM can understand and use. This approach leverages Python's native features for a clean, functional tool development experience.

For detailed information about Strands tools, see the [Python Tools documentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Basic Tool Creation

Create a new function decorated with the `@tool` decorator from Strands:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Perform mathematical calculations safely.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Result in Strands format with toolUseId, status, and content
    """
    try:
        # Your calculation logic here
        result = eval(expression)  # Note: Use safe evaluation in production
        return {
            "toolUseId": "placeholder",
            "status": "success",
            "content": [{"text": str(result)}]
        }
    except Exception as e:
        return {
            "toolUseId": "placeholder",
            "status": "error",
            "content": [{"text": f"Error: {str(e)}"}]
        }
```

### Tools with Bot Context (Closure Pattern)

To access bot information (BotModel), use a closure pattern that captures the bot context:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Create calculator tool with bot context closure."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Perform mathematical calculations safely.

        Args:
            expression: Mathematical expression to evaluate (e.g., "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Result in Strands format with toolUseId, status, and content
        """
        # Access bot context within the tool
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # Use safe evaluation in production
            return {
                "toolUseId": "placeholder",
                "status": "success",
                "content": [{"text": str(result)}]
            }
        except Exception as e:
            return {
                "toolUseId": "placeholder",
                "status": "error",
                "content": [{"text": f"Error: {str(e)}"}]
            }

    return calculator
```

### Return Format Requirements

All Strands tools must return a dictionary with the following structure:

```python
{
    "toolUseId": "placeholder",  # Will be replaced by Strands
    "status": "success" | "error",
    "content": [
        {"text": "Simple text response"} |
        {"json": {"key": "Complex data object"}}
    ]
}
```

- Use `{"text": "message"}` for simple text responses
- Use `{"json": data}` for complex data that should be preserved as structured information
- Always set `status` to either `"success"` or `"error"`

### Implementation Guidelines

- The function name and docstring are used when the LLM considers which tool to use. The docstring is embedded in the prompt, so describe the tool's purpose and parameters precisely.

- Refer to the sample implementation of a [BMI calculation tool](../examples/agents/tools/bmi/bmi_strands.py). This example demonstrates how to create a tool that calculates the Body Mass Index (BMI) using the Strands `@tool` decorator and closure pattern.

- After completing development, place your implementation file in the [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/) directory. Then open [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) and edit `get_strands_registered_tools` to include your new tool.

- [Optional] Add clear names and descriptions for the frontend. This step is optional, but if you don't do this step, the tool name and description from your function will be used. Since these are for LLM consumption, it's recommended to add user-friendly explanations for better UX.

  - Edit i18n files. Open [en/index.ts](../frontend/src/i18n/en/index.ts) and add your own `name` and `description` on `agent.tools`.
  - Edit `xx/index.ts` as well. Where `xx` represents the country code you wish.

- Run `npx cdk deploy` to deploy your changes. This will make your custom tool available in the custom bot screen.
