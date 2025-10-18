# LLM 驅動的代理 (ReAct)

## 什麼是 Agent (ReAct)?

Agent 是一個以大型語言模型 (LLM) 為核心運算引擎的進階 AI 系統。它結合了 LLM 的推理能力以及規劃和工具使用等額外功能,能夠自主執行複雜任務。Agent 可以分解複雜的查詢、生成逐步解決方案,並與外部工具或 API 互動以收集資訊或執行子任務。

這個範例使用 [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) 方法來實作 Agent。ReAct 讓 Agent 能夠透過結合推理和行動的反饋循環來解決複雜任務。Agent 會重複執行三個關鍵步驟:思考、行動和觀察。它使用 LLM 分析當前情況、決定下一步行動、使用可用的工具或 API 執行行動,並從觀察到的結果中學習。這個持續的過程讓 Agent 能夠適應動態環境、提升任務解決的準確度,並提供符合情境的解決方案。

此實作是由 [Strands Agents](https://strandsagents.com/) 驅動,這是一個採用模型驅動方法來建構 AI agents 的開源 SDK。Strands 提供了一個輕量且靈活的框架,可以使用 Python 裝飾器來創建自訂工具,並支援包括 Amazon Bedrock 在內的多個模型提供者。

## 使用案例範例

使用 ReAct 的 Agent 可以應用在各種情境中，提供準確且有效率的解決方案。

### 文字轉 SQL

當使用者詢問「上一季度的總銷售額」時，Agent 會解讀這個請求，將其轉換為 SQL 查詢，在資料庫中執行查詢，並呈現結果。

### 財務預測

當財務分析師需要預測下一季度的營收時，Agent 會收集相關資料，使用財務模型進行必要的計算，並生成詳細的預測報告，確保預測的準確性。

## 使用 Agent 功能

要為您的自定義聊天機器人啟用 Agent 功能，請按照以下步驟操作：

有兩種使用 Agent 功能的方式：

### 使用工具功能

要為您的自定義聊天機器人啟用帶有工具使用功能的 Agent，請按照以下步驟操作：

1. 在自定義機器人畫面中導航至 Agent 部分。

2. 在 Agent 部分，您會看到 Agent 可以使用的工具列表。預設情況下，所有工具都是停用的。

3. 要啟用工具，只需切換所需工具旁邊的開關。一旦工具被啟用，Agent 就可以存取並在處理用戶查詢時使用它。

![](./imgs/agent_tools.png)

4. 例如，「網路搜尋」工具允許 Agent 從網路獲取資訊來回答用戶問題。

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. 您可以開發並添加自己的自定義工具來擴展 Agent 的功能。有關創建和整合自定義工具的更多資訊，請參考[如何開發自己的工具](#how-to-develop-your-own-tools)部分。

### 使用 Bedrock Agent

您可以使用在 Amazon Bedrock 中創建的 [Bedrock Agent](https://aws.amazon.com/bedrock/agents/)。

首先，在 Bedrock 中創建一個 Agent（例如，通過管理控制台）。然後，在自定義機器人設置畫面中指定 Agent ID。設置完成後，您的聊天機器人將利用 Bedrock Agent 來處理用戶查詢。

![](./imgs/bedrock_agent_tool.png)

## 如何開發自己的工具

要使用 Strands SDK 為 Agent 開發自定義工具，請遵循以下指南：

### 關於 Strands 工具

Strands 提供了一個簡單的 `@tool` 裝飾器，可將普通的 Python 函數轉換為 AI agent 工具。該裝飾器會自動從函數的文檔字符串和類型提示中提取信息，創建 LLM 可以理解和使用的工具規格。這種方法利用 Python 的原生特性，提供了一個簡潔、實用的工具開發體驗。

有關 Strands 工具的詳細信息，請參閱 [Python Tools 文檔](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/)。

### 基本工具創建

使用 Strands 的 `@tool` 裝飾器創建新函數：

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    安全地執行數學計算。

    Args:
        expression: 要計算的數學表達式（例如："2+2"、"10*5"、"sqrt(16)"）

    Returns:
        dict: Strands 格式的結果，包含 toolUseId、status 和 content
    """
    try:
        # 在此處添加計算邏輯
        result = eval(expression)  # 注意：在生產環境中使用安全的計算方法
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

### 帶有機器人上下文的工具（閉包模式）

要訪問機器人信息（BotModel），請使用捕獲機器人上下文的閉包模式：

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """創建帶有機器人上下文閉包的計算器工具。"""

    @tool
    def calculator(expression: str) -> dict:
        """
        安全地執行數學計算。

        Args:
            expression: 要計算的數學表達式（例如："2+2"、"10*5"、"sqrt(16)"）

        Returns:
            dict: Strands 格式的結果，包含 toolUseId、status 和 content
        """
        # 在工具內部訪問機器人上下文
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # 在生產環境中使用安全的計算方法
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

所有 Strands 工具必須返回具有以下結構的字典：

```python
{
    "toolUseId": "placeholder",  # 將由 Strands 替換
    "status": "success" | "error",
    "content": [
        {"text": "簡單文本回應"} |
        {"json": {"key": "複雜數據對象"}}
    ]
}
```

- 使用 `{"text": "message"}` 作為簡單文本回應
- 使用 `{"json": data}` 作為需要保持結構化的複雜數據
- 始終將 `status` 設置為 `"success"` 或 `"error"`

### 實施指南

- LLM 在考慮使用哪個工具時會使用函數名稱和文檔字符串。文檔字符串會嵌入到提示中，因此請準確描述工具的用途和參數。

- 參考 [BMI 計算工具](../examples/agents/tools/bmi/bmi_strands.py) 的示例實現。此示例展示了如何使用 Strands `@tool` 裝飾器和閉包模式創建計算身體質量指數（BMI）的工具。

- 完成開發後，將實現文件放在 [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/) 目錄中。然後打開 [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) 並編輯 `get_strands_registered_tools` 以包含您的新工具。

- [可選] 為前端添加清晰的名稱和描述。這一步是可選的，如果不執行此步驟，將使用函數中的工具名稱和描述。由於這些是供 LLM 使用的，建議添加用戶友好的解釋以獲得更好的用戶體驗。

  - 編輯 i18n 文件。打開 [en/index.ts](../frontend/src/i18n/en/index.ts) 並在 `agent.tools` 中添加您自己的 `name` 和 `description`。
  - 同樣編輯 `xx/index.ts`。其中 `xx` 代表您想要的國家代碼。

- 運行 `npx cdk deploy` 以部署您的更改。這將使您的自定義工具在自定義機器人界面中可用。