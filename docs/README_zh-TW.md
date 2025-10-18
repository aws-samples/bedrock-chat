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


一個由 [Amazon Bedrock](https://aws.amazon.com/bedrock/) 驅動的多語言生成式 AI 平台。
支援聊天、具有知識庫的自定義機器人（RAG）、透過機器人商店分享機器人，以及使用代理進行任務自動化。

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 已發布。要更新，請仔細閱讀[遷移指南](./migration/V2_TO_V3_zh-TW.md)。** 如果不小心處理，**V2 版本的機器人將無法使用。**

### 機器人個人化 / 機器人商店

添加您自己的指令和知識（又稱 [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。機器人可以通過機器人商店市場在應用程序用戶之間共享。自定義機器人也可以作為獨立 API 發布（詳見[說明](./PUBLISH_API_zh-TW.md)）。

<details>
<summary>截圖</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

您也可以匯入現有的 [Amazon Bedrock's KnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/)。

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> 出於治理原因，只有獲得允許的用戶才能創建自定義機器人。要允許創建自定義機器人，用戶必須是名為 `CreatingBotAllowed` 群組的成員，該群組可以通過管理控制台 > Amazon Cognito User pools 或 aws cli 設置。請注意，可以通過訪問 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` 來參考用戶池 ID。

### 管理功能

API 管理、將機器人標記為必要、分析機器人使用情況。[詳情](./ADMINISTRATOR_zh-TW.md)

<details>
<summary>截圖</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png)

</details>

### 代理

通過使用[代理功能](./AGENT_zh-TW.md)，您的聊天機器人可以自動處理更複雜的任務。例如，為了回答用戶的問題，代理可以從外部工具檢索必要的信息，或將任務分解為多個步驟進行處理。

<details>
<summary>截圖</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超簡單部署

- 在 us-east-1 區域中,打開 [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > 勾選所有您想使用的模型然後點選 `Save changes`。

<details>
<summary>截圖</summary>

![](./imgs/model_screenshot.png)

</details>

### 支援的區域

請確保您在[有提供 OpenSearch Serverless 和 Ingestion APIs 的區域](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html)部署 Bedrock Chat,如果您想要使用聊天機器人和建立知識庫的話(OpenSearch Serverless 是預設選項)。截至 2025 年 8 月,支援的區域包括:us-east-1、us-east-2、us-west-1、us-west-2、ap-south-1、ap-northeast-1、ap-northeast-2、ap-southeast-1、ap-southeast-2、ca-central-1、eu-central-1、eu-west-1、eu-west-2、eu-south-2、eu-north-1、sa-east-1

對於 **bedrock-region** 參數,您需要選擇一個[有提供 Bedrock 服務的區域](https://docs.aws.amazon.com/general/latest/gr/bedrock.html)。

- 在您想要部署的區域中開啟 [CloudShell](https://console.aws.amazon.com/cloudshell/home)
- 透過以下指令執行部署。如果您想要指定要部署的版本或需要套用安全性政策,請從[選用參數](#optional-parameters)中指定適當的參數。

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- 系統會詢問您是否為新使用者或使用 v3。如果您不是從 v0 升級的使用者,請輸入 `y`。

### 選用參數

您可以在部署時指定以下參數來加強安全性和客製化:

- **--disable-self-register**: 停用自助註冊(預設:啟用)。如果設定此旗標,您將需要在 cognito 上建立所有使用者,且不允許使用者自行註冊帳號。
- **--enable-lambda-snapstart**: 啟用 [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (預設:停用)。如果設定此旗標,可改善 Lambda 函數的冷啟動時間,提供更快的回應時間以獲得更好的使用者體驗。
- **--ipv4-ranges**: 允許的 IPv4 範圍清單(以逗號分隔)。(預設:允許所有 IPv4 位址)
- **--ipv6-ranges**: 允許的 IPv6 範圍清單(以逗號分隔)。(預設:允許所有 IPv6 位址)
- **--disable-ipv6**: 停用 IPv6 連線。(預設:啟用)
- **--allowed-signup-email-domains**: 允許註冊的電子郵件網域清單(以逗號分隔)。(預設:無網域限制)
- **--bedrock-region**: 定義可使用 bedrock 的區域。(預設:us-east-1)
- **--repo-url**: 要部署的 Bedrock Chat 自訂儲存庫,如果是 fork 或自訂原始碼控制。(預設:https://github.com/aws-samples/bedrock-chat.git)
- **--version**: 要部署的 Bedrock Chat 版本。(預設:開發中的最新版本)
- **--cdk-json-override**: 您可以在部署期間使用覆寫 JSON 區塊來覆寫任何 CDK context 值。這允許您修改設定而無需直接編輯 cdk.json 檔案。

使用範例:

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

覆寫 JSON 必須遵循與 cdk.json 相同的結構。您可以覆寫任何 context 值,包括:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: 接受要啟用的模型 ID 清單。預設值為空清單,會啟用所有模型。
- `logoPath`: 前端 `public/` 目錄中出現在導航抽屜頂部的標誌資產的相對路徑。
- 以及 cdk.json 中定義的其他 context 值

> [!Note]
> 覆寫值將在 AWS code build 的部署時與現有的 cdk.json 設定合併。覆寫中指定的值將優先於 cdk.json 中的值。

#### 含參數的範例指令:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 大約 35 分鐘後,您將獲得以下輸出,您可以從瀏覽器存取

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

將會出現如上所示的註冊畫面,您可以在此註冊電子郵件並登入。

> [!Important]
> 若未設定選用參數,此部署方法允許任何知道 URL 的人註冊。對於生產環境使用,強烈建議新增 IP 位址限制並停用自助註冊以降低安全風險(您可以定義 allowed-signup-email-domains 來限制使用者,使得只有來自貴公司網域的電子郵件地址可以註冊)。執行 ./bin 時請同時使用 ipv4-ranges 和 ipv6-ranges 進行 IP 位址限制,並使用 disable-self-register 停用自助註冊。

> [!TIP]
> 如果 `Frontend URL` 沒有出現或 Bedrock Chat 無法正常運作,可能是最新版本的問題。在這種情況下,請在參數中加入 `--version "v3.0.0"` 並重新嘗試部署。

## 架構

這是一個建立在 AWS 託管服務上的架構，無需管理基礎設施。透過使用 Amazon Bedrock，不需要與 AWS 以外的 API 通訊。這使得能夠部署可擴展、可靠且安全的應用程式。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：用於儲存對話歷史的 NoSQL 資料庫
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：後端 API 端點 ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：前端應用程式交付 ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/)：IP 位址限制
- [Amazon Cognito](https://aws.amazon.com/cognito/)：使用者認證
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：透過 API 使用基礎模型的託管服務
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)：提供檢索增強生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）的託管介面，提供文件嵌入和解析服務
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：接收來自 DynamoDB 串流的事件並啟動 Step Functions 以嵌入外部知識
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：編排嵌入外部知識到 Bedrock Knowledge Bases 的擷取管道
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：作為 Bedrock Knowledge Bases 的後端資料庫，提供全文搜尋和向量搜尋功能，實現準確的相關資訊檢索
- [Amazon Athena](https://aws.amazon.com/athena/)：用於分析 S3 儲存桶的查詢服務

![](./imgs/arch.png)

## 使用 CDK 部署

超簡易部署內部使用 [AWS CodeBuild](https://aws.amazon.com/codebuild/) 透過 CDK 執行部署。本節說明直接使用 CDK 部署的程序。

- 請準備 UNIX、Docker 和 Node.js 執行環境。

> [!Important]
> 如果在部署期間本地環境的儲存空間不足，CDK 啟動程序可能會出錯。我們建議在部署前擴充執行個體的磁碟區大小。

- 複製此儲存庫

```
git clone https://github.com/aws-samples/bedrock-chat
```

- 安裝 npm 套件

```
cd bedrock-chat
cd cdk
npm ci
```

- 如有必要，編輯 [cdk.json](./cdk/cdk.json) 中的以下項目。

  - `bedrockRegion`: Bedrock 可用的區域。**注意：Bedrock 目前尚未支援所有區域。**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: 允許的 IP 位址範圍。
  - `enableLambdaSnapStart`: 預設為 true。如果部署到[不支援 Python 函數 Lambda SnapStart 的區域](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)，請設為 false。
  - `globalAvailableModels`: 預設為全部。如果設定(模型 ID 列表)，可以全域控制在 Bedrock Chat 應用程式中所有使用者的聊天和建立機器人時下拉選單中顯示的模型。
  - `logoPath`: 指向應用程式抽屜頂部顯示圖片的 `frontend/public` 下的相對路徑。
支援以下模型 ID (請確保在部署區域的 Bedrock 控制台的模型存取中也已啟用這些模型):
- **Claude 模型:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Amazon Nova 模型:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Mistral 模型:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **DeepSeek 模型:** `deepseek-r1`
- **Meta Llama 模型:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

完整列表可在 [index.ts](./frontend/src/constants/index.ts) 中找到。

- 在部署 CDK 之前，您需要先為要部署的區域執行一次 Bootstrap。

```
npx cdk bootstrap
```

- 部署此範例專案

```
npx cdk deploy --require-approval never --all
```

- 您將得到類似以下的輸出。網頁應用程式的 URL 將輸出在 `BedrockChatStack.FrontendURL` 中，請從瀏覽器存取。

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### 定義參數

您可以透過兩種方式定義部署參數：使用 `cdk.json` 或使用類型安全的 `parameter.ts` 檔案。

#### 使用 cdk.json (傳統方法)

配置參數的傳統方式是編輯 `cdk.json` 檔案。這種方法簡單但缺乏類型檢查：

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

#### 使用 parameter.ts (建議的類型安全方法)

為了更好的類型安全性和開發者體驗，您可以使用 `parameter.ts` 檔案來定義參數：

```typescript
// 定義預設環境的參數
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

// 定義額外環境的參數
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 開發環境的成本節省
  enableBotStoreReplicas: false, // 開發環境的成本節省
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 生產環境的增強可用性
  enableBotStoreReplicas: true, // 生產環境的增強可用性
});
```

> [!Note]
> 現有使用者可以繼續使用 `cdk.json` 而無需任何變更。建議新的部署或需要管理多個環境時使用 `parameter.ts` 方法。

### 部署多個環境

您可以使用 `parameter.ts` 檔案和 `-c envName` 選項從同一程式碼庫部署多個環境。

#### 先決條件

1. 如上所示在 `parameter.ts` 中定義您的環境
2. 每個環境都將擁有自己的資源，並帶有環境特定的前綴

#### 部署命令

部署特定環境：

```bash
# 部署開發環境
npx cdk deploy --all -c envName=dev

# 部署生產環境
npx cdk deploy --all -c envName=prod
```

如果未指定環境，則使用「預設」環境：

```bash
# 部署預設環境
npx cdk deploy --all
```

#### 重要注意事項

1. **堆疊命名**：

   - 每個環境的主要堆疊將帶有環境名稱前綴(例如 `dev-BedrockChatStack`、`prod-BedrockChatStack`)
   - 然而，自定義機器人堆疊(`BrChatKbStack*`)和 API 發布堆疊(`ApiPublishmentStack*`)不會收到環境前綴，因為它們是在運行時動態創建的

2. **資源命名**：

   - 只有部分資源在其名稱中收到環境前綴(例如 `dev_ddb_export` 表、`dev-FrontendWebAcl`)
   - 大多數資源保持其原始名稱，但通過在不同堆疊中進行隔離

3. **環境識別**：

   - 所有資源都使用包含環境名稱的 `CDKEnvironment` 標籤進行標記
   - 您可以使用此標籤識別資源所屬的環境
   - 例如：`CDKEnvironment: dev` 或 `CDKEnvironment: prod`

4. **預設環境覆蓋**：如果您在 `parameter.ts` 中定義「預設」環境，它將覆蓋 `cdk.json` 中的設定。要繼續使用 `cdk.json`，請不要在 `parameter.ts` 中定義「預設」環境。

5. **環境要求**：要創建「預設」以外的環境，您必須使用 `parameter.ts`。單獨使用 `-c envName` 選項而沒有相應的環境定義是不夠的。

6. **資源隔離**：每個環境創建自己的資源集，允許您在同一 AWS 帳戶中擁有開發、測試和生產環境，而不會發生衝突。

## 其他

您可以透過兩種方式定義部署參數：使用 `cdk.json` 或使用類型安全的 `parameter.ts` 檔案。

#### 使用 cdk.json（傳統方法）

配置參數的傳統方式是編輯 `cdk.json` 檔案。這種方法簡單但缺乏類型檢查：

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

#### 使用 parameter.ts（建議的類型安全方法）

為了更好的類型安全性和開發者體驗，您可以使用 `parameter.ts` 檔案來定義參數：

```typescript
// 定義預設環境的參數
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// 定義額外環境的參數
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 開發環境的成本節省措施
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 生產環境的增強可用性
});
```

> [!Note]
> 現有使用者可以繼續使用 `cdk.json` 而不需要任何更改。建議新的部署或需要管理多個環境時使用 `parameter.ts` 方法。

### 部署多個環境

您可以使用 `parameter.ts` 檔案和 `-c envName` 選項從同一程式碼庫部署多個環境。

#### 前置條件

1. 如上所示在 `parameter.ts` 中定義您的環境
2. 每個環境都將擁有自己的資源集合，並帶有環境特定的前綴

#### 部署命令

部署特定環境：

```bash
# 部署開發環境
npx cdk deploy --all -c envName=dev

# 部署生產環境
npx cdk deploy --all -c envName=prod
```

如果未指定環境，則使用「預設」環境：

```bash
# 部署預設環境
npx cdk deploy --all
```

#### 重要注意事項

1. **堆疊命名**：

   - 每個環境的主要堆疊將帶有環境名稱前綴（例如：`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - 但是，自訂機器人堆疊（`BrChatKbStack*`）和 API 發布堆疊（`ApiPublishmentStack*`）不會收到環境前綴，因為它們是在執行時動態建立的

2. **資源命名**：

   - 只有部分資源在其名稱中接收環境前綴（例如：`dev_ddb_export` 表格、`dev-FrontendWebAcl`）
   - 大多數資源保持其原始名稱，但透過位於不同堆疊中而保持隔離

3. **環境識別**：

   - 所有資源都會標記有包含環境名稱的 `CDKEnvironment` 標籤
   - 您可以使用此標籤來識別資源屬於哪個環境
   - 範例：`CDKEnvironment: dev` 或 `CDKEnvironment: prod`

4. **預設環境覆寫**：如果您在 `parameter.ts` 中定義了「預設」環境，它將覆寫 `cdk.json` 中的設定。要繼續使用 `cdk.json`，請不要在 `parameter.ts` 中定義「預設」環境。

5. **環境要求**：要建立「預設」以外的環境，您必須使用 `parameter.ts`。單獨使用 `-c envName` 選項而沒有相應的環境定義是不夠的。

6. **資源隔離**：每個環境建立自己的資源集合，讓您可以在同一個 AWS 帳戶中擁有開發、測試和生產環境，而不會發生衝突。

## 其他

### 移除資源

如果使用 CLI 和 CDK,請執行 `npx cdk destroy`。如果沒有,請存取 [CloudFormation](https://console.aws.amazon.com/cloudformation/home) 然後手動刪除 `BedrockChatStack` 和 `FrontendWafStack`。請注意 `FrontendWafStack` 位於 `us-east-1` 區域。

### 語言設定

此應用程式使用 [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector) 自動偵測語言。您可以從應用程式選單切換語言。或者,您可以使用如下所示的查詢字串來設定語言。

> `https://example.com?lng=ja`

### 停用自行註冊

此範例預設啟用自行註冊功能。要停用自行註冊,請開啟 [cdk.json](./cdk/cdk.json) 並將 `selfSignUpEnabled` 切換為 `false`。如果您設定了[外部身分提供者](#external-identity-provider),此值將被忽略並自動停用。

### 限制註冊電子郵件地址的網域

預設情況下,此範例不限制註冊電子郵件地址的網域。若要僅允許特定網域的註冊,請開啟 `cdk.json` 並在 `allowedSignUpEmailDomains` 中指定網域清單。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部身分提供者

此範例支援外部身分提供者。目前我們支援 [Google](./idp/SET_UP_GOOGLE_zh-TW.md) 和[自訂 OIDC 提供者](./idp/SET_UP_CUSTOM_OIDC_zh-TW.md)。

### 選用的前端 WAF

對於 CloudFront 分配,AWS WAF WebACL 必須在 us-east-1 區域中建立。在某些組織中,政策限制在主要區域之外建立資源。在這種環境中,當嘗試在 us-east-1 中佈建前端 WAF 時,CDK 部署可能會失敗。

為了適應這些限制,前端 WAF 堆疊是選用的。當停用時,CloudFront 分配將在沒有 WebACL 的情況下部署。這表示您將無法在前端邊緣進行 IP 允許/拒絕控制。身分驗證和所有其他應用程式控制將照常運作。請注意,此設定僅影響前端 WAF (CloudFront 範圍);已發佈的 API WAF (區域性) 不受影響。

要停用前端 WAF,請在 `parameter.ts` 中設定以下內容(建議的類型安全方法):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

或者如果使用舊版 `cdk/cdk.json`,請設定以下內容:

```json
"enableFrontendWaf": false
```

### 自動將新使用者加入群組

此範例具有以下群組來授予使用者權限:

- [`Admin`](./ADMINISTRATOR_zh-TW.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_zh-TW.md)

如果您希望新建立的使用者自動加入群組,可以在 [cdk.json](./cdk/cdk.json) 中指定。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

預設情況下,新建立的使用者將加入 `CreatingBotAllowed` 群組。

### 設定 RAG 複本

`enableRagReplicas` 是 [cdk.json](./cdk/cdk.json) 中的一個選項,用於控制 RAG 資料庫(特別是使用 Amazon OpenSearch Serverless 的知識庫)的複本設定。

- **預設值**: true
- **true**: 透過啟用額外的複本來增強可用性,適合生產環境但會增加成本。
- **false**: 透過使用較少的複本來降低成本,適合開發和測試。

這是帳戶/區域層級的設定,影響整個應用程式而不是個別機器人。

> [!Note]
> 截至 2024 年 6 月,Amazon OpenSearch Serverless 支援 0.5 OCU,降低了小規模工作負載的入門成本。生產部署可以從 2 個 OCU 開始,而開發/測試工作負載可以使用 1 個 OCU。OpenSearch Serverless 會根據工作負載需求自動擴展。詳情請參閱[公告](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)。

### 設定機器人商店

機器人商店功能允許使用者分享和探索自訂機器人。您可以透過 [cdk.json](./cdk/cdk.json) 中的以下設定來設定機器人商店:

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: 控制是否啟用機器人商店功能(預設: `true`)
- **botStoreLanguage**: 設定機器人搜尋和探索的主要語言(預設: `"en"`)。這會影響機器人在商店中的索引和搜尋方式,針對指定的語言最佳化文字分析。
- **enableBotStoreReplicas**: 控制是否為機器人商店使用的 OpenSearch Serverless 集合啟用待命複本(預設: `false`)。設為 `true` 可提高可用性但會增加成本,而 `false` 則可降低成本但可能影響可用性。
  > **重要**: 集合建立後無法更新此屬性。如果您嘗試修改此屬性,集合將繼續使用原始值。

### 跨區域和全球推論

[跨區域和全球推論](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
允許 Amazon Bedrock 在多個 AWS 區域之間動態路由模型推論請求,在尖峰需求期間提高吞吐量和彈性。全球推論根據延遲和可用性將請求路由到世界上最佳的區域,而跨區域推論則在同一 AWS 區域內路由請求,例如在美國境內。某些 SCP 可能限制其中一個或兩個,因此您可以獨立設定它們。預設情況下兩者都啟用。

要設定,請在 `cdk.json` 或 `parameters.ts` 中更改以下設定:

```json
"enableBedrockGlobalInference": false,
"enableBedrockCrossRegionInference": false,
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) 改善了 Lambda 函數的冷啟動時間,提供更快的回應時間以獲得更好的使用者體驗。另一方面,對於 Python 函數,目前會根據[快取大小收費](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing),並且[在某些區域不可用](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)。要停用 SnapStart,請編輯 `cdk.json`。

```json
"enableLambdaSnapStart": false
```

### 設定自訂網域

您可以透過在 [cdk.json](./cdk/cdk.json) 中設定以下參數來為 CloudFront 分配設定自訂網域:

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: 聊天應用程式的自訂網域名稱(例如 chat.example.com)
- `hostedZoneId`: 將建立網域記錄的 Route 53 託管區域的 ID

提供這些參數後,部署將自動:

- 在 us-east-1 區域建立具有 DNS 驗證的 ACM 憑證
- 在您的 Route 53 託管區域中建立必要的 DNS 記錄
- 設定 CloudFront 使用您的自訂網域

> [!Note]
> 網域必須由您 AWS 帳戶中的 Route 53 管理。託管區域 ID 可以在 Route 53 控制台中找到。

### 設定允許的國家(地理限制)

您可以根據客戶端存取的國家來限制對 Bedrock-Chat 的存取。
使用 [cdk.json](./cdk/cdk.json) 中的 `allowedCountries` 參數,該參數接受 [ISO-3166 國家代碼](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) 列表。
例如,一家紐西蘭的企業可能決定只允許來自紐西蘭(NZ)和澳洲(AU)的 IP 地址存取入口網站,而拒絕其他所有人的存取。
要設定此行為,請在 [cdk.json](./cdk/cdk.json) 中使用以下設定:

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

或者,使用 `parameter.ts`(建議的類型安全方法):

```ts
// 為預設環境定義參數
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### 停用 IPv6 支援

前端預設會同時取得 IP 和 IPv6 地址。在某些罕見情況下,您可能需要明確停用 IPv6 支援。要執行此操作,請在 [parameter.ts](./cdk/parameter.ts) 或類似地在 [cdk.json](./cdk/cdk.json) 中設定以下參數:

```ts
"enableFrontendIpv6": false
```

如果未設定,則預設會啟用 IPv6 支援。

### 本地開發

請參閱 [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_zh-TW.md)。

### 貢獻

感謝您考慮為此儲存庫做出貢獻！我們歡迎錯誤修復、語言翻譯(i18n)、功能增強、[代理工具](./docs/AGENT.md#how-to-develop-your-own-tools)和其他改進。

對於功能增強和其他改進,**在建立拉取請求之前,我們非常感謝您能建立功能請求問題來討論實作方法和細節。對於錯誤修復和語言翻譯(i18n),請直接建立拉取請求。**

在貢獻之前,也請查看以下指南:

- [本地開發](./LOCAL_DEVELOPMENT_zh-TW.md)
- [CONTRIBUTING](./CONTRIBUTING_zh-TW.md)

## 聯絡方式

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 重要貢獻者

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## 貢獻者

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## 授權條款

此函式庫採用 MIT-0 授權條款。詳見[授權條款文件](./LICENSE)。