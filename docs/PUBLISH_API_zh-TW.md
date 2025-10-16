# API 發佈

## 概述

此範例包含了發布 API 的功能。雖然聊天介面對於初步驗證來說很方便，但實際的實作方式取決於特定的使用案例和期望的使用者體驗 (UX)。在某些情境下，聊天使用者介面可能是較佳的選擇，而在其他情況下，獨立的 API 可能更為合適。在初步驗證之後，此範例提供了根據專案需求發布客製化機器人的功能。透過輸入配額、節流、來源等設定，可以發布一個端點並配置 API 金鑰，為各種整合方案提供彈性選擇。

## 安全性

如 [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html) 中所述，不建議僅使用 API 金鑰。因此，此範例透過 AWS WAF 實作了簡單的 IP 位址限制。考慮到成本因素，WAF 規則被統一應用於整個應用程式，這是基於需要限制的來源在所有已發布的 API 中可能相同的假設。**實際實作時請遵循貴組織的安全政策。**另請參閱[架構](#architecture)章節。

## 如何發布客製化機器人 API

### 前置條件

基於管理原因，只有特定用戶可以發布機器人。在發布之前，用戶必須是名為 `PublishAllowed` 群組的成員，可以透過管理控制台 > Amazon Cognito User pools 或 aws cli 進行設定。請注意，可以通過訪問 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` 來查看使用者池 ID。

![](./imgs/group_membership_publish_allowed.png)

### API 發布設定

以 `PublishedAllowed` 用戶身份登入並建立機器人後，選擇 `API PublishSettings`。請注意，只有共享的機器人才能發布。
![](./imgs/bot_api_publish_screenshot.png)

在接下來的畫面中，我們可以配置幾個與流量限制相關的參數。詳細資訊請參考：[Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)。
![](./imgs/bot_api_publish_screenshot2.png)

部署完成後，將會出現以下畫面，您可以在此獲取端點 URL 和 API 金鑰。我們也可以新增和刪除 API 金鑰。

![](./imgs/bot_api_publish_screenshot3.png)

## 架構

API 的發佈如下圖所示:

![](./imgs/published_arch.png)

WAF 用於 IP 位址限制。可以通過在 `cdk.json` 中設置參數 `publishedApiAllowedIpV4AddressRanges` 和 `publishedApiAllowedIpV6AddressRanges` 來配置允許的位址。

當使用者點擊發佈機器人時，[AWS CodeBuild](https://aws.amazon.com/codebuild/) 會啟動 CDK 部署任務來配置 API 堆疊（另見：[CDK 定義](../cdk/lib/api-publishment-stack.ts)），其中包含 API Gateway、Lambda 和 SQS。由於生成輸出可能超過 API Gateway 配額限制的 30 秒，因此使用 SQS 來解耦使用者請求和 LLM 操作。要獲取輸出，需要非同步訪問 API。有關更多詳細信息，請參見 [API 規格](#api-specification)。

客戶端需要在請求標頭中設置 `x-api-key`。

## API 規格

請參閱[這裡](https://aws-samples.github.io/bedrock-chat)。