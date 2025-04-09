# 本地開發

## 後端開發

請參閱 [backend/README](../backend/README_zh-TW.md)。

## 前端開發

在此範例中，您可以使用已透過 `npx cdk deploy` 部署的 AWS 資源（`API Gateway`、`Cognito` 等）在本機修改和啟動前端。

1. 參考 [使用 CDK 部署](../README.md#deploy-using-cdk) 以在 AWS 環境中部署。
2. 複製 `frontend/.env.template` 並儲存為 `frontend/.env.local`。
3. 根據 `npx cdk deploy` 的輸出結果（例如 `BedrockChatStack.AuthUserPoolClientIdXXXXX`）填寫 `.env.local` 的內容。
4. 執行以下指令：

```zsh
cd frontend && npm ci && npm run dev
```

## （可選，建議）設置預提交掛鉤

我們引入了用於類型檢查和程式碼風格檢查的 GitHub 工作流程。這些工作流程在建立 Pull Request 時執行，但等待程式碼風格檢查完成再繼續並不是一個好的開發體驗。因此，這些程式碼風格檢查任務應在提交階段自動執行。我們引入了 [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) 作為實現這一目標的機制。這不是強制性的，但我們建議採用它以獲得高效的開發體驗。另外，雖然我們不強制使用 [Prettier](https://prettier.io/) 進行 TypeScript 格式化，但我們希望您在貢獻時能採用它，因為這有助於防止代碼審查時出現不必要的差異。

### 安裝 lefthook

請參考[此處](https://github.com/evilmartians/lefthook#install)。如果您是 Mac 並使用 Homebrew，只需運行 `brew install lefthook`。

### 安裝 poetry

這是必需的，因為 Python 代碼的程式碼風格檢查依賴於 `mypy` 和 `black`。

```sh
cd backend
python3 -m venv .venv  # 可選（如果您不想在環境中安裝 poetry）
source .venv/bin/activate  # 可選（如果您不想在環境中安裝 poetry）
pip install poetry
poetry install
```

更多詳細信息，請查看 [backend README](../backend/README_zh-TW.md)。

### 建立預提交掛鉤

只需在此項目的根目錄運行 `lefthook install`。