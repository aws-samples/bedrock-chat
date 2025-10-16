# Tác nhân được hỗ trợ bởi LLM (ReAct)

## Agent (ReAct) là gì?

Agent là một hệ thống AI tiên tiến sử dụng các mô hình ngôn ngữ lớn (LLM) làm động cơ tính toán trung tâm. Nó kết hợp khả năng lập luận của LLM với các chức năng bổ sung như lập kế hoạch và sử dụng công cụ để tự động thực hiện các tác vụ phức tạp. Agent có thể chia nhỏ các truy vấn phức tạp, tạo ra giải pháp từng bước và tương tác với các công cụ hoặc API bên ngoài để thu thập thông tin hoặc thực thi các tác vụ phụ.

Mẫu này triển khai một Agent sử dụng phương pháp [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct cho phép agent giải quyết các tác vụ phức tạp bằng cách kết hợp lập luận và hành động trong một vòng lặp phản hồi. Agent liên tục trải qua ba bước chính: Suy nghĩ, Hành động và Quan sát. Nó phân tích tình huống hiện tại bằng LLM, quyết định hành động tiếp theo cần thực hiện, thực thi hành động đó bằng các công cụ hoặc API có sẵn, và học hỏi từ kết quả quan sát được. Quá trình liên tục này cho phép agent thích nghi với môi trường động, cải thiện độ chính xác trong giải quyết tác vụ và đưa ra các giải pháp phù hợp với ngữ cảnh.

Việc triển khai được hỗ trợ bởi [Strands Agents](https://strandsagents.com/), một SDK mã nguồn mở sử dụng phương pháp tiếp cận hướng mô hình để xây dựng các AI agent. Strands cung cấp một framework nhẹ, linh hoạt để tạo các công cụ tùy chỉnh bằng cách sử dụng Python decorators và hỗ trợ nhiều nhà cung cấp mô hình khác nhau bao gồm cả Amazon Bedrock.

## Ví dụ Trường hợp Sử dụng

Một Agent sử dụng ReAct có thể được áp dụng trong nhiều tình huống khác nhau, cung cấp giải pháp chính xác và hiệu quả.

### Text-to-SQL

Một người dùng yêu cầu "tổng doanh số bán hàng của quý trước." Agent sẽ diễn giải yêu cầu này, chuyển đổi nó thành truy vấn SQL, thực thi truy vấn đối với cơ sở dữ liệu và trình bày kết quả.

### Dự báo Tài chính

Một chuyên viên phân tích tài chính cần dự báo doanh thu quý tới. Agent thu thập dữ liệu liên quan, thực hiện các tính toán cần thiết sử dụng các mô hình tài chính, và tạo ra báo cáo dự báo chi tiết, đảm bảo độ chính xác của các dự đoán.

## Để sử dụng tính năng Agent

Để kích hoạt chức năng Agent cho chatbot tùy chỉnh của bạn, hãy làm theo các bước sau:

Có hai cách để sử dụng tính năng Agent:

### Sử dụng Tool Use

Để kích hoạt chức năng Agent với Tool Use cho chatbot tùy chỉnh của bạn, hãy làm theo các bước sau:

1. Điều hướng đến phần Agent trong màn hình bot tùy chỉnh.

2. Trong phần Agent, bạn sẽ thấy danh sách các công cụ có sẵn mà Agent có thể sử dụng. Theo mặc định, tất cả các công cụ đều bị vô hiệu hóa.

3. Để kích hoạt một công cụ, chỉ cần bật công tắc bên cạnh công cụ mong muốn. Khi một công cụ được kích hoạt, Agent sẽ có quyền truy cập vào nó và có thể sử dụng nó khi xử lý các truy vấn của người dùng.

![](./imgs/agent_tools.png)

4. Ví dụ, công cụ "Internet Search" cho phép Agent tìm kiếm thông tin từ internet để trả lời câu hỏi của người dùng.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Bạn có thể phát triển và thêm các công cụ tùy chỉnh của riêng mình để mở rộng khả năng của Agent. Tham khảo phần [How to develop your own tools](#how-to-develop-your-own-tools) để biết thêm thông tin về việc tạo và tích hợp các công cụ tùy chỉnh.

### Sử dụng Bedrock Agent

Bạn có thể sử dụng [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) được tạo trong Amazon Bedrock.

Đầu tiên, tạo một Agent trong Bedrock (ví dụ: thông qua Management Console). Sau đó, chỉ định Agent ID trong màn hình cài đặt bot tùy chỉnh. Sau khi thiết lập, chatbot của bạn sẽ tận dụng Bedrock Agent để xử lý các truy vấn của người dùng.

![](./imgs/bedrock_agent_tool.png)

## Cách phát triển công cụ của riêng bạn

Để phát triển các công cụ tùy chỉnh cho Agent bằng Strands SDK, hãy làm theo các hướng dẫn sau:

### Về Công cụ Strands

Strands cung cấp một decorator `@tool` đơn giản để chuyển đổi các hàm Python thông thường thành công cụ cho AI agent. Decorator này tự động trích xuất thông tin từ docstring và type hints của hàm để tạo ra các thông số kỹ thuật mà LLM có thể hiểu và sử dụng. Cách tiếp cận này tận dụng các tính năng có sẵn của Python để có trải nghiệm phát triển công cụ sạch sẽ và chức năng.

Để biết thông tin chi tiết về công cụ Strands, hãy xem [Tài liệu Python Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Tạo Công cụ Cơ bản

Tạo một hàm mới được trang trí bằng decorator `@tool` từ Strands:

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

### Công cụ với Bot Context (Mẫu Closure)

Để truy cập thông tin bot (BotModel), sử dụng mẫu closure để nắm bắt ngữ cảnh bot:

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

### Yêu cầu về Định dạng Trả về

Tất cả công cụ Strands phải trả về một từ điển có cấu trúc sau:

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

- Sử dụng `{"text": "message"}` cho phản hồi văn bản đơn giản
- Sử dụng `{"json": data}` cho dữ liệu phức tạp cần được bảo toàn dưới dạng thông tin có cấu trúc
- Luôn đặt `status` là `"success"` hoặc `"error"`

### Hướng dẫn Triển khai

- Tên hàm và docstring được sử dụng khi LLM xem xét công cụ nào để sử dụng. Docstring được nhúng trong prompt, vì vậy hãy mô tả chính xác mục đích và tham số của công cụ.

- Tham khảo mẫu triển khai của [công cụ tính BMI](../examples/agents/tools/bmi/bmi_strands.py). Ví dụ này minh họa cách tạo một công cụ tính Chỉ số Khối cơ thể (BMI) bằng decorator `@tool` của Strands và mẫu closure.

- Sau khi hoàn thành phát triển, đặt file triển khai của bạn trong thư mục [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/). Sau đó mở [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) và chỉnh sửa `get_strands_registered_tools` để thêm công cụ mới của bạn.

- [Tùy chọn] Thêm tên và mô tả rõ ràng cho frontend. Bước này là tùy chọn, nhưng nếu bạn không thực hiện bước này, tên và mô tả công cụ từ hàm của bạn sẽ được sử dụng. Vì những thông tin này dành cho LLM sử dụng, nên bạn nên thêm giải thích thân thiện với người dùng để có trải nghiệm người dùng tốt hơn.

  - Chỉnh sửa file i18n. Mở [en/index.ts](../frontend/src/i18n/en/index.ts) và thêm `name` và `description` của riêng bạn vào `agent.tools`.
  - Chỉnh sửa `xx/index.ts` tương tự. Trong đó `xx` đại diện cho mã quốc gia bạn muốn.

- Chạy `npx cdk deploy` để triển khai các thay đổi của bạn. Điều này sẽ làm cho công cụ tùy chỉnh của bạn có sẵn trong màn hình bot tùy chỉnh.