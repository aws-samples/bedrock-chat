# Google の外部 ID プロバイダーの設定

## Step 1: Google OAuth 2.0クライアントの作成

1. Google Developer Consoleにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして「OAuthクライアントID」を選択します。
4. 要求された場合は、同意画面を設定します。
5. アプリケーションの種類で「ウェブアプリケーション」を選択します。
6. リダイレクトURIは後で設定するため、一時的に空白のままにしておきます。[Step5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモしておきます。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ2：Google OAuth認証情報をAWS Secrets Managerに保存する

1. AWSマネジメントコンソールにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットの保存」を選択します。
3. 「その他のシークレットタイプ」を選択します。
4. Google OAuthのclientIdとclientSecretをキーと値のペアとして入力します。

   1. キー: clientId, 値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret, 値: <YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで必要となるため、シークレット名を控えておいてください。例：googleOAuthCredentials（ステップ3の変数名<YOUR_SECRET_NAME>で使用）
6. シークレットを確認して保存します。

### 注意

キー名は'clientId'と'clientSecret'に正確に一致している必要があります。

## ステップ3：cdk.jsonの更新

cdk.jsonファイルに、IDプロバイダーとSecretNameを追加します。

以下のように：

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

### 注意事項

#### 一意性

userPoolDomainPrefixは、すべてのAmazon Cognitoユーザー間でグローバルに一意である必要があります。他のAWSアカウントですでに使用されているプレフィックスを選択した場合、ユーザープールドメインの作成は失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ4: CDKスタックのデプロイ

CDKスタックをAWSにデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## Step 5: Google OAuthクライアントをCognitoリダイレクトURIで更新する

スタックのデプロイ後、CloudFormationの出力にAuthApprovedRedirectURIが表示されます。Google Developer Consoleに戻り、OAuthクライアントに正しいリダイレクトURIを更新してください。