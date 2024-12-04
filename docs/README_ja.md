# Bedrock Claude Chat (Nova)

> [!Warning]
> **V2 がリリースされました。** 更新する際は、[移行ガイド](./migration/V1_TO_V2.md)を必ずご確認ください。 **注意を払わずに進めると、V1 の BOT は使用できなくなります。**

このリポジトリは、生成系 AI を提供する[Amazon Bedrock](https://aws.amazon.com/jp/bedrock/)の基盤モデルの一つである、Anthropic 社製 LLM [Claude](https://www.anthropic.com/)を利用したチャットボットのサンプルです。

### 基本的な会話

![](./imgs/demo_ja.gif)

### ボットのカスタマイズ

外部のナレッジおよび具体的なインストラクションを組み合わせ、ボットをカスタマイズすることが可能です（外部のナレッジを利用した方法は[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)として知られています）。なお、作成したボットはアプリケーションのユーザー間で共有することができます。カスタマイズされたボットはスタンドアロンの API として公開できます (詳細は[こちら](./PUBLISH_API.md)をご覧ください)。

![](./imgs/bot_creation_ja.png)
![](./imgs/bot_chat_ja.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由により、許可されたユーザーのみがカスタマイズされたボットを作成できます。作成を許可するには、そのユーザーをマネジメントコンソール > Amazon Cognito ユーザープールまたは aws cli で `CreatingBotAllowed` というグループのメンバーにする必要があります。ユーザープール ID は CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` で確認できます。

### 管理者ダッシュボード

管理者ダッシュボードで各ユーザー/ボットの使用状況を分析できます。[詳細](./ADMINISTRATOR.md)

![](./imgs/admin_bot_analytics.png)

### エージェント

[エージェント機能](./AGENT.md)を使うと、チャットボットがより複雑なタスクを自動的に処理できるようになります。例えば、ユーザーの質問に答えるために、必要な情報を外部ツールから取得したり、複数のステップに分けて処理したりすることができます。
![](./imgs/agent1.png)

## 🚀 まずはお試し

- us-east-1 リージョンにて、[Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > すべての`Anthropic / Claude 3`、 すべての `Amazon / Nova`、`Cohere / Embed Multilingual`をチェックし、`Save changes`をクリックします

<details>
<summary>スクリーンショット</summary>

![](./imgs/model_screenshot.png)

</details>

- [CloudShell](https://console.aws.amazon.com/cloudshell/home)をデプロイしたいリージョン (ap-northeast-1 など) で開きます

- 下記のコマンドでデプロイを実行します。デプロイするバージョンを指定したい場合や、セキュリティポリシーを適用する必要がある場合は、[オプションのパラメータ](#オプションのパラメータ)から該当するものを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーまたは v2 ユーザーかどうかを聞かれます。v0 からの継続利用でない場合は `y` を入力してください。

### オプションのパラメータ

デプロイ時に以下のパラメータを指定することで、セキュリティとカスタマイズを強化できます。

- **--disable-self-register**: セルフ登録を無効にします（デフォルト: 有効）。このフラグを設定すると、Cognito 上で全てのユーザーを作成する必要があり、ユーザーが自分でアカウントを登録することはできなくなります。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) を有効化します (デフォルト: 無効)。 このフラグを設定すると、Lambda 関数のコールドスタート時間を短縮し、レスポンスタイムの改善によってユーザー体験を向上させます。
- **--ipv4-ranges**: 許可する IPv4 範囲のカンマ区切りリスト。（デフォルト: 全ての IPv4 アドレスを許可）
- **--ipv6-ranges**: 許可する IPv6 範囲のカンマ区切りリスト。（デフォルト: 全ての IPv6 アドレスを許可）
- **--disable-ipv6**: IPv6 での接続を無効にします (デフォルト: 有効)
- **--allowed-signup-email-domains**: サインアップ時に許可するメールドメインのカンマ区切りリスト。（デフォルト: ドメイン制限なし）
- **--bedrock-region**: Bedrock が利用可能なリージョンを指定します。（デフォルト: us-east-1）
- **--version**: デプロイする Bedrock Claude Chat のバージョン。 (デフォルト: 開発中の最新バージョン)

#### パラメータを指定したコマンド例:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "ap-northeast-1" --version "v1.2.6"
```

- 30 分ほど経過後、下記の出力が得られるのでブラウザからアクセスします

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

上記のようなサインアップ画面が現れますので、E メールを登録・ログインしご利用ください。

> [!Important]
> オプションのパラメータを設定しない場合、このデプロイ方法では URL を知っている誰でもサインアップできてしまいます。本番環境で使用する場合は、セキュリティリスクを軽減するために、IP アドレスの制限を追加し、セルフサインアップを無効にすることを強くお勧めします（`allowed-signup-email-domains` を定義して、会社のドメインからのメールアドレスのみがサインアップできるようにすることで、ユーザーを制限できます）。IP アドレスの制限には `ipv4-ranges` と `ipv6-ranges` の両方を使用し、`./bin` を実行する際に `disable-self-register` を使用してセルフサインアップを無効にしてください。

> [!TIP] > `Frontend URL` が正しく表示されない場合や、Bedrock Claude Chat が正常に動作しない場合は、最新バージョンの不具合である可能性がありますので、パラメータに `--version "v1.2.6"` を追加して再度デプロイを試してみてください。

## アーキテクチャ

AWS のマネージドサービスで構成した、インフラストラクチャ管理の不要なアーキテクチャとなっています。Amazon Bedrock の活用により、 AWS 外部の API と通信する必要がありません。スケーラブルで信頼性が高く、安全なアプリケーションをデプロイすることが可能です。

- [Amazon DynamoDB](https://aws.amazon.com/jp/dynamodb/): 会話履歴保存用の NoSQL データベース
- [Amazon API Gateway](https://aws.amazon.com/jp/api-gateway/) + [AWS Lambda](https://aws.amazon.com/jp/lambda/): バックエンド API エンドポイント ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/jp/cloudfront/) + [S3](https://aws.amazon.com/jp/s3/): フロントエンドアプリケーションの配信 ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/jp/waf/): IP アドレス制限
- [Amazon Cognito](https://aws.amazon.com/jp/cognito/): ユーザ認証
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): 基盤となるモデルを API 経由で利用できるマネージドサービス
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Retrieval-Augmented Generation (RAG)のためのマネージドなインターフェースを提供し、埋め込みやドキュメントのパース機能を提供
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): DynamoDB ストリームからのイベントを受け取り、Step Functions を起動して外部知識の埋め込みを行う
- [AWS Step Functions](https://aws.amazon.com/step-functions/): 外部知識を Bedrock Knowledge Bases に埋め込むためのパイプラインをオーケストレーション
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Bedrock Knowledge Bases のバックエンドデータベースとして機能し、全文検索やベクトル検索機能を提供して、関連情報の正確な取得を可能にする
- [Amazon Athena](https://aws.amazon.com/athena/): S3 バケット内のデータを分析するクエリサービス

![](imgs/arch.png)

## Deploy using CDK

上記 Easy Deployment は[AWS CodeBuild](https://aws.amazon.com/jp/codebuild/)を利用し、内部で CDK によるデプロイを実行しています。ここでは直接 CDK によりデプロイする手順を記載します。

- お手元に UNIX コマンドおよび Node.js, Docker 実行環境を用意してください。もし無い場合、[Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)をご利用いただくことも可能です。

> [!Note]
> デプロイ時にローカル環境のストレージ容量が不足すると CDK のブートストラップがエラーとなってしまう可能性があります。Cloud9 等で実行される場合は、インスタンスのボリュームサイズを拡張のうえデプロイ実施されることをお勧めします。

- このリポジトリをクローンします

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- npm パッケージをインストールします

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- [AWS CDK](https://aws.amazon.com/jp/cdk/)をインストールします

```
npm i -g aws-cdk
```

- CDK デプロイ前に、デプロイ先リージョンに対して 1 度だけ Bootstrap の作業が必要となります。ここでは東京リージョンへデプロイするものとします。なお`<account id>`はアカウント ID に置換してください。

```
cdk bootstrap aws://<account id>/ap-northeast-1
```

- 必要に応じて[cdk.json](../cdk/cdk.json)の下記項目を編集します

  - `bedrockRegion`: Bedrock が利用できるリージョン
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: 許可する IP アドレス範囲の指定
  - `enableLambdaSnapStart`: デフォルトでは true ですが、[Python 関数の Lambda SnapStart をサポートしていないリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)にデプロイする場合は false に変更してください。

- プロジェクトをデプロイします

```
cdk deploy --require-approval never --all
```

- 下記のような出力が得られれば成功です。`BedrockChatStack.FrontendURL`に WEB アプリの URL が出力されますので、ブラウザからアクセスしてください。

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

### Mistral を利用する

cdk.json 内の`enableMistral`を`true`に更新し、`cdk deploy`を実行します。

```json
...
  "enableMistral": true,
```

> [!Important]
> このプロジェクトは Anthropic の Claude モデルを中心としており、Mistral モデルはサポートが限定的です。例えば、プロンプトの例は Claude モデルを基準としています。これは Mistral モデル専用のオプションです。一度 Mistral モデルを有効にすると、すべてのチャット機能で Mistral モデルのみを使用できます。Claude モデルと Mistral モデルの両方を使用することはできません。

### テキスト生成パラメータの設定

[config.py](../backend/app/config.py)を編集後、`cdk deploy`を実行してください。

```py
GENERATION_CONFIG = {
    "max_tokens_to_sample": 500,
    "temperature": 0.6,
    "top_k": 250,
    "top_p": 0.999,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### サインアップ可能なメールアドレスのドメインを制限

このサンプルはデフォルトではサインアップ可能なメールアドレスのドメインに制限がありません。特定のドメインのみに限定してサインアップを可能にするには、 `cdk.json` を開き、`allowedSignUpEmailDomains` にリスト形式でドメインを指定してください。

```
"allowedSignUpEmailDomains": ["example.com"],
```

### リソースの削除

cli および CDK を利用されている場合、`cdk destroy`を実行してください。そうでない場合は[CloudFormation](https://console.aws.amazon.com/cloudformation/home)へアクセスし、手動で`BedrockChatStack`および`FrontendWafStack`を削除してください。なお`FrontendWafStack`は `us-east-1` リージョンにあります。

### 言語設定について

このアセットは、[i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector) を用いて自動で言語を検出します。もし任意の言語へ変更されたい場合はアプリケーション左下のメニューから切り替えてください。なお以下のように Query String で設定することも可能です。

> `https://example.com?lng=ja`

### セルフサインアップを無効化する

このサンプルはデフォルトでセルフサインアップが有効になっています。セルフサインアップを無効にするには、[cdk.json](../cdk/cdk.json) を開き、`selfSignUpEnabled` を `false` に切り替えてください。[外部のアイデンティティプロバイダー](#外部のアイデンティティプロバイダー)を設定している場合、この値は無視され、自動的に無効になります。

### 外部のアイデンティティプロバイダー

このサンプルは外部のアイデンティティプロバイダーをサポートしています。現在、[Google](./idp/SET_UP_GOOGLE_ja.md)および[カスタム OIDC プロバイダー](./idp/SET_UP_CUSTOM_OIDC.md)をサポートしています。

### 新規ユーザーを自動的にグループに追加

このサンプルには、ユーザーに権限を与えるための以下のようなグループがあります。

- [`Admin`](./ADMINISTRATOR.md)
- [`CreatingBotAllowed`](#ボットのカスタマイズ)
- [`PublishAllowed`](./PUBLISH_API.md)

新規に作成されたユーザーを自動的にグループに参加させたい場合、[cdk.json](../cdk/cdk.json) で指定することができます。

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

デフォルトでは、新規作成ユーザーは `CreatingBotAllowed` グループに参加します。

### RAG レプリカの設定

`enableRagReplicas` は、[cdk.json](../cdk/cdk.json) にあるオプションで、RAG のデータベース、つまり Knowledge Bases が利用する Amazon OpenSearch Serverless のレプリカ設定を制御します。

- **デフォルト**: true
- **true**: レプリカを有効にして可用性を向上させます。本番環境向けですが、コストが増加します。
- **false**: レプリカ数を減らしてコストを削減します。開発やテスト環境向けです。

この設定はアカウント/リージョンレベルで適用され、個々のボットではなくアプリ全体に影響します。

> [!Note]
> 2024 年 6 月時点で、Amazon OpenSearch Serverless は 0.5 OCU をサポートし、小規模なワークロードのエントリーコストを削減しました。本番環境では 2 OCU から、開発/テスト環境では 1 OCU から利用可能です。負荷に応じて自動的にスケールします。詳細は[アナウンス](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)をご覧ください。

### クロスリージョン推論

[クロスリージョン推論](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)を有効にすると、Amazon Bedrock はモデル推論リクエストを複数の AWS リージョン間で動的にルーティングし、ピーク時の需要に対してスループットとレジリエンスを向上させます。設定するには、`cdk.json`ファイルを編集し、以下のように指定します。

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) は Lambda 関数のコールドスタート時間を短縮し、レスポンスタイムの改善によってユーザー体験を向上させます。ただし、Python 関数については[キャッシュサイズに比例した利用料金](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)が発生するのに加え、[一部のリージョン](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)では現在利用できません。SnapStart を無効化するには、`cdk.json` を以下のように編集します。

```json
"enableLambdaSnapStart": false
```

### ローカルでの開発について

- [こちら](./LOCAL_DEVELOPMENT_ja.md)を参照ください。

### Pull Request

コントリビュートを検討していただきありがとうございます！バグ修正、言語翻訳（i18n）、機能拡張、[エージェントのツール](./AGENT.md#how-to-develop-your-own-tools)、その他の改善を歓迎しています。

機能拡張やその他の改善については、**プルリクエストを作成する前に、実装方法や詳細について議論するために、Feature Request Issue を作成いただくようお願いいたします。**

バグ修正については、直接プルリクエストを作成してください。

コントリビュートする前に、以下のガイドラインもご確認ください。

- [ローカル環境での開発](./LOCAL_DEVELOPMENT_ja.md)
- [CONTRIBUTING](../CONTRIBUTING.md)
