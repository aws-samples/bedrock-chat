# Thiết lập nhà cung cấp danh tính bên ngoài

## Bước 1: Tạo Ứng dụng Khách OIDC

Thực hiện các thủ tục cho nhà cung cấp OIDC mục tiêu và ghi chú các giá trị cho ID ứng dụng khách OIDC và bí mật. URL phát hành cũng được yêu cầu trong các bước sau. Nếu URI chuyển hướng được yêu cầu trong quá trình thiết lập, hãy nhập giá trị giả, sau đó sẽ được thay thế sau khi triển khai hoàn tất.

## Bước 2: Lưu Thông Tin Đăng Nhập trong AWS Secrets Manager

1. Truy cập vào AWS Management Console.
2. Điều hướng đến Secrets Manager và chọn "Lưu trữ bí mật mới".
3. Chọn "Loại bí mật khác".
4. Nhập client ID và client secret dưới dạng các cặp khóa-giá trị.

   - Khóa: `clientId`, Giá trị: <YOUR_GOOGLE_CLIENT_ID>
   - Khóa: `clientSecret`, Giá trị: <YOUR_GOOGLE_CLIENT_SECRET>
   - Khóa: `issuerUrl`, Giá trị: <ISSUER_URL_OF_THE_PROVIDER>

5. Làm theo các lời nhắc để đặt tên và mô tả bí mật. Ghi chú tên bí mật vì bạn sẽ cần nó trong mã CDK (Được sử dụng trong biến tên <YOUR_SECRET_NAME> của Bước 3).
6. Xem lại và lưu trữ bí mật.

### Lưu Ý

Các tên khóa phải chính xác khớp với các chuỗi `clientId`, `clientSecret` và `issuerUrl`.

## Bước 3: Cập nhật cdk.json

Trong tệp cdk.json của bạn, hãy thêm ID Provider và SecretName vào tệp cdk.json.

như sau:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Không thay đổi
        "serviceName": "<TÊN_DỊCH_VỤ_CỦA_BẠN>", // Đặt bất kỳ giá trị nào bạn muốn
        "secretName": "<TÊN_BÍ_MẬT_CỦA_BẠN>"
      }
    ],
    "userPoolDomainPrefix": "<TIỀN_TỐ_MIỀN_DUY_NHẤT_CHO_USER_POOL_CỦA_BẠN>"
  }
}
```

### Lưu ý

#### Tính Duy Nhất

`userPoolDomainPrefix` phải là duy nhất trên toàn cầu đối với tất cả người dùng Amazon Cognito. Nếu bạn chọn một tiền tố đã được sử dụng bởi một tài khoản AWS khác, việc tạo miền user pool sẽ thất bại. Là một thực hành tốt, hãy bao gồm các định danh, tên dự án hoặc tên môi trường trong tiền tố để đảm bảo tính duy nhất.

## Bước 4: Triển Khai Stack CDK

Triển khai stack CDK của bạn lên AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Bước 5: Cập Nhật Client OIDC với URI Chuyển Hướng của Cognito

Sau khi triển khai stack, `AuthApprovedRedirectURI` sẽ hiển thị trong các kết quả của CloudFormation. Hãy quay lại cấu hình OIDC của bạn và cập nhật các URI chuyển hướng chính xác.