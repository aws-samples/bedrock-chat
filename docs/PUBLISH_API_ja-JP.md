# API公開

## 概要

このサンプルには、APIを公開する機能が含まれています。チャットインターフェースは予備的な検証に便利かもしれませんが、実際の実装は特定のユースケースとエンドユーザーのユーザーエクスペリエンス（UX）に依存します。状況によっては、チャットUIが望ましい選択肢となる一方で、スタンドアロンAPIがより適している場合もあります。初期検証の後、このサンプルはプロジェクトのニーズに応じてカスタマイズされたボットを公開する機能を提供します。クォータ、スロットリング、オリジンなどの設定を入力することで、APIキーと共にエンドポイントを公開でき、多様な統合オプションに柔軟に対応できます。

## セキュリティ

[AWS API Gateway開発者ガイド](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)で説明されているように、APIキーのみを使用することは推奨されません。そのため、このサンプルではAWS WAFを介した単純なIPアドレス制限を実装しています。WAFルールは、コスト面の考慮から、アプリケーション全体に共通して適用されます。これは、制限したいソースが発行されたすべてのAPIで同じである可能性が高いという前提に基づいています。**実際の実装については、組織のセキュリティポリシーに従ってください。**また、[アーキテクチャ](#architecture)セクションも参照してください。

## カスタマイズされたボット APIの公開方法

### 前提条件

ガバナンス上の理由から、限られたユーザーのみがボットを公開できます。公開する前に、ユーザーは `PublishAllowed` という名前のグループのメンバーである必要があります。このグループは管理コンソール > Amazon Cognito ユーザープール、またはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > 出力 > `AuthUserPoolIdxxxx` からアクセスできます。

![](./imgs/group_membership_publish_allowed.png)

### API 公開設定

`PublishedAllowed` ユーザーとしてログインし、ボットを作成した後、`API 公開設定` を選択します。共有ボットのみが公開可能であることに注意してください。
![](./imgs/bot_api_publish_screenshot.png)

次の画面で、スロットリングに関するいくつかのパラメータを設定できます。詳細については、以下のリンクも参照してください：[スループット向上のためのAPIリクエストのスロットリング](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)。
![](./imgs/bot_api_publish_screenshot2.png)

デプロイ後、以下の画面が表示され、エンドポイントURLとAPIキーを取得できます。APIキーの追加や削除も可能です。

![](./imgs/bot_api_publish_screenshot3.png)

## アーキテクチャ

APIは次の図のように公開されています：

![](./imgs/published_arch.png)

WAFはIPアドレスの制限に使用されます。アドレスは、`cdk.json`の`publishedApiAllowedIpV4AddressRanges`および`publishedApiAllowedIpV6AddressRanges`パラメータを設定することで構成できます。

ユーザーがボットを公開すると、[AWS CodeBuild](https://aws.amazon.com/codebuild/)がCDKデプロイメントタスクを起動し、API Gateway、Lambda、SQSを含むAPIスタックをプロビジョニングします（参照：[CDK定義](../cdk/lib/api-publishment-stack.ts)）。SQSは、ユーザーリクエストとLLM操作を分離するために使用されます。これは、出力の生成がAPI Gatewayのクォータである30秒を超える可能性があるためです。出力を取得するには、APIに非同期でアクセスする必要があります。詳細については、[API仕様](#api-specification)を参照してください。

クライアントはリクエストヘッダーに`x-api-key`を設定する必要があります。

## APIの仕様

[こちら](https://aws-samples.github.io/bedrock-chat)を参照してください。