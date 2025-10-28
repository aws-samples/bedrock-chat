# LLM驱动的智能代理(ReAct)

## 什么是智能代理（ReAct）？

智能代理是一个以大语言模型（LLMs）为核心计算引擎的高级 AI 系统。它将 LLMs 的推理能力与规划和工具使用等附加功能相结合，可以自主执行复杂任务。智能代理能够分解复杂查询、生成逐步解决方案，并与外部工具或 API 交互以收集信息或执行子任务。

本示例使用 [ReAct（推理 + 行动）](https://www.promptingguide.ai/techniques/react)方法实现了一个智能代理。ReAct 通过将推理和行动结合在一个迭代反馈循环中，使代理能够解决复杂任务。代理反复经历三个关键步骤：思考、行动和观察。它使用 LLM 分析当前情况，决定下一步要采取的行动，使用可用的工具或 API 执行行动，并从观察到的结果中学习。这个持续的过程使代理能够适应动态环境、提高任务解决的准确性，并提供符合上下文的解决方案。

该实现由 [Strands Agents](https://strandsagents.com/) 提供支持，这是一个采用模型驱动方法构建 AI 代理的开源 SDK。Strands 提供了一个轻量级、灵活的框架，可以使用 Python 装饰器创建自定义工具，并支持包括 Amazon Bedrock 在内的多个模型提供商。

## 示例用例

使用 ReAct 的 Agent 可以应用于各种场景，提供准确高效的解决方案。

### 文本转 SQL

用户询问"上季度的总销售额"。Agent 会解析这个请求，将其转换为 SQL 查询，在数据库中执行查询，并展示结果。

### 财务预测

财务分析师需要预测下个季度的收入。Agent 会收集相关数据，使用财务模型进行必要的计算，并生成详细的预测报告，确保预测的准确性。

## 使用 Agent 功能

要为您的自定义聊天机器人启用 Agent 功能，请按照以下步骤操作：

有两种使用 Agent 功能的方式：

### 使用工具

要为您的自定义聊天机器人启用带有工具使用功能的 Agent，请按照以下步骤操作：

1. 在自定义机器人界面中导航到 Agent 部分。

2. 在 Agent 部分，您会看到可供 Agent 使用的工具列表。默认情况下，所有工具都是禁用的。

3. 要激活某个工具，只需切换该工具旁边的开关即可。一旦工具被启用，Agent 就可以访问它并在处理用户查询时使用它。

![](./imgs/agent_tools.png)

4. 例如，"互联网搜索"工具允许 Agent 从互联网获取信息来回答用户问题。

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. 您可以开发并添加自己的自定义工具来扩展 Agent 的功能。有关创建和集成自定义工具的更多信息，请参阅[如何开发自己的工具](#how-to-develop-your-own-tools)部分。

### 使用 Bedrock Agent

您可以使用在 Amazon Bedrock 中创建的 [Bedrock Agent](https://aws.amazon.com/bedrock/agents/)。

首先，在 Bedrock 中创建一个 Agent（例如，通过管理控制台）。然后，在自定义机器人设置界面中指定 Agent ID。设置完成后，您的聊天机器人将利用 Bedrock Agent 来处理用户查询。

![](./imgs/bedrock_agent_tool.png)

## 如何开发您自己的工具

要使用 Strands SDK 为 Agent 开发自定义工具，请遵循以下指南：

### 关于 Strands 工具

Strands 提供了一个简单的 `@tool` 装饰器，可以将普通的 Python 函数转换为 AI agent 工具。该装饰器会自动从函数的文档字符串和类型提示中提取信息，创建 LLM 可以理解和使用的工具规范。这种方法利用 Python 的原生特性，提供了一个清晰、实用的工具开发体验。

有关 Strands 工具的详细信息，请参阅 [Python Tools 文档](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/)。

### 基本工具创建

创建一个使用 Strands 的 `@tool` 装饰器的新函数：

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

### 带有机器人上下文的工具（闭包模式）

要访问机器人信息(BotModel)，使用捕获机器人上下文的闭包模式：

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

### 返回格式要求

所有 Strands 工具必须返回具有以下结构的字典：

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

- 使用 `{"text": "message"}` 作为简单文本响应
- 使用 `{"json": data}` 作为需要保持结构化信息的复杂数据
- 始终将 `status` 设置为 `"success"` 或 `"error"`

### 实现指南

- 函数名称和文档字符串在 LLM 考虑使用哪个工具时会被使用。文档字符串会被嵌入到提示中，因此请准确描述工具的用途和参数。

- 参考 [BMI 计算工具](../examples/agents/tools/bmi/bmi_strands.py) 的示例实现。这个例子展示了如何使用 Strands `@tool` 装饰器和闭包模式创建一个计算体重指数(BMI)的工具。

- 完成开发后，将实现文件放在 [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/) 目录中。然后打开 [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) 并编辑 `get_strands_registered_tools` 以包含您的新工具。

- [可选] 为前端添加清晰的名称和描述。这一步是可选的，如果不执行此步骤，将使用函数中的工具名称和描述。由于这些是供 LLM 使用的，建议添加用户友好的解释以获得更好的用户体验。

  - 编辑 i18n 文件。打开 [en/index.ts](../frontend/src/i18n/en/index.ts) 并在 `agent.tools` 中添加您自己的 `name` 和 `description`。
  - 同样编辑 `xx/index.ts`。其中 `xx` 代表您希望的国家代码。

- 运行 `npx cdk deploy` 以部署您的更改。这将使您的自定义工具在自定义机器人界面中可用。