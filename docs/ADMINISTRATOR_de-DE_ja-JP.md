# 管理者機能

管理者機能は、カスタムボットの利用状況とユーザー行動に関する重要な洞察を提供する、決定的なツールです。これらの機能がなければ、管理者は人気のあるカスタムボット、その人気の理由、および利用者を理解することが困難になります。これらの情報は、指示プロンプトの最適化、RAGデータソースのカスタマイズ、そして潜在的にインフルエンサーになり得る集中的な利用者の特定において極めて重要です。

## フィードバックループ

LLMの出力は、必ずしもユーザーの期待に応えられないことがあります。時には、ユーザーのニーズを満たせないこともあります。LLMをビジネスプロセスや日常生活に効果的に統合するためには、フィードバックループの実装が不可欠です。Bedrock Claude Chatには、ユーザーが不満が生じた理由を分析できるフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を通じて会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)を参照できます。

## 管理者ダッシュボード

現在、指定された期間にわたる各ボットとユーザーのデータ集計に焦点を当て、使用料に基づいて結果を並べ替えることで、チャットボットおよびユーザー使用状況の基本的な概要を提供しています。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー使用状況分析は近日利用可能になります。

### 前提条件

管理者ユーザーは、管理コンソール > Amazon Cognito ユーザープール、またはAWS CLIを通じて設定できる `Admin` グループのメンバーである必要があります。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` からアクセスできることに注意してください。

![](./imgs/group_membership_admin.png)

## 注意事項

- [アーキテクチャ](../README.md#architecture)で説明されているように、管理機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間に1回しか実行されないため、最新の会話がすぐに表示されない可能性があることに注意してください。

- パブリックボットの利用状況では、指定された期間中に全く利用されなかったボットは一覧表示されません。

- ユーザー利用状況では、指定された期間中にシステムを全く利用しなかったユーザーは一覧表示されません。

> [!重要]
> **複数の環境のデータベース名**
>
> 複数の環境（dev、prod など）を使用する場合、Athenaデータベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は次のようになります：
>
> - 標準環境の場合：`bedrockchatstack_usage_analysis`
> - 名前付き環境の場合：`<環境プレフィックス>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境プレフィックスが含まれます：
>
> - 標準環境の場合：`ddb_export`
> - 名前付き環境の場合：`<環境プレフィックス>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する場合は、クエリを適切に調整してください。

## 会話データのダウンロード

Athenaを使用して、SQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。次の例のクエリは、ユースケース分析に役立ちます。フィードバックは`MessageMap`属性で確認できます。

### Bot IDによる検索

`bot-id`と`datehour`を編集します。`bot-id`は、Bot公開APIからアクセスできるBot管理画面の左サイドバーに表示されます。URLの末尾（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注目してください。

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
> 名前付き環境（例：「dev」）を使用している場合、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### ユーザーIDによる検索

`user-id`と`datehour`を編集します。`user-id`はBot管理画面で確認できます。

> [!メモ]
> ユーザー利用状況分析は近日中に追加予定です。

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
> 名前付き環境（例：「dev」）を使用している場合、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。