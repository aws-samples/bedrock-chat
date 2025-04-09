# 管理者向け機能

管理者向け機能は、カスタムボットの使用状況とユーザーの行動に関する重要な洞察を提供する重要なツールです。この機能がない場合、管理者は、どのカスタムボットが人気があるのか、なぜ人気があるのか、誰がそれらを使用しているのかを理解するのに苦労するでしょう。この情報は、指示プロンプトの最適化、RAGデータソースのカスタマイズ、潜在的なインフルエンサーになり得るヘビーユーザーの特定に非常に重要です。

## フィードバックループ

LLMの出力は常にユーザーの期待に応えられるわけではありません。時には、ユーザーのニーズを満たせないこともあります。LLMをビジネスや日常生活に効果的に「統合」するためには、フィードバックループの実装が重要です。Bedrock Claude Chatには、ユーザーが不満の理由を分析するのに役立つように設計されたフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、および対応するパラメータを調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合は、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)が参考になるでしょう。

## 管理ダッシュボード

現在、チャットボットと利用者の基本的な概要を提供し、指定された時間枠内の各ボットおよび利用者のデータを集計し、使用量に基づいて結果を整理します。

![](./imgs/admin_bot_analytics.png)

> [!注意]
> ユーザー利用分析は近日提供予定です。

### 前提条件

管理者ユーザーは、`Admin`と呼ばれるグループのメンバーである必要があり、管理ダッシュボード > Amazon Cognito ユーザープール、またはAWS CLIを通じて設定できます。ユーザーグループIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`にアクセスすることで参照できます。

![](./imgs/group_membership_admin.png)

## 注意事項

- [アーキテクチャ](../README.md#architecture)で述べたように、管理機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに実行されるため、最新の会話がすぐに反映されない可能性があることに注意してください。

- パブリックボットの使用では、指定された期間内に使用されていないボットは一覧表示されません。

- ユーザー使用状況では、指定された期間内にシステムを使用していないユーザーは一覧表示されません。

> [!重要]
> **マルチ環境データベース名**
>
> 複数の環境（dev、prod など）を使用している場合、Athenaのデータベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は以下のようになります：
>
> - デフォルト環境の場合: `bedrockchatstack_usage_analysis`
> - 名前付き環境の場合: `<環境プレフィックス>_bedrockchatstack_usage_analysis`（例: `dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境プレフィックスが含まれます：
>
> - デフォルト環境の場合: `ddb_export`
> - 名前付き環境の場合: `<環境プレフィックス>_ddb_export`（例: `dev_ddb_export`）
>
> 複数の環境で作業する際は、クエリを適切に調整してください。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、分析に役立つ例のクエリです。レスポンスは `MessageMap` 属性で参照できます。

### Bot IDによるクエリ

`bot-id` と `datehour` を編集します。`bot-id` はBot管理画面で確認でき、Bot公開APIからアクセスでき、左側のサイドバーに表示されます。URLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注目してください。

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

> [!メモ]
> 名前付き環境（例：「dev」）を使用している場合は、上記のクエリの `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。

### ユーザー IDによるクエリ

`user-id` と `datehour` を編集します。`user-id` はBot管理画面で確認できます。

> [!メモ]
> ユーザー利用状況の分析は近日公開予定です。

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

> [!メモ]
> 名前付き環境（例：「dev」）を使用している場合は、上記のクエリの `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。