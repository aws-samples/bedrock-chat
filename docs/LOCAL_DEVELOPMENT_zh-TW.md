# 本地開發

## 後端開發

請參閱 [backend/README](../backend/README_zh-TW.md)。

## 前端開發

在這個範例中，您可以在本地端修改並啟動前端，使用已通過 `npx cdk deploy` 部署的 AWS 資源（如 `API Gateway`、`Cognito` 等）。

1. 關於在 AWS 環境上的部署，請參考 [Deploy using CDK](../README.md#deploy-using-cdk)。
2. 複製 `frontend/.env.template` 並將其儲存為 `frontend/.env.local`。
3. 根據 `npx cdk deploy` 的輸出結果（例如 `BedrockChatStack.AuthUserPoolClientIdXXXXX`）填寫 `.env.local` 的內容。
4. 執行以下指令：

```zsh
cd frontend && npm ci && npm run dev
```

## (選擇性，建議) 設置 pre-commit hook

我們已經引入了用於類型檢查和程式碼檢查的 GitHub 工作流程。這些檢查會在建立 Pull Request 時執行，但是等待程式碼檢查完成才能繼續並不是一個良好的開發體驗。因此，這些檢查任務應該在提交階段自動執行。我們引入了 [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) 作為實現這一目標的機制。這不是強制性的，但我們建議採用它以獲得高效的開發體驗。此外，雖然我們不強制使用 [Prettier](https://prettier.io/) 來格式化 TypeScript，但在貢獻代碼時，如果您能採用它，我們將不勝感激，因為它有助於在程式碼審查期間避免不必要的差異。

### 安裝 lefthook

參考[這裡](https://github.com/evilmartians/lefthook#install)。如果您是 Mac 用戶並使用 homebrew，只需執行 `brew install lefthook`。

### 安裝 poetry

這是必需的，因為 Python 程式碼檢查依賴於 `mypy` 和 `black`。

```sh
cd backend
python3 -m venv .venv  # 選擇性 (如果你不想在你的環境中安裝 poetry)
source .venv/bin/activate  # 選擇性 (如果你不想在你的環境中安裝 poetry)
pip install poetry
poetry install
```

更多詳細信息，請查看 [backend README](../backend/README_zh-TW.md)。

### 建立 pre-commit hook

只需在此專案的根目錄執行 `lefthook install`。