# ローカル開発

## バックエンド開発

[backend/README](../backend/README_ja-JP.md) を参照してください。

## フロントエンド開発

このサンプルでは、`npx cdk deploy`でデプロイされた AWS リソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで変更および起動できます。

1. AWS 環境へのデプロイについては、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template` をコピーし、`frontend/.env.local` として保存します。
3. `.env.local` の内容を `npx cdk deploy` の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX` など）に基づいて入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## （オプション、推奨）プレコミットフックのセットアップ

型チェックとリンティングのためのGitHubワークフローを導入しました。これらはプルリクエスト作成時に実行されますが、リンティングの完了を待つことは良い開発体験ではありません。そのため、これらのリンティングタスクはコミット段階で自動的に実行されるべきです。効率的な開発体験を実現するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)をメカニズムとして導入しました。必須ではありませんが、採用をお勧めします。また、[Prettier](https://prettier.io/)でTypeScriptのフォーマットを強制はしていませんが、コードレビュー時の不要な差分を防ぐため、貢献する際に採用していただければ幸いです。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。MacとHomebrewユーザーの場合、`brew install lefthook`を実行するだけです。

### Poetryのインストール

Pythonコードのリンティングが`mypy`と`black`に依存するため、これが必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（環境にPoetryをインストールしたくない場合）
source .venv/bin/activate  # オプション（環境にPoetryをインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_ja-JP.md)を確認してください。

### プレコミットフックの作成

プロジェクトのルートディレクトリで`lefthook install`を実行するだけです。