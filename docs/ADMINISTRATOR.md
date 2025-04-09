# Administrative features

## Prerequisites

The admin user must be a member of group called `Admin`, which can be set up via the management console > Amazon Cognito User pools or aws cli. Note that the user pool id can be referred by accessing CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Mark public bots as Essential

Public bots can now be marked as "Essential" by administrators. Bots marked as Essential will be featured in the "Essential" section of the bot store, making them easily accessible to users. This allows administrators to pin important bots that they want all users to use.

### Examples

- HR Assistant Bot: Helps employees with HR-related questions and tasks.
- IT Support Bot: Provides assistance for internal technical issues and account management.
- Internal Policy Guide Bot: Answers frequently asked questions about attendance rules, security policies, and other internal regulations.
- New Employee Onboarding Bot: Guides new hires through procedures and system usage on their first day.
- Benefits Information Bot: Explains company benefit programs and welfare services.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Feedback loop

The output from LLM may not always meet the user's expectations. Sometimes it fails to satisfy the user's needs. To effectively "integrate" LLMs into business operations and daily life, implementing a feedback loop is essential. Bedrock Chat is equipped with a feedback feature designed to enable users to analyze why dissatisfaction arose. Based on the analysis results, users can adjust the prompts, RAG data sources, and parameters accordingly.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Data analysts can access to conversation logs using [Amazon Athena](https://aws.amazon.com/jp/athena/). If they want to analyze the data by [Jupyter Notebook](https://jupyter.org/), [this notebook example](../examples/notebooks/feedback_analysis_example.ipynb) can be a reference.

## Dashboard

Currently provides a basic overview of chatbot and user usage, focusing on aggregating data for each bot and user over specified time periods and sorting the results by usage fees.

![](./imgs/admin_bot_analytics.png)

## Notes

- As stated in the [architecture](../README.md#architecture), the admin features will refer to the S3 bucket exported from DynamoDB. Please note that since the export is performed once every hour, the latest conversations may not be reflected immediately.

- In public bot usages, bots that have not been used at all during the specified period will not be listed.

- In user usages, users who have not used the system at all during the specified period will not be listed.

> [!Important]
> If you're using multiple environments (dev, prod, etc.), the Athena database name will include the environment prefix. Instead of `bedrockchatstack_usage_analysis`, the database name will be:
>
> - For default environment: `bedrockchatstack_usage_analysis`
> - For named environments: `<env-prefix>_bedrockchatstack_usage_analysis` (e.g., `dev_bedrockchatstack_usage_analysis`)
>
> Additionally, the table name will include the environment prefix:
>
> - For default environment: `ddb_export`
> - For named environments: `<env-prefix>_ddb_export` (e.g., `dev_ddb_export`)
>
> Make sure to adjust your queries accordingly when working with multiple environments.

## Download conversation data

You can query the conversation logs by Athena, using SQL. To download logs, open Athena Query Editor from management console and run SQL. Followings are some example queries which are useful to analyze use-cases. Feedback can be referred in `MessageMap` attribute.

### Query per Bot ID

Edit `bot-id` and `datehour`. `bot-id` can be referred on Bot Management screen, where can be accessed from Bot Publish APIs, showing on the left sidebar. Note the end part of the URL like `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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
> If using a named environment (e.g., "dev"), replace `bedrockchatstack_usage_analysis.ddb_export` with `dev_bedrockchatstack_usage_analysis.dev_ddb_export` in the query above.

### Query per User ID

Edit `user-id` and `datehour`. `user-id` can be referred on Bot Management screen.

> [!Note]
> User usage analytics is coming soon.

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
> If using a named environment (e.g., "dev"), replace `bedrockchatstack_usage_analysis.ddb_export` with `dev_bedrockchatstack_usage_analysis.dev_ddb_export` in the query above.
