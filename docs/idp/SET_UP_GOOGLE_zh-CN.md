# 为 Google 设置外部身份提供者

## 步骤1：创建Google OAuth 2.0客户端

1. 进入Google开发者控制台。
2. 创建新项目或选择现有项目。
3. 导航至"凭据"，然后点击"创建凭据"并选择"OAuth客户端ID"。
4. 如果提示，配置同意屏幕。
5. 对于应用程序类型，选择"Web应用程序"。
6. 现在暂时将重定向URI留空，稍后再设置。[请参见步骤5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 创建完成后，记下客户端ID和客户端密钥。

有关详细信息，请访问[Google官方文档](https://support.google.com/cloud/answer/6158849?hl=en)

## 步骤 2：在 AWS Secrets Manager 中存储 Google OAuth 凭据

1. 进入 AWS 管理控制台。
2. 导航到 Secrets Manager 并选择"存储新的密钥"。
3. 选择"其他类型的密钥"。
4. 以键值对的形式输入 Google OAuth clientId 和 clientSecret。

   1. 键：clientId，值：<YOUR_GOOGLE_CLIENT_ID>
   2. 键：clientSecret，值：<YOUR_GOOGLE_CLIENT_SECRET>

5. 按照提示为密钥命名和描述。记下密钥名称，因为您将在 CDK 代码中使用它。例如，googleOAuthCredentials。（在步骤 3 中使用变量名 <YOUR_SECRET_NAME>）
6. 检查并存储密钥。

### 注意

键名必须完全匹配字符串 'clientId' 和 'clientSecret'。

## 步骤3：更新 cdk.json

在您的 cdk.json 文件中，添加身份提供程序和密钥名称。

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

### 注意

#### 唯一性

userPoolDomainPrefix 必须在所有 Amazon Cognito 用户中全局唯一。如果您选择的前缀已被其他 AWS 账户使用，用户池域的创建将失败。最好在前缀中包含标识符、项目名称或环境名称，以确保唯一性。

## 步骤4：部署您的CDK堆栈

部署您的CDK堆栈到AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步骤 5：使用 Cognito 重定向 URI 更新 Google OAuth 客户端

部署堆栈后，AuthApprovedRedirectURI 将显示在 CloudFormation 输出中。返回 Google 开发者控制台，使用正确的重定向 URI 更新 OAuth 客户端。