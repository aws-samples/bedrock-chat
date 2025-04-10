# ローカル開発

## バックエンド開発

[バックエンド/README](../backend/README_nb-NO_ja-JP.md) を参照してください。

## フロントエンド開発

この例では、`npx cdk deploy`でデプロイされたAWSリソース（`API Gateway`、`Cognito`など）を使用して、ローカルでフロントエンドを変更および起動できます。

1. AWS環境へのデプロイは[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーし、`frontend/.env.local`として保存します。
3. `.env.local`の内容を`npx cdk deploy`の結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) pre-commitフックの設定

GitHub ワークフローを型チェックとリンティングのために導入しました。これらは Pull Request 作成時に実行されますが、リンティングの完了を待つ開発体験は良くありません。そのため、これらのリンティングタスクをコミット段階で自動的に実行する必要があります。これを実現するために [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) を導入しました。必須ではありませんが、効率的な開発体験のために使用することをお勧めします。また、[Prettier](https://prettier.io/) で TypeScript のフォーマットを強制していませんが、コードレビュー時の不要な差分を防ぐため、貢献する際に使用していただけると幸いです。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。MacユーザーでHomebrewを使用している場合は、単に `brew install lefthook` を実行してください。

### Poetryのインストール

これは、Pythonコードのリンティングが `mypy` と `black` に依存しているためです。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドREADME](../backend/README_nb-NO_ja-JP.md)を参照してください。

### pre-commitフックの作成

プロジェクトのルートディレクトリで単に `lefthook install` を実行してください。