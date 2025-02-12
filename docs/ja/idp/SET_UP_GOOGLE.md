# Google用の外部IDプロバイダーの設定

## ステップ1：Google OAuth 2.0クライアントの作成

1. Google開発者コンソールにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして、「OAuth クライアントID」を選択します。
4. プロンプトが表示されたら同意画面を設定します。
5. アプリケーションの種類で「ウェブアプリケーション」を選択します。
6. 今は後で設定するためリダイレクトURIは空白のままにし、一時的に保存します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ2：AWS Secrets ManagerにGoogle OAuth認証情報を保存

1. AWS管理コンソールにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. Google OAuthのclientIdとclientSecretをキーと値のペアで入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで必要になるため、シークレット名をメモしてください。例: googleOAuthCredentials。（ステップ3の変数名 <YOUR_SECRET_NAME>で使用）
6. レビューしてシークレットを保存します。

### 注意

キー名は「clientId」と「clientSecret」の文字列と完全に一致する必要があります。

## ステップ3：cdk.jsonの更新

cdk.jsonファイルに、IDプロバイダーとSecretNameを追加します。

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

userPoolDomainPrefixは、すべてのAmazon Cognito ユーザー間でグローバルに一意である必要があります。他のAWSアカウントですでに使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ4：CDKスタックのデプロイ

CDKスタックをAWSにデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ5：Cognito リダイレクトURIでGoogle OAuthクライアントを更新

スタックをデプロイした後、CloudFormationの出力にAuthApprovedRedirectURIが表示されます。Google開発者コンソールに戻り、正しいリダイレクトURIでOAuthクライアントを更新します。