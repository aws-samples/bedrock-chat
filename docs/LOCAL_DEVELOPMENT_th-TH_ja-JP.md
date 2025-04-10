# ローカルネットワーク上での開発

## バックエンド開発

[backend/README](../backend/README_th-TH_ja-JP.md) を参照してください。

## フロントエンドの開発

この例では、`npx cdk deploy` でデプロイされた AWS リソース（`API Gateway`、`Cognito` など）を使用して、ローカル環境でフロントエンドを編集および実行できます。

1. AWS 環境へのデプロイについては、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください
2. `frontend/.env.template` をコピーし、`frontend/.env.local` として保存します
3. `npx cdk deploy` の結果（例：`BedrockChatStack.AuthUserPoolClientIdXXXXX`）に基づいて、`.env.local` の内容を入力します
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (推奨) コミット前フックの設定

GitHub ワークフローを追加して、Pull Request 作成時に型チェックとコードレビューを行いますが、コードレビューの完了を待つことは最適な開発体験ではありません。そのため、これらのコードチェックは自動的にコミット時に実行されるべきです。この目的を達成するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) をお勧めします。必須ではありませんが、効率的な開発体験のために導入することをお勧めします。また、[Prettier](https://prettier.io/) による TypeScript のフォーマット強制はしませんが、貢献する際に使用していただければ幸いです。不要な差分を防ぐのに役立ちます。

### Lefthookのインストール

Mac と Homebrew を使用している場合は、`brew install lefthook` を実行するだけです。詳細は[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。

### Poetryのインストール

Python コードチェックが `mypy` と `black` に依存しているため、必要です。

```sh
cd backend
python3 -m venv .venv  # オプション (Poetryを環境にインストールしたくない場合)
source .venv/bin/activate  # オプション (Poetryを環境にインストールしたくない場合)
pip install poetry
poetry install
```

詳細については、[バックエンドの README](../backend/README_th-TH_ja-JP.md) を確認してください。

### コミット前フックの作成

プロジェクトのルートディレクトリで `lefthook install` を実行するだけです。