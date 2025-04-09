# 管理者機能

管理者機能は、カスタムチャットボットの使用状況とユーザーの行動に関する重要な洞察を提供する重要なツールです。この機能がなければ、管理者にとって、どのカスタムチャットボットが人気があり、なぜ人気があり、誰が使用しているかを理解することは困難でしょう。この情報は、指示プロンプトの最適化、RAGデータソースのカスタマイズ、潜在的なインフルエンサーとなり得る頻繁なユーザーの特定に不可欠です。

## フィードバックループ

LLMの結果は常にユーザーの期待に応えるわけではありません。時には、ユーザーのニーズを満たせないこともあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループを実装することが重要です。Bedrock Claude Chatには、ユーザーが不満の原因を分析できるように設計されたフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合、[このノートブック例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## 管理者パネル

現在、チャットボットとユーザー使用状況の基本的な概要を提供し、指定された期間にわたる各ボットおよびユーザーのデータ収集に焦点を当て、使用料に基づいて結果をソートします。

![](./imgs/admin_bot_analytics.png)

> [!注意]
> ユーザー使用状況分析は近日公開予定です。

### 前提条件

管理者ユーザーは、`Admin`と呼ばれるグループのメンバーである必要があります。これは、管理コンソール > Amazon Cognito User Pools または AWS CLIを通じて設定できます。ユーザーグループIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`を開くことで参照できます。

![](./imgs/group_membership_admin.png)

## メモ

- [アーキテクチャ](../README.md#architecture)で言及されているように、管理機能は DynamoDB からエクスポートされた S3 バケットを参照します。エクスポートは1時間に1回実行されるため、最新の会話がすぐに反映されない可能性があることに注意してください。

- パブリックボットの使用状況では、指定された期間に全く使用されていないボットは一覧に表示されません。

- ユーザー使用状況では、指定された期間にシステムを全く使用していないユーザーは一覧に表示されません。

> [!重要]
> **複数の環境のデータベース名**
>
> 複数の環境（dev、prod など）を使用する場合、Athena データベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis` の代わりに、データベース名は次のようになります：
>
> - 標準環境の場合: `bedrockchatstack_usage_analysis`
> - 名前付き環境の場合: `<環境プレフィックス>_bedrockchatstack_usage_analysis`（例: `dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境プレフィックスが含まれます：
>
> - 標準環境の場合: `ddb_export`
> - 名前付き環境の場合: `<環境プレフィックス>_ddb_export`（例: `dev_ddb_export`）
>
> 複数の環境で作業する際は、それに応じてクエリを調整してください。

## 会話データのダウンロード

Athenaを使用し、SQLを利用して会話ログを検索できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、使用事例を分析するのに役立ついくつかの例示クエリです。フィードバックは`MessageMap`属性で参照できます。

### Bot IDごとのクエリ

`bot-id`と`datehour`を編集します。`bot-id`はBotマネジメント画面で参照でき、左側のサイドパネルに表示されるBot Publish APIsからアクセスできます。URLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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

> [!注意]
> 名前付き環境（例：「dev」）を使用している場合、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### ユーザーIDごとのクエリ

`user-id`と`datehour`を編集します。`user-id`はBotマネジメント画面で参照できます。

> [!注意]
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

> [!注意]
> 名前付き環境（例：「dev」）を使用している場合、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。