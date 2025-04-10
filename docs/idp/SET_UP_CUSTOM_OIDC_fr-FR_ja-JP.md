# 外部アイデンティティプロバイダーの設定

## ステップ 1: OIDC クライアントの作成

対象の OIDC プロバイダーの手順に従い、OIDC クライアント ID とシークレットの値を記録してください。発行者の URL も次のステップで必要になります。設定プロセス中にリダイレクト URI が必要な場合は、デプロイ完了後に置き換えられる仮の値を入力してください。

## ステップ2：AWS Secrets Managerに認証情報を保存する

1. AWS管理コンソールにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他のタイプのシークレット」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアで入力します。

   - キー：`clientId`、値：<YOUR_GOOGLE_CLIENT_ID>
   - キー：`clientSecret`、値：<YOUR_GOOGLE_CLIENT_SECRET>
   - キー：`issuerUrl`、値：<ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDKコードで必要になるので、シークレット名を必ず控えておいてください（ステップ3で <YOUR_SECRET_NAME> 変数名として使用）。
6. シークレットを確認して保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl`の文字列と完全に一致する必要があります。

## ステップ3：cdk.jsonの更新

cdk.jsonファイルに、IDプロバイダーとシークレット名を以下のように追加します：

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
    "userPoolDomainPrefix": "<ユーザープールの一意のドメインプレフィックス>"
  }
}
```

### 注意

#### ユニーク性

`userPoolDomainPrefix`は、すべてのAmazon Cognitoユーザー間でグローバルに一意である必要があります。すでに他のAWSアカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。プレフィックスの一意性を保証するために、識別子、プロジェクト名、または環境名を含めることをお勧めします。

## ステップ 4: CDKスタックのデプロイ

AWS上にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ5：CognitoのリダイレクトURIを使用してOIDCクライアントを更新

スタックをデプロイした後、`AuthApprovedRedirectURI`がCloudFormationの出力に表示されます。OIDCの設定に戻り、正しいリダイレクトURIに更新してください。