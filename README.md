# Bedrock Claude Chat (Nova)

![](https://github.com/aws-samples/bedrock-claude-chat/actions/workflows/cdk.yml/badge.svg)

> [!Warning] > **V2 released. To update, please carefully review the [migration guide](./docs/migration/V1_TO_V2.md).** Without any care, **BOTS FROM V1 WILL BECOME UNUSABLE.**

This repository is a sample chatbot using the Anthropic company's LLM [Claude](https://www.anthropic.com/), one of the foundational models provided by [Amazon Bedrock](https://aws.amazon.com/bedrock/) for generative AI.

### Watch Overview and Installation on YouTube

[![Overview](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Basic Conversation

![](./docs/imgs/demo.gif)

### Bot Personalization

Add your own instruction and give external knowledge as URL or files (a.k.a [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/). The bot can be shared among application users. The customized bot also can be published as stand-alone API (See the [detail](./docs/PUBLISH_API.md)).

![](./docs/imgs/bot_creation.png)
![](./docs/imgs/bot_chat.png)
![](./docs/imgs/bot_api_publish_screenshot3.png)

> [!Important]
> For governance reasons, only allowed users are able to create customized bots. To allow the creation of customized bots, the user must be a member of group called `CreatingBotAllowed`, which can be set up via the management console > Amazon Cognito User pools or aws cli. Note that the user pool id can be referred by accessing CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Administrator dashboard

<details>
<summary>Administrator dashboard</summary>

Analyze usage for each user / bot on administrator dashboard. [detail](./docs/ADMINISTRATOR.md)

![](./docs/imgs/admin_bot_analytics.png)

</details>

### LLM-powered Agent

<details>
<summary>LLM-powered Agent</summary>

By using the [Agent functionality](./docs/AGENT.md), your chatbot can automatically handle more complex tasks. For example, to answer a user's question, the Agent can retrieve necessary information from external tools or break down the task into multiple steps for processing.

![](./docs/imgs/agent1.png)
![](./docs/imgs/agent2.png)

</details>

## 📚 Supported Languages

- English 💬
- 日本語 💬 (ドキュメントは[こちら](./docs/README_ja.md))
- 한국어 💬
- 中文 💬
- Français 💬
- Deutsch 💬
- Español 💬
- Italian 💬
- Norsk 💬
- ไทย 💬
- Bahasa Indonesia 💬
- Bahasa Melayu 💬

## 🚀 Super-easy Deployment

- In the us-east-1 region, open [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > Check all of `Anthropic / Claude 3`, all of `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` and `Cohere / Embed Multilingual` then `Save changes`.

<details>
<summary>Screenshot</summary>

![](./docs/imgs/model_screenshot.png)

</details>

- Open [CloudShell](https://console.aws.amazon.com/cloudshell/home) at the region where you want to deploy
- Run deployment via following commands. If you want to specify the version to deploy or need to apply security policies, please specify the appropriate parameters from [Optional Parameters](#optional-parameters).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- You will be asked if a new user or using v2. If you are not a continuing user from v0, please enter `y`.

### Optional Parameters

You can specify the following parameters during deployment to enhance security and customization:

- **--disable-self-register**: Disable self-registration (default: enabled). If this flag is set, you will need to create all users on cognito and it will not allow users to self register their accounts.
- **--enable-lambda-snapstart**: Enable [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (default: disabled). If this flag is set, improves cold start times for Lambda functions, providing faster response times for better user experience.
- **--ipv4-ranges**: Comma-separated list of allowed IPv4 ranges. (default: allow all ipv4 addresses)
- **--ipv6-ranges**: Comma-separated list of allowed IPv6 ranges. (default: allow all ipv6 addresses)
- **--disable-ipv6**: Disable connections over IPv6. (default: enabled)
- **--allowed-signup-email-domains**: Comma-separated list of allowed email domains for sign-up. (default: no domain restriction)
- **--bedrock-region**: Define the region where bedrock is available. (default: us-east-1)
- **--version**: The version of Bedrock Claude Chat to deploy. (default: latest version in development)

#### Example command with parameters:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- After about 35 minutes, you will get the following output, which you can access from your browser

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./docs/imgs/signin.png)

The sign-up screen will appear as shown above, where you can register your email and log in.

> [!Important]
> Without setting the optional parameter, this deployment method allows anyone who knows the URL to sign up. For production use, it is strongly recommended to add IP address restrictions and disable self-signup to mitigate security risks (you can define allowed-signup-email-domains to restrict users so that only email addresses from your company’s domain can sign up). Use both ipv4-ranges and ipv6-ranges for IP address restrictions, and disable self-signup by using disable-self-register when executing ./bin.

> [!TIP]
> If the `Frontend URL` does not appear or Bedrock Claude Chat does not work properly, it may be a problem with the latest version. In this case, please add `--version "v1.2.6"` to the parameters and try deployment again.

## Architecture

It's an architecture built on AWS managed services, eliminating the need for infrastructure management. Utilizing Amazon Bedrock, there's no need to communicate with APIs outside of AWS. This enables deploying scalable, reliable, and secure applications.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): NoSQL database for conversation history storage
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Backend API endpoint ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Frontend application delivery ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP address restriction
- [Amazon Cognito](https://aws.amazon.com/cognito/): User authentication
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Managed service to utilize foundational models via APIs
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Provides a managed interface for Retrieval-Augmented Generation ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), offering services for embedding and parsing documents
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Receiving event from DynamoDB stream and launching Step Functions to embed external knowledge
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orchestrating ingestion pipeline to embed external knowledge into Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Serves as the backend database for Bedrock Knowledge Bases, providing full-text search and vector search capabilities, enabling accurate retrieval of relevant information
- [Amazon Athena](https://aws.amazon.com/athena/): Query service to analyze S3 bucket

![](docs/imgs/arch.png)

## Deploy using CDK

Super-easy Deployment uses [AWS CodeBuild](https://aws.amazon.com/codebuild/) to perform deployment by CDK internally. This section describes the procedure for deploying directly with CDK.

- Please have UNIX, Docker and a Node.js runtime environment. If not, you can also use [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Important]
> If there is insufficient storage space in the local environment during deployment, CDK bootstrapping may result in an error. If you are running in Cloud9 etc., we recommend expanding the volume size of the instance before deploying.

- Clone this repository

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Install npm packages

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Install [AWS CDK](https://aws.amazon.com/cdk/)

```
npm i -g aws-cdk
```

- Before deploying the CDK, you will need to work with Bootstrap once for the region you are deploying to. In this example, we will deploy to the us-east-1 region. Please replace your account id into `<account id>`.

```
cdk bootstrap aws://<account id>/us-east-1
```

- If necessary, edit the following entries in [cdk.json](./cdk/cdk.json) if necessary.

  - `bedrockRegion`: Region where Bedrock is available. **NOTE: Bedrock does NOT support all regions for now.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Allowed IP Address range.
  - `enableLambdaSnapStart`: Defaults to true. Set to false if deploying to a [region that doesn't support Lambda SnapStart for Python functions](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Deploy this sample project

```
cdk deploy --require-approval never --all
```

- You will get output similar to the following. The URL of the web app will be output in `BedrockChatStack.FrontendURL`, so please access it from your browser.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## Others

### Configure Mistral models support

Update `enableMistral` to `true` in [cdk.json](./cdk/cdk.json), and run `cdk deploy`.

```json
...
  "enableMistral": true,
```

> [!Important]
> This project focus on Anthropic Claude models, the Mistral models are limited supported. For example, prompt examples are based on Claude models. This is a Mistral-only option, once you toggled to enable Mistral models, you can only use Mistral models for all the chat features, NOT both Claude and Mistral models.

### Configure default text generation

Users can adjust the [text generation parameters](https://docs.anthropic.com/claude/reference/complete_post) from the custom bot creation screen. If the bot is not used, the default parameters set in [config.py](./backend/app/config.py) will be used.

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Remove resources

If using cli and CDK, please `cdk destroy`. If not, access [CloudFormation](https://console.aws.amazon.com/cloudformation/home) and then delete `BedrockChatStack` and `FrontendWafStack` manually. Please note that `FrontendWafStack` is in `us-east-1` region.

### Language Settings

This asset automatically detects the language using [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). You can switch languages from the application menu. Alternatively, you can use Query String to set the language as shown below.

> `https://example.com?lng=ja`

### Disable self sign up

This sample has self sign up enabled by default. To disable self sign up, open [cdk.json](./cdk/cdk.json) and switch `selfSignUpEnabled` as `false`. If you configure [external identity provider](#external-identity-provider), the value will be ignored and automatically disabled.

### Restrict Domains for Sign-Up Email Addresses

By default, this sample does not restrict the domains for sign-up email addresses. To allow sign-ups only from specific domains, open `cdk.json` and specify the domains as a list in `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### External Identity Provider

This sample supports external identity provider. Currently we support [Google](./docs/idp/SET_UP_GOOGLE.md) and [custom OIDC provider](./docs/idp/SET_UP_CUSTOM_OIDC.md).

### Add new users to groups automatically

This sample has the following groups to give permissions to users:

- [`Admin`](./docs/ADMINISTRATOR.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./docs/PUBLISH_API.md)

If you want newly created users to automatically join groups, you can specify them in [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

By default, newly created users will be joined to the `CreatingBotAllowed` group.

### Configure RAG Replicas

`enableRagReplicas` is an option in [cdk.json](./cdk/cdk.json) that controls the replica settings for the RAG database, specifically the Knowledge Bases using Amazon OpenSearch Serverless.

- **Default**: true
- **true**: Enhances availability by enabling additional replicas, making it suitable for production environments but increasing costs.
- **false**: Reduces costs by using fewer replicas, making it suitable for development and testing.

This is an account/region-level setting, affecting the entire application rather than individual bots.

> [!Note]
> As of June 2024, Amazon OpenSearch Serverless supports 0.5 OCU, lowering entry costs for small-scale workloads. Production deployments can start with 2 OCUs, while dev/test workloads can use 1 OCU. OpenSearch Serverless automatically scales based on workload demands. For more detail, visit [announcement](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Cross-region inference

[Cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) allows Amazon Bedrock to dynamically route model inference requests across multiple AWS regions, enhancing throughput and resilience during peak demand periods. To configure, edit `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) improves cold start times for Lambda functions, providing faster response times for better user experience. On the other hand, for Python functions, there is a [charge depending on cache size](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) and [not available in some regions](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) currently. To disable SnapStart, edit `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Local Development

See [LOCAL DEVELOPMENT](./docs/LOCAL_DEVELOPMENT.md).

### Contribution

Thank you for considering contributing to this repository! We welcome bug fixes, language translations (i18n), feature enhancements, [agent tools](./docs/AGENT.md#how-to-develop-your-own-tools), and other improvements.

For feature enhancements and other improvements, **before creating a Pull Request, we would greatly appreciate it if you could create a Feature Request Issue to discuss the implementation approach and details. For bug fixes and language translations (i18n), proceed with creating a Pull Request directly.**

Please also take a look at the following guidelines before contributing:

- [Local Development](./docs/LOCAL_DEVELOPMENT.md)
- [CONTRIBUTING](./CONTRIBUTING.md)

## Contacts

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Significant Contributors

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Contributors

[![bedrock claude chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## License

This library is licensed under the MIT-0 License. See [the LICENSE file](./LICENSE).
