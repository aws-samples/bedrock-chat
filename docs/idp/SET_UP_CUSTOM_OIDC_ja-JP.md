# 外部アイデンティティプロバイダーの設定

## ステップ1：OIDCクライアントの作成

対象のOIDCプロバイダーの手順に従い、OIDCクライアントIDとシークレットの値を記録してください。また、以降のステップで発行者URL（issuer URL）が必要となります。セットアップ時にリダイレクトURIが必要な場合は、デプロイ完了後に置き換えられるダミー値を入力してください。

## ステップ2：AWS Secrets Managerに認証情報を保存する

1. AWS Management Consoleにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他のシークレットタイプ」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアとして入力します。

   - キー: `clientId`, 値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`, 値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`, 値: <ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従ってシークレットの名前と説明を入力します。CDKコード（ステップ3の変数名<YOUR_SECRET_NAME>で使用）で必要になるため、シークレット名を控えておいてください。
6. 内容を確認してシークレットを保存します。

### 注意

キー名は正確に `clientId`、`clientSecret`、`issuerUrl` と一致している必要があります。

## ステップ3：cdk.jsonの更新

cdk.jsonファイルに、IDプロバイダーとSecretNameを追加します。

以下のように設定します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<YOUR_SERVICE_NAME>", // お好みの値を設定してください
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 注意事項

#### 一意性について

`userPoolDomainPrefix`は、すべてのAmazon Cognitoユーザー間でグローバルに一意である必要があります。他のAWSアカウントですでに使用されているプレフィックスを選択した場合、ユーザープールドメインの作成は失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ 4: CDK スタックのデプロイ

CDK スタックを AWS にデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## Step 5: OIDC クライアントを Cognito のリダイレクト URI で更新

スタックのデプロイ後、CloudFormation の出力に `AuthApprovedRedirectURI` が表示されます。OIDC の設定に戻り、正しいリダイレクト URI で更新してください。