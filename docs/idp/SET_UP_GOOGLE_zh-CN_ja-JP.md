# Google の外部 ID プロバイダの設定

## 手順1：Google OAuth 2.0クライアントを作成する

1. Googleデベロッパーコンソールに移動します。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして「OAuth クライアントID」を選択します。
4. 求められた場合、同意画面を設定します。
5. アプリケーションタイプで「ウェブアプリケーション」を選択します。
6. リダイレクトURIは一時的に空のままにし、後で設定します。[手順5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Google公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## 手順2：AWS Secrets ManagerにGoogle OAuth認証情報を保存する

1. AWS管理コンソールにログインします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. キーと値のペアでGoogle OAuth認証情報のclientIdとclientSecretを入力します。

   1. キー：clientId、値：<YOUR_GOOGLE_CLIENT_ID>
   2. キー：clientSecret、値：<YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。後でCDKコードで使用するため、シークレット名をメモしておいてください。例えば、googleOAuthCredentials。（手順3で変数名<YOUR_SECRET_NAME>として使用）
6. 内容を確認し、シークレットを保存します。

### 注意

キー名は、文字列'clientId'と'clientSecret'と完全に一致する必要があります。

## 手順3：cdk.json の更新

cdk.json ファイルに、ID プロバイダーとシークレット名を追加します。

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

userPoolDomainPrefix は、すべての Amazon Cognito ユーザー間でグローバルにユニークである必要があります。選択したプレフィックスが他の AWS アカウントで既に使用されている場合、ユーザープールドメインの作成は失敗します。最適な方法は、プレフィックスに識別子、プロジェクト名、または環境名を含めることで、ユニーク性を確保することです。

## ステップ 4：CDKスタックのデプロイ

CDKスタックをAWSにデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## 手順5：CognitoのリダイレクトURIを使用してGoogleのOAuthクライアントを更新

スタックをデプロイした後、AuthApprovedRedirectURIがCloudFormationの出力に表示されます。Google開発者コンソールに戻り、正しいリダイレクトURIを使用してOAuthクライアントを更新します。