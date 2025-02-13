# 管理者機能

管理者機能は、カスタムボットの利用状況とユーザーの行動に関する重要な洞察を提供する不可欠なツールです。この機能がなければ、管理者にとって、どのカスタムボットが人気があり、なぜ人気があるのか、そしてどのユーザーが利用しているのかを理解することは困難になります。この情報は、指示プロンプトの最適化、RAGデータソースのカスタマイズ、そして潜在的なインフルエンサーとなり得るヘビーユーザーの特定において極めて重要です。

## フィードバックループ

LLMの出力が常にユーザーの期待に応えるわけではありません。時には、ユーザーのニーズを満たすことができないことがあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループの実装が不可欠です。Bedrock Claude Chatには、ユーザーが不満の原因を分析できるようにするフィードバック機能が備わっています。分析結果に基づき、ユーザーはプロンプト、RAGデータソース、およびパラメータを適宜調整できます。

![](../imgs/feedback_loop.png)

![](../imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合、[このノートブック例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## 管理者ダッシュボード

現在、チャットボットとユーザーの使用状況の基本的な概要を提供し、指定された期間内の各ボットおよびユーザーのデータを集計し、使用料金でソートした結果を表示しています。

![](../imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー使用状況分析は近日公開予定です。

### 前提条件

管理者ユーザーは、管理コンソール > Amazon Cognito ユーザープール または aws cli で設定できる `Admin` というグループのメンバーである必要があります。ユーザープール ID は、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` にアクセスすることで参照できます。

![](../imgs/group_membership_admin.png)

## メモ

- [アーキテクチャ](../README.md#architecture)で述べられているように、管理機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間に1回実行されるため、最新の会話がすぐに反映されない可能性があることに注意してください。

- パブリックボットの使用状況において、指定された期間中まったく使用されていないボットはリストに表示されません。

- ユーザーの使用状況において、指定された期間中システムをまったく使用していないユーザーはリストに表示されません。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、ユースケースを分析するのに役立つクエリの例です。フィードバックは`MessageMap`属性で参照できます。

### Bot IDごとのクエリ

`bot-id`と`datehour`を編集します。`bot-id`はBotパブリッシュAPIからアクセスできるBot管理画面で確認できます。URLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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

### ユーザーIDごとのクエリ

`user-id`と`datehour`を編集します。`user-id`はBot管理画面で確認できます。

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