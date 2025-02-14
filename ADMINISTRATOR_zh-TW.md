# 管理員功能

管理員功能是一個至關重要的工具，因為它提供了關於自訂機器人使用情況和使用者行為的重要洞察。沒有這些功能，管理員將難以了解哪些自訂機器人受歡迎、為什麼受歡迎，以及誰在使用它們。這些資訊對於優化指令提示、自訂 RAG 資料來源，以及識別可能成為影響者的重度使用者至關重要。

## 回饋迴路

來自大型語言模型（LLM）的輸出可能無法始終符合使用者的期望。有時它無法滿足使用者的需求。為了有效地將大型語言模型整合到商業運營和日常生活中，建立回饋迴路至關重要。Bedrock Claude Chat 配備了一個回饋功能，旨在讓使用者能夠分析不滿意的原因。根據分析結果，使用者可以相應地調整提示詞、RAG 資料來源和參數。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

資料分析師可以使用 [Amazon Athena](https://aws.amazon.com/jp/athena/) 存取對話記錄。如果他們想要使用 [Jupyter Notebook](https://jupyter.org/) 進行資料分析，[此筆記本範例](../examples/notebooks/feedback_analysis_example.ipynb) 可以作為參考。

## 管理員儀表板

目前提供聊天機器人和使用者使用情況的基本總覽，著重於針對每個機器人和使用者在指定時間段內彙總資料，並按使用費用排序結果。

![](./imgs/admin_bot_analytics.png)

> [!Note]
> 使用者使用分析即將推出。

### 先決條件

管理員使用者必須是名為 `Admin` 的群組成員，可以透過管理主控台 > Amazon Cognito 使用者池或 AWS CLI 設定。請注意，使用者池 ID 可以通過存取 CloudFormation > BedrockChatStack > 輸出 > `AuthUserPoolIdxxxx` 來參考。

![](./imgs/group_membership_admin.png)

## 備註

- 如[架構](../README.md#architecture)中所述，管理功能將參考從 DynamoDB 匯出的 S3 儲存貯體。請注意，由於匯出是每小時執行一次，最新的對話可能不會立即反映。

- 在公開機器人使用情況中，在指定期間內完全未使用的機器人將不會被列出。

- 在使用者使用情況中，在指定期間內完全未使用系統的使用者將不會被列出。

## 下載對話資料

您可以使用 Athena 透過 SQL 查詢對話日誌。要下載日誌，請從管理主控台開啟 Athena 查詢編輯器並執行 SQL。以下是一些有助於分析使用案例的範例查詢。回饋可以在 `MessageMap` 屬性中參考。

### 依 Bot ID 查詢

編輯 `bot-id` 和 `datehour`。`bot-id` 可以在 Bot 管理畫面中查看，該畫面可以從左側側邊欄的 Bot 發佈 API 存取。注意 URL 的最後部分，如 `https://xxxx.cloudfront.net/admin/bot/<bot-id>`。

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

### 依 User ID 查詢

編輯 `user-id` 和 `datehour`。`user-id` 可以在 Bot 管理畫面中查看。

> [!Note]
> 使用者使用分析即將推出。

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