# 管理機能

管理機能は、カスタムボットの使用状況とユーザーの行動に関する重要な洞察を提供する不可欠なツールです。この機能がなければ、管理者にとって、どのカスタムボットが最も普及しているか、その理由、そしてそれを使用しているユーザーを理解することは困難になります。これらの情報は、指示プロンプトを最適化し、RAGのデータソースをカスタマイズし、潜在的なインフルエンサーとなり得る最も活発なユーザーを特定するために非常に重要です。

## フィードバックループ

大規模言語モデル（LLM）の出力は、常にユーザーの期待を満たすわけではありません。時には、ユーザーのニーズを満たせないことがあります。LLMを効果的にビジネス運営や日常生活に統合するためには、フィードバックループの実装が不可欠です。Bedrock Claude Chatには、ユーザーが不満の理由を分析できるように設計されたフィードバック機能が備わっています。分析結果に基づき、ユーザーはプロンプト、RAGのデータソース、パラメータを適宜調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)が参考になります。

## 管理者ダッシュボード

現在、チャットボットとユーザーの基本的な利用状況の概要を提供し、特定の期間内の各ボットとユーザーのデータを集計し、利用率に基づいて結果を並べ替えることに焦点を当てています。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー利用状況の分析は間もなく利用可能になります。

### 前提条件

管理者ユーザーは、Amazon Cognito User poolsの管理コンソールまたはAWS CLIを通じて設定できる `Admin` というグループのメンバーである必要があります。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` からアクセスできることに注意してください。

![](./imgs/group_membership_admin.png)

## 注意

- [アーキテクチャ](../README.md#architecture)で示されているように、管理機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに実行されるため、最新の会話がすぐに反映されない可能性があることに注意してください。

- パブリックボットの利用状況において、指定された期間に全く使用されていないボットはリストされません。

- ユーザーの利用状況において、指定された期間にシステムを使用していないユーザーはリストされません。

> [!重要]
> **マルチ環境のデータベース名**
>
> 複数の環境（dev、prod など）を使用する場合、Athenaデータベース名には環境のプレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は以下のようになります：
>
> - デフォルト環境の場合: `bedrockchatstack_usage_analysis`
> - 名前付き環境の場合: `<env-prefix>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境のプレフィックスが含まれます：
>
> - デフォルト環境の場合: `ddb_export`
> - 名前付き環境の場合: `<env-prefix>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する際は、クエリを適切に調整してください。

## 会話データのダウンロード

Athenaを使用してSQL経由で会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、ユースケースを分析するのに役立つクエリの例です。フィードバックは`MessageMap`属性で確認できます。

### Bot IDによるクエリ

`bot-id`と`datehour`を変更します。`bot-id`はBot管理画面で確認でき、Bot公開APIから左サイドバーにアクセスできます。URLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注目してください。

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
> 名前付き環境（例：「dev」）を使用している場合、前述のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### User IDによるクエリ

`user-id`と`datehour`を変更します。`user-id`はBot管理画面で確認できます。

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
> 名前付き環境（例：「dev」）を使用している場合、前述のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。