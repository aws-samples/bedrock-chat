# ローカル開発

## バックエンド開発

[backend/README](../backend/README_vi-VN_ja-JP.md) を参照してください。

## フロントエンドの開発

このテンプレートでは、`npx cdk deploy`でデプロイされたAWSリソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで変更および起動できます。

1. AWS環境にデプロイするには、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーして`frontend/.env.local`として保存します。
3. `.env.local`の内容を`npx cdk deploy`の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて入力します。
4. 以下のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) pre-commitフックの設定

GitHub workflowsを使用してスタイルチェックとエラーチェックを導入しました。これらのチェックはPull Requestが作成されたときに実行されますが、エラーチェックの完了を待つ必要があるのは良い開発体験ではありません。そのため、これらのエラーチェックタスクはコミット時に自動的に実行されるべきです。この目的のために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)を導入しました。これは必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、[Prettier](https://prettier.io/)でTypeScriptの書式を強制はしていませんが、コントリビュートする際に適用していただけると、不要な差分を防ぐことができるため、大変感謝します。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。Macとhomebrewユーザーの場合は、`brew install lefthook`を実行するだけです。

### Poetryのインストール

これは、Python コードのエラーチェックが `mypy` と `black` に依存しているため必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを自分の環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを自分の環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[backendのREADME](../backend/README_vi-VN_ja-JP.md)を確認してください。

### pre-commitフックの作成

プロジェクトのルートディレクトリで `lefthook install` を実行するだけです。