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


一个由[Amazon Bedrock](https://aws.amazon.com/bedrock/)驱动的多语言生成式AI平台。
支持聊天、具有知识库的自定义机器人（RAG）、通过机器人商店分享机器人，以及使用代理进行任务自动化。

![](./imgs/demo.gif)

> [!Warning]
>
> **V3已发布。要更新，请仔细阅读[迁移指南](./migration/V2_TO_V3_zh-CN.md)。** 如果不注意，**V2版本的机器人将变得不可用。**

### 机器人个性化 / 机器人商店

添加您自己的指令和知识（即[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。机器人可以通过机器人商店市场在应用程序用户之间共享。定制的机器人还可以作为独立的API发布（查看[详情](./PUBLISH_API_zh-CN.md)）。

<details>
<summary>截图</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

您还可以导入现有的[Amazon Bedrock's KnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/)。

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> 出于治理原因，只有获得允许的用户才能创建定制机器人。要允许创建定制机器人，用户必须是名为`CreatingBotAllowed`群组的成员，可以通过管理控制台 > Amazon Cognito User pools或aws cli进行设置。请注意，可以通过访问CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`来查看用户池ID。

### 管理功能

API管理、将机器人标记为必需、分析机器人使用情况。[详情](./ADMINISTRATOR_zh-CN.md)

<details>
<summary>截图</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### 代理

通过使用[代理功能](./AGENT_zh-CN.md)，您的聊天机器人可以自动处理更复杂的任务。例如，为了回答用户的问题，代理可以从外部工具检索必要的信息或将任务分解为多个步骤进行处理。

<details>
<summary>截图</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超简单部署

- 在 us-east-1 区域,打开 [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > 勾选所有你想使用的模型然后点击 `Save changes`。

<details>
<summary>截图</summary>

![](./imgs/model_screenshot.png)

</details>

### 支持的区域

如果你想使用机器人和创建知识库(OpenSearch Serverless 是默认选择),请确保你在[OpenSearch Serverless 和 Ingestion APIs 可用的区域](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html)部署 Bedrock Chat。截至 2025 年 8 月,支持以下区域:us-east-1、us-east-2、us-west-1、us-west-2、ap-south-1、ap-northeast-1、ap-northeast-2、ap-southeast-1、ap-southeast-2、ca-central-1、eu-central-1、eu-west-1、eu-west-2、eu-south-2、eu-north-1、sa-east-1

对于 **bedrock-region** 参数,你需要选择一个 [Bedrock 可用的区域](https://docs.aws.amazon.com/general/latest/gr/bedrock.html)。

- 在你想要部署的区域打开 [CloudShell](https://console.aws.amazon.com/cloudshell/home)
- 通过以下命令运行部署。如果你想指定要部署的版本或需要应用安全策略,请从[可选参数](#optional-parameters)中指定适当的参数。

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- 系统会询问你是否是新用户或使用 v3。如果你不是从 v0 升级的用户,请输入 `y`。

### 可选参数

你可以在部署期间指定以下参数来增强安全性和自定义性:

- **--disable-self-register**: 禁用自助注册(默认:启用)。如果设置此标志,你需要在 cognito 上创建所有用户,并且不允许用户自行注册账户。
- **--enable-lambda-snapstart**: 启用 [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)(默认:禁用)。如果设置此标志,可以改善 Lambda 函数的冷启动时间,提供更快的响应时间以获得更好的用户体验。
- **--ipv4-ranges**: 允许的 IPv4 范围列表,用逗号分隔。(默认:允许所有 ipv4 地址)
- **--ipv6-ranges**: 允许的 IPv6 范围列表,用逗号分隔。(默认:允许所有 ipv6 地址)
- **--disable-ipv6**: 禁用 IPv6 连接。(默认:启用)
- **--allowed-signup-email-domains**: 允许注册的电子邮件域名列表,用逗号分隔。(默认:无域名限制)
- **--bedrock-region**: 定义 bedrock 可用的区域。(默认:us-east-1)
- **--repo-url**: 要部署的 Bedrock Chat 的自定义仓库,如果是 fork 或自定义源代码控制。(默认:https://github.com/aws-samples/bedrock-chat.git)
- **--version**: 要部署的 Bedrock Chat 版本。(默认:开发中的最新版本)
- **--cdk-json-override**: 你可以在部署期间使用覆盖 JSON 块覆盖任何 CDK 上下文值。这允许你在不直接编辑 cdk.json 文件的情况下修改配置。

使用示例:

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

覆盖 JSON 必须遵循与 cdk.json 相同的结构。你可以覆盖任何上下文值,包括:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: 接受要启用的模型 ID 列表。默认值为空列表,这将启用所有模型。
- `logoPath`: 前端 `public/` 目录中出现在导航抽屉顶部的 logo 资产的相对路径。
- 以及 cdk.json 中定义的其他上下文值

> [!Note]
> 覆盖值将在 AWS code build 的部署时与现有的 cdk.json 配置合并。覆盖中指定的值将优先于 cdk.json 中的值。

#### 带参数的示例命令:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 大约 35 分钟后,你将获得以下输出,你可以从浏览器访问

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

将出现如上所示的注册界面,你可以在此注册电子邮件并登录。

> [!Important]
> 如果不设置可选参数,此部署方法允许任何知道 URL 的人注册。对于生产环境使用,强烈建议添加 IP 地址限制并禁用自助注册以降低安全风险(你可以定义 allowed-signup-email-domains 来限制用户,使得只有来自你公司域名的电子邮件地址才能注册)。执行 ./bin 时使用 ipv4-ranges 和 ipv6-ranges 进行 IP 地址限制,并使用 disable-self-register 禁用自助注册。

> [!TIP]
> 如果 `Frontend URL` 没有出现或 Bedrock Chat 无法正常工作,可能是最新版本的问题。在这种情况下,请在参数中添加 `--version "v3.0.0"` 并重新尝试部署。

## 架构

这是一个基于 AWS 托管服务构建的架构，无需进行基础设施管理。通过使用 Amazon Bedrock，无需与 AWS 外部的 API 通信。这使得可以部署可扩展、可靠且安全的应用程序。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): 用于存储对话历史的 NoSQL 数据库
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): 后端 API 端点 ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): 前端应用程序分发 ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP 地址限制
- [Amazon Cognito](https://aws.amazon.com/cognito/): 用户认证
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): 通过 API 使用基础模型的托管服务
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): 为检索增强生成 ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)) 提供托管接口，提供文档嵌入和解析服务
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): 接收来自 DynamoDB 流的事件并启动 Step Functions 以嵌入外部知识
- [AWS Step Functions](https://aws.amazon.com/step-functions/): 编排引入管道，将外部知识嵌入到 Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): 作为 Bedrock Knowledge Bases 的后端数据库，提供全文搜索和向量搜索功能，实现准确的相关信息检索
- [Amazon Athena](https://aws.amazon.com/athena/): 用于分析 S3 存储桶的查询服务

![](./imgs/arch.png)

## 使用 CDK 部署

超简单部署内部使用 [AWS CodeBuild](https://aws.amazon.com/codebuild/) 通过 CDK 执行部署。本节描述直接使用 CDK 部署的步骤。

- 请准备 UNIX、Docker 和 Node.js 运行环境。

> [!Important]
> 如果在部署期间本地环境存储空间不足，CDK 引导可能会导致错误。我们建议在部署前扩展实例的卷大小。

- 克隆此存储库

```
git clone https://github.com/aws-samples/bedrock-chat
```

- 安装 npm 包

```
cd bedrock-chat
cd cdk
npm ci
```

- 如有必要，编辑 [cdk.json](./cdk/cdk.json) 中的以下条目。

  - `bedrockRegion`: Bedrock 可用的区域。**注意：Bedrock 目前不支持所有区域。**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: 允许的 IP 地址范围。
  - `enableLambdaSnapStart`: 默认为 true。如果部署到[不支持 Python 函数 Lambda SnapStart 的区域](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)，则设置为 false。
  - `globalAvailableModels`: 默认为全部。如果设置（模型 ID 列表），可以在 Bedrock Chat 应用程序中全局控制所有用户的聊天下拉菜单和创建机器人时显示的模型。
  - `logoPath`: 指向在应用程序抽屉顶部显示的图像的 `frontend/public` 下的相对路径。
支持以下模型 ID（请确保它们在部署区域的 Bedrock 控制台中的"模型访问"下也已启用）：
- **Claude 模型:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Amazon Nova 模型:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Mistral 模型:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **DeepSeek 模型:** `deepseek-r1`
- **Meta Llama 模型:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

完整列表可以在 [index.ts](./frontend/src/constants/index.ts) 中找到。

- 在部署 CDK 之前，您需要对要部署到的区域进行一次引导。

```
npx cdk bootstrap
```

- 部署此示例项目

```
npx cdk deploy --require-approval never --all
```

- 您将获得类似以下的输出。Web 应用程序的 URL 将在 `BedrockChatStack.FrontendURL` 中输出，请从浏览器访问它。

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### 定义参数

您可以通过两种方式定义部署参数：使用 `cdk.json` 或使用类型安全的 `parameter.ts` 文件。

#### 使用 cdk.json（传统方法）

配置参数的传统方式是编辑 `cdk.json` 文件。这种方法简单但缺乏类型检查：

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

#### 使用 parameter.ts（推荐的类型安全方法）

为了获得更好的类型安全性和开发者体验，您可以使用 `parameter.ts` 文件定义参数：

```typescript
// 为默认环境定义参数
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

> [!Note]
> 现有用户可以继续使用 `cdk.json` 而无需任何更改。对于新部署或需要管理多个环境时，建议使用 `parameter.ts` 方法。

### 部署多个环境

您可以使用 `parameter.ts` 文件和 `-c envName` 选项从同一代码库部署多个环境。

#### 前提条件

1. 如上所示在 `parameter.ts` 中定义您的环境
2. 每个环境都将拥有带有环境特定前缀的自己的资源集

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

   - 每个环境的主堆栈将以环境名称为前缀（例如，`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - 但是，自定义机器人堆栈（`BrChatKbStack*`）和 API 发布堆栈（`ApiPublishmentStack*`）不会收到环境前缀，因为它们是在运行时动态创建的

2. **资源命名**：

   - 只有一些资源在其名称中接收环境前缀（例如，`dev_ddb_export` 表、`dev-FrontendWebAcl`）
   - 大多数资源保持其原始名称，但通过在不同的堆栈中进行隔离

3. **环境标识**：

   - 所有资源都带有包含环境名称的 `CDKEnvironment` 标签
   - 您可以使用此标签识别资源属于哪个环境
   - 示例：`CDKEnvironment: dev` 或 `CDKEnvironment: prod`

4. **默认环境覆盖**：如果您在 `parameter.ts` 中定义了"默认"环境，它将覆盖 `cdk.json` 中的设置。要继续使用 `cdk.json`，请不要在 `parameter.ts` 中定义"默认"环境。

5. **环境要求**：要创建"默认"以外的环境，您必须使用 `parameter.ts`。仅使用 `-c envName` 选项而没有相应的环境定义是不够的。

6. **资源隔离**：每个环境创建自己的资源集，允许您在同一 AWS 账户中拥有开发、测试和生产环境，而不会发生冲突。

## 其他

您可以通过两种方式为部署定义参数：使用 `cdk.json` 或使用类型安全的 `parameter.ts` 文件。

#### 使用 cdk.json（传统方法）

配置参数的传统方式是编辑 `cdk.json` 文件。这种方法简单但缺乏类型检查：

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

> [!Note]
> 现有用户可以继续使用 `cdk.json` 而无需任何更改。`parameter.ts` 方法推荐用于新部署或需要管理多个环境时。

### 部署多个环境

您可以使用 `parameter.ts` 文件和 `-c envName` 选项从同一代码库部署多个环境。

#### 前提条件

1. 如上所示在 `parameter.ts` 中定义您的环境
2. 每个环境将拥有带有环境特定前缀的自己的资源集

#### 部署命令

部署特定环境：

```bash
# 部署开发环境
npx cdk deploy --all -c envName=dev

# 部署生产环境
npx cdk deploy --all -c envName=prod
```

如果未指定环境，将使用"默认"环境：

```bash
# 部署默认环境
npx cdk deploy --all
```

#### 重要说明

1. **堆栈命名**：

   - 每个环境的主堆栈将带有环境名称前缀（例如，`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - 但是，自定义机器人堆栈（`BrChatKbStack*`）和 API 发布堆栈（`ApiPublishmentStack*`）不会收到环境前缀，因为它们是在运行时动态创建的

2. **资源命名**：

   - 只有一些资源在其名称中接收环境前缀（例如，`dev_ddb_export` 表、`dev-FrontendWebAcl`）
   - 大多数资源保持其原始名称，但通过在不同的堆栈中隔离

3. **环境标识**：

   - 所有资源都带有包含环境名称的 `CDKEnvironment` 标签
   - 您可以使用此标签来识别资源属于哪个环境
   - 示例：`CDKEnvironment: dev` 或 `CDKEnvironment: prod`

4. **默认环境覆盖**：如果您在 `parameter.ts` 中定义了"默认"环境，它将覆盖 `cdk.json` 中的设置。要继续使用 `cdk.json`，请不要在 `parameter.ts` 中定义"默认"环境。

5. **环境要求**：要创建"默认"以外的环境，您必须使用 `parameter.ts`。仅使用 `-c envName` 选项而没有相应的环境定义是不够的。

6. **资源隔离**：每个环境创建自己的资源集，允许您在同一个 AWS 账户中拥有开发、测试和生产环境，而不会发生冲突。

## 其他

### 删除资源

如果使用 cli 和 CDK,请执行 `npx cdk destroy`。如果没有使用,请访问 [CloudFormation](https://console.aws.amazon.com/cloudformation/home) 然后手动删除 `BedrockChatStack` 和 `FrontendWafStack`。请注意 `FrontendWafStack` 在 `us-east-1` 区域。

### 语言设置

本应用使用 [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector) 自动检测语言。您可以从应用菜单切换语言。另外,您也可以使用查询字符串来设置语言,如下所示:

> `https://example.com?lng=ja`

### 禁用自助注册

本示例默认启用自助注册。要禁用自助注册,请打开 [cdk.json](./cdk/cdk.json) 并将 `selfSignUpEnabled` 设置为 `false`。如果您配置了[外部身份提供商](#external-identity-provider),该值将被忽略并自动禁用。

### 限制注册邮箱域名

默认情况下,本示例不限制注册邮箱的域名。要只允许特定域名的邮箱注册,请打开 `cdk.json` 并在 `allowedSignUpEmailDomains` 中指定域名列表。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部身份提供商

本示例支持外部身份提供商。目前我们支持 [Google](./idp/SET_UP_GOOGLE_zh-CN.md) 和[自定义 OIDC 提供商](./idp/SET_UP_CUSTOM_OIDC_zh-CN.md)。

### 可选的前端 WAF

对于 CloudFront 分配,AWS WAF WebACL 必须在 us-east-1 区域创建。在某些组织中,策略限制在主要区域之外创建资源。在这种环境中,当尝试在 us-east-1 配置前端 WAF 时,CDK 部署可能会失败。

为了适应这些限制,前端 WAF 堆栈是可选的。禁用时,CloudFront 分配将在没有 WebACL 的情况下部署。这意味着您将无法在前端边缘进行 IP 允许/拒绝控制。身份验证和所有其他应用程序控制继续正常工作。请注意,此设置仅影响前端 WAF(CloudFront 范围);已发布的 API WAF(区域性)不受影响。

要禁用前端 WAF,请在 `parameter.ts` 中设置以下内容(推荐的类型安全方法):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

或者如果使用传统的 `cdk/cdk.json` 设置以下内容:

```json
"enableFrontendWaf": false
```

### 自动将新用户添加到群组

本示例有以下群组来为用户授予权限:

- [`Admin`](./ADMINISTRATOR_zh-CN.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_zh-CN.md)

如果您希望新创建的用户自动加入群组,可以在 [cdk.json](./cdk/cdk.json) 中指定。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

默认情况下,新创建的用户将加入 `CreatingBotAllowed` 群组。

### 配置 RAG 副本

`enableRagReplicas` 是 [cdk.json](./cdk/cdk.json) 中的一个选项,用于控制 RAG 数据库的副本设置,特别是使用 Amazon OpenSearch Serverless 的知识库。

- **默认值**: true
- **true**: 通过启用额外的副本来提高可用性,适合生产环境但会增加成本。
- **false**: 通过使用较少的副本来降低成本,适合开发和测试。

这是一个账户/区域级别的设置,影响整个应用程序而不是单个机器人。

> [!Note]
> 从 2024 年 6 月起,Amazon OpenSearch Serverless 支持 0.5 OCU,降低了小规模工作负载的入门成本。生产部署可以从 2 个 OCU 开始,而开发/测试工作负载可以使用 1 个 OCU。OpenSearch Serverless 根据工作负载需求自动扩展。更多详情,请访问[公告](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)。

### 配置机器人商店

机器人商店功能允许用户共享和发现自定义机器人。您可以通过 [cdk.json](./cdk/cdk.json) 中的以下设置配置机器人商店:

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: 控制是否启用机器人商店功能(默认: `true`)
- **botStoreLanguage**: 设置机器人搜索和发现的主要语言(默认: `"en"`)。这会影响机器人在商店中的索引和搜索方式,优化指定语言的文本分析。
- **enableBotStoreReplicas**: 控制是否为机器人商店使用的 OpenSearch Serverless 集合启用备用副本(默认: `false`)。设置为 `true` 可提高可用性但会增加成本,而 `false` 可降低成本但可能影响可用性。
  > **重要**: 集合创建后无法更新此属性。如果您尝试修改此属性,集合将继续使用原始值。

### 跨区域推理

[跨区域推理](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)允许 Amazon Bedrock 在多个 AWS 区域之间动态路由模型推理请求,在高峰需求期间提高吞吐量和弹性。要配置,请编辑 `cdk.json`。

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) 改善了 Lambda 函数的冷启动时间,提供更快的响应时间以获得更好的用户体验。另一方面,对于 Python 函数,目前[根据缓存大小收费](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)且[在某些区域不可用](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)。要禁用 SnapStart,请编辑 `cdk.json`。

```json
"enableLambdaSnapStart": false
```

### 配置自定义域名

您可以通过在 [cdk.json](./cdk/cdk.json) 中设置以下参数来为 CloudFront 分配配置自定义域名:

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: 聊天应用程序的自定义域名(例如,chat.example.com)
- `hostedZoneId`: 将创建域名记录的 Route 53 托管区域的 ID

提供这些参数后,部署将自动:

- 在 us-east-1 区域创建带有 DNS 验证的 ACM 证书
- 在您的 Route 53 托管区域创建必要的 DNS 记录
- 配置 CloudFront 使用您的自定义域名

> [!Note]
> 域名必须由您的 AWS 账户中的 Route 53 管理。托管区域 ID 可以在 Route 53 控制台中找到。

### 配置允许的国家(地理限制)

您可以根据客户端访问的国家限制对 Bedrock-Chat 的访问。
使用 [cdk.json](./cdk/cdk.json) 中的 `allowedCountries` 参数,该参数接受 [ISO-3166 国家代码](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)列表。
例如,一个新西兰的企业可能决定只允许来自新西兰(NZ)和澳大利亚(AU)的 IP 地址访问门户,而拒绝其他所有人的访问。
要配置此行为,请在 [cdk.json](./cdk/cdk.json) 中使用以下设置:

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

或者,使用 `parameter.ts`(推荐的类型安全方法):

```ts
// 为默认环境定义参数
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### 禁用 IPv6 支持

前端默认同时获取 IP 和 IPv6 地址。在某些罕见的情况下,您可能需要明确禁用 IPv6 支持。要实现这一点,请在 [parameter.ts](./cdk/parameter.ts) 或类似地在 [cdk.json](./cdk/cdk.json) 中设置以下参数:

```ts
"enableFrontendIpv6": false
```

如果未设置,默认将启用 IPv6 支持。

### 本地开发

请参阅 [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_zh-CN.md)。

### 贡献

感谢您考虑为这个仓库做出贡献！我们欢迎错误修复、语言翻译(i18n)、功能增强、[代理工具](./docs/AGENT.md#how-to-develop-your-own-tools)和其他改进。

对于功能增强和其他改进,**在创建拉取请求之前,我们非常感谢您能创建一个功能请求问题来讨论实现方法和细节。对于错误修复和语言翻译(i18n),直接创建拉取请求即可。**

在贡献之前,请也查看以下指南:

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

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## 许可证

本库采用 MIT-0 许可证授权。详见[许可证文件](./LICENSE)。