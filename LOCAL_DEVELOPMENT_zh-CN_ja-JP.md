# ローカル開発

## バックエンド開発

[backend/README](../backend/README_zh-CN_ja-JP.md) を参照してください。

## フロントエンド開発

この例では、`npx cdk deploy` でデプロイされた AWS リソース（`API Gateway`、`Cognito` など）をローカルで変更および起動できます。

1. [CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照して、AWS環境にデプロイします。
2. `frontend/.env.template` をコピーし、`frontend/.env.local` として保存します。
3. `npx cdk deploy` の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX` など）に基づいて、`.env.local` の内容を入力します。
4. 以下のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## （可选，推荐）プレコミットフックの設定

私たちは型チェックとコードスタイルチェックのための GitHub ワークフローを導入しました。これらのワークフローはプルリクエスト作成時に実行されますが、コードスタイルチェックの完了を待つことは良い開発体験ではありません。そのため、これらのコードスタイルチェックタスクはコミット段階で自動的に実行されるべきです。この目的を達成するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) を導入しました。これは必須ではありませんが、効率的な開発体験を得るためにお勧めします。また、[Prettier](https://prettier.io/) を使用して TypeScript をフォーマットすることは強制していませんが、コード審査時の不要な差分を防ぐため、コントリビュート時に採用することをお勧めします。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。Macで Homebrew を使用している場合は、`brew install lefthook` を実行するだけです。

### Poetryのインストール

Python コードのコードスタイルチェックが `mypy` と `black` に依存しているため、これは必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（環境に poetry をインストールしたくない場合）
source .venv/bin/activate  # オプション（環境に poetry をインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_zh-CN_ja-JP.md)を参照してください。

### プレコミットフックの作成

プロジェクトのルートディレクトリで `lefthook install` を実行するだけです。