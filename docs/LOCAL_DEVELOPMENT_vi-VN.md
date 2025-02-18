# Phát triển trên máy local

Would you like me to continue translating the rest of the content? I'll make sure to follow the critical requirements you specified.

## Phát Triển Backend

Xem [backend/README](../backend/README_vi-VN.md).

## Phát triển Frontend

Trong ví dụ này, bạn có thể sửa đổi và khởi chạy frontend cục bộ bằng cách sử dụng các tài nguyên AWS (`API Gateway`, `Cognito`, v.v.) đã được triển khai với `npx cdk deploy`.

1. Tham khảo [Triển khai bằng CDK](../README.md#deploy-using-cdk) để triển khai trên môi trường AWS.
2. Sao chép `frontend/.env.template` và lưu thành `frontend/.env.local`.
3. Điền nội dung của `.env.local` dựa trên kết quả đầu ra của `npx cdk deploy` (như `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Thực thi lệnh sau:

```zsh
cd frontend && npm ci && npm run dev
```

## (Tùy chọn, khuyến nghị) Thiết lập hook pre-commit

Chúng tôi đã giới thiệu các GitHub workflows để kiểm tra kiểu và kiểm tra mã. Các quy trình này được thực thi khi một Pull Request được tạo, nhưng việc chờ đợi quá trình kiểm tra mã hoàn tất trước khi tiếp tục không phải là trải nghiệm phát triển tốt. Do đó, các tác vụ kiểm tra mã này nên được thực hiện tự động tại giai đoạn commit. Chúng tôi đã giới thiệu [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) như một cơ chế để đạt được điều này. Việc sử dụng này không bắt buộc, nhưng chúng tôi khuyến nghị áp dụng nó để có trải nghiệm phát triển hiệu quả. Ngoài ra, mặc dù chúng tôi không áp đặt định dạng TypeScript với [Prettier](https://prettier.io/), nhưng chúng tôi rất mong bạn có thể áp dụng nó khi đóng góp, vì nó giúp ngăn chặn các khác biệt không cần thiết trong quá trình xem xét mã.

### Cài đặt lefthook

Tham khảo [tại đây](https://github.com/evilmartians/lefthook#install). Nếu bạn là người dùng Mac và homebrew, chỉ cần chạy `brew install lefthook`.

### Cài đặt poetry

Điều này là cần thiết vì việc kiểm tra mã Python phụ thuộc vào `mypy` và `black`.

```sh
cd backend
python3 -m venv .venv  # Tùy chọn (Nếu bạn không muốn cài đặt poetry trên môi trường của mình)
source .venv/bin/activate  # Tùy chọn (Nếu bạn không muốn cài đặt poetry trên môi trường của mình)
pip install poetry
poetry install
```

Để biết thêm chi tiết, vui lòng kiểm tra [README backend](../backend/README_vi-VN.md).

### Tạo hook pre-commit

Chỉ cần chạy `lefthook install` trong thư mục gốc của dự án này.