# ローカル開発

## バックエンド開発

[backend/README](../backend/README_ko-KR_ja-JP.md)を参照してください。

## フロントエンド開発

このサンプルでは、`npx cdk deploy`でデプロイされたAWSリソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで修正および実行できます。

1. AWS環境にデプロイするには、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーして`frontend/.env.local`として保存します。
3. `npx cdk deploy`の出力結果（例：`BedrockChatStack.AuthUserPoolClientIdXXXXX`）に基づいて、`.env.local`の内容を入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) プレコミットフックの設定

GitHub ワークフローで型チェックとリンティングを導入しました。これはプルリクエストが作成されたときに実行されますが、リンティングが完了するまで待つのは良い開発体験ではありません。そのため、これらのリンティングタスクはコミット段階で自動的に実行される必要があります。これには [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) をメカニズムとして導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、[Prettier](https://prettier.io/) で TypeScript のフォーマットを強制はしませんが、コードレビュー中の不要な差分を防ぐため、貢献する際に採用していただくことをお願いします。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。MacとHomebrewユーザーの場合は、`brew install lefthook` を実行してください。

### Poetryのインストール

Python コードのリンティングが `mypy` と `black` に依存しているため、必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細は [バックエンドREADME](../backend/README_ko-KR_ja-JP.md) を確認してください。

### プレコミットフックの作成

プロジェクトのルートディレクトリで `lefthook install` を実行してください。