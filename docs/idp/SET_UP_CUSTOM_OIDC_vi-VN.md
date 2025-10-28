# Thiết lập nhà cung cấp định danh bên ngoài

## Bước 1: Tạo một OIDC Client

Thực hiện theo quy trình của nhà cung cấp OIDC mục tiêu, và ghi lại các giá trị ID client OIDC và secret. URL của issuer cũng sẽ được yêu cầu trong các bước tiếp theo. Nếu URI chuyển hướng được yêu cầu trong quá trình thiết lập, hãy nhập một giá trị tạm thời, giá trị này sẽ được thay thế sau khi hoàn tất triển khai.

## Bước 2: Lưu trữ Thông tin Xác thực trong AWS Secrets Manager

1. Truy cập vào AWS Management Console.
2. Điều hướng đến Secrets Manager và chọn "Store a new secret".
3. Chọn "Other type of secrets".
4. Nhập ID khách hàng và mã bí mật khách hàng dưới dạng cặp khóa-giá trị.

   - Khóa: `clientId`, Giá trị: <YOUR_GOOGLE_CLIENT_ID>
   - Khóa: `clientSecret`, Giá trị: <YOUR_GOOGLE_CLIENT_SECRET>
   - Khóa: `issuerUrl`, Giá trị: <ISSUER_URL_OF_THE_PROVIDER>

5. Làm theo các bước để đặt tên và mô tả secret. Ghi nhớ tên secret vì bạn sẽ cần nó trong mã CDK của mình (Được sử dụng trong tên biến Bước 3 <YOUR_SECRET_NAME>).
6. Xem xét và lưu trữ secret.

### Lưu ý

Tên các khóa phải khớp chính xác với các chuỗi `clientId`, `clientSecret` và `issuerUrl`.

## Bước 3: Cập nhật cdk.json

Trong tệp cdk.json của bạn, thêm ID Provider và SecretName vào tệp cdk.json.

như sau:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Không thay đổi
        "serviceName": "<YOUR_SERVICE_NAME>", // Đặt bất kỳ giá trị nào bạn muốn
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Lưu ý

#### Tính duy nhất

`userPoolDomainPrefix` phải là duy nhất trên toàn cầu trong tất cả người dùng Amazon Cognito. Nếu bạn chọn một tiền tố đã được sử dụng bởi một tài khoản AWS khác, việc tạo domain user pool sẽ thất bại. Một cách làm tốt là nên bao gồm các định danh, tên dự án hoặc tên môi trường trong tiền tố để đảm bảo tính duy nhất.

## Bước 4: Triển khai Stack CDK

Triển khai stack CDK của bạn lên AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Bước 5: Cập nhật OIDC Client với các URI Chuyển hướng của Cognito

Sau khi triển khai stack, `AuthApprovedRedirectURI` sẽ hiển thị trong phần đầu ra của CloudFormation. Quay lại cấu hình OIDC của bạn và cập nhật với các URI chuyển hướng chính xác.