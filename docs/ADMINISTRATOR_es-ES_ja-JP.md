# 管理機能

管理機能は、カスタムボットの使用状況とユーザーの行動に関する重要な情報を提供する重要なツールです。この機能がなければ、管理者にとって、どのカスタムボットが人気があり、なぜ人気があり、誰が使用しているかを理解することは困難になります。この情報は、指示メッセージの最適化、RAGデータソースのカスタマイズ、潜在的なインフルエンサーになる可能性のある集中的なユーザーの特定に不可欠です。

## フィードバックループ

LLMの出力は常にユーザーの期待に応えるわけではありません。時には、ユーザーのニーズを満たせないこともあります。LLMを効果的にビジネス運営や日常生活に「統合」するためには、フィードバックループを実装することが不可欠です。Bedrock Claude Chatには、ユーザーが不満の原因を分析できるように設計されたフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合は、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)を参照できます。

## 管理パネル

現在、チャットボットと利用者の基本的な概要を提供し、特定の時間枠内で各ボットと利用者のデータを追加し、使用率に基づいて結果を並べ替えることに焦点を当てています。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー利用分析は近日中に利用可能になります。

### 前提条件

管理者ユーザーは、Amazon Cognito のユーザーグループコンソールまたは AWS CLI を通じて設定できる `Admin` という名前のグループのメンバーである必要があります。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` にアクセスすることで確認できます。

![](./imgs/group_membership_admin.png)

## 注意事項

- [アーキテクチャ](../README.md#architecture)で示されているように、管理機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに1回実行されるため、最新の会話がすぐに反映されない可能性があることに注意してください。

- 公開ボットの使用では、指定された期間に全く使用されていないボットは表示されません。

- ユーザーの使用では、指定された期間にシステムを全く使用していないユーザーは表示されません。

> [!重要]
> **マルチ環境のデータベース名**
>
> 複数の環境（dev、prod など）を使用している場合、Athenaデータベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は次のようになります：
>
> - デフォルト環境の場合: `bedrockchatstack_usage_analysis`
> - 名前付き環境の場合: `<環境プレフィックス>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境プレフィックスが含まれます：
>
> - デフォルト環境の場合: `ddb_export`
> - 名前付き環境の場合: `<環境プレフィックス>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する際は、クエリを適切に調整してください。

## 会話データのダウンロード

Athenaを使用し、SQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、ユースケースを分析するための便利なクエリの例です。コメントは`MessageMap`属性で照会できます。

### ボットIDによるクエリ

`bot-id`と`datehour`を編集します。`bot-id`は、左サイドバーに表示されるBotパブリッシングAPIからアクセスできるボット管理画面で確認できます。URLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注目してください。

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
> 名前付き環境（例：「dev」）を使用している場合は、前述のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### ユーザーIDによるクエリ

`user-id`と`datehour`を編集します。`user-id`はボット管理画面で確認できます。

> [!メモ]
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

> [!メモ]
> 名前付き環境（例：「dev」）を使用している場合は、前述のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。