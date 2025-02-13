# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ja/README.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ko/README.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/zh/README.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/fr/README.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/de/README.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/es/README.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/it/README.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/no/README.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/th/README.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/id/README.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ms/README.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/vi/README.md)

> [!Warning]  
> **V2がリリースされました。アップグレードには[移行ガイド](./migration/V1_TO_V2.md)を必ず注意深く確認してください。** 注意を払わないと、**V1のBOTが使用不可能になります。**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)のLLMモデルを使用した生成的AIによる多言語チャットボット。

### YouTubeで概要とインストールを視聴

[![概要](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](../../imgs/demo.gif)

### ボットのパーソナライズ

独自の指示を追加し、URLやファイルとして外部知識を提供します（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)として知られています）。ボットはアプリケーションユーザー間で共有できます。カスタマイズされたボットはスタンドアロンAPIとしても公開できます（詳細は[こちら](./PUBLISH_API.md)）。

![](../../imgs/bot_creation.png)
![](../../imgs/bot_chat.png)
![](../../imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由から、承認されたユーザーのみがカスタムボットを作成できます。カスタムボットの作成を許可するには、ユーザーは管理コンソール > Amazon CognitoユーザープールまたはAWS CLIを通じて設定できる`CreatingBotAllowed`グループのメンバーである必要があります。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx`からアクセスできます。

### 管理者ダッシュボード

<details>
<summary>管理者ダッシュボード</summary>

管理者ダッシュボードで、ユーザーごと/ボットごとの利用状況を分析します。[詳細](./ADMINISTRATOR.md)

![](../../imgs/admin_bot_analytics.png)

</details>

### LLMベースのエージェント

<details>
<summary>LLMベースのエージェント</summary>

[エージェント機能](./AGENT.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、外部ツールから必要な情報を取得したり、タスクを処理のために複数のステップに分割したりできます。

![](../../imgs/agent1.png)
![](../../imgs/agent2.png)

</details>

## 🚀 超簡単デプロイ

- [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) を us-east-1 リージョンで開き > `モデルアクセスの管理` > `Anthropic / Claude 3` のすべてのオプション、`Amazon / Nova`、`Amazon / Titan Text Embeddings V2`、`Cohere / Embed Multilingual` を有効にし、`変更を保存` をクリックします。

<details>
<summary>スクリーンショット</summary>

![](../../imgs/model_screenshot.png)

</details>

- デプロイするリージョンで [CloudShell](https://console.aws.amazon.com/cloudshell/home) を開きます
- 以下のコマンドでデプロイを実行します。特定のバージョンをデプロイしたり、セキュリティポリシーを適用したい場合は、[オプションパラメータ](#オプションパラメータ)から該当するパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーか v2 の使用かを尋ねられます。v0 のユーザーでない場合は、`y` を入力してください。

### オプションパラメータ

デプロイ時に以下のパラメータを指定して、セキュリティとカスタマイズを向上させることができます：

- **--disable-self-register**: セルフ登録を無効にする（デフォルト：有効）。このフラグが設定されている場合、Cognito で全ユーザーを作成する必要があり、アカウントのセルフ登録は許可されません。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) を有効にする（デフォルト：無効）。このフラグが設定されている場合、Lambda 関数のコールドスタート時間を改善し、より良いユーザー体験のために迅速な応答を提供します。
- **--ipv4-ranges**: 許可される IPv4 範囲のカンマ区切りリスト。（デフォルト：全 IPv4 アドレスを許可）
- **--ipv6-ranges**: 許可される IPv6 範囲のカンマ区切りリスト。（デフォルト：全 IPv6 アドレスを許可）
- **--disable-ipv6**: IPv6 接続を無効にする。（デフォルト：有効）
- **--allowed-signup-email-domains**: 登録に許可されるメールドメインのカンマ区切りリスト。（デフォルト：ドメイン制限なし）
- **--bedrock-region**: Bedrock が利用可能なリージョンを定義。（デフォルト：us-east-1）
- **--repo-url**: フォークまたはカスタムソース管理の場合の、Bedrock Claude Chat のカスタムリポジトリ。（デフォルト：https://github.com/aws-samples/bedrock-claude-chat.git）
- **--version**: デプロイする Bedrock Claude Chat のバージョン。（デフォルト：開発中の最新バージョン）
- **--cdk-json-override**: デプロイ時に上書き JSON ブロックで任意の CDK コンテキスト値を上書きできます。これにより、cdk.json ファイルを直接編集せずに設定を変更できます。

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

上書き JSON は cdk.json と同じ構造に従う必要があります。以下を含む任意のコンテキスト値を上書きできます：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- その他 cdk.json で定義されているコンテキスト値

> [!注意]
> 上書き値は、AWS CodeBuild でのデプロイ時に既存の cdk.json 設定とマージされます。指定された値は cdk.json の値よりも優先されます。

#### パラメータを使用したコマンド例：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 約35分後、ブラウザで開くことができる以下の出力が表示されます

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](../../imgs/signin.png)

上記のように、登録画面が表示され、メールアドレスを登録してサインインできます。

> [!重要]
> オプションパラメータを指定しない場合、このデプロイ方法では URL を知っている誰もが登録できます。本番環境では、セキュリティリスクを最小限に抑えるために、IP アドレス制限を追加し、セルフ登録を無効にすることを強くお勧めします（allowed-signup-email-domains を定義して、会社のドメインのメールアドレスのみが登録できるようにできます）。ipv4-ranges と ipv6-ranges の両方を使用して IP アドレス制限を設定し、./bin 実行時に disable-self-register を使用してセルフ登録を無効にしてください。

> [!ヒント]
> `Frontend URL` が表示されないか、Bedrock Claude Chat が正常に機能しない場合、最新バージョンに問題がある可能性があります。その場合は、`--version "v1.2.6"` をパラメータに追加し、デプロイを再試行してください。

## アーキテクチャ

AWS管理サービスに基づくアーキテクチャであり、インフラストラクチャ管理を不要にします。Amazon Bedrockを使用することで、AWS外のAPIとの通信が不要になります。これにより、スケーラブルで信頼性が高く、安全なアプリケーションの展開が可能になります。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：会話履歴を保存するNoSQLデータベース
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：バックエンドAPIエンドポイント（[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)、[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：フロントエンドアプリケーションの提供（[React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/)：IPアドレス制限
- [Amazon Cognito](https://aws.amazon.com/cognito/)：ユーザー認証
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：APIを介して基本モデルを利用する管理サービス
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)：検索拡張生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）用の管理インターフェースを提供し、ドキュメントの埋め込みと分析のサービスを提供
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：DynamoDBストリームからイベントを受信し、外部知識を埋め込むためのStep Functionsを起動
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：Bedrock Knowledge Basesに外部知識を埋め込むための取り込みパイプラインのオーケストレーション
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：Bedrock Knowledge Basesのバックエンドデータベースとして機能し、正確な情報検索のためのフルテキスト検索とベクター検索機能を提供
- [Amazon Athena](https://aws.amazon.com/athena/)：S3バケットを分析するためのクエリサービス

![](../../imgs/arch.png)

## デプロイ with CDK

[AWS CodeBuild](https://aws.amazon.com/codebuild/)を使用して、CDKで内部的にデプロイする超簡単なデプロイ方法です。このセクションでは、CDKを使用した直接デプロイの手順を説明します。

- UNIX、Docker、Node.js実行環境があることを確認してください。ない場合は、[Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)を使用できます

> [!重要]
> デプロイ中にローカル環境に十分なストレージがない場合、CDKのブートストラップでエラーが発生する可能性があります。Cloud9またはそれに類似した環境で作業する場合は、デプロイ前にインスタンスのボリュームサイズを拡張することをお勧めします。

- このリポジトリをクローンします

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- npmパッケージをインストールします

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- 必要に応じて、[cdk.json](./cdk/cdk.json)の次のエントリを編集します

  - `bedrockRegion`: Bedrockが利用可能なリージョン。**注意：Bedrockはまだすべてのリージョンをサポートしていません。**
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`: 許可されたIPアドレス範囲。
  - `enableLambdaSnapStart`: デフォルトでtrueに設定。[Python関数のLambda SnapStartをサポートしていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)にデプロイする場合はfalseに設定します。

- CDKデプロイの前に、デプロイするリージョンに対して1回ブートストラップを実行する必要があります。

```
npx cdk bootstrap
```

- サンプルプロジェクトをデプロイします

```
npx cdk deploy --require-approval never --all
```

- 以下のような出力が表示されます。Webアプリケーションのアドレスは`BedrockChatStack.FrontendURL`に出力されるので、ブラウザでアクセスしてください。

```sh
 ✅  BedrockChatStack

✨  デプロイ時間: 78.57s

出力:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## その他

### Mistralモデルの設定

[cdk.json](./cdk/cdk.json)の`enableMistral`を`true`に更新し、`npx cdk deploy`を実行します。

```json
...
  "enableMistral": true,
```

> [!重要]
> このプロジェクトはAnthropicのClaudeモデルに焦点を当てており、Mistralモデルは限定的にサポートされています。例えば、プロンプトの例はClaudeモデルに基づいています。これはMistral固有のオプションです。Mistralモデルを有効にすると、Claude、Mistralのモデルの両方ではなく、すべてのチャット機能にMistralモデルのみを使用できます。

### デフォルトのテキスト生成設定

ユーザーは、カスタムボット作成画面で[テキスト生成パラメータ](https://docs.anthropic.com/claude/reference/complete_post)を調整できます。ボットが使用されていない場合、[config.py](./backend/app/config.py)のデフォルトパラメータが使用されます。

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

このアセットは、[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)を使用して言語を自動的に検出します。アプリケーションメニューで言語を切り替えることができます。または、次のようにクエリ文字列で言語を設定できます。

> `https://example.com?lng=ja`

### セルフサインアップの無効化

このサンプルアプリケーションは、デフォルトでセルフサインアップが有効になっています。セルフサインアップを無効にするには、[cdk.json](./cdk/cdk.json)を開き、`selfSignUpEnabled`を`false`に設定します。[外部IDプロバイダ](#外部idプロバイダ)を設定する場合、この値は無視され、自動的に無効になります。

### サインアップ可能なメールアドレスのドメインを制限

デフォルトでは、このサンプルはサインアップ可能なメールアドレスのドメインを制限しません。特定のドメインのみ登録を許可するには、`cdk.json`を開き、`allowedSignUpEmailDomains`にドメインをリストとして指定します。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部IDプロバイダ

このサンプルは外部IDプロバイダをサポートしています。現在、[Google](./idp/SET_UP_GOOGLE.md)と[カスタムOIDCプロバイダ](./idp/SET_UP_CUSTOM_OIDC.md)がサポートされています。

### 新規ユーザーを自動的にグループに追加

このサンプルには、ユーザーに権限を付与するために次のグループがあります：

- [`Admin`](./ADMINISTRATOR.md)
- [`CreatingBotAllowed`](#ボットのパーソナライズ)
- [`PublishAllowed`](./PUBLISH_API.md)

新規作成されたユーザーを自動的にグループに追加したい場合は、[cdk.json](./cdk/cdk.json)でグループを指定できます。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

デフォルトでは、新規作成されたユーザーは`CreatingBotAllowed`グループに追加されます。

## 連絡先

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 重要な貢献者

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## コントリビューター

[![bedrock claude chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## ライセンス

このライブラリは MIT-0 ライセンスの下でライセンス供与されています。詳細については、[ライセンスファイル](./LICENSE) をご確認ください。