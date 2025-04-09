# Google の外部 ID プロバイダを設定する

## ステップ1：Google OAuth 2.0 クライアントを作成

1. Google デベロッパーコンソールに移動します。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして、「OAuth クライアントID」を選択します。
4. 必要に応じて、同意画面を設定します。
5. アプリケーションの種類で、「ウェブアプリケーション」を選択します。
6. リダイレクトURIは後で設定するため、今は空のままにし、一時的に保存します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)を参照してください。

## ステップ 2: Google OAuth 認証情報を AWS Secrets Manager に保存する

1. AWS Management Console にログインします。
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択します。
3. 「その他のタイプのシークレット」を選択します。
4. Google OAuth の clientId と clientSecret をキーと値のペアとして入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. シークレットに名前と説明を付けるための手順に従います。CDKコードで使用するため、シークレット名（例：googleOAuthCredentials）をメモしておいてください。（ステップ 3 の変数名に <YOUR_SECRET_NAME> を使用）
6. シークレットを確認して保存します。

### 注意

キー名は、厳密に 'clientId' と 'clientSecret' の文字列と一致する必要があります。

## ステップ3: cdk.jsonの更新

cdk.jsonファイルに、IDプロバイダーとシークレット名を以下のように追加します：

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
    "userPoolDomainPrefix": "<ユーザープールのための一意のドメイン接頭辞>"
  }
}
```

### 注意

#### 一意性

userPoolDomainPrefixは、Amazon Cognitoのすべてのユーザー間でグローバルに一意である必要があります。すでに別のAWSアカウントで使用されている接頭辞を選択すると、ユーザープールドメインの作成に失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名を接頭辞に含めることをお勧めします。

## ステップ 4: CDKスタックをデプロイ

AWS上にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Google OAuth クライアントを Cognito のリダイレクト URI で更新する

スタックをデプロイした後、AuthApprovedRedirectURI が CloudFormation の出力に表示されます。Google Developer Console に戻り、OAuth クライアントを正しいリダイレクト URI で更新してください。