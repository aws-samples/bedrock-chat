# 外部IDプロバイダーの設定

## ステップ1: OIDCクライアントの作成

該当するOIDCプロバイダーの手順に従い、OIDC クライアントIDとシークレットの値を記録してください。発行者URLも後続のステップで必要になります。セットアップ手順でリダイレクトURIが要求される場合は、デプロイメント完了後に置き換えられる一時的な値を指定してください。

## ステップ 2: AWS Secrets Managerに認証情報を保存

1. AWS Management Consoleにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアで入力します。

   - キー: `clientId`、値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`、値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`、値: <ISSUER_URL_OF_THE_PROVIDER>

5. シークレットに名前と説明を付けるための手順に従います。シークレット名をメモしておいてください。CDKコードで後で必要になります（ステップ3の変数名 <YOUR_SECRET_NAME>で使用）。
6. 内容を確認し、シークレットを保存します。

### 注意

キー名は、文字列 `clientId`、`clientSecret`、`issuerUrl` と完全に一致する必要があります。

## ステップ 3: cdk.json を更新

cdk.json ファイルに、ID プロバイダーとシークレット名を次のように追加します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<あなたのサービス名>", // 任意の値を設定
        "secretName": "<あなたのシークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールの一意のドメインプレフィックス>"
  }
}
```

### 注意

#### 一意の名前

`userPoolDomainPrefix` は、すべての Amazon Cognito ユーザー間でグローバルに一意である必要があります。既に別の AWS アカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。一意の名前を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ 4: CDKスタックをデプロイ

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Cognito リダイレクト URI で OIDC クライアントを更新

スタックがデプロイされた後、`AuthApprovedRedirectURI` が CloudFormation の出力に表示されます。OIDC 設定に戻り、正しいリダイレクト URI で更新してください。