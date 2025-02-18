# 管理者機能

管理者機能は、カスタムボットの利用状況とユーザーの行動に関する重要な洞察を提供する不可欠なツールです。この機能がなければ、管理者にとって、どのカスタムボットが人気があり、なぜ人気があるのか、そしてだれが利用しているのかを理解することは困難になります。この情報は、指示プロンプトの最適化、RAGデータソースのカスタマイズ、そして潜在的なインフルエンサーとなりうるヘビーユーザーの特定において極めて重要です。

## フィードバックループ

LLMの出力が常にユーザーの期待に応えるとは限りません。時にはユーザーのニーズを満たせないことがあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループの実装が不可欠です。Bedrock Claude Chatには、ユーザーが不満の原因を分析できるフィードバック機能が備わっています。分析結果に基づき、ユーザーはプロンプト、RAGデータソース、パラメータを適宜調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合、[このノートブック例](../examples/notebooks/feedback_analysis_example.ipynb)が参考になります。

## 管理者ダッシュボード

現在、チャットボットとユーザーの利用状況の基本的な概要を提供しており、指定された期間内の各ボットおよびユーザーのデータを集計し、利用料金で結果をソートすることに焦点を当てています。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー利用状況の分析は近日中に提供予定です。

### 前提条件

管理者ユーザーは、管理コンソール > Amazon Cognito ユーザープール または AWS CLI を通じて設定できる `Admin` という名前のグループのメンバーである必要があります。ユーザープール ID は、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` にアクセスすることで参照できます。

![](./imgs/group_membership_admin.png)

## メモ

- [アーキテクチャ](../README.md#architecture)で述べられているように、管理機能は DynamoDB からエクスポートされた S3 バケットを参照します。エクスポートは1時間ごとに実行されるため、最新の会話がすぐに反映されない場合があることに注意してください。

- パブリックボットの利用状況では、指定された期間中に全く使用されていないボットはリストに表示されません。

- ユーザー利用状況では、指定された期間中にシステムを全く使用していないユーザーはリストに表示されません。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、ユースケースを分析するのに役立つ例のクエリです。フィードバックは`MessageMap`属性で参照できます。

### Bot IDごとのクエリ

`bot-id`と`datehour`を編集します。`bot-id`はBot管理画面で参照でき、Bot公開APIからアクセスできるサイドバーの左側に表示されます。URLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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

`user-id`と`datehour`を編集します。`user-id`はBot管理画面で参照できます。

> [!Note]
> ユーザー利用状況分析は近日公開予定です。

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