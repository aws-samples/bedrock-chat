# Thiết lập nhà cung cấp định danh bên ngoài cho Google

## Bước 1: Tạo Google OAuth 2.0 Client

1. Truy cập vào Google Developer Console.
2. Tạo một dự án mới hoặc chọn một dự án có sẵn.
3. Điều hướng đến "Credentials", sau đó nhấp vào "Create Credentials" và chọn "OAuth client ID".
4. Cấu hình màn hình chấp thuận nếu được yêu cầu.
5. Đối với loại ứng dụng, chọn "Web application".
6. Tạm thời để trống URI chuyển hướng để cài đặt sau.[Xem Bước 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Sau khi tạo xong, ghi lại Client ID và Client Secret.

Để biết chi tiết, truy cập [tài liệu chính thức của Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Bước 2: Lưu trữ Thông tin xác thực Google OAuth trong AWS Secrets Manager

1. Truy cập vào AWS Management Console.
2. Điều hướng đến Secrets Manager và chọn "Store a new secret".
3. Chọn "Other type of secrets".
4. Nhập clientId và clientSecret của Google OAuth dưới dạng cặp khóa-giá trị.

   1. Khóa: clientId, Giá trị: <YOUR_GOOGLE_CLIENT_ID>
   2. Khóa: clientSecret, Giá trị: <YOUR_GOOGLE_CLIENT_SECRET>

5. Làm theo hướng dẫn để đặt tên và mô tả secret. Ghi nhớ tên secret vì bạn sẽ cần nó trong mã CDK của mình. Ví dụ: googleOAuthCredentials (Sử dụng trong tên biến Bước 3 <YOUR_SECRET_NAME>)
6. Xem lại và lưu trữ secret.

### Lưu ý

Tên các khóa phải khớp chính xác với chuỗi 'clientId' và 'clientSecret'.

## Bước 3: Cập nhật cdk.json

Trong tệp cdk.json của bạn, thêm ID Provider và SecretName vào tệp cdk.json.

như sau:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Lưu ý

#### Tính duy nhất

userPoolDomainPrefix phải là duy nhất trên toàn cầu trong tất cả người dùng Amazon Cognito. Nếu bạn chọn một tiền tố đã được sử dụng bởi một tài khoản AWS khác, việc tạo domain user pool sẽ thất bại. Một cách thực hành tốt là bao gồm các định danh, tên dự án, hoặc tên môi trường trong tiền tố để đảm bảo tính duy nhất.

## Bước 4: Triển khai Stack CDK

Triển khai stack CDK của bạn lên AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Bước 5: Cập nhật Google OAuth Client với các URI chuyển hướng của Cognito

Sau khi triển khai stack, AuthApprovedRedirectURI sẽ hiển thị trong phần đầu ra của CloudFormation. Quay lại Google Developer Console và cập nhật OAuth client với các URI chuyển hướng chính xác.