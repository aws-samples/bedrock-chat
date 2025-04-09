# 外部IDプロバイダの設定

## 1ステップ: OIDCクライアントの作成

対象のOIDCプロバイダーの手順に従い、OIDCクライアントIDとシークレット値を記録しておいてください。また、次のステップで発行者URLが必要になります。設定プロセスでリダイレクトURIが必要な場合は、デプロイ完了後に置き換えられるダミー値を入力してください。

## 第2ステップ: AWS Secrets Managerに認証情報を保存

1. AWS管理コンソールに移動します。
2. Secrets Managerに移動し、「新しい秘密を保存」を選択します。
3. 「その他の種類の秘密」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアで入力します。

   - キー: `clientId`、値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`、値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`、値: <ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従って、秘密の名前と説明を入力します。CDKコードで使用する秘密の名前をメモしておきます（第3ステップの変数名 <YOUR_SECRET_NAME>で使用されます）。
6. 秘密を確認して保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl`の文字列と正確に一致する必要があります。

## 3단계: cdk.json の更新

cdk.json ファイルに ID プロバイダとシークレット名を追加します。

次のように記述します：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<YOUR_SERVICE_NAME>", // 希望する値を設定してください
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix` は、すべての Amazon Cognito ユーザー間でグローバルに一意である必要があります。他の AWS アカウントですでに使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。一意性を確保するために、識別子、プロジェクト名、または環境名をプレフィックスに含めることをお勧めします。

## 4段階: CDKスタックのデプロイ

AWS にCDKスタックをデプロイします:

```sh
npx cdk deploy --require-approval never --all
```

## 5段階: CognitoリダイレクトURIでOIDCクライアントを更新

スタックをデプロイした後、CloudFormationの出力に`AuthApprovedRedirectURI`が表示されます。OIDCの設定に戻り、正しいリダイレクトURIで更新してください。