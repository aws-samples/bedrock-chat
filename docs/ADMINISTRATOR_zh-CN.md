# 管理员功能

管理员功能是一个至关重要的工具，因为它提供了关于自定义机器人使用情况和用户行为的关键洞察。没有这些功能，管理员将难以了解哪些自定义机器人受欢迎，为什么受欢迎，以及谁在使用它们。这些信息对于优化指令提示、定制RAG数据源以及识别可能成为影响者的重度用户至关重要。

## 反馈循环

来自大语言模型（LLM）的输出可能并不总是符合用户的期望。有时它无法满足用户的需求。为了有效地将大语言模型"集成"到业务运营和日常生活中，实施反馈循环至关重要。Bedrock Claude Chat 配备了反馈功能，旨在使用户能够分析不满意的原因。基于分析结果，用户可以相应地调整提示词、RAG数据源和参数。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

数据分析师可以使用 [Amazon Athena](https://aws.amazon.com/jp/athena/) 访问对话日志。如果他们想通过 [Jupyter Notebook](https://jupyter.org/) 分析数据，[此笔记本示例](../examples/notebooks/feedback_analysis_example.ipynb) 可以作为参考。

## 管理员仪表板

目前提供了聊天机器人和用户使用情况的基本概述，主要侧重于按指定时间段汇总每个机器人和用户的数据，并按使用费用对结果进行排序。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> 用户使用分析即将推出。

### 先决条件

管理员用户必须是名为 `Admin` 的组的成员，可以通过管理控制台 > Amazon Cognito 用户池或 AWS CLI 进行设置。请注意，可以通过访问 CloudFormation > BedrockChatStack > 输出 > `AuthUserPoolIdxxxx` 来引用用户池 ID。

![](./imgs/group_membership_admin.png)

## 注意事项

- 如[架构](../README.md#architecture)中所述，管理功能将引用从 DynamoDB 导出的 S3 存储桶。请注意，由于导出每小时执行一次，最新的对话可能不会立即反映。

- 在公共机器人使用情况中，在指定期间未被使用的机器人将不会被列出。

- 在用户使用情况中，在指定期间未使用系统的用户将不会被列出。

> [!Important] > **多环境数据库名称**
>
> 如果你使用多个环境（开发、生产等），Athena 数据库名称将包含环境前缀。不是 `bedrockchatstack_usage_analysis`，数据库名称将是：
>
> - 对于默认环境：`bedrockchatstack_usage_analysis`
> - 对于命名环境：`<env-prefix>_bedrockchatstack_usage_analysis`（例如，`dev_bedrockchatstack_usage_analysis`）
>
> 此外，表名将包含环境前缀：
>
> - 对于默认环境：`ddb_export`
> - 对于命名环境：`<env-prefix>_ddb_export`（例如，`dev_ddb_export`）
>
> 在处理多个环境时，请确保相应地调整你的查询。

## 下载对话数据

您可以使用 Athena 通过 SQL 查询对话日志。要下载日志，请从管理控制台打开 Athena 查询编辑器并运行 SQL。以下是一些有用于分析用例的示例查询。反馈可以在 `MessageMap` 属性中引用。

### 按 Bot ID 查询

编辑 `bot-id` 和 `datehour`。`bot-id` 可以在机器人管理屏幕上查看，该屏幕可从机器人发布 API 访问，显示在左侧侧边栏上。注意 URL 末尾部分，如 `https://xxxx.cloudfront.net/admin/bot/<bot-id>`。

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
> 如果使用命名环境（例如"dev"），请在上面的查询中将 `bedrockchatstack_usage_analysis.ddb_export` 替换为 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`。

### 按用户 ID 查询

编辑 `user-id` 和 `datehour`。`user-id` 可以在机器人管理屏幕上查看。

> [!Note]
> 用户使用分析即将推出。

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
> 如果使用命名环境（例如"dev"），请在上面的查询中将 `bedrockchatstack_usage_analysis.ddb_export` 替换为 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`。