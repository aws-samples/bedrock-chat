# 设置外部身份提供者

## 步骤1：创建OIDC客户端

按照目标OIDC提供程序的流程操作，并记录OIDC客户端ID和密钥的值。后续步骤还需要颁发者URL。如果设置过程需要重定向URI，请输入虚拟值，该值将在部署完成后替换。

## 步骤2：在AWS Secrets Manager中存储凭据

1. 进入AWS管理控制台。
2. 导航到Secrets Manager并选择"存储新的密钥"。
3. 选择"其他类型的密钥"。
4. 输入客户端ID和客户端密钥作为键值对。

   - 键：`clientId`，值：<YOUR_GOOGLE_CLIENT_ID>
   - 键：`clientSecret`，值：<YOUR_GOOGLE_CLIENT_SECRET>
   - 键：`issuerUrl`，值：<ISSUER_URL_OF_THE_PROVIDER>

5. 按照提示为密钥命名和描述。请记下密钥名称，因为您将在CDK代码中需要它（在步骤3中使用的变量名为<YOUR_SECRET_NAME>）。
6. 审查并存储密钥。

### 注意

键名必须完全匹配字符串 `clientId`、`clientSecret` 和 `issuerUrl`。

## 步骤 3：更新 cdk.json

在 cdk.json 文件中，添加身份提供程序和密钥名称。

如下所示：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 不要变更变改servicYOUR SERVICE_",", // 可以设置任何您喜欢的值
        "secret_SECRET YOUR
_NAME>"
    
    ],user
om"<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
}


### ####一事项

`userPoolDomainPrefixix` 必须在所有 Amazon Cognito 用户中全局唯一。如果您选择的前缀已被其他 AWS 账户使用，用户池域的创建将失败。最佳实践是在前缀中包含标标识符、项目名称或环境名称，以确保唯一性。

## 步骤 4：部署您的 CDK 堆栈

将您的 CDK 堆栈部署到 AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步骤5：使用 Cognito 重定向 URI 更新 OIDC 客户端

在部署堆栈后，`AuthApprovedRedirectURI` 将显示在 CloudFormation 输出中。返回到您的 OIDC 配置，并使用正确的重定向 URI 进行更新。