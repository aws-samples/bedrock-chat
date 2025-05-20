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

一个由 [Amazon Bedrock](https://aws.amazon.com/bedrock/) 驱动的多语言生成式人工智能平台。
支持聊天、带知识的自定义机器人（RAG）、通过机器人商店共享机器人以及使用代理进行任务自动化。

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 已发布。更新时，请仔细查看 [迁移指南](./migration/V2_TO_V3_zh-CN.md)。** 不小心操作可能会导致 **V2 版本的机器人无法使用。**

### 机器人个性化 / 机器人商店

添加您自己的指令和知识（又称 [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。机器人可以通过机器人商店市场在应用程序用户之间共享。自定义机器人还可以发布为独立的 API（请参见 [详情](./PUBLISH_API_zh-CN.md)）。

<details>
<summary>屏幕截图</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

您还可以导入现有的 [Amazon Bedrock 知识库](https://aws.amazon.com/bedrock/knowledge-bases/)。

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> 出于治理原因，只有允许的用户才能创建自定义机器人。要允许创建自定义机器人，用户必须是名为 `CreatingBotAllowed` 的组的成员，可以通过管理控制台 > Amazon Cognito 用户池或 AWS CLI 设置。请注意，可以通过访问 CloudFormation > BedrockChatStack > 输出 > `AuthUserPoolIdxxxx` 来查看用户池 ID。

### 管理功能

API 管理、标记重要机器人、分析机器人使用情况。[详情](./ADMINISTRATOR_zh-CN.md)

<details>
<summary>屏幕截图</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### 代理

通过使用 [代理功能](./AGENT_zh-CN.md)，您的聊天机器人可以自动处理更复杂的任务。例如，要回答用户的问题，代理可以从外部工具检索必要的信息，或将任务分解为多个步骤进行处理。

<details>
<summary>屏幕截图</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超级简单的部署

- 在 us-east-1 区域，打开 [Bedrock 模型访问](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `管理模型访问` > 勾选您想要使用的所有模型，然后点击 `保存更改`。

<details>
<summary>截图</summary>

![](./imgs/model_screenshot.png)

</details>

- 在您想要部署的区域打开 [CloudShell](https://console.aws.amazon.com/cloudshell/home)
- 通过以下命令运行部署。如果您想指定部署的版本或需要应用安全策略，请从[可选参数](#optional-parameters)中指定适当的参数。

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- 系统会询问是新用户还是使用 v3。如果您不是 v0 的延续用户，请输入 `y`。

### 可选参数

您可以在部署期间指定以下参数以增强安全性和自定义性：

- **--disable-self-register**：禁用自注册（默认：启用）。如果设置此标志，您将需要在 Cognito 上创建所有用户，并且不允许用户自行注册账户。
- **--enable-lambda-snapstart**：启用 [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)（默认：禁用）。如果设置此标志，将改善 Lambda 函数的冷启动时间，提供更快的响应时间，以获得更好的用户体验。
- **--ipv4-ranges**：允许的 IPv4 地址范围的逗号分隔列表。（默认：允许所有 IPv4 地址）
- **--ipv6-ranges**：允许的 IPv6 地址范围的逗号分隔列表。（默认：允许所有 IPv6 地址）
- **--disable-ipv6**：禁用 IPv6 连接。（默认：启用）
- **--allowed-signup-email-domains**：允许注册的电子邮件域名的逗号分隔列表。（默认：无域名限制）
- **--bedrock-region**：定义 Bedrock 可用的区域。（默认：us-east-1）
- **--repo-url**：要部署的 Bedrock Chat 的自定义仓库，如果是 fork 或自定义源代码控制。（默认：https://github.com/aws-samples/bedrock-chat.git）
- **--version**：要部署的 Bedrock Chat 版本。（默认：开发中的最新版本）
- **--cdk-json-override**：您可以在部署期间使用覆盖 JSON 块覆盖任何 CDK 上下文值。这允许您在不直接编辑 cdk.json 文件的情况下修改配置。

使用示例：

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

覆盖 JSON 必须遵循与 cdk.json 相同的结构。您可以覆盖任何上下文值，包括：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- 以及 cdk.json 中定义的其他上下文值

> [!Note]
> 覆盖值将在 AWS 代码构建部署期间与现有的 cdk.json 配置合并。指定的覆盖值将优先于 cdk.json 中的值。

#### 带参数的示例命令：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 大约 35 分钟后，您将获得以下输出，可以从浏览器访问

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

将出现如上所示的注册屏幕，您可以在其中注册您的电子邮件并登录。

> [!Important]
> 如果不设置可选参数，此部署方法允许任何知道 URL 的人注册。对于生产使用，强烈建议添加 IP 地址限制并禁用自注册，以降低安全风险（您可以定义 allowed-signup-email-domains 以限制用户，使只有来自贵公司域名的电子邮件地址可以注册）。在执行 ./bin 时同时使用 ipv4-ranges 和 ipv6-ranges 进行 IP 地址限制，并通过使用 disable-self-register 禁用自注册。

> [!TIP]
> 如果 `Frontend URL` 未出现或 Bedrock Chat 无法正常工作，可能是最新版本的问题。在这种情况下，请在参数中添加 `--version "v3.0.0"`，然后重试部署。

## 架构

这是一个基于 AWS 托管服务构建的架构，无需基础设施管理。通过使用 Amazon Bedrock，无需与 AWS 外部的 API 通信。这使得部署可扩展、可靠和安全的应用程序成为可能。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：用于存储对话历史的 NoSQL 数据库
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：后端 API 端点（[AWS Lambda Web 适配器](https://github.com/awslabs/aws-lambda-web-adapter)，[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：前端应用程序交付（[React](https://react.dev/)，[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/)：IP 地址限制
- [Amazon Cognito](https://aws.amazon.com/cognito/)：用户认证
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：通过 API 利用基础模型的托管服务
- [Amazon Bedrock 知识库](https://aws.amazon.com/bedrock/knowledge-bases/)：提供检索增强生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）的托管接口，提供文档嵌入和解析服务
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：从 DynamoDB 流接收事件并启动 Step Functions 以嵌入外部知识
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：编排嵌入外部知识到 Bedrock 知识库的摄取管道
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：作为 Bedrock 知识库的后端数据库，提供全文搜索和向量搜索功能，实现准确检索相关信息
- [Amazon Athena](https://aws.amazon.com/athena/)：查询服务，用于分析 S3 存储桶

![](./imgs/arch.png)

## 使用 CDK 部署

超级简单的部署使用 [AWS CodeBuild](https://aws.amazon.com/codebuild/) 在内部通过 CDK 执行部署。本节描述直接使用 CDK 部署的步骤。

- 请准备 UNIX、Docker 和 Node.js 运行时环境。如果没有，也可以使用 [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!重要]
> 如果在部署过程中本地环境存储空间不足，CDK 引导可能会导致错误。如果您在 Cloud9 等环境中运行，建议在部署前扩展实例的卷大小。

- 克隆此仓库

```
git clone https://github.com/aws-samples/bedrock-chat
```

- 安装 npm 包

```
cd bedrock-chat
cd cdk
npm ci
```

- 如有必要，编辑 [cdk.json](./cdk/cdk.json) 中的以下条目

  - `bedrockRegion`：Bedrock 可用的区域。**注意：目前 Bedrock 不支持所有区域。**
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`：允许的 IP 地址范围。
  - `enableLambdaSnapStart`：默认为 true。如果部署到[不支持 Python 函数 Lambda SnapStart 的区域](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)，请设置为 false。

- 在部署 CDK 之前，需要为要部署的区域进行一次引导

```
npx cdk bootstrap
```

- 部署此示例项目

```
npx cdk deploy --require-approval never --all
```

- 您将获得类似以下的输出。Web 应用的 URL 将在 `BedrockChatStack.FrontendURL` 中输出，请从浏览器访问。

```sh
 ✅  BedrockChatStack

✨  部署时间: 78.57s

输出:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### 定义参数

您可以通过两种方式定义部署参数：使用 `cdk.json` 或使用类型安全的 `parameter.ts` 文件。

#### 使用 cdk.json（传统方法）

配置参数的传统方式是编辑 `cdk.json` 文件。这种方法简单，但缺乏类型检查：

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

#### 使用 parameter.ts（推荐的类型安全方法）

为了获得更好的类型安全性和开发体验，您可以使用 `parameter.ts` 文件定义参数：

```typescript
// 为默认环境定义参数
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// 为其他环境定义参数
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 开发环境节省成本
  enableBotStoreReplicas: false, // 开发环境节省成本
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 生产环境增强可用性
  enableBotStoreReplicas: true, // 生产环境增强可用性
});
```

> [!注意]
> 现有用户可以继续使用 `cdk.json` 而无需任何更改。对于新部署或需要管理多个环境，推荐使用 `parameter.ts` 方法。

### 部署多个环境

您可以使用 `parameter.ts` 文件和 `-c envName` 选项从同一代码库部署多个环境。

#### 先决条件

1. 在 `parameter.ts` 中按上述方式定义环境
2. 每个环境将有其自己的资源，并带有特定于环境的前缀

#### 部署命令

部署特定环境：

```bash
# 部署开发环境
npx cdk deploy --all -c envName=dev

# 部署生产环境
npx cdk deploy --all -c envName=prod
```

如果未指定环境，则使用"默认"环境：

```bash
# 部署默认环境
npx cdk deploy --all
```

#### 重要说明

1. **堆栈命名**：

   - 每个环境的主要堆栈将以环境名为前缀（例如，`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - 但是，自定义机器人堆栈（`BrChatKbStack*`）和 API 发布堆栈（`ApiPublishmentStack*`）不会收到环境前缀，因为它们是在运行时动态创建的

2. **资源命名**：

   - 只有一些资源在名称中接收环境前缀（例如，`dev_ddb_export` 表，`dev-FrontendWebAcl`）
   - 大多数资源保持其原始名称，但通过位于不同堆栈中而隔离

3. **环境标识**：

   - 所有资源都使用包含环境名称的 `CDKEnvironment` 标签进行标记
   - 您可以使用此标签识别资源属于哪个环境
   - 示例：`CDKEnvironment: dev` 或 `CDKEnvironment: prod`

4. **默认环境覆盖**：如果在 `parameter.ts` 中定义了"默认"环境，它将覆盖 `cdk.json` 中的设置。要继续使用 `cdk.json`，请不要在 `parameter.ts` 中定义"默认"环境。

5. **环境要求**：要创建"默认"以外的环境，必须使用 `parameter.ts`。仅使用 `-c envName` 选项是不够的，必须有相应的环境定义。

6. **资源隔离**：每个环境都会创建自己的资源集，允许您在同一个 AWS 账户中拥有开发、测试和生产环境，且不会发生冲突。

## 其他

您可以通过两种方式为部署定义参数：使用 `cdk.json` 或使用类型安全的 `parameter.ts` 文件。

#### 使用 cdk.json（传统方法）

配置参数的传统方法是编辑 `cdk.json` 文件。这种方法简单，但缺乏类型检查：

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

#### 使用 parameter.ts（推荐的类型安全方法）

为了获得更好的类型安全性和开发者体验，您可以使用 `parameter.ts` 文件来定义参数：

```typescript
// 为默认环境定义参数
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// 为其他环境定义参数
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 开发环境节省成本
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 生产环境增强可用性
});
```

> [!注意]
> 现有用户可以继续使用 `cdk.json` 而无需任何更改。对于新部署或需要管理多个环境，推荐使用 `parameter.ts` 方法。

### 部署多个环境

您可以使用 `parameter.ts` 文件和 `-c envName` 选项从同一代码库部署多个环境。

#### 先决条件

1. 如上所示在 `parameter.ts` 中定义您的环境
2. 每个环境都将有其自己的资源，并带有环境特定的前缀

#### 部署命令

部署特定环境：

```bash
# 部署开发环境
npx cdk deploy --all -c envName=dev

# 部署生产环境
npx cdk deploy --all -c envName=prod
```

如果未指定环境，则使用"default"环境：

```bash
# 部署默认环境
npx cdk deploy --all
```

#### 重要说明

1. **堆栈命名**：

   - 每个环境的主堆栈将以环境名称为前缀（例如 `dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - 但是，自定义机器人堆栈（`BrChatKbStack*`）和 API 发布堆栈（`ApiPublishmentStack*`）不会收到环境前缀，因为它们是在运行时动态创建的

2. **资源命名**：

   - 只有部分资源会在其名称中收到环境前缀（例如 `dev_ddb_export` 表，`dev-FrontendWebAcl`）
   - 大多数资源保持其原始名称，但通过位于不同堆栈中而实现隔离

3. **环境标识**：

   - 所有资源都带有 `CDKEnvironment` 标签，包含环境名称
   - 您可以使用此标签识别资源属于哪个环境
   - 示例：`CDKEnvironment: dev` 或 `CDKEnvironment: prod`

4. **默认环境覆盖**：如果在 `parameter.ts` 中定义了"default"环境，它将覆盖 `cdk.json` 中的设置。要继续使用 `cdk.json`，请不要在 `parameter.ts` 中定义"default"环境。

5. **环境要求**：要创建"default"以外的环境，必须使用 `parameter.ts`。仅使用 `-c envName` 选项是不够的，还需要相应的环境定义。

6. **资源隔离**：每个环境都会创建自己的资源集，允许您在同一个 AWS 账户中拥有开发、测试和生产环境，且不会发生冲突。

## 其他

### 删除资源

如果使用 CLI 和 CDK，请使用 `npx cdk destroy`。如果不是，请访问 [CloudFormation](https://console.aws.amazon.com/cloudformation/home)，然后手动删除 `BedrockChatStack` 和 `FrontendWafStack`。请注意 `FrontendWafStack` 位于 `us-east-1` 区域。

### 语言设置

该资源使用 [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector) 自动检测语言。您可以从应用程序菜单切换语言。或者，您可以使用查询字符串设置语言，如下所示。

> `https://example.com?lng=ja`

### 禁用自助注册

此示例默认启用自助注册。要禁用自助注册，请打开 [cdk.json](./cdk/cdk.json) 并将 `selfSignUpEnabled` 设置为 `false`。如果配置了[外部身份提供者](#external-identity-provider)，则该值将被忽略并自动禁用。

### 限制注册邮箱地址的域名

默认情况下，此示例不限制注册邮箱地址的域名。要仅允许来自特定域名的注册，请打开 `cdk.json` 并在 `allowedSignUpEmailDomains` 中指定域名列表。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部身份提供者

此示例支持外部身份提供者。目前我们支持 [Google](./idp/SET_UP_GOOGLE_zh-CN.md) 和[自定义 OIDC 提供者](./idp/SET_UP_CUSTOM_OIDC_zh-CN.md)。

### 自动将新用户添加到组

此示例具有以下组以授予用户权限：

- [`Admin`](./ADMINISTRATOR_zh-CN.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_zh-CN.md)

如果希望新创建的用户自动加入组，可以在 [cdk.json](./cdk/cdk.json) 中指定。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

默认情况下，新创建的用户将加入 `CreatingBotAllowed` 组。

### 配置 RAG 副本

[cdk.json](./cdk/cdk.json) 中的 `enableRagReplicas` 选项控制 RAG 数据库的副本设置，特别是使用 Amazon OpenSearch Serverless 的知识库。

- **默认**：true
- **true**：通过启用额外副本来增强可用性，适合生产环境，但会增加成本。
- **false**：通过减少副本来降低成本，适合开发和测试。

这是一个账户/区域级别的设置，影响整个应用程序，而不是单个机器人。

> [!注意]
> 截至 2024 年 6 月，Amazon OpenSearch Serverless 支持 0.5 OCU，降低了小规模工作负载的入门成本。生产部署可以从 2 个 OCU 开始，而开发/测试工作负载可以使用 1 个 OCU。OpenSearch Serverless 将根据工作负载需求自动扩展。更多详情请访问[公告](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)。

### 配置机器人商店

机器人商店功能允许用户共享和发现自定义机器人。您可以通过 [cdk.json](./cdk/cdk.json) 中的以下设置配置机器人商店：

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**：控制是否启用机器人商店功能（默认：`true`）
- **botStoreLanguage**：设置机器人搜索和发现的主要语言（默认：`"en"`）。这会影响机器人在机器人商店中的索引和搜索方式，为指定语言优化文本分析。
- **enableBotStoreReplicas**：控制机器人商店使用的 OpenSearch Serverless 集合是否启用备用副本（默认：`false`）。将其设置为 `true` 可提高可用性但会增加成本，而 `false` 可降低成本但可能影响可用性。
  > **重要**：创建集合后无法更新此属性。如果尝试修改此属性，集合将继续使用原始值。

### 跨区域推理

[跨区域推理](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)允许 Amazon Bedrock 在多个 AWS 区域动态路由模型推理请求，在高峰需求期间提高吞吐量和弹性。要配置，请编辑 `cdk.json`。

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) 改善 Lambda 函数的冷启动时间，为更好的用户体验提供更快的响应时间。另一方面，对于 Python 函数，根据缓存大小有[相应的费用](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)，并且[目前在某些区域不可用](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)。要禁用 SnapStart，请编辑 `cdk.json`。

```json
"enableLambdaSnapStart": false
```

### 配置自定义域名

您可以通过在 [cdk.json](./cdk/cdk.json) 中设置以下参数来为 CloudFront 分配配置自定义域名：

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`：聊天应用程序的自定义域名（例如 chat.example.com）
- `hostedZoneId`：将创建域名记录的 Route 53 托管区域的 ID

提供这些参数后，部署将自动：

- 在 us-east-1 区域创建带有 DNS 验证的 ACM 证书
- 在您的 Route 53 托管区域中创建必要的 DNS 记录
- 配置 CloudFront 使用您的自定义域名

> [!注意]
> 域名必须在您的 AWS 账户中由 Route 53 管理。可以在 Route 53 控制台中找到托管区域 ID。

### 本地开发

请参见 [本地开发](./LOCAL_DEVELOPMENT_zh-CN.md)。

### 贡献

感谢您考虑为此仓库做出贡献！我们欢迎修复 bug、语言翻译（i18n）、功能增强、[代理工具](./docs/AGENT.md#how-to-develop-your-own-tools)和其他改进。

对于功能增强和其他改进，**在创建拉取请求之前，我们非常希望您能创建一个功能请求 Issue 来讨论实施方法和细节。对于 bug 修复和语言翻译（i18n），可以直接创建拉取请求。**

在贡献之前，请也查看以下指南：

- [本地开发](./LOCAL_DEVELOPMENT_zh-CN.md)
- [贡献指南](./CONTRIBUTING_zh-CN.md)

## 联系人

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 重要贡献者

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## 贡献者

[![bedrock chat 贡献者](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## 许可证

本库在 MIT-0 许可证下授权。请参见 [LICENSE 文件](./LICENSE)。