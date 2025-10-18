# ローカル開発

## バックエンド開発

[backend/README](../backend/README_ja-JP.md)をご覧ください。

## フロントエンド開発

このサンプルでは、`npx cdk deploy`でデプロイされたAWSリソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで変更・起動することができます。

1. AWSの環境へのデプロイについては、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーして、`frontend/.env.local`として保存します。
3. `npx cdk deploy`の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて、`.env.local`の内容を入力します。
4. 以下のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) プリコミットフックの設定

型チェックとリンティングのためのGitHubワークフローを導入しています。これらはプルリクエストの作成時に実行されますが、リンティングの完了を待ってから作業を進めるのは良い開発体験とは言えません。そのため、これらのリンティングタスクはコミット段階で自動的に実行されるべきです。この仕組みを実現するために[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)を導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、TypeScriptのフォーマットを[Prettier](https://prettier.io/)で強制はしていませんが、コードレビュー時の不要な差分を防ぐため、コントリビューション時に採用していただけると幸いです。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。MacでHomebrewを使用している場合は、`brew install lefthook`を実行するだけです。

### Poetryのインストール

Pythonコードのリンティングが`mypy`と`black`に依存しているため、これが必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（環境にpoetryをインストールしたくない場合）
source .venv/bin/activate  # オプション（環境にpoetryをインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_ja-JP.md)をご確認ください。

### プリコミットフックの作成

このプロジェクトのルートディレクトリで`lefthook install`を実行するだけです。