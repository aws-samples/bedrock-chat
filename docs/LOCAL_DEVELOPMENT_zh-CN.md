# 本地开发

## 后端开发

请查看 [backend/README](../backend/README_zh-CN.md)。

## 前端开发

在此示例中，您可以在本地修改和启动前端，使用通过 `npx cdk deploy` 部署的 AWS 资源（`API Gateway`、`Cognito` 等）。

1. 关于在 AWS 环境中的部署，请参考 [使用 CDK 部署](../README.md#deploy-using-cdk)。
2. 复制 `frontend/.env.template` 并将其保存为 `frontend/.env.local`。
3. 根据 `npx cdk deploy` 的输出结果（如 `BedrockChatStack.AuthUserPoolClientIdXXXXX`）填写 `.env.local` 的内容。
4. 执行以下命令：

```zsh
cd frontend && npm ci && npm run dev
```

## (可选，推荐) 设置 pre-commit hook

我们已经引入了用于类型检查和代码检查的 GitHub 工作流。这些检查会在创建 Pull Request 时执行，但等待代码检查完成才能继续并不是一个良好的开发体验。因此，这些代码检查任务应该在提交阶段自动执行。我们引入了 [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) 作为实现这一目标的机制。这不是强制性的，但我们建议采用它以获得高效的开发体验。此外，虽然我们不强制使用 [Prettier](https://prettier.io/) 来格式化 TypeScript，但如果您在贡献代码时能采用它，我们将不胜感激，因为它有助于在代码审查期间避免不必要的差异。

### 安装 lefthook

参考[这里](https://github.com/evilmartians/lefthook#install)。如果您是 Mac 用户并使用 homebrew，只需运行 `brew install lefthook`。

### 安装 poetry

这是必需的，因为 Python 代码检查依赖于 `mypy` 和 `black`。

```sh
cd backend
python3 -m venv .venv  # 可选（如果您不想在环境中安装 poetry）
source .venv/bin/activate  # 可选（如果您不想在环境中安装 poetry）
pip install poetry
poetry install
```

更多详细信息，请查看 [backend README](../backend/README_zh-CN.md)。

### 创建 pre-commit hook

只需在项目的根目录运行 `lefthook install`。