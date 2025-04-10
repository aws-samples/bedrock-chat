# 管理機能

管理機能は、カスタムボットの利用状況とユーザーの行動に関する重要な情報を提供する不可欠なツールです。この機能がなければ、管理者にとって、どのカスタムボットが人気があり、なぜ人気があり、誰が使用しているかを理解することは困難になります。これらの情報は、指示プロンプトを最適化し、RAGのデータソースをカスタマイズし、集中的に使用するユーザーを特定して潜在的な影響力のある人物を見つけるために不可欠です。

## フィードバックループ

LLMの出力が常にユーザーの期待に応えるとは限りません。時には、ユーザーのニーズを満たさないこともあります。LLMを事業運営や日常生活に効果的に統合するためには、フィードバックループの確立が不可欠です。Bedrock Claude Chatには、ユーザーが不満の理由を分析できるフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を通じて会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合は、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## 管理者ダッシュボード

現在、チャットボットとユーザーの基本的な利用状況の概要を提供し、特定の期間における各ボットおよびユーザーのデータ集計に焦点を当て、利用料金で結果をソートします。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー利用分析は近日公開予定です。

### 前提条件

管理者ユーザーは、Amazon Cognito管理コンソールまたはAWS CLIで設定可能な`Admin`と呼ばれるグループのメンバーである必要があります。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx`にアクセスすることで確認できます。

![](./imgs/group_membership_admin.png)

## メモ

- [アーキテクチャ](../README.md#architecture)で説明されているように、管理機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに行われるため、最新の会話がすぐに反映されない場合があることに注意してください。

- パブリックボットの使用状況では、指定された期間に全く使用されていないボットはリストに表示されません。

- ユーザー使用状況では、指定された期間にシステムを全く使用していないユーザーはリストに表示されません。

> [!Important] > **マルチ環境データベース名**
>
> 複数の環境（dev、prod など）を使用する場合、Athenaデータベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は次のようになります：
>
> - デフォルト環境の場合：`bedrockchatstack_usage_analysis`
> - 名前付き環境の場合：`<環境プレフィックス>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境プレフィックスが含まれます：
>
> - デフォルト環境の場合：`ddb_export`
> - 名前付き環境の場合：`<環境プレフィックス>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する際は、クエリを適切に調整してください。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、使用事例を分析するためのいくつかの便利なクエリ例です。コメントは`MessageMap`属性で参照できます。

### ボットIDによるクエリ

`bot-id`と`datehour`を変更します。`bot-id`は、ボット公開APIからアクセスできるボット管理画面で確認できます。左サイドバーに表示されるURLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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
> 名前付き環境（例：「dev」）を使用している場合は、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### ユーザーIDによるクエリ

`user-id`と`datehour`を変更します。`user-id`はボット管理画面で確認できます。

> [!Note]
> ユーザー別の利用分析は近日中に提供予定です。

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
> 名前付き環境（例：「dev」）を使用している場合は、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。