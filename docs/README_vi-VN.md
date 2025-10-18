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


Một nền tảng AI tạo sinh đa ngôn ngữ được hỗ trợ bởi [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Hỗ trợ trò chuyện, bot tùy chỉnh với kiến thức (RAG), chia sẻ bot thông qua cửa hàng bot và tự động hóa tác vụ bằng tác nhân.

![](./imgs/demo.gif)

> [!Warning]
>
> **Đã phát hành V3. Để cập nhật, vui lòng xem kỹ [hướng dẫn di chuyển](./migration/V2_TO_V3_vi-VN.md).** Nếu không cẩn thận, **CÁC BOT TỪ V2 SẼ TRỞ NÊN KHÔNG SỬ DỤNG ĐƯỢC.**

### Tùy chỉnh Bot / Cửa hàng Bot

Thêm hướng dẫn và kiến thức riêng của bạn (còn gọi là [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Bot có thể được chia sẻ giữa người dùng ứng dụng thông qua thị trường cửa hàng bot. Bot đã tùy chỉnh cũng có thể được xuất bản dưới dạng API độc lập (Xem [chi tiết](./PUBLISH_API_vi-VN.md)).

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Bạn cũng có thể nhập [Amazon Bedrock's KnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/) hiện có.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> Vì lý do quản trị, chỉ những người dùng được phép mới có thể tạo bot tùy chỉnh. Để cho phép tạo bot tùy chỉnh, người dùng phải là thành viên của nhóm có tên `CreatingBotAllowed`, có thể được thiết lập thông qua bảng điều khiển quản lý > Amazon Cognito User pools hoặc aws cli. Lưu ý rằng id của user pool có thể được tham chiếu bằng cách truy cập CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Tính năng quản trị

Quản lý API, Đánh dấu bot là thiết yếu, Phân tích việc sử dụng bot. [chi tiết](./ADMINISTRATOR_vi-VN.md)

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Tác nhân

Bằng cách sử dụng [chức năng Tác nhân](./AGENT_vi-VN.md), chatbot của bạn có thể tự động xử lý các tác vụ phức tạp hơn. Ví dụ, để trả lời câu hỏi của người dùng, Tác nhân có thể truy xuất thông tin cần thiết từ các công cụ bên ngoài hoặc chia nhỏ tác vụ thành nhiều bước để xử lý.

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Triển khai Siêu đơn giản

- Trong vùng us-east-1, mở [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > Chọn tất cả các model bạn muốn sử dụng rồi `Save changes`.

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/model_screenshot.png)

</details>

### Các vùng được hỗ trợ

Hãy đảm bảo rằng bạn triển khai Bedrock Chat trong một vùng [nơi có sẵn OpenSearch Serverless và API Ingestion](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html), nếu bạn muốn sử dụng bot và tạo cơ sở kiến thức (OpenSearch Serverless là lựa chọn mặc định). Tính đến tháng 8 năm 2025, các vùng sau được hỗ trợ: us-east-1, us-east-2, us-west-1, us-west-2, ap-south-1, ap-northeast-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-south-2, eu-north-1, sa-east-1

Đối với tham số **bedrock-region**, bạn cần chọn một vùng [nơi có sẵn Bedrock](https://docs.aws.amazon.com/general/latest/gr/bedrock.html).

- Mở [CloudShell](https://console.aws.amazon.com/cloudshell/home) tại vùng bạn muốn triển khai
- Chạy triển khai bằng các lệnh sau. Nếu bạn muốn chỉ định phiên bản để triển khai hoặc cần áp dụng chính sách bảo mật, vui lòng chỉ định các tham số thích hợp từ [Tham số Tùy chọn](#optional-parameters).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Bạn sẽ được hỏi nếu là người dùng mới hoặc đang sử dụng v3. Nếu bạn không phải là người dùng tiếp tục từ v0, vui lòng nhập `y`.

### Tham số Tùy chọn

Bạn có thể chỉ định các tham số sau trong quá trình triển khai để tăng cường bảo mật và tùy chỉnh:

- **--disable-self-register**: Vô hiệu hóa tự đăng ký (mặc định: đã bật). Nếu cờ này được đặt, bạn sẽ cần tạo tất cả người dùng trên cognito và nó sẽ không cho phép người dùng tự đăng ký tài khoản của họ.
- **--enable-lambda-snapstart**: Bật [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (mặc định: đã tắt). Nếu cờ này được đặt, cải thiện thời gian khởi động lạnh cho các hàm Lambda, cung cấp thời gian phản hồi nhanh hơn để trải nghiệm người dùng tốt hơn.
- **--ipv4-ranges**: Danh sách các dải IPv4 được phép, phân cách bằng dấu phẩy. (mặc định: cho phép tất cả địa chỉ ipv4)
- **--ipv6-ranges**: Danh sách các dải IPv6 được phép, phân cách bằng dấu phẩy. (mặc định: cho phép tất cả địa chỉ ipv6)
- **--disable-ipv6**: Vô hiệu hóa kết nối qua IPv6. (mặc định: đã bật)
- **--allowed-signup-email-domains**: Danh sách các tên miền email được phép đăng ký, phân cách bằng dấu phẩy. (mặc định: không giới hạn tên miền)
- **--bedrock-region**: Xác định vùng nơi có sẵn bedrock. (mặc định: us-east-1)
- **--repo-url**: Repo tùy chỉnh của Bedrock Chat để triển khai, nếu được fork hoặc kiểm soát nguồn tùy chỉnh. (mặc định: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: Phiên bản của Bedrock Chat để triển khai. (mặc định: phiên bản mới nhất trong phát triển)
- **--cdk-json-override**: Bạn có thể ghi đè bất kỳ giá trị ngữ cảnh CDK nào trong quá trình triển khai bằng khối JSON ghi đè. Điều này cho phép bạn sửa đổi cấu hình mà không cần chỉnh sửa trực tiếp tệp cdk.json.

Ví dụ sử dụng:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedCountries": ["US", "CA"],
    "allowedSignUpEmailDomains": ["example.com"],
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ]
  }
}'
```

JSON ghi đè phải tuân theo cùng cấu trúc như cdk.json. Bạn có thể ghi đè bất kỳ giá trị ngữ cảnh nào bao gồm:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: chấp nhận danh sách ID model để bật. Giá trị mặc định là danh sách trống, điều này sẽ bật tất cả các model.
- `logoPath`: đường dẫn tương đối đến tài sản logo trong thư mục `public/` của frontend xuất hiện ở đầu ngăn điều hướng.
- Và các giá trị ngữ cảnh khác được định nghĩa trong cdk.json

> [!Note]
> Các giá trị ghi đè sẽ được hợp nhất với cấu hình cdk.json hiện có trong thời gian triển khai trong AWS code build. Các giá trị được chỉ định trong phần ghi đè sẽ được ưu tiên hơn các giá trị trong cdk.json.

#### Ví dụ lệnh với tham số:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Sau khoảng 35 phút, bạn sẽ nhận được đầu ra sau đây, bạn có thể truy cập từ trình duyệt của mình

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Màn hình đăng ký sẽ xuất hiện như hình trên, nơi bạn có thể đăng ký email và đăng nhập.

> [!Important]
> Nếu không đặt tham số tùy chọn, phương thức triển khai này cho phép bất kỳ ai biết URL đều có thể đăng ký. Đối với việc sử dụng trong sản xuất, chúng tôi khuyến nghị mạnh mẽ nên thêm hạn chế địa chỉ IP và vô hiệu hóa tự đăng ký để giảm thiểu rủi ro bảo mật (bạn có thể xác định allowed-signup-email-domains để hạn chế người dùng sao cho chỉ địa chỉ email từ tên miền công ty của bạn mới có thể đăng ký). Sử dụng cả ipv4-ranges và ipv6-ranges để hạn chế địa chỉ IP, và vô hiệu hóa tự đăng ký bằng cách sử dụng disable-self-register khi thực thi ./bin.

> [!TIP]
> Nếu `Frontend URL` không xuất hiện hoặc Bedrock Chat không hoạt động bình thường, có thể là do vấn đề với phiên bản mới nhất. Trong trường hợp này, vui lòng thêm `--version "v3.0.0"` vào tham số và thử triển khai lại.

## Kiến trúc

Đây là một kiến trúc được xây dựng trên các dịch vụ được quản lý của AWS, loại bỏ nhu cầu quản lý cơ sở hạ tầng. Sử dụng Amazon Bedrock, không cần phải giao tiếp với các API bên ngoài AWS. Điều này cho phép triển khai các ứng dụng có khả năng mở rộng, đáng tin cậy và bảo mật.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Cơ sở dữ liệu NoSQL để lưu trữ lịch sử hội thoại
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Điểm cuối API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Phân phối ứng dụng frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Hạn chế địa chỉ IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Xác thực người dùng
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Dịch vụ được quản lý để sử dụng các mô hình nền tảng thông qua API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Cung cấp giao diện được quản lý cho Tạo sinh Tăng cường bằng Truy xuất ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), cung cấp các dịch vụ nhúng và phân tích tài liệu
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Nhận sự kiện từ luồng DynamoDB và khởi chạy Step Functions để nhúng kiến thức bên ngoài
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Điều phối quy trình tiếp nhận để nhúng kiến thức bên ngoài vào Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Đóng vai trò là cơ sở dữ liệu backend cho Bedrock Knowledge Bases, cung cấp khả năng tìm kiếm toàn văn và tìm kiếm vector, cho phép truy xuất thông tin liên quan một cách chính xác
- [Amazon Athena](https://aws.amazon.com/athena/): Dịch vụ truy vấn để phân tích bucket S3

![](./imgs/arch.png)

## Triển khai bằng CDK

Triển khai Super-easy sử dụng [AWS CodeBuild](https://aws.amazon.com/codebuild/) để thực hiện triển khai bằng CDK nội bộ. Phần này mô tả quy trình triển khai trực tiếp với CDK.

- Vui lòng chuẩn bị môi trường UNIX, Docker và Node.js runtime.

> [!Important]
> Nếu không đủ dung lượng lưu trữ trong môi trường cục bộ trong quá trình triển khai, việc khởi tạo CDK có thể gây ra lỗi. Chúng tôi khuyến nghị mở rộng dung lượng ổ đĩa của instance trước khi triển khai.

- Clone repository này

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Cài đặt các gói npm

```
cd bedrock-chat
cd cdk
npm ci
```

- Nếu cần, hãy chỉnh sửa các mục sau trong [cdk.json](./cdk/cdk.json).

  - `bedrockRegion`: Khu vực có Bedrock khả dụng. **LƯU Ý: Bedrock KHÔNG hỗ trợ tất cả các khu vực hiện tại.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Dải địa chỉ IP được phép.
  - `enableLambdaSnapStart`: Mặc định là true. Đặt thành false nếu triển khai ở [khu vực không hỗ trợ Lambda SnapStart cho hàm Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).
  - `globalAvailableModels`: Mặc định là tất cả. Nếu được đặt (danh sách ID model), cho phép kiểm soát toàn cục các model xuất hiện trong menu thả xuống trong các cuộc trò chuyện cho tất cả người dùng và trong quá trình tạo bot trong ứng dụng Bedrock Chat.
  - `logoPath`: Đường dẫn tương đối trong `frontend/public` trỏ đến hình ảnh hiển thị ở đầu ngăn kéo ứng dụng.
Các ID model sau được hỗ trợ (vui lòng đảm bảo chúng cũng được kích hoạt trong bảng điều khiển Bedrock dưới mục Model access trong khu vực triển khai của bạn):
- **Claude Models:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Amazon Nova Models:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Mistral Models:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **DeepSeek Models:** `deepseek-r1`
- **Meta Llama Models:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

Danh sách đầy đủ có thể được tìm thấy trong [index.ts](./frontend/src/constants/index.ts).

- Trước khi triển khai CDK, bạn cần thực hiện Bootstrap một lần cho khu vực bạn đang triển khai.

```
npx cdk bootstrap
```

- Triển khai dự án mẫu này

```
npx cdk deploy --require-approval never --all
```

- Bạn sẽ nhận được kết quả tương tự như sau. URL của ứng dụng web sẽ được hiển thị trong `BedrockChatStack.FrontendURL`, vui lòng truy cập từ trình duyệt của bạn.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Định nghĩa Tham số

Bạn có thể định nghĩa tham số cho việc triển khai theo hai cách: sử dụng `cdk.json` hoặc sử dụng file `parameter.ts` an toàn về kiểu.

#### Sử dụng cdk.json (Phương pháp Truyền thống)

Cách truyền thống để cấu hình tham số là chỉnh sửa file `cdk.json`. Cách tiếp cận này đơn giản nhưng thiếu kiểm tra kiểu:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true,
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
  }
}
```

#### Sử dụng parameter.ts (Phương pháp An toàn về Kiểu được Khuyến nghị)

Để có trải nghiệm phát triển tốt hơn và an toàn về kiểu, bạn có thể sử dụng file `parameter.ts` để định nghĩa tham số:

```typescript
// Định nghĩa tham số cho môi trường mặc định
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// Định nghĩa tham số cho các môi trường bổ sung
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Tiết kiệm chi phí cho môi trường dev
  enableBotStoreReplicas: false, // Tiết kiệm chi phí cho môi trường dev
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Tăng cường khả năng sẵn sàng cho production
  enableBotStoreReplicas: true, // Tăng cường khả năng sẵn sàng cho production
});
```

> [!Note]
> Người dùng hiện tại có thể tiếp tục sử dụng `cdk.json` mà không cần thay đổi. Cách tiếp cận `parameter.ts` được khuyến nghị cho các triển khai mới hoặc khi bạn cần quản lý nhiều môi trường.

### Triển khai Nhiều Môi trường

Bạn có thể triển khai nhiều môi trường từ cùng một codebase bằng cách sử dụng file `parameter.ts` và tùy chọn `-c envName`.

#### Điều kiện tiên quyết

1. Định nghĩa môi trường của bạn trong `parameter.ts` như đã hiển thị ở trên
2. Mỗi môi trường sẽ có bộ tài nguyên riêng với tiền tố cụ thể cho môi trường đó

#### Lệnh Triển khai

Để triển khai một môi trường cụ thể:

```bash
# Triển khai môi trường dev
npx cdk deploy --all -c envName=dev

# Triển khai môi trường prod
npx cdk deploy --all -c envName=prod
```

Nếu không chỉ định môi trường, môi trường "default" sẽ được sử dụng:

```bash
# Triển khai môi trường mặc định
npx cdk deploy --all
```

#### Lưu ý Quan trọng

1. **Đặt tên Stack**:

   - Các stack chính cho mỗi môi trường sẽ có tiền tố là tên môi trường (ví dụ: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Tuy nhiên, các stack bot tùy chỉnh (`BrChatKbStack*`) và stack xuất bản API (`ApiPublishmentStack*`) không nhận tiền tố môi trường vì chúng được tạo động trong thời gian chạy

2. **Đặt tên Tài nguyên**:

   - Chỉ một số tài nguyên nhận tiền tố môi trường trong tên của chúng (ví dụ: bảng `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Hầu hết các tài nguyên giữ nguyên tên gốc nhưng được cô lập bằng cách nằm trong các stack khác nhau

3. **Nhận dạng Môi trường**:

   - Tất cả tài nguyên được gắn thẻ với thẻ `CDKEnvironment` chứa tên môi trường
   - Bạn có thể sử dụng thẻ này để xác định tài nguyên thuộc môi trường nào
   - Ví dụ: `CDKEnvironment: dev` hoặc `CDKEnvironment: prod`

4. **Ghi đè Môi trường Mặc định**: Nếu bạn định nghĩa môi trường "default" trong `parameter.ts`, nó sẽ ghi đè các cài đặt trong `cdk.json`. Để tiếp tục sử dụng `cdk.json`, đừng định nghĩa môi trường "default" trong `parameter.ts`.

5. **Yêu cầu Môi trường**: Để tạo các môi trường khác ngoài "default", bạn phải sử dụng `parameter.ts`. Chỉ tùy chọn `-c envName` không đủ nếu không có định nghĩa môi trường tương ứng.

6. **Cô lập Tài nguyên**: Mỗi môi trường tạo bộ tài nguyên riêng của nó, cho phép bạn có các môi trường phát triển, kiểm thử và sản xuất trong cùng một tài khoản AWS mà không có xung đột.

## Khác

Bạn có thể định nghĩa các tham số cho việc triển khai theo hai cách: sử dụng `cdk.json` hoặc sử dụng file `parameter.ts` kiểu an toàn.

#### Sử dụng cdk.json (Phương pháp truyền thống)

Cách truyền thống để cấu hình tham số là chỉnh sửa file `cdk.json`. Cách tiếp cận này đơn giản nhưng thiếu kiểm tra kiểu:

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

#### Sử dụng parameter.ts (Phương pháp kiểu an toàn được khuyến nghị)

Để có kiểu an toàn và trải nghiệm phát triển tốt hơn, bạn có thể sử dụng file `parameter.ts` để định nghĩa các tham số:

```typescript
// Define parameters for the default environment
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Define parameters for additional environments
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Cost-saving for dev environment
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Enhanced availability for production
});
```

> [!Note]
> Người dùng hiện tại có thể tiếp tục sử dụng `cdk.json` mà không cần thay đổi gì. Cách tiếp cận `parameter.ts` được khuyến nghị cho các triển khai mới hoặc khi bạn cần quản lý nhiều môi trường.

### Triển khai nhiều môi trường

Bạn có thể triển khai nhiều môi trường từ cùng một mã nguồn bằng cách sử dụng file `parameter.ts` và tùy chọn `-c envName`.

#### Điều kiện tiên quyết

1. Định nghĩa các môi trường của bạn trong `parameter.ts` như đã hiển thị ở trên
2. Mỗi môi trường sẽ có bộ tài nguyên riêng với tiền tố đặc thù cho môi trường đó

#### Lệnh triển khai

Để triển khai một môi trường cụ thể:

```bash
# Deploy the dev environment
npx cdk deploy --all -c envName=dev

# Deploy the prod environment
npx cdk deploy --all -c envName=prod
```

Nếu không chỉ định môi trường, môi trường "default" sẽ được sử dụng:

```bash
# Deploy the default environment
npx cdk deploy --all
```

#### Lưu ý quan trọng

1. **Đặt tên Stack**:

   - Các stack chính cho mỗi môi trường sẽ có tiền tố là tên môi trường (ví dụ: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Tuy nhiên, các stack bot tùy chỉnh (`BrChatKbStack*`) và stack xuất bản API (`ApiPublishmentStack*`) không nhận tiền tố môi trường vì chúng được tạo động trong thời gian chạy

2. **Đặt tên tài nguyên**:

   - Chỉ một số tài nguyên nhận tiền tố môi trường trong tên của chúng (ví dụ: bảng `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Hầu hết các tài nguyên giữ nguyên tên gốc nhưng được cô lập bằng cách nằm trong các stack khác nhau

3. **Nhận dạng môi trường**:

   - Tất cả tài nguyên được gắn thẻ với tag `CDKEnvironment` chứa tên môi trường
   - Bạn có thể sử dụng tag này để xác định tài nguyên thuộc môi trường nào
   - Ví dụ: `CDKEnvironment: dev` hoặc `CDKEnvironment: prod`

4. **Ghi đè môi trường mặc định**: Nếu bạn định nghĩa môi trường "default" trong `parameter.ts`, nó sẽ ghi đè các cài đặt trong `cdk.json`. Để tiếp tục sử dụng `cdk.json`, đừng định nghĩa môi trường "default" trong `parameter.ts`.

5. **Yêu cầu môi trường**: Để tạo các môi trường khác ngoài "default", bạn phải sử dụng `parameter.ts`. Chỉ riêng tùy chọn `-c envName` là không đủ nếu không có định nghĩa môi trường tương ứng.

6. **Cô lập tài nguyên**: Mỗi môi trường tạo bộ tài nguyên riêng của nó, cho phép bạn có các môi trường phát triển, kiểm thử và sản xuất trong cùng một tài khoản AWS mà không có xung đột.

## Khác

### Xóa tài nguyên

Nếu sử dụng cli và CDK, vui lòng chạy `npx cdk destroy`. Nếu không, truy cập [CloudFormation](https://console.aws.amazon.com/cloudformation/home) và xóa thủ công `BedrockChatStack` và `FrontendWafStack`. Lưu ý rằng `FrontendWafStack` nằm ở region `us-east-1`.

### Cài đặt ngôn ngữ

Tài nguyên này tự động phát hiện ngôn ngữ bằng [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Bạn có thể chuyển đổi ngôn ngữ từ menu ứng dụng. Ngoài ra, bạn có thể sử dụng Query String để đặt ngôn ngữ như dưới đây.

> `https://example.com?lng=ja`

### Tắt tính năng tự đăng ký

Mẫu này mặc định cho phép tự đăng ký. Để tắt tính năng tự đăng ký, mở [cdk.json](./cdk/cdk.json) và chuyển `selfSignUpEnabled` thành `false`. Nếu bạn cấu hình [nhà cung cấp danh tính bên ngoài](#external-identity-provider), giá trị này sẽ bị bỏ qua và tự động bị tắt.

### Giới hạn tên miền cho địa chỉ email đăng ký

Mặc định, mẫu này không giới hạn tên miền cho địa chỉ email đăng ký. Để chỉ cho phép đăng ký từ các tên miền cụ thể, mở `cdk.json` và chỉ định các tên miền dưới dạng danh sách trong `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Nhà cung cấp danh tính bên ngoài

Mẫu này hỗ trợ nhà cung cấp danh tính bên ngoài. Hiện tại chúng tôi hỗ trợ [Google](./idp/SET_UP_GOOGLE_vi-VN.md) và [nhà cung cấp OIDC tùy chỉnh](./idp/SET_UP_CUSTOM_OIDC_vi-VN.md).

### WAF Frontend tùy chọn

Đối với các phân phối CloudFront, WebACL của AWS WAF phải được tạo trong khu vực us-east-1. Trong một số tổ chức, việc tạo tài nguyên bên ngoài khu vực chính bị hạn chế bởi chính sách. Trong những môi trường như vậy, việc triển khai CDK có thể thất bại khi cố gắng cung cấp Frontend WAF ở us-east-1.

Để đáp ứng những hạn chế này, stack Frontend WAF là tùy chọn. Khi bị tắt, phân phối CloudFront được triển khai mà không có WebACL. Điều này có nghĩa là bạn sẽ không có kiểm soát cho phép/từ chối IP ở cạnh frontend. Xác thực và tất cả các điều khiển ứng dụng khác tiếp tục hoạt động như bình thường. Lưu ý rằng cài đặt này chỉ ảnh hưởng đến Frontend WAF (phạm vi CloudFront); WAF API đã xuất bản (khu vực) vẫn không bị ảnh hưởng.

Để tắt Frontend WAF, đặt thông số sau trong `parameter.ts` (Phương pháp An toàn về Kiểu được Khuyến nghị):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

Hoặc nếu sử dụng `cdk/cdk.json` cũ, đặt thông số sau:

```json
"enableFrontendWaf": false
```

### Tự động thêm người dùng mới vào nhóm

Mẫu này có các nhóm sau để cấp quyền cho người dùng:

- [`Admin`](./ADMINISTRATOR_vi-VN.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_vi-VN.md)

Nếu bạn muốn người dùng mới được tạo tự động tham gia các nhóm, bạn có thể chỉ định chúng trong [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Theo mặc định, người dùng mới được tạo sẽ được tham gia vào nhóm `CreatingBotAllowed`.

### Cấu hình RAG Replicas

`enableRagReplicas` là một tùy chọn trong [cdk.json](./cdk/cdk.json) kiểm soát cài đặt bản sao cho cơ sở dữ liệu RAG, cụ thể là Knowledge Bases sử dụng Amazon OpenSearch Serverless.

- **Mặc định**: true
- **true**: Nâng cao tính sẵn sàng bằng cách kích hoạt các bản sao bổ sung, phù hợp cho môi trường sản xuất nhưng tăng chi phí.
- **false**: Giảm chi phí bằng cách sử dụng ít bản sao hơn, phù hợp cho phát triển và thử nghiệm.

Đây là cài đặt cấp tài khoản/khu vực, ảnh hưởng đến toàn bộ ứng dụng thay vì từng bot riêng lẻ.

> [!Note]
> Kể từ tháng 6 năm 2024, Amazon OpenSearch Serverless hỗ trợ 0.5 OCU, giảm chi phí ban đầu cho khối lượng công việc quy mô nhỏ. Các triển khai sản xuất có thể bắt đầu với 2 OCU, trong khi khối lượng công việc phát triển/thử nghiệm có thể sử dụng 1 OCU. OpenSearch Serverless tự động mở rộng dựa trên nhu cầu khối lượng công việc. Để biết thêm chi tiết, hãy truy cập [thông báo](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Cấu hình Bot Store

Tính năng bot store cho phép người dùng chia sẻ và khám phá các bot tùy chỉnh. Bạn có thể cấu hình bot store thông qua các cài đặt sau trong [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Kiểm soát việc bật tính năng bot store (mặc định: `true`)
- **botStoreLanguage**: Đặt ngôn ngữ chính cho tìm kiếm và khám phá bot (mặc định: `"en"`). Điều này ảnh hưởng đến cách bot được lập chỉ mục và tìm kiếm trong bot store, tối ưu hóa phân tích văn bản cho ngôn ngữ được chỉ định.
- **enableBotStoreReplicas**: Kiểm soát việc bật các bản sao dự phòng cho bộ sưu tập OpenSearch Serverless được sử dụng bởi bot store (mặc định: `false`). Đặt thành `true` cải thiện tính sẵn sàng nhưng tăng chi phí, trong khi `false` giảm chi phí nhưng có thể ảnh hưởng đến tính sẵn sàng.
  > **Quan trọng**: Bạn không thể cập nhật thuộc tính này sau khi bộ sưu tập đã được tạo. Nếu bạn cố gắng sửa đổi thuộc tính này, bộ sưu tập sẽ tiếp tục sử dụng giá trị ban đầu.

### Suy luận xuyên khu vực và toàn cầu

[Suy luận xuyên khu vực và toàn cầu](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
cho phép Amazon Bedrock định tuyến động các yêu cầu suy luận mô hình qua
nhiều khu vực AWS, nâng cao thông lượng và khả năng phục hồi trong thời kỳ cao điểm.
Suy luận toàn cầu định tuyến các yêu cầu đến khu vực tối ưu dựa trên độ trễ
và tính khả dụng ở bất kỳ đâu trên thế giới, trong khi suy luận xuyên khu vực
định tuyến yêu cầu trong cùng một khu vực AWS, ví dụ, trong US. Một số SCP có
thể hạn chế một hoặc cả hai và do đó bạn có thể cấu hình chúng độc lập. Mặc
định cả hai đều được bật.

Để cấu hình, thay đổi các cài đặt sau trong `cdk.json` hoặc `parameters.ts`:

```json
"enableBedrockGlobalInference": false,
"enableBedrockCrossRegionInference": false,
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) cải thiện thời gian khởi động lạnh cho các hàm Lambda, cung cấp thời gian phản hồi nhanh hơn để trải nghiệm người dùng tốt hơn. Mặt khác, đối với các hàm Python, có [phí tùy thuộc vào kích thước bộ nhớ cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) và [hiện không có sẵn ở một số khu vực](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions). Để tắt SnapStart, chỉnh sửa `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Cấu hình tên miền tùy chỉnh

Bạn có thể cấu hình tên miền tùy chỉnh cho phân phối CloudFront bằng cách đặt các tham số sau trong [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Tên miền tùy chỉnh cho ứng dụng chat của bạn (ví dụ: chat.example.com)
- `hostedZoneId`: ID của hosted zone Route 53 nơi các bản ghi tên miền sẽ được tạo

Khi các tham số này được cung cấp, việc triển khai sẽ tự động:

- Tạo chứng chỉ ACM với xác thực DNS trong khu vực us-east-1
- Tạo các bản ghi DNS cần thiết trong hosted zone Route 53 của bạn
- Cấu hình CloudFront để sử dụng tên miền tùy chỉnh của bạn

> [!Note]
> Tên miền phải được quản lý bởi Route 53 trong tài khoản AWS của bạn. ID hosted zone có thể được tìm thấy trong bảng điều khiển Route 53.

### Cấu hình các quốc gia được phép (giới hạn địa lý)

Bạn có thể hạn chế quyền truy cập vào Bedrock-Chat dựa trên quốc gia mà khách hàng đang truy cập từ đó.
Sử dụng tham số `allowedCountries` trong [cdk.json](./cdk/cdk.json) nhận danh sách [Mã Quốc gia ISO-3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).
Ví dụ, một doanh nghiệp có trụ sở tại New Zealand có thể quyết định rằng chỉ các địa chỉ IP từ New Zealand (NZ) và Australia (AU) có thể truy cập cổng thông tin và tất cả những người khác sẽ bị từ chối truy cập.
Để cấu hình hành vi này, sử dụng cài đặt sau trong [cdk.json](./cdk/cdk.json):

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

Hoặc, sử dụng `parameter.ts` (Phương pháp An toàn về Kiểu được Khuyến nghị):

```ts
// Định nghĩa tham số cho môi trường mặc định
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### Tắt hỗ trợ IPv6

Frontend mặc định nhận cả địa chỉ IP và IPv6. Trong một số trường hợp hiếm
gặp, bạn có thể cần tắt hỗ trợ IPv6 một cách rõ ràng. Để làm điều này, đặt
tham số sau trong [parameter.ts](./cdk/parameter.ts) hoặc tương tự trong [cdk.json](./cdk/cdk.json):

```ts
"enableFrontendIpv6": false
```

Nếu không được đặt, hỗ trợ IPv6 sẽ được bật theo mặc định.

### Phát triển cục bộ

Xem [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_vi-VN.md).

### Đ

## Liên hệ

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Những Người Đóng Góp Nổi Bật

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Những người đóng góp

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Giấy phép

Thư viện này được cấp phép theo Giấy phép MIT-0. Xem [tệp LICENSE](./LICENSE).