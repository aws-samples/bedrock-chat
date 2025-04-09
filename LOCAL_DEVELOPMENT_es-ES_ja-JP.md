# ローカル開発

## バックエンド開発

[backend/README](../backend/README_es-ES_ja-JP.md) を参照してください。

## フロントエンド開発

この例では、`npx cdk deploy`でデプロイされたAWSリソース（`API Gateway`、`Cognito`など）を使用して、ローカルでフロントエンドを変更および起動できます。

1. AWS環境にデプロイするには、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーし、`frontend/.env.local`として保存します。
3. `.env.local`の内容を`npx cdk deploy`の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) pre-commitフックの設定

GitHub ワークフローで型チェックとリンティングを導入しました。これらは pull request 作成時に実行されますが、リンティングが完了するまで待つのは開発体験としては良くありません。そのため、これらのリンティングタスクはコミット段階で自動的に実行されるべきです。これを実現するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) を導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、TypeScriptの書式を [Prettier](https://prettier.io/) で強制はしていませんが、コードレビュー時の不要な差分を防ぐため、コントリビュート時に採用していただけると幸いです。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。MacとHomebrewのユーザーの場合、`brew install lefthook` を実行するだけです。

### Poetryのインストール

これは、Pythonのコードレビューが `mypy` と `black` に依存しているためです。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを独自の環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（poetryを独自の環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_es-ES_ja-JP.md)を参照してください。

### pre-commitフックの作成

プロジェクトのルートディレクトリで `lefthook install` を実行するだけです。