# Tính năng quản trị

## Điều kiện tiên quyết

Người dùng quản trị phải là thành viên của nhóm có tên `Admin`, có thể được thiết lập thông qua bảng điều khiển quản lý > Amazon Cognito User pools hoặc aws cli. Lưu ý rằng id của user pool có thể được tham chiếu bằng cách truy cập CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Đánh dấu bot công khai là Thiết yếu

Giờ đây, quản trị viên có thể đánh dấu các bot công khai là "Thiết yếu". Các bot được đánh dấu là Thiết yếu sẽ được hiển thị trong mục "Thiết yếu" của cửa hàng bot, giúp người dùng dễ dàng truy cập. Điều này cho phép quản trị viên ghim những bot quan trọng mà họ muốn tất cả người dùng sử dụng.

### Ví dụ

- Bot Hỗ trợ Nhân sự: Giúp nhân viên với các câu hỏi và công việc liên quan đến nhân sự.
- Bot Hỗ trợ CNTT: Cung cấp hỗ trợ cho các vấn đề kỹ thuật nội bộ và quản lý tài khoản.
- Bot Hướng dẫn Chính sách Nội bộ: Trả lời các câu hỏi thường gặp về quy định chấm công, chính sách bảo mật và các quy định nội bộ khác.
- Bot Hướng dẫn Nhân viên Mới: Hướng dẫn nhân viên mới về quy trình và cách sử dụng hệ thống trong ngày đầu tiên.
- Bot Thông tin Phúc lợi: Giải thích về các chương trình phúc lợi và dịch vụ phúc lợi của công ty.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Vòng phản hồi

Đầu ra từ LLM không phải lúc nào cũng đáp ứng được mong đợi của người dùng. Đôi khi nó không thể thỏa mãn nhu cầu của người dùng. Để "tích hợp" LLM vào hoạt động kinh doanh và cuộc sống hàng ngày một cách hiệu quả, việc triển khai vòng phản hồi là rất cần thiết. Bedrock Chat được trang bị tính năng phản hồi được thiết kế để giúp người dùng phân tích nguyên nhân gây ra sự không hài lòng. Dựa trên kết quả phân tích, người dùng có thể điều chỉnh các prompt, nguồn dữ liệu RAG và các tham số cho phù hợp.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Các chuyên gia phân tích dữ liệu có thể truy cập nhật ký hội thoại bằng [Amazon Athena](https://aws.amazon.com/jp/athena/). Nếu họ muốn phân tích dữ liệu bằng [Jupyter Notebook](https://jupyter.org/), [notebook mẫu này](../examples/notebooks/feedback_analysis_example.ipynb) có thể được dùng làm tham khảo.

## Bảng điều khiển

Hiện đang cung cấp tổng quan cơ bản về việc sử dụng chatbot và người dùng, tập trung vào việc tổng hợp dữ liệu cho từng bot và người dùng trong các khoảng thời gian cụ thể và sắp xếp kết quả theo phí sử dụng.

![](./imgs/admin_bot_analytics.png)

## Ghi chú

- Như đã nêu trong [kiến trúc](../README.md#architecture), các tính năng quản trị sẽ tham chiếu đến bucket S3 được xuất từ DynamoDB. Xin lưu ý rằng do việc xuất dữ liệu được thực hiện mỗi giờ một lần, các cuộc hội thoại mới nhất có thể không được phản ánh ngay lập tức.

- Trong thống kê sử dụng bot công khai, những bot chưa được sử dụng trong khoảng thời gian được chỉ định sẽ không được liệt kê.

- Trong thống kê người dùng, những người dùng chưa sử dụng hệ thống trong khoảng thời gian được chỉ định sẽ không được liệt kê.

> [!Important]
> Nếu bạn đang sử dụng nhiều môi trường (dev, prod, v.v.), tên cơ sở dữ liệu Athena sẽ bao gồm tiền tố môi trường. Thay vì `bedrockchatstack_usage_analysis`, tên cơ sở dữ liệu sẽ là:
>
> - Cho môi trường mặc định: `bedrockchatstack_usage_analysis`
> - Cho môi trường có tên: `<env-prefix>_bedrockchatstack_usage_analysis` (ví dụ: `dev_bedrockchatstack_usage_analysis`)
>
> Ngoài ra, tên bảng cũng sẽ bao gồm tiền tố môi trường:
>
> - Cho môi trường mặc định: `ddb_export`
> - Cho môi trường có tên: `<env-prefix>_ddb_export` (ví dụ: `dev_ddb_export`)
>
> Hãy đảm bảo điều chỉnh các truy vấn của bạn cho phù hợp khi làm việc với nhiều môi trường.

## Tải dữ liệu hội thoại

Bạn có thể truy vấn nhật ký hội thoại bằng Athena, sử dụng SQL. Để tải nhật ký, mở Athena Query Editor từ bảng điều khiển quản lý và chạy SQL. Dưới đây là một số ví dụ về các truy vấn hữu ích để phân tích các trường hợp sử dụng. Phản hồi có thể được tham chiếu trong thuộc tính `MessageMap`.

### Truy vấn theo Bot ID

Chỉnh sửa `bot-id` và `datehour`. `bot-id` có thể được tham chiếu trên màn hình Quản lý Bot, có thể truy cập từ Bot Publish APIs, hiển thị ở thanh bên trái. Lưu ý phần cuối của URL như `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> Nếu sử dụng môi trường có tên (ví dụ: "dev"), thay thế `bedrockchatstack_usage_analysis.ddb_export` bằng `dev_bedrockchatstack_usage_analysis.dev_ddb_export` trong truy vấn trên.

### Truy vấn theo User ID

Chỉnh sửa `user-id` và `datehour`. `user-id` có thể được tham chiếu trên màn hình Quản lý Bot.

> [!Note]
> Phân tích sử dụng của người dùng sẽ sớm ra mắt.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> Nếu sử dụng môi trường có tên (ví dụ: "dev"), thay thế `bedrockchatstack_usage_analysis.ddb_export` bằng `dev_bedrockchatstack_usage_analysis.dev_ddb_export` trong truy vấn trên.