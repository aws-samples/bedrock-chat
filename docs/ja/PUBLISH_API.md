# APIの公開

## 概要

このサンプルには、APIを公開する機能が含まれています。チャットインターフェースは予備的な検証に便利ですが、実際の実装は特定のユースケースとエンドユーザーの望むユーザーエクスペリエンス（UX）に依存します。状況によっては、チャットUIが好まれる場合もあれば、スタンドアロンAPIがより適している場合もあります。初期検証後、このサンプルはプロジェクトのニーズに応じてカスタマイズされたボットを公開する機能を提供します。クォータ、スロットリング、オリジンなどの設定を入力することで、APIキーと共にエンドポイントを公開し、多様な統合オプションを提供します。

## セキュリティ

[AWS API Gateway開発者ガイド](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)に記載されているように、APIキーのみを使用することは推奨されません。そのため、このサンプルはAWS WAFを介したシンプルなIPアドレス制限を実装しています。コスト上の理由から、WAFルールはアプリケーション全体に共通して適用され、制限したいソースは発行されるすべてのAPIで同じである可能性が高いという前提に基づいています。**実際の実装では、組織のセキュリティポリシーに従ってください。** [アーキテクチャ](#アーキテクチャ)セクションも参照してください。

## カスタマイズされたボットAPIを公開する方法

### 前提条件

ガバナンス上の理由から、限られたユーザーのみがボットを公開できます。公開する前に、ユーザーは`PublishAllowed`グループのメンバーである必要があり、これは管理コンソール > Amazon Cognito User poolsまたはAWS CLIで設定できます。ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`からアクセスできます。

![](../imgs/group_membership_publish_allowed.png)

### API公開設定

`PublishedAllowed`ユーザーとしてログインし、ボットを作成した後、`API公開設定`を選択します。共有ボットのみ公開できることに注意してください。
![](../imgs/bot_api_publish_screenshot.png)

次の画面で、スロットリングに関するいくつかのパラメータを設定できます。詳細については、[APIリクエストをスロットルしてスループットを向上させる](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)も参照してください。
![](../imgs/bot_api_publish_screenshot2.png)

デプロイ後、次の画面が表示され、エンドポイントURLとAPIキーを取得できます。APIキーの追加と削除も可能です。

![](../imgs/bot_api_publish_screenshot3.png)

## アーキテクチャ

APIは次の図のように公開されます：

![](../imgs/published_arch.png)

WAFはIPアドレス制限に使用されます。アドレスは`cdk.json`の`publishedApiAllowedIpV4AddressRanges`および`publishedApiAllowedIpV6AddressRanges`パラメータで設定できます。

ユーザーがボットを公開すると、[AWS CodeBuild](https://aws.amazon.com/codebuild/)がCDKデプロイメントタスクを起動し、API Gateway、Lambda、SQSを含むAPIスタックをプロビジョニングします（[CDK定義](../cdk/lib/api-publishment-stack.ts)も参照）。SQSは、ユーザーリクエストとLLM操作を分離するために使用されます。出力の生成に30秒を超える場合があるためです。これはAPI Gatewayのクォータ制限です。出力を取得するには、APIに非同期でアクセスする必要があります。詳細については、[API仕様](#api仕様)を参照してください。

クライアントはリクエストヘッダーに`x-api-key`を設定する必要があります。

## API仕様

[こちら](https://aws-samples.github.io/bedrock-claude-chat)を参照してください。