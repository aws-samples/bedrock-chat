# Google用の外部IDプロバイダーを設定する

## 前提条件

- Okta、Azure AD、Google Workspace などの外部 ID プロバイダー
- Google Cloud コンソールへの管理者アクセス

## 手順

1. Google Cloud コンソールにログインします

2. ID プロバイダーを設定:
   - **セキュリティ** > **ID 管理** に移動
   - 「外部 ID プロバイダーの追加」をクリック

3. ID プロバイダーの詳細を構成:
   - プロバイダー名を入力
   - メタデータ URL またはメタデータファイルをアップロード
   - 必要な属性マッピングを設定

4. 接続を検証:
   - テストユーザーでサインインを試行
   - 属性が正しくマッピングされていることを確認

## 注意事項

- セキュリティ設定を慎重に確認
- 最小権限の原則に従う
- 定期的に接続を監査

## ステップ1：Google OAuth 2.0 クライアントを作成する

1. Google Cloud Consoleに移動します。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして、「OAuth クライアントID」を選択します。
4. プロンプトが表示されたら、同意画面を設定します。
5. アプリケーションの種類で、「ウェブアプリケーション」を選択します。
6. リダイレクトURIは一時的に空白のままにします。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Google公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ 2: Google OAuth の認証情報を AWS Secrets Manager に保存する

1. AWS Management Console にアクセスします。
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. Google OAuth の clientId と clientSecret をキーと値のペアとして入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. シークレットに名前を付け、説明を追加するための手順に従います。後で CDK コードで使用するため、シークレット名をメモしておきます。例: googleOAuthCredentials（ステップ 3 の <YOUR_SECRET_NAME> 変数で使用）
6. シークレットを確認して保存します。

### 注意

キー名は、'clientId' と 'clientSecret' の文字列と完全に一致する必要があります。

## ステップ 3: cdk.json の更新

cdk.json ファイルで、プロバイダー ID と SecretName を追加します。

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
    "userPoolDomainPrefix": "<ユーザープールの一意のドメイン接頭辞>"
  }
}
```

### 注意

#### ユニーク性

userPoolDomainPrefix は、Amazon Cognito のすべてのユーザー間でグローバルに一意である必要があります。既に使用されている接頭辞を選択すると、ユーザープールドメインの作成が失敗します。識別子、プロジェクト名、または環境名を接頭辞に含めて、一意性を確保することをお勧めします。

## ステップ 4: CDKスタックをデプロイする

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Cognito のリダイレクト URI で Google OAuth クライアントを更新

スタックを使用した後、CloudFormation の出力に AuthApprovedRedirectURI が表示されます。Google デベロッパーコンソールに戻り、正しいリダイレクト URI で OAuth クライアントを更新します。