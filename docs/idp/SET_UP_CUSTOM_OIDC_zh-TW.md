# 設定外部身分提供者

## 步驟 1：建立 OIDC 用戶端

按照目標 OIDC 提供者的程序進行操作，並記下 OIDC 用戶端 ID 和密鑰的值。在後續步驟中還需要簽發者 URL。如果在設定過程中需要重新導向 URI，請輸入臨時值，這些值將在部署完成後被替換。

## 步驟 2：在 AWS Secrets Manager 中儲存憑證

1. 前往 AWS Management Console。
2. 導航至 Secrets Manager 並選擇「儲存新機密」。
3. 選擇「其他類型的機密」。
4. 以鍵值對的形式輸入用戶端 ID 和用戶端密鑰。

   - 鍵：`clientId`，值：<YOUR_GOOGLE_CLIENT_ID>
   - 鍵：`clientSecret`，值：<YOUR_GOOGLE_CLIENT_SECRET>
   - 鍵：`issuerUrl`，值：<ISSUER_URL_OF_THE_PROVIDER>

5. 依照提示為機密命名並描述。請記下機密名稱，因為您將在 CDK 程式碼中需要它（用於步驟 3 變數名稱 <YOUR_SECRET_NAME>）。
6. 檢查並儲存機密。

### 注意

鍵名必須與字串 `clientId`、`clientSecret` 和 `issuerUrl` 完全相符。

## 步驟 3: 更新 cdk.json

在您的 cdk.json 檔案中，加入身分提供者（ID Provider）和密碼名稱（SecretName）。

如下所示：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 請勿更改
        "serviceName": "<YOUR_SERVICE_NAME>", // 設定任何您喜歡的值
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 注意事項

#### 唯一性

`userPoolDomainPrefix` 必須在所有 Amazon Cognito 使用者中保持全域唯一性。如果您選擇的前綴已被其他 AWS 帳戶使用，使用者池網域的建立將會失敗。建議在前綴中加入識別碼、專案名稱或環境名稱，以確保唯一性。

## 步驟 4：部署您的 CDK 堆疊

將您的 CDK 堆疊部署到 AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步驟 5：使用 Cognito 重新導向 URI 更新 OIDC 客戶端

在部署堆疊後，CloudFormation 輸出中會顯示 `AuthApprovedRedirectURI`。返回您的 OIDC 設定並使用正確的重新導向 URI 進行更新。