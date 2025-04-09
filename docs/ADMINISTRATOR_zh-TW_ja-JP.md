# 管理者機能

管理者機能は、カスタムボットの使用状況とユーザーの行動に関する重要な洞察を提供する、非常に重要なツールです。これらの機能がなければ、管理者は、どのカスタムボットが人気があり、なぜ人気があるのか、そしてそれらを誰が使用しているのかを理解することが困難になります。これらの情報は、プロンプトの最適化、RAGデータソースのカスタマイズ、そして潜在的なインフルエンサーとなり得る重度のユーザーを特定するために極めて重要です。

## フィードバックループ

大規模言語モデル（LLM）の出力は、必ずしもユーザーの期待に沿わない場合があります。時にはユーザーのニーズを満たせないこともあります。大規模言語モデルをビジネス運営や日常生活に効果的に統合するためには、フィードバックループの実装が不可欠です。Bedrock Claude Chatには、ユーザーが不満の理由を分析できるフィードバック機能が備わっています。分析結果に基づいて、ユーザーはプロンプト、RAGデータソース、パラメータを適切に調整できます。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

データアナリストは、[Amazon Athena](https://aws.amazon.com/jp/athena/)を使用して会話ログにアクセスできます。[Jupyter Notebook](https://jupyter.org/)でデータ分析を行う場合、[このノートブックの例](../examples/notebooks/feedback_analysis_example.ipynb)を参考にできます。

## 管理者ダッシュボード

現在、チャットボットとユーザーの使用状況に関する基本的な概要を提供し、指定された期間内の各ボットおよびユーザーの集計データに焦点を当て、使用コストでソートした結果を表示しています。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> ユーザー使用状況分析は近日公開予定です。

### 前提条件

管理者ユーザーは、`Admin` という名前のグループのメンバーである必要があり、管理コンソール > Amazon Cognito ユーザープールまたは AWS CLI を通じて設定できます。ユーザープール ID は、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` からアクセスできることに注意してください。

![](./imgs/group_membership_admin.png)

## Notes

- As described in the [architecture](../README.md#architecture), management features will reference the S3 bucket exported from DynamoDB. Please note that since the export is performed hourly, the most recent conversations may not be immediately reflected.

- In bot usage, bots that have not been used at all during the specified period will not be listed.

- In user usage, users who have not used the system at all during the specified period will not be listed.

> [!Important] > **Multi-Environment Database Names**
>
> If you are using multiple environments (development, production, etc.), the Athena database names will include an environment prefix. Instead of `bedrockchatstack_usage_analysis`, the database names will be:
>
> - For the default environment: `bedrockchatstack_usage_analysis`
> - For named environments: `<env-prefix>_bedrockchatstack_usage_analysis` (e.g., `dev_bedrockchatstack_usage_analysis`)
>
> Additionally, table names will also include the environment prefix:
>
> - For the default environment: `ddb_export`
> - For named environments: `<env-prefix>_ddb_export` (e.g., `dev_ddb_export`)
>
> When dealing with multiple environments, be sure to adjust your queries accordingly.

## 対話データのダウンロード

Athena と SQL を使用して対話ログをクエリできます。ログをダウンロードするには、管理コンソールから Athena クエリエディターを開き、SQLを実行します。以下は、使用事例を分析するのに役立つ例のクエリです。フィードバックは `MessageMap` 属性で参照できます。

### Bot ID によるクエリ

`bot-id` と `datehour` を編集します。`bot-id` は、左側のサイドバーにあるBot発行APIからアクセスできるBotの管理画面で確認できます。URLの末尾部分（`https://xxxx.cloudfront.net/admin/bot/<bot-id>` など）に注意してください。

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
> 名前付き環境（例：「dev」）を使用している場合は、上記のクエリの `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。

### ユーザー ID によるクエリ

`user-id` と `datehour` を編集します。`user-id` は、Botの管理画面で確認できます。

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
> 名前付き環境（例：「dev」）を使用している場合は、上記のクエリの `bedrockchatstack_usage_analysis.ddb_export` を `dev_bedrockchatstack_usage_analysis.dev_ddb_export` に置き換えてください。