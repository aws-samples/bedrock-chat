# 管理機能

## 前提条件

管理者ユーザーは、管理コンソール > Amazon Cognito ユーザープールまたはaws cliを通じて設定できる`Admin`というグループのメンバーである必要があります。なお、ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできます。

![](./imgs/group_membership_admin.png)

## 公開ボットを「Essential」としてマークする

管理者は公開ボットを「Essential」（必須）としてマークできるようになりました。Essentialとしてマークされたボットは、ボットストアの「Essential」セクションに表示され、ユーザーが簡単にアクセスできるようになります。これにより、管理者は全ユーザーに使ってほしい重要なボットをピン留めすることができます。

### 例

- HR アシスタントボット：人事関連の質問やタスクについて従業員をサポート
- IT サポートボット：社内の技術的な問題やアカウント管理についてサポートを提供
- 社内規定ガイドボット：勤怠規則、セキュリティポリシー、その他の社内規定に関するよくある質問に回答
- 新入社員オンボーディングボット：初日の手続きやシステムの使用方法について新入社員をガイド
- 福利厚生情報ボット：会社の福利厚生プログラムやサービスについて説明

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## フィードバックループ

LLMからの出力は、必ずしもユーザーの期待に沿うものとは限りません。時にはユーザーのニーズを満たせないこともあります。LLMをビジネス運営や日常生活に効果的に「統合」するためには、フィードバックループの実装が不可欠です。Bedrock Chatには、不満が生じた理由を分析できるフィードバック機能が搭載されています。分析結果に基づいて、プロンプト、RAGデータソース、パラメータなどを適宜調整することができます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータを分析したい場合は、[このノートブック例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にすることができます。

## ダッシュボード

現在、チャットボットとユーザーの使用状況の基本的な概要を提供しており、各ボットとユーザーのデータを特定の期間にわたって集計し、使用料金順に結果を並べ替えることに重点を置いています。

![](./imgs/admin_bot_analytics.png)

## 注意事項

- [アーキテクチャ](../README.md#architecture)に記載されているように、管理者機能はDynamoDBからエクスポートされたS3バケットを参照します。エクスポートは1時間ごとに実行されるため、最新の会話がすぐには反映されない場合があることにご注意ください。

- パブリックボットの使用状況では、指定された期間中に全く使用されていないボットは一覧に表示されません。

- ユーザーの使用状況では、指定された期間中にシステムを全く使用していないユーザーは一覧に表示されません。

> [!Important]
> 複数の環境（dev、prodなど）を使用している場合、Athenaのデータベース名には環境のプレフィックスが含まれます。`bedrockchatstack_usage_analysis`の代わりに、以下のようになります：
>
> - デフォルト環境の場合：`bedrockchatstack_usage_analysis`
> - 名前付き環境の場合：`<env-prefix>_bedrockchatstack_usage_analysis`（例：`dev_bedrockchatstack_usage_analysis`）
>
> さらに、テーブル名にも環境のプレフィックスが含まれます：
>
> - デフォルト環境の場合：`ddb_export`
> - 名前付き環境の場合：`<env-prefix>_ddb_export`（例：`dev_ddb_export`）
>
> 複数の環境で作業する場合は、クエリを適切に調整するようにしてください。

## 会話データのダウンロード

Athenaを使用してSQLで会話ログを照会することができます。ログをダウンロードするには、管理コンソールからAthena Query Editorを開いてSQLを実行します。以下は、ユースケースの分析に役立つクエリ例です。フィードバックは`MessageMap`属性で参照できます。

### ボットID別のクエリ

`bot-id`と`datehour`を編集してください。`bot-id`は、左サイドバーに表示されているBot Publish APIsからアクセスできるBot Management画面で参照できます。URLの末尾の`https://xxxx.cloudfront.net/admin/bot/<bot-id>`のような部分に注目してください。

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
> 名前付き環境（例：「dev」）を使用している場合は、上記クエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。

### ユーザーID別のクエリ

`user-id`と`datehour`を編集してください。`user-id`はBot Management画面で参照できます。

> [!Note]
> ユーザー使用状況の分析は近日公開予定です。

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
> 名前付き環境（例：「dev」）を使用している場合は、上記クエリの`bedrockchatstack_usage_analysis.ddb_export`を`dev_bedrockchatstack_usage_analysis.dev_ddb_export`に置き換えてください。