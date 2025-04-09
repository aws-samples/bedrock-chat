# Google用の外部IDプロバイダの設定

## 第1ステップ: Google OAuth 2.0クライアントの作成

1. Google開発者コンソールに移動してください。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択してください。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして、「OAuth クライアントID」を選択してください。
4. メッセージが表示されたら、同意画面を構成してください。
5. アプリケーションタイプで「Webアプリケーション」を選択してください。
6. 後で設定するリダイレクトURIは、今は空のままで一時保存してください。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモしておいてください。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)を参照してください。

## 第2ステップ: Google OAuth資格情報をAWS Secrets Managerに保存

1. AWS管理コンソールに移動します。
2. Secrets Managerに移動し、「新しい秘密を保存」を選択します。
3. 「その他の種類の秘密」を選択します。
4. Google OAuth clientIdとclientSecretをキー値ペアとして入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従って、秘密の名前と説明を入力します。CDKコードで使用する秘密の名前をメモしておきます。例えば、googleOAuthCredentials。（第3ステップで<YOUR_SECRET_NAME>変数名として使用）
6. 秘密を確認して保存します。

### 注意

キー名は、正確に'clientId'と'clientSecret'の文字列と一致する必要があります。

## 3단계: cdk.json の更新

cdk.json ファイルに ID プロバイダーと SecretName を追加してください。

次のように記述します：

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

userPoolDomainPrefix は、すべての Amazon Cognito ユーザー間でグローバルに一意である必要があります。すでに他の AWS アカウントで使用されている接頭辞を選択すると、ユーザープールドメインの作成が失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名を接頭辞に含めることをお勧めします。

## 第4段階: CDKスタックのデプロイ

AWS上にCDKスタックをデプロイします:

```sh
npx cdk deploy --require-approval never --all
```

## 第5ステップ: Cognito リダイレクトURIでGoogle OAuthクライアントを更新

スタックをデプロイした後、CloudFormationの出力から`AuthApprovedRedirectURI`が表示されます。Google開発者コンソールに戻り、正しいリダイレクトURIでOAuthクライアントを更新してください。