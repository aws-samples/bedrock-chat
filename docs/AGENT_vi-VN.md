# Đại Lý Được Hỗ Trợ bởi LLM (ReAct)

## Agent (ReAct) là gì?

Agent là một hệ thống AI tiên tiến sử dụng các mô hình ngôn ngữ lớn (LLMs) làm động cơ tính toán trung tâm. Nó kết hợp các khả năng suy luận của LLMs với các chức năng bổ sung như lập kế hoạch và sử dụng công cụ để tự động thực hiện các nhiệm vụ phức tạp. Các Agent có thể phân tích các truy vấn phức tạp, tạo ra các giải pháp từng bước, và tương tác với các công cụ hoặc API bên ngoài để thu thập thông tin hoặc thực hiện các nhiệm vụ phụ.

Mẫu này triển khai một Agent sử dụng phương pháp [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct cho phép agent giải quyết các nhiệm vụ phức tạp bằng cách kết hợp suy luận và hành động trong một vòng phản hồi lặp đi lặp lại. Agent liên tục trải qua ba bước chính: Suy nghĩ, Hành động và Quan sát. Nó phân tích tình huện hiện tại bằng cách sử dụng LLM, quyết định hành động tiếp theo cần thực hiện, thực thi hành động bằng các công cụ hoặc API có sẵn, và học hỏi từ các kết quả quan sát được. Quá trình liên tục này cho phép agent thích ứng với các môi trường năng động, cải thiện độ chính xác giải quyết nhiệm vụ, và cung cấp các giải pháp nhạy với bối cảnh.

## Ví Dụ Về Trường Hợp Sử Dụng

Một Tác Nhân sử dụng ReAct có thể được áp dụng trong nhiều tình huống khác nhau, cung cấp các giải pháp chính xác và hiệu quả.

### Chuyển Đổi Văn Bản Sang SQL

Một người dùng yêu cầu "tổng doanh số của quý vừa qua". Tác Nhân sẽ hiểu yêu cầu này, chuyển đổi nó thành một truy vấn SQL, thực thi truy vấn trên cơ sở dữ liệu, và trình bày kết quả.

### Dự Báo Tài Chính

Một chuyên viên phân tích tài chính cần dự báo doanh thu của quý tới. Tác Nhân sẽ thu thập dữ liệu có liên quan, thực hiện các phép tính cần thiết bằng các mô hình tài chính, và tạo ra một báo cáo dự báo chi tiết, đảm bảo tính chính xác của các dự đoán.

## Sử dụng Tính năng Đại lý

Để kích hoạt chức năng Đại lý cho chatbot tùy chỉnh của bạn, hãy làm theo các bước sau:

Có hai cách để sử dụng Tính năng Đại lý:

### Sử dụng Công cụ

Để kích hoạt chức năng Đại lý với Sử dụng Công cụ cho chatbot tùy chỉnh của bạn, hãy làm theo các bước sau:

1. Điều hướng đến phần Đại lý trong màn hình bot tùy chỉnh.

2. Trong phần Đại lý, bạn sẽ tìm thấy danh sách các công cụ có sẵn có thể được sử dụng bởi Đại lý. Theo mặc định, tất cả các công cụ đều bị vô hiệu hóa.

3. Để kích hoạt một công cụ, chỉ cần chuyển công tắc bên cạnh công cụ mong muốn. Một khi công cụ được kích hoạt, Đại lý sẽ có quyền truy cập và có thể sử dụng nó khi xử lý truy vấn của người dùng.

![](./imgs/agent_tools.png)

4. Ví dụ, công cụ "Tìm kiếm Internet" cho phép Đại lý tìm nạp thông tin từ internet để trả lời các câu hỏi của người dùng.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Bạn có thể phát triển và thêm các công cụ tùy chỉnh của riêng mình để mở rộng khả năng của Đại lý. Tham khảo phần [Cách phát triển công cụ của riêng bạn](#how-to-develop-your-own-tools) để biết thêm thông tin về việc tạo và tích hợp các công cụ tùy chỉnh.

### Sử dụng Đại lý Bedrock

Bạn có thể sử dụng [Đại lý Bedrock](https://aws.amazon.com/bedrock/agents/) được tạo trong Amazon Bedrock.

Trước tiên, tạo một Đại lý trong Bedrock (ví dụ: qua Bảng điều khiển Quản lý). Sau đó, chỉ định ID Đại lý trong màn hình cài đặt bot tùy chỉnh. Một khi được thiết lập, chatbot của bạn sẽ tận dụng Đại lý Bedrock để xử lý các truy vấn của người dùng.

![](./imgs/bedrock_agent_tool.png)

## Cách phát triển công cụ của riêng bạn

Để phát triển các công cụ tùy chỉnh cho Agent, hãy làm theo các hướng dẫn sau:

- Tạo một lớp mới kế thừa từ lớp `AgentTool`. Mặc dù giao diện tương thích với LangChain, nhnhưmngu mẫu này cung cấp lớp `AgentTool` riêng mà bạn nên kếa ([nguồn](../backend/app/agents/tools/agent_tool.py)).

- Tham khảo triển khai mẫu của [công cụ tính BMI](../examples/agents/tools/bmi/bmi.py). Ví dụ này cho thấy cách tạo một công cụ tính Chỉ số Khối Cơ thể (BMI) dựa trên đầu vào của người dùng.

  - Tên và mô tả được khai báo trên công cụ được sử dụng khi LLM xem xcông xcụnào nnào nên nđược sdụng dđể trả lời câlh�i của người ddùng.Ngói khác, chúng được nhúng vào lời nhắc khi gọi LLM. Do đó, khuybáến khích mô tả càng chính xác càng t.

- [`Tùchyn Sau khi đđã triển khai công cụ tùy chỉnh, kibạn, bạn nênnn xác minh chức năng của nó bằng cngập lệể../vd](../examples/agents/tools/bmi/test_bmi.py)).. Tập lnh này sẽ giúp bạn đảm bảo rằng công cụ của bạn đang hoạt động như mđợ- Saum khi phát triển và kiểm tra xong công hchuyển tệp triển khai đếnàthànhến thư [backend/app/agents/tools/](../backend/app/agents/tools/). Sau đó mở [ệbackend agents/utils.py](../backend/app/agents/utils.py) và chỉnh sửa `get_available_tools` để người dùng có thể chọn công cụ đã phát triển.

- [Tùy chọ]êênên và mô tả rõ ràng cho giao diện người dùng. Bước này là ty, nếu khôngm thực hiện,, tên và mô tả được khaibảo trong công dtrong công c�ụ của bạn sẽ được sử dchúng dành cho LLM chứ không phải cho người dùng, doạy khuyến nghích thêm giảiuyệcung thiện trảimg  -Ay ch�sfilep i18nở n. Mở [en/index.ts](../frontend/src/i18n/en/index.ts) và thêm `name` và `description` củaririêng bạn vào `agent.tools`.
  -ở Chsửxx/` index.ts đ. Trong đó` xx bitượng mãngã quốc bạc.

- `np`npx cdk deploy` để trikhai ththay đổi của bạn. Điều này sẽ khcc chcủa trong mà hình tùy chỉnh bot.

## Đóng góp

**Chúng tôi hoan nghênh các đóng góp cho kho công cụ này!** Nếu bạn phát triển một công cụ hữu ích và được triển khai tốt, hãy cân nhắc đóng góp nó cho dự án bằng cách gửi một issue hoặc pull request.