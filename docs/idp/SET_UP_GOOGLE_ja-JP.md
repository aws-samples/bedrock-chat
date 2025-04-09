# Google の外部 ID プロバイダを設定する

## ステップ1: Google OAuth 2.0 クライアントの作成

1. Google Developer Consoleにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして「OAuth クライアントID」を選択します。
4. プロンプトが表示されたら、同意画面を設定します。
5. アプリケーションの種類で、「ウェブアプリケーション」を選択します。
6. リダイレクトURIは、後で設定するため、今は空白のままにし、一時的に保存します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモしておきます。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ2: Google OAuth認証情報をAWS Secrets Managerに保存する

1. AWS管理コンソールにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. Google OAuth のclientIdとclientSecretをキーと値のペアとして入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。後でCDKコードで使用するため、シークレット名をメモしておきます。例: googleOAuthCredentials（ステップ3の変数名 <YOUR_SECRET_NAME>）
6. 内容を確認し、シークレットを保存します。

### 注意

キー名は、文字列 'clientId' と 'clientSecret' と完全に一致する必要があります。

## ステップ 3: cdk.json の更新

cdk.json ファイルに、ID プロバイダと SecretName を追加します。

以下のようになります：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 注意

#### 一意性

ユーザープールドメインプレフィックスは、すべての Amazon Cognito ユーザー間でグローバルに一意である必要があります。すでに他の AWS アカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ 4: CDKスタックのデプロイ

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Google OAuth クライアントを Cognito リダイレクト URI で更新

スタックをデプロイした後、CloudFormation のアウトプットに AuthApprovedRedirectURI が表示されます。Google Developer Console に戻り、正しいリダイレクト URI で OAuth クライアントを更新してください。