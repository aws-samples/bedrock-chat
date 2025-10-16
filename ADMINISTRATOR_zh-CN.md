# 管理功能

## 前提条件

管理员用户必须是名为 `Admin` 的用户组成员，可以通过管理控制台 > Amazon Cognito 用户池或 aws cli 进行设置。请注意，可以通过访问 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` 来获取用户池 ID。

![](./imgs/group_membership_admin.png)

## 将公共机器人标记为"基础"

管理员现在可以将公共机器人标记为"基础"。被标记为基础的机器人将在机器人商店的"基础"区域中展示，让用户可以轻松访问。这使管理员能够置顶他们希望所有用户使用的重要机器人。

### 示例

- HR 助手机器人：帮助员工解答人力资源相关问题和任务。
- IT 支持机器人：为内部技术问题和账户管理提供协助。
- 内部政策指南机器人：回答关于考勤规则、安全政策和其他内部规定的常见问题。
- 新员工入职机器人：指导新员工完成入职第一天的程序和系统使用。
- 福利信息机器人：解释公司福利计划和员工服务。

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## 反馈循环

LLM的输出可能并不总是符合用户的期望。有时它无法满足用户的需求。为了有效地将LLMs"集成"到业务运营和日常生活中，实施反馈循环至关重要。Bedrock Chat配备了反馈功能，旨在使用户能够分析产生不满意的原因。基于分析结果，用户可以相应地调整提示词、RAG数据源和参数。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

数据分析师可以使用[Amazon Athena](https://aws.amazon.com/jp/athena/)访问对话日志。如果他们想要通过[Jupyter Notebook](https://jupyter.org/)分析数据，可以参考[这个笔记本示例](../examples/notebooks/feedback_analysis_example.ipynb)。

## 仪表盘

目前提供了聊天机器人和用户使用情况的基本概览，主要关注在特定时间段内汇总每个机器人和用户的数据，并按使用费用对结果进行排序。

![](./imgs/admin_bot_analytics.png)

## 注意事项

- 如[架构](../README.md#architecture)中所述，管理功能将引用从 DynamoDB 导出到 S3 存储桶的数据。请注意，由于导出操作每小时执行一次，最新的对话可能不会立即反映出来。

- 在公共机器人使用情况中，在指定时期内完全未被使用过的机器人将不会被列出。

- 在用户使用情况中，在指定时期内完全未使用过系统的用户将不会被列出。

> [!Important]
> 如果您使用多个环境（开发环境、生产环境等），Athena 数据库名称将包含环境前缀。数据库名称将不再是 `bedrockchatstack_usage_analysis`，而是：
>
> - 默认环境：`bedrockchatstack_usage_analysis`
> - 指定环境：`<env-prefix>_bedrockchatstack_usage_analysis`（例如：`dev_bedrockchatstack_usage_analysis`）
>
> 此外，表名也将包含环境前缀：
>
> - 默认环境：`ddb_export`
> - 指定环境：`<env-prefix>_ddb_export`（例如：`dev_ddb_export`）
>
> 在使用多个环境时，请确保相应地调整您的查询。

## 下载对话数据

您可以使用 SQL 通过 Athena 查询对话日志。要下载日志，请从管理控制台打开 Athena 查询编辑器并运行 SQL。以下是一些用于分析用例的示例查询。反馈可以在 `MessageMap` 属性中查看。

### 按 Bot ID 查询

编辑 `bot-id` 和 `datehour`。`bot-id` 可以在 Bot 管理界面上查看，该界面可以从左侧边栏的 Bot 发布 API 访问。注意 URL 末尾的格式如 `https://xxxx.cloudfront.net/admin/bot/<bot-id>`。

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
> 如果使用命名环境（例如"dev"），请在上述查询中将 `bedrockchatstack_usage_analysis.ddb_export` 替换为 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`。

### 按用户 ID 查询

编辑 `user-id` 和 `datehour`。`user-id` 可以在 Bot 管理界面上查看。

> [!Note]
> 用户使用分析功能即将推出。

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
> 如果使用命名环境（例如"dev"），请在上述查询中将 `bedrockchatstack_usage_analysis.ddb_export` 替换为 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`。