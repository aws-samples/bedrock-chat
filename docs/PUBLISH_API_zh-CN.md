# API 发布

## 概述

此示例包含了发布 API 的功能。虽然聊天界面对于初步验证来说很方便，但实际实现取决于具体的使用场景和期望的最终用户体验(UX)。在某些情况下，聊天界面可能是首选，而在其他情况下，独立的 API 可能更合适。在初步验证之后，此示例提供了根据项目需求发布自定义机器人的功能。通过输入配额、限流、来源等设置，可以发布带有 API 密钥的端点，为各种集成选项提供灵活性。

## 安全性

如[AWS API Gateway开发者指南](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)中所述，仅使用API密钥的方式是不推荐的。因此，本示例通过AWS WAF实现了一个简单的IP地址限制。出于成本考虑，WAF规则被统一应用于整个应用程序，这是基于需要限制的来源在所有已发布的API中可能是相同的这一假设。**在实际实施时，请遵循贵组织的安全政策。**另请参阅[架构](#architecture)部分。

## 如何发布自定义机器人 API

### 前提条件

出于治理原因，只有有限的用户能够发布机器人。在发布之前，用户必须是名为 `PublishAllowed` 组的成员，该组可以通过管理控制台 > Amazon Cognito User pools 或 aws cli 进行设置。请注意，可以通过访问 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` 来查找用户池 ID。

![](./imgs/group_membership_publish_allowed.png)

### API 发布设置

以 `PublishedAllowed` 用户身份登录并创建机器人后，选择 `API PublishSettings`。请注意，只有共享的机器人才能发布。
![](./imgs/bot_api_publish_screenshot.png)

在下面的界面中，我们可以配置几个与限流相关的参数。详细信息请参见：[Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)。
![](./imgs/bot_api_publish_screenshot2.png)

部署后，将出现以下界面，您可以在其中获取端点 URL 和 API 密钥。我们还可以添加和删除 API 密钥。

![](./imgs/bot_api_publish_screenshot3.png)

## 架构

API 的发布如下图所示：

![](./imgs/published_arch.png)

WAF 用于 IP 地址限制。可以通过在 `cdk.json` 中设置参数 `publishedApiAllowedIpV4AddressRanges` 和 `publishedApiAllowedIpV6AddressRanges` 来配置地址。

当用户点击发布机器人时，[AWS CodeBuild](https://aws.amazon.com/codebuild/) 启动 CDK 部署任务来配置 API 堆栈（另见：[CDK 定义](../cdk/lib/api-publishment-stack.ts)），其中包含 API Gateway、Lambda 和 SQS。使用 SQS 来解耦用户请求和 LLM 操作，因为生成输出可能超过 30 秒，这是 API Gateway 配额的限制。要获取输出，需要异步访问 API。有关更多详细信息，请参阅 [API 规范](#api-specification)。

客户端需要在请求头中设置 `x-api-key`。

## API 规范

参见[此处](https://aws-samples.github.io/bedrock-chat)。