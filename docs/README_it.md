# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_no.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi.md)

> [!Warning]  
> **V2 가 출시되었습니다. 업데이트하려면 [마이그레이션 가이드](./migration/V1_TO_V2_it.md)를 주의깊게 검토하세요.** 주의하지 않으면 **V1의 봇은 사용할 수 없게 됩니다.**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)에서 제공하는 LLM 모델을 사용하는 다국어 챗봇입니다.

### YouTube에서 개요 및 설치 영상 보기

[![Overview](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 기본 대화

![](./imgs/demo.gif)

### 봇 개인화

고유한 지시사항을 추가하고 URL 또는 파일로 외부 지식을 제공할 수 있습니다 (이른바 [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). 봇은 애플리케이션 사용자들과 공유할 수 있으며, 사용자 정의된 봇은 독립 실행형 API로 게시할 수도 있습니다 (자세한 내용은 [여기](./PUBLISH_API_it.md) 참조).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> 거버넌스 이유로, 허용된 사용자만 사용자 정의 봇을 만들 수 있습니다. 사용자 정의 봇 생성을 허용하려면 해당 사용자는 `CreatingBotAllowed` 그룹의 구성원이어야 합니다. 이는 관리 콘솔 > Amazon Cognito 사용자 풀 또는 aws cli를 통해 설정할 수 있습니다. 사용자 풀 ID는 CloudFormation > BedrockChatStack > 출력 > `AuthUserPoolIdxxxx`를 통해 확인할 수 있습니다.

### 관리자 대시보드

<details>
<summary>관리자 대시보드</summary>

관리자 대시보드에서 사용자/봇별 사용량을 분석할 수 있습니다. [자세히 보기](./ADMINISTRATOR_it.md)

![](./imgs/admin_bot_analytics.png)

</details>

### LLM 기반 에이전트

<details>
<summary>LLM 기반 에이전트</summary>

[에이전트 기능](./AGENT_it.md)을 사용하면 챗봇이 더 복잡한 작업을 자동으로 처리할 수 있습니다. 예를 들어, 사용자의 질문에 답하기 위해 에이전트는 외부 도구에서 필요한 정보를 검색하거나 작업을 여러 단계로 나누어 처리할 수 있습니다.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超简单部署

- 在 us-east-1 区域，打开 [Bedrock 模型访问](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `管理模型访问` > 勾选所有 `Anthropic / Claude 3`，所有 `Amazon / Nova`，`Amazon / Titan 文本嵌入 V2` 和 `Cohere / 多语言嵌入`，然后 `保存更改`。

<details>
<summary>截图</summary>

![](./imgs/model_screenshot.png)

</details>

- 在您想要部署的区域打开 [CloudShell](https://console.aws.amazon.com/cloudshell/home)
- 通过以下命令运行部署。如果您想指定部署的版本或需要应用安全策略，请从[可选参数](#optional-parameters)中指定适当的参数。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 系统会询问您是新用户还是使用 v2。如果您不是 v0 的继续用户，请输入 `y`。

### 可选参数

您可以在部署期间指定以下参数以增强安全性和自定义性：

- **--disable-self-register**：禁用自注册（默认：启用）。如果设置此标志，您将需要在 Cognito 上创建所有用户，并且不允许用户自行注册账户。
- **--enable-lambda-snapstart**：启用 [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)（默认：禁用）。如果设置此标志，将改善 Lambda 函数的冷启动时间，提供更快的响应时间，从而带来更好的用户体验。
- **--ipv4-ranges**：允许的 IPv4 范围的逗号分隔列表。（默认：允许所有 IPv4 地址）
- **--ipv6-ranges**：允许的 IPv6 范围的逗号分隔列表。（默认：允许所有 IPv6 地址）
- **--disable-ipv6**：禁用 IPv6 连接。（默认：启用）
- **--allowed-signup-email-domains**：允许注册的电子邮件域名的逗号分隔列表。（默认：无域名限制）
- **--bedrock-region**：定义 Bedrock 可用的区域。（默认：us-east-1）
- **--repo-url**：要部署的 Bedrock Claude Chat 的自定义仓库，如果已分叉或使用自定义源代码控制。（默认：https://github.com/aws-samples/bedrock-claude-chat.git）
- **--version**：要部署的 Bedrock Claude Chat 版本。（默认：开发中的最新版本）
- **--cdk-json-override**：您可以使用覆盖 JSON 块在部署期间覆盖任何 CDK 上下文值。这允许您在不直接编辑 cdk.json 文件的情况下修改配置。

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

> [!注意]
> 覆盖值将在 AWS 代码构建部署期间与现有的 cdk.json 配置合并。指定的覆盖值将优先于 cdk.json 中的值。

#### 带参数的示例命令：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 大约 35 分钟后，您将获得以下输出，可以从浏览器访问

```
前端 URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

将出现如上所示的注册屏幕，您可以注册您的电子邮件并登录。

> [!重要]
> 如果不设置可选参数，此部署方法允许任何知道 URL 的人注册。对于生产使用，强烈建议添加 IP 地址限制并禁用自注册，以降低安全风险（您可以定义 allowed-signup-email-domains 以限制用户，使只有公司域名的电子邮件地址可以注册）。在执行 ./bin 时同时使用 ipv4-ranges 和 ipv6-ranges 进行 IP 地址限制，并通过使用 disable-self-register 禁用自注册。

> [!提示]
> 如果 `前端 URL` 未出现或 Bedrock Claude Chat 无法正常工作，可能是最新版本存在问题。在这种情况下，请在参数中添加 `--version "v1.2.6"` 并重新尝试部署。

## 아키텍처

AWS 관리형 서비스를 기반으로 구축된 아키텍처로, 인프라 관리의 필요성을 제거합니다. Amazon Bedrock을 활용함으로써 AWS 외부 API와 통신할 필요가 없습니다. 이를 통해 확장 가능하고 안정적이며 안전한 애플리케이션을 배포할 수 있습니다.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): 대화 이력 저장을 위한 NoSQL 데이터베이스
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): 백엔드 API 엔드포인트 ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): 프론트엔드 애플리케이션 전송 ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP 주소 제한
- [Amazon Cognito](https://aws.amazon.com/cognito/): 사용자 인증
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): API를 통해 기본 모델을 활용하는 관리형 서비스
- [Amazon Bedrock 지식 기반](https://aws.amazon.com/bedrock/knowledge-bases/): 검색 증강 생성([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/))을 위한 관리형 인터페이스 제공, 문서 임베딩 및 파싱 서비스 제공
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): DynamoDB 스트림에서 이벤트를 수신하고 외부 지식을 임베딩하기 위해 Step Functions 실행
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Bedrock 지식 기반에 외부 지식을 임베딩하기 위한 수집 파이프라인 오케스트레이션
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Bedrock 지식 기반의 백엔드 데이터베이스로 작용, 전체 텍스트 검색 및 벡터 검색 기능 제공, 관련 정보의 정확한 검색 가능
- [Amazon Athena](https://aws.amazon.com/athena/): S3 버킷을 분석하기 위한 쿼리 서비스

![](./imgs/arch.png)

## CDKを使用したデプロイ

簡単デプロイは、[AWS CodeBuild](https://aws.amazon.com/codebuild/)を内部的に使用してCDKによるデプロイを実行します。このセクションでは、CDKを直接使用したデプロイ手順を説明します。

- UNIX、Docker、Node.jsランタイム環境が必要です。ない場合は、[Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)を使用できます

> [!Important]
> デプロイ中にローカル環境のストレージ容量が不足している場合、CDKブートストラップでエラーが発生する可能性があります。Cloud9などで実行している場合は、デプロイ前にインスタンスのボリュームサイズを拡張することをお勧めします。

- リポジトリをクローン

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- npmパッケージをインストール

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- 必要に応じて、[cdk.json](./cdk/cdk.json)の以下のエントリを編集します。

  - `bedrockRegion`: Bedrockが利用可能なリージョン。**注意：現在、Bedrockはすべてのリージョンをサポートしているわけではありません。**
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`: 許可されるIPアドレス範囲。
  - `enableLambdaSnapStart`: デフォルトはtrue。[PythonファンクションのLambda SnapStartをサポートしていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)にデプロイする場合はfalseに設定します。

- CDKをデプロイする前に、デプロイするリージョンでブートストラップを1回実行する必要があります。

```
npx cdk bootstrap
```

- このサンプルプロジェクトをデプロイ

```
npx cdk deploy --require-approval never --all
```

- 以下のような出力が表示されます。WebアプリのURLは`BedrockChatStack.FrontendURL`に出力されるので、ブラウザからアクセスしてください。

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## その他

### Mistralモデルのサポートを設定

[cdk.json](./cdk/cdk.json)の`enableMistral`を`true`に更新し、`npx cdk deploy`を実行します。

```json
...
  "enableMistral": true,
```

> [!Important]
> このプロジェクトはAnthropicのClaudeモデルに焦点を当てており、Mistralモデルは限定的にサポートされています。例えば、プロンプト例はClaudeモデルに基づいています。これはMistral専用のオプションであり、一度Mistralモデルを有効にすると、チャット機能ではClaudeとMistralの両方のモデルではなく、Mistralモデルのみを使用できます。

### デフォルトのテキスト生成を設定

ユーザーは、カスタムボット作成画面から[テキスト生成パラメータ](https://docs.anthropic.com/claude/reference/complete_post)を調整できます。ボットが使用されない場合、[config.py](./backend/app/config.py)で設定されたデフォルトのパラメータが使用されます。

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### リソースの削除

CLIとCDKを使用している場合は、`npx cdk destroy`を実行してください。そうでない場合は、[CloudFormation](https://console.aws.amazon.com/cloudformation/home)にアクセスし、`BedrockChatStack`と`FrontendWafStack`を手動で削除してください。`FrontendWafStack`は`us-east-1`リージョンにあることに注意してください。

### 言語設定

このアセットは[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)を使用して言語を自動検出します。アプリケーションメニューから言語を切り替えることができます。または、以下のようにクエリ文字列を使用して言語を設定することもできます。

> `https://example.com?lng=ja`

### セルフサインアップの無効化

このサンプルはデフォルトでセルフサインアップが有効になっています。セルフサインアップを無効にするには、[cdk.json](./cdk/cdk.json)を開き、`selfSignUpEnabled`を`false`に切り替えます。[外部IDプロバイダ](#external-identity-provider)を設定した場合、この値は無視され、自動的に無効になります。

### サインアップ可能なメールアドレスのドメイン制限

デフォルトでは、このサンプルはサインアップ可能なメールアドレスのドメインを制限しません。特定のドメインのみサインアップを許可するには、`cdk.json`を開き、`allowedSignUpEmailDomains`にドメインをリストとして指定します。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部IDプロバイダ

このサンプルは外部IDプロバイダをサポートしています。現在、[Google](./idp/SET_UP_GOOGLE_it.md)と[カスタムOIDCプロバイダ](./idp/SET_UP_CUSTOM_OIDC_it.md)をサポートしています。

### 新規ユーザーを自動的にグループに追加

このサンプルには、ユーザーに権限を与えるために以下のグループがあります：

- [`Admin`](./ADMINISTRATOR_it.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_it.md)

新規作成されたユーザーを自動的にグループに参加させたい場合は、[cdk.json](./cdk/cdk.json)で指定できます。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

デフォルトでは、新規作成されたユーザーは`CreatingBotAllowed`グループに参加します。

### RAGレプリカの設定

[cdk.json](./cdk/cdk.json)の`enableRagReplicas`は、Amazon OpenSearch Serverlessを使用するナレッジベースの具体的にはレプリカ設定を制御するオプションです。

- **デフォルト**：true
- **true**：追加のレプリカを有効にすることで可用性を向上させ、本番環境に適していますが、コストが増加します。
- **false**：レプリカを減らすことでコストを削減し、開発とテストに適しています。

これはアカウント/リージョンレベルの設定で、個々のボットではなくアプリケーション全体に影響します。

> [!Note]
> 2024年6月現在、Amazon OpenSearch Serverlessは0.5 OCUをサポートし、小規模ワークロードのエントリーコストを引き下げています。本番環境では2 OCUから開始でき、開発/テストワークロードは1 OCUを使用できます。OpenSearch Serverlessは自動的にワークロードの需要に応じてスケーリングします。詳細は[アナウンス](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)をご覧ください。

### クロスリージョン推論

[クロスリージョン推論](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)により、Amazon Bedrockは複数のAWSリージョン間でモデル推論リクエストを動的にルーティングし、ピーク時の需要期間中のスループットと回復力を向上させます。設定するには、`cdk.json`を編集します。

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)はLambda関数のコールドスタート時間を改善し、ユーザーエクスペリエンスをより良くするより速い応答時間を提供します。一方、Pythonの関数では、[キャッシュサイズに応じた課金](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)と[現在いくつかのリージョンで利用できない](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)制限があります。SnapStartを無効にするには、`cdk.json`を編集します。

```json
"enableLambdaSnapStart": false
```

### カスタムドメインの設定

[cdk.json](./cdk/cdk.json)で以下のパラメータを設定することで、CloudFront配信のカスタムドメインを設定できます：

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`：チャットアプリケーションのカスタムドメイン名（例：chat.example.com）
- `hostedZoneId`：ドメインレコードが作成されるRoute 53ホストゾーンのID

これらのパラメータが提供されると、デプロイメントは自動的に以下を行います：

- us-east-1リージョンでDNS検証を使用したACM証明書の作成
- Route 53ホストゾーンに必要なDNSレコードの作成
- カスタムドメインを使用するようにCloudFrontを設定

> [!Note]
> ドメインはAWSアカウントのRoute 53で管理されている必要があります。ホストゾーンIDはRoute 53コンソールで確認できます。

### ローカル開発

[ローカル開発](./LOCAL_DEVELOPMENT_it.md)を参照してください。

### 貢献

このリポジトリへの貢献を検討していただき、ありがとうございます！バグ修正、言語翻訳（i18n）、機能拡張、[エージェントツール](./docs/AGENT.md#how-to-develop-your-own-tools)、その他の改善を歓迎します。

機能拡張やその他の改善については、**プルリクエストを作成する前に、実装アプローチと詳細について議論するために機能リクエストの課題を作成していただけると大変感謝します。バグ修正と言語翻訳（i18n）については、直接プルリクエストを作成してください。**

貢献する前に、以下のガイドラインも参照してください：

- [ローカル開発](./LOCAL_DEVELOPMENT_it.md)
- [貢献](./CONTRIBUTING_it.md)

## 連絡先

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 主要贡献者

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## 貢献者

[![bedrock claude chat 貢献者](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Licenza

Questa libreria è licenziata sotto la Licenza MIT-0. Consulta [il file LICENSE](./LICENSE).