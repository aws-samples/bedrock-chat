# 管理者機能

管理者機能は、カスタムボットの使用状況とユーザーの行動に関する重要な洞察を提供する重要なツールです。この機能がなければ、管理者にとって、どのカスタムボットが人気があるのか、なぜ人気があるのか、誰が使用しているのかを理解することは困難になります。この情報は、指示プロンプトの最適化、RAGデータソースのカスタマイズ、そして影響力のある可能性のある大量利用者の特定において極めて重要です。

## フィードバックループ

LLMの出力が常にユーザーの期待に応えるとは限りません。時にはユーザーのニーズを満たせないことがあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループの実装が不可欠です。Bedrock Claude Chatには、ユーザーが不満の原因を分析できるようにするフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適宜調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合、[このノートブック例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## 管理者ダッシュボード

現在、チャットボットとユーザーの使用状況の基本的な概要を提供し、指定された期間内の各ボットとユーザーのデータを集計し、使用料金で結果をソートすることに焦点を当てています。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー使用状況分析は近日公開予定です。

### 前提条件

管理者ユーザーは、管理コンソール > Amazon Cognito ユーザープール、またはAWS CLIを介して設定できる `Admin` と呼ばれるグループのメンバーである必要があります。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` にアクセスすることで参照できることに注意してください。

![](./imgs/group_membership_admin.png)

## メモ

- [アーキテクチャ](../README.md#architecture)で述べられているように、管理機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに実行されるため、最新の会話がすぐに反映されない場合があることに注意してください。

- パブリックボットの使用状況では、指定された期間中に全く使用されていないボットはリストに表示されません。

- ユーザーの使用状況では、指定された期間中にシステムを全く使用していないユーザーはリストに表示されません。

> [!Important] > **マルチ環境データベース名**
>
> 複数の環境（dev、prodなど）を使用している場合、Athenaデータベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は以下のようになります：
>
> - デフォルト環境の場合: `bedrockchatstack_usage_analysis`
> - 名前付き環境の場合: `<env-prefix>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境プレフィックスが含まれます：
>
> - デフォルト環境の場合: `ddb_export`
> - 名前付き環境の場合: `<env-prefix>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する際は、クエリを適切に調整してください。

## 会話データのダウンロード

Athenaを使用してSQL形式で会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、ユースケースを分析するのに役立つ例のクエリです。フィードバックは `MessageMap` 属性で参照できます。

### Bot IDごとのクエリ

`bot-id` と `datehour` を編集します。`bot-id` はBot管理画面で参照でき、Bot公開APIからアクセスできます。左サイドバーに表示されます。URLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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
> 名前付き環境（例：「dev」）を使用している場合、上記のクエリの `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。

### ユーザーIDごとのクエリ

`user-id` と `datehour` を編集します。`user-id` はBot管理画面で参照できます。

> [!メモ]
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

> [!メモ]
> 名前付き環境（例：「dev」）を使用している場合、上記のクエリの `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。