# ローカル開発

## バックエンド開発

[backend/README](../backend/README_pl-PL_ja-JP.md) を確認してください。

## フロントエンド開発

この例では、`npx cdk deploy`でデプロイされたAWSリソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで変更および実行できます。

1. AWS環境にデプロイするには、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`ファイルをコピーし、`frontend/.env.local`として保存します。
3. `npx cdk deploy`の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて、`.env.local`の内容を入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) pre-commitフックの設定

GitHub workflowsを使用して型チェックとリンティングを行っています。これらはPull Request作成時に実行されますが、リンティングの完了を待つことは開発者体験として良くありません。そのため、これらのリンティングタスクはコミット時に自動的に実行されるべきです。この目的のために[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)を導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、TypeScriptの[Prettier](https://prettier.io/)によるフォーマットを強制はしていませんが、コードレビュー時の不要な差分を防ぐため、使用していただけると幸いです。

### Lefthookをインストールする

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。MacとHomebrewを使用している場合は、単に`brew install lefthook`を実行してください。

### poetryをインストールする

Python コードのリンティングが `mypy` と `black` に依存しているため、これが必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを独自の環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを独自の環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_pl-PL_ja-JP.md)を確認してください。

### pre-commitフックを作成する

プロジェクトのルートディレクトリで`lefthook install`を実行するだけです。