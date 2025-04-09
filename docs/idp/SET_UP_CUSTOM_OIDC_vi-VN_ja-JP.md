# 外部アイデンティティプロバイダーの設定

## ステップ1: OIDCクライアントの作成

対象のOIDCプロバイダーの手順に従い、OIDCクライアントIDとシークレットの値を記録します。同時に、後続のステップで発行者のURLも必要になります。セットアップ中にリダイレクトURIが要求される場合は、仮の値を入力し、デプロイメント完了後に置き換えます。

## ステップ2: AWS Secrets Managerに認証情報を保存

1. AWS Management Consoleにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他のタイプのシークレット」を選択します。
4. クライアントIDとシークレットをキーと値のペアとして入力します。

   - Key: `clientId`、Value: <YOUR_GOOGLE_CLIENT_ID>
   - Key: `clientSecret`、Value: <YOUR_GOOGLE_CLIENT_SECRET>
   - Key: `issuerUrl`、Value: <ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従ってシークレットに名前と説明を設定します。CDKコードで使用するため、シークレット名をメモしておいてください（ステップ3の <YOUR_SECRET_NAME> 変数で使用）。
6. 確認してシークレットを保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl` の文字列と完全に一致する必要があります。

## ステップ3: cdk.jsonの更新

cdk.jsonファイルに、IDプロバイダーとSecretNameを次のように追加します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<あなたのサービス名>", // 好きな値を設定してください
        "secretName": "<あなたのシークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールの一意のドメイン接頭辞>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix`は、Amazon Cognitoのすべてのユーザー間でグローバルに一意である必要があります。他のAWSアカウントですでに使用されている接頭辞を選択すると、ユーザープールドメインの作成に失敗します。ベストプラクティスとして、識別子、プロジェクト名、または環境名を接頭辞に含めて、一意性を確保してください。

## ステップ4: CDKスタックのデプロイ

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Cognito のリダイレクト URI で OIDC クライアントを更新

スタックをデプロイした後、`AuthApprovedRedirectURI` が CloudFormation の出力に表示されます。OIDC 設定に戻り、正確なリダイレクト URI を更新してください。