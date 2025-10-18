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


[Amazon Bedrock](https://aws.amazon.com/bedrock/)を活用した多言語生成AI プラットフォームです。
チャット、知識を持つカスタムボット（RAG）、ボットストアを通じたボット共有、エージェントを使用したタスク自動化をサポートしています。

![](./imgs/demo.gif)

> [!Warning]
>
> **V3がリリースされました。アップデートする場合は、[移行ガイド](./migration/V2_TO_V3_ja-JP.md)を慎重に確認してください。** 注意を払わない場合、**V2のボットは使用できなくなります。**

### ボットのパーソナライズ化 / ボットストア

独自の指示と知識（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)として知られる）を追加できます。ボットはボットストアマーケットプレイスを通じてアプリケーションユーザー間で共有できます。カスタマイズされたボットはスタンドアロンAPIとしても公開できます（[詳細](./PUBLISH_API_ja-JP.md)をご覧ください）。

<details>
<summary>スクリーンショット</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

既存の[Amazon BedrockのKnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/)をインポートすることもできます。

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> ガバナンス上の理由から、許可されたユーザーのみがカスタマイズされたボットを作成できます。カスタマイズされたボットの作成を許可するには、ユーザーは`CreatingBotAllowed`というグループのメンバーである必要があります。これは管理コンソール > Amazon Cognito User poolsまたはaws cliを通じて設定できます。ユーザープールIDはCloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`でアクセスできます。

### 管理機能

APIの管理、ボットを必須としてマーク付け、ボットの使用状況分析。[詳細](./ADMINISTRATOR_ja-JP.md)

<details>
<summary>スクリーンショット</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### エージェント

[エージェント機能](./AGENT_ja-JP.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、エージェントは外部ツールから必要な情報を取得したり、タスクを複数のステップに分解して処理したりすることができます。

<details>
<summary>スクリーンショット</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 簡単なデプロイメント

- us-east-1リージョンで、[Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` を開き、使用したいすべてのモデルにチェックを入れて `Save changes` をクリックします。

<details>
<summary>スクリーンショット</summary>

![](./imgs/model_screenshot.png)

</details>

### サポートされているリージョン

ボットやナレッジベースを作成する場合（OpenSearch Serverlessがデフォルトの選択肢です）、Bedrock Chatを[OpenSearch ServerlessとIngestion APIが利用可能なリージョン](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html)にデプロイしていることを確認してください。2025年8月現在、以下のリージョンがサポートされています：us-east-1、us-east-2、us-west-1、us-west-2、ap-south-1、ap-northeast-1、ap-northeast-2、ap-southeast-1、ap-southeast-2、ca-central-1、eu-central-1、eu-west-1、eu-west-2、eu-south-2、eu-north-1、sa-east-1

**bedrock-region**パラメータについては、[Bedrockが利用可能なリージョン](https://docs.aws.amazon.com/general/latest/gr/bedrock.html)から選択する必要があります。

- デプロイしたいリージョンで[CloudShell](https://console.aws.amazon.com/cloudshell/home)を開きます
- 以下のコマンドでデプロイを実行します。デプロイするバージョンを指定したい場合やセキュリティポリシーを適用する必要がある場合は、[オプションパラメータ](#optional-parameters)から適切なパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーかv3を使用しているかを確認されます。v0からの継続ユーザーでない場合は、`y`を入力してください。

### オプションパラメータ

デプロイ時に以下のパラメータを指定することで、セキュリティとカスタマイズを強化できます：

- **--disable-self-register**: セルフ登録を無効にします（デフォルト：有効）。このフラグを設定すると、すべてのユーザーをcognitoで作成する必要があり、ユーザーが自分でアカウントを登録することはできません。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)を有効にします（デフォルト：無効）。このフラグを設定すると、Lambda関数のコールドスタート時間が改善され、より良いユーザー体験のために応答時間が速くなります。
- **--ipv4-ranges**: 許可するIPv4範囲のカンマ区切りリスト。（デフォルト：すべてのipv4アドレスを許可）
- **--ipv6-ranges**: 許可するIPv6範囲のカンマ区切りリスト。（デフォルト：すべてのipv6アドレスを許可）
- **--disable-ipv6**: IPv6接続を無効にします。（デフォルト：有効）
- **--allowed-signup-email-domains**: サインアップを許可するメールドメインのカンマ区切りリスト。（デフォルト：ドメイン制限なし）
- **--bedrock-region**: bedrockが利用可能なリージョンを定義します。（デフォルト：us-east-1）
- **--repo-url**: フォークまたはカスタムソースコントロールの場合、デプロイするBedrock Chatのカスタムリポジトリ。（デフォルト：https://github.com/aws-samples/bedrock-chat.git）
- **--version**: デプロイするBedrock Chatのバージョン。（デフォルト：開発中の最新バージョン）
- **--cdk-json-override**: デプロイ時にオーバーライドJSONブロックを使用して、任意のCDKコンテキスト値をオーバーライドできます。これにより、cdk.jsonファイルを直接編集せずに設定を変更できます。

使用例：

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

オーバーライドJSONはcdk.jsonと同じ構造に従う必要があります。以下を含む任意のコンテキスト値をオーバーライドできます：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: 有効にするモデルIDのリストを受け付けます。デフォルト値は空のリストで、すべてのモデルが有効になります。
- `logoPath`: ナビゲーションドロワーの上部に表示されるロゴアセットのフロントエンド`public/`ディレクトリ内の相対パス。
- およびcdk.jsonで定義されているその他のコンテキスト値

> [!Note]
> オーバーライド値は、AWSコードビルドでのデプロイ時に既存のcdk.json設定とマージされます。オーバーライドで指定された値は、cdk.jsonの値よりも優先されます。

#### パラメータを使用したコマンド例：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 約35分後、ブラウザからアクセスできる以下の出力が表示されます

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

上記のようなサインアップ画面が表示され、メールアドレスを登録してログインできます。

> [!Important]
> オプションパラメータを設定しない場合、このデプロイ方法ではURLを知っている誰でもサインアップできます。本番環境での使用には、セキュリティリスクを軽減するためにIPアドレス制限を追加し、セルフサインアップを無効にすることを強く推奨します（allowed-signup-email-domainsを定義して、会社のドメインのメールアドレスのみがサインアップできるようにユーザーを制限できます）。IPアドレス制限にはipv4-rangesとipv6-rangesの両方を使用し、./binを実行する際にdisable-self-registerを使用してセルフサインアップを無効にしてください。

> [!TIP]
> `Frontend URL`が表示されない場合やBedrock Chatが正常に動作しない場合は、最新バージョンに問題がある可能性があります。この場合は、パラメータに`--version "v3.0.0"`を追加してデプロイを再試行してください。

## アーキテクチャ

AWSのマネージドサービスを基盤としたアーキテクチャで、インフラストラクチャの管理が不要です。Amazon Bedrockを利用することで、AWS外部のAPIとの通信が不要になります。これにより、スケーラブルで信頼性が高く、安全なアプリケーションのデプロイが可能になります。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): 会話履歴を保存するNoSQLデータベース
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): バックエンドAPIエンドポイント（[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)、[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): フロントエンドアプリケーションの配信（[React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/): IPアドレス制限
- [Amazon Cognito](https://aws.amazon.com/cognito/): ユーザー認証
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): APIを通じて基盤モデルを利用するためのマネージドサービス
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Retrieval-Augmented Generation（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）のためのマネージドインターフェースを提供し、文書の埋め込みと解析のサービスを提供
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): DynamoDBストリームからイベントを受信し、外部知識を埋め込むためのStep Functionsを起動
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Bedrock Knowledge Basesに外部知識を埋め込むための取り込みパイプラインを調整
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Bedrock Knowledge Basesのバックエンドデータベースとして機能し、全文検索とベクトル検索機能を提供して、関連情報の正確な検索を可能に
- [Amazon Athena](https://aws.amazon.com/athena/): S3バケットを分析するためのクエリサービス

![](./imgs/arch.png)

## CDKを使用したデプロイ

Super-easy Deploymentは内部でCDKによるデプロイを実行するために[AWS CodeBuild](https://aws.amazon.com/codebuild/)を使用します。このセクションではCDKを直接使用したデプロイ手順について説明します。

- UNIX、DockerおよびNode.jsランタイム環境が必要です。

> [!Important]
> デプロイ時にローカル環境のストレージ容量が不足している場合、CDKブートストラップでエラーが発生する可能性があります。デプロイ前にインスタンスのボリュームサイズを拡張することをお勧めします。

- このリポジトリをクローンします

```
git clone https://github.com/aws-samples/bedrock-chat
```

- npmパッケージをインストールします

```
cd bedrock-chat
cd cdk
npm ci
```

- 必要に応じて[cdk.json](./cdk/cdk.json)の以下のエントリを編集します。

  - `bedrockRegion`: Bedrockが利用可能なリージョン。**注: Bedrockはすべてのリージョンをサポートしているわけではありません。**
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`: 許可するIPアドレスの範囲。
  - `enableLambdaSnapStart`: デフォルトはtrue。[Python関数のLambda SnapStartをサポートしていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)にデプロイする場合はfalseに設定します。
  - `globalAvailableModels`: デフォルトはすべて。設定する場合（モデルIDのリスト）、Bedrock Chatアプリケーションのすべてのユーザーのチャット全体とボット作成時にドロップダウンメニューに表示されるモデルをグローバルに制御できます。
  - `logoPath`: アプリケーションドロワーの上部に表示される画像を指す`frontend/public`配下の相対パス。
以下のモデルIDがサポートされています（デプロイリージョンのBedrockコンソールのModel accessでも有効になっていることを確認してください）：
- **Claude Models:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Amazon Nova Models:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Mistral Models:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **DeepSeek Models:** `deepseek-r1`
- **Meta Llama Models:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

完全なリストは[index.ts](./frontend/src/constants/index.ts)で確認できます。

- CDKをデプロイする前に、デプロイ先のリージョンに対して一度Bootstrapを実行する必要があります。

```
npx cdk bootstrap
```

- このサンプルプロジェクトをデプロイします

```
npx cdk deploy --require-approval never --all
```

- 以下のような出力が得られます。WebアプリケーションのURLは`BedrockChatStack.FrontendURL`に出力されるので、ブラウザからアクセスしてください。

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### パラメータの定義

デプロイのパラメータは`cdk.json`を使用する方法と、型安全な`parameter.ts`ファイルを使用する方法の2つの方法で定義できます。

#### cdk.jsonの使用（従来の方法）

パラメータを設定する従来の方法は`cdk.json`ファイルを編集することです。このアプローチは単純ですが、型チェックはありません：

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

#### parameter.tsの使用（推奨される型安全な方法）

より良い型安全性と開発者体験のために、`parameter.ts`ファイルを使用してパラメータを定義できます：

```typescript
// デフォルト環境のパラメータを定義
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

// 追加環境のパラメータを定義
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 開発環境のコスト削減
  enableBotStoreReplicas: false, // 開発環境のコスト削減
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 本番環境の可用性向上
  enableBotStoreReplicas: true, // 本番環境の可用性向上
});
```

> [!Note]
> 既存のユーザーは`cdk.json`を変更せずに引き続き使用できます。`parameter.ts`アプローチは新規デプロイまたは複数環境を管理する必要がある場合に推奨されます。

### 複数環境のデプロイ

`parameter.ts`ファイルと`-c envName`オプションを使用して、同じコードベースから複数の環境をデプロイできます。

#### 前提条件

1. 上記のように`parameter.ts`で環境を定義する
2. 各環境には環境固有のプレフィックスを持つ独自のリソースセットがあります

#### デプロイコマンド

特定の環境をデプロイするには：

```bash
# 開発環境をデプロイ
npx cdk deploy --all -c envName=dev

# 本番環境をデプロイ
npx cdk deploy --all -c envName=prod
```

環境が指定されていない場合、「default」環境が使用されます：

```bash
# デフォルト環境をデプロイ
npx cdk deploy --all
```

#### 重要な注意事項

1. **スタックの命名**：

   - 各環境のメインスタックには環境名のプレフィックスが付きます（例：`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - ただし、カスタムボットスタック（`BrChatKbStack*`）とAPI公開スタック（`ApiPublishmentStack*`）は実行時に動的に作成されるため、環境プレフィックスは付きません

2. **リソースの命名**：

   - 一部のリソースのみ名前に環境プレフィックスが付きます（例：`dev_ddb_export`テーブル、`dev-FrontendWebAcl`）
   - ほとんどのリソースは元の名前を維持しますが、異なるスタックに存在することで分離されています

3. **環境の識別**：

   - すべてのリソースには環境名を含む`CDKEnvironment`タグが付けられます
   - このタグを使用してリソースがどの環境に属しているかを識別できます
   - 例：`CDKEnvironment: dev`または`CDKEnvironment: prod`

4. **デフォルト環境のオーバーライド**：`parameter.ts`で「default」環境を定義すると、`cdk.json`の設定がオーバーライドされます。`cdk.json`を引き続き使用するには、`parameter.ts`で「default」環境を定義しないでください。

5. **環境要件**：「default」以外の環境を作成するには、`parameter.ts`を使用する必要があります。対応する環境定義がない場合、`-c envName`オプションだけでは不十分です。

6. **リソースの分離**：各環境は独自のリソースセットを作成するため、同じAWSアカウント内で開発、テスト、本番環境を競合なく持つことができます。

## その他

デプロイメントのパラメータを定義するには2つの方法があります: `cdk.json`を使用する方法と、型安全な`parameter.ts`ファイルを使用する方法です。

#### cdk.jsonの使用（従来の方法）

パラメータを設定する従来の方法は、`cdk.json`ファイルを編集することです。このアプローチはシンプルですが、型チェックがありません：

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

#### parameter.tsの使用（推奨される型安全な方法）

より良い型安全性と開発者体験のために、`parameter.ts`ファイルを使用してパラメータを定義できます：

```typescript
// デフォルト環境のパラメータを定義
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// 追加環境のパラメータを定義
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 開発環境のコスト削減
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 本番環境の可用性向上
});
```

> [!Note]
> 既存のユーザーは`cdk.json`を変更せずに引き続き使用できます。`parameter.ts`アプローチは、新規デプロイメントや複数環境を管理する必要がある場合に推奨されます。

### 複数環境のデプロイ

`parameter.ts`ファイルと`-c envName`オプションを使用して、同じコードベースから複数の環境をデプロイできます。

#### 前提条件

1. 上記のように`parameter.ts`で環境を定義する
2. 各環境は、環境固有のプレフィックスを持つ独自のリソースセットを持つ

#### デプロイメントコマンド

特定の環境をデプロイするには：

```bash
# 開発環境のデプロイ
npx cdk deploy --all -c envName=dev

# 本番環境のデプロイ
npx cdk deploy --all -c envName=prod
```

環境が指定されていない場合、「default」環境が使用されます：

```bash
# デフォルト環境のデプロイ
npx cdk deploy --all
```

#### 重要な注意事項

1. **スタックの命名**：

   - 各環境のメインスタックには環境名のプレフィックスが付きます（例：`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - ただし、カスタムボットスタック（`BrChatKbStack*`）とAPIパブリッシングスタック（`ApiPublishmentStack*`）は実行時に動的に作成されるため、環境プレフィックスは付きません

2. **リソースの命名**：

   - 一部のリソースのみ名前に環境プレフィックスが付きます（例：`dev_ddb_export`テーブル、`dev-FrontendWebAcl`）
   - ほとんどのリソースは元の名前を維持しますが、異なるスタックにあることで分離されます

3. **環境の識別**：

   - すべてのリソースには環境名を含む`CDKEnvironment`タグが付けられます
   - このタグを使用してリソースがどの環境に属しているかを識別できます
   - 例：`CDKEnvironment: dev`または`CDKEnvironment: prod`

4. **デフォルト環境のオーバーライド**：`parameter.ts`で「default」環境を定義すると、`cdk.json`の設定がオーバーライドされます。`cdk.json`を引き続き使用するには、`parameter.ts`で「default」環境を定義しないでください。

5. **環境要件**：「default」以外の環境を作成するには、`parameter.ts`を使用する必要があります。対応する環境定義がない場合、`-c envName`オプションだけでは不十分です。

6. **リソースの分離**：各環境は独自のリソースセットを作成するため、同じAWSアカウント内で開発、テスト、本番環境を競合なく持つことができます。

## その他

### リソースの削除

CLIとCDKを使用している場合は、`npx cdk destroy`を実行してください。使用していない場合は、[CloudFormation](https://console.aws.amazon.com/cloudformation/home)にアクセスし、`BedrockChatStack`と`FrontendWafStack`を手動で削除してください。`FrontendWafStack`は`us-east-1`リージョンにあることにご注意ください。

### 言語設定

このアセットは[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)を使用して言語を自動検出します。アプリケーションメニューから言語を切り替えることができます。また、以下のようにクエリ文字列を使用して言語を設定することもできます。

> `https://example.com?lng=ja`

### セルフサインアップの無効化

このサンプルはデフォルトでセルフサインアップが有効になっています。セルフサインアップを無効にするには、[cdk.json](./cdk/cdk.json)を開き、`selfSignUpEnabled`を`false`に切り替えてください。[外部IDプロバイダー](#external-identity-provider)を設定する場合、この値は無視され自動的に無効化されます。

### サインアップメールアドレスのドメイン制限

デフォルトでは、このサンプルはサインアップメールアドレスのドメインを制限しません。特定のドメインからのサインアップのみを許可するには、`cdk.json`を開き、`allowedSignUpEmailDomains`にドメインのリストを指定してください。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部IDプロバイダー

このサンプルは外部IDプロバイダーをサポートしています。現在、[Google](./idp/SET_UP_GOOGLE_ja-JP.md)と[カスタムOIDCプロバイダー](./idp/SET_UP_CUSTOM_OIDC_ja-JP.md)をサポートしています。

### オプションのフロントエンドWAF

CloudFrontディストリビューションの場合、AWS WAF WebACLはus-east-1リージョンで作成する必要があります。一部の組織では、ポリシーによってプライマリリージョン以外でのリソース作成が制限されています。このような環境では、us-east-1でフロントエンドWAFをプロビジョニングしようとするとCDKデプロイメントが失敗する可能性があります。

これらの制限に対応するため、フロントエンドWAFスタックはオプションとなっています。無効化すると、CloudFrontディストリビューションはWebACLなしでデプロイされます。これは、フロントエンドエッジでIPの許可/拒否制御が行えないことを意味します。認証やその他のアプリケーション制御は通常通り機能し続けます。この設定はフロントエンドWAF（CloudFrontスコープ）のみに影響し、公開APIのWAF（リージョナル）には影響しません。

フロントエンドWAFを無効にするには、`parameter.ts`で以下のように設定します（推奨される型安全な方法）：

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

または、従来の`cdk/cdk.json`を使用する場合は以下のように設定します：

```json
"enableFrontendWaf": false
```

### 新規ユーザーを自動的にグループに追加

このサンプルには、ユーザーに権限を付与するための以下のグループがあります：

- [`Admin`](./ADMINISTRATOR_ja-JP.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_ja-JP.md)

新規作成されたユーザーを自動的にグループに参加させたい場合は、[cdk.json](./cdk/cdk.json)で指定できます。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

デフォルトでは、新規作成されたユーザーは`CreatingBotAllowed`グループに参加します。

### RAGレプリカの設定

`enableRagReplicas`は[cdk.json](./cdk/cdk.json)のオプションで、Amazon OpenSearch Serverlessを使用するナレッジベースのRAGデータベースのレプリカ設定を制御します。

- **デフォルト**: true
- **true**: 追加のレプリカを有効にして可用性を向上させます。本番環境に適していますがコストが増加します。
- **false**: レプリカを減らしてコストを削減します。開発およびテスト環境に適しています。

これはアカウント/リージョンレベルの設定で、個々のボットではなくアプリケーション全体に影響します。

> [!Note]
> 2024年6月現在、Amazon OpenSearch Serverlessは0.5 OCUをサポートし、小規模なワークロードの初期コストを低減しています。本番デプロイメントは2 OCUから開始でき、開発/テストワークロードは1 OCUを使用できます。OpenSearch Serverlessはワークロードの需要に基づいて自動的にスケーリングします。詳細については、[発表](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)をご覧ください。

### ボットストアの設定

ボットストア機能により、ユーザーはカスタムボットを共有および発見できます。[cdk.json](./cdk/cdk.json)で以下の設定を通じてボットストアを設定できます：

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: ボットストア機能を有効にするかどうかを制御します（デフォルト：`true`）
- **botStoreLanguage**: ボットの検索と発見のための主要言語を設定します（デフォルト：`"en"`）。これはボットのインデックス作成と検索方法に影響し、指定された言語のテキスト分析を最適化します。
- **enableBotStoreReplicas**: ボットストアが使用するOpenSearch Serverlessコレクションのスタンバイレプリカを有効にするかどうかを制御します（デフォルト：`false`）。`true`に設定すると可用性が向上しますがコストが増加し、`false`に設定するとコストは削減されますが可用性に影響する可能性があります。
  > **重要**: コレクション作成後にこのプロパティを更新することはできません。このプロパティを変更しようとしても、コレクションは元の値を使用し続けます。

### クロスリージョンおよびグローバル推論

[クロスリージョンおよびグローバル推論](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)により、Amazon Bedrockはピーク需要時のスループットと回復力を向上させるため、複数のAWSリージョン間でモデル推論リクエストを動的にルーティングできます。グローバル推論は世界中のどこでも、レイテンシーと可用性に基づいて最適なリージョンにリクエストをルーティングし、クロスリージョン推論は同じAWSリージョン内（例：US内）でリクエストをルーティングします。一部のSCPはいずれかまたは両方を制限する可能性があるため、これらは個別に設定できます。デフォルトでは両方とも有効になっています。

設定を変更するには、`cdk.json`または`parameters.ts`で以下の設定を変更してください：

```json
"enableBedrockGlobalInference": false,
"enableBedrockCrossRegionInference": false,
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)はLambda関数のコールドスタート時間を改善し、より良いユーザーエクスペリエンスのために応答時間を高速化します。一方、Python関数の場合、[キャッシュサイズに応じた課金](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)があり、現在[一部のリージョンでは利用できません](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)。SnapStartを無効にするには、`cdk.json`を編集してください。

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
- `hostedZoneId`: ドメインレコードを作成するRoute 53ホストゾーンのID

これらのパラメータが提供されると、デプロイメントは自動的に以下を実行します：

- us-east-1リージョンでDNS検証付きのACM証明書を作成
- Route 53ホストゾーンに必要なDNSレコードを作成
- CloudFrontにカスタムドメインを設定

> [!Note]
> ドメインはAWSアカウントのRoute 53で管理されている必要があります。ホストゾーンIDはRoute 53コンソールで確認できます。

### 許可国の設定（地理的制限）

クライアントがアクセスする国に基づいてBedrock-Chatへのアクセスを制限できます。
[cdk.json](./cdk/cdk.json)の`allowedCountries`パラメータを使用し、[ISO-3166国コード](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)のリストを指定します。
例えば、ニュージーランドを拠点とする企業が、ニュージーランド（NZ）とオーストラリア（AU）からのIPアドレスのみにアクセスを許可し、他のすべてのアクセスを拒否する場合、[cdk.json](./cdk/cdk.json)で以下のように設定します：

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

または、`parameter.ts`を使用する場合（推奨される型安全な方法）：

```ts
// デフォルト環境のパラメータを定義
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### IPv6サポートの無効化

フロントエンドはデフォルトでIPとIPv6アドレスの両方を取得します。まれに、
IPv6サポートを明示的に無効にする必要がある場合があります。これを行うには、
[parameter.ts](./cdk/parameter.ts)または同様に[cdk.json](./cdk/cdk.json)で以下のパラメータを設定します：

```ts
"enableFrontendIpv6": false
```

設定されていない場合、IPv6サポートはデフォルトで有効になります。

### ローカル開発

[LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_ja-JP.md)をご覧ください。

### コントリビューション

このリポジトリへのコントリビューションをご検討いただき、ありがとうございます！バグ修正、言語翻訳（i18n）、機能強化、[エージェントツール](./docs/AGENT.md#how-to-develop-your-own-tools)、その他の改善を歓迎します。

機能強化やその他の改善については、**プルリクエストを作成する前に、実装アプローチと詳細について議論するために機能リクエストのイシューを作成していただけると大変ありがたいです。バグ修正と言語翻訳（i18n）については、直接プルリクエストを作成してください。**

コントリビューションの前に、以下のガイドラインもご確認ください：

- [ローカル開発](./LOCAL_DEVELOPMENT_ja-JP.md)
- [CONTRIBUTING](./CONTRIBUTING_ja-JP.md)

## 連絡先

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 主要な貢献者

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## 貢献者

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## ライセンス

このライブラリは MIT-0 ライセンスの下で提供されています。[ライセンスファイル](./LICENSE)をご参照ください。