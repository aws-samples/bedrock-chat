# Phát triển cục bộ

## Phát triển Backend

Xem [backend/README](../backend/README_vi-VN.md).

## Phát triển Frontend

Trong mẫu này, bạn có thể chỉnh sửa và khởi chạy frontend cục bộ sử dụng các tài nguyên AWS (`API Gateway`, `Cognito`, v.v.) đã được triển khai bằng `npx cdk deploy`.

1. Tham khảo [Triển khai bằng CDK](../README.md#deploy-using-cdk) để triển khai trên môi trường AWS.
2. Sao chép `frontend/.env.template` và lưu thành `frontend/.env.local`.
3. Điền nội dung vào `.env.local` dựa trên kết quả đầu ra của `npx cdk deploy` (như `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Thực thi lệnh sau:

```zsh
cd frontend && npm ci && npm run dev
```

## (Tùy chọn, khuyến nghị) Thiết lập pre-commit hook

Chúng tôi đã giới thiệu các quy trình GitHub để kiểm tra kiểu dữ liệu và linting. Những quy trình này được thực thi khi tạo Pull Request, tuy nhiên việc phải chờ đợi quá trình linting hoàn thành trước khi tiếp tục không phải là trải nghiệm phát triển tốt. Do đó, các tác vụ linting này nên được thực hiện tự động tại giai đoạn commit. Chúng tôi đã giới thiệu [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) như một cơ chế để đạt được điều này. Mặc dù không bắt buộc, nhưng chúng tôi khuyến nghị áp dụng nó để có trải nghiệm phát triển hiệu quả. Ngoài ra, mặc dù chúng tôi không bắt buộc định dạng TypeScript với [Prettier](https://prettier.io/), chúng tôi sẽ rất cảm kích nếu bạn có thể áp dụng nó khi đóng góp, vì nó giúp tránh các diff không cần thiết trong quá trình review code.

### Cài đặt lefthook

Tham khảo [tại đây](https://github.com/evilmartians/lefthook#install). Nếu bạn là người dùng mac và homebrew, chỉ cần chạy `brew install lefthook`.

### Cài đặt poetry

Điều này là cần thiết vì việc linting code python phụ thuộc vào `mypy` và `black`.

```sh
cd backend
python3 -m venv .venv  # Tùy chọn (Nếu bạn không muốn cài đặt poetry trên môi trường của mình)
source .venv/bin/activate  # Tùy chọn (Nếu bạn không muốn cài đặt poetry trên môi trường của mình)
pip install poetry
poetry install
```

Để biết thêm chi tiết, vui lòng kiểm tra [backend README](../backend/README_vi-VN.md).

### Tạo pre-commit hook

Chỉ cần chạy `lefthook install` trong thư mục gốc của dự án này.