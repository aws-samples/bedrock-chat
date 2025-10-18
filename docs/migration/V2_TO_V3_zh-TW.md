# 遷移指南（v2 至 v3）

## 重點摘要

- V3 版本引入細緻的權限控制和 Bot 商店功能，需要更改 DynamoDB 結構
- **在遷移前請備份您的 DynamoDB ConversationTable**
- 將您的儲存庫 URL 從 `bedrock-claude-chat` 更新為 `bedrock-chat`
- 執行遷移腳本以將您的資料轉換為新的結構
- 所有您的機器人和對話將在新的權限模型下得到保留
- **重要提醒：在遷移過程中，應用程式將對所有使用者無法使用，直到遷移完成。此過程通常需要約 60 分鐘，具體取決於資料量和您的開發環境性能。**
- **重要提醒：在遷移過程中必須刪除所有已發布的 API。**
- **警告：遷移過程無法保證所有機器人 100% 成功遷移。請在遷移前記錄下重要的機器人配置，以防需要手動重新建立**

## 簡介

### V3 的新功能

V3 為 Bedrock Chat 引入了重大改進：

1. **精細的權限控制**：透過使用者群組權限來控制機器人的存取
2. **機器人商店**：透過集中式市集分享和探索機器人
3. **管理功能**：管理 API、標記重要機器人，並分析機器人使用情況

這些新功能需要變更 DynamoDB 結構，因此現有使用者需要進行遷移程序。

### 為什麼需要這次遷移

新的權限模型和機器人商店功能需要重新架構機器人資料的儲存和存取方式。遷移程序會將您現有的機器人和對話轉換為新結構，同時保留所有資料。

> [!WARNING]
> 服務中斷通知：**在遷移過程中，應用程式將無法供所有使用者使用。** 請計劃在使用者不需要存取系統的維護時段內執行此遷移。應用程式只有在遷移腳本成功完成且所有資料都正確轉換為新結構後才能重新使用。這個過程通常需要約 60 分鐘，具體取決於資料量和您的開發環境效能。

> [!IMPORTANT]
> 開始遷移前注意事項：**遷移程序無法保證所有機器人 100% 成功**，特別是使用較舊版本或自訂配置建立的機器人。請在開始遷移程序前記錄下重要的機器人配置（指令、知識來源、設定），以備需要手動重新建立時使用。

## 遷移程序

### V3版本中機器人可見性的重要通知

在V3中，**所有啟用公開分享的v2機器人都可以在機器人商店中被搜尋到。** 如果您有包含敏感資訊且不希望被發現的機器人，請考慮在遷移到V3之前將它們設為私密。

### 步驟1：確認您的環境名稱

在此程序中，`{YOUR_ENV_PREFIX}` 用於識別您的 CloudFormation Stacks 名稱。如果您正在使用[部署多個環境](../../README.md#deploying-multiple-environments)功能，請將其替換為要遷移的環境名稱。如果沒有使用，則替換為空字串。

### 步驟2：更新儲存庫URL（建議）

儲存庫已從 `bedrock-claude-chat` 重新命名為 `bedrock-chat`。更新您的本地儲存庫：

```bash
# 檢查您目前的遠端URL
git remote -v

# 更新遠端URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# 驗證變更
git remote -v
```

### 步驟3：確保您使用的是最新的V2版本

> [!WARNING]
> 在遷移到V3之前，您必須更新到v2.10.0。**跳過此步驟可能會導致遷移過程中的資料遺失。**

在開始遷移之前，請確保您執行的是最新版本的V2（**v2.10.0**）。這可確保在升級到V3之前，您擁有所有必要的錯誤修復和改進：

```bash
# 取得最新標籤
git fetch --tags

# 切換到最新的V2版本
git checkout v2.10.0

# 部署最新的V2版本
cd cdk
npm ci
npx cdk deploy --all
```

### 步驟4：記錄您的V2 DynamoDB資料表名稱

從CloudFormation輸出中獲取V2 ConversationTable名稱：

```bash
# 獲取V2 ConversationTable名稱
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

請確保將此資料表名稱保存在安全的位置，因為稍後您將需要它來執行遷移腳本。

### 步驟5：備份您的DynamoDB資料表

在繼續之前，使用您剛才記錄的名稱創建DynamoDB ConversationTable的備份：

```bash
# 創建V2資料表的備份
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# 檢查備份狀態是否可用
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### 步驟6：刪除所有已發布的API

> [!IMPORTANT]
> 在部署V3之前，您必須刪除所有已發布的API，以避免在升級過程中出現Cloudformation輸出值衝突。

1. 以管理員身份登入您的應用程式
2. 導航到管理員部分並選擇"API管理"
3. 檢視所有已發布API的列表
4. 點擊每個API旁邊的刪除按鈕來刪除它

您可以在[PUBLISH_API.md](../PUBLISH_API_zh-TW.md)、[ADMINISTRATOR.md](../ADMINISTRATOR_zh-TW.md)文檔中找到更多關於API發布和管理的信息。

### 步驟7：拉取V3並部署

拉取最新的V3代碼並部署：

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> 一旦您部署V3，在完成遷移過程之前，所有用戶都將無法使用該應用程式。新的架構與舊的資料格式不相容，因此在完成下一步驟的遷移腳本之前，用戶將無法訪問他們的機器人或對話。

### 步驟8：記錄您的V3 DynamoDB資料表名稱

部署V3後，您需要獲取新的ConversationTable和BotTable名稱：

```bash
# 獲取V3 ConversationTable名稱
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# 獲取V3 BotTable名稱
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> 請確保將這些V3資料表名稱與您之前保存的V2資料表名稱一起保存，因為您將需要它們來執行遷移腳本。

### 步驟9：執行遷移腳本

遷移腳本將把您的V2資料轉換為V3架構。首先，編輯遷移腳本 `docs/migration/migrate_v2_v3.py` 來設置您的資料表名稱和區域：

```python
# DynamoDB所在的區域
REGION = "ap-northeast-1" # 替換為您的區域

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # 替換為您在步驟4中記錄的值
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # 替換為您在步驟8中記錄的值
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # 替換為您在步驟8中記錄的值
```

然後使用Poetry從後端目錄運行腳本：

> [!NOTE]
> Python需求版本已更改為3.13.0或更高版本（可能在未來開發中更改。請參見pyproject.toml）。如果您安裝了不同Python版本的venv，您需要先將其移除。

```bash
# 導航到後端目錄
cd backend

# 如果尚未安裝依賴項，請安裝
poetry install

# 首先運行乾跑以查看將要遷移的內容
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# 如果一切看起來都沒問題，執行實際遷移
poetry run python ../docs/migration/migrate_v2_v3.py

# 驗證遷移是否成功
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

遷移腳本將在您的當前目錄中生成一個報告文件，其中包含有關遷移過程的詳細信息。檢查此文件以確保所有資料都正確遷移。

#### 處理大量資料

對於有大量用戶或大量資料的環境，請考慮以下方法：

1. **單獨遷移用戶**：對於擁有大量資料的用戶，一次遷移一個：

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **記憶體考慮**：遷移過程會將資料載入記憶體。如果遇到記憶體不足（OOM）錯誤，請嘗試：

   - 一次遷移一個用戶
   - 在記憶體較大的機器上運行遷移
   - 將遷移分成較小的用戶批次

3. **監控遷移**：檢查生成的報告文件以確保所有資料都正確遷移，特別是對於大型資料集。

### 步驟10：驗證應用程式

遷移後，打開您的應用程式並驗證：

- 所有機器人都可用
- 對話已保留
- 新的權限控制正常運作

### 清理（可選）

在確認遷移成功且所有資料都能在V3中正確訪問後，您可以選擇刪除V2對話資料表以節省成本：

```bash
# 刪除V2對話資料表（僅在確認遷移成功後）
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> 只有在徹底驗證所有重要資料已成功遷移到V3後，才刪除V2資料表。即使您刪除了原始資料表，我們也建議在遷移後至少保留步驟2中創建的備份幾週時間。

## V3 常見問題

### 機器人存取與權限

**Q: 如果我正在使用的機器人被刪除或我的存取權限被移除會發生什麼事?**
A: 授權會在對話時進行檢查，所以你會立即失去存取權。

**Q: 如果使用者被刪除(例如:員工離職)會發生什麼事?**
A: 可以透過刪除 DynamoDB 中以其使用者 ID 為分區鍵(PK)的所有項目來完全移除其資料。

**Q: 我可以關閉必要公開機器人的分享功能嗎?**
A: 不行，管理員必須先將機器人標記為非必要才能關閉分享。

**Q: 我可以刪除必要公開機器人嗎?**
A: 不行，管理員必須先將機器人標記為非必要才能刪除。

### 安全性與實作

**Q: 機器人資料表是否實作了行級安全性(RLS)?**
A: 否，考慮到存取模式的多樣性。授權是在存取機器人時執行，相較於對話歷史，元數據洩漏的風險被認為是最小的。

**Q: 發布 API 有什麼要求?**
A: 機器人必須是公開的。

**Q: 是否會有所有私人機器人的管理畫面?**
A: 在初始 V3 版本中沒有。不過，仍可以根據需要透過使用者 ID 查詢來刪除項目。

**Q: 是否會有機器人標籤功能以改善搜尋體驗?**
A: 在初始 V3 版本中沒有，但未來更新可能會加入基於 LLM 的自動標籤功能。

### 管理

**Q: 管理員可以做什麼?**
A: 管理員可以:

- 管理公開機器人(包括檢查高成本機器人)
- 管理 API
- 將公開機器人標記為必要

**Q: 我可以將部分分享的機器人設為必要嗎?**
A: 不行，僅支援公開機器人。

**Q: 我可以設定釘選機器人的優先順序嗎?**
A: 在初始版本中不行。

### 授權設定

**Q: 如何設定授權?**
A:

1. 開啟 Amazon Cognito 控制台並在 BrChat 使用者池中建立使用者群組
2. 根據需要將使用者加入這些群組
3. 在 BrChat 中設定機器人分享設定時，選擇要允許存取的使用者群組

注意: 群組成員變更需要重新登入才能生效。變更會在 token 重新整理時反映，但在 ID token 有效期間內不會生效(V3 預設為 30 分鐘，可透過 `cdk.json` 或 `parameter.ts` 中的 `tokenValidMinutes` 設定)。

**Q: 系統是否會在每次存取機器人時都檢查 Cognito?**
A: 否，授權是使用 JWT token 進行檢查，以避免不必要的 I/O 操作。

### 搜尋功能

**Q: 機器人搜尋是否支援語意搜尋?**
A: 否，僅支援部分文字匹配。由於目前 OpenSearch Serverless 的限制(2025年3月)，不支援語意搜尋(例如: "automobile" → "car"、"EV"、"vehicle")。