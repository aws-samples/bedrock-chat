# Google用の外部IDプロバイダーを設定する

## ステップ1: Google OAuth 2.0 クライアントを作成する

1. Google Developer Consoleにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして、「OAuth クライアントID」を選択します。
4. プロンプトが表示されたら、同意画面を設定します。
5. アプリケーションの種類で、「ウェブアプリケーション」を選択します。
6. 今は後で設定するためにリダイレクトURIは空白のままにし、一時的に保存します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモしておきます。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ2: Google OAuth 認証情報をAWS Secrets Managerに保存する

1. AWS管理コンソールにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他のタイプのシークレット」を選択します。
4. Google OAuth のclientIdとclientSecretをキーと値のペアとして入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで使用するため、シークレット名をメモしておきます。例: googleOAuthCredentials（ステップ3の変数名 <YOUR_SECRET_NAME>）
6. シークレットを確認して保存します。

### 注意

キー名は、厳密に 'clientId' と 'clientSecret' の文字列と一致する必要があります。

## ステップ 3: cdk.jsonの更新

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

#### ユニーク性

userPoolDomainPrefixは、すべてのAmazon Cognitoユーザーの間でグローバルにユニークである必要があります。他のAWSアカウントですでに使用されている接頭辞を選択すると、ユーザープールドメインの作成に失敗します。ユニーク性を確保するために、識別子、プロジェクト名、または環境名を接頭辞に含めることをお勧めします。

## ステップ4: CDKスタックのデプロイ

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Google OAuth クライアントを Cognito リダイレクト URI で更新する

スタックをデプロイした後、AuthApprovedRedirectURI が CloudFormation のアウトプットに表示されます。Google Developer Console に戻り、正しいリダイレクト URI で OAuth クライアントを更新してください。