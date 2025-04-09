# Google向けの外部IDプロバイダの設定

## ステップ1：Google OAuth 2.0クライアントの作成

1. Google開発者コンソールにアクセスします。
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します。
3. 「認証情報」に移動し、「認証情報を作成」をクリックし、「OAuthクライアントID」を選択します。
4. プロンプトが表示されたら、同意画面を設定します。
5. アプリケーションタイプで「Webアプリケーション」を選択します。
6. リダイレクトURIは現時点では空のままにし、後で設定します。[ステップ5を参照](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 作成後、クライアントIDとクライアントシークレットをメモします。

詳細については、[Googleの公式ドキュメント](https://support.google.com/cloud/answer/6158849?hl=en)をご覧ください。

## ステップ 2: Google OAuth 認証情報を AWS Secrets Manager に保存する

1. AWS 管理コンソールにアクセスします。
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択します。
3. 「その他のシークレットタイプ」を選択します。
4. Google OAuth のクライアント ID とクライアントシークレットをキーと値のペアとして入力します。

   1. キー: clientId、値: <あなたのGoogleクライアントID>
   2. キー: clientSecret、値: <あなたのGoogleクライアントシークレット>

5. シークレットに名前と説明を付けるための手順に従います。CDK コードで必要になるため、シークレット名を控えておいてください。例えば、googleOAuthCredentials のようなもの。（ステップ 3 の <あなたのシークレット名> 変数で使用）
6. シークレットを確認して保存します。

### 注意

キー名は、正確に 'clientId' と 'clientSecret' の文字列と一致する必要があります。

## ステップ 3: cdk.jsonファイルの更新

cdk.jsonファイルにアイデンティティプロバイダーとシークレット名を追加します。

次のように：

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
    "userPoolDomainPrefix": "<ユーザープールのためのユニークなドメインプレフィックス>"
  }
}
```

### 注意

#### ユニーク性

userPoolDomainPrefixは、Amazon Cognitoのすべてのユーザー間でグローバルにユニークである必要があります。すでに他のAWSアカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。識別子、プロジェクト名、または環境名をプレフィックスに含めることで、ユニーク性を確保するのがベストプラクティスです。

## ステップ4: CDKスタックのデプロイ

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Cognito のリダイレクト URI で Google OAuth クライアントを更新

スタックをデプロイした後、AuthApprovedRedirectURI が CloudFormation の出力に表示されます。Google Developer Console に戻り、OAuth クライアントを正しいリダイレクト URI で更新します。