# 設定外部身份提供者

## 步驟 1：建立 OIDC 用戶端

依照目標 OIDC 提供者的程序，並記下 OIDC 用戶端 ID 和密鑰的值。後續步驟還需要簽發者 URL。如果設定過程需要重新導向 URI，可以先輸入虛擬值，並在部署完成後進行替換。

## 步驟 2：在 AWS Secrets Manager 中儲存憑證

1. 進入 AWS 管理主控台。
2. 導航至 Secrets Manager 並選擇「儲存新的密鑰」。
3. 選擇「其他類型的密鑰」。
4. 輸入用戶端 ID 和用戶端密鑰作為鍵值對。

   - 鍵：`clientId`，值：<YOUR_GOOGLE_CLIENT_ID>
   - 鍵：`clientSecret`，值：<YOUR_GOOGLE_CLIENT_SECRET>
   - 鍵：`issuerUrl`，值：<ISSUER_URL_OF_THE_PROVIDER>

5. 依照提示為密鑰命名並加以描述。記下密鑰名稱，因為您將在 CDK 程式碼中需要它（在步驟 3 中使用的變數名稱 <YOUR_SECRET_NAME>）。
6. 檢閱並儲存密鑰。

### 注意

鍵名必須完全符合字串 `clientId`、`clientSecret` 和 `issuerUrl`。

## 步驟 3：更新 cdk.json

在您的 cdk.json 檔案中，新增身份提供者和秘密名稱。

如下所示：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 請勿更改
        "serviceName": "<您的服務名稱>", // 可以設定任何您喜歡的值
        "secretName": "<您的秘密名稱>"
      }
    ],
    "userPoolDomainPrefix": "<您的用戶池域名前綴>"
  }
}
```

### 注意

#### 唯一性

`userPoolDomainPrefix` 必須在所有 Amazon Cognito 使用者中全域唯一。如果您選擇的前綴已被其他 AWS 帳戶使用，則建立用戶池域名將會失敗。建議在前綴中包含識別碼、專案名稱或環境名稱，以確保唯一性。

## 步驟 4：部署您的 CDK 堆疊

將您的 CDK 堆疊部署到 AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步驟 5：使用 Cognito 重新導向 URI 更新 OIDC 用戶端

部署堆疊後，`AuthApprovedRedirectURI` 將顯示在 CloudFormation 輸出中。返回您的 OIDC 設定，並使用正確的重新導向 URI 進行更新。