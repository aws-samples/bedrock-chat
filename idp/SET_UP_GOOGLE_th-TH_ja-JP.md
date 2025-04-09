# Google用の外部認証プロバイダの設定

## ステップ 1: Google OAuth 2.0 クライアントの作成

1. Google 開発者コンソールにアクセスします
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します
3. 「認証情報」に移動し、「認証情報を作成」をクリックして「OAuth クライアントID」を選択します
4. プロンプトが表示された場合、同意画面を設定します
5. アプリケーションの種類を「ウェブアプリケーション」に選択します
6. リダイレクト URI は後で設定するため、一時的に空白のままにしておきます [ステップ 5 を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成が完了したら、クライアントID とクライアントシークレットをメモします

詳細については、[Google の公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ2: Google OAuth の資格情報を AWS Secrets Manager に保存する

1. AWS Management Console にアクセスする
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択する
3. 「その他の種類のシークレット」を選択する
4. Google OAuth の clientId と clientSecret をキーと値のペアで入力する

   1. キー: clientId、値: <YOUR_GOOGLE_CLIENT_ID>
   2. キー: clientSecret、値: <YOUR_GOOGLE_CLIENT_SECRET>

5. 指示に従ってシークレットに名前と説明を付ける。CDK コードで後で使用するため、シークレット名をメモしておく。例: googleOAuthCredentials（ステップ3の変数 <YOUR_SECRET_NAME> で使用）
6. シークレットを確認して保存する

### 注意

キー名は厳密に 'clientId' と 'clientSecret' の文字列と一致する必要があります。

## ステップ3: cdk.jsonの更新

cdk.jsonファイルに、ID プロバイダとSecretNameを追加します：

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
    "userPoolDomainPrefix": "<User Poolのグローバルにユニークなドメイン接頭辞>"
  }
}
```

### 注意事項

#### ユニーク性

User Poolのドメイン接頭辞は、Amazon Cognito内でグローバルにユニークである必要があります。他のAWSアカウントですでに使用されている接頭辞を選択すると、User Poolドメインの作成に失敗します。ベストプラクティスは、識別子、プロジェクト名、または環境名を接頭辞に含めることで、ユニーク性を確保することです。

## ステップ4: CDKスタックのデプロイ

AWS に CDK スタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: CognitoのリダイレクトURIsを使用してGoogleのOAuthクライアントを更新

CloudFormationのスタックをデプロイした後、AuthApprovedRedirectURIが結果に表示されます。Googleの開発者コンソールに戻り、正しいリダイレクトURIsを使用してOAuthクライアントを更新してください。