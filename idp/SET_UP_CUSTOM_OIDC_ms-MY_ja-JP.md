# 外部アイデンティティプロバイダの設定

## ステップ1: OIDCクライアントを作成

対象のOIDCプロバイダーの手順に従い、OIDCクライアントIDとシークレットの値を記録します。発行者のURLも次のステップで必要になります。リダイレクトURIが設定プロセスで必要な場合は、デプロイ完了後に置き換える一時的な値を入力してください。

## ステップ2: AWS Secrets Managerで認証情報を保存

1. AWS Management Consoleにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他のタイプのシークレット」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアとして入力します。

   - キー: `clientId`、値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`、値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`、値: <ISSUER_URL_OF_THE_PROVIDER>

5. シークレットに名前を付け、説明するための手順に従います。CDKコードで使用する（ステップ3の <YOUR_SECRET_NAME> 変数名で使用）ので、シークレット名をメモしてください。
6. シークレットを確認し、保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl` の文字列と完全に一致する必要があります。

## ステップ 3: cdk.json の更新

cdk.json ファイルで、プロバイダー ID と SecretName を追加します。

以下のようになります：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<あなたのサービス名>", // 好きな値を設定してください
        "secretName": "<あなたのシークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールの一意のドメインプレフィックス>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix` は、すべての Amazon Cognito ユーザー間でグローバルに一意である必要があります。他の AWS アカウントですでに使用されているプレフィックスを選択すると、ユーザープールドメインの生成に失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ 4: CDKスタックのデプロイ

AWS にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: CognitoのリダイレクトURIを使用してOIDCクライアントを更新

スタックの実行後、`AuthApprovedRedirectURI`がCloudFormationの出力に表示されます。OIDCの設定に戻り、正しいリダイレクトURIで更新してください。