# 管理者機能

管理者機能は、カスタムボットの使用状況とユーザーの行動に関する重要な洞察を提供する重要なツールです。この機能がないと、管理者がどのカスタムボットが人気なのか、なぜ人気なのか、誰が使用しているのかを理解することは困難になります。この情報は、指示プロンプトの最適化、RAGデータソースのカスタマイズ、影響力のある可能性のある大量利用者の特定に不可欠です。

## フィードバックループ

LLMの出力が常にユーザーの期待に応えるとは限りません。時にはユーザーのニーズを満たせないことがあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループの実装が不可欠です。Bedrock Claude Chatには、ユーザーが不満の原因を分析できるフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](../imgs/feedback_loop.png)

![](../imgs/feedback-using-claude-chat.png)

データアナリストは[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合は、[このノートブック例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## 管理者ダッシュボード

現在、指定された期間内の各ボットおよびユーザーのデータを集計し、使用料金でソートする基本的な概要を提供しています。

![](../imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー使用状況分析は近日公開予定です。

### 前提条件

管理者ユーザーは、管理コンソール > Amazon Cognito ユーザープール またはAWS CLIで設定できる `Admin` というグループのメンバーである必要があります。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` からアクセスできます。

![](../imgs/group_membership_admin.png)

## 注意事項

- [アーキテクチャ](../README.md#architecture)で述べたように、管理者機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに実行されるため、最新の会話がすぐに反映されない可能性があることに注意してください。

- パブリックボットの使用状況では、指定された期間に全く使用されていないボットは一覧に表示されません。

- ユーザー使用状況では、指定された期間にシステムを全く使用していないユーザーは一覧に表示されません。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、ユースケースを分析するのに役立つ例のクエリです。フィードバックは `MessageMap` 属性で参照できます。

### ボットID別のクエリ

`bot-id` と `datehour` を編集します。`bot-id` はBot管理画面で参照でき、Bot公開APIからアクセスできます。左サイドバーに表示されます。URLの末尾（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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

### ユーザーID別のクエリ

`user-id` と `datehour` を編集します。`user-id` はBot管理画面で参照できます。

> [!Note]
> ユーザー使用状況分析は近日公開予定です。

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