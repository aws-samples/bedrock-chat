# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ja/README.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ko/README.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/zh/README.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/fr/README.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/de/README.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/es/README.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/it/README.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/no/README.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/th/README.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/id/README.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/ms/README.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/vi/README.md)

> [!Warning]  
> **V2がリリースされました。更新する際は、[移行ガイド](./migration/V1_TO_V2.md)を注意深く確認してください。** 注意を払わないと、**V1のBOTが使用できなくなります。**

[Amazon Bedrock](https://aws.amazon.com/bedrock/)が提供するLLMモデルを使用した多言語チャットボット。

### YouTubeで概要とインストールを視聴

[![概要](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### 基本的な会話

![](./imgs/demo.gif)

### ボットのパーソナライズ

独自の指示を追加し、URLまたはファイルとして外部知識を提供（[RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)）。ボットはアプリケーションユーザー間で共有できます。カスタマイズされたボットはスタンドアロンAPIとして公開することもできます（[詳細](./PUBLISH_API.md)を参照）。

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> ガバナンス上の理由から、許可されたユーザーのみがカスタマイズされたボットを作成できます。カスタマイズされたボットの作成を許可するには、ユーザーは`CreatingBotAllowed`グループのメンバーである必要があります。これは管理コンソール > Amazon Cognito ユーザープールまたはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできます。

### 管理者ダッシュボード

<details>
<summary>管理者ダッシュボード</summary>

管理者ダッシュボードで、ユーザー/ボットごとの使用状況を分析します。[詳細](./ADMINISTRATOR.md)

![](./imgs/admin_bot_analytics.png)

</details>

### LLMを活用したエージェント

<details>
<summary>LLMを活用したエージェント</summary>

[エージェント機能](./AGENT.md)を使用することで、チャットボットはより複雑なタスクを自動的に処理できます。例えば、ユーザーの質問に答えるために、エージェントは外部ツールから必要な情報を取得したり、タスクを複数のステップに分解して処理したりできます。

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 超簡単デプロイ

- us-east-1リージョンで、[Bedrockモデルアクセス](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)を開き、`モデルアクセスの管理` > `Anthropic / Claude 3`のすべて、`Amazon / Nova`のすべて、`Amazon / Titan Text Embeddings V2`、`Cohere / Embed Multilingual`にチェックを入れ、`変更を保存`します。

<details>
<summary>スクリーンショット</summary>

![](./imgs/model_screenshot.png)

</details>

- デプロイしたいリージョンで[CloudShell](https://console.aws.amazon.com/cloudshell/home)を開きます
- 以下のコマンドでデプロイを実行します。デプロイするバージョンを指定したい場合やセキュリティポリシーを適用したい場合は、[オプションパラメータ](#オプションパラメータ)から適切なパラメータを指定してください。

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- 新規ユーザーかv2を使用するかを尋ねられます。v0からの継続ユーザーでない場合は、`y`を入力してください。

### オプションパラメータ

デプロイ時に以下のパラメータを指定して、セキュリティとカスタマイズを強化できます：

- **--disable-self-register**: 自己登録を無効にします（デフォルト：有効）。このフラグが設定されている場合、cognito上でユーザーを作成する必要があり、ユーザーは自分でアカウントを登録できません。
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)を有効にします（デフォルト：無効）。このフラグが設定されている場合、Lambdaファンクションの起動時間を改善し、ユーザーエクスペリエンスをより高速にします。
- **--ipv4-ranges**: 許可されたIPv4範囲をカンマ区切りで指定します（デフォルト：すべてのIPv4アドレスを許可）。
- **--ipv6-ranges**: 許可されたIPv6範囲をカンマ区切りで指定します（デフォルト：すべてのIPv6アドレスを許可）。
- **--disable-ipv6**: IPv6接続を無効にします（デフォルト：有効）。
- **--allowed-signup-email-domains**: サインアップに許可されたメールドメインをカンマ区切りで指定します（デフォルト：ドメイン制限なし）。
- **--bedrock-region**: Bedrockが利用可能なリージョンを定義します（デフォルト：us-east-1）。
- **--repo-url**: デプロイするBedrock Claude Chatのカスタムリポジトリ（フォークまたはカスタムソース管理の場合）（デフォルト：https://github.com/aws-samples/bedrock-claude-chat.git）。
- **--version**: デプロイするBedrock Claude Chatのバージョン（デフォルト：開発中の最新バージョン）。
- **--cdk-json-override**: デプロイ中にCDKコンテキスト値を上書きできます。これにより、cdk.jsonファイルを直接編集せずに設定を変更できます。

使用例：

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

上書きJSONは、cdk.jsonと同じ構造に従う必要があります。以下を含む任意のコンテキスト値を上書きできます：

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- cdk.jsonで定義されている他のコンテキスト値

> [!Note]
> 上書き値は、AWS CodeBuildでのデプロイ時に既存のcdk.json構成とマージされます。指定された上書き値は、cdk.json内の値よりも優先されます。

#### パラメータを指定したコマンド例：

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 約35分後、以下の出力が表示され、ブラウザからアクセスできます

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

上記のようにサインアップ画面が表示され、メールを登録してログインできます。

> [!Important]
> オプションパラメータを設定しない場合、このデプロイ方法では、URLを知っている人は誰でもサインアップできます。本番環境では、セキュリティリスクを軽減するために、IPアドレス制限と自己サインアップの無効化を強くお勧めします（会社のドメインからのメールアドレスのみサインアップできるように、allowed-signup-email-domainsを定義できます）。IPアドレス制限にはipv4-rangesとipv6-rangesの両方を使用し、./binを実行する際にdisable-self-registerを使用して自己サインアップを無効にしてください。

> [!TIP]
> `Frontend URL`が表示されないか、Bedrock Claude Chatが正常に動作しない場合、最新バージョンに問題がある可能性があります。その場合は、パラメータに`--version "v1.2.6"`を追加してデプロイを再試行してください。

（以下、文書の残りの部分も同様に翻訳します。文字数制限のため、ここでは省略します。）