# 管理者機能

管理者機能は、カスタムボットの使用状況とユーザーの行動に関する重要な洞察を提供する、非常に重要なツールです。これらの機能がなければ、管理者は、どのカスタムボットが人気があり、なぜ人気があるのか、そしてだれがそれらを使用しているのかを理解することが困難になります。これらの情報は、インストラクションプロンプトの最適化、カスタムRAGデータソースの調整、そして潜在的なインフルエンサーになり得る重度ユーザーの特定において極めて重要です。

## フィードバックループ

大規模言語モデル（LLM）の出力は、必ずしもユーザーの期待に沿わない場合があります。時には、ユーザーのニーズを満たせないこともあります。大規模言語モデルを効果的にビジネス運営や日常生活に統合するためには、フィードバックループの実装が重要です。Bedrock Claude Chat には、ユーザーが不満足な理由を分析できるフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/) を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/) でデータを分析したい場合、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb) を参考にできます。

## 管理者ダッシュボード

現在、チャットボットとユーザーの利用状況に関する基本的な概要が提供されており、特定の期間内の各ボットおよびユーザーのデータを集計し、利用コストで結果をソートすることに重点を置いています。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー利用分析は近日公開予定です。

### 前提条件

管理者ユーザーは、`Admin` という名前のグループのメンバーである必要があり、管理コンソール > Amazon Cognito ユーザープールまたは AWS CLI を通じて設定できます。ユーザープール ID は、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` から参照できることに注意してください。

![](./imgs/group_membership_admin.png)

## Notes

- As described in the [architecture](../README.md#architecture), management functions will reference the S3 bucket exported from DynamoDB. Note that due to exports being performed hourly, the most recent conversations may not be immediately reflected.

- In public bot usage, bots that have not been used during the specified period will not be listed.

- In user usage, users who have not used the system during the specified period will not be listed.

> [!Important] > **Multi-Environment Database Names**
>
> If you are using multiple environments (development, production, etc.), the Athena database names will include an environment prefix. Instead of `bedrockchatstack_usage_analysis`, the database names will be:
>
> - For the default environment: `bedrockchatstack_usage_analysis`
> - For named environments: `<env-prefix>_bedrockchatstack_usage_analysis` (e.g., `dev_bedrockchatstack_usage_analysis`)
>
> Additionally, table names will include the environment prefix:
>
> - For the default environment: `ddb_export`
> - For named environments: `<env-prefix>_ddb_export` (e.g., `dev_ddb_export`)
>
> When working with multiple environments, be sure to adjust your queries accordingly.

## 対話データのダウンロード

Athenaを使用してSQLクエリで対話ログをダウンロードできます。ログをダウンロードするには、管理コンソールからAthenaクエリエディターを開き、SQLを実行します。以下は、分析ユースケースに役立つクエリ例です。フィードバックは `MessageMap` 属性で参照できます。

### Bot IDによるクエリ

`bot-id` と `datehour` を編集します。`bot-id` はボット管理画面で確認できます。この画面はボット公開APIからアクセスでき、左側のサイドバーに表示されます。URLの末尾部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>` など）に注目してください。

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
> 名前付き環境（「dev」など）を使用している場合は、上記のクエリの `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。

### ユーザーIDによるクエリ

`user-id` と `datehour` を編集します。`user-id` はボット管理画面で確認できます。

> [!Note]
> ユーザー使用状況分析は近日公開予定です。

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
> 名前付き環境（「dev」など）を使用している場合は、上記のクエリの `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。