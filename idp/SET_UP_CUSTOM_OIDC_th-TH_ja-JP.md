# 外部認証プロバイダの設定

## ステップ 1: OIDC クライアントの作成

対象の OIDC プロバイダーの手順に従い、OIDC クライアント ID とシークレットの値を記録します。また、次のステップで必要となる発行者 URL も記録してください。リダイレクト URI が必要な場合は、デプロイ後に置き換えられるダミー値を入力します。

## ステップ 2: AWS Secrets Managerに認証情報を保存する

1. AWS Management Consoleにアクセスします
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します
3. 「その他のタイプのシークレット」を選択します
4. クライアントIDとクライアントシークレットをキーと値のペアで入力します

   - Key: `clientId`、Value: <YOUR_GOOGLE_CLIENT_ID>
   - Key: `clientSecret`、Value: <YOUR_GOOGLE_CLIENT_SECRET>
   - Key: `issuerUrl`、Value: <ISSUER_URL_OF_THE_PROVIDER>

5. 指示に従ってシークレットに名前と説明を付けます。CDKコードで使用するため（ステップ3の <YOUR_SECRET_NAME> 変数）、シークレット名に注意してください
6. シークレットを確認して保存します

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl` の文字列と完全に一致する必要があります

## ステップ3: cdk.jsonの更新

cdk.jsonファイルに、ID プロバイダとSecretNameを追加します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<あなたのサービス名>", // 好きな名前を設定できます
        "secretName": "<あなたのシークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<User Poolの一意のドメインプレフィックス>"
  }
}
```

### 注意事項

#### 一意性

`userPoolDomainPrefix`は、すべてのAmazon Cognitoユーザーにおいて、グローバルに一意である必要があります。他のAWSアカウントですでに使用されているプレフィックスを選択すると、User Poolドメインの作成に失敗します。ベストプラクティスは、識別子、プロジェクト名、または環境名をプレフィックスに含めて、一意性を確保することです。

## ステップ 4: CDKスタックのデプロイ

CDKスタックをAWSにデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: CognitoのリダイレクトURIを使用してOIDCクライアントを更新

CloudFormationスタックの`AuthApprovedRedirectURI`の出力結果が表示されたら、OIDCの設定に戻り、正しいリダイレクトURIで更新します。