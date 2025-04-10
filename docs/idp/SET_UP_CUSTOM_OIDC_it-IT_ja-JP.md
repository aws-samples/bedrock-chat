# 外部アイデンティティプロバイダーの設定

## ステップ1：OIDCクライアントの作成

対象のOIDCプロバイダーの手順に従い、OIDCクライアントIDとシークレットの値を記録してください。また、発行者のURLは後続のステップで必要になります。設定プロセス中にリダイレクトURIが要求された場合は、デプロイメント完了後に置き換えられる仮のURIを入力してください。

## ステップ 2: AWS Secrets Manager に認証情報を保存

1. AWS Management Console にログインします。
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択します。
3. 「その他のタイプのシークレット」を選択します。
4. クライアント ID とクライアントシークレットをキーと値のペアとして入力します。

   - キー: `clientId`、値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`、値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`、値: <ISSUER_URL_OF_THE_PROVIDER>

5. シークレットに名前と説明を付けるための手順に従います。CDKコードで使用するシークレット名をメモしておいてください（ステップ 3 で <YOUR_SECRET_NAME> として使用）。
6. シークレットを確認して保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl` の文字列と完全に一致する必要があります。

## ステップ3: cdk.jsonの更新

cdk.jsonファイルに、プロバイダーIDとSecretNameを次のように追加します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<あなたのサービス名>", // 任意の値を設定
        "secretName": "<あなたのシークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールに一意のドメイン接頭辞>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix`は、すべてのAmazon Cognitoユーザー間でグローバルに一意である必要があります。既に別のAWSアカウントで使用されている接頭辞を選択すると、ユーザープールドメインの作成に失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名を接頭辞に含めることをお勧めします。

## ステップ4: CDKスタックのデプロイ

AWS上にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ5: CognitoのリダイレクトURIでOIDCクライアントを更新

スタックをデプロイした後、`AuthApprovedRedirectURI`がCloudFormationの出力に表示されます。OIDCの設定に戻り、正しいリダイレクトURIで更新してください。