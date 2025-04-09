# 外部アイデンティティプロバイダーの設定

## ステップ 1：OIDCクライアントの作成

目的のOIDCプロバイダーの手順に従い、OIDCクライアントIDとシークレットの値をメモしてください。後続のステップでは、発行者URLも必要になります。設定プロセス中にリダイレクトURIが必要な場合は、一時的な値を入力し、デプロイ完了後に置き換えます。

## 手順 2：AWS Secrets Manager に認証情報を保存する

1. AWS 管理コンソールにアクセスします。
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアとして入力します。

   - キー：`clientId`、値：<YOUR_GOOGLE_CLIENT_ID>
   - キー：`clientSecret`、値：<YOUR_GOOGLE_CLIENT_SECRET>
   - キー：`issuerUrl`、値：<ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従ってシークレットに名前と説明を付けます。シークレット名をメモしてください。これは CDK コードで使用します（手順 3 で使用する変数名 <YOUR_SECRET_NAME>）。
6. シークレットを確認して保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl` の文字列と完全に一致する必要があります。

## 手順 3：cdk.json の更新

cdk.json ファイルに、IDプロバイダーとシークレット名を追加します。

以下のようになります：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<サービス名>", // 任意の値を設定できます
        "secretName": "<シークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールドメイン接頭辞の一意の値>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix` は、すべてのAmazon Cognitoユーザー間でグローバルに一意である必要があります。選択した接頭辞が他のAWSアカウントで既に使用されている場合、ユーザープールドメインの作成は失敗します。ベストプラクティスは、識別子、プロジェクト名、または環境名を接頭辞に含めて、一意性を確保することです。

## 手順 4：CDKスタックのデプロイ

CDKスタックをAWSにデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5：Cognito のリダイレクト URI で OIDC クライアントを更新

スタックをデプロイした後、`AuthApprovedRedirectURI` が CloudFormation の出力に表示されます。OIDC の設定に戻り、正しいリダイレクト URI で更新してください。