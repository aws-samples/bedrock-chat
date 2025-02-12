# ローカル開発

## バックエンド開発

[backend/README](../backend/README.md) を参照してください。

## フロントエンド開発

このサンプルでは、`npx cdk deploy` でデプロイされた AWS リソース（`API Gateway`、`Cognito` など）を使用して、フロントエンドをローカルで変更および起動できます。

1. AWS 環境へのデプロイは [CDK を使用したデプロイ](../README.md#deploy-using-cdk) を参照してください。
2. `frontend/.env.template` をコピーし、`frontend/.env.local` として保存します。
3. `npx cdk deploy` の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX` など）に基づいて、`.env.local` の内容を入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## （オプション、推奨）プレコミットフックの設定

型チェックとリンティングのための GitHub ワークフローを導入しています。これらは Pull Request 作成時に実行されますが、リンティングの完了を待つことは良い開発体験ではありません。そのため、これらのリンティングタスクをコミット時に自動的に実行する必要があります。この目的を達成するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) を導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、[Prettier](https://prettier.io/) で TypeScript のフォーマットを強制していませんが、コードレビュー時の不要な差分を防ぐため、貢献する際に採用していただければ幸いです。

### Lefthook のインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。Mac と Homebrew ユーザーの場合は、`brew install lefthook` を実行するだけです。

### Poetry のインストール

これは、Python コードのリンティングが `mypy` と `black` に依存しているために必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（システムに poetry をインストールしたくない場合）
source .venv/bin/activate  # オプション（システムに poetry をインストールしたくない場合）
pip install poetry
poetry install
```

詳細は [バックエンド README](../backend/README.md) を確認してください。

### プレコミットフックの作成

プロジェクトのルートディレクトリで `lefthook install` を実行するだけです。