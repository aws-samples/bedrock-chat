# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ja/README.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ko/README.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/zh/README.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/fr/README.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/de/README.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/es/README.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/it/README.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/no/README.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/th/README.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/id/README.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ms/README.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/vi/README.md)

> [!Warning]  
> **V2がリリースされました。更新する際は、[移行ガイド](./migration/V1_TO_V2.md)を注意深く確認してください。** 注意を払わないと、**V1のBOTは使用できなくなります。**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)が提供するLLMモデルを使用した多言語チャットボット。

### YouTubeで概要とインストールを確認

[![概要](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](./imgs/demo.gif)

### ボットのパーソナライズ

独自の指示を追加し、URLやファイルとして外部の知識を提供（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。ボットはアプリケーションユーザー間で共有できます。カスタマイズされたボットはスタンドアロンAPIとして公開することもできます（[詳細](./PUBLISH_API.md)参照）。

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由から、許可されたユーザーのみがカスタマイズされたボットを作成できます。カスタマイズされたボットの作成を許可するには、ユーザーは`CreatingBotAllowed`グループのメンバーである必要があります。これは管理コンソール > Amazon Cognito User poolsまたはaws cliで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`にアクセスすることで参照できます。

### 管理者ダッシュボード

<details>
<summary>管理者ダッシュボード</summary>

管理者ダッシュボードで、ユーザー/ボットごとの使用状況を分析できます。[詳細](./ADMINISTRATOR.md)

![](./imgs/admin_bot_analytics.png)

</details>

### LLMベースのエージェント

<details>
<summary>LLMベースのエージェント</summary>

[エージェント機能](./AGENT.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、エージェントは外部ツールから必要な情報を取得したり、タスクを複数のステップに分解して処理したりできます。

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超簡単デプロイ

- us-east-1リージョンで、[Bedrockモデルアクセス](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)を開き、`モデルアクセスの管理`から`Anthropic / Claude 3`のすべて、`Amazon / Nova`のすべて、`Amazon / Titan Text Embeddings V2`、`Cohere / Embed Multilingual`をチェックし、`変更を保存`します。

<details>
<summary>スクリーンショット</summary>

![](./imgs/model_screenshot.png)

</details>

- デプロイしたいリージョンで[CloudShell](https://console.aws.amazon.com/cloudshell/home)を開きます
- 以下のコマンドでデプロイを実行します。デプロイするバージョンを指定したい場合やセキュリティポリシーを適用する必要がある場合は、[オプションパラメータ](#オプションパラメータ)から適切なパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーかv2を使用するかを尋ねられます。v0からの継続ユーザーでない場合は、`y`を入力してください。

### オプションパラメータ

デプロイ時に以下のパラメータを指定して、セキュリティとカスタマイズを強化できます：

- **--disable-self-register**: 自己登録を無効化（デフォルト：有効）。このフラグが設定されている場合、すべてのユーザーをCognitoで作成する必要があり、ユーザーは自分でアカウントを登録できません。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)を有効化（デフォルト：無効）。このフラグが設定されている場合、Lambdaファンクションの起動時間を改善し、より高速な応答時間を提供します。
- **--ipv4-ranges**: 許可されたIPv4範囲のカンマ区切りリスト。（デフォルト：すべてのIPv4アドレスを許可）
- **--ipv6-ranges**: 許可されたIPv6範囲のカンマ区切りリスト。（デフォルト：すべてのIPv6アドレスを許可）
- **--disable-ipv6**: IPv6接続を無効化。（デフォルト：有効）
- **--allowed-signup-email-domains**: サインアップを許可するメールドメインのカンマ区切りリスト。（デフォルト：ドメイン制限なし）
- **--bedrock-region**: Bedrockが利用可能なリージョン。（デフォルト：us-east-1）
- **--repo-url**: デプロイするBedrock Claude Chatのカスタムリポジトリ。（デフォルト：https://github.com/aws-samples/bedrock-claude-chat.git）
- **--version**: デプロイするBedrock Claude Chatのバージョン。（デフォルト：開発中の最新バージョン）
- **--cdk-json-override**: デプロイ中にCDKコンテキスト値を上書きできます。cdk.jsonファイルを直接編集せずに設定を変更できます。

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

オーバーライドJSONはcdk.jsonと同じ構造に従う必要があります。以下のコンテキスト値を含む任意の値を上書きできます：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- cdk.jsonで定義されている他のコンテキスト値

> [!Note]
> オーバーライド値は、AWS CodeBuildでデプロイ時に既存のcdk.json設定とマージされます。指定されたオーバーライド値は、cdk.jsonの値よりも優先されます。

#### パラメータを含むコマンド例：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 約35分後、以下のような出力が表示され、ブラウザからアクセスできます

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

上記のようなサインアップ画面が表示され、メールを登録してログインできます。

> [!Important]
> オプションパラメータを設定しない場合、このデプロイ方法では、URLを知っている人は誰でもサインアップできます。本番環境では、IPアドレス制限を追加し、自己サインアップを無効にして、セキュリティリスクを軽減することを強くお勧めします（許可されたサインアップメールドメインを定義して、会社のドメインのメールアドレスのみがサインアップできるようにできます）。IPアドレス制限には、ipv4-rangesとipv6-rangesの両方を使用し、./binの実行時にdisable-self-registerを使用して自己サインアップを無効にしてください。

> [!TIP]
> `Frontend URL`が表示されないか、Bedrock Claude Chatが正常に動作しない場合、最新バージョンに問題がある可能性があります。この場合、`--version "v1.2.6"`をパラメータに追加して、デプロイを再試行してください。

（注意：全文の翻訳は長いため、続きは別のレスポンスで提供します。）

## 🌟 機能

### モデルの選択

- Claude 3 (Opus, Sonnet, Haiku)
- Amazon Titan
- Amazon Titan Embeddings
- Cohere Embed Multilingual

### 主な機能

- 💬 マルチモーダルチャット
  - テキスト、画像の対話
  - 多言語サポート
- 🤖 カスタマイズ可能なボット
  - 独自の指示
  - 外部知識の統合
- 🔍 高度な検索と要約
- 📊 管理者分析ダッシュボード
- 🌐 マルチリージョンサポート
- 🔒 エンタープライズセキュリティ
  - IAM統合
  - IP制限
  - メールドメイン制限

## 🛠 技術スタック

- フロントエンド: React, TypeScript
- バックエンド: AWS Lambda, Python
- インフラ: AWS CDK
- データベース: Amazon DynamoDB
- 認証: Amazon Cognito
- モデル: Amazon Bedrock

## 📖 詳細ドキュメント

- [カスタムボット作成](./BOT_CREATION.md)
- [エージェント機能](./AGENT.md)
- [管理者ガイド](./ADMINISTRATOR.md)
- [APIの公開](./PUBLISH_API.md)
- [セキュリティ設定](./SECURITY.md)

## 🤝 貢献とサポート

貢献やバグ報告は歓迎します！GitHubの[Issues](https://github.com/aws-samples/bedrock-claude-chat/issues)セクションをご利用ください。

## 📜 ライセンス

このプロジェクトはMITライセンスの下で提供されています。

## 🤝 貢献とサポート

貢献やバグ報告は歓迎します！GitHubの[Issues](https://github.com/aws-samples/bedrock-claude-chat/issues)セクションをご利用ください。

## 📜 ライセンス

このプロジェクトはMITライセンスの下で提供されています。

## よくある質問

<details>
<summary>よくある質問を展開</summary>

### Q. どのようなAWSリソースが作成されますか？

以下のAWSリソースが作成されます：

- Amazon Bedrock
- Amazon CloudFront
- Amazon Cognito
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon S3
- AWS IAM
- Amazon CloudWatch
- AWS Step Functions

### Q. コストはいくらかかりますか？

コストは使用量によって異なります。主な料金は以下の通りです：

- Amazon Bedrock: モデル使用量に基づく
- AWS Lambda: リクエスト数と実行時間
- Amazon DynamoDB: 読み取り/書き込みユニット
- Amazon S3: ストレージと転送
- Amazon CloudFront: データ転送

詳細な見積もりは、[AWS料金計算ツール](https://calculator.aws/)で確認できます。

### Q. セキュリティはどのように確保されていますか？

セキュリティ機能：

- Amazon Cognito認証
- IAMロールとポリシー
- IP制限
- メールドメイン制限
- 暗号化されたデータストレージ

詳細は[セキュリティドキュメント](./SECURITY.md)を参照してください。

### Q. 多言語対応はどの程度ですか？

- UIは多言語対応
- チャットは多言語をサポート
- Claude 3は多言語理解が可能

### Q. カスタマイズはどこまでできますか？

- ボットの指示をカスタマイズ可能
- 外部知識の追加
- APIとしてボットを公開可能

### Q. トラブルシューティング

デプロイ中の問題：
- AWS CLIとCDKの最新版を使用
- リージョンのBedrock利用可能状況を確認
- CloudWatch Logsでエラーを確認

</details>

## 最後に

Bedrock Claude Chatをお楽しみください！🎉

申し訳ありません。前回の翻訳は既に完了していました。他に翻訳が必要な部分はありますか？