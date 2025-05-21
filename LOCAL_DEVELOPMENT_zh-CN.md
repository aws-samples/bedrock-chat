# 本地开发

## 后端开发

查看 [backend/README](../backend/README_zh-CN.md)。

## 前端开发

在此示例中，您可以使用已通过 `npx cdk deploy` 部署的 AWS 资源（`API Gateway`、`Cognito` 等）在本地修改和启动前端。

1. 参考 [使用 CDK 部署](../README.md#deploy-using-cdk) 以在 AWS 环境中部署。
2. 复制 `frontend/.env.template` 并将其保存为 `frontend/.env.local`。
3. 根据 `npx cdk deploy` 的输出结果（如 `BedrockChatStack.AuthUserPoolClientIdXXXXX`）填写 `.env.local` 的内容。
4. 执行以下命令：

```zsh
cd frontend && npm ci && npm run dev
```

## （可选，推荐）设置预提交钩子

我们引入了用于类型检查和代码风格检查的 GitHub 工作流。这些工作流在创建 Pull Request 时执行，但等待代码风格检查完成后再继续并不是一个好的开发体验。因此，这些代码风格检查任务应在提交阶段自动执行。我们引入了 [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) 作为实现这一目标的机制。这不是强制性的，但我们建议采用它以获得高效的开发体验。此外，虽然我们不强制使用 [Prettier](https://prettier.io/) 进行 TypeScript 格式化，但我们希望你在贡献代码时能够采用它，因为这有助于防止代码审查时出现不必要的差异。

### 安装 Lefthook

请参考[此处](https://github.com/evilmartians/lefthook#install)。如果你是 Mac 并使用 Homebrew，只需运行 `brew install lefthook`。

### 安装 Poetry

这是必需的，因为 Python 代码风格检查依赖于 `mypy` 和 `black`。

```sh
cd backend
python3 -m venv .venv  # 可选（如果你不想在环境中安装 poetry）
source .venv/bin/activate  # 可选（如果你不想在环境中安装 poetry）
pip install poetry
poetry install
```

更多详细信息，请查看 [backend README](../backend/README_zh-CN.md)。

### 创建预提交钩子

只需在项目根目录运行 `lefthook install`。