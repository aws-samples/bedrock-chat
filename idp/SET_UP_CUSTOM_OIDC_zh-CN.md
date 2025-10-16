# 设置外部身份提供商

## 步骤1：创建OIDC客户端

按照目标OIDC提供商的程序进行操作，并记录OIDC客户端ID和密钥的值。在后续步骤中还需要签发者URL。如果在设置过程中需要重定向URI，请输入一个临时值，该值将在部署完成后被替换。

## 步骤 2：在 AWS Secrets Manager 中存储凭证

1. 登录 AWS 管理控制台。
2. 导航至 Secrets Manager 并选择"存储新密钥"。
3. 选择"其他类型的密钥"。
4. 以键值对的形式输入客户端 ID 和客户端密钥。

   - 键：`clientId`，值：<YOUR_GOOGLE_CLIENT_ID>
   - 键：`clientSecret`，值：<YOUR_GOOGLE_CLIENT_SECRET>
   - 键：`issuerUrl`，值：<ISSUER_URL_OF_THE_PROVIDER>

5. 按照提示为密钥命名并添加描述。请记下密钥名称，因为您将在 CDK 代码中需要它（在步骤 3 中用作变量名 <YOUR_SECRET_NAME>）。
6. 检查并存储密钥。

### 注意

键名必须与字符串 `clientId`、`clientSecret` 和 `issuerUrl` 完全匹配。

## 步骤 3：更新 cdk.json

在您的 cdk.json 文件中，添加身份提供商（ID Provider）和密钥名称（SecretName）。

如下所示：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 请勿修改
        "serviceName": "<YOUR_SERVICE_NAME>", // 设置任何您喜欢的值
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 注意事项

#### 唯一性

`userPoolDomainPrefix` 必须在所有 Amazon Cognito 用户中保持全局唯一性。如果您选择的前缀已被其他 AWS 账户使用，用户池域名的创建将会失败。建议在前缀中包含标识符、项目名称或环境名称，以确保唯一性。

## 步骤4：部署您的CDK堆栈

将您的CDK堆栈部署到AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步骤5：使用 Cognito 重定向 URI 更新 OIDC 客户端

部署堆栈后，`AuthApprovedRedirectURI` 将显示在 CloudFormation 输出中。返回您的 OIDC 配置并使用正确的重定向 URI 进行更新。