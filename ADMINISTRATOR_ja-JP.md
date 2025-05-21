# 管理機能

## 前提条件

管理者ユーザーは、管理コンソール > Amazon Cognito ユーザープールまたはAWS CLIを介して設定できる `Admin` と呼ばれるグループのメンバーである必要があります。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` にアクセスすることで参照できます。

![](./imgs/group_membership_admin.png)

## 公ボットットット」として指マーク

公開ットボ管者者」ーク可能になり。「Essential（要要不可欠）」」とマークされたでたボットは、、ストアの「Essential」セクションに�特集され、ユーザーが�簡単にクる。これに理理者は、要すべのユ使用したほしい重要なボをットをピンできますよう。



### 例

- HR ア助タントボット：従事関問と タスクを支援します。
- ITサポートボットット技術的的的な問題とアカウント管理のサポート提供します。
。
- 内部針ドボット：出席規則、セ全セキュリティポリシー、その他の内部規定に関する頻繁な質問に回答します。
- 新入社員オンボーディングボット：新入社員の初日の、順とシステム使用をガイドします。
- 福利厚生情報ボット：会社の福利厚生プログラムと福祉サービスをします明。

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## フィードバックループ

LLMの出力が常にユーザーの期待に応えるとは限りません。時にはユーザーのニーズを満たせないことがあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループの実装が不可欠です。Bedrock Chatには、ユーザーが不満の原因を分析できるフィードバック機能が備わっています。分析結果に基づき、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## ダッシュボード

現在、チャットボットとユーザーの使用状況に関する基本的な概要を提供しており、特定の期間内の各ボットとユーザーのデータを集計し、使用料金によって結果をソートすることに焦点を当てています。

![](./imgs/admin_bot_analytics.png)

## 注意事項

- [アーキテクチャ](../README.md#architecture)で述べられているように、管理者機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに実行されるため、最新の会話がすぐに反映されない場合があることに注意してください。

- パブリックボットの使用状況では、指定された期間中に全く使用されていないボットは一覧に表示されません。

- ユーザーの使用状況では、指定された期間中にシステムを全く使用していないユーザーは一覧に表示されません。

> [!Important]
> 複数の環境（dev、prod など）を使用している場合、Athenaデータベース名には環境プレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は次のようになります：
>
> - デフォルト環境の場合：`bedrockchatstack_usage_analysis`
> - 名前付き環境の場合：`<env-prefix>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境プレフィックスが含まれます：
>
> - デフォルト環境の場合：`ddb_export`
> - 名前付き環境の場合：`<env-prefix>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する際は、クエリを適切に調整してください。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、ユースケースを分析するのに役立つクエリの例です。フィードバックは`MessageMap`属性で参照できます。

### Bot IDごとのクエリ

`bot-id`と`datehour`を編集します。`bot-id`は、Bot公開APIからアクセスできるBot管理画面で確認できます。URLの最後の部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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
> 名前付き環境（例：「dev」）を使用する場合、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### ユーザーIDごとのクエリ

`user-id`と`datehour`を編集します。`user-id`はBot管理画面で確認できます。

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
> 名前付き環境（例：「dev」）を使用する場合、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。