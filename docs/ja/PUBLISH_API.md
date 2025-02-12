# API 公開

## 概要

このサンプルには、API を公開する機能が含まれています。チャットインターフェースは予備的な検証に便利ですが、実際の実装は特定のユースケースとエンドユーザーの望むユーザーエクスペリエンス（UX）に依存します。状況によっては、チャット UI が好まれる場合もあれば、スタンドアロンの API がより適している場合もあります。初期検証後、このサンプルはプロジェクトのニーズに応じてカスタマイズされたボットを公開する機能を提供します。クォータ、スロットリング、オリジンなどの設定を入力することで、API キーと共にエンドポイントを公開し、多様な統合オプションに柔軟に対応できます。

## セキュリティ

[AWS API Gateway 開発者ガイド](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)で説明されているように、API キーのみを使用することは推奨されません。そのため、このサンプルでは AWS WAF を介した単純な IP アドレス制限を実装しています。コスト面を考慮し、制限したいソースは発行されるすべての API で同じである可能性が高いという前提で、WAF ルールはアプリケーション全体に共通して適用されます。**実際の実装では、組織のセキュリティポリシーに従ってください。** [アーキテクチャ](#アーキテクチャ)セクションも参照してください。

## カスタマイズされたボット API の公開方法

### 前提条件

ガバナンス上の理由から、限られたユーザーのみがボットを公開できます。公開する前に、ユーザーは `PublishAllowed` というグループのメンバーである必要があり、管理コンソール > Amazon Cognito ユーザープール または aws cli で設定できます。ユーザープール ID は、CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` からアクセスできます。

![](../imgs/group_membership_publish_allowed.png)

### API 公開設定

`PublishedAllowed` ユーザーとしてログインし、ボットを作成した後、`API 公開設定` を選択します。共有ボットのみ公開できることに注意してください。
![](../imgs/bot_api_publish_screenshot.png)

次の画面では、スロットリングに関するいくつかのパラメータを設定できます。詳細については、[API リクエストのスロットリングによるスループットの向上](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)も参照してください。
![](../imgs/bot_api_publish_screenshot2.png)

デプロイ後、以下の画面が表示され、エンドポイント URL と API キーを取得できます。API キーの追加や削除も可能です。

![](../imgs/bot_api_publish_screenshot3.png)

## アーキテクチャ

API は以下の図のように公開されます：

![](../imgs/published_arch.png)

WAF は IP アドレス制限に使用されます。アドレスは `cdk.json` の `publishedApiAllowedIpV4AddressRanges` および `publishedApiAllowedIpV6AddressRanges` パラメータで設定できます。

ユーザーがボットを公開すると、[AWS CodeBuild](https://aws.amazon.com/jp/codebuild/) が CDK デプロイメントタスクを起動し、API Gateway、Lambda、SQS を含む API スタックをプロビジョニングします（[CDK 定義](../cdk/lib/api-publishment-stack.ts)も参照）。SQS は、出力の生成に 30 秒を超える場合があるため、ユーザーリクエストと LLM 操作を分離するために使用されます。これは API Gateway のクォータ制限です。出力を取得するには、API に非同期でアクセスする必要があります。詳細については、[API 仕様](#api-仕様)を参照してください。

クライアントはリクエストヘッダーに `x-api-key` を設定する必要があります。

## API 仕様

[こちら](https://aws-samples.github.io/bedrock-claude-chat)を参照してください。