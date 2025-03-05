# Bedrock Claude 聊天（Nova）

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_pl-PL.md)

> [!Warning]  
> **V2 已發布。要更新，請仔細查看[遷移指南](./migration/V1_TO_V2_zh-TW.md)。若不小心處理，**V1 版本的機器人將無法使用。**

一個使用 [Amazon Bedrock](https://aws.amazon.com/bedrock/) 提供的大型語言模型（LLM）的多語言聊天機器人，用於生成式人工智慧。

### 在 YouTube 上觀看概述和安裝

[![概述](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本對話

![](./imgs/demo.gif)

### 機器人個性化

添加您自己的指令，並提供外部知識作為 URL 或文件（又稱為[檢索增強生成（RAG）](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。該機器人可以在應用程式用戶之間共享。自定義機器人還可以發布為獨立的 API（請參見[詳情](./PUBLISH_API_zh-TW.md)）。

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> 出於治理原因，只有允許的用戶才能創建自定義機器人。要允許創建自定義機器人，用戶必須是名為 `CreatingBotAllowed` 的組的成員，可以通過管理控制台 > Amazon Cognito 用戶池或 AWS CLI 進行設置。請注意，用戶池 ID 可以通過訪問 CloudFormation > BedrockChatStack > 輸出 > `AuthUserPoolIdxxxx` 來查看。

### 管理員儀表板

<details>
<summary>管理員儀表板</summary>

在管理員儀表板上分析每個用戶/機器人的使用情況。[詳情](./ADMINISTRATOR_zh-TW.md)

![](./imgs/admin_bot_analytics.png)

</details>

### 基於大型語言模型的代理

<details>
<summary>基於大型語言模型的代理</summary>

通過使用[代理功能](./AGENT_zh-TW.md)，您的聊天機器人可以自動處理更複雜的任務。例如，為了回答用戶的問題，代理可以從外部工具檢索必要的信息，或將任務分解為多個步驟進行處理。

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超級簡單的部署

- 在 us-east-1 區域，開啟 [Bedrock 模型存取](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `管理模型存取` > 勾選所有的 `Anthropic / Claude 3`、`Amazon / Nova`、`Amazon / Titan 文本嵌入 V2` 和 `Cohere / 多語言嵌入`，然後 `儲存變更`。

<details>
<summary>螢幕截圖</summary>

![](./imgs/model_screenshot.png)

</details>

- 在您要部署的區域開啟 [CloudShell](https://console.aws.amazon.com/cloudshell/home)
- 透過以下命令進行部署。如果您想指定要部署的版本或需要套用安全性原則，請從[可選參數](#optional-parameters)中指定適當的參數。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 系統會詢問是新用戶還是使用 v2。如果您不是 v0 的延續用戶，請輸入 `y`。

### 可選參數

您可以在部署期間指定以下參數以增強安全性和自訂性：

- **--disable-self-register**：停用自行註冊（預設：啟用）。如果設定此標誌，您將需要在 Cognito 上建立所有用戶，且不允許用戶自行註冊帳戶。
- **--enable-lambda-snapstart**：啟用 [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)（預設：停用）。如果設定此標誌，可改善 Lambda 函數的冷啟動時間，提供更快的響應時間，以獲得更好的用戶體驗。
- **--ipv4-ranges**：允許的 IPv4 範圍的逗號分隔清單。（預設：允許所有 IPv4 位址）
- **--ipv6-ranges**：允許的 IPv6 範圍的逗號分隔清單。（預設：允許所有 IPv6 位址）
- **--disable-ipv6**：停用 IPv6 連線。（預設：啟用）
- **--allowed-signup-email-domains**：允許註冊的電子郵件網域的逗號分隔清單。（預設：無網域限制）
- **--bedrock-region**：定義 Bedrock 可用的區域。（預設：us-east-1）
- **--repo-url**：要部署的 Bedrock Claude Chat 的自訂儲存庫，如果是 fork 或自訂原始碼控制。（預設：https://github.com/aws-samples/bedrock-claude-chat.git）
- **--version**：要部署的 Bedrock Claude Chat 版本。（預設：開發中的最新版本）
- **--cdk-json-override**：您可以使用覆蓋 JSON 區塊在部署期間覆蓋任何 CDK 上下文值。這允許您在不直接編輯 cdk.json 檔案的情況下修改配置。

使用範例：

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

覆蓋 JSON 必須遵循與 cdk.json 相同的結構。您可以覆蓋任何上下文值，包括：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- 以及 cdk.json 中定義的其他上下文值

> [!注意]
> 覆蓋值將在 AWS 代碼構建期間與現有的 cdk.json 配置合併。指定的覆蓋值將優先於 cdk.json 中的值。

#### 帶有參數的範例命令：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 大約 35 分鐘後，您將獲得以下輸出，可以從瀏覽器訪問

```
前端 URL：https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

如上所示，將出現登入畫面，您可以在其中註冊您的電子郵件並登入。

> [!重要]
> 如果不設置可選參數，此部署方法允許任何知道 URL 的人註冊。對於生產使用，強烈建議添加 IP 位址限制並停用自行註冊，以減輕安全風險（您可以定義 allowed-signup-email-domains 以限制用戶，使只有來自您公司網域的電子郵件地址可以註冊）。在執行 ./bin 時，同時使用 ipv4-ranges 和 ipv6-ranges 進行 IP 位址限制，並使用 disable-self-register 停用自行註冊。

> [!提示]
> 如果 `前端 URL` 未顯示或 Bedrock Claude Chat 無法正常工作，可能是最新版本的問題。在這種情況下，請在參數中添加 `--version "v1.2.6"` 並重新嘗試部署。

## 架構

這是建立在 AWS 受管服務之上的架構，無需基礎設施管理。利用 Amazon Bedrock，無需與 AWS 外部的 API 通訊。這使得部署可擴展、可靠且安全的應用程式成為可能。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：用於儲存對話歷史的 NoSQL 資料庫
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：後端 API 端點（[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)、[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：前端應用程式傳遞（[React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/)：IP 位址限制
- [Amazon Cognito](https://aws.amazon.com/cognito/)：使用者驗證
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：透過 API 利用基礎模型的受管服務
- [Amazon Bedrock 知識庫](https://aws.amazon.com/bedrock/knowledge-bases/)：提供檢索增強生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）的受管介面，提供文件嵌入和解析服務
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：從 DynamoDB 串流接收事件並啟動 Step Functions 以嵌入外部知識
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：協調將外部知識嵌入 Bedrock 知識庫的擷取管道
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：作為 Bedrock 知識庫的後端資料庫，提供全文檢索和向量搜尋功能，實現準確檢索相關資訊
- [Amazon Athena](https://aws.amazon.com/athena/)：用於分析 S3 儲存桶的查詢服務

![](./imgs/arch.png)

## 使用 CDK 部署

超級簡單的部署使用 [AWS CodeBuild](https://aws.amazon.com/codebuild/) 透過 CDK 內部執行部署。本節描述直接使用 CDK 部署的步驟。

- 請準備 UNIX、Docker 和 Node.js 運行環境。如果沒有，您也可以使用 [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Important]
> 如果在本地環境部署期間儲存空間不足，CDK 引導可能會導致錯誤。如果您在 Cloud9 等環境中運行，建議在部署前擴大實例的磁碟區大小。

- 克隆此儲存庫

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- 安裝 npm 套件

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- 如有必要，編輯 [cdk.json](./cdk/cdk.json) 中的以下條目

  - `bedrockRegion`：Bedrock 可用的區域。**注意：目前 Bedrock 不支持所有區域。**
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`：允許的 IP 地址範圍。
  - `enableLambdaSnapStart`：預設為 true。如果部署到[不支持 Python 函數 Lambda SnapStart 的區域](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)，請設為 false。

- 在部署 CDK 之前，您需要為部署的區域進行一次引導。

```
npx cdk bootstrap
```

- 部署此範例專案

```
npx cdk deploy --require-approval never --all
```

- 您將得到類似以下的輸出。Web 應用程式的 URL 將在 `BedrockChatStack.FrontendURL` 中輸出，請從瀏覽器訪問。

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## 其他

### 配置 Mistral 模型支持

在 [cdk.json](./cdk/cdk.json) 中將 `enableMistral` 更新為 `true`，然後運行 `npx cdk deploy`。

```json
...
  "enableMistral": true,
```

> [!重要]
> 此專案專注於 Anthropic Claude 模型，Mistral 模型支援有限。例如，提示範例是基於 Claude 模型。這是一個僅限 Mistral 的選項，一旦您啟用 Mistral 模型，您只能對所有聊天功能使用 Mistral 模型，而不能同時使用 Claude 和 Mistral 模型。

### 配置預設文本生成

用戶可以在自定義機器人創建畫面調整[文本生成參數](https://docs.anthropic.com/claude/reference/complete_post)。如果機器人未被使用，將使用 [config.py](./backend/app/config.py) 中設置的預設參數。

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### 移除資源

如果使用 CLI 和 CDK，請執行 `npx cdk destroy`。如果不是，請訪問 [CloudFormation](https://console.aws.amazon.com/cloudformation/home) 並手動刪除 `BedrockChatStack` 和 `FrontendWafStack`。請注意 `FrontendWafStack` 位於 `us-east-1` 區域。

### 語言設定

此資源使用 [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector) 自動檢測語言。您可以從應用程式選單切換語言。另外，您也可以使用查詢字串設置語言，如下所示。

> `https://example.com?lng=ja`

### 禁用自助註冊

此範例預設啟用自助註冊。要禁用自助註冊，請打開 [cdk.json](./cdk/cdk.json) 並將 `selfSignUpEnabled` 設置為 `false`。如果您配置了[外部身份提供者](#external-identity-provider)，該值將被忽略並自動禁用。

### 限制註冊電子郵件地址的網域

預設情況下，此範例不限制註冊電子郵件地址的網域。要僅允許從特定網域註冊，請打開 `cdk.json` 並在 `allowedSignUpEmailDomains` 中指定網域列表。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部身份提供者

此範例支持外部身份提供者。目前我們支持 [Google](./idp/SET_UP_GOOGLE_zh-TW.md) 和[自定義 OIDC 提供者](./idp/SET_UP_CUSTOM_OIDC_zh-TW.md)。

### 自動將新用戶添加到組

此範例有以下組來為用戶授予權限：

- [`Admin`](./ADMINISTRATOR_zh-TW.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_zh-TW.md)

如果您希望新創建的用戶自動加入組，可以在 [cdk.json](./cdk/cdk.json) 中指定。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

預設情況下，新創建的用戶將加入 `CreatingBotAllowed` 組。

### 配置 RAG 副本

[cdk.json](./cdk/cdk.json) 中的 `enableRagReplicas` 選項控制 RAG 數據庫的副本設置，特別是使用 Amazon OpenSearch Serverless 的知識庫。

- **預設值**：true
- **true**：通過啟用額外的副本來增強可用性，適合生產環境，但會增加成本。
- **false**：通過減少副本來降低成本，適合開發和測試。

這是一個賬戶/區域級別的設置，影響整個應用程式而不是個別機器人。

> [!注意]
> 截至 2024 年 6 月，Amazon OpenSearch Serverless 支持 0.5 OCU，降低了小規模工作負載的入門成本。生產部署可以從 2 個 OCU 開始，而開發/測試工作負載可以使用 1 個 OCU。OpenSearch Serverless 會根據工作負載需求自動擴展。更多詳情請訪問[公告](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)。

### 跨區域推理

[跨區域推理](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)允許 Amazon Bedrock 在多個 AWS 區域動態路由模型推理請求，在高峰需求期間提高吞吐量和彈性。要配置，請編輯 `cdk.json`。

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) 改善 Lambda 函數的冷啟動時間，提供更快的響應時間以獲得更好的用戶體驗。另一方面，對於 Python 函數，根據緩存大小會有[費用](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)，並且[目前在某些區域不可用](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)。要禁用 SnapStart，請編輯 `cdk.json`。

```json
"enableLambdaSnapStart": false
```

### 配置自定義域名

您可以通過在 [cdk.json](./cdk/cdk.json) 中設置以下參數來為 CloudFront 分佈配置自定義域名：

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`：聊天應用程式的自定義域名（例如 chat.example.com）
- `hostedZoneId`：將創建域名記錄的 Route 53 託管區域 ID

提供這些參數時，部署將自動：

- 在 us-east-1 區域創建具有 DNS 驗證的 ACM 證書
- 在您的 Route 53 託管區域中創建必要的 DNS 記錄
- 配置 CloudFront 使用您的自定義域名

> [!注意]
> 域名必須由您的 AWS 賬戶中的 Route 53 管理。託管區域 ID 可以在 Route 53 控制台中找到。

### 本地開發

請參見 [本地開發](./LOCAL_DEVELOPMENT_zh-TW.md)。

### 貢獻

感謝您考慮為此儲存庫做出貢獻！我們歡迎錯誤修復、語言翻譯（i18n）、功能增強、[代理工具](./docs/AGENT.md#how-to-develop-your-own-tools)和其他改進。

對於功能增強和其他改進，**在創建 Pull Request 之前，我們非常感謝您創建一個功能請求 Issue 來討論實施方法和細節。對於錯誤修復和語言翻譯（i18n），直接創建 Pull Request。**

在貢獻之前，請查看以下指南：

- [本地開發](./LOCAL_DEVELOPMENT_zh-TW.md)
- [貢獻指南](./CONTRIBUTING_zh-TW.md)

## 聯絡人

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 重要貢獻者

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## 貢獻者

[![bedrock claude chat 貢獻者](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## 授權

此程式庫採用 MIT-0 授權。請參閱 [授權檔案](./LICENSE)。