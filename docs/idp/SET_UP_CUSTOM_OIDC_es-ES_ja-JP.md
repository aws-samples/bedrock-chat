# 外部アイデンティティプロバイダの設定

## ステップ1: OIDCクライアントの作成

対象のOIDCプロバイダーの手順に従い、OIDCクライアントIDとシークレットの値を記録してください。以降のステップでは、発行者のURLも必要になります。設定プロセス中にリダイレクトURIが必要な場合は、実装完了後に置き換えられる仮のURIを入力してください。

## ステップ2: AWS Secrets Managerに認証情報を保存する

1. AWS管理コンソールに移動します。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアとして入力します。

   - キー: `clientId`、値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`、値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`、値: <ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従ってシークレットに名前と説明を付けます。シークレット名をメモしておいてください。CDKコードで後で使用します（ステップ3の <YOUR_SECRET_NAME> 変数名で使用）。
6. シークレットを確認して保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl`の文字列と完全に一致する必要があります。

## ステップ3: cdk.jsonの更新

cdk.jsonファイルに、IDプロバイダとシークレット名を次のように追加します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<サービス名>", // 任意の値を設定してください
        "secretName": "<シークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールの一意のドメインプレフィックス>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix`は、Amazon Cognitoのすべてのユーザーで一意である必要があります。既に別のAWSアカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。一意性を保証するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## ステップ4: CDKスタックのデプロイ

AWS上でCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: Cognito のリダイレクト URI で OIDC クライアントを更新

スタックをデプロイした後、`AuthApprovedRedirectURI` が CloudFormation の出力に表示されます。OIDC の設定に戻り、正しいリダイレクト URI で更新してください。