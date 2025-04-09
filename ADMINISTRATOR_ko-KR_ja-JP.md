# 管理者機能

管理者機能は、カスタマイズされたボットの使用と、ユーザーの行動に関する重要な洞察を提供する重要なツールです。この機能がなければ、管理者は、どのカスタマイズされたボットが人気があり、その理由は何か、そして誰が使用しているかを把握することが困難になります。この情報は、指示プロンプトの最適化、RAGデータソースのカスタマイズ、そして潜在的に影響力のある重度のユーザーを特定するために非常に重要です。

## フィードバックループ

LLMの出力が常にユーザーの期待に応えるわけではありません。時には、ユーザーのニーズを満たせないこともあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループを実装することが不可欠です。Bedrock Claude Chatは、ユーザーが不満の原因を分析できるように設計されたフィードバック機能を備えています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合は、[このノートブック例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## 管理者ダッシュボード

現在のチャットボットおよびユーザー使用状況に関する基本的な概要を提供し、指定された期間中の各ボットおよびユーザーのデータを集計し、使用量に基づいて結果を並べ替えます。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー使用状況分析は近日提供予定です。

### 前提条件

管理者ユーザーは、`Admin`グループのメンバーである必要があり、管理コンソール > Amazon Cognito ユーザープール、またはAWS CLIを通じて設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx`からアクセスして参照できます。

![](./imgs/group_membership_admin.png)

## 注意事項

- [アーキテクチャ](../README.md#architecture)で述べられているように、管理者機能は、DynamoDBからエクスポートされたS3バケットを参照します。エクスポートは毎時1回実行されるため、最新の会話がすぐに反映されない場合があります。

- パブリックボットの使用状況では、指定された期間中まったく使用されていないボットは一覧表示されません。

- ユーザー使用状況では、指定された期間中システムをまったく使用していないユーザーは一覧表示されません。

> [!重要] > **マルチ環境データベース名**
>
> 複数の環境（dev、prodなど）を使用している場合、Athenaデータベース名には環境の接頭辞が含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は次のようになります：
>
> - デフォルト環境の場合：`bedrockchatstack_usage_analysis`
> - 名前付き環境の場合：`<env-prefix>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> また、テーブル名にも環境の接頭辞が含まれます：
>
> - デフォルト環境の場合：`ddb_export`
> - 名前付き環境の場合：`<env-prefix>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する場合は、クエリを適切に調整する必要があります。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールでAthenaクエリエディターを開き、SQLを実行してください。以下は、ユースケースを分析するのに役立つ例のクエリです。フィードバックは`MessageMap`属性から参照できます。

### ボットID別のクエリ

`bot-id`と`datehour`を編集してください。`bot-id`はボット管理画面で参照でき、Bot Publish APIを通じて左サイドバーに表示されます。URLの末尾部分（例：`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）を参考にしてください。

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

### ユーザーID別のクエリ

`user-id`と`datehour`を編集してください。`user-id`はボット管理画面で参照できます。

> [!注意]
> ユーザー使用状況分析は近日提供予定です。

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