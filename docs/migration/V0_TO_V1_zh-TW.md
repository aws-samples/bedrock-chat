# 遷移指南（v0 到 v1）

如果您已經使用 Bedrock Chat 的舊版本（約 `0.4.x`），您需要按照以下步驟進行遷移。

## 為什麼需要這麼做？

此主要更新包含重要的安全性更新。

- 向量資料庫（即 Aurora PostgreSQL 上的 pgvector）儲存現已加密，這會在部署時觸發替換。這意味著現有的向量項目將被刪除。
- 我們引入了 `CreatingBotAllowed` Cognito 使用者群組，以限制可以建立機器人的使用者。目前現有的使用者不在此群組中，因此如果您希望他們具有建立機器人的能力，需要手動附加權限。請參閱：[機器人個人化](../../README.md#bot-personalization)

## 先決條件

閱讀 [資料庫遷移指南](./DATABASE_MIGRATION_zh-TW.md) 並確定還原項目的方法。

## 步驟

### 向量存儲遷移

- 打開終端機並導航到專案目錄
- 拉取您想要部署的分支。以下是切換到所需分支（在本例中為 `v1`）並拉取最新更改：

```sh
git fetch
git checkout v1
git pull origin v1
```

- 如果您希望使用 DMS 還原項目，請務必禁用密碼輪換並記下訪問資料庫的密碼。如果使用遷移腳本（[migrate_v0_v1.py](./migrate_v0_v1.py)），則無需記下密碼。
- 刪除所有[已發布的 API](../PUBLISH_API_zh-TW.md)，以便 CloudFormation 可以刪除現有的 Aurora 叢集。
- 運行 [npx cdk deploy](../README.md#deploy-using-cdk) 觸發 Aurora 叢集替換並刪除所有向量項目。
- 按照[資料庫遷移指南](./DATABASE_MIGRATION_zh-TW.md)還原向量項目。
- 驗證用戶是否可以使用現有的具有知識的機器人，即 RAG 機器人。

### 附加 CreatingBotAllowed 權限

- 部署後，所有用戶將無法創建新的機器人。
- 如果您希望特定用戶能夠創建機器人，請使用管理控制台或 CLI 將這些用戶添加到 `CreatingBotAllowed` 群組。
- 驗證用戶是否可以創建機器人。請注意，用戶需要重新登入。