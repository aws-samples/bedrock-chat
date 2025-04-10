# Google の外部 ID プロバイダの設定

## ステップ1：Google OAuth 2.0クライアントを作成する

1. Google開発者コンソールにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックし、「OAuthクライアントID」を選択します。
4. 要求に応じて同意画面を設定します。
5. アプリケーションの種類で「ウェブアプリケーション」を選択します。
6. リダイレクトURIは、後で設定するため、現時点では空のままにし、一時的に保存します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)を参照してください。

## ステップ2：Google OAuth資格情報をAWS Secrets Managerに保存する

1. AWS管理コンソールにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. Google OAuth の clientId と clientSecret をキーと値のペアとして入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで必要になるので、シークレット名を必ずメモしてください。例: googleOAuthCredentials。（ステップ3で <YOUR_SECRET_NAME> 変数名として使用）
6. シークレットを確認して保存します。

### 注意

キー名は、'clientId' と 'clientSecret' の文字列に完全に一致する必要があります。

## ステップ3：cdk.jsonを更新する

cdk.jsonファイルに、IDプロバイダーとシークレット名を追加します。

以下のようになります：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<あなたのシークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールの一意のドメインプレフィックス>"
  }
}
```

### 注意

#### 一意性

userPoolDomainPrefixは、Amazon Cognitoのすべてのユーザーで一意である必要があります。すでに他のAWSアカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。プレフィックスの一意性を保証するために、識別子、プロジェクト名、環境名などを含めることをお勧めします。

## ステップ 4: CDKスタックのデプロイ

AWS上にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5：Cognitoのリダイレクト URIでGoogleOAuthクライアントを更新する

スタックをデプロイした後、CloudFormationの出力に`AuthApprovedRedirectURI`が表示されます。Googleデベロッパーコンソールに戻り、正しいリダイレクトURIでOAuthクライアントを更新します。