# Google の外部 ID プロバイダの設定

## ステップ 1: Google OAuth 2.0 クライアントを作成

1. Google Developer Consoleに移動します。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「Credentials」に移動し、「Create Credentials」をクリックして「OAuth client ID」を選択します。
4. プロンプトが表示されたら、同意画面を設定します。
5. アプリケーションタイプで、「Web application」を選択します。
6. リダイレクトURIは今は空のままにしておきます。後で設定します。[ステップ 5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ2: Google OAuth認証情報をAWS Secrets Managerに保存

1. AWS Management Consoleにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他のタイプのシークレット」を選択します。
4. Google OAuth clientIdとclientSecretをキー値ペアとして入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. シークレットに名前と説明を付けるための手順に従います。CDKコードで必要になるため、シークレット名をメモしておいてください。例えば、googleOAuthCredentials。（ステップ3の変数名 <YOUR_SECRET_NAME> で使用）
6. 確認して、シークレットを保存します。

### 注意

キー名は、文字列 'clientId' と 'clientSecret' と完全に一致する必要があります。

## ステップ3: cdk.jsonの更新

cdk.json ファイルで、以下のように ID プロバイダと秘密の名前を追加します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<あなたの秘密の名前>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールの一意のドメインプレフィックス>"
  }
}
```

### 注意

#### 一意の名前

ユーザープールのドメインプレフィックスは、すべての Amazon Cognito ユーザー間でグローバルに一意である必要があります。すでに別の AWS アカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。一意の名前を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ4: CDKスタックをデプロイ

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Cognito リダイレクト URI で Google OAuth クライアントを更新

スタックがデプロイされた後、AuthApprovedRedirectURI が CloudFormation の出力に表示されます。Google Developer Console に戻り、適切なリダイレクト URI で OAuth クライアントを更新してください。