# 管理者の特徴

管理者の特徴は非常に重要なツールであり、カスタムボットの使用状況とユーザーの行動について重要な洞察を提供します。この機能がなければ、管理者にとって、どのカスタムボットが人気があり、なぜ人気があり、誰が使用しているかを理解することは困難になります。この情報は、プロンプト指示の最適化、RAGデータソースの調整、頻繁に使用するユーザーの特定において非常に重要です。

## フィードバックループ

LLMの出力は常にユーザーの期待に応えられるわけではありません。時には、ユーザーのニーズを満たすことに失敗することがあります。LLMをビジネス運営や日常生活に効果的に統合するためには、フィードバックループを実装することが重要です。Bedrock Claude Chatには、ユーザーが不満の理由を分析できるように設計されたフィードバック機能が備わっています。分析結果に基づいて、ユーザーは適切な指示、RAGのデータソース、パラメータを調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合は、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)を参照できます。

## 管理者ダッシュボード

現在、チャットボットの基本的な使用状況と利用者の概要を提供し、特定の期間内の各ボットおよび利用者のデータ収集に焦点を当て、使用料に基づいて結果を並べ替えます。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー利用状況の分析は近々提供予定です。

### 前提条件

管理者ユーザーは、`Admin`と呼ばれるグループのメンバーである必要があります。これは、管理コンソール > Amazon Cognito ユーザープールまたはAWS CLIを通じて設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`にアクセスすることで参照できます。

![](./imgs/group_membership_admin.png)

## 注意

- [アーキテクチャ](../README.md#architecture)で述べられているように、管理者の特性は、DynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに行われるため、最新の会話がすぐに反映されない可能性があることに注意してください。

- パブリックボットの使用では、指定された期間まったく使用されていないボットはリストされません。

- ユーザー使用では、指定された期間にシステムをまったく使用していないユーザーはリストされません。

> [!重要] > **マルチ環境データベース名**
>
> 複数の環境（dev、prod など）を使用している場合、Athenaのデータベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は次のようになります：
>
> - デフォルト環境の場合：`bedrockchatstack_usage_analysis`
> - 名前付き環境の場合：`<環境プレフィックス>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境プレフィックスが含まれます：
>
> - デフォルト環境の場合：`ddb_export`
> - 名前付き環境の場合：`<環境プレフィックス>_ddb_export`（例：`dev_ddb_export`）
>
> マルチ環境で作業する際は、適切にクエリを調整してください。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを取得できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、使用事例を分析するためのいくつかの有用なクエリの例です。応答は`MessageMap`属性で参照できます。

### Bot IDによるクエリ

`bot-id`と`datehour`を編集します。`bot-id`は、左サイドバーのBot Publish APIsからアクセスできるBot管理画面で参照できます。URLの末尾部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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
> 名前付き環境（例："dev"）を使用している場合は、上記のクエリ内の`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### ユーザーIDによるクエリ

`user-id`と`datehour`を編集します。`user-id`はBot管理画面で参照できます。

> [!メモ]
> ユーザー使用状況分析は近々提供予定です。

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
> 名前付き環境（例："dev"）を使用している場合は、上記のクエリ内の`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。