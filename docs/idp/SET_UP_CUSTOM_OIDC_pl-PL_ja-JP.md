# 外部IDプロバイダの設定

## ステップ1: OIDCクライアントの作成

対象のOIDCプロバイダーの手順に従い、OIDCクライアントIDとそのシークレットを記録します。発行者のURLも後続のステップで必要となります。設定プロセス中にリダイレクトURIが要求される場合は、デプロイメント完了後に置き換えられる代替値を入力してください。

## ステップ2: AWS Secrets Managerで資格情報を保存する

1. AWS管理コンソールに移動します。
2. Secrets Managerに移動し、「新しいシークレットを保存」を選択します。
3. 「その他のシークレットタイプ」を選択します。
4. クライアントIDとクライアントシークレットをキーと値のペアとして入力します。

   - キー: `clientId`、値: <YOUR_GOOGLE_CLIENT_ID>
   - キー: `clientSecret`、値: <YOUR_GOOGLE_CLIENT_SECRET>
   - キー: `issuerUrl`、値: <ISSUER_URL_OF_THE_PROVIDER>

5. シークレットに名前と説明を付けるための手順に従います。CDKコード（ステップ3の <YOUR_SECRET_NAME> 変数で使用）で必要になるため、シークレット名をメモしておきます。
6. シークレットを確認して保存します。

### 注意

キー名は、`clientId`、`clientSecret`、`issuerUrl` の文字列と完全に一致する必要があります。

## ステップ3: cdk.jsonファイルの更新

cdk.jsonファイルに、以下のように身元プロバイダとシークレット名を追加します：

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
    "userPoolDomainPrefix": "<ユーザープールのグローバルにユニークなドメインプレフィックス>"
  }
}
```

### 注意

#### ユニーク性

`userPoolDomainPrefix`は、Amazon Cognitoのすべてのユーザーでグローバルにユニークである必要があります。すでに他のAWSアカウントで使用されているプレフィックスを選択すると、ユーザープールドメインの作成に失敗します。プレフィックスのユニーク性を確保するには、識別子、プロジェクト名、環境名などを追加することをお勧めします。

## ステップ4: CDKスタックのデプロイ

AWS上にCDKスタックをデプロイします：

```sh
npx cdk deploy --require-approval never --all
```

## ステップ 5：CognitoのリダイレクトURIを使用したOIDCクライアントの更新

スタックをデプロイすると、`AuthApprovedRedirectURI`がCloudFormationの出力に表示されます。OIDCの設定に戻り、正しいリダイレクトURIで更新してください。