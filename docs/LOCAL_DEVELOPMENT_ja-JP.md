# ローカル開発

## バックエンド開発

[backend/README](../backend/README_ja-JP.md) を参照してください。

## フロントエンド開発

このサンプルでは、`npx cdk deploy`でデプロイされた AWS リソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで修正および起動できます。

1. AWS 環境へのデプロイについては、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template` をコピーして、`frontend/.env.local` として保存します。
3. `.env.local` の内容を、`npx cdk deploy` の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## （オプション、推奨）pre-commitフックの設定

GitHub workflowsで型チェックとリンティングを導入しました。これらはプルリクエスト作成時に実行されますが、リンティングの完了を待つことは開発体験として良くありません。そのため、これらのリンティングタスクをコミット時に自動的に実行する必要があります。この目的のために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)を導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、[Prettier](https://prettier.io/)でTypeScriptのフォーマットを強制はしていませんが、コードレビュー時の不要な差分を防ぐため、貢献する際に採用していただけると幸いです。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。MacとHomebrewユーザーの場合は、`brew install lefthook`を実行するだけです。

### Poetryのインストール

これはPythonコードのリンティングが`mypy`と`black`に依存しているため必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細は[バックエンドのREADME](../backend/README_ja-JP.md)を確認してください。

### pre-commitフックの作成

プロジェクトのルートディレクトリで`lefthook install`を実行するだけです。