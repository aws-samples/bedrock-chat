# Hướng Dẫn Di Chuyển (từ v0 đến v1)

Nếu bạn đã sử dụng Bedrock Chat với phiên bản trước đó (~`0.4.x`), bạn cần thực hiện các bước dưới đây để di chuyển.

## Tại là gì?

Bản cập nhật lớn này bao gồm các bản cập nhật bảo mật quan trọng.

- Kho lưu trữ cơ sở dữ liệu vector (tức là pgvector trên Aurora PostgreSQL) giờ đã được mã hóa, điều này sẽ kích hoạt việc thay thế khi triển khai. Điều này có nghĩa là các mục vector hiện có sẽ bị xóa.
- Chúng tôi đã giới thiệu nhatingowed` nhóm người dùng Cognito để hạhn người dùng có thể tạo bot. Người dùng hiện tại không thuộc nhóm này, vì vậy bạn cần gắn quyền một cách thủ công nếu muốn họ có khả năng tạo bot. Xem: [Cá nhân hóa Bot](../../README.md#bot-personalization)

## Điều kiện tiên quyết

Đọc [Hướng dẫn Di chuyển Cơ sở dữ liệu](./DATABASE_MIGRATION_vi-VN.md) và xác định phương pháp khôi phục các mục.

## Các bước

### Di chuyển kho vector

- Mở terminal và điều hướng đến thư mục dự án
- Kéo nhánh bạn muốn triển khai. Sau đây là chuyển sang nhánh mong muốn (trong trường hợp này là `v1`) và kéo các thay đổi mới nhất:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Nếu bạn muốn khôi phục các mục với DMS, ĐỪNG QUÊN vô hiệu hóa việc xoay mật khẩu và ghi chú mật khẩu để truy cập cơ sở dữ liệu. Nếu khôi phục bằng tập lệnh di chuyển ([migrate_v0_v1.py](./migrate_v0_v1.py)), bạn không cần ghi chú mật khẩu.
- Xóa tất cả [các API đã xuất bản](../PUBLISH_API_vi-VN.md) để CloudFormation có thể xóa cụm Aurora hiện tại.
- Chạy [npx cdk deploy](../README.md#deploy-using-cdk) sẽ kích hoạt việc thay thế cụm Aurora và XÓA TẤT CẢ CÁC MỤC VECTOR.
- Thực hiện theo [Hướng dẫn Di chuyển Cơ sở dữ liệu](./DATABASE_MIGRATION_vi-VN.md) để khôi phục các mục vector.
- Xác minh người dùng có thể sử dụng các bot hiện có có kiến thức, tức là các bot RAG.

### Gắn quyền CreatingBotAllowed

- Sau khi triển khai, tất cả người dùng sẽ không thể tạo bot mới.
- Nếu bạn muốn người dùng cụ thể có thể tạo bot, hãy thêm những người dùng đó vào nhóm `CreatingBotAllowed` bằng bảng điều khiển quản lý hoặc CLI.
- Xác minh xem người dùng có thể tạo bot không. Lưu ý rằng người dùng cần đăng nhập lại.