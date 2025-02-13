# Bedrock Claude チャット (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ja/README.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ko/README.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/zh/README.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/fr/README.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/de/README.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/es/README.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/it/README.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/no/README.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/th/README.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/id/README.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ko/README.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/vi/README.md)

> [!Warning]  
> **V2がリリースされました。更新する際は、[移行ガイド](./migration/V1_TO_V2.md)を慎重に確認してください。** 注意を払わないと、**V1のBOTは使用できなくなります。**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)が提供する大規模言語モデル（LLM）を使用した多言語チャットボット。

### YouTubeで概要とインストール方法を見る

[![概要](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](../../imgs/demo.gif)

### ボットのパーソナライズ

独自の指示を追加し、URLやファイルで外部知識を提供できます（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。ボットはアプリケーションユーザー間で共有できます。カスタマイズしたボットはスタンドアロンAPIとして公開することもできます（[詳細](./PUBLISH_API.md)参照）。

![](../../imgs/bot_creation.png)
![](../../imgs/bot_chat.png)
![](../../imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由から、許可されたユーザーのみがカスタムボットを作成できます。カスタムボットの作成を許可するには、ユーザーが`CreatingBotAllowed`グループのメンバーである必要があります。これは管理コンソール > Amazon Cognito ユーザープールまたはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx`からアクセスできます。

### 管理者ダッシュボード

<details>
<summary>管理者ダッシュボード</summary>

管理者ダッシュボードで、ユーザーごと/ボットごとの利用状況を分析できます。[詳細](./ADMINISTRATOR.md)

![](../../imgs/admin_bot_analytics.png)

</details>

### LLMベースのエージェント

<details>
<summary>LLMベースのエージェント</summary>

[エージェント機能](./AGENT.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、エージェントは外部ツールから必要な情報を取得したり、タスクを複数のステップに分解して処理したりできます。

![](../../imgs/agent1.png)
![](../../imgs/agent2.png)

</details>

## 🚀 超簡単デプロイ

- us-east-1リージョンで、[Bedrock モデルアクセス](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)を開き > `モデルアクセスの管理` > `Anthropic / Claude 3`のすべて、`Amazon / Nova`、`Amazon / Titan Text Embeddings V2`、`Cohere / Embed Multilingual`をすべてチェックし、`変更を保存`をクリックします。

<details>
<summary>スクリーンショット</summary>

![](../../imgs/model_screenshot.png)

</details>

- デプロイしたいリージョンで[CloudShell](https://console.aws.amazon.com/cloudshell/home)を開きます
- 以下のコマンドでデプロイを実行します。デプロイするバージョンを指定したい場合やセキュリティポリシーを適用する必要がある場合は、[オプションパラメータ](#optional-parameters)から適切なパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーかv2を使用するかを尋ねられます。v0からの継続ユーザーでない場合は、`y`を入力してください。

### オプションパラメータ

デプロイ時に以下のパラメータを指定して、セキュリティとカスタマイズを強化できます：

- **--disable-self-register**: 自己登録を無効化（デフォルト：有効）。このフラグが設定されている場合、すべてのユーザーをCognitoで作成する必要があり、ユーザーの自己登録は許可されません。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)を有効化（デフォルト：無効）。このフラグが設定されている場合、Lambda関数のコールドスタート時間を改善し、ユーザーエクスペリエンスを向上させます。
- **--ipv4-ranges**: 許可されたIPv4範囲のカンマ区切りリスト。（デフォルト：すべてのIPv4アドレスを許可）
- **--ipv6-ranges**: 許可されたIPv6範囲のカンマ区切りリスト。（デフォルト：すべてのIPv6アドレスを許可）
- **--disable-ipv6**: IPv6接続を無効化。（デフォルト：有効）
- **--allowed-signup-email-domains**: サインアップに許可されるメールドメインのカンマ区切りリスト。（デフォルト：ドメイン制限なし）
- **--bedrock-region**: Bedrockが利用可能なリージョンを定義。（デフォルト：us-east-1）
- **--repo-url**: フォークまたはカスタムソース管理の場合、Bedrock Claude Chatのカスタムリポジトリ。（デフォルト：https://github.com/aws-samples/bedrock-claude-chat.git）
- **--version**: デプロイするBedrock Claude Chatのバージョン。（デフォルト：開発中の最新バージョン）
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

上書きJSONは、cdk.jsonと同じ構造に従う必要があります。以下を含む任意のコンテキスト値を上書きできます：

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
> 上書き値は、AWS CodeBuildデプロイ時に既存のcdk.json設定とマージされます。指定された上書き値は、cdk.jsonの値よりも優先されます。

#### パラメータを使用したコマンド例：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 約35分後、以下の出力が表示され、ブラウザからアクセスできます

```
フロントエンドURL: https://xxxxxxxxx.cloudfront.net
```

![](../../imgs/signin.png)

上記のようにサインアップ画面が表示され、メールを登録してログインできます。

> [!Important]
> オプションパラメータを設定しない場合、URLを知っている人は誰でもサインアップできます。本番環境では、セキュリティリスクを軽減するために、IPアドレス制限を追加し、自己サインアップを無効にすることを強くお勧めします（allowed-signup-email-domainsを定義して、会社のドメインのメールアドレスのみがサインアップできるように制限できます）。./binを実行する際は、ipv4-rangesとipv6-rangesを使用してIPアドレス制限を設定し、disable-self-registerを使用して自己サインアップを無効にしてください。

> [!TIP]
> `フロントエンドURL`が表示されないか、Bedrock Claude Chatが正常に動作しない場合、最新バージョンに問題がある可能性があります。この場合、`--version "v1.2.6"`をパラメータに追加してデプロイを再試行してください。

## アーキテクチャ

AWSマネージドサービスに基づいて構築されたアーキテクチャであり、インフラストラクチャ管理の必要性を排除しています。Amazon Bedrockを利用することで、AWS外のAPIと通信する必要がなくなります。これにより、スケーラブルで信頼性が高く、セキュアなアプリケーションを展開できます。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：会話履歴を保存するためのNoSQLデータベース
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：バックエンドAPIエンドポイント（[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)、[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：フロントエンドアプリケーションの配信（[React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/)：IPアドレス制限
- [Amazon Cognito](https://aws.amazon.com/cognito/)：ユーザー認証
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：APIを介して基盤モデルを利用するマネージドサービス
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)：検索拡張生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）のためのマネージドインターフェースを提供し、ドキュメントの埋め込みと解析サービスを提供
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：DynamoDBストリームからイベントを受信し、外部知識を埋め込むStep Functionsを起動
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：Bedrock Knowledge Baseに外部知識を埋め込むための取り込みパイプラインのオーケストレーション
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：Bedrock Knowledge Basesのバックエンドデータベースとして機能し、全文検索とベクター検索機能を提供し、関連情報の正確な取得を可能にする
- [Amazon Athena](https://aws.amazon.com/athena/)：S3バケットを分析するためのクエリサービス

![](../../imgs/arch.png)

## CDKを使用したデプロイ

簡単デプロイは、[AWS CodeBuild](https://aws.amazon.com/codebuild/)を使用して、内部的にCDKによるデプロイを実行します。このセクションでは、CDKを直接使用したデプロイ手順を説明します。

- UNIX、Docker、Node.jsランタイム環境が必要です。ない場合は、[Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)を使用することもできます。

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
  - `enableLambdaSnapStart`: デフォルトはtrueです。[Python関数のLambda SnapStartをサポートしていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)にデプロイする場合はfalseに設定します。

- CDKをデプロイする前に、デプロイするリージョンでブートストラップを1回実行する必要があります。

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

### Mistralモデルのサポートを設定

[cdk.json](./cdk/cdk.json)の`enableMistral`を`true`に更新し、`npx cdk deploy`を実行します。

```json
...
  "enableMistral": true,
```

> [!重要]
> このプロジェクトはAnthropicのClaudeモデルに焦点を当てており、Mistralモデルのサポートは限定的です。例えば、プロンプトの例はClaudeモデルに基づいています。これはMistral専用のオプションであり、一度Mistralモデルを有効にすると、すべてのチャット機能でMistralモデルのみを使用でき、ClaudeとMistralの両方のモデルは使用できません。

### デフォルトのテキスト生成を設定

ユーザーは、カスタムボット作成画面から[テキスト生成パラメータ](https://docs.anthropic.com/claude/reference/complete_post)を調整できます。ボットが使用されない場合、[config.py](./backend/app/config.py)で設定されたデフォルトパラメータが使用されます。

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

このアセットは[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)を使用して言語を自動検出します。アプリケーションメニューから言語を切り替えることができます。または、以下に示すようにクエリ文字列を使用して言語を設定することもできます。

> `https://example.com?lng=ja`

### セルフサインアップを無効にする

このサンプルはデフォルトでセルフサインアップが有効になっています。セルフサインアップを無効にするには、[cdk.json](./cdk/cdk.json)を開き、`selfSignUpEnabled`を`false`に切り替えます。[外部IDプロバイダ](#外部idプロバイダ)を設定すると、この値は無視され、自動的に無効になります。

### サインアップ可能なメールアドレスのドメインを制限

デフォルトでは、このサンプルはサインアップ可能なメールアドレスのドメインを制限していません。特定のドメインからのみサインアップを許可するには、`cdk.json`を開き、`allowedSignUpEmailDomains`にドメインをリストとして指定します。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部IDプロバイダ

このサンプルは外部IDプロバイダをサポートしています。現在、[Google](./idp/SET_UP_GOOGLE.md)と[カスタムOIDCプロバイダ](./idp/SET_UP_CUSTOM_OIDC.md)をサポートしています。

### 新規ユーザーを自動的にグループに追加

このサンプルには、ユーザーに権限を与えるために以下のグループがあります：

- [`Admin`](./ADMINISTRATOR.md)
- [`CreatingBotAllowed`](#ボットのパーソナライズ)
- [`PublishAllowed`](./PUBLISH_API.md)

新規作成されたユーザーを自動的にグループに参加させたい場合は、[cdk.json](./cdk/cdk.json)で指定できます。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

デフォルトでは、新規作成されたユーザーは`CreatingBotAllowed`グループに参加します。

### RAGレプリカを設定

`enableRagReplicas`は[cdk.json](./cdk/cdk.json)のオプションで、Amazon OpenSearch Serverlessを使用するナレッジベースのレプリカ設定を制御します。

- **デフォルト**: true
- **true**: 追加のレプリカを有効にして可用性を向上させ、本番環境に適していますが、コストが増加します。
- **false**: レプリカを減らしてコストを削減し、開発とテストに適しています。

これはアカウント/リージョンレベルの設定で、個々のボットではなくアプリケーション全体に影響します。

> [!メモ]
> 2024年6月現在、Amazon OpenSearch Serverlessは0.5 OCUをサポートし、小規模ワークロードのエントリーコストを低減しています。本番展開は2 OCUから開始でき、開発/テストワークロードは1 OCUを使用できます。OpenSearch Serverlessは、ワークロードの需要に応じて自動的にスケーリングします。詳細は[アナウンス](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)をご覧ください。

### クロスリージョン推論

[クロスリージョン推論](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)により、Amazon Bedrockは複数のAWSリージョン間でモデル推論リクエストを動的にルーティングし、ピーク時の需要期間中のスループットと回復力を向上させます。設定するには、`cdk.json`を編集します。

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)は、Lambdaファンクションのコールドスタート時間を改善し、よりユーザーエクスペリエンスの良い高速な応答時間を提供します。一方、Pythonファンクションの場合、[キャッシュサイズに応じた課金](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)があり、[現在一部のリージョンでは利用できません](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)。SnapStartを無効にするには、`cdk.json`を編集します。

```json
"enableLambdaSnapStart": false
```

### カスタムドメインを設定

[cdk.json](./cdk/cdk.json)で以下のパラメータを設定することで、CloudFrontディストリビューションのカスタムドメインを設定できます：

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: チャットアプリケーションのカスタムドメイン名（例：chat.example.com）
- `hostedZoneId`: DNSレコードが作成されるRoute 53ホストゾーンのID

これらのパラメータが提供されると、デプロイメントは自動的に以下を行います：

- us-east-1リージョンでDNS検証を使用したACM証明書を作成
- Route 53ホストゾーンに必要なDNSレコードを作成
- CloudFrontをカスタムドメインを使用するように設定

> [!メモ]
> ドメインはAWSアカウントのRoute 53で管理されている必要があります。ホストゾーンIDはRoute 53コンソールで確認できます。

### ローカル開発

[ローカル開発](./LOCAL_DEVELOPMENT.md)を参照してください。

### 貢献

このリポジトリに貢献を検討していただき、ありがとうございます！バグ修正、言語翻訳（i18n）、機能拡張、[エージェントツール](./AGENT.md#独自のツールを開発する方法)、その他の改善を歓迎します。

機能拡張やその他の改善については、**プルリクエストを作成する前に、実装アプローチと詳細について議論するためにフィーチャーリクエストの課題を作成していただければ幸いです。バグ修正や言語翻訳（i18n）については、直接プルリクエストを作成してください。**

貢献する前に、以下のガイドラインも確認してください：

- [ローカル開発](./LOCAL_DEVELOPMENT.md)
- [貢献](./CONTRIBUTING.md)

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

このライブラリは MIT-0 ライセンスの下でライセンス供与されています。[ライセンスファイル](./LICENSE)を参照してください。