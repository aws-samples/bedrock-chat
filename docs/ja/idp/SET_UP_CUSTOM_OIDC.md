# 外部 ID プロバイダーの設定

## ステップ 1: OIDC クライアントの作成

対象の OIDC プロバイダーの手順に従い、OIDC クライアント ID とシークレットの値を確認します。また、以降の手順で発行者 URL が必要です。セットアップ処理にリダイレクト URI が必要な場合は、デプロイ完了後に置き換えられるダミー値を入力してください。

## ステップ 2: AWS Secrets Manager に資格情報を保存

1. AWS マネジメントコンソールに移動します。
2. Secrets Manager に移動し、「新しいシークレットを保存」を選択します。
3. 「その他のタイプのシークレット」を選択します。
4. クライアント ID とクライアントシークレットをキーと値のペアで入力します。

   - キー: `clientId`、値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`、値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`、値: <ISSUER_URL_OF_THE_PROVIDER>

5. プロンプトに従ってシークレットに名前と説明を付けます。CDK コードで使用するシークレット名をメモしてください（ステップ 3 の変数名 <YOUR_SECRET_NAME> で使用）。
6. 確認してシークレットを保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl` の文字列と完全に一致する必要があります。

## ステップ 3: cdk.json を更新

cdk.json ファイルに、ID プロバイダーとシークレット名を追加します。

以下のようにします：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 変更しないでください
        "serviceName": "<YOUR_SERVICE_NAME>", // 任意の値を設定
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 注意

#### 一意性

`userPoolDomainPrefix` は、すべての Amazon Cognito ユーザーにわたってグローバルに一意である必要があります。他の AWS アカウントで既に使用されている接頭辞を選択すると、ユーザープールドメインの作成に失敗します。一意性を確保するために、識別子、プロジェクト名、環境名などを接頭辞に含めることをお勧めします。

## ステップ 4: CDK スタックをデプロイ

CDK スタックを AWS にデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5: OIDC クライアントを Cognito リダイレクト URI で更新

スタックをデプロイした後、CloudFormation の出力に `AuthApprovedRedirectURI` が表示されます。OIDC 設定に戻り、正しいリダイレクト URI で更新します。