# 地域開発

## バックエンド開発

[backend/README](../backend/README_ms-MY_ja-JP.md) を参照してください。

## フロントエンド開発

この例では、`npx cdk deploy`で使用されたAWSリソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで変更および起動できます。

1. AWS環境で使用するには、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーし、`frontend/.env.local`として保存します。
3. `.env.local`の内容を`npx cdk deploy`の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (推奨オプション) プレコミットフックを準備する

私たちはコードの種類を確認し、レビューするGitHubワークフローを導入しました。これはプルリクエストが作成されたときに行われますが、レビューの完了を待つ開発体験は良くありません。そのため、このレビュータスクは自動的にコミット時に行われるべきです。私たちは[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)をこれを達成するためのメカニズムとして導入しました。これは必須ではありませんが、効率的な開発体験のために使用することをお勧めします。さらに、TypeScriptの自動フォーマットを[Prettier](https://prettier.io/)で強制していませんが、不要な差分を防ぐために貢献する際に使用していただければ幸いです。

### Lefthookをインストールする

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。macとHomebrewのユーザーの場合は、`brew install lefthook`を実行するだけです。

### Poetryをインストールする

これはPythonコードのレビューが`mypy`と`black`に依存しているために必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_ms-MY_ja-JP.md)を確認してください。

### プレコミットフックを作成する

プロジェクトのルートディレクトリで`lefthook install`を実行するだけです。