# Bedrock Claude チャット (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_pl-PL.md)

> [!Warning]
>
> **V2がリリースされました。更新する際は、[移行ガイド](./migration/V1_TO_V2_ja-JP.md)を慎重に確認してください。注意せずに更新すると、**V1のBOTが使用できなくなります。**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)で提供されるLLMモデルを使用した多言語チャットボット。

### YouTubeで概要とインストール方法を視聴

[![概要](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](./imgs/demo.gif)

### ボットのカスタマイズ

独自の指示を追加し、URLやファイルで外部知識を提供できます（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。ボットはアプリケーションユーザー間で共有できます。カスタマイズしたボットはスタンドアロンAPIとして公開することもできます（[詳細](./PUBLISH_API_ja-JP.md)参照）。

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由から、許可されたユーザーのみがカスタマイズしたボットを作成できます。カスタマイズボットの作成を許可するには、ユーザーは`CreatingBotAllowed`グループのメンバーである必要があります。これは管理コンソール > Amazon Cognito ユーザープールまたはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできます。

### 管理者ダッシュボード

<details>
<summary>管理者ダッシュボード</summary>

管理者ダッシュボードで、ユーザーごと/ボットごとの使用状況を分析できます。[詳細](./ADMINISTRATOR_ja-JP.md)

![](./imgs/admin_bot_analytics.png)

</details>

### LLMを活用したエージェント

<details>
<summary>LLMを活用したエージェント</summary>

[エージェント機能](./AGENT_ja-JP.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、エージェントは外部ツールから必要な情報を取得したり、タスクを複数のステップに分解して処理したりできます。

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超簡単デプロイ

- us-east-1リージョンで、[Bedrockモデルアクセス](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)を開き > `モデルアクセスの管理` > `Anthropic / Claude 3`のすべて、`Amazon / Nova`、`Amazon / Titan Text Embeddings V2`、`Cohere / Embed Multilingual`をすべてチェックし、`変更を保存`をクリックします。

<details>
<summary>スクリーンショット</summary>

![](./imgs/model_screenshot.png)

</details>

- デプロイしたいリージョンの[CloudShell](https://console.aws.amazon.com/cloudshell/home)を開きます
- 以下のコマンドでデプロイを実行します。特定のバージョンをデプロイしたい場合やセキュリティポリシーを適用する必要がある場合は、[オプションパラメータ](#オプションパラメータ)から適切なパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーかv2を使用するかを尋ねられます。v0からの継続ユーザーでない場合は、`y`を入力してください。

### オプションパラメータ

デプロイ時に以下のパラメータを指定して、セキュリティとカスタマイズを強化できます：

- **--disable-self-register**: 自己登録を無効化（デフォルト：有効）。このフラグを設定すると、Cognitoですべてのユーザーを作成する必要があり、ユーザーが自分でアカウントを登録できなくなります。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)を有効化（デフォルト：無効）。このフラグを設定すると、Lambdaファンクションのコールドスタート時間が改善され、ユーザーエクスペリエンスが向上します。
- **--ipv4-ranges**: 許可されるIPv4範囲のカンマ区切りリスト。（デフォルト：すべてのIPv4アドレスを許可）
- **--ipv6-ranges**: 許可されるIPv6範囲のカンマ区切りリスト。（デフォルト：すべてのIPv6アドレスを許可）
- **--disable-ipv6**: IPv6接続を無効化。（デフォルト：有効）
- **--allowed-signup-email-domains**: サインアップ時に許可されるメールドメインのカンマ区切りリスト。（デフォルト：ドメイン制限なし）
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

上書きJSONは、cdk.jsonと同じ構造に従う必要があります。以下のようなコンテキスト値を上書きできます：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- cdk.jsonで定義されている他のコンテキスト値

> [!メモ]
> 上書き値は、AWS CodeBuildでのデプロイ時に既存のcdk.json設定とマージされます。指定された上書き値は、cdk.jsonの値よりも優先されます。

#### パラメータを含むコマンド例：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 約35分後、以下の出力が表示され、ブラウザからアクセスできます

```
フロントエンドURL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

上記のようにサインアップ画面が表示され、メールアドレスを登録してログインできます。

> [!重要]
> オプションパラメータを設定しない場合、URLを知っている人は誰でもサインアップできます。本番環境では、IPアドレス制限を追加し、自己サインアップを無効化することを強くお勧めします（allowed-signup-email-domainsを定義して、会社のドメインのメールアドレスのみがサインアップできるように制限できます）。./binを実行する際に、ipv4-rangesとipv6-rangesでIPアドレス制限を行い、disable-self-registerを使用して自己サインアップを無効化してください。

> [!ヒント]
> `フロントエンドURL`が表示されないか、Bedrock Claude Chatが正常に動作しない場合、最新バージョンに問題がある可能性があります。その場合は、`--version "v1.2.6"`をパラメータに追加してデプロイを再試行してください。

## アーキテクチャ

AWS管理サービスに基づいて構築されたアーキテクチャで、インフラストラクチャ管理の必要性を排除しています。Amazon Bedrockを利用することで、AWS外のAPIと通信する必要がありません。これにより、スケーラブルで信頼性が高く、セキュアなアプリケーションを展開できます。

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)：会話履歴を保存するためのNoSQLデータベース
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/)：バックエンドAPIエンドポイント（[AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)、[FastAPI](https://fastapi.tiangolo.com/)）
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/)：フロントエンドアプリケーションの配信（[React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)）
- [AWS WAF](https://aws.amazon.com/waf/)：IPアドレス制限
- [Amazon Cognito](https://aws.amazon.com/cognito/)：ユーザー認証
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)：APIを介して基盤モデルを利用する管理サービス
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)：検索拡張生成（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）のための管理インターフェースを提供し、ドキュメントの埋め込みと解析サービスを提供
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/)：DynamoDBストリームからイベントを受信し、外部知識を埋め込むStep Functionsを起動
- [AWS Step Functions](https://aws.amazon.com/step-functions/)：外部知識をBedrock Knowledge Basesに埋め込むための取り込みパイプラインのオーケストレーション
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)：Bedrock Knowledge Basesのバックエンドデータベースとして機能し、全文検索とベクター検索機能を提供し、関連情報の正確な検索を可能にする
- [Amazon Athena](https://aws.amazon.com/athena/)：S3バケットを分析するためのクエリサービス

![](./imgs/arch.png)

## CDKを使用したデプロイ

超簡単なデプロイは、[AWS CodeBuild](https://aws.amazon.com/codebuild/)を使用して、内部的にCDKによるデプロイを実行します。このセクションでは、CDKを直接使用してデプロイする手順を説明します。

- UNIX、Docker、Node.jsランタイム環境が必要です。ない場合は、[Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)を使用することもできます。

> [!Important]
> デプロイ中にローカル環境のストレージ容量が不足している場合、CDKブートストラップでエラーが発生する可能性があります。Cloud9などで実行している場合は、デプロイ前にインスタンスのボリュームサイズを拡張することをお勧めします。

- リポジトリをクローンします

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- npmパッケージをインストールします

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- 必要に応じて、[cdk.json](./cdk/cdk.json)の以下のエントリを編集します。

  - `bedrockRegion`: Bedrockが利用可能なリージョン。**注意：現時点でBedrockはすべてのリージョンをサポートしているわけではありません。**
  - `allowedIpV4AddressRanges`、`allowedIpV6AddressRanges`：許可されるIPアドレス範囲。
  - `enableLambdaSnapStart`：デフォルトはtrueです。[Lambda SnapStartがPython関数をサポートしていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)にデプロイする場合はfalseに設定します。

- CDKをデプロイする前に、デプロイするリージョンに対して一度ブートストラップを実行する必要があります。

```
npx cdk bootstrap
```

- このサンプルプロジェクトをデプロイします

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

### パラメータの定義

デプロイのパラメータは、`cdk.json`を使用するか、型安全な`parameter.ts`ファイルを使用して定義できます。

#### cdk.json を使用する（従来の方法）

パラメータを構成する従来の方法は、`cdk.json`ファイルを編集することです。このアプローチは簡単ですが、型チェックがありません：

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "enableMistral": false,
    "selfSignUpEnabled": true
  }
}
```

#### parameter.ts を使用する（推奨される型安全な方法）

より優れた型安全性と開発者エクスペリエンスを得るために、`parameter.ts`ファイルを使用してパラメータを定義できます：

```typescript
// デフォルト環境のパラメータを定義
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  enableMistral: false,
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
> 既存のユーザーは、変更なしで`cdk.json`を引き続き使用できます。`parameter.ts`アプローチは、新規デプロイや複数の環境を管理する必要がある場合に推奨されます。

### 複数の環境のデプロイ

`parameter.ts`ファイルと`-c envName`オプションを使用して、同じコードベースから複数の環境をデプロイできます。

#### 前提条件

1. 上記のように`parameter.ts`に環境を定義します
2. 各環境は環境固有のプレフィックスを持つ独自のリソースセットを持ちます

#### デプロイコマンド

特定の環境をデプロイするには：

```bash
# dev環境をデプロイ
npx cdk deploy --all -c envName=dev

# prod環境をデプロイ
npx cdk deploy --all -c envName=prod
```

環境が指定されない場合、「default」環境が使用されます：

```bash
# デフォルト環境をデプロイ
npx cdk deploy --all
```

#### 重要な注意点

1. **スタックの命名**:

   - 各環境のメインスタックは環境名のプレフィックスが付きます（例：`dev-BedrockChatStack`、`prod-BedrockChatStack`）
   - ただし、カスタムボットスタック（`BrChatKbStack*`）とAPI公開スタック（`ApiPublishmentStack*`）は、実行時に動的に作成されるため、環境プレフィックスは付きません

2. **リソースの命名**:

   - 一部のリソースのみが環境プレフィックスを名前に持ちます（例：`dev_ddb_export`テーブル、`dev-FrontendWebAcl`）
   - ほとんどのリソースは元の名前を維持しますが、異なるスタックに分離されます

3. **環境の識別**:

   - すべてのリソースには、環境名を含む`CDKEnvironment`タグが付けられます
   - このタグを使用して、リソースがどの環境に属するかを識別できます
   - 例：`CDKEnvironment: dev`または`CDKEnvironment: prod`

4. **デフォルト環境の上書き**: `parameter.ts`で「default」環境を定義すると、`cdk.json`の設定が上書きされます。`cdk.json`を引き続き使用するには、`parameter.ts`に「default」環境を定義しないでください。

5. **環境の要件**: 「default」以外の環境を作成するには、`parameter.ts`を使用する必要があります。`-c envName`オプションだけでは不十分です。

6. **リソースの分離**: 各環境は独自のリソースセットを作成するため、同じAWSアカウント内に開発、テスト、本番環境を持つことができ、競合を回避できます。

## その他

### Mistralモデルのサポートを設定

[cdk.json](./cdk/cdk.json)の`enableMistral`を`true`に更新し、`npx cdk deploy`を実行します。

```json
...
  "enableMistral": true,
```

> [!Important]
> このプロジェクトはAnthropicのClaudeモデルに焦点を当てており、Mistralモデルは限定的にサポートされています。例えば、プロンプトの例はClaudeモデルに基づいています。これはMistral専用のオプションであり、一度Mistralモデルを有効にすると、チャット機能にはMistralモデルのみを使用でき、ClaudeとMistralの両方のモデルは使用できません。

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

このアセットは[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)を使用して自動的に言語を検出します。アプリケーションメニューから言語を切り替えることができます。または、以下のようにクエリ文字列を使用して言語を設定することもできます。

> `https://example.com?lng=ja`

### セルフサインアップを無効にする

このサンプルはデフォルトでセルフサインアップが有効になっています。セルフサインアップを無効にするには、[cdk.json](./cdk/cdk.json)を開き、`selfSignUpEnabled`を`false`に切り替えます。[外部IDプロバイダ](#外部idプロバイダ)を設定した場合、この値は無視され、自動的に無効になります。

### サインアップ可能なメールアドレスのドメインを制限

デフォルトでは、このサンプルはサインアップ可能なメールアドレスのドメインを制限していません。特定のドメインからのみサインアップを許可するには、`cdk.json`を開き、`allowedSignUpEmailDomains`にドメインをリストとして指定します。

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

（以下、同様に翻訳を続けます）

## 連絡先

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 主要貢献者

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## 貢献者

[![bedrock claude chat 貢献者](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## ライセンス

このライブラリは MIT-0 ライセンスの下でライセンス供与されています。[ライセンスファイル](./LICENSE)を参照してください。