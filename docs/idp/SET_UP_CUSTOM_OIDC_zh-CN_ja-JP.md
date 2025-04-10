# 外部IDプロバイダの設定

## ステップ1：OIDCクライアントの作成

対象のOIDCプロバイダーの手順に従い、OIDCクライアントIDとシークレットの値を記録します。後続のステップでは、発行者URLも必要になります。セットアップ中にリダイレクトURIが必要な場合は、デプロイ後に置き換える仮のURIを入力してください。

## ステップ2：AWS Secrets Managerに認証情報を保存する

1. AWS管理コンソールにアクセスします。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他の種類のシークレット」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアとして入力します。

   - キー：`clientId`、値：<YOUR_GOOGLE_CLIENT_ID>
   - キー：`clientSecret`、値：<YOUR_GOOGLE_CLIENT_SECRET>
   - キー：`issuerUrl`、値：<ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従って、シークレットに名前と説明を付けます。CDKコードで使用するため、シークレット名をメモしてください（ステップ3で使用される変数名は<YOUR_SECRET_NAME>です）。
6. 内容を確認し、シークレットを保存します。

### 注意

キー名は、文字列 `clientId`、`clientSecret`、`issuerUrl` と完全に一致する必要があります。

## 步骤3：cdk.json の更新

cdk.json ファイルに、ID プロバイダとシークレット名を追加します。

以下のようになります：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<サービス名>", // 任意の値を設定できます
        "secretName": "<シークレット名>"
      }
    ],
    "userPoolDomainPrefix": "<ユーザープールの一意のドメインプレフィックス>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix` は、すべての Amazon Cognito ユーザー間でグローバルに一意である必要があります。選択したプレフィックスが他の AWS アカウントで既に使用されている場合、ユーザープールドメインの作成は失敗します。ベストプラクティスは、識別子、プロジェクト名、または環境名をプレフィックスに含めて、一意性を確保することです。

## ステップ 4：CDKスタックのデプロイ

次のコマンドを使用して、CDKスタックをAWSにデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ5：CognitoリダイレクトURIを使用してOIDCクライアントを更新

スタックをデプロイした後、`AuthApprovedRedirectURI`はCloudFormationの出力に表示されます。OIDCの設定に戻り、正しいリダイレクトURIで更新してください。