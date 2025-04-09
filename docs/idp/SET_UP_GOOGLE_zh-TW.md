# 設定 Google 外部身份提供者

## 步驟1：建立 Google OAuth 2.0 用戶端

1. 前往 Google 開發者控制台。
2. 建立新專案或選擇現有專案。
3. 導覽至「憑證」，然後點擊「建立憑證」並選擇「OAuth 用戶端 ID」。
4. 如出現提示，設定同意畫面。
5. 應用程式類型，選擇「Web 應用程式」。
6. 暫時將重新導向 URI 留空，稍後再設定。[請參閱步驟5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 建立完成後，記下用戶端 ID 和用戶端密鑰。

欲了解詳細資訊，請瀏覽 [Google 官方文件](https://support.google.com/cloud/answer/6158849?hl=en)

## 步驟 2：在 AWS Secrets Manager 中儲存 Google OAuth 憑證

1. 進入 AWS 管理主控台。
2. 導覽至 Secrets Manager 並選擇「儲存新的密鑰」。
3. 選擇「其他類型的密鑰」。
4. 輸入 Google OAuth clientId 和 clientSecret 作為鍵值對。

   1. 鍵：clientId，值：<YOUR_GOOGLE_CLIENT_ID>
   2. 鍵：clientSecret，值：<YOUR_GOOGLE_CLIENT_SECRET>

5. 按照提示為密鑰命名和描述。記下密鑰名稱，因為您將在 CDK 程式碼中使用它。例如，googleOAuthCredentials（在步驟 3 中使用變數名稱 <YOUR_SECRET_NAME>）
6. 檢查並儲存密鑰。

### 注意

鍵名必須完全符合 'clientId' 和 'clientSecret' 字串。

## 步驟 3：更新 cdk.json

在您的 cdk.json 檔案中，新增身份提供者和密鑰名稱：

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

### 注意

#### 唯一性

userPoolDomainPrefix 必須在所有 Amazon Cognito 使用者中全域唯一。如果您選擇的前綴已被其他 AWS 帳戶使用，使用者池域的建立將會失敗。建議在前綴中包含識別碼、專案名稱或環境名稱，以確保唯一性。

## 步驟 4：部署您的 CDK 堆疊

使用以下指令將 CDK 堆疊部署到 AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步驟 5：使用 Cognito 重新導向 URI 更新 Google OAuth 用戶端

在部署堆疊後，AuthApprovedRedirectURI 會顯示在 CloudFormation 輸出中。返回 Google 開發者控制台，並使用正確的重新導向 URI 更新 OAuth 用戶端。