<h1 align="center">Bedrock チャット (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md)

[Amazon Bedrock](https://aws.amazon.com/bedrock/)を活用した多言語対応の生成型AIプラットフォーム。
チャット、ナレッジベースのカスタムボット（RAG）、ボットストアでのボット共有、エージェントによるタスク自動化をサポートしています。

![](./imgs/demo.gif)

> [!Warning]
>
> **V3がリリースされました。更新する際は、[移行ガイド](./migration/V2_TO_V3_ja-JP.md)を慎重に確認してください。** 注意せずに更新すると、**V2のボットが使用できなくなります。**

### ボットのパーソナライズ / ボットストア

独自の指示とナレッジ（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）を追加できます。ボットはボットストアマーケットプレイスでアプリケーションユーザー間で共有可能です。カスタマイズされたボットはスタンドアロンAPIとして公開することもできます（[詳細](./PUBLISH_API_ja-JP.md)参照）。

<details>
<summary>スクリーンショット</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

既存の[Amazon BedrockのナレッジベースBase](https://aws.amazon.com/bedrock/knowledge-bases/)もインポート可能です。

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> ガバナンス上の理由により、許可されたユーザーのみがカスタマイズされたボットを作成できます。カスタマイズされたボットの作成を許可するには、ユーザーが`CreatingBotAllowed`グループのメンバーである必要があります。これは管理コンソール > Amazon Cognito ユーザープール、またはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできます。

### 管理機能

APIの管理、重要なボットのマーク、ボットの利用状況分析。[詳細](./ADMINISTRATOR_ja-JP.md)

<details>
<summary>スクリーンショット</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### エージェント

[エージェント機能](./AGENT_ja-JP.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、エージェントは外部ツールから必要な情報を取得したり、タスクを複数のステップに分解して処理したりできます。

<details>
<summary>スクリーンショット</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超簡単デプロイ

- us-east-1リージョンで、[Bedrock モデルアクセス](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)を開き > `モデルアクセスの管理` > 使用したいモデルをすべてチェックし、`変更を保存`します。

<details>
<summary>スクリーンショット</summary>

![](./imgs/model_screenshot.png)

</details>

- デプロイしたいリージョンで[CloudShell](https://console.aws.amazon.com/cloudshell/home)を開きます
- 以下のコマンドでデプロイを実行します。特定のバージョンをデプロイしたい場合やセキュリティポリシーを適用する必要がある場合は、[オプションパラメータ](#オプションパラメータ)から適切なパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーか v3 を使用するかを尋ねられます。v0からの継続ユーザーでない場合は、`y` を入力してください。

### オプションパラメータ

デプロイ時に以下のパラメータを指定して、セキュリティとカスタマイズを強化できます：

- **--disable-self-register**: 自己登録を無効にします（デフォルト：有効）。このフラグが設定されている場合、Cognitoですべてのユーザーを作成する必要があり、ユーザーが自分でアカウントを登録することはできません。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)を有効にします（デフォルト：無効）。このフラグが設定されている場合、Lambdaファンクションのコールドスタート時間を改善し、より高速な応答時間を提供します。
- **--ipv4-ranges**: 許可されたIPv4範囲のカンマ区切りリスト。（デフォルト：すべてのIPv4アドレスを許可）
- **--ipv6-ranges**: 許可されたIPv6範囲のカンマ区切りリスト。（デフォルト：すべてのIPv6アドレスを許可）
- **--disable-ipv6**: IPv6経由の接続を無効にします。（デフォルト：有効）
- **--allowed-signup-email-domains**: サインアップに許可されたメールドメインのカンマ区切りリスト。（デフォルト：ドメイン制限なし）
- **--bedrock-region**: Bedrockが利用可能なリージョンを定義します。（デフォルト：us-east-1）
- **--repo-url**: フォークまたはカスタムソース管理の場合のBedrock Chatのカスタムリポジトリ。（デフォルト：https://github.com/aws-samples/bedrock-chat.git）
- **--version**: デプロイするBedrock Chatのバージョン。（デフォルト：開発中の最新バージョン）
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

> [!メモ]
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

上記のように、サインアップ画面が表示され、メールアドレスを登録してログインできます。

> [!重要]
> オプションパラメータを設定しない場合、URLを知っている人は誰でもサインアップできます。本番環境では、セキュリティリスクを軽減するために、IPアドレス制限と自己サインアップの無効化を強くお勧めします（allowed-signup-email-domainsを定義して、会社のドメインのメールアドレスのみがサインアップできるように制限できます）。./binを実行する際に、ipv4-rangesとipv6-rangesでIPアドレス制限を行い、disable-self-registerを使用して自己サインアップを無効にしてください。

> [!ヒント]
> `Frontend URL`が表示されないか、Bedrock Chatが正常に動作しない場合、最新バージョンに問題がある可能性があります。その場合、パラメータに `--version "v3.0.0"` を追加して、デプロイを再試行してください。

## アーキテクチャ

AWS管理サービスに基づいて構築されたアーキテクチャであり、インフラストラクチャ管理の必要性を排除しています。Amazon Bedrockを利用することで、AWS外のAPIと通信する必要がありません。これにより、スケーラブルで信頼性が高く、セキュアなアプリケーションをデプロイできます。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：会話履歴を保存するためのNoSQLデータベース
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：バックエンドAPIエンドポイント（[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)、[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：フロントエンドアプリケーションの配信（[React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/)：IPアドレス制限
- [Amazon Cognito](https://aws.amazon.com/cognito/)：ユーザー認証
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：APIを介して基盤モデルを利用する管理サービス
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)：検索拡張生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）のための管理インターフェースを提供し、ドキュメントの埋め込みと解析サービスを提供
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：DynamoDBストリームからイベントを受信し、外部知識を埋め込むStep Functionsを起動
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：Bedrock Knowledge Basesに外部知識を埋め込むための取り込みパイプラインのオーケストレーション
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：Bedrock Knowledge Basesのバックエンドデータベースとして機能し、全文検索とベクター検索機能を提供し、関連情報の正確な検索を可能にする
- [Amazon Athena](https://aws.amazon.com/athena/)：S3バケットを分析するためのクエリサービス

![](./imgs/arch.png)

## AWS CDKを使用したデプロイ

簡単デプロイは、デプロイメントを内部的に実行するために[AWS CodeBuild](https://aws.amazon.com/codebuild/)を使用します。このセクションでは、CDKを使用して直接デプロイする手順について説明します。

- UNIX、Docker、Node.jsランタイム環境が必要です。ない場合は、[Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)を使用できます

> [!重要]
> デプロイ中にローカル環境のストレージ容量が不足している場合、CDKブートストラップでエラーが発生する可能性があります。Cloud9などで実行している場合は、デプロイ前にインスタンスのボリュームサイズを拡張することをお勧めします。

- リポジトリをクローンします

```
git clone https://github.com/aws-samples/bedrock-chat
```

- npmパッケージをインストールします

```
cd bedrock-chat
cd cdk
npm ci
```

- 必要に応じて、[cdk.json](./cdk/cdk.json)の以下のエントリを編集します。

  - `bedrockRegion`: Bedrockが利用可能なリージョン。**注意：現時点でBedrockはすべてのリージョンをサポートしているわけではありません。**
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`: 許可されたIPアドレス範囲。
  - `enableLambdaSnapStart`: デフォルトはtrueです。[Lambda SnapStartがPython関数でサポートされていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)にデプロイする場合はfalseに設定します。

- CDKをデプロイする前に、デプロイするリージョンでブートストラップを1回実行する必要があります。

```
npx cdk bootstrap
```

- このサンプルプロジェクトをデプロイします

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

### パラメータの定義

デプロイのパラメータは、`cdk.json`を使用するか、型安全な`parameter.ts`ファイルを使用して定義できます。

#### cdk.json（従来の方法）の使用

パラメータを構成する従来の方法は、`cdk.json`ファイルを編集することです。このアプローチは簡単ですが、型チェックがありません：

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

#### parameter.ts（推奨される型安全な方法）の使用

より優れた型安全性と開発者エクスペリエンスを得るには、`parameter.ts`ファイルを使用してパラメータを定義できます：

```typescript
// デフォルト環境のパラメータを定義
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// 追加の環境のパラメータを定義
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 開発環境でのコスト削減
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 本番環境での可用性向上
});
```

> [!メモ]
> 既存のユーザーは、変更なしで`cdk.json`を引き続き使用できます。`parameter.ts`アプローチは、新規デプロイや複数の環境を管理する必要がある場合に推奨されます。

### 複数の環境へのデプロイ

`parameter.ts`ファイルと`-c envName`オプションを使用して、同じコードベースから複数の環境にデプロイできます。

#### 前提条件

1. 上記のように`parameter.ts`に環境を定義します
2. 各環境は環境固有の接頭辞を持つ独自のリソースセットを持ちます

#### デプロイコマンド

特定の環境にデプロイするには：

```bash
# 開発環境にデプロイ
npx cdk deploy --all -c envName=dev

# 本番環境にデプロイ
npx cdk deploy --all -c envName=prod
```

環境が指定されていない場合、「default」環境が使用されます：

```bash
# デフォルト環境にデプロイ
npx cdk deploy --all
```

#### 重要な注意点

1. **スタックの命名**:
   - 各環境のメインスタックは環境名が接頭辞として付けられます（例：`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - ただし、カスタムボットスタック（`BrChatKbStack*`）とAPI公開スタック（`ApiPublishmentStack*`）は、実行時に動的に作成されるため、環境接頭辞は付きません

2. **リソースの命名**:
   - 一部のリソースのみが環境接頭辞を名前に持ちます（例：`dev_ddb_export`テーブル、`dev-FrontendWebAcl`）
   - ほとんどのリソースは元の名前を維持しますが、異なるスタックに分離されます

3. **環境の識別**:
   - すべてのリソースには環境名を含む`CDKEnvironment`タグが付けられます
   - このタグを使用して、リソースがどの環境に属するかを識別できます
   - 例：`CDKEnvironment: dev`または`CDKEnvironment: prod`

4. **デフォルト環境の上書き**: `parameter.ts`で「default」環境を定義すると、`cdk.json`の設定が上書きされます。`cdk.json`を引き続き使用するには、`parameter.ts`に「default」環境を定義しないでください。

5. **環境の要件**: 「default」以外の環境を作成するには、`parameter.ts`を使用する必要があります。`-c envName`オプションだけでは不十分です。

6. **リソースの分離**: 各環境は独自のリソースセットを作成するため、同じAWSアカウント内で開発、テスト、本番環境を競合なく持つことができます。

## その他

デプロイメントのパラメータを定義する方法は2つあります：`cdk.json`を使用する方法と、型安全な`parameter.ts`ファイルを使用する方法です。

#### cdk.jsonを使用する（従来の方法）

パラメータを構成する従来の方法は、`cdk.json`ファイルを編集することです。このアプローチは簡単ですが、型チェックがありません：

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

#### parameter.tsを使用する（推奨される型安全な方法）

より優れた型安全性と開発者体験のために、`parameter.ts`ファイルを使用してパラメータを定義できます：

```typescript
// デフォルト環境のパラメータを定義
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// 追加の環境のパラメータを定義
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 開発環境でのコスト削減
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 本番環境での可用性向上
});
```

> [!Note]
> 既存のユーザーは変更なしで`cdk.json`を引き続き使用できます。`parameter.ts`のアプローチは、新規デプロイメントまたは複数の環境を管理する必要がある場合に推奨されます。

### 複数の環境のデプロイ

`parameter.ts`ファイルと`-c envName`オプションを使用して、同じコードベースから複数の環境をデプロイできます。

#### 前提条件

1. 上記のように`parameter.ts`に環境を定義する
2. 各環境は環境固有の接頭辞を持つ独自のリソースセットを持ちます

#### デプロイコマンド

特定の環境をデプロイするには：

```bash
# 開発環境をデプロイ
npx cdk deploy --all -c envName=dev

# 本番環境をデプロイ
npx cdk deploy --all -c envName=prod
```

環境が指定されない場合、「default」環境が使用されます：

```bash
# デフォルト環境をデプロイ
npx cdk deploy --all
```

#### 重要な注意点

1. **スタックの命名**：

   - 各環境のメインスタックは環境名の接頭辞が付けられます（例：`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - ただし、カスタムボットスタック（`BrChatKbStack*`）とAPIパブリッシュスタック（`ApiPublishmentStack*`）は、実行時に動的に作成されるため、環境接頭辞は付けられません

2. **リソースの命名**：

   - 一部のリソースのみが名前に環境接頭辞を持ちます（例：`dev_ddb_export`テーブル、`dev-FrontendWebAcl`）
   - ほとんどのリソースは元の名前を維持しますが、異なるスタックに分離されます

3. **環境の識別**：

   - すべてのリソースには、環境名を含む`CDKEnvironment`タグが付けられます
   - このタグを使用して、リソースがどの環境に属しているかを識別できます
   - 例：`CDKEnvironment: dev`または`CDKEnvironment: prod`

4. **デフォルト環境の上書き**：`parameter.ts`で「default」環境を定義すると、`cdk.json`の設定が上書きされます。`cdk.json`を引き続き使用するには、`parameter.ts`に「default」環境を定義しないでください。

5. **環境の要件**：「default」以外の環境を作成するには、`parameter.ts`を使用する必要があります。`-c envName`オプションだけでは不十分です。

6. **リソースの分離**：各環境は独自のリソースセットを作成するため、同じAWSアカウント内で開発、テスト、本番環境を競合なく設定できます。

## その他

### リソースの削除

CLIとCDKを使用している場合は、`npx cdk destroy`を実行してください。そうでない場合は、[CloudFormation](https://console.aws.amazon.com/cloudformation/home)にアクセスし、`BedrockChatStack`と`FrontendWafStack`を手動で削除してください。`FrontendWafStack`は`us-east-1`リージョンにあることに注意してください。

### 言語設定

このアセットは、[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)を使用して自動的に言語を検出します。アプリケーションメニューから言語を切り替えることができます。または、以下に示すようにクエリ文字列を使用して言語を設定することもできます。

> `https://example.com?lng=ja`

### セルフサインアップの無効化

このサンプルはデフォルトでセルフサインアップが有効になっています。セルフサインアップを無効にするには、[cdk.json](./cdk/cdk.json)を開き、`selfSignUpEnabled`を`false`に切り替えてください。[外部IDプロバイダ](#外部idプロバイダ)を設定した場合、この値は無視され、自動的に無効になります。

### サインアップ可能なメールアドレスのドメイン制限

デフォルトでは、このサンプルはサインアップ可能なメールアドレスのドメインを制限しません。特定のドメインからのみサインアップを許可するには、`cdk.json`を開き、`allowedSignUpEmailDomains`にドメインをリストとして指定してください。

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 外部IDプロバイダ

このサンプルは外部IDプロバイダをサポートしています。現在、[Google](./idp/SET_UP_GOOGLE_ja-JP.md)と[カスタムOIDCプロバイダ](./idp/SET_UP_CUSTOM_OIDC_ja-JP.md)をサポートしています。

### 新規ユーザーを自動的にグループに追加

このサンプルには、ユーザーに権限を与えるために以下のグループがあります：

- [`Admin`](./ADMINISTRATOR_ja-JP.md)
- [`CreatingBotAllowed`](#ボットのパーソナライズ)
- [`PublishAllowed`](./PUBLISH_API_ja-JP.md)

新規作成されたユーザーを自動的にグループに参加させたい場合は、[cdk.json](./cdk/cdk.json)で指定できます。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

デフォルトでは、新規作成されたユーザーは`CreatingBotAllowed`グループに参加します。

### RAGレプリカの設定

`enableRagReplicas`は[cdk.json](./cdk/cdk.json)のオプションで、Amazon OpenSearch Serverlessを使用するナレッジベースのレプリカ設定を制御します。これはボットストアデータベースにも影響します。

- **デフォルト**: true
- **true**: 追加のレプリカを有効にし、可用性を向上させ、本番環境に適していますが、コストが増加します。
- **false**: レプリカを減らしてコストを削減し、開発とテストに適しています。

これはアカウント/リージョンレベルの設定で、アプリケーション全体に影響を与えます。

> [!Note]
> 2024年6月現在、Amazon OpenSearch Serverlessは0.5 OCUをサポートし、小規模ワークロードのエントリコストを下げています。本番環境では2 OCU、開発/テスト環境では1 OCUから始めることができます。OpenSearch Serverlessはワークロードの需要に基づいて自動的にスケーリングします。詳細は[アナウンス](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)をご覧ください。

### ボットストアの設定

ボットストア機能により、ユーザーはカスタムボットを共有および発見できます。[cdk.json](./cdk/cdk.json)の以下の設定を通じてボットストアを設定できます：

```json
{
  "context": {
    "enableBotStore": true,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: ボットストア機能を有効にするかどうかを制御します（デフォルト: `true`）
- **botStoreLanguage**: ボットの検索と発見のプライマリ言語を設定します（デフォルト: `"en"`）。これはボットがボットストアでインデックス付けおよび検索される方法に影響し、指定された言語のテキスト分析を最適化します。
- **enableRagReplicas**: この設定（前のセクションで言及）はボットストアのOpenSearchデータベースにも適用されます。`true`に設定すると可用性が向上しますが、コストが増加します。`false`に設定するとコストが削減されますが、可用性に影響を与える可能性があります。

### クロスリージョン推論

[クロスリージョン推論](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)により、Amazon Bedrockは複数のAWSリージョン間でモデル推論リクエストを動的にルーティングし、ピーク需要期間中のスループットと回復力を向上させます。設定するには、`cdk.json`を編集してください。

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)は、Lambdaファンクションのコールドスタート時間を改善し、より良いユーザーエクスペリエンスのために高速な応答時間を提供します。一方、Pythonファンクションの場合、[キャッシュサイズに応じて課金](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)があり、[現在一部のリージョンでは利用できません](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)。SnapStartを無効にするには、`cdk.json`を編集してください。

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
- `hostedZoneId`: ドメインレコードが作成されるRoute 53ホストゾーンのID

これらのパラメータが提供されると、デプロイメントは自動的に以下を行います：

- us-east-1リージョンでDNS検証を使用したACM証明書を作成
- Route 53ホストゾーンに必要なDNSレコードを作成
- CloudFrontをカスタムドメインを使用するように設定

> [!Note]
> ドメインはAWSアカウントのRoute 53で管理されている必要があります。ホストゾーンIDはRoute 53コンソールで確認できます。

### ローカル開発

[ローカル開発](./LOCAL_DEVELOPMENT_ja-JP.md)を参照してください。

### 貢献

このリポジトリへの貢献を検討していただき、ありがとうございます！バグ修正、言語翻訳（i18n）、機能拡張、[エージェントツール](./docs/AGENT.md#独自のツールを開発する方法)、その他の改善を歓迎します。

機能拡張やその他の改善については、**プルリクエストを作成する前に、実装アプローチと詳細について議論するために機能リクエストの課題を作成していただければ幸いです。バグ修正と言語翻訳（i18n）については、直接プルリクエストを作成してください。**

貢献する前に、以下のガイドラインもご確認ください：

- [ローカル開発](./LOCAL_DEVELOPMENT_ja-JP.md)
- [貢献](./CONTRIBUTING_ja-JP.md)

## 連絡先

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 主要貢献者

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## コントリビューター

[![bedrock chat コントリビューター](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## ライセンス

このライブラリは MIT-0 ライセンスの下でライセンスされています。[ライセンスファイル](./LICENSE) を参照してください。