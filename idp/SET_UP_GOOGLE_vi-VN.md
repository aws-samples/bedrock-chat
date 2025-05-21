# Thiết lập nhà cung cấp danh tính bên ngoài cho Google

## Bước 1: Tạo Client OAuth 2.0 của Google

1. Truy cập Bảng điều khiển Nhà phát triển Google.
2. Tạo một dự án mới hoặc chọn một dự án hiện có.
3. Điều hướng đến "Thông tin xác thực", sau đó nhấp vào "Tạo thông tin xác thực" và chọn "ID client OAuth".
4. Cấu hình màn hình đồng ý nếu được yêu cầu.
5. Đối với loại ứng dụng, chọn "Ứng dụng web".
6. Để trống URI chuyển hướng tạm thời để thiết lập sau, và lưu tạm thời.[Xem Bước 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Sau khi tạo, ghi lại ID Client và Client Secret.

Để biết chi tiết, hãy truy cập [tài liệu chính thức của Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Bước 2: Lưu Thông Tin Đăng Nhập Google OAuth trong AWS Secrets Manager

1. Truy cập vào AWS Management Console.
2. Điều hướng đến Secrets Manager và chọn "Store a new secret".
3. Chọn "Other type of secrets".
4. Nhập clientId và clientSecret của Google OAuth dưới dạng các cặp key-value.

   1. Key: clientId, Value: <YOUR_GOOGLE_CLIENT_ID>
   2. Key: clientSecret, Value: <YOUR_GOOGLE_CLIENT_SECRET>

5. Làm theo các lời nhắc để đặt tên và mô tả secret. Ghi chú tên secret vì bạn sẽ cần nó trong mã CDK. Ví dụ: googleOAuthCredentials. (Sử dụng trong tên biến <YOUR_SECRET_NAME> ở Bước 3)
6. Xem lại và lưu secret.

### Lưu Ý

Tên key phải chính xác là các chuỗi 'clientId' và 'clientSecret'.

## Bước 3: Cập nhật cdk.json

Trong tệp cdk.json của bạn, hãy thêm ID Provider và SecretName vào tệp cdk.json.

như sau:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<TÊN_BÍ_MẬT_CỦA_BẠN>"
      }
    ],
    "userPoolDomainPrefix": "<TIỀN_TỐ_MIỀN_DUY_NHẤT_CHO_USER_POOL_CỦA_BẠN>"
  }
}
```

### Lưu ý

#### Tính Duy Nhất

Tiền tố userPoolDomainPrefix phải là duy nhất trên toàn cầu giữa tất cả người dùng Amazon Cognito. Nếu bạn chọn một tiền tố đã được sử dụng bởi một tài khoản AWS khác, việc tạo miền user pool sẽ thất bại. Một thực hành tốt là bao gồm các định danh, tên dự án hoặc tên môi trường trong tiền tố để đảm bảo tính duy nhất.

## Bước 4: Triển Khai Stack CDK

Triển khai stack CDK của bạn lên AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Bước 5: Cập Nhật OAuth Client của Google với URI Chuyển Hướng Cognito

Sau khi triển khai stack, AuthApprovedRedirectURI sẽ hiển thị trong các kết quả của CloudFormation. Hãy quay lại Bảng điều khiển Nhà phát triển Google và cập nhật OAuth client với các URI chuyển hướng chính xác.