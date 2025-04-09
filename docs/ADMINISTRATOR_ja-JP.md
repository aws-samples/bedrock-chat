# 管理機能

## 前提条件

管理者ユーザーは、管理コンソール > Amazon Cognito ユーザープール または AWS CLI を通じて設定できる `Admin` というグループのメンバーである必要があります。ユーザープール ID は、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` にアクセスすることで参照できます。

![](./imgs/group_membership_admin.png)

## 公開ボットを「重要」としてマーク

公開ボットは、管理者によって「重要」としてマークできるようになりました。重要としてマークされたボットは、ボットストアの「重要」セクションに掲載され、ユーザーが簡単にアクセスできるようになります。これにより、管理者は全ユーザーに使用してほしい重要なボットを固定できます。

### 例

- HRアシスタントボット：従業員のHR関連の質問や業務を支援します。
- ITサポートボット：社内の技術的な問題やアカウント管理に関する支援を提供します。
- 社内ポリシーガイドボット：出勤ルール、セキュリティポリシー、その他の社内規定に関する頻繁な質問に回答します。
- 新入社員オンボーディングボット：新入社員の初日に、手続きやシステムの使用方法をガイドします。
- 福利厚生情報ボット：会社の福利厚生プログラムと福祉サービスを説明します。

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## フィードバックループ

LLMの出力が常にユーザーの期待に応えるとは限りません。時には、ユーザーのニーズを満たせないことがあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループの実装が不可欠です。Bedrock Chatには、ユーザーが不満の原因を分析できるフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## ダッシュボード

現在、チャットボットとユーザーの使用状況に関する基本的な概要を提供し、各ボットとユーザーの指定された期間のデータを集計し、使用料金によって結果をソートすることに焦点を当てています。

![](./imgs/admin_bot_analytics.png)

## 注意事項

- [アーキテクチャ](../README.md#architecture)で述べられているように、管理者機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに実行されるため、最新の会話がすぐには反映されない可能性があることに注意してください。

- パブリックボットの使用状況では、指定された期間中に全く使用されていないボットはリストに表示されません。

- ユーザー使用状況では、指定された期間中にシステムを全く使用していないユーザーはリストに表示されません。

> [!重要]
> 複数の環境（dev、prod など）を使用している場合、Athenaデータベース名には環境接頭辞が含まれます。`bedrockchatstack_usage_analysis`の代わりに、データベース名は次のようになります：
>
> - デフォルト環境の場合: `bedrockchatstack_usage_analysis`
> - 名前付き環境の場合: `<env-prefix>_bedrockchatstack_usage_analysis`（例: `dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境接頭辞が含まれます：
>
> - デフォルト環境の場合: `ddb_export`
> - 名前付き環境の場合: `<env-prefix>_ddb_export`（例: `dev_ddb_export`）
>
> 複数の環境を扱う際は、クエリを適切に調整してください。

## 会話データのダウンロード

Athenaを使用してSQL形式で会話ログを照会できます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、ユースケースを分析するのに役立つクエリの例です。フィードバックは`MessageMap`属性で参照できます。

### ボットIDごとのクエリ

`bot-id`と`datehour`を編集します。`bot-id`はボット管理画面で参照できます。ボット公開APIからアクセスでき、左サイドバーに表示されます。URLの末尾部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>`）に注意してください。

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
> 名前付き環境（例：「dev」）を使用している場合、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### ユーザーIDごとのクエリ

`user-id`と`datehour`を編集します。`user-id`はボット管理画面で参照できます。

> [!Note]
> ユーザー使用状況分析は近日中に提供予定です。

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
> 名前付き環境（例：「dev」）を使用している場合、上記のクエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。