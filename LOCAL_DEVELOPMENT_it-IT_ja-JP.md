# ローカル開発

## バックエンド開発

[backend/README](../backend/README_it-IT_ja-JP.md) を参照してください。

## フロントエンド開発

この例では、`npx cdk deploy`で配置されたAWSリソース（`API Gateway`、`Cognito`など）を使用して、フロントエンドをローカルで変更および起動できます。

1. AWS環境への配置については、[CDKを使用した配置](../README.md#deploy-using-cdk)を参照してください。
2. `frontend/.env.template`をコピーし、`frontend/.env.local`として保存します。
3. `npx cdk deploy`の出力結果（`BedrockChatStack.AuthUserPoolClientIdXXXXX`など）に基づいて、`.env.local`の内容を入力します。
4. 次のコマンドを実行します：

```zsh
cd frontend && npm ci && npm run dev
```

## (オプション、推奨) pre-commitフックの設定

GitHub workflowでtype-checkingとlintingを導入しました。これらはPull Requestが作成されたときに実行されますが、lintingが完了するまで待つのは開発体験として良くありません。そのため、これらのlintingタスクはコミット時に自動的に実行されるべきです。この目的を達成するために、[Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)を導入しました。必須ではありませんが、効率的な開発体験のために採用することをお勧めします。また、TypeScriptの整形を[Prettier](https://prettier.io/)で設定していない場合でも、コード・レビュー時の不要な差分を防ぐため、コントリビュート時に採用することを歓迎します。

### Lefthookのインストール

[こちら](https://github.com/evilmartians/lefthook#install)を参照してください。Homebrewを使用するMacの場合、`brew install lefthook`を実行するだけです。

### Poetryのインストール

これは、PythonコードのlintingがPython `mypy`と`black`に依存しているために必要です。

```sh
cd backend
python3 -m venv .venv  # オプション（poetryを環境にインストールしない場合）
source .venv/bin/activate  # オプション（poetryを環境にインストールしない場合）
pip install poetry
poetry install
```

詳細については、[バックエンドのREADME](../backend/README_it-IT_ja-JP.md)を参照してください。

### pre-commitフックの作成

プロジェクトのルートディレクトリで`lefthook install`を実行するだけです。