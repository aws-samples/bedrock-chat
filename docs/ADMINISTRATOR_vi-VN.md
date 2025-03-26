# Tính năng dành cho quản trị viên

Các tính năng dành cho quản trị viên là một công cụ quan trọng vì nó cung cấp những thông tin chi tiết thiết yếu về việc sử dụng bot tùy chỉnh và hành vi người dùng. Nếu không có chức năng này, các quản trị viên sẽ gặp khó khăn trong việc hiểu được những bot tùy chỉnh nào đang phổ biến, tại sao chúng lại phổ biến, và ai đang sử dụng chúng. Thông tin này rất quan trọng để tối ưu hóa các lời nhắc hướng dẫn, tùy chỉnh các nguồn dữ liệu RAG, và xác định những người dùng nặng ký có thể trở thành những người có ảnh hưởng.

## Vòng phản hồi

Đầu ra từ LLM không phải lúc nào cũng đáp ứng được kỳ vọng của người dùng. Đôi khi nó không thể thỏa mãn nhu cầu của người dùng. Để hiệu quả "tích hợp" LLM vào hoạt động kinh doanh và cuộc sống hàng ngày, việc triển khai vòng phản hồi là rất quan trọng. Bedrock Claude Chat được trang bị tính năng phản hồi được thiết kế để giúp người dùng phân tích lý do tại sao sự không hài lòng xuất hiện. Dựa trên kết quả phân tích, người dùng có thể điều chỉnh các lời nhắc, nguồn dữ liệu RAG và các thông số tương ứng.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Các nhà phân tích dữ liệu có thể truy cập nhật ký cuộc hội thoại bằng [Amazon Athena](https://aws.amazon.com/jp/athena/). Nếu họ muốn phân tích dữ liệu bằng [Jupyter Notebook](https://jupyter.org/), [ví dụ notebook này](../examples/notebooks/feedback_analysis_example.ipynb) có thể là một tham khảo.

## Bảng điều khiển quản trị

Hiện tại cung cấp tổng quan cơ bản về việc sử dụng chatbot và người dùng, tập trung vào việc tổng hợp dữ liệu cho từng bot và người dùng trong các khoảng thời gian được chỉ định và sắp xếp kết quả theo phí sử dụng.

![](./imgs/admin_bot_analytics.png)

> [!Lưu ý]
> Phân tích sử dụng người dùng sẽ sớm được cung cấp.

### Điều kiện tiên quyết

Người dùng quản trị phải là thành viên của nhóm được gọi là `Admin`, có thể được thiết lập thông qua bảng điều khiển quản lý > Amazon Cognito User pools hoặc aws cli. Lưu ý rằng ID nhóm người dùng có thể được tham chiếu bằng cách truy cập CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Ghi chú

- Như đã nêu trong [kiến trúc](../README.md#architecture), các tính năng quản trị sẽ tham chiếu đến bucket S3 được xuất từ DynamoDB. Lưu ý rằng do việc xuất được thực hiện mỗi giờ một lần, các cuộc trò chuyện mới nhất có thể sẽ không được phản ánh ngay lập tức.

- Trong việc sử dụng bot công khai, các bot chưa được sử dụng trong khoảng thời gian được chỉ định sẽ không được liệt kê.

- Trong việc sử dụng của người dùng, những người dùng chưa sử dụng hệ thống trong khoảng thời gian được chỉ định sẽ không được liệt kê.

> [!Quan trọng] > **Tên Cơ Sở Dữ Liệu Môi Trường Đa**
>
> Nếu bạn đang sử dụng nhiều môi trường (dev, prod, v.v.), tên cơ sở dữ liệu Athena sẽ bao gồm tiền tố môi trường. Thay vì `bedrockchatstack_usage_analysis`, tên cơ sở dữ liệu sẽ là:
>
> - Đối với môi trường mặc định: `bedrockchatstack_usage_analysis`
> - Đối với các môi trường được đặt tên: `<tiền-tố-môi-trường>_bedrockchatstack_usage_analysis` (ví dụ: `dev_bedrockchatstack_usage_analysis`)
>
> Ngoài ra, tên bảng sẽ bao gồm tiền tố môi trường:
>
> - Đối với môi trường mặc định: `ddb_export`
> - Đối với các môi trường được đặt tên: `<tiền-tố-môi-trường>_ddb_export` (ví dụ: `dev_ddb_export`)
>
> Đảm bảo điều chỉnh các truy vấn của bạn một cách phù hợp khi làm việc với nhiều môi trường.

## Tải xuống dữ liệu cuộc trò chuyện

Bạn có thể truy vấn nhật ký cuộc trò chuyện bằng Athena, sử dụng SQL. Để tải xuống nhật ký, hãy mở Trình soạn thảo Truy vấn Athena từ bảng điều khiển quản lý và chạy SQL. Dưới đây là một số truy vấn ví dụ hữu ích để phân tích các trường hợp sử dụng. Phản hồi có thể được tham khảo trong thuộc tính `MessageMap`.

### Truy vấn theo ID Bot

Chỉnh sửa `bot-id` và `datehour`. `bot-id` có thể được tham khảo trên màn hình Quản lý Bot, có thể truy cập từ API Xuất Bản Bot, hiển thị trên thanh bên trái. Lưu ý phần cuối của URL như `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

> [!Lưu ý]
> Nếu sử dụng môi trường có tên (ví dụ: "dev"), hãy thay thế `bedrockchatstack_usage_analysis.ddb_export` bằng `dev_bedrockchatstack_usage_analysis.dev_ddb_export` trong truy vấn ở trên.

### Truy vấn theo ID Người dùng

Chỉnh sửa `user-id` và `datehour`. `user-id` có thể được tham khảo trên màn hình Quản lý Bot.

> [!Lưu ý]
> Phân tích sử dụng của người dùng sắp được ra mắt.

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

> [!Lưu ý]
> Nếu sử dụng môi trường có tên (ví dụ: "dev"), hãy thay thế `bedrockchatstack_usage_analysis.ddb_export` bằng `dev_bedrockchatstack_usage_analysis.dev_ddb_export` trong truy vấn ở trên.