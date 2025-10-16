# API 发布

## 概述

此示例包含一个用于发布API的功能。虽然聊天界面对于初步验证来说很方便，但实际实现取决于特定用例和期望的最终用户体验(UX)。在某些场景中，聊天界面可能是首选，而在其他场景中，独立的API可能更合适。在初步验证之后，此示例提供了根据项目需求发布定制机器人的功能。通过输入配额、限流、来源等设置，可以发布一个带有API密钥的端点，为各种集成选项提供灵活性。

## 安全性

如[AWS API Gateway开发者指南](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)中所述，仅使用API密钥的方式并不推荐。因此，本示例通过AWS WAF实现了一个简单的IP地址限制。考虑到成本因素，WAF规则被统一应用于整个应用程序，这是基于需要限制的来源在所有已发布的API中可能相同的假设。**在实际实施时，请遵循您所在组织的安全策略。**另请参阅[架构](#architecture)部分。

## 如何发布自定义机器人 API

### 前提条件

出于治理原因，只有有限的用户能够发布机器人。在发布之前，用户必须是名为 `PublishAllowed` 群组的成员，该群组可以通过管理控制台 > Amazon Cognito User pools 或 aws cli 进行设置。请注意，可以通过访问 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` 来获取用户池 ID。

![](./imgs/group_membership_publish_allowed.png)

### API 发布设置

以 `PublishedAllowed` 用户身份登录并创建机器人后，选择 `API PublishSettings`。请注意，只有共享的机器人才能被发布。
![](./imgs/bot_api_publish_screenshot.png)

在接下来的界面中，我们可以配置几个与限流相关的参数。详细信息请参见：[Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)。
![](./imgs/bot_api_publish_screenshot2.png)

部署后，将出现以下界面，您可以在其中获取端点 URL 和 API 密钥。我们还可以添加和删除 API 密钥。

![](./imgs/bot_api_publish_screenshot3.png)

## 架构

API的发布架构如下图所示：

![](./imgs/published_arch.png)

WAF用于IP地址限制。可以通过在`cdk.json`中设置参数`publishedApiAllowedIpV4AddressRanges`和`publishedApiAllowedIpV6AddressRanges`来配置允许访问的地址。

当用户点击发布机器人时，[AWS CodeBuild](https://aws.amazon.com/codebuild/)会启动CDK部署任务来配置API堆栈（另见：[CDK定义](../cdk/lib/api-publishment-stack.ts)），其中包含API Gateway、Lambda和SQS。使用SQS是为了解耦用户请求和LLM操作，因为生成输出可能超过30秒，这是API Gateway配额的限制。要获取输出，需要异步访问API。更多详细信息，请参见[API规范](#api-specification)。

客户端需要在请求头中设置`x-api-key`。

## API 规范

请参见[此处](https://aws-samples.github.io/bedrock-chat)。