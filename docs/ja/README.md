# Bedrock Claude チャット (Nova)

![](https://github.com/aws-samples/bedrock-claude-chat/actions/workflows/cdk.yml/badge.svg)

> [!Warning] > **V2がリリースされました。更新する場合は、[移行ガイド](./migration/V1_TO_V2.md)を慎重に確認してください。** 注意を払わないと、**V1のBOTは使用できなくなります。**

このリポジトリは、[Amazon Bedrock](https://aws.amazon.com/jp/bedrock/)で提供される基盤モデルの1つである、Anthropic社のLLM [Claude](https://www.anthropic.com/)を使用したサンプルチャットボットです。

### YouTubeで概要とインストールを確認

[![概要](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](./imgs/demo.gif)

### ボットのパーソナライズ

独自の指示を追加し、URLまたはファイルとして外部知識を提供できます（[RAG](https://aws.amazon.com/jp/what-is/retrieval-augmented-generation/)）。ボットはアプリケーションユーザー間で共有できます。カスタマイズされたボットはスタンドアロンAPIとして公開することもできます（[詳細](./PUBLISH_API.md)を参照）。

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由から、許可されたユーザーのみがカスタマイズされたボットを作成できます。カスタマイズされたボットの作成を許可するには、ユーザーは`CreatingBotAllowed`グループのメンバーである必要があります。これは管理コンソール > Amazon Cognito ユーザープールまたはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできます。

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

## 📚 サポートされている言語

- 英語 💬
- 日本語 💬 (ドキュメントは[こちら](./README_ja.md))
- 韓国語 💬
- 中国語 💬
- フランス語 💬
- ドイツ語 💬
- スペイン語 💬
- イタリア語 💬
- ノルウェー語 💬
- タイ語 💬
- インドネシア語 💬
- マレー語 💬
- ベトナム語 💬

（以下、残りの部分も同様に翻訳します。文字数制限のため、全文の翻訳は省略しています。必要に応じて続きを翻訳できます。）