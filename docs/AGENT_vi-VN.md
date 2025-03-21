# Tác Nhân Được Hỗ Trợ bởi LLM (ReAct)

## Agent (ReAct) là gì?

Agent là một hệ thống AI tiên tiến sử dụng các mô hình ngôn ngữ lớn (LLMs) làm động cơ tính toán trung tâm. Nó kết hợp các khả năng suy luận của LLMs với các chức năng bổ sung như lập kế hoạch và sử dụng công cụ để tự động thực hiện các nhiệm vụ phức tạp. Các Agent có thể phân tích các truy vấn phức tạp, tạo ra các giải pháp từng bước và tương tác với các công cụ hoặc API bên ngoài để thu thập thông tin hoặc thực hiện các nhiệm vụ phụ.

Mẫu này triển khai một Agent bằng cách sử dụng phương pháp [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct cho phép agent giải quyết các nhiệm vụ phức tạp bằng cách kết hợp suy luận và hành động trong một vòng phản hồi lặp đi lặp lại. Agent liên tục trải qua ba bước chính: Suy nghĩ, Hành động và Quan sát. Nó phân tích tình huện hiện tại bằng LLM, quyết định hành động tiếp theo cần thực hiện, thực thi hành động bằng các công cụ hoặc API có sẵn, và học hỏi từ các kết quả quan sát được. Quá trình liên tục này cho phép agent thích ứng với các môi trường năng động, cải thiện độ chính xác giải quyết nhiệm vụ và cung cấp các giải pháp nhạy với bối cảnh.

## Ví Dụ Về Trường Hợp Sử Dụng

Một Tác Nhân sử dụng ReAct có thể được áp dụng trong nhiều kịch bản khác nhau, mang lại các giải pháp chính xác và hiệu quả.

### Chuyển Đổi Văn Bản Sang SQL

Một người dùng yêu cầu "tổng doanh số bán hàng của quý vừa qua". Tác Nhân sẽ hiểu yêu cầu này, chuyển đổi nó thành một truy vấn SQL, thực thi truy vấn trên cơ sở dữ liệu, và trình bày kết quả.

### Dự Báo Tài Chính

Một nhà phân tích tài chính cần dự báo doanh thu của quý tới. Tác Nhân sẽ thu thập dữ liệu có liên quan, thực hiện các phép tính cần thiết bằng các mô hình tài chính, và tạo ra một báo cáo dự báo chi tiết, đảm bảo tính chính xác của các dự đoán.

## Sử dụng Tính năng Agent

Để bật chức năng Agent cho chatbot tùy chỉnh của bạn, hãy làm theo các bước sau:

1. Điều hướng đến phần Agent trong màn hình bot tùy chỉnh.

2. Trong phần Agent, bạn sẽ tìm thấy danh sách các công cụ có sẵn có thể được sử dụng bởi Agent. Theo mặc định, tất cả các công cụ đều bị vô hiệu hóa.

3. Để kích hoạt một công cụ, chỉ cần chuyển công tắc bên cạnh công cụ mong muốn. Một khi một công cụ được bật, Agent sẽ có quyền truy cập vào nó và có thể sử dụng nó khi xử lý truy vấn của người dùng.

![](./imgs/agent_tools.png)

> [!Quan trọng]
> Điều quan trọng cần lưu ý là việc bật bất kỳ công cụ nào trong phần Agent sẽ tự động coi chức năng "Kiến thức" như một công cụ. Điều này có nghĩa là LLM sẽ tự động xác định xem có nên sử dụng "Kiến thức" để trả lời truy vấn của người dùng hay không, coi nó như một trong những công cụ có sẵn.

4. Theo mặc định, công cụ "Tìm kiếm Internet" được cung cấp. Công cụ này cho phép Agent tìm nạp thông tin từ internet để trả lời câu hỏi của người dùng.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

Công cụ này phụ thuộc vào [DuckDuckGo](https://duckduckgo.com/) có giới hạn tỷ lệ. Nó phù hợp cho mục đích PoC hoặc demo, nhưng nếu bạn muốn sử dụng trong môi trường sản xuất, chúng tôi khuyến nghị sử dụng API tìm kiếm khác.

5. Bạn có thể phát triển và thêm các công cụ tùy chỉnh của riêng mình để mở rộng khả năng của Agent. Tham khảo phần [Cách phát triển các công cụ của riêng bạn](#how-to-develop-your-own-tools) để biết thêm thông tin về việc tạo và tích hợp các công cụ tùy chỉnh.

## Cách phát triển công cụ của riêng bạn

Để phát triển các công cụ tùy chỉnh cho Agent, hãy làm theo các hướng dẫn sau:

- Tạo một lớp mới kế thừa từ lớp `AgentTool`. Mặc dù giao diện tương thích với LangChain, nhưng việc triển khai mẫu này cung cấp lớp `AgentTool` riêng mà bạn nên kế thừa ([nguồn](../backend/app/agents/tools/agent_tool.py)).

- Tham khảo việc triển khai mẫu của [công cụ tính BMI](../examples/agents/tools/bmi/bmi.py). Ví dụ này cho thấy cách tạo một công cụ tính Chỉ số Khối Cơ Thể (BMI) dựa trên đầu vào của người dùng.

  - Tên và mô tả được khai báo trên công cụ được sử dụng khi LLM xem xét công cụ nào nên được sử dụng để trả lời câu hỏi của người dùng. Nói cách khác, chúng được nhúng vào lời nhắc khi gọi LLM. Vì vậy, nên mô tả càng chính xác càng tốt.

- [Tùy chọn] Sau khi triển khai công cụ tùy chỉnh của bạn, bạn nên xác minh chức năng của nó bằng tập lệnh kiểm tra ([ví dụ](../examples/agents/tools/bmi/test_bmi.py)). Tập lệnh này sẽ giúp bạn đảm bảo rằng công cụ của bạn hoạt động như mong đợi.

- Sau khi hoàn thành việc phát triển và kiểm tra công cụ tùy chỉnh, hãy di chuyển tệp triển khai đến thư mục [backend/app/agents/tools/](../backend/app/agents/tools/). Sau đó mở [backend/app/agents/utils.py](../backend/app/agents/utils.py) và chỉnh sửa `get_available_tools` để người dùng có thể chọn công cụ đã phát triển.

- [Tùy chọn] Thêm tên và mô tả rõ ràng cho giao diện người dùng. Bước này là tùy chọn, nhưng nếu bạn không thực hiện bước này, tên và mô tả công cụ được khai báo trong công cụ của bạn sẽ được sử dụng. Chúng dành cho LLM nhưng không phải cho người dùng, vì vậy bạn nên thêm giải thích chuyên dụng để cải thiện trải nghiệm người dùng.

  - Chỉnh sửa các tệp i18n. Mở [en/index.ts](../frontend/src/i18n/en/index.ts) và thêm `name` và `description` của riêng bạn vào `agent.tools`.
  - Chỉnh sửa `xx/index.ts` tương tự. Trong đó `xx` đại diện cho mã quốc gia bạn muốn.

- Chạy `npx cdk deploy` để triển khai các thay đổi của bạn. Điều này sẽ làm cho công cụ tùy chỉnh của bạn có sẵn trong màn hình bot tùy chỉnh.

## Đóng góp

**Chúng tôi hoan nghênh các đóng góp cho kho công cụ!** Nếu bạn phát triển một công cụ hữu ích và được triển khai tốt, hãy cân nhắc đóng góp nó cho dự án bằng cách gửi một issue hoặc pull request.