# Hướng dẫn di chuyển (v0 sang v1)

Nếu bạn đã sử dụng Bedrock Chat với phiên bản trước đó (~`0.4.x`), bạn cần thực hiện các bước dưới đây để di chuyển.

## Tại sao tôi cần phải làm điều này?

Bản cập nhật lớn này bao gồm các cập nhật bảo mật quan trọng.

- Kho lưu trữ cơ sở dữ liệu vector (tức là pgvector trên Aurora PostgreSQL) hiện đã được mã hóa, điều này kích hoạt việc thay thế khi triển khai. Điều này có nghĩa là các mục vector hiện có sẽ bị xóa.
- Chúng tôi đã giới thiệu nhóm người dùng Cognito `CreatingBotAllowed` để giới hạn những người dùng có thể tạo bot. Những người dùng hiện tại không nằm trong nhóm này, vì vậy bạn cần gắn quyền thủ công nếu muốn họ có khả năng tạo bot. Xem: [Bot Personalization](../../README.md#bot-personalization)

## Điều kiện tiên quyết

Đọc [Hướng dẫn Di chuyển Cơ sở dữ liệu](./DATABASE_MIGRATION_vi-VN.md) và xác định phương pháp khôi phục các mục.

## Các bước

### Di chuyển kho vector

- Mở terminal và di chuyển đến thư mục dự án
- Pull nhánh bạn muốn triển khai. Sau đây là cách pull về nhánh mong muốn (trong trường hợp này là `v1`) và lấy các thay đổi mới nhất:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Nếu bạn muốn khôi phục các mục bằng DMS, ĐỪNG QUÊN tắt tính năng xoay vòng mật khẩu và ghi lại mật khẩu để truy cập cơ sở dữ liệu. Nếu khôi phục bằng script di chuyển ([migrate_v0_v1.py](./migrate_v0_v1.py)), bạn không cần ghi nhớ mật khẩu.
- Xóa tất cả [API đã xuất bản](../PUBLISH_API_vi-VN.md) để CloudFormation có thể xóa cụm Aurora hiện có.
- Chạy [npx cdk deploy](../README.md#deploy-using-cdk) để kích hoạt thay thế cụm Aurora và XÓA TẤT CẢ CÁC MỤC VECTOR.
- Làm theo [Hướng dẫn Di chuyển Cơ sở dữ liệu](./DATABASE_MIGRATION_vi-VN.md) để khôi phục các mục vector.
- Xác minh rằng người dùng có thể sử dụng các bot hiện có có kiến thức, ví dụ như các bot RAG.

### Gắn quyền CreatingBotAllowed

- Sau khi triển khai, tất cả người dùng sẽ không thể tạo bot mới.
- Nếu bạn muốn cho phép một số người dùng cụ thể tạo bot, hãy thêm những người dùng đó vào nhóm `CreatingBotAllowed` bằng bảng điều khiển quản lý hoặc CLI.
- Xác minh xem người dùng có thể tạo bot hay không. Lưu ý rằng người dùng cần phải đăng nhập lại.