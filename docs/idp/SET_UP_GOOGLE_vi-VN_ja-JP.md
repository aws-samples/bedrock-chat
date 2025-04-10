# Google の外部 ID プロバイダの設定

## ステップ1：Google OAuth 2.0 クライアントの作成

1. Google デベロッパーコンソールにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「Credentials」に移動し、「Create Credentials」をクリックして「OAuth client ID」を選択します。
4. プロンプトが表示されたら、同意画面を設定します。
5. アプリケーションの種類で「Web application」を選択します。
6. リダイレクトURIは今は空のままにし、後で設定します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)を参照してください。

## ステップ2: Google OAuth の認証情報を AWS Secrets Manager に保存

1. AWS Management Console にアクセスします。
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. Google OAuth の clientId と clientSecret をキーと値のペアとして入力します。

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. シークレットに名前と説明を設定する手順に従います。CDK コードで使用するため、シークレット名をメモしておきます。例: googleOAuthCredentials。（ステップ3の <YOUR_SECRET_NAME> 変数で使用）
6. シークレットを確認して保存します。

### 注意

キー名は正確に 'clientId' と 'clientSecret' の文字列である必要があります。

## ステップ3: cdk.jsonを更新する

cdk.jsonファイルに、IDプロバイダとSecretNameを次のように追加します：

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

userPoolDomainPrefixは、Amazon Cognitoのすべてのユーザーにおいて、グローバルで一意である必要があります。すでに別のAWSアカウントで使用されている接頭辞を選択すると、ユーザープールドメインの作成に失敗します。一意性を確保する良い方法は、識別子、プロジェクト名、または環境名を接頭辞に含めることです。

## ステップ4: CDKスタックのデプロイ

CDKスタックをAWSにデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ5: Google OAuth クライアントを Cognito のリダイレクトURIで更新

スタックをデプロイした後、AuthApprovedRedirectURIがCloudFormationの出力に表示されます。Google Developer Consoleに戻り、OAuth クライアントを正確なリダイレクトURIで更新します。