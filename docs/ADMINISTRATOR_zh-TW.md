# 管理功能

## 前置條件

管理員使用者必須是名為 `Admin` 群組的成員，此群組可以透過管理主控台 > Amazon Cognito User pools 或 aws cli 來設定。請注意，使用者集區 ID 可以透過 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` 來查詢。

![](./imgs/group_membership_admin.png)

## 將公開機器人標記為必備機器人

管理員現在可以將公開機器人標記為「必備」。被標記為必備的機器人將會在機器人商店的「必備」區域中展示，讓使用者能夠輕鬆存取。這使管理員能夠將他們希望所有使用者都能使用的重要機器人置頂。

### 範例

- HR 助理機器人：協助員工處理人力資源相關問題和任務。
- IT 支援機器人：提供內部技術問題和帳戶管理的協助。
- 內部政策指南機器人：回答關於出勤規則、安全政策和其他內部規定的常見問題。
- 新進員工入職機器人：指導新進員工完成第一天的程序和系統使用。
- 福利資訊機器人：說明公司福利計劃和員工福利服務。

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## 反饋循環

LLM的輸出可能並不總是符合用戶的期望。有時它無法滿足用戶的需求。為了有效地將LLM"整合"到業務運營和日常生活中，實施反饋循環是至關重要的。Bedrock Chat配備了反饋功能，旨在使用戶能夠分析為什麼會產生不滿意的結果。根據分析結果，用戶可以相應地調整提示、RAG數據源和參數。

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

數據分析師可以使用[Amazon Athena](https://aws.amazon.com/jp/athena/)訪問對話日誌。如果他們想要通過[Jupyter Notebook](https://jupyter.org/)分析數據，可以參考[這個筆記本示例](../examples/notebooks/feedback_analysis_example.ipynb)。

## 儀表板

目前提供聊天機器人和使用者使用情況的基本概覽，著重於在指定時間期間內彙整每個機器人和使用者的數據，並依據使用費用進行排序。

![](./imgs/admin_bot_analytics.png)

## 備註

- 如[架構](../README.md#architecture)中所述，管理功能將參考從 DynamoDB 匯出的 S3 儲存桶。請注意，由於匯出每小時執行一次，最新的對話可能不會立即反映。

- 在公開機器人使用量中，在指定期間內完全未被使用的機器人將不會被列出。

- 在使用者使用量中，在指定期間內完全未使用系統的使用者將不會被列出。

> [!Important]
> 如果您使用多個環境（開發、正式等），Athena 資料庫名稱將包含環境前綴。資料庫名稱將不是 `bedrockchatstack_usage_analysis`，而是：
>
> - 預設環境：`bedrockchatstack_usage_analysis`
> - 具名環境：`<env-prefix>_bedrockchatstack_usage_analysis`（例如：`dev_bedrockchatstack_usage_analysis`）
>
> 此外，資料表名稱也將包含環境前綴：
>
> - 預設環境：`ddb_export`
> - 具名環境：`<env-prefix>_ddb_export`（例如：`dev_ddb_export`）
>
> 在處理多個環境時，請確保相應地調整您的查詢。

## 下載對話資料

您可以使用 SQL 透過 Athena 查詢對話記錄。要下載記錄，請從管理控制台開啟 Athena Query Editor 並執行 SQL。以下是一些用於分析使用案例的範例查詢。回饋可以在 `MessageMap` 屬性中查看。

### 依 Bot ID 查詢

編輯 `bot-id` 和 `datehour`。`bot-id` 可以在 Bot 管理畫面上查看，該畫面可從左側邊欄的 Bot Publish APIs 進入。注意 URL 末尾的格式如 `https://xxxx.cloudfront.net/admin/bot/<bot-id>`。

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
> 如果使用命名環境（例如 "dev"），請將查詢中的 `bedrockchatstack_usage_analysis.ddb_export` 替換為 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`。

### 依使用者 ID 查詢

編輯 `user-id` 和 `datehour`。`user-id` 可以在 Bot 管理畫面上查看。

> [!Note]
> 使用者使用分析功能即將推出。

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
> 如果使用命名環境（例如 "dev"），請將查詢中的 `bedrockchatstack_usage_analysis.ddb_export` 替換為 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`。