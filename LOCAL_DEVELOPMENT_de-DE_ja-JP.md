# ローカル開発

## バックエンド開発

[backend/README](../backend/README_de-DE_ja-JP.md) をお読みください。

## フロントエンド開発

この例では、`npx cdk deploy`でデプロイされた`API Gateway`、`Cognito`などのAWSリソースを使用しながら、フロントエンドをローカルで変更および起動できます。

1. AWS環境へのデプロイについては、[CDKを使用したデプロイ](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーし、`frontend/.env.local`として保存します。
3. `npx cdk deploy`の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて、`.env.local`の内容を入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) Pre-Commitフックの設定

GitHub Workflowsを型チェックとリンティングのために導入しました。これらはPull Requestが作成されたときに実行されますが、リンティングが完了するのを待つのは良い開発体験ではありません。そのため、これらのリンティングタスクをコミット段階で自動的に実行する必要があります。これを実現するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)を導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、[Prettier](https://prettier.io/)でTypeScriptのフォーマットを強制していませんが、コードレビュー時の不要な差分を避けるのに役立つため、貢献の際に採用していただけると幸いです。

### Lefthookのインストール

詳細は[こちら](https://github.com/evilmartians/lefthook#install)をご覧ください。MacとHomebrewユーザーの場合は、`brew install lefthook`を実行するだけです。

### Poetryのインストール

これは、Pythonコードのリンティングがmypyとblackに依存しているため必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（Poetryを環境にインストールしたくない場合）
source .venv/bin/activate  # オプション（Poetryを環境にインストールしたくない場合）
pip install poetry
poetry install
```

詳細は[バックエンドのREADME](../backend/README_de-DE_ja-JP.md)をご覧ください。

### Pre-Commitフックの作成

プロジェクトのルートディレクトリで`lefthook install`を実行するだけです。