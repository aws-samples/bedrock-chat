<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)

Một nền tảng AI sinh thành đa ngôn ngữ được hỗ trợ bởi [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Hỗ trợ trò chuyện, bot tùy chỉnh với kiến thức (RAG), chia sẻ bot thông qua cửa hàng bot và tự động hóa tác vụ bằng các tác nhân.

![](./imgs/demo.gif)

> [!Cảnh báo]
>
> **Phiên bản V3 đã phát hành. Để cập nhật, vui lòng xem kỹ [hướng dẫn di chuyển](./migration/V2_TO_V3_vi-VN.md).** Nếu không cẩn thận, **CÁC BOT TỪ V2 SẼ TRỞ NÊN KHÔNG SỬ DỤNG ĐƯỢC.**

### Cá nhân hóa Bot / Cửa hàng Bot

Thêm hướng dẫn và kiến thức của riêng bạn (còn gọi là [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Bot có thể được chia sẻ giữa các người dùng ứng dụng thông qua cửa hàng bot. Bot được tùy chỉnh cũng có thể được xuất bản dưới dạng API độc lập (Xem [chi tiết](./PUBLISH_API_vi-VN.md)).

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Bạn cũng có thể nhập [Cơ sở Kiến thức của Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/) hiện có.

![](./imgs/import_existing_kb.png)

</details>

> [!Quan trọng]
> Vì lý do quản trị, chỉ những người dùng được phép mới có thể tạo bot tùy chỉnh. Để cho phép tạo bot tùy chỉnh, người dùng phải là thành viên của nhóm có tên `CreatingBotAllowed`, có thể được thiết lập thông qua bảng điều khiển quản lý > Nhóm người dùng Amazon Cognito hoặc aws cli. Lưu ý rằng ID nhóm người dùng có thể được tham chiếu bằng cách truy cập CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Các tính năng quản trị

Quản lý API, Đánh dấu bot là thiết yếu, Phân tích việc sử dụng bot. [chi tiết](./ADMINISTRATOR_vi-VN.md)

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Tác nhân

Bằng cách sử dụng [Chức năng Tác nhân](./AGENT_vi-VN.md), chatbot của bạn có thể tự động xử lý các tác vụ phức tạp hơn. Ví dụ: để trả lời câu hỏi của người dùng, Tác nhân có thể truy xuất thông tin cần thiết từ các công cụ bên ngoài hoặc chia nhỏ tác vụ thành nhiều bước để xử lý.

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Triển Khai Siêu Dễ Dàng

- Trong khu vực us-east-1, mở [Truy cập Mô hình Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Quản lý truy cập mô hình` > Chọn tất cả các mô hình bạn muốn sử dụng và sau đó `Lưu thay đổi`.

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/model_screenshot.png)

</details>

- Mở [CloudShell](https://console.aws.amazon.com/cloudshell/home) tại khu vực bạn muốn triển khai
- Chạy triển khai thông qua các lệnh sau. Nếu bạn muốn chỉ định phiên bản để triển khai hoặc cần áp dụng các chính sách bảo mật, vui lòng chỉ định các tham số thích hợp từ [Các Tham Số Tùy Chọn](#các-tham-số-tùy-chọn).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Bạn sẽ được hỏi liệu đây là người dùng mới hay sử dụng v3. Nếu bạn không phải là người dùng tiếp tục từ v0, vui lòng nhập `y`.

### Các Tham Số Tùy Chọn

Bạn có thể chỉ định các tham số sau trong quá trình triển khai để tăng cường bảo mật và tùy chỉnh:

- **--disable-self-register**: Vô hiệu hóa đăng ký tự động (mặc định: được kích hoạt). Nếu cờ này được đặt, bạn sẽ cần tạo tất cả người dùng trên cognito và sẽ không cho phép người dùng tự đăng ký tài khoản.
- **--enable-lambda-snapstart**: Bật [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (mặc định: vô hiệu). Nếu cờ này được đặt, sẽ cải thiện thời gian khởi động lạnh cho các hàm Lambda, mang lại thời gian phản hồi nhanh hơn để có trải nghiệm người dùng tốt hơn.
- **--ipv4-ranges**: Danh sách các phạm vi IPv4 được phép, phân tách bằng dấu phẩy. (mặc định: cho phép tất cả các địa chỉ ipv4)
- **--ipv6-ranges**: Danh sách các phạm vi IPv6 được phép, phân tách bằng dấu phẩy. (mặc định: cho phép tất cả các địa chỉ ipv6)
- **--disable-ipv6**: Vô hiệu hóa kết nối qua IPv6. (mặc định: được kích hoạt)
- **--allowed-signup-email-domains**: Danh sách các miền email được phép đăng ký, phân tách bằng dấu phẩy. (mặc định: không hạn chế miền)
- **--bedrock-region**: Xác định khu vực nơi Bedrock có sẵn. (mặc định: us-east-1)
- **--repo-url**: Kho lưu trữ tùy chỉnh của Bedrock Chat để triển khai, nếu đã fork hoặc nguồn điều khiển tùy chỉnh. (mặc định: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: Phiên bản của Bedrock Chat để triển khai. (mặc định: phiên bản mới nhất trong quá trình phát triển)
- **--cdk-json-override**: Bạn có thể ghi đè bất kỳ giá trị ngữ cảnh CDK nào trong quá trình triển khai bằng cách sử dụng khối JSON ghi đè. Điều này cho phép bạn sửa đổi cấu hình mà không cần chỉnh sửa trực tiếp tệp cdk.json.

Ví dụ sử dụng:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

JSON ghi đè phải tuân theo cùng cấu trúc như cdk.json. Bạn có thể ghi đè bất kỳ giá trị ngữ cảnh nào bao gồm:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- Và các giá trị ngữ cảnh khác được định nghĩa trong cdk.json

> [!Lưu ý]
> Các giá trị ghi đè sẽ được hợp nhất với cấu hình cdk.json hiện tại trong thời gian xây dựng mã AWS. Các giá trị được chỉ định trong phần ghi đè sẽ có ưu tiên cao hơn so với các giá trị trong cdk.json.

#### Ví dụ lệnh với các tham số:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Sau khoảng 35 phút, bạn sẽ nhận được đầu ra sau, mà bạn có thể truy cập từ trình duyệt của mình

```
URL Frontend: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Màn hình đăng ký sẽ xuất hiện như ở trên, nơi bạn có thể đăng ký email và đăng nhập.

> [!Quan Trọng]
> Nếu không đặt tham số tùy chọn, phương pháp triển khai này cho phép bất kỳ ai biết URL đều có thể đăng ký. Đối với việc sử dụng trong sản xuất, rất khuyến nghị thêm các hạn chế địa chỉ IP và vô hiệu hóa đăng ký tự động để giảm thiểu các rủi ro bảo mật (bạn có thể xác định allowed-signup-email-domains để hạn chế người dùng sao cho chỉ các địa chỉ email từ miền công ty của bạn mới được phép đăng ký). Sử dụng cả ipv4-ranges và ipv6-ranges để hạn chế địa chỉ IP, và vô hiệu hóa đăng ký tự động bằng cách sử dụng disable-self-register khi thực thi ./bin.

> [!MẸO]
> Nếu `URL Frontend` không xuất hiện hoặc Bedrock Chat không hoạt động đúng, có thể là do vấn đề với phiên bản mới nhất. Trong trường hợp này, vui lòng thêm `--version "v3.0.0"` vào các tham số và thử triển khai lại.

## Kiến trúc

Đây là kiến trúc được xây dựng trên các dịch vụ được quản lý của AWS, loại bỏ nhu cầu quản lý cơ sở hạ tầng. Sử dụng Amazon Bedrock, không cần giao tiếp với các API bên ngoài AWS. Điều này cho phép triển khai các ứng dụng có khả năng mở rộng, đáng tin cậy và an toàn.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Cơ sở dữ liệu NoSQL để lưu trữ lịch sử cuộc trò chuyện
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Điểm cuối API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Phân phối ứng dụng frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Hạn chế địa chỉ IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Xác thực người dùng
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Dịch vụ được quản lý để sử dụng các mô hình nền tảng thông qua API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Cung cấp giao diện được quản lý cho Truy xuất-Tăng cường Sinh thành ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), cung cấp các dịch vụ để nhúng và phân tích tài liệu
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Nhận sự kiện từ luồng DynamoDB và khởi chạy Step Functions để nhúng kiến thức bên ngoài
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Điều phối quy trình nhập để nhúng kiến thức bên ngoài vào Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Phục vụ như cơ sở dữ liệu backend cho Bedrock Knowledge Bases, cung cấp khả năng tìm kiếm toàn văn và tìm kiếm vector, cho phép truy xuất thông tin liên quan chính xác
- [Amazon Athena](https://aws.amazon.com/athena/): Dịch vụ truy vấn để phân tích bucket S3

![](./imgs/arch.png)

## Triển khai bằng CDK

Việc Triển khai Siêu dễ dàng sử dụng [AWS CodeBuild](https://aws.amazon.com/codebuild/) để thực hiện triển khai CDK nội bộ. Phần này mô tả quy trình triển khai trực tiếp bằng CDK.

- Vui lòng chuẩn bị môi trường UNIX, Docker và môi trường chạy Node.js. Nếu không, bạn cũng có thể sử dụng [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Quan trọng]
> Nếu không gian lưu trữ trong môi trường cục bộ không đủ trong quá trình triển khai, việc CDK bootstrapping có thể dẫn đến lỗi. Nếu bạn đang chạy trên Cloud9 v.v., chúng tôi khuyến nghị mở rộng kích thước volume của instance trước khi triển khai.

- Sao chép kho lưu trữ này

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Cài đặt các gói npm

```
cd bedrock-chat
cd cdk
npm ci
```

- Nếu cần, hãy chỉnh sửa các mục sau trong [cdk.json](./cdk/cdk.json) nếu cần.

  - `bedrockRegion`: Khu vực có sẵn Bedrock. **LƯU Ý: Bedrock KHÔNG hỗ trợ tất cả các khu vực vào lúc này.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Phạm vi địa chỉ IP được phép.
  - `enableLambdaSnapStart`: Mặc định là true. Đặt thành false nếu triển khai tại [khu vực không hỗ trợ Lambda SnapStart cho các hàm Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Trước khi triển khai CDK, bạn sẽ cần thực hiện Bootstrap một lần cho khu vực bạn đang triển khai.

```
npx cdk bootstrap
```

- Triển khai dự án mẫu này

```
npx cdk deploy --require-approval never --all
```

- Bạn sẽ nhận được đầu ra tương tự như sau. URL của ứng dụng web sẽ được xuất ra trong `BedrockChatStack.FrontendURL`, vì vậy vui lòng truy cập từ trình duyệt của bạn.

```sh
 ✅  BedrockChatStack

✨  Thời gian triển khai: 78.57s

Đầu ra:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Xác định Tham số

Bạn có thể xác định các tham số cho việc triển khai của mình theo hai cách: sử dụng `cdk.json` hoặc sử dụng tệp `parameter.ts` an toàn về kiểu.

#### Sử dụng cdk.json (Phương pháp Truyền thống)

Cách truyền thống để cấu hình các tham số là chỉnh sửa tệp `cdk.json`. Phương pháp này đơn giản nhưng thiếu kiểm tra kiểu:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Sử dụng parameter.ts (Phương pháp An toàn về Kiểu Được Khuyến nghị)

Để có tính an toàn về kiểu và trải nghiệm nhà phát triển tốt hơn, bạn có thể sử dụng tệp `parameter.ts` để xác định các tham số của mình:

```typescript
// Xác định các tham số cho môi trường mặc định
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Xác định các tham số cho các môi trường bổ sung
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Tiết kiệm chi phí cho môi trường phát triển
  enableBotStoreReplicas: false, // Tiết kiệm chi phí cho môi trường phát triển
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Tăng tính khả dụng cho sản xuất
  enableBotStoreReplicas: true, // Tăng tính khả dụng cho sản xuất
});
```

> [!Ghi chú]
> Người dùng hiện tại có thể tiếp tục sử dụng `cdk.json` mà không cần thay đổi. Phương pháp `parameter.ts` được khuyến nghị cho các triển khai mới hoặc khi bạn cần quản lý nhiều môi trường.

### Triển khai Nhiều Môi trường

Bạn có thể triển khai nhiều môi trường từ cùng một codebase bằng cách sử dụng tệp `parameter.ts` và tùy chọn `-c envName`.

#### Điều kiện Tiên quyết

1. Xác định các môi trường của bạn trong `parameter.ts` như đã hiển thị ở trên
2. Mỗi môi trường sẽ có bộ tài nguyên riêng với các tiền tố cụ thể của môi trường

#### Lệnh Triển khai

Để triển khai một môi trường cụ thể:

```bash
# Triển khai môi trường dev
npx cdk deploy --all -c envName=dev

# Triển khai môi trường prod
npx cdk deploy --all -c envName=prod
```

Nếu không có môi trường nào được chỉ định, môi trường "default" sẽ được sử dụng:

```bash
# Triển khai môi trường mặc định
npx cdk deploy --all
```

#### Lưu ý Quan trọng

1. **Đặt tên Ngăn xếp**:

   - Các ngăn xếp chính cho mỗi môi trường sẽ được thêm tiền tố tên môi trường (ví dụ: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Tuy nhiên, các ngăn xếp bot tùy chỉnh (`BrChatKbStack*`) và các ngăn xếp xuất bản API (`ApiPublishmentStack*`) sẽ không nhận các tiền tố môi trường vì chúng được tạo động tại thời điểm chạy

2. **Đặt tên Tài nguyên**:

   - Chỉ một số tài nguyên nhận các tiền tố môi trường trong tên của chúng (ví dụ: bảng `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Hầu hết các tài nguyên giữ nguyên tên của chúng nhưng được cô lập bằng cách nằm trong các ngăn xếp khác nhau

3. **Nhận dạng Môi trường**:

   - Tất cả các tài nguyên được gắn thẻ với thẻ `CDKEnvironment` chứa tên môi trường
   - Bạn có thể sử dụng thẻ này để xác định tài nguyên thuộc môi trường nào
   - Ví dụ: `CDKEnvironment: dev` hoặc `CDKEnvironment: prod`

4. **Ghi đè Môi trường Mặc định**: Nếu bạn xác định môi trường "default" trong `parameter.ts`, nó sẽ ghi đè các cài đặt trong `cdk.json`. Để tiếp tục sử dụng `cdk.json`, đừng xác định môi trường "default" trong `parameter.ts`.

5. **Yêu cầu Môi trường**: Để tạo các môi trường khác ngoài "default", bạn phải sử dụng `parameter.ts`. Tùy chọn `-c envName` một mình là không đủ nếu không có các định nghĩa môi trường tương ứng.

6. **Cô lập Tài nguyên**: Mỗi môi trường tạo bộ tài nguyên riêng của mình, cho phép bạn có các môi trường phát triển, thử nghiệm và sản xuất trong cùng một tài khoản AWS mà không có xung đột.

## Những Điều Khác

Bạn có thể xác định các tham số cho việc triển khai của mình theo hai cách: sử dụng `cdk.json` hoặc sử dụng tệp `parameter.ts` an toàn về kiểu.

#### Sử Dụng cdk.json (Phương Pháp Truyền Thống)

Cách truyền thống để cấu hình các tham số là chỉnh sửa tệp `cdk.json`. Phương pháp này đơn giản nhưng thiếu kiểm tra kiểu:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Sử Dụng parameter.ts (Phương Pháp An Toàn Về Kiểu Được Khuyến Nghị)

Để có được tính an toàn về kiểu và trải nghiệm phát triển tốt hơn, bạn có thể sử dụng tệp `parameter.ts` để xác định các tham số của mình:

```typescript
// Xác định các tham số cho môi trường mặc định
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Xác định các tham số cho các môi trường bổ sung
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Tiết kiệm chi phí cho môi trường dev
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Tăng tính sẵn sàng cho môi trường sản xuất
});
```

> [!Ghi Chú]
> Người dùng hiện tại có thể tiếp tục sử dụng `cdk.json` mà không cần thay đổi. Phương pháp `parameter.ts` được khuyến nghị cho các triển khai mới hoặc khi bạn cần quản lý nhiều môi trường.

### Triển Khai Nhiều Môi Trường

Bạn có thể triển khai nhiều môi trường từ cùng một cơ sở mã sử dụng tệp `parameter.ts` và tùy chọn `-c envName`.

#### Điều Kiện Tiên Quyết

1. Xác định các môi trường của bạn trong `parameter.ts` như đã hiển thị ở trên
2. Mỗi môi trường sẽ có bộ tài nguyên riêng với các tiền tố đặc thù cho môi trường

#### Lệnh Triển Khai

Để triển khai một môi trường cụ thể:

```bash
# Triển khai môi trường dev
npx cdk deploy --all -c envName=dev

# Triển khai môi trường prod
npx cdk deploy --all -c envName=prod
```

Nếu không có môi trường nào được chỉ định, môi trường "default" sẽ được sử dụng:

```bash
# Triển khai môi trường mặc định
npx cdk deploy --all
```

#### Ghi Chú Quan Trọng

1. **Đặt Tên Ngăn Xếp**:

   - Các ngăn xếp chính cho mỗi môi trường sẽ được thêm tiền tố là tên môi trường (ví dụ: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Tuy nhiên, các ngăn xếp bot tùy chỉnh (`BrChatKbStack*`) và các ngăn xếp xuất bản API (`ApiPublishmentStack*`) sẽ không nhận các tiền tố môi trường vì chúng được tạo động tại thời điểm chạy

2. **Đặt Tên Tài Nguyên**:

   - Chỉ một số tài nguyên nhận các tiền tố môi trường trong tên của chúng (ví dụ: bảng `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Hầu hết các tài nguyên giữ nguyên tên của chúng nhưng được cô lập bằng cách nằm trong các ngăn xếp khác nhau

3. **Nhận Dạng Môi Trường**:

   - Tất cả các tài nguyên được gắn thẻ với thẻ `CDKEnvironment` chứa tên môi trường
   - Bạn có thể sử dụng thẻ này để xác định tài nguyên thuộc về môi trường nào
   - Ví dụ: `CDKEnvironment: dev` hoặc `CDKEnvironment: prod`

4. **Ghi Đè Môi Trường Mặc Định**: Nếu bạn xác định môi trường "default" trong `parameter.ts`, nó sẽ ghi đè các cài đặt trong `cdk.json`. Để tiếp tục sử dụng `cdk.json`, đừng xác định môi trường "default" trong `parameter.ts`.

5. **Yêu Cầu Môi Trường**: Để tạo các môi trường khác ngoài "default", bạn phải sử dụng `parameter.ts`. Tùy chọn `-c envName` một mình là không đủ nếu không có các định nghĩa môi trường tương ứng.

6. **Cô Lập Tài Nguyên**: Mỗi môi trường tạo bộ tài nguyên riêng của mình, cho phép bạn có các môi trường phát triển, thử nghiệm và sản xuất trong cùng một tài khoản AWS mà không có xung đột.

## Các mục khác

### Gỡ bỏ tài nguyên

Nếu sử dụng CLI và CDK, vui lòng sử dụng `npx cdk destroy`. Nếu không, truy cập [CloudFormation](https://console.aws.amazon.com/cloudformation/home) và xóa `BedrockChatStack` và `FrontendWafStack` theo cách thủ công. Lưu ý rằng `FrontendWafStack` nằm ở khu vực `us-east-1`.

### Cài đặt Ngôn ngữ

Tài sản này tự động phát hiện ngôn ngữ bằng cách sử dụng [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Bạn có thể chuyển đổi ngôn ngữ từ menu ứng dụng. Ngoài ra, bạn có thể sử dụng Query String để đặt ngôn ngữ như sau.

> `https://example.com?lng=ja`

### Vô hiệu hóa đăng ký tự động

Mẫu này mặc định cho phép đăng ký tự động. Để vô hiệu hóa đăng ký tự động, hãy mở [cdk.json](./cdk/cdk.json) và chuyển `selfSignUpEnabled` thành `false`. Nếu bạn cấu hình [nhà cung cấp danh tính bên ngoài](#external-identity-provider), giá trị sẽ bị bỏ qua và tự động bị vô hiệu hóa.

### Hạn chế Tên miền cho Địa chỉ Email Đăng ký

Theo mặc định, mẫu này không hạn chế tên miền cho các địa chỉ email đăng ký. Để chỉ cho phép đăng ký từ các tên miền cụ thể, hãy mở `cdk.json` và chỉ định các tên miền dưới dạng danh sách trong `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Nhà cung cấp Danh tính Bên ngoài

Mẫu này hỗ trợ nhà cung cấp danh tính bên ngoài. Hiện tại chúng tôi hỗ trợ [Google](./idp/SET_UP_GOOGLE_vi-VN.md) và [nhà cung cấp OIDC tùy chỉnh](./idp/SET_UP_CUSTOM_OIDC_vi-VN.md).

### Tự động thêm người dùng mới vào nhóm

Mẫu này có các nhóm sau để cấp quyền cho người dùng:

- [`Admin`](./ADMINISTRATOR_vi-VN.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_vi-VN.md)

Nếu bạn muốn người dùng mới được tạo tự động gia nhập các nhóm, bạn có thể chỉ định chúng trong [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Theo mặc định, người dùng mới được tạo sẽ được thêm vào nhóm `CreatingBotAllowed`.

### Cấu hình Bản sao RAG

`enableRagReplicas` là một tùy chọn trong [cdk.json](./cdk/cdk.json) điều khiển cài đặt bản sao cho cơ sở dữ liệu RAG, cụ thể là Cơ sở Kiến thức sử dụng Amazon OpenSearch Serverless.

- **Mặc định**: true
- **true**: Tăng tính sẵn sàng bằng cách kích hoạt các bản sao bổ sung, phù hợp cho môi trường sản xuất nhưng tăng chi phí.
- **false**: Giảm chi phí bằng cách sử dụng ít bản sao hơn, phù hợp cho phát triển và thử nghiệm.

Đây là cài đặt cấp tài khoản/khu vực, ảnh hưởng đến toàn bộ ứng dụng thay vì các bot riêng lẻ.

> [!Lưu ý]
> Tính đến tháng 6 năm 2024, Amazon OpenSearch Serverless hỗ trợ 0.5 OCU, giảm chi phí đầu vào cho các khối lượng công việc quy mô nhỏ. Các triển khai sản xuất có thể bắt đầu với 2 OCU, trong khi các khối lượng công việc phát triển/thử nghiệm có thể sử dụng 1 OCU. OpenSearch Serverless tự động mở rộng quy mô dựa trên nhu cầu công việc. Để biết thêm chi tiết, hãy truy cập [thông báo](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Cấu hình Cửa hàng Bot

Tính năng cửa hàng bot cho phép người dùng chia sẻ và khám phá các bot tùy chỉnh. Bạn có thể cấu hình cửa hàng bot thông qua các cài đặt sau trong [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Điều khiển việc bật tính năng cửa hàng bot (mặc định: `true`)
- **botStoreLanguage**: Đặt ngôn ngữ chính cho tìm kiếm và khám phá bot (mặc định: `"en"`). Điều này ảnh hưởng đến cách bot được lập chỉ mục và tìm kiếm trong cửa hàng bot, tối ưu hóa phân tích văn bản cho ngôn ngữ được chỉ định.
- **enableBotStoreReplicas**: Điều khiển việc bật bản sao chế độ chờ cho bộ sưu tập OpenSearch Serverless được sử dụng bởi cửa hàng bot (mặc định: `false`). Đặt giá trị thành `true` sẽ cải thiện tính sẵn sàng nhưng tăng chi phí, còn `false` sẽ giảm chi phí nhưng có thể ảnh hưởng đến tính sẵn sàng.
  > **Quan trọng**: Bạn không thể cập nhật thuộc tính này sau khi bộ sưu tập đã được tạo. Nếu bạn cố gắng sửa đổi thuộc tính này, bộ sưu tập sẽ tiếp tục sử dụng giá trị ban đầu.

### Suy luận liên vùng

[Suy luận liên vùng](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) cho phép Amazon Bedrock định tuyến động các yêu cầu suy luận mô hình trên nhiều khu vực AWS, tăng cường thông lượng và khả năng phục hồi trong các giai đoạn nhu cầu cao điểm. Để cấu hình, hãy chỉnh sửa `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) cải thiện thời gian khởi động lạnh cho các hàm Lambda, cung cấp thời gian phản hồi nhanh hơn để mang lại trải nghiệm người dùng tốt hơn. Mặt khác, đối với các hàm Python, có [khoản phí phụ thuộc vào kích thước bộ nhớ đệm](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) và [không khả dụng ở một số khu vực](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) hiện tại. Để vô hiệu hóa SnapStart, hãy chỉnh sửa `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Cấu hình Tên miền Tùy chỉnh

Bạn có thể cấu hình tên miền tùy chỉnh cho bản phân phối CloudFront bằng cách đặt các tham số sau trong [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Tên miền tùy chỉnh cho ứng dụng trò chuyện của bạn (ví dụ: chat.example.com)
- `hostedZoneId`: ID của vùng được lưu trữ Route 53 nơi các bản ghi DNS sẽ được tạo

Khi các tham số này được cung cấp, việc triển khai sẽ tự động:

- Tạo chứng chỉ ACM với xác thực DNS ở khu vực us-east-1
- Tạo các bản ghi DNS cần thiết trong vùng Route 53 của bạn
- Cấu hình CloudFront để sử dụng tên miền tùy chỉnh của bạn

> [!Lưu ý]
> Tên miền phải được quản lý bởi Route 53 trong tài khoản AWS của bạn. ID vùng được lưu trữ có thể được tìm thấy trong bảng điều khiển Route 53.

### Phát triển Cục bộ

Xem [PHÁT TRIỂN CỤC BỘ](./LOCAL_DEVELOPMENT_vi-VN.md).

### Đóng góp

Cảm ơn bạn đã cân nhắc đóng góp cho kho lưu trữ này! Chúng tôi chào đón các bản sửa lỗi, bản dịch ngôn ngữ (i18n), cải tiến tính năng, [công cụ đại lý](./docs/AGENT.md#how-to-develop-your-own-tools) và các cải tiến khác.

Đối với các cải tiến tính năng và các cải tiến khác, **trước khi tạo Pull Request, chúng tôi rất mong bạn có thể tạo một Issue Yêu cầu Tính năng để thảo luận về phương pháp và chi tiết triển khai. Đối với các bản sửa lỗi và bản dịch ngôn ngữ (i18n), hãy tiến hành tạo Pull Request trực tiếp.**

Vui lòng cũng xem xét các hướng dẫn sau trước khi đóng góp:

- [Phát triển Cục bộ](./LOCAL_DEVELOPMENT_vi-VN.md)
- [ĐÓNG GÓP](./CONTRIBUTING_vi-VN.md)

## Danh bạ

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Những Đóng Góp Viên Nổi Bật

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Những người đóng góp

[![những người đóng góp bedrock chat](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Giấy Phép

Thư viện này được cấp phép theo Giấy Phép MIT-0. Xem [tệp LICENSE](./LICENSE).