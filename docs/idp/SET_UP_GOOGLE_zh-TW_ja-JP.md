# Google の外部 ID プロバイダの設定

## ステップ1：Google OAuth 2.0 クライアントを作成する

1. Google 開発者コンソールにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして「OAuth クライアントID」を選択します。
4. 求められた場合、同意画面を設定します。
5. アプリケーションの種類で、「Web アプリケーション」を選択します。
6. リダイレクトURIは一時的に空白のままにし、後で設定します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Google 公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## 手順 2：AWS Secrets Manager に Google OAuth 認証情報を保存する

1. AWS マネジメントコンソールにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. キーと値のペアで Google OAuth のクライアントIDとクライアントシークレットを入力します。

   1. キー：clientId、値：<YOUR_GOOGLE_CLIENT_ID>
   2. キー：clientSecret、値：<YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで使用するため、シークレット名を必ず控えておいてください。例えば、googleOAuthCredentials。（ステップ3で変数名 <YOUR_SECRET_NAME> を使用）
6. 内容を確認し、シークレットを保存します。

### 注意

キー名は、'clientId' と 'clientSecret' の文字列と完全に一致する必要があります。

## ステップ 3：cdk.json の更新

cdk.json ファイルに、IDプロバイダーとシークレット名を追加します：

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

userPoolDomainPrefix は、すべての Amazon Cognito ユーザープール間でグローバルに一意である必要があります。選択した接頭辞が別の AWS アカウントで既に使用されている場合、ユーザープールドメインの作成は失敗します。最良の方法は、接頭辞に識別子、プロジェクト名、または環境名を含めて、一意性を確保することです。

## ステップ 4：CDKスタックのデプロイ

CDKスタックをAWSにデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5：Cognito のリダイレクト URI で Google OAuth クライアントを更新

スタックをデプロイした後、AuthApprovedRedirectURI が CloudFormation の出力に表示されます。Google 開発者コンソールに戻り、正しいリダイレクト URI で OAuth クライアントを更新します。