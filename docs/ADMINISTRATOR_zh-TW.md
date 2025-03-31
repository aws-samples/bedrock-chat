# 管理員功能

管理員功能是一個至關重要的工具，因為它提供了關於客製化機器人使用情況和使用者行為的重要洞察。若沒有這些功能，管理員將難以了解哪些客製化機器人受歡迎、為什麼受歡迎，以及誰在使用它們。這些資訊對於優化指令提示、自訂RAG資料來源，以及識別可能成為影響者的重度使用者至關重要。

## 回饋迴路

來自大型語言模型（LLM）的輸出可能無法始終符合使用者的期望。有時它無法滿足使用者的需求。為了有效地將大型語言模型整合到商業運營和日常生活中，建立回饋迴路是至關重要的。Bedrock Claude Chat 配備了一個回饋功能，旨在使用戶能夠分析不滿意的原因。根據分析結果，用戶可以相應地調整提示詞、RAG 資料來源和參數。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

資料分析師可以使用 [Amazon Athena](https://aws.amazon.com/jp/athena/) 存取對話記錄。如果他們想使用 [Jupyter Notebook](https://jupyter.org/) 進行數據分析，[此筆記本範例](../examples/notebooks/feedback_analysis_example.ipynb) 可以作為參考。

## 管理員儀表板

目前提供聊天機器人和使用者使用情況的基本概述，著重於在指定的時間段內彙總每個機器人和使用者的資料，並按使用費用進行排序。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> 使用者使用分析即將推出。

### 先決條件

管理員使用者必須是名為 `Admin` 的群組成員，可以透過管理控制台 > Amazon Cognito 使用者池或 AWS CLI 設定。請注意，可以透過存取 CloudFormation > BedrockChatStack > 輸出 > `AuthUserPoolIdxxxx` 來參考使用者池 ID。

![](./imgs/group_membership_admin.png)

## 備註

- 如[架構](../README.md#architecture)中所述，管理功能將參考從 DynamoDB 匯出的 S3 儲存貯體。請注意，由於匯出是每小時執行一次，最新的對話可能不會立即反映。

- 在公開機器人使用情況中，在指定期間內未被使用的機器人將不會被列出。

- 在使用者使用情況中，在指定期間內未使用系統的使用者將不會被列出。

> [!Important] > **多環境資料庫名稱**
>
> 如果您使用多個環境（開發、正式等），Athena 資料庫名稱將包含環境前綴。不是 `bedrockchatstack_usage_analysis`，資料庫名稱將是：
>
> - 對於預設環境：`bedrockchatstack_usage_analysis`
> - 對於具名環境：`<環境前綴>_bedrockchatstack_usage_analysis`（例如 `dev_bedrockchatstack_usage_analysis`）
>
> 此外，表格名稱也將包含環境前綴：
>
> - 對於預設環境：`ddb_export`
> - 對於具名環境：`<環境前綴>_ddb_export`（例如 `dev_ddb_export`）
>
> 在使用多個環境時，請務必相應調整您的查詢。

## 下載對話資料

您可以使用 Athena 和 SQL 查詢對話日誌。要下載日誌，請從管理控制台打開 Athena 查詢編輯器並運行 SQL。以下是一些有助於分析用例的範例查詢。反饋可以在 `MessageMap` 屬性中查看。

### 按機器人 ID 查詢

編輯 `bot-id` 和 `datehour`。`bot-id` 可以在機器人管理畫面上查看，該畫面可以從左側邊欄的機器人發佈 API 存取。注意 URL 末尾部分，如 `https://xxxx.cloudfront.net/admin/bot/<bot-id>`。

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
> 如果使用命名環境（例如 "dev"），請在上述查詢中將 `bedrockchatstack_usage_analysis.ddb_export` 替換為 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`。

### 按用戶 ID 查詢

編輯 `user-id` 和 `datehour`。`user-id` 可以在機器人管理畫面上查看。

> [!Note]
> 用戶使用分析即將推出。

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
> 如果使用命名環境（例如 "dev"），請在上述查詢中將 `bedrockchatstack_usage_analysis.ddb_export` 替換為 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`。