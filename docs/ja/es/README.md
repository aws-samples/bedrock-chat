# Bedrock Claude チャット (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ja/README.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ko/README.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/zh/README.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/fr/README.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/de/README.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/es/README.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/it/README.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/no/README.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/th/README.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/id/README.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ms/README.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/vi/README.md)

> [!警告]  
> **V2がリリースされました。更新する場合は、[移行ガイド](./migration/V1_TO_V2.md)を慎重に確認してください。** 注意を払わないと、**V1のボットが使用できなくなります。**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)が提供するLLMモデルを使用した多言語チャットボット。

### YouTubeで概要とインストールを確認

[![概要](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](../../imgs/demo.gif)

### ボットのカスタマイズ

独自の指示を追加し、URLやファイルとして外部知識を提供（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)とも呼ばれる）。ボットはアプリケーションユーザー間で共有できます。カスタムボットは独立したAPIとして公開することも可能です（[詳細](./PUBLISH_API.md)参照）。

![](../../imgs/bot_creation.png)
![](../../imgs/bot_chat.png)
![](../../imgs/bot_api_publish_screenshot3.png)

> [!重要]
> ガバナンス上の理由から、許可されたユーザーのみがカスタムボットを作成できます。カスタムボットの作成を許可するには、ユーザーは`CreatingBotAllowed`という名前のグループのメンバーである必要があります。これは、Amazon Cognitoユーザープールの管理コンソールまたはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできます。

### 管理パネル

<details>
<summary>管理パネル</summary>

管理パネルで各ユーザー/ボットの使用状況を分析します。[詳細](./ADMINISTRATOR.md)

![](../../imgs/admin_bot_analytics.png)

</details>

### LLM搭載エージェント

<details>
<summary>LLM搭載エージェント</summary>

[エージェント機能](./AGENT.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、エージェントは外部ツールから必要な情報を取得したり、タスクを複数のステップに分割して処理したりできます。

![](../../imgs/agent1.png)
![](../../imgs/agent2.png)

</details>

## 🚀 超簡単デプロイ

- us-east-1リージョンで[Bedrockモデルアクセス](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)を開き、`モデルアクセスの管理` > `Anthropic / Claude 3`のすべて、`Amazon / Nova`、`Amazon / Titan Text Embeddings V2`、`Cohere / Embed Multilingual`にチェックを入れ、`変更を保存`をクリックします。

<details>
<summary>スクリーンショット</summary>

![](../../imgs/model_screenshot.png)

</details>

- デプロイしたいリージョンで[CloudShell](https://console.aws.amazon.com/cloudshell/home)を開きます
- 以下のコマンドでデプロイを実行します。特定のバージョンをデプロイしたい場合やセキュリティポリシーを適用する必要がある場合は、[オプションパラメータ](#オプションパラメータ)から適切なパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーかv2を使用しているかを尋ねられます。v0からの継続的なユーザーでない場合は、`y`を入力します。

### オプションパラメータ

デプロイ時に以下のパラメータを指定して、セキュリティとカスタマイズを向上させることができます：

- **--disable-self-register**: 自己登録を無効化（デフォルト：有効）。このフラグが設定されている場合、Cognitoですべてのユーザーを作成する必要があり、ユーザーは自分で登録できなくなります。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)を有効化（デフォルト：無効）。このフラグが設定されている場合、Lambda関数のコールドスタート時間を改善し、ユーザーエクスペリエンスを向上させます。
- **--ipv4-ranges**: カンマ区切りの許可されたIPv4範囲のリスト。（デフォルト：すべてのIPv4アドレスを許可）
- **--ipv6-ranges**: カンマ区切りの許可されたIPv6範囲のリスト。（デフォルト：すべてのIPv6アドレスを許可）
- **--disable-ipv6**: IPv6接続を無効化。（デフォルト：有効）
- **--allowed-signup-email-domains**: 登録を許可するメールドメインのカンマ区切りリスト。（デフォルト：ドメイン制限なし）
- **--bedrock-region**: Bedrockが利用可能なリージョンを定義。（デフォルト：us-east-1）
- **--repo-url**: フォークまたはカスタムソース管理がある場合の、Bedrock Claude Chatのカスタムリポジトリ。（デフォルト：https://github.com/aws-samples/bedrock-claude-chat.git）
- **--version**: デプロイするBedrock Claude Chatのバージョン。（デフォルト：開発中の最新バージョン）
- **--cdk-json-override**: CDKコンテキストの任意の値を上書きできます。これにより、cdk.jsonファイルを直接編集せずに設定を変更できます。

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

上書きJSONはcdk.jsonと同じ構造に従う必要があります。以下を含む任意のコンテキスト値を上書きできます：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- cdk.jsonで定義された他のコンテキスト値

> [!メモ]
> 上書き値は、AWS CodeビルドでのデプロイメントでCDKコンテキスト設定とマージされます。指定された上書き値は、cdk.jsonの値よりも優先されます。

#### パラメータ付きコマンド例：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 約35分後、以下の出力が得られ、ブラウザからアクセスできます

```
フロントエンドURL: https://xxxxxxxxx.cloudfront.net
```

![](../../imgs/signin.png)

上記のように登録画面が表示され、メールアドレスを登録してログインできます。

> [!重要]
> オプションパラメータを設定しない場合、このデプロイ方法では、URLを知っている誰もが登録できます。本番環境では、IPアドレスの制限と自己登録の無効化を強くお勧めします（allowed-signup-email-domainsを設定して、企業のメールドメインのユーザーのみ登録できるようにできます）。IPv4-rangesとipv6-rangesを使用してIPアドレスを制限し、./bin実行時にdisable-self-registerを使用して自己登録を無効にしてください。

> [!ヒント]
> `フロントエンドURL`が表示されないか、Bedrock Claude Chatが正常に機能しない場合、最新バージョンに問題がある可能性があります。その場合は、パラメータに`--version "v1.2.6"`を追加して、デプロイを再試行してください。

## アーキテクチャ

AWS管理サービス上に構築されたアーキテクチャであり、インフラストラクチャの管理の必要性を排除しています。Amazon Bedrockを使用することで、AWS外の外部APIと通信する必要がありません。これにより、スケーラブルで、信頼性が高く、安全なアプリケーションを実装できます。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：会話履歴を保存するためのNoSQLデータベース
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：バックエンドAPIエンドポイント（[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)、[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：フロントエンドアプリケーションの配信（[React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/)：IPアドレスの制限
- [Amazon Cognito](https://aws.amazon.com/cognito/)：ユーザー認証
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：APIを通じて基盤モデルを利用するための管理サービス
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)：検索拡張生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）用の管理インターフェースを提供し、ドキュメントの埋め込みと分析のサービスを提供
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：DynamoDBストリームからイベントを受信し、外部知識を埋め込むためのStep Functionsを開始
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：Bedrock Knowledge Basesに外部知識を埋め込むための取り込みパイプラインのオーケストレーション
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：Bedrock Knowledge Basesのバックエンドデータベースとして機能し、全文検索とベクター検索機能を提供し、関連情報の正確な検索を可能にする
- [Amazon Athena](https://aws.amazon.com/athena/)：S3バケットを分析するためのクエリサービス

![](../../imgs/arch.png)

## CDKを使用した実装

この超簡単な実装では、[AWS CodeBuild](https://aws.amazon.com/codebuild/)を内部的に使用してCDKで展開を行います。このセクションでは、直接CDKで展開する手順を説明します。

- UNIX、Docker、Node.jsランタイム環境を用意してください。ない場合は、[Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)も使用できます

> [!Important]
> 展開中にローカル環境のストレージ容量が不足すると、CDKのブートストラップでエラーが発生する可能性があります。Cloud9などで実行している場合は、展開前にインスタンスボリュームのサイズを拡張することをお勧めします。

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

  - `bedrockRegion`: Bedrockが利用可能なリージョン。**注意：現時点でBedrockはすべてのリージョンでサポートされていません。**
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`: 許可されるIPアドレス範囲。
  - `enableLambdaSnapStart`: デフォルトはtrueです。[Lambda SnapStartがPython関数でサポートされていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)に展開する場合はfalseに設定してください。

- CDKを展開する前に、展開するリージョンに対して一度ブートストラップする必要があります。

```
npx cdk bootstrap
```

- このサンプルプロジェクトを展開

```
npx cdk deploy --require-approval never --all
```

- 以下のような出力が得られます。WebアプリケーションのURLは`BedrockChatStack.FrontendURL`に表示されるので、ブラウザからアクセスしてください。

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

### Mistralモデルのサポートを設定する

[cdk.json](./cdk/cdk.json)の`enableMistral`を`true`に更新し、`npx cdk deploy`を実行します。

```json
...
  "enableMistral": true,
```

> [!重要]
> このプロジェクトはAnthropicのClaudeモデルに焦点を当てており、Mistralモデルのサポートは限定的です。例えば、プロンプト例はClaudeモデルに基づいています。これはMistral用のオプションのみであり、Mistralモデルを有効にすると、ClaudeとMistralの両方のモデルではなく、Mistralモデルのみを使用できます。

### デフォルトのテキスト生成を設定する

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

CLIとCDKを使用している場合は、`npx cdk destroy`を実行します。そうでない場合は、[CloudFormation](https://console.aws.amazon.com/cloudformation/home)にアクセスし、`BedrockChatStack`と`FrontendWafStack`を手動で削除します。`FrontendWafStack`は`us-east-1`リージョンにあることに注意してください。

### 言語設定

このアセットは[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)を使用して言語を自動検出します。アプリケーションメニューから言語を変更できます。または、以下に示すようにクエリ文字列を使用して言語を設定できます。

> `https://example.com?lng=ja`

### 自動サインアップを無効にする

この例では、デフォルトで自動サインアップが有効になっています。無効にするには、[cdk.json](./cdk/cdk.json)を開き、`selfSignUpEnabled`を`false`に変更します。[外部IDプロバイダ](#external-identity-provider)を設定した場合、この値は無視され、自動的に無効になります。

### サインアップ用のメールドメインを制限する

デフォルトでは、この例はサインアップ用のメールドメインを制限しません。特定のドメインからのみサインアップを許可するには、`cdk.json`を開き、`allowedSignUpEmailDomains`にドメインをリストとして指定します。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部IDプロバイダ

この例は外部IDプロバイダをサポートしています。現在、[Google](./idp/SET_UP_GOOGLE.md)と[カスタムOIDCプロバイダ](./idp/SET_UP_CUSTOM_OIDC.md)をサポートしています。

### ユーザーを自動的にグループに追加する

この例では、ユーザーに権限を与えるために次のグループがあります：

- [`Admin`](./ADMINISTRATOR.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API.md)

新規作成されたユーザーを自動的にグループに参加させたい場合は、[cdk.json](./cdk/cdk.json)で指定できます。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

デフォルトでは、新規作成されたユーザーは`CreatingBotAllowed`グループに参加します。

### RAGレプリカの設定

`enableRagReplicas`は[cdk.json](./cdk/cdk.json)のオプションで、Amazon OpenSearch Serverlessを使用するナレッジベースのデータベースレプリカの設定を制御します。

- **デフォルト**: true
- **true**: 追加のレプリカを有効にすることで可用性を向上させ、本番環境に適していますが、コストが増加します。
- **false**: レプリカを減らしてコストを削減し、開発とテストに適しています。

これはアカウント/リージョンレベルの設定で、アプリケーション全体に影響します。

> [!注意]
> 2024年6月現在、Amazon OpenSearch Serverlessは0.5 OCUをサポートし、小規模ワークロードのエントリコストを削減しています。本番ワークロードは2 OCUから開始でき、開発/テストワークロードは1 OCUを使用できます。OpenSearch Serverlessはワークロードの需要に応じて自動的にスケーリングします。詳細については、[アナウンス](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)をご覧ください。

### リージョン間推論

[リージョン間推論](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)により、Amazon Bedrockは高需要期間中に複数のAWSリージョン間でモデル推論リクエストを動的にルーティングし、パフォーマンスと耐障害性を向上させます。設定するには、`cdk.json`を編集します。

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)は、Lambdaファンクションのコールドスタート時間を改善し、ユーザーエクスペリエンスをより良くします。一方、Pythonファンクションの場合、[キャッシュサイズに依存する料金](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)があり、[現在一部のリージョンで利用できません](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)。SnapStartを無効にするには、`cdk.json`を編集します。

```json
"enableLambdaSnapStart": false
```

### カスタムドメインの設定

[cdk.json](./cdk/cdk.json)で以下のパラメータを設定することで、CloudFrontディストリビューションのカスタムドメインを設定できます：

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: チャットアプリケーションのカスタムドメイン名（例：chat.example.com）
- `hostedZoneId`: DNS レコードが作成されるRoute 53ホストゾーンのID

これらのパラメータが提供されると、デプロイメントは自動的に以下を行います：

- us-east-1リージョンでDNS検証を使用したACM証明書を作成
- Route 53ホストゾーンに必要なDNSレコードを作成
- CloudFrontにカスタムドメインを使用するよう設定

> [!注意]
> ドメインはAWSアカウントのRoute 53で管理されている必要があります。ホストゾーンIDはRoute 53コンソールで確認できます。

### ローカル開発

[ローカル開発](./LOCAL_DEVELOPMENT.md)を参照してください。

### 貢献

このリポジトリに貢献を検討していただき、ありがとうございます！バグ修正、言語翻訳（i18n）、機能改善、[エージェントツール](./AGENT.md#how-to-develop-your-own-tools)などの改善を歓迎しています。

機能改善やその他の改善については、**プルリクエストを作成する前に、実装アプローチと詳細について議論するために機能リクエストIssueを作成していただけると感謝します。バグ修正と言語翻訳（i18n）については、直接プルリクエストを作成してください。**

貢献する前に、以下のガイドラインをご確認ください：

- [ローカル開発](./LOCAL_DEVELOPMENT.md)
- [貢献](./CONTRIBUTING.md)

## 連絡先

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 重要な貢献者

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## コントリビューター

[![bedrock claude chatのコントリビューター](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## ライセンス

このライブラリは MIT-0 ライセンスの下でライセンスされています。[ライセンスファイル](./LICENSE) を参照してください。