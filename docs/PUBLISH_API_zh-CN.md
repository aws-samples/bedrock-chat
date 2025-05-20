# API 发布

## 概述

此示例包含发布 API 的功能。虽然聊天界面对于初步验证很方便，但实际实现取决于特定用例和最终用户所需的用户体验（UX）。在某些情况下，聊天用户界面可能是首选，而在其他情况下，独立的 API 可能更为合适。在初步验证后，此示例提供了根据项目需求发布自定义机器人的能力。通过输入配额、限流、来源等设置，可以发布端点并附带 API 密钥，为不同的集成选项提供灵活性。

## 安全性

仅使用 API 密钥是不推荐的，如 [AWS API Gateway 开发者指南](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html) 中所述。因此，此示例通过 AWS WAF 实现了简单的 IP 地址限制。出于成本考虑，WAF 规则通常应用于整个应用程序，假设希望限制的源在所有已发布的 API 中可能是相同的。**对于实际实施，请遵循您组织的安全策略。**另请参阅 [架构](#architecture) 部分。

## 如何发布自定义机器人 API

### 先决条件

出于治理原因，只有有限的用户能够发布机器人。发布之前，用户必须是名为 `PublishAllowed` 的组的成员，该组可以通过管理控制台 > Amazon Cognito 用户池或 AWS CLI 设置。请注意，可以通过访问 CloudFormation > BedrockChatStack > 输出 > `AuthUserPoolIdxxxx` 来引用用户池 ID。

![](./imgs/group_membership_publish_allowed.png)

### API 发布设置

以 `PublishedAllowed` 用户登录并创建机器人后，选择 `API 发布设置`。请注意，只有共享机器人可以发布。
![](./imgs/bot_api_publish_screenshot.png)

在以下屏幕中，我们可以配置关于限流的几个参数。详细信息，请参见：[限制 API 请求以提高吞吐量](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)。
![](./imgs/bot_api_publish_screenshot2.png)

部署后，将出现以下屏幕，您可以获取端点 URL 和 API 密钥。我们还可以添加和删除 API 密钥。

![](./imgs/bot_api_publish_screenshot3.png)

## 架构

API 按照以下图表发布：

![](./imgs/published_arch.png)

WAF 用于 IP 地址限制。可以通过在 `cdk.json` 中设置参数 `publishedApiAllowedIpV4AddressRanges` 和 `publishedApiAllowedIpV6AddressRanges` 来配置地址。

当用户点击发布机器人时，[AWS CodeBuild](https://aws.amazon.com/codebuild/) 启动 CDK 部署任务以配置 API 堆栈（另请参见：[CDK 定义](../cdk/lib/api-publishment-stack.ts)），该堆栈包含 API Gateway、Lambda 和 SQS。使用 SQS 解耦用户请求和 LLM 操作，因为生成输出可能超过 30 秒，这是 API Gateway 配额的限制。要获取输出，需要异步访问 API。更多详情请参见 [API 规范](#api-specification)。

客户端需要在请求标头中设置 `x-api-key`。

## API规范

请查看[此处](https://aws-samples.github.io/bedrock-chat)。