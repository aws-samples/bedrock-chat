# Trò chuyện Bedrock Claude (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_pl-PL.md)

> [!Warning]
>
> **Đã phát hành phiên bản V2. Để cập nhật, vui lòng xem kỹ [hướng dẫn di chuyển](./migration/V1_TO_V2_vi-VN.md).** Nếu không cẩn thận, **CÁC BOT TỪ V1 SẼ TRỞ NÊN VÔ DỤNG.**

Một trợ lý chat đa ngôn ngữ sử dụng các mô hình LLM do [Amazon Bedrock](https://aws.amazon.com/bedrock/) cung cấp cho trí tuệ nhân tạo sinh thành.

### Xem Tổng quan và Hướng dẫn Cài đặt trên YouTube

[![Tổng quan](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Cuộc Trò chuyện Cơ bản

![](./imgs/demo.gif)

### Cá nhân hóa Bot

Thêm hướng dẫn riêng của bạn và cung cấp kiến thức bên ngoài qua URL hoặc tệp tin (còn gọi là [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Bot có thể được chia sẻ giữa các người dùng ứng dụng. Bot được tùy chỉnh cũng có thể được xuất bản dưới dạng API độc lập (Xem [chi tiết](./PUBLISH_API_vi-VN.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> Vì lý do quản trị, chỉ những người dùng được phép mới có thể tạo bot tùy chỉnh. Để cho phép tạo bot tùy chỉnh, người dùng phải là thành viên của nhóm có tên `CreatingBotAllowed`, có thể được thiết lập thông qua bảng điều khiển quản lý > Nhóm người dùng Amazon Cognito hoặc aws cli. Lưu ý rằng ID nhóm người dùng có thể được tham chiếu bằng cách truy cập CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Bảng điều khiển quản trị

<details>
<summary>Bảng điều khiển quản trị</summary>

Phân tích mức sử dụng cho từng người dùng / bot trên bảng điều khiển quản trị. [chi tiết](./ADMINISTRATOR_vi-VN.md)

![](./imgs/admin_bot_analytics.png)

</details>

### Tác nhân được hỗ trợ bởi LLM

<details>
<summary>Tác nhân được hỗ trợ bởi LLM</summary>

Bằng cách sử dụng [chức năng Tác nhân](./AGENT_vi-VN.md), chatbot của bạn có thể tự động xử lý các tác vụ phức tạp hơn. Ví dụ: để trả lời câu hỏi của người dùng, Tác nhân có thể truy xuất thông tin cần thiết từ các công cụ bên ngoài hoặc chia nhỏ tác vụ thành nhiều bước để xử lý.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Triển Khai Siêu Dễ Dàng

- Tại khu vực us-east-1, mở [Quyền truy cập Mô hình Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Quản lý quyền truy cập mô hình` > Chọn tất cả các mục `Anthropic / Claude 3`, tất cả các mục `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` và `Cohere / Embed Multilingual` sau đó nhấn `Lưu thay đổi`.

<details>
<summary>Ảnh chụp màn hình</summary>

![](./imgs/model_screenshot.png)

</details>

- Mở [CloudShell](https://console.aws.amazon.com/cloudshell/home) tại khu vực bạn muốn triển khai
- Chạy triển khai qua các lệnh sau. Nếu bạn muốn chỉ định phiên bản để triển khai hoặc cần áp dụng các chính sách bảo mật, vui lòng chỉ định các tham số phù hợp từ [Các Tham Số Tùy Chọn](#các-tham-số-tùy-chọn).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Bạn sẽ được hỏi liệu là người dùng mới hay sử dụng phiên bản 2. Nếu bạn không phải là người dùng tiếp tục từ phiên bản 0, vui lòng nhập `y`.

### Các Tham Số Tùy Chọn

Bạn có thể chỉ định các tham số sau trong quá trình triển khai để tăng cường bảo mật và tùy chỉnh:

- **--disable-self-register**: Vô hiệu hóa đăng ký tự động (mặc định: được bật). Nếu cờ này được đặt, bạn sẽ cần tạo tất cả người dùng trên cognito và sẽ không cho phép người dùng tự đăng ký tài khoản.
- **--enable-lambda-snapstart**: Bật [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (mặc định: vô hiệu hóa). Nếu cờ này được đặt, sẽ cải thiện thời gian khởi động lạnh cho các hàm Lambda, cung cấp thời gian phản hồi nhanh hơn để mang lại trải nghiệm người dùng tốt hơn.
- **--ipv4-ranges**: Danh sách các phạm vi IPv4 được phép, phân tách bằng dấu phẩy. (mặc định: cho phép tất cả các địa chỉ ipv4)
- **--ipv6-ranges**: Danh sách các phạm vi IPv6 được phép, phân tách bằng dấu phẩy. (mặc định: cho phép tất cả các địa chỉ ipv6)
- **--disable-ipv6**: Vô hiệu hóa kết nối qua IPv6. (mặc định: được bật)
- **--allowed-signup-email-domains**: Danh sách các miền email được phép đăng ký, phân tách bằng dấu phẩy. (mặc định: không hạn chế miền)
- **--bedrock-region**: Xác định khu vực nơi Bedrock có sẵn. (mặc định: us-east-1)
- **--repo-url**: Kho lưu trữ tùy chỉnh của Bedrock Claude Chat để triển khai, nếu đã fork hoặc điều khiển nguồn tùy chỉnh. (mặc định: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: Phiên bản của Bedrock Claude Chat để triển khai. (mặc định: phiên bản mới nhất trong quá trình phát triển)
- **--cdk-json-override**: Bạn có thể ghi đè bất kỳ giá trị ngữ cảnh CDK nào trong quá trình triển khai bằng cách sử dụng khối ghi đè JSON. Điều này cho phép bạn sửa đổi cấu hình mà không cần chỉnh sửa trực tiếp tệp cdk.json.

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

JSON ghi đè phải tuân theo cấu trúc giống như cdk.json. Bạn có thể ghi đè bất kỳ giá trị ngữ cảnh nào bao gồm:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- Và các giá trị ngữ cảnh khác được xác định trong cdk.json

> [!Lưu ý]
> Các giá trị ghi đè sẽ được hợp nhất với cấu hình cdk.json hiện có trong thời gian triển khai trong AWS code build. Các giá trị được chỉ định trong phần ghi đè sẽ được ưu tiên hơn các giá trị trong cdk.json.

#### Ví dụ lệnh với các tham số:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Sau khoảng 35 phút, bạn sẽ nhận được đầu ra sau, mà bạn có thể truy cập từ trình duyệt của mình

```
URL Frontend: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Màn hình đăng ký sẽ xuất hiện như hình trên, nơi bạn có thể đăng ký email và đăng nhập.

> [!Quan Trọng]
> Nếu không đặt tham số tùy chọn, phương pháp triển khai này cho phép bất kỳ ai biết URL đều có thể đăng ký. Đối với việc sử dụng trong sản xuất, rất khuyến nghị thêm các hạn chế địa chỉ IP và vô hiệu hóa đăng ký tự động để giảm thiểu rủi ro bảo mật (bạn có thể xác định allowed-signup-email-domains để hạn chế người dùng sao cho chỉ các địa chỉ email từ miền công ty của bạn mới được đăng ký). Sử dụng cả ipv4-ranges và ipv6-ranges để hạn chế địa chỉ IP, và vô hiệu hóa đăng ký tự động bằng cách sử dụng disable-self-register khi thực thi ./bin.

> [!MẸO]
> Nếu `URL Frontend` không xuất hiện hoặc Bedrock Claude Chat không hoạt động đúng, có thể là do vấn đề với phiên bản mới nhất. Trong trường hợp này, vui lòng thêm `--version "v1.2.6"` vào các tham số và thử triển khai lại.

## Kiến trúc

Đây là kiến trúc được xây dựng trên các dịch vụ quản lý của AWS, loại bỏ nhu cầu quản lý cơ sở hạ tầng. Sử dụng Amazon Bedrock, không cần thiết phải giao tiếp với các API bên ngoài AWS. Điều này cho phép triển khai các ứng dụng có khả năng mở rộng, đáng tin cậy và an toàn.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Cơ sở dữ liệu NoSQL để lưu trữ lịch sử cuộc trò chuyện
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Điểm cuối API backend (AWS Lambda Web Adapter, FastAPI)
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Phân phối ứng dụng frontend (React, Tailwind CSS)
- [AWS WAF](https://aws.amazon.com/waf/): Hạn chế địa chỉ IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Xác thực người dùng
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Dịch vụ quản lý để sử dụng các mô hình nền tảng thông qua API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Cung cấp giao diện quản lý cho Truy xuất-Tăng cường Sinh thành (RAG), cung cấp các dịch vụ để nhúng và phân tích tài liệu
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Nhận sự kiện từ luồng DynamoDB và khởi chạy Step Functions để nhúng kiến thức bên ngoài
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Điều phối quy trình nhập liệu để nhúng kiến thức bên ngoài vào Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Phục vụ làm cơ sở dữ liệu backend cho Bedrock Knowledge Bases, cung cấp khả năng tìm kiếm toàn văn và tìm kiếm vector, cho phép truy xuất thông tin liên quan một cách chính xác
- [Amazon Athena](https://aws.amazon.com/athena/): Dịch vụ truy vấn để phân tích bucket S3

![](./imgs/arch.png)

## Triển khai bằng CDK

Việc Triển khai Siêu Dễ Dàng sử dụng [AWS CodeBuild](https://aws.amazon.com/codebuild/) để thực hiện triển khai CDK nội bộ. Phần này mô tả quy trình triển khai trực tiếp bằng CDK.

- Vui lòng chuẩn bị môi trường UNIX, Docker và môi trường chạy Node.js. Nếu không, bạn cũng có thể sử dụng [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Quan Trọng]
> Nếu không gian lưu trữ trong môi trường cục bộ không đủ trong quá trình triển khai, việc khởi tạo CDK có thể gây ra lỗi. Nếu bạn đang chạy trên Cloud9, v.v., chúng tôi khuyến nghị mở rộng kích thước khối lượng của phiên bản trước khi triển khai.

- Sao chép kho lưu trữ này

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Cài đặt các gói npm

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Nếu cần, hãy chỉnh sửa các mục sau trong [cdk.json](./cdk/cdk.json) nếu cần.

  - `bedrockRegion`: Khu vực có sẵn Bedrock. **LƯU Ý: Bedrock KHÔNG hỗ trợ tất cả các khu vực vào lúc này.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Phạm vi Địa chỉ IP được phép.
  - `enableLambdaSnapStart`: Mặc định là true. Đặt thành false nếu triển khai tại [khu vực không hỗ trợ Lambda SnapStart cho các hàm Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Trước khi triển khai CDK, bạn sẽ cần thực hiện Bootstrap một lần cho khu vực bạn đang triển khai.

```
npx cdk bootstrap
```

- Triển khai dự án mẫu này

```
npx cdk deploy --require-approval never --all
```

- Bạn sẽ nhận được đầu ra tương tự như sau. URL của ứng dụng web sẽ được xuất trong `BedrockChatStack.FrontendURL`, vì vậy vui lòng truy cập từ trình duyệt của bạn.

```sh
 ✅  BedrockChatStack

✨  Thời gian triển khai: 78.57s

Đầu ra:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Xác Định Các Tham Số

Bạn có thể xác định các tham số cho việc triển khai của mình theo hai cách: sử dụng `cdk.json` hoặc sử dụng tệp `parameter.ts` an toàn về mặt kiểu.

#### Sử Dụng cdk.json (Phương Pháp Truyền Thống)

Cách truyền thống để định cấu hình các tham số là chỉnh sửa tệp `cdk.json`. Cách tiếp cận này đơn giản nhưng thiếu kiểm tra kiểu:

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

#### Sử Dụng parameter.ts (Phương Pháp An Toàn Về Mặt Kiểu Được Khuyến Nghị)

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
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Tăng tính sẵn sàng cho sản xuất
});
```

> [!Ghi Chú]
> Người dùng hiện tại có thể tiếp tục sử dụng `cdk.json` mà không cần thay đổi. Cách tiếp cận `parameter.ts` được khuyến nghị cho các triển khai mới hoặc khi bạn cần quản lý nhiều môi trường.

### Triển Khai Nhiều Môi Trường

Bạn có thể triển khai nhiều môi trường từ cùng một cơ sở mã bằng cách sử dụng tệp `parameter.ts` và tùy chọn `-c envName`.

#### Điều Kiện Tiên Quyết

1. Xác định các môi trường của bạn trong `parameter.ts` như đã hiển thị ở trên
2. Mỗi môi trường sẽ có bộ tài nguyên riêng với các tiền tố cụ thể theo môi trường

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

#### Lưu Ý Quan Trọng

1. **Đặt Tên Ngăn Xếp**:

   - Các ngăn xếp chính cho mỗi môi trường sẽ được thêm tiền tố tên môi trường (ví dụ: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Tuy nhiên, các ngăn xếp bot tùy chỉnh (`BrChatKbStack*`) và các ngăn xếp xuất bản API (`ApiPublishmentStack*`) không nhận các tiền tố môi trường vì chúng được tạo động tại thời điểm chạy

2. **Đặt Tên Tài Nguyên**:

   - Chỉ một số tài nguyên nhận các tiền tố môi trường trong tên của chúng (ví dụ: bảng `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Hầu hết các tài nguyên duy trì tên gốc của chúng nhưng được cô lập bằng cách nằm trong các ngăn xếp khác nhau

3. **Nhận Dạng Môi Trường**:

   - Tất cả các tài nguyên được gắn thẻ với thẻ `CDKEnvironment` chứa tên môi trường
   - Bạn có thể sử dụng thẻ này để xác định tài nguyên thuộc môi trường nào
   - Ví dụ: `CDKEnvironment: dev` hoặc `CDKEnvironment: prod`

4. **Ghi Đè Môi Trường Mặc Định**: Nếu bạn xác định môi trường "default" trong `parameter.ts`, nó sẽ ghi đè các cài đặt trong `cdk.json`. Để tiếp tục sử dụng `cdk.json`, đừng xác định môi trường "default" trong `parameter.ts`.

5. **Yêu Cầu Môi Trường**: Để tạo các môi trường khác ngoài "default", bạn phải sử dụng `parameter.ts`. Tùy chọn `-c envName` một mình là không đủ nếu không có các định nghĩa môi trường tương ứng.

6. **Cô Lập Tài Nguyên**: Mỗi môi trường tạo bộ tài nguyên riêng của nó, cho phép bạn có môi trường phát triển, thử nghiệm và sản xuất trong cùng một tài khoản AWS mà không có xung đột.

## Khác

### Cấu hình sinh văn bản mặc định

Người dùng có thể điều chỉnh [các tham số sinh văn bản](https://docs.anthropic.com/claude/reference/complete_post) từ màn hình tạo bot tùy chỉnh. Nếu bot không được sử dụng, các tham số mặc định được đặt trong [config.py](./backend/app/config.py) sẽ được sử dụng.

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Xóa tài nguyên

Nếu sử dụng cli và CDK, hãy chạy `npx cdk destroy`. Nếu không, truy cập [CloudFormation](https://console.aws.amazon.com/cloudformation/home) và sau đó xóa `BedrockChatStack` và `FrontendWafStack` theo cách thủ công. Lưu ý rằng `FrontendWafStack` nằm ở khu vực `us-east-1`.

### Cài đặt Ngôn ngữ

Tài sản này tự động phát hiện ngôn ngữ bằng cách sử dụng [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Bạn có thể chuyển đổi ngôn ngữ từ menu ứng dụng. Ngoài ra, bạn có thể sử dụng Chuỗi Truy vấn để đặt ngôn ngữ như dưới đây.

> `https://example.com?lng=ja`

### Vô hiệu hóa đăng ký tự động

Mẫu này mặc định cho phép đăng ký tự động. Để vô hiệu hóa đăng ký tự động, hãy mở [cdk.json](./cdk/cdk.json) và chuyển `selfSignUpEnabled` thành `false`. Nếu bạn cấu hình [nhà cung cấp danh tính bên ngoài](#external-identity-provider), giá trị sẽ bị bỏ qua và tự động bị vô hiệu hóa.

### Hạn chế Miền cho Địa chỉ Email Đăng ký

Theo mặc định, mẫu này không giới hạn các miền cho địa chỉ email đăng ký. Để chỉ cho phép đăng ký từ các miền cụ thể, hãy mở `cdk.json` và chỉ định các miền dưới dạng danh sách trong `allowedSignUpEmailDomains`.

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

Nếu bạn muốn người dùng mới được tự động tham gia các nhóm, bạn có thể chỉ định chúng trong [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Theo mặc định, người dùng mới được tạo sẽ được thêm vào nhóm `CreatingBotAllowed`.

### Cấu hình Bản sao RAG

`enableRagReplicas` là một tùy chọn trong [cdk.json](./cdk/cdk.json) điều khiển các cài đặt bản sao cho cơ sở dữ liệu RAG, cụ thể là Cơ sở Kiến thức sử dụng Amazon OpenSearch Serverless.

- **Mặc định**: true
- **true**: Tăng tính sẵn sàng bằng cách kích hoạt các bản sao bổ sung, phù hợp cho môi trường sản xuất nhưng tăng chi phí.
- **false**: Giảm chi phí bằng cách sử dụng ít bản sao hơn, phù hợp cho phát triển và thử nghiệm.

Đây là cài đặt cấp tài khoản/khu vực, ảnh hưởng đến toàn bộ ứng dụng chứ không phải từng bot riêng lẻ.

> [!Ghi chú]
> Tính đến tháng 6 năm 2024, Amazon OpenSearch Serverless hỗ trợ 0,5 OCU, hạ thấp chi phí đầu vào cho các khối lượng công việc quy mô nhỏ. Các triển khai sản xuất có thể bắt đầu với 2 OCU, trong khi các khối lượng công việc phát triển/thử nghiệm có thể sử dụng 1 OCU. OpenSearch Serverless tự động mở rộng quy mô dựa trên nhu cầu công việc. Để biết thêm chi tiết, hãy truy cập [thông báo](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Suy luận liên vùng

[Suy luận liên vùng](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) cho phép Amazon Bedrock định tuyến động các yêu cầu suy luận mô hình trên nhiều khu vực AWS, tăng cường thông lượng và khả năng phục hồi trong các giai đoạn nhu cầu cao điểm. Để cấu hình, hãy chỉnh sửa `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) cải thiện thời gian khởi động lạnh cho các hàm Lambda, cung cấp thời gian phản hồi nhanh hơn để mang lại trải nghiệm người dùng tốt hơn. Mặt khác, đối với các hàm Python, có [mức phí phụ thuộc vào kích thước bộ nhớ đệm](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) và [không khả dụng ở một số khu vực](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) hiện tại. Để vô hiệu hóa SnapStart, hãy chỉnh sửa `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Cấu hình Tên miền Tùy chỉnh

Bạn có thể cấu hình tên miền tùy chỉnh cho phân phối CloudFront bằng cách đặt các tham số sau trong [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Tên miền tùy chỉnh cho ứng dụng chat của bạn (ví dụ: chat.example.com)
- `hostedZoneId`: ID của vùng được lưu trữ Route 53 nơi các bản ghi DNS sẽ được tạo

Khi các tham số này được cung cấp, việc triển khai sẽ tự động:

- Tạo chứng chỉ ACM với xác thực DNS trong khu vực us-east-1
- Tạo các bản ghi DNS cần thiết trong vùng được lưu trữ Route 53 của bạn
- Cấu hình CloudFront để sử dụng tên miền tùy chỉnh của bạn

> [!Ghi chú]
> Tên miền phải được quản lý bởi Route 53 trong tài khoản AWS của bạn. ID vùng được lưu trữ có thể được tìm thấy trong bảng điều khiển Route 53.

### Phát triển Cục bộ

Xem [PHÁT TRIỂN CỤC BỘ](./LOCAL_DEVELOPMENT_vi-VN.md).

### Đóng góp

Cảm ơn bạn đã xem xét đóng góp cho kho lưu trữ này! Chúng tôi hoan nghênh các bản sửa lỗi, bản dịch ngôn ngữ (i18n), cải tiến tính năng, [công cụ đại lý](./docs/AGENT.md#how-to-develop-your-own-tools) và các cải tiến khác.

Đối với các cải tiến tính năng và các cải tiến khác, **trước khi tạo Pull Request, chúng tôi rất mong bạn tạo Vấn đề Yêu cầu Tính năng để thảo luận về phương pháp và chi tiết triển khai. Đối với các bản sửa lỗi và bản dịch ngôn ngữ (i18n), hãy tiến hành tạo Pull Request trực tiếp.**

Vui lòng cũng xem xét các hướng dẫn sau trước khi đóng góp:

- [Phát triển Cục bộ](./LOCAL_DEVELOPMENT_vi-VN.md)
- [ĐÓNG GÓP](./CONTRIBUTING_vi-VN.md)

## Liên hệ

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Những Đóng Góp Viên Xuất Sắc

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## Những người đóng góp

[![những người đóng góp bedrock claude chat](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Giấy phép

Thư viện này được cấp phép theo Giấy phép MIT-0. Xem [tệp LICENSE](./LICENSE).