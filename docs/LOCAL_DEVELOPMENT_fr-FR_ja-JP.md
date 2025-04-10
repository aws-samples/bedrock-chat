# ローカル開発

## バックエンド開発

[backend/README](../backend/README_fr-FR_ja-JP.md) を参照してください。

## フロントエンド開発

この例では、`npx cdk deploy`でデプロイされたAWSリソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで変更および起動できます。

1. AWS環境へのデプロイについては、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーし、`frontend/.env.local`として保存します。
3. `.env.local`の内容を`npx cdk deploy`の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) pre-commitフックの設定

GitHub workflowsを型チェックとリンティングのために導入しました。これらはPull Requestの作成時に実行されますが、リンティングが完了するまで待つことは開発体験として良くありません。そのため、これらのリンティングタスクはコミット段階で自動的に実行される必要があります。これを実現するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)をメカニズムとして導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、[Prettier](https://prettier.io/)でTypeScriptのフォーマッティングを適用していませんが、コード レビュー時の不要な差分を防ぐため、貢献する際にPrettierを採用していただければ幸いです。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。Homebrewを使用しているMacの場合は、単に`brew install lefthook`を実行してください。

### Poetryのインストール

これは、Python コードのリンティングが `mypy` と `black` に依存しているため必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_fr-FR_ja-JP.md)を参照してください。

### pre-commitフックの作成

プロジェクトのルートディレクトリで単に `lefthook install` を実行してください。