# 遷移指南 (v0 至 v1)

如果您已經在使用舊版本的 Bedrock Chat (~`0.4.x`)，您需要遵循以下步驟進行遷移。

## 為什麼需要執行這個操作？

這個重大更新包含了重要的安全性更新。

- 向量資料庫（即 Aurora PostgreSQL 上的 pgvector）的儲存現在已加密，這會在部署時觸發替換。這意味著現有的向量項目將被刪除。
- 我們引入了 `CreatingBotAllowed` Cognito 使用者群組來限制可以建立機器人的使用者。目前的現有使用者並不在此群組中，因此如果您希望他們具有建立機器人的功能，您需要手動附加權限。參見：[Bot Personalization](../../README.md#bot-personalization)

## 先決條件

閱讀[資料庫遷移指南](./DATABASE_MIGRATION_zh-TW.md)並確定還原項目的方法。

## 步驟

### 向量儲存遷移

- 開啟終端機並導航至專案目錄
- 拉取您要部署的分支。以下是切換到目標分支(此例中為 `v1`)並拉取最新變更：

```sh
git fetch
git checkout v1
git pull origin v1
```

- 如果您想要使用 DMS 還原項目，切記要停用密碼輪換並記下存取資料庫的密碼。如果使用遷移腳本([migrate_v0_v1.py](./migrate_v0_v1.py))進行還原，則不需要記下密碼。
- 移除所有[已發布的 API](../PUBLISH_API_zh-TW.md)，以便 CloudFormation 可以移除現有的 Aurora 叢集。
- 執行 [npx cdk deploy](../README.md#deploy-using-cdk) 會觸發 Aurora 叢集替換並刪除所有向量項目。
- 按照[資料庫遷移指南](./DATABASE_MIGRATION_zh-TW.md)還原向量項目。
- 驗證使用者是否可以使用現有的具有知識庫的機器人，例如 RAG 機器人。

### 附加 CreatingBotAllowed 權限

- 部署後，所有使用者將無法建立新的機器人。
- 如果您想要特定使用者能夠建立機器人，請使用管理控制台或 CLI 將這些使用者加入 `CreatingBotAllowed` 群組。
- 驗證使用者是否可以建立機器人。請注意，使用者需要重新登入。