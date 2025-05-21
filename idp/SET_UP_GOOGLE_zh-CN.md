# 为 Google 设置外部身份提供者

## 步骤 1：创建 Google OAuth 2.0 客户端

1. 转到 Google 开发者控制台。
2. 创建新项目或选择现有项目。
3. 导航到"凭据"，然后点击"创建凭据"并选择"OAuth 客户端 ID"。
4. 如果提示，配置同意屏幕。
5. 对于应用程序类型，选择"Web 应用程序"。
6. 暂时将重定向 URI 留空，以便稍后设置，并临时保存。[请参见步骤5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 创建后，记下客户端 ID 和客户端密钥。

详细信息，请访问 [Google 官方文档](https://support.google.com/cloud/answer/6158849?hl=en)

## 步骤2：在AWS Secrets Manager中存储Google OAuth凭证

1. 进入AWS管理控制台。
2. 导航到Secrets Manager并选择"存储新密钥"。
3. 选择"其他类型的密钥"。
4. 以键值对的形式输入Google OAuth的clientId和clientSecret。

   1. 键：clientId，值：<YOUR_GOOGLE_CLIENT_ID>
   2. 键：clientSecret，值：<YOUR_GOOGLE_CLIENT_SECRET>

5. 按照提示为密钥命名和描述。记下密钥名称，因为你将在CDK代码中使用它。例如，googleOAuthCredentials。（在步骤3中使用变量名<YOUR_SECRET_NAME>）
6. 查看并存储密钥。

### 注意

键名必须完全匹配字符串'clientId'和'clientSecret'。

## 步骤3：更新 cdk.json

在您的 cdk.json 文件中，添加身份提供商和秘密名称：

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

userPoolDomainPrefix 在所有 Amazon Cognito 用户中必须全局唯一。如果选择的前缀已被其他 AWS 账户使用，用户池域的创建将失败。最佳实践是在前缀中包含标识符、项目名称或环境名称，以确保唯一性。

## 步骤4：部署您的CDK堆栈

使用以下命令将CDK堆栈部署到AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步骤 5：使用 Cognito 重定向 URI 更新 Google OAuth 客户端

部署堆栈后，AuthApprovedRedirectURI 将显示在 CloudFormation 输出中。返回 Google 开发者控制台，并使用正确的重定向 URI 更新 OAuth 客户端。