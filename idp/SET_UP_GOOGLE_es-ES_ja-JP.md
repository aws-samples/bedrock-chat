# Google用の外部IDプロバイダの設定

## ステップ1：Google OAuth 2.0 クライアントを作成する

1. Google開発者コンソールにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックし、「OAuthクライアントID」を選択します。
4. 求められた場合、同意画面を設定します。
5. アプリケーションの種類で「ウェブアプリケーション」を選択します。
6. リダイレクトURIは後で設定するため、今は空白のままにし、一時的に保存します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモしておきます。

詳細については、[Google公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ 2: Google OAuth の認証情報を AWS Secrets Manager に保存

1. AWS マネジメントコンソールにアクセスします。
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. Google OAuth の clientId と clientSecret をキーと値のペアで入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで必要になるため、シークレット名をメモしておいてください。例えば、googleOAuthCredentials。（ステップ 3 の変数名 <YOUR_SECRET_NAME> で使用）
6. 内容を確認し、シークレットを保存します。

### 注意

キー名は、厳密に 'clientId' と 'clientSecret' の文字列と一致する必要があります。

## ステップ3: cdk.jsonを更新

cdk.jsonファイルに、IDプロバイダとシークレット名を次のように追加します：

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

#### ユニーク性

userPoolDomainPrefixは、Amazon Cognitoのすべてのユーザー間でグローバルにユニークである必要があります。すでに別のAWSアカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。プレフィックスの一意性を確保するために、識別子、プロジェクト名、または環境名を含めることをお勧めします。

## ステップ4：CDKスタックのデプロイ

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ5: Cognito のリダイレクト URI で Google OAuth クライアントを更新する

スタックをデプロイした後、AuthApprovedRedirectURI が CloudFormation の出力に表示されます。Google デベロッパーコンソールに戻り、正しいリダイレクト URI で OAuth クライアントを更新してください。