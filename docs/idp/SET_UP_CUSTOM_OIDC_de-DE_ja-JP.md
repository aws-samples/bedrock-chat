# 外部IDプロバイダーの設定

## ステップ1: OIDCクライアントの作成

対象のOIDCプロバイダーの手順に従い、OIDC クライアントIDとシークレットの値を記録します。以降のステップで発行者URL（Issuer URL）も必要となります。セットアップ手順でリダイレクトURI（Redirect URI）が必要な場合は、デプロイ完了後に置き換える仮の値を入力してください。

## ステップ 2: 認証情報をAWS Secrets Managerに保存する

1. AWS Management Consoleを開きます。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアとして入力します。

   - キー: `clientId`、値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`、値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`、値: <ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで必要になるシークレット名をメモしておきます（ステップ3で <YOUR_SECRET_NAME> として使用されます）。
6. シークレットを確認して保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl` の文字列と完全に一致する必要があります。

## ステップ 3: cdk.jsonの更新

cdk.json ファイルに、IDプロバイダーとシークレット名を次のように追加します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<あなたのサービス名>", // 任意の値を選択
        "secretName": "<あなたのシークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールの一意のドメインプレフィックス>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix` は、すべてのAmazon Cognitoユーザープール間でグローバルに一意である必要があります。既に他のAWSアカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ4: CDKスタックのデプロイ

AWS に CDK スタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Cognito リダイレクト URI で OIDC クライアントを更新

スタックのデプロイ後、`AuthApprovedRedirectURI` が CloudFormation の出力に表示されます。OIDC 設定に戻り、正しいリダイレクト URI で更新してください。