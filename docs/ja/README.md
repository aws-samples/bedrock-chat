# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ja/README.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ko/README.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/zh/README.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/fr/README.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/de/README.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/es/README.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/it/README.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/no/README.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/th/README.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/id/README.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ms/README.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/vi/README.md)

> [!Warning]  
> **V2がリリースされました。更新する際は、[移行ガイド](./migration/V1_TO_V2.md)を慎重に確認してください。** 注意を払わないと、**V1のボットは使用できなくなります。**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)が提供する生成AIのLLMモデルを使用した多言語チャットボット。

### YouTubeで概要とインストールを視聴

[![概要](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](./imgs/demo.gif)

### ボットのパーソナライズ

独自の指示を追加し、URLやファイルとして外部知識を提供（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。ボットはアプリケーションユーザー間で共有できます。カスタマイズされたボットはスタンドアロンAPIとして公開することもできます（[詳細](./PUBLISH_API.md)を参照）。

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由により、許可されたユーザーのみがカスタマイズされたボットを作成できます。カスタマイズされたボットの作成を許可するには、ユーザーは`CreatingBotAllowed`グループのメンバーである必要があります。これは管理コンソール > Amazon Cognito ユーザープールまたはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできます。

### 管理者ダッシュボード

<details>
<summary>管理者ダッシュボード</summary>

管理者ダッシュボードで、ユーザー/ボットごとの使用状況を分析します。[詳細](./ADMINISTRATOR.md)

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

- us-east-1リージョンで、[Bedrockモデルアクセス](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)を開き、`モデルアクセスの管理` > `Anthropic / Claude 3`のすべて、`Amazon / Nova`のすべて、`Amazon / Titan Text Embeddings V2`、`Cohere / Embed Multilingual`をチェックし、`変更を保存`します。

<details>
<summary>スクリーンショット</summary>

![](./imgs/model_screenshot.png)

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

- デプロイが完了したら、コンソール出力に表示されるURLにアクセスします。
- 初めてのサインアップ時は、`Sign up`を選択し、新しいユーザーを作成します。

### オプションパラメータ

デプロイ時に以下のパラメータをカスタマイズできます：

| パラメータ | デフォルト | 説明 |
|----------|------------|------|
| `--region` | `us-east-1` | デプロイするAWSリージョン |
| `--branch` | `v2` | デプロイするGitブランチ |
| `--allow-origin` | `*` | CORSで許可するオリジン |
| `--bot-creating-allowed-group` | なし | ボット作成を許可するCognitoグループ名 |
| `--admin-email` | なし | 管理者のメールアドレス |

例：
```sh
./bin.sh --region us-west-2 --branch v2 --admin-email your-email@example.com
```

## 🌟 主な機能

- **多言語対応**: 日本語、英語、韓国語など、多言語でチャットできます
- **カスタムボット**: 独自の指示と知識ベースを持つボットを作成可能
- **高度なRAG**: URLやファイルからの情報検索
- **エージェント機能**: 複雑なタスクを自動処理
- **管理者ダッシュボード**: 使用状況の分析と管理

## 🔒 セキュリティ

- Amazon Cognito認証
- IAMベースのアクセス制御
- AWS WAFによるWebアプリケーション保護

## 🛠 アーキテクチャ

![Architecture](./imgs/architecture.png)

## 📦 主要コンポーネント

- フロントエンド: React
- バックエンド: AWS Lambda, API Gateway
- データベース: Amazon DynamoDB
- 認証: Amazon Cognito
- AI基盤: Amazon Bedrock

## 🤝 貢献

貢献方法は[貢献ガイドライン](CONTRIBUTING.md)を参照してください。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細は[LICENSE](LICENSE)を参照してください。

## 🚨 免責事項

これはサンプル実装であり、本番環境での使用には追加の設定と調整が必要です。

🚨 免責事項は既に翻訳されているため、追加の翻訳は不要です。他に翻訳が必要な部分がありますか?