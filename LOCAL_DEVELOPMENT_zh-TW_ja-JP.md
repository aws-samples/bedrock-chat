# ローカル開発

## バックエンド開発

[backend/README](../backend/README_zh-TW_ja-JP.md) を参照してください。

## Frontend Development

In this example, you can modify and start the frontend locally using AWS resources (`API Gateway`, `Cognito`, etc.) that have been deployed via `npx cdk deploy`.

1. Refer to [Deploy Using CDK](../README.md#deploy-using-cdk) to deploy in the AWS environment.
2. Copy `frontend/.env.template` and save it as `frontend/.env.local`.
3. Fill in the contents of `.env.local` based on the output of `npx cdk deploy` (such as `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Run the following command:

```zsh
cd frontend && npm ci && npm run dev
```

## （可選，建議）プリコミットフックの設定

GitHub ワークフローを使用して型チェックとコードスタイルチェックを導入しました。これらのワークフローはプルリクエスト作成時に実行されますが、コードスタイルチェックの完了を待つのは良い開発体験ではありません。そのため、これらのコードスタイルチェックタスクはコミット段階で自動的に実行される必要があります。この目的を達成するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) を導入しました。これは必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、[Prettier](https://prettier.io/) を使用した TypeScript のフォーマットは強制していませんが、コード審査時の不要な差分を防ぐため、貢献する際に採用することを希望しています。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。Macで Homebrew を使用している場合は、`brew install lefthook` を実行するだけです。

### Poetryのインストール

Python コードのコードスタイルチェックは `mypy` と `black` に依存しているため、これが必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_zh-TW_ja-JP.md) を参照してください。

### プリコミットフックの作成

プロジェクトのルートディレクトリで `lefthook install` を実行するだけです。