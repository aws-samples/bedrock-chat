# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ja/README.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ko/README.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/zh/README.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/fr/README.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/de/README.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/es/README.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/it/README.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/no/README.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/th/README.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/id/README.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ms/README.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/vi/README.md)

> [!Warning]  
> **V2がリリースされました。更新する際は、[移行ガイド](./migration/V1_TO_V2.md)を注意深く確認してください。** 注意を払わないと、**V1のBOTが使用できなくなります。**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)が提供するLLMモデルを使用した多言語チャットボット。

### YouTubeで概要とインストールを視聴

[![Overview](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](./imgs/demo.gif)

### ボットのパーソナライズ

独自の指示を追加し、URLやファイルとして外部知識を提供（いわゆる[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。ボットはアプリケーションユーザー間で共有できます。カスタマイズされたボットはスタンドアロンAPIとして公開することもできます（[詳細](./PUBLISH_API.md)を参照）。

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由から、許可されたユーザーのみがカスタマイズされたボットを作成できます。カスタマイズされたボットの作成を許可するには、ユーザーは`CreatingBotAllowed`というグループのメンバーである必要があります。これは管理コンソール > Amazon Cognito ユーザープールまたはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`にアクセスすることで参照できます。

### 管理者ダッシュボード

<details>
<summary>管理者ダッシュボード</summary>

管理者ダッシュボードで、ユーザーごと/ボットごとの使用状況を分析できます。[詳細](./ADMINISTRATOR.md)

![](./imgs/admin_bot_analytics.png)

</details>

### LLMを活用したエージェント

<details>
<summary>LLMを活用したエージェント</summary>

[エージェント機能](./AGENT.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、エージェントは外部ツールから必要な情報を取得したり、タスクを複数のステップに分解して処理したりできます。

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超簡単デプロイ

- us-east-1リージョンで、[Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)を開き > `Manage model access` > `Anthropic / Claude 3`のすべて、`Amazon / Nova`、`Amazon / Titan Text Embeddings V2`、`Cohere / Embed Multilingual`をチェックし、`Save changes`をクリックします。

<details>
<summary>スクリーンショット</summary>

![](./imgs/model_screenshot.png)

</details>

- デプロイしたいリージョンの[CloudShell](https://console.aws.amazon.com/cloudshell/home)を開きます
- 以下のコマンドでデプロイを実行します。バージョンを指定したい場合や、セキュリティポリシーを適用する必要がある場合は、[オプションパラメータ](#optional-parameters)から適切なパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーかv2を使用するかの確認があります。v0からの継続ユーザーでない場合は、`y`を入力してください。

### オプションパラメータ

デプロイ時に以下のパラメータを指定して、セキュリティとカスタマイズを強化できます：

- **--disable-self-register**: 自己登録を無効にします（デフォルト：有効）。このフラグを設定すると、cognitoですべてのユーザーを作成する必要があり、ユーザーは自分でアカウントを登録できなくなります。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)を有効にします（デフォルト：無効）。このフラグを設定すると、Lambdaファンクションのコールドスタート時間が改善され、ユーザーエクスペリエンスの向上につながります。
- **--ipv4-ranges**: 許可されたIPv4範囲のカンマ区切りリスト（デフォルト：すべてのIPv4アドレスを許可）。
- **--ipv6-ranges**: 許可されたIPv6範囲のカンマ区切りリスト（デフォルト：すべてのIPv6アドレスを許可）。
- **--disable-ipv6**: IPv6接続を無効にします（デフォルト：有効）。
- **--allowed-signup-email-domains**: サインアップ時に許可されるメールドメインのカンマ区切りリスト（デフォルト：ドメイン制限なし）。
- **--bedrock-region**: Bedrockが利用可能なリージョンを定義します（デフォルト：us-east-1）。
- **--repo-url**: フォークまたはカスタムソース管理の場合、Bedrock Claude Chatのカスタムリポジトリをデプロイします（デフォルト：https://github.com/aws-samples/bedrock-claude-chat.git）。
- **--version**: デプロイするBedrock Claude Chatのバージョン（デフォルト：開発中の最新バージョン）。
- **--cdk-json-override**: デプロイ時にCDKコンテキスト値を上書きできます。これにより、cdk.jsonファイルを直接編集せずに設定を変更できます。

使用例：

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

上書きJSONは、cdk.jsonと同じ構造に従う必要があります。以下を含むすべてのコンテキスト値を上書きできます：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- cdk.jsonで定義された他のコンテキスト値

> [!Note]
> 上書き値は、AWS CodeBuildでのデプロイ時に既存のcdk.json設定とマージされます。指定された上書き値は、cdk.jsonの値よりも優先されます。

#### パラメータを指定したコマンド例：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 約35分後、以下の出力が表示され、ブラウザからアクセスできます

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

上記のようなサインアップ画面が表示され、メールを登録してログインできます。

> [!Important]
> オプションパラメータを設定しないと、URLを知っている人は誰でもサインアップできます。本番環境では、IPアドレス制限を追加し、自己サインアップを無効にして、セキュリティリスクを軽減することを強くお勧めします（allowed-signup-email-domainsを定義して、会社のドメインのメールアドレスのみがサインアップできるように制限できます）。./binを実行する際に、ipv4-rangesとipv6-rangesの両方を使用してIPアドレス制限を設定し、disable-self-registerを使用して自己サインアップを無効にしてください。

> [!TIP]
> `Frontend URL`が表示されないか、Bedrock Claude Chatが正常に機能しない場合、最新バージョンに問題がある可能性があります。この場合、`--version "v1.2.6"`をパラメータに追加してデプロイを再試行してください。

## アーキテクチャ

AWS マネージドサービスを基盤とするアーキテクチャで、インフラストラクチャ管理の必要性を排除しています。Amazon Bedrockを利用することで、AWS外のAPIと通信する必要がありません。これにより、スケーラブルで信頼性が高く、セキュアなアプリケーションをデプロイできます。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：会話履歴を保存するNoSQLデータベース
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：バックエンドAPIエンドポイント（[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)、[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：フロントエンドアプリケーションの配信（[React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/)：IPアドレス制限
- [Amazon Cognito](https://aws.amazon.com/cognito/)：ユーザー認証
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：APIを介して基盤モデルを利用するマネージドサービス
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)：検索拡張生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）のマネージドインターフェースを提供し、ドキュメントの埋め込みと解析サービスを提供
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：DynamoDBストリームからイベントを受信し、外部知識を埋め込むStep Functionsを起動
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：Bedrock Knowledge Baseに外部知識を埋め込むための取り込みパイプラインのオーケストレーション
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：Bedrock Knowledge Basesのバックエンドデータベースとして機能し、全文検索とベクター検索機能を提供し、関連情報の正確な検索を可能にする
- [Amazon Athena](https://aws.amazon.com/athena/)：S3バケットを分析するクエリサービス

![](./imgs/arch.png)

## CDKを使用したデプロイ

簡単デプロイは、内部的にCDKを使用して[AWS CodeBuild](https://aws.amazon.com/codebuild/)でデプロイを実行します。このセクションでは、直接CDKを使用したデプロイ手順を説明します。

- UNIX、Docker、Node.jsランタイム環境が必要です。ない場合は、[Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)を使用することもできます

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
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`: 許可されたIPアドレス範囲。
  - `enableLambdaSnapStart`: デフォルトはtrue。[Pythonファンクション用のLambda SnapStartをサポートしていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)にデプロイする場合はfalseに設定します。

- CDKをデプロイする前に、デプロイするリージョンのブートストラップを1回実行する必要があります。

```
npx cdk bootstrap
```

- このサンプルプロジェクトをデプロイ

```
npx cdk deploy --require-approval never --all
```

- 以下のような出力が得られます。WebアプリのURLは`BedrockChatStack.FrontendURL`に出力されるので、ブラウザからアクセスしてください。

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

### Mistralモデルのサポートを構成する

[cdk.json](./cdk/cdk.json)の`enableMistral`を`true`に更新し、`npx cdk deploy`を実行します。

```json
...
  "enableMistral": true,
```

> [!Important]
> このプロジェクトはAnthropicのClaudeモデルに焦点を当てており、Mistralモデルは限定的にサポートされています。例えば、プロンプト例はClaudeモデルに基づいています。これはMistralモデル専用のオプションであり、一度有効にすると、チャット機能のためにMistralモデルのみを使用でき、ClaudeとMistralの両方のモデルは使用できません。

### デフォルトのテキスト生成を構成する

ユーザーは、カスタムボット作成画面から[テキスト生成パラメータ](https://docs.anthropic.com/claude/reference/complete_post)を調整できます。ボットが使用されていない場合、[config.py](./backend/app/config.py)で設定されたデフォルトパラメータが使用されます。

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

このアセットは[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)を使用して、言語を自動的に検出します。アプリケーションメニューから言語を切り替えることができます。または、以下に示すようにクエリ文字列を使用して言語を設定することもできます。

> `https://example.com?lng=ja`

### セルフサインアップの無効化

このサンプルはデフォルトでセルフサインアップが有効になっています。セルフサインアップを無効にするには、[cdk.json](./cdk/cdk.json)を開き、`selfSignUpEnabled`を`false`に切り替えます。[外部IDプロバイダ](#external-identity-provider)を設定した場合、この値は無視され、自動的に無効になります。

### サインアップ可能なメールアドレスのドメインを制限する

デフォルトでは、このサンプルはサインアップ可能なメールアドレスのドメインを制限していません。特定のドメインからのみサインアップを許可するには、`cdk.json`を開き、`allowedSignUpEmailDomains`にドメインをリストとして指定します。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部IDプロバイダ

このサンプルは外部IDプロバイダをサポートしています。現在、[Google](./idp/SET_UP_GOOGLE.md)と[カスタムOIDCプロバイダ](./idp/SET_UP_CUSTOM_OIDC.md)をサポートしています。

### 新しいユーザーを自動的にグループに追加する

このサンプルには、ユーザーに権限を与えるために以下のグループがあります：

- [`Admin`](./ADMINISTRATOR.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API.md)

新規作成されたユーザーを自動的にグループに参加させたい場合は、[cdk.json](./cdk/cdk.json)で指定できます。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

デフォルトでは、新規作成されたユーザーは`CreatingBotAllowed`グループに参加します。

### RAGレプリカの構成

[cdk.json](./cdk/cdk.json)の`enableRagReplicas`は、Amazon OpenSearch Serverlessを使用するナレッジベースのレプリカ設定を制御するオプションです。

- **デフォルト**: true
- **true**: 追加のレプリカを有効にして可用性を向上させ、本番環境に適していますが、コストが増加します。
- **false**: レプリカを減らしてコストを削減し、開発とテストに適しています。

これはアカウント/リージョンレベルの設定で、個々のボットではなく、アプリケーション全体に影響します。

> [!Note]
> 2024年6月現在、Amazon OpenSearch Serverlessは0.5 OCUをサポートし、小規模ワークロードのエントリーコストを下げています。本番環境は2 OCUから開始でき、開発/テストワークロードは1 OCUを使用できます。OpenSearch Serverlessは自動的にワークロードの需要に応じてスケーリングします。詳細は[アナウンス](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)をご覧ください。

### クロスリージョン推論

[クロスリージョン推論](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)により、Amazon Bedrockは複数のAWSリージョン間でモデル推論リクエストを動的にルーティングし、ピーク時の需要期間中のスループットと耐性を向上させます。構成するには、`cdk.json`を編集します。

```json
"enableBedrockCrossRegionInference": true
```

### Lambdaスナップスタート

[Lambdaスナップスタート](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)は、Lambdaファンクションのコールドスタート時間を改善し、より良いユーザーエクスペリエンスのためにより高速な応答時間を提供します。一方、Pythonファンクションの場合、[キャッシュサイズに応じた課金](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)と[一部のリージョンでの利用不可](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)があります。スナップスタートを無効にするには、`cdk.json`を編集します。

```json
"enableLambdaSnapStart": false
```

### カスタムドメインの構成

[cdk.json](./cdk/cdk.json)で以下のパラメータを設定することで、CloudFrontディストリビューションのカスタムドメインを構成できます：

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: チャットアプリケーションのカスタムドメイン名（例：chat.example.com）
- `hostedZoneId`: ドメインレコードが作成されるRoute 53ホストゾーンのID

これらのパラメータが提供されると、デプロイメントは自動的に以下を行います：

- us-east-1リージョンでDNS検証を使用してACM証明書を作成
- Route 53ホストゾーンに必要なDNSレコードを作成
- CloudFrontをカスタムドメインを使用するように設定

> [!Note]
> ドメインはAWSアカウントのRoute 53で管理されている必要があります。ホストゾーンIDはRoute 53コンソールで確認できます。

### ローカル開発

[ローカル開発](./LOCAL_DEVELOPMENT.md)を参照してください。

### コントリビューション

このリポジトリへの貢献を検討していただき、ありがとうございます！バグ修正、言語翻訳（i18n）、機能拡張、[エージェントツール](./AGENT.md#how-to-develop-your-own-tools)、その他の改善を歓迎します。

機能拡張やその他の改善については、**プルリクエストを作成する前に、実装アプローチと詳細について議論するために、機能リクエストの課題を作成していただけると大変助かります。バグ修正と言語翻訳（i18n）については、直接プルリクエストを作成してください。**

コントリビュートする前に、以下のガイドラインも確認してください：

- [ローカル開発](./LOCAL_DEVELOPMENT.md)
- [CONTRIBUTING](./CONTRIBUTING.md)

## 連絡先

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 主要貢献者

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## コントリビューター

[![bedrock claude chat コントリビューター](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## ライセンス

このライブラリは MIT-0 ライセンスの下でライセンス供与されています。[LICENSEファイル](./LICENSE)を参照してください。