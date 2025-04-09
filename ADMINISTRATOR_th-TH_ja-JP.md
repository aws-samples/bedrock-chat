# 管理者の属性

管理者の属性は非常に重要なツールです。カスタムボットの使用状況とユーザーの行動に関する重要な洞察を提供するためです。この機能がないと、管理者は、どのカスタムボットが人気があり、なぜ人気があり、誰がユーザーであるかを理解することが困難になります。これらの情報は、推奨事項の改善、RAGソースのカスタマイズ、そして潜在的な影響力のあるヘビーユーザーの特定において非常に重要です。

## フィードバックループ

LLMの出力は常にユーザーの期待に応えるわけではありません。時には、ユーザーのニーズに応えられないこともあります。LLMsをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループを活用することが重要です。Bedrock Claude Chatには、ユーザーが不満の原因を分析できるように設計されたフィードバック機能があります。分析結果に基づいて、ユーザーは適切にプロンプト、RAGソース、およびその他のパラメータを調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスし、[Jupyter Notebook](https://jupyter.org/)でデータを分析できます。[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)を参照することができます。

## 管理者ダッシュボード

現在、チャットボットと利用者の基本的な利用概要を提供し、特定の期間における各ボットと利用者のデータ収集に焦点を当て、利用コストに基づいて結果を並べ替えています。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー利用分析は近日中に提供予定です

### 前提条件

管理者ユーザーは、`Admin`という名前のグループのメンバーである必要があります。このグループは管理コンソール > Amazon Cognito User pools または AWS CLIを通じて設定できます。ユーザーグループIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできることに注意してください。

![](./imgs/group_membership_admin.png)

## メモ

- [アーキテクチャ](../README.md#architecture)で指定されているように、管理者機能は DynamoDB からエクスポートされた S3 バケットを参照します。エクスポートは1時間ごとに行われるため、最新の会話がすぐに表示されない可能性があることに注意してください。

- パブリックボットの使用では、指定された期間に全く使用されていないボットは表示されません。

- ユーザー使用状況では、指定された期間にシステムを全く使用していないユーザーは表示されません。

> [!重要]
> **マルチ環境データベース名**
>
> 複数の環境（dev、prod など）を使用している場合、Athena のデータベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis` の代わりに、データベース名は以下のようになります：
>
> - デフォルト環境の場合: `bedrockchatstack_usage_analysis`
> - 名前付き環境の場合: `<環境プレフィックス>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> また、テーブル名にも環境プレフィックスが含まれます：
>
> - デフォルト環境の場合: `ddb_export`
> - 名前付き環境の場合: `<環境プレフィックス>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する際は、クエリを適切に調整してください。

## 会話データのダウンロード

Athena を使用して SQL で会話ログを検索できます。Athena クエリエディターを管理コンソールから開き、以下の SQL クエリを実行します。以下は、ユースケース分析に役立つクエリの例です。`MessageMap` 属性で参照できます。

### Bot ID によるクエリ

`bot-id` と `datehour` を編集します。`bot-id` はサイドバーに表示される Bot Publish API から、Bot 管理ページで参照できます。URL の末尾（例：`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）を確認してください。

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> 名前付き環境（例：「dev」）を使用する場合は、クエリ内の `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。

### ユーザー ID によるクエリ

`user-id` と `datehour` を編集します。`user-id` は Bot 管理ページで参照できます。

> [!Note]
> ユーザー利用状況分析は近日中に提供予定です。

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> 名前付き環境（例：「dev」）を使用する場合は、クエリ内の `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。