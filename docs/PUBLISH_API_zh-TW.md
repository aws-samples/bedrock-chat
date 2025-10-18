# API 發布

## 概述

此範例包含發布 API 的功能。雖然聊天界面對於初步驗證來說很方便，但實際的實作取決於特定的使用案例和期望達到的終端使用者體驗 (UX)。在某些情況下，聊天界面可能是較佳的選擇，而在其他情況下，獨立的 API 可能更為合適。在初步驗證之後，此範例提供了根據專案需求發布客製化機器人的功能。透過輸入配額、節流、來源等設定，可以發布一個端點以及 API 金鑰，為各種整合選項提供靈活性。

## 安全性

如 [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html) 所述，不建議僅使用 API 金鑰。因此，本範例透過 AWS WAF 實作了簡單的 IP 位址限制。考量到成本因素，且假設在所有發布的 API 中，想要限制的來源可能都是相同的，因此 WAF 規則會統一套用於整個應用程式。**實際實作時請遵循貴組織的安全政策。**另請參閱 [Architecture](#architecture) 章節。

## 如何發布自訂聊天機器人 API

### 前置條件

基於治理原因，只有少數使用者可以發布聊天機器人。在發布之前，使用者必須是名為 `PublishAllowed` 群組的成員，可以透過管理控制台 > Amazon Cognito User pools 或 aws cli 來設定。請注意，可以透過存取 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` 來參考使用者池 ID。

![](./imgs/group_membership_publish_allowed.png)

### API 發布設定

以 `PublishedAllowed` 使用者身份登入並建立聊天機器人後，選擇 `API PublishSettings`。請注意，只有共享的聊天機器人才能發布。
![](./imgs/bot_api_publish_screenshot.png)

在下一個畫面中，我們可以設定幾個與流量限制相關的參數。詳細資訊請參考：[Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)。
![](./imgs/bot_api_publish_screenshot2.png)

部署後，將會出現以下畫面，您可以在其中獲取端點 URL 和 API 金鑰。我們還可以新增和刪除 API 金鑰。

![](./imgs/bot_api_publish_screenshot3.png)

## 架構

API 的發布如下圖所示：

![](./imgs/published_arch.png)

WAF 用於 IP 位址限制。可以通過在 `cdk.json` 中設置參數 `publishedApiAllowedIpV4AddressRanges` 和 `publishedApiAllowedIpV6AddressRanges` 來配置地址。

當用戶點擊發布機器人時，[AWS CodeBuild](https://aws.amazon.com/codebuild/) 會啟動 CDK 部署任務來配置 API 堆疊（另見：[CDK 定義](../cdk/lib/api-publishment-stack.ts)），其中包含 API Gateway、Lambda 和 SQS。由於生成輸出可能超過 30 秒（這是 API Gateway 配額的限制），因此使用 SQS 來解耦用戶請求和 LLM 操作。要獲取輸出，需要非同步訪問 API。有關更多詳細信息，請參見 [API 規範](#api-specification)。

客戶端需要在請求標頭中設置 `x-api-key`。

## API 規格說明

請參閱[此處](https://aws-samples.github.io/bedrock-chat)。