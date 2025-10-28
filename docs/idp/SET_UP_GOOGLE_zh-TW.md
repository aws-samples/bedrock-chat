# 設定 Google 外部身分提供者

## 步驟 1：建立 Google OAuth 2.0 客戶端

1. 前往 Google Developer Console。
2. 建立新專案或選擇現有專案。
3. 導航至「憑證」，然後點擊「建立憑證」並選擇「OAuth client ID」。
4. 如果出現提示，請設定同意畫面。
5. 在應用程式類型中，選擇「網頁應用程式」。
6. 暫時將重定向 URI 留空，稍後再設定。[參見步驟5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 建立完成後，記下用戶端 ID 和用戶端密鑰。

詳細資訊請參考 [Google 官方文件](https://support.google.com/cloud/answer/6158849?hl=en)

## 步驟 2：將 Google OAuth 憑證儲存在 AWS Secrets Manager

1. 前往 AWS Management Console。
2. 導航至 Secrets Manager 並選擇「儲存新密鑰」。
3. 選擇「其他類型的密鑰」。
4. 以鍵值對的形式輸入 Google OAuth clientId 和 clientSecret。

   1. 鍵：clientId，值：<YOUR_GOOGLE_CLIENT_ID>
   2. 鍵：clientSecret，值：<YOUR_GOOGLE_CLIENT_SECRET>

5. 按照提示為密鑰命名並描述。請記下密鑰名稱，因為您將在 CDK 程式碼中需要它。例如：googleOAuthCredentials（在步驟 3 中使用變數名稱 <YOUR_SECRET_NAME>）
6. 檢查並儲存密鑰。

### 注意事項

鍵名必須完全匹配字串 'clientId' 和 'clientSecret'。

## 步驟 3：更新 cdk.json

在您的 cdk.json 檔案中，加入身分提供者 ID 和密鑰名稱到 cdk.json 檔案中。

如下所示：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 注意事項

#### 唯一性

userPoolDomainPrefix 必須在所有 Amazon Cognito 使用者中保持全域唯一性。如果您選擇的前綴已被其他 AWS 帳戶使用，則使用者集區網域的建立將會失敗。建議在前綴中包含識別碼、專案名稱或環境名稱，以確保唯一性。

## 步驟 4：部署您的 CDK 堆疊

將您的 CDK 堆疊部署到 AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步驟 5：使用 Cognito 重定向 URI 更新 Google OAuth 客戶端

部署堆疊後，CloudFormation 輸出中會顯示 AuthApprovedRedirectURI。回到 Google 開發者控制台，並使用正確的重定向 URI 更新 OAuth 客戶端。