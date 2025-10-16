# API公開

## 概要

このサンプルにはAPIを公開するための機能が含まれています。チャットインターフェースは初期の検証には便利ですが、実際の実装は特定のユースケースとエンドユーザーに求められるユーザーエクスペリエンス（UX）に依存します。シナリオによっては、チャットUIが最適な選択となる場合もあれば、スタンドアロンのAPIがより適している場合もあります。初期検証の後、このサンプルではプロジェクトのニーズに応じてカスタマイズされたボットを公開する機能を提供します。クォータ、スロットリング、オリジンなどの設定を入力することで、APIキーと共にエンドポイントを公開でき、多様な統合オプションに対する柔軟性を提供します。

## セキュリティ

APIキーのみを使用することは、[AWS API Gateway 開発者ガイド](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)で説明されているように推奨されていません。そのため、このサンプルではAWS WAFを介してシンプルなIPアドレス制限を実装しています。WAFルールは、制限したい送信元が提供されるすべてのAPI全体で同じである可能性が高いという前提のもと、コスト面を考慮してアプリケーション全体に共通して適用されています。**実際の実装では、組織のセキュリティポリシーに従ってください。**また、[アーキテクチャ](#architecture)セクションもご参照ください。

## ボットAPIのカスタマイズと公開方法

### 前提条件

ガバナンス上の理由により、ボットを公開できるのは限られたユーザーのみです。公開前に、ユーザーは`PublishAllowed`というグループのメンバーである必要があります。このグループは、管理コンソール > Amazon Cognito User poolsまたはaws cliを通じて設定できます。なお、ユーザープールIDは、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`でご確認いただけます。

![](./imgs/group_membership_publish_allowed.png)

### API公開設定

`PublishedAllowed`ユーザーとしてログインしボットを作成した後、`API PublishSettings`を選択します。共有設定されているボットのみが公開可能であることにご注意ください。
![](./imgs/bot_api_publish_screenshot.png)

次の画面では、スロットリングに関する複数のパラメータを設定できます。詳細については、以下もご参照ください：[Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)。
![](./imgs/bot_api_publish_screenshot2.png)

デプロイ後、エンドポイントURLとAPIキーを取得できる以下の画面が表示されます。APIキーの追加と削除も可能です。

![](./imgs/bot_api_publish_screenshot3.png)

## アーキテクチャ

APIは以下の図のように公開されています：

![](./imgs/published_arch.png)

WAFはIPアドレス制限に使用されます。アドレスは`cdk.json`内のパラメータ`publishedApiAllowedIpV4AddressRanges`と`publishedApiAllowedIpV6AddressRanges`を設定することで構成できます。

ユーザーがボットを公開すると、[AWS CodeBuild](https://aws.amazon.com/codebuild/)がCDKデプロイメントタスクを起動し、API Gateway、Lambda、SQSを含むAPIスタックをプロビジョニングします（[CDKの定義](../cdk/lib/api-publishment-stack.ts)も参照）。SQSは、出力の生成にAPI Gatewayのクォータ制限である30秒を超える可能性があるため、ユーザーリクエストとLLMの操作を分離するために使用されます。出力を取得するには、非同期でAPIにアクセスする必要があります。詳細については、[API仕様](#api-specification)を参照してください。

クライアントはリクエストヘッダーに`x-api-key`を設定する必要があります。

## API仕様

[こちら](https://aws-samples.github.io/bedrock-chat)をご覧ください。