# 遷移指南（v2 至 v3）

## 摘要

- V3 引入了細粒度的權限控制和機器人商店功能，需要 DynamoDB 架構變更
- **在遷移前備份您的 DynamoDB ConversationTable**
- 將您的倉庫 URL 從 `bedrock-claude-chat` 更新至 `bedrock-chat`
- 執行遷移腳本以將資料轉換為新架構
- 所有您的機器人和對話將在新的權限模型下保留
- **重要：在遷移過程中，應用程式將對所有用戶不可用，直到遷移完成。此過程通常需要約 60 分鐘，具體取決於資料量和開發環境的性能。**
- **重要：所有已發布的 API 必須在遷移過程中刪除。**
- **警告：遷移過程無法保證所有機器人 100% 成功。請在遷移前記錄您重要的機器人配置，以防需要手動重新建立。**

## 簡介

### V3 的新功能

V3 為 Bedrock Chat 引入了重大增強：

1. **細粒度權限控制**：使用基於用戶群組的權限控制對您的機器人的存取
2. **機器人商店**：通過集中的市場共享和發現機器人
3. **管理功能**：管理 API、標記機器人為必要，並分析機器人使用情況

這些新功能需要對 DynamoDB 架構進行更改，因此需要現有用戶進行遷移過程。

### 為什麼需要這次遷移

新的權限模型和機器人商店功能需要重新構建機器人資料的儲存和存取方式。遷移過程將轉換您現有的機器人和對話到新架構，同時保留所有資料。

> [!WARNING]
> 服務中斷通知：**在遷移過程中，應用程式將對所有用戶不可用。**請計劃在用戶不需要存取系統的維護時段執行此遷移。應用程式只有在遷移腳本成功完成並且所有資料已正確轉換為新架構後才會重新可用。此過程通常需要大約 60 分鐘，具體取決於資料量和開發環境的效能。

> [!IMPORTANT]
> 在繼續遷移之前：**遷移過程無法保證所有機器人 100% 成功**，尤其是使用舊版本或自定義配置創建的機器人。請在開始遷移過程之前記錄您重要的機器人配置（指令、知識來源、設置），以防需要手動重新創建。

## 遷移流程

### 關於 V3 中機器人可見性的重要通知

在 V3 中，**所有啟用公開分享的 V2 機器人都將可在機器人商店中搜尋到。** 如果您有包含敏感資訊且不希望被發現的機器人，請考慮在遷移至 V3 之前將其設為私密。

### 步驟 1：識別您的環境名稱

在此程序中，`{YOUR_ENV_PREFIX}` 用於識別 CloudFormation Stacks 的名稱。如果您正在使用[部署多個環境](../../README.md#deploying-multiple-environments)功能，請將其替換為要遷移的環境名稱。如果沒有，請替換為空字串。

### 步驟 2：更新儲存庫 URL（建議）

儲存庫已從 `bedrock-claude-chat` 重新命名為 `bedrock-chat`。更新您的本機儲存庫：

```bash
# 檢查您目前的遠端 URL
git remote -v

# 更新遠端 URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# 驗證變更
git remote -v
```

### 步驟 3：確保您使用最新的 V2 版本

> [!WARNING]
> 您必須在遷移到 V3 之前更新到 v2.10.0。**跳過此步驟可能導致遷移期間資料遺失。**

在開始遷移之前，請確保您正在運行 V2 的最新版本（**v2.10.0**）。這確保在升級到 V3 之前，您已擁有所有必要的錯誤修復和改進：

```bash
# 取得最新的標籤
git fetch --tags

# 檢出最新的 V2 版本
git checkout v2.10.0

# 部署最新的 V2 版本
cd cdk
npm ci
npx cdk deploy --all
```

### 步驟 4：記錄您的 V2 DynamoDB 表名稱

從 CloudFormation 輸出中取得 V2 ConversationTable 名稱：

```bash
# 取得 V2 ConversationTable 名稱
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

請確保將此表名稱安全地保存，因為您稍後將在遷移腳本中需要它。

### 步驟 5：備份您的 DynamoDB 表

在繼續之前，使用您剛記錄的名稱建立 DynamoDB ConversationTable 的備份：

```bash
# 建立 V2 表的備份
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

### 步驟 6：刪除所有已發布的 API

> [!IMPORTANT]
> 在部署 V3 之前，您必須刪除所有已發布的 API，以避免 Cloudformation 輸出值在升級過程中衝突。

1. 以管理員身份登入您的應用程式
2. 導覽至管理員區段並選擇「API 管理」
3. 檢查所有已發布 API 的清單
4. 通過點擊每個 API 旁邊的刪除按鈕來刪除每個已發布的 API

您可以在 [PUBLISH_API.md](../PUBLISH_API_zh-TW.md)、[ADMINISTRATOR.md](../ADMINISTRATOR_zh-TW.md) 文件中找到更多關於 API 發布和管理的資訊。

### 步驟 7：拉取 V3 並部署

拉取最新的 V3 代碼並部署：

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> 部署 V3 後，在遷移過程完成之前，應用程式將對所有用戶不可用。新架構與舊資料格式不相容，因此用戶將無法訪問其機器人或對話，直到您完成下一步的遷移腳本。

### 步驟 8：記錄您的 V3 DynamoDB 表名稱

部署 V3 後，您需要取得新的 ConversationTable 和 BotTable 名稱：

```bash
# 取得 V3 ConversationTable 名稱
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# 取得 V3 BotTable 名稱
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> 請確保與先前保存的 V2 表名稱一起保存這些 V3 表名稱，因為您將在遷移腳本中需要所有這些名稱。

### 步驟 9：運行遷移腳本

遷移腳本將把您的 V2 資料轉換為 V3 架構。首先，編輯遷移腳本 `docs/migration/migrate_v2_v3.py` 以設置您的表名稱和區域：

```python
# DynamoDB 所在的區域
REGION = "ap-northeast-1" # 替換為您的區域

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # 替換為您在步驟 4 記錄的值
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # 替換為您在步驟 8 記錄的值
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # 替換為您在步驟 8 記錄的值
```

然後從後端目錄使用 Poetry 運行腳本：

> [!NOTE]
> Python 需求版本已更改為 3.13.0 或更高版本（可能在未來開發中更改。請參見 pyproject.toml）。如果您已使用不同的 Python 版本安裝了 venv，則需要先將其刪除。

```bash
# 導覽至後端目錄
cd backend

# 如果尚未安裝依賴項，請安裝
poetry install

# 首先進行試運行，查看將遷移的內容
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# 如果一切看起來正常，運行實際遷移
poetry run python ../docs/migration/migrate_v2_v3.py

# 驗證遷移是否成功
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

遷移腳本將在您目前的目錄中生成一個報告文件，其中包含遷移過程的詳細資訊。檢查此文件以確保所有資料已正確遷移。

#### 處理大量資料

對於有大量用戶或大量資料的環境，考慮以下方法：

1. **逐個用戶遷移**：對於資料量大的用戶，逐個遷移：

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **記憶體考慮**：遷移過程會將資料載入記憶體。如果遇到記憶體不足（OOM）錯誤，請嘗試：

   - 逐個用戶遷移
   - 在記憶體更大的機器上運行遷移
   - 將遷移分成較小的用戶批次

3. **監控遷移**：檢查生成的報告文件，確保所有資料（特別是大型資料集）都已正確遷移。

### 步驟 10：驗證應用程式

遷移後，打開您的應用程式並驗證：

- 所有機器人都可用
- 對話已保留
- 新的權限控制正常工作

### 清理（可選）

在確認遷移成功且所有資料在 V3 中正確可訪問後，您可以選擇刪除 V2 對話表以節省成本：

```bash
# 刪除 V2 對話表（僅在確認成功遷移後）
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> 僅在徹底驗證所有重要資料已成功遷移到 V3 後才刪除 V2 表。即使刪除原始表，我們建議在遷移後至少保留幾週的備份。

## V3 常見問題集

### 機器人存取和權限

**Q: 如果我正在使用的機器人被刪除或我的存取權限被移除會發生什麼事？**
A: 授權會在聊天時被檢查，所以您將立即失去存取權限。

**Q: 如果使用者被刪除（例如，員工離職）會發生什麼事？**
A: 可以通過刪除 DynamoDB 中以使用者 ID 作為分割鍵 (PK) 的所有項目來完全移除其資料。

**Q: 我可以關閉重要公開機器人的共享功能嗎？**
A: 不可以，管理員必須先將機器人標記為非重要，才能關閉共享。

**Q: 我可以刪除重要公開機器人嗎？**
A: 不可以，管理員必須先將機器人標記為非重要，才能刪除它。

### 安全性和實作

**Q: 機器人表格是否實作了資料列級安全性 (RLS)？**
A: 否，考慮到存取模式的多樣性。存取機器人時會執行授權，與對話歷史記錄相比，元資料洩露的風險被認為是最小的。

**Q: 發佈 API 的要求是什麼？**
A: 機器人必須是公開的。

**Q: 是否會有管理所有私人機器人的畫面？**
A: 在初始的 V3 版本中不會。但是，仍然可以根據需要通過查詢使用者 ID 來刪除項目。

**Q: 是否會有機器人標記功能以改善搜尋使用者體驗？**
A: 在初始的 V3 版本中不會，但未來更新可能會新增基於 LLM 的自動標記。

### 管理

**Q: 管理員可以做什麼？**
A: 管理員可以：

- 管理公開機器人（包括檢查高成本機器人）
- 管理 API
- 將公開機器人標記為重要

**Q: 我可以將部分共享的機器人標記為重要嗎？**
A: 不可以，僅支援公開機器人。

**Q: 我可以為置頂機器人設定優先順序嗎？**
A: 在初始版本中，不可以。

### 授權設定

**Q: 如何設定授權？**
A:

1. 開啟 Amazon Cognito 控制台，在 BrChat 使用者池中建立使用者群組
2. 根據需要將使用者新增到這些群組
3. 在 BrChat 中，設定機器人共享設定時，選擇要允許存取的使用者群組

注意：群組成員資格變更需要重新登入才能生效。變更會在權杖重新整理時反映，但在 ID 權杖有效期間（V3 中預設為 30 分鐘，可在 `cdk.json` 或 `parameter.ts` 中透過 `tokenValidMinutes` 進行配置）內不會立即生效。

**Q: 系統是否每次存取機器人時都會檢查 Cognito？**
A: 否，授權是使用 JWT 權杖檢查，以避免不必要的 I/O 作業。

### 搜尋功能

**Q: 機器人搜尋是否支援語義搜尋？**
A: 不支援，僅支援部分文字匹配。由於目前 OpenSearch Serverless 的限制（2025 年 3 月），不支援語義搜尋（例如，"automobile" → "car"、"EV"、"vehicle"）。