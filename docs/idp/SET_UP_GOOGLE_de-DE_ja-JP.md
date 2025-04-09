# Google用の外部IDプロバイダの設定

## ステップ1：Google OAuth 2.0 クライアントを作成

1. Google Developer Consoleにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックして、「OAuth クライアントID」を選択します。
4. プロンプトが表示されたら、同意画面を設定します。
5. アプリケーションタイプで「ウェブアプリケーション」を選択します。
6. リダイレクトURIは後で設定するため、現時点では空のままにし、一時的に保存します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモしておきます。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)を参照してください。

## ステップ 2: Google OAuth認証情報をAWS Secrets Managerに保存

1. AWS Management Consoleを開きます。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. Google OAuth clientIdとclientSecretをキーと値のペアで入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで必要になるため、シークレット名を控えておいてください。例：googleOAuthCredentials。（ステップ 3 では <YOUR_SECRET_NAME> 変数名を使用します）
6. シークレットを確認して保存します。

### 注意

キー名は正確に「clientId」と「clientSecret」の文字列と一致する必要があります。

## ステップ 3: cdk.jsonの更新

cdk.json ファイルに、IDプロバイダとシークレット名を以下のように追加します：

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

#### 一意性

userPoolDomainPrefixは、すべてのAmazon Cognitoユーザープールにおいてグローバルに一意である必要があります。既に別のAWSアカウントで使用されている接頭辞を選択すると、ユーザープールドメインの作成に失敗します。識別子、プロジェクト名、または環境名を接頭辞に含めることで、一意性を確保するのがベストプラクティスです。

## ステップ4: CDKスタックのデプロイ

AWS に CDK スタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Google OAuth クライアントを Cognito リダイレクト URI に更新する

スタックのデプロイ後、CloudFormation の出力に `AuthApprovedRedirectURI` が表示されます。Google Developer Console に戻り、OAuth クライアントを正しいリダイレクト URI で更新します。