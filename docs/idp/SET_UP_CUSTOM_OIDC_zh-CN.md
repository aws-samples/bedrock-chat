# 设置外部身份提供者

## 步骤1：创建OIDC客户端

按照目标OIDC提供程序的流程操作，并记录OIDC客户端ID和密钥的值。后续步骤还需要颁发者URL。如果设置过程需要重定向URI，请输入虚拟值，该值将在部署完成后替换。

## 步骤 2：在 AWS Secrets Manager 中存储凭证

1. 进入 AWS 管理控制台。
2. 导航到 Secrets Manager 并选择"存储新的密钥"。
3. 选择"其他类型的密钥"。
4. 输入客户端 ID 和客户端密钥作为键值对。

   - 键：`clientId`，值：<YOUR_GOOGLE_CLIENT_ID>
   - 键：`clientSecret`，值：<YOUR_GOOGLE_CLIENT_SECRET>
   - 键：`issuerUrl`，值：<ISSUER_URL_OF_THE_PROVIDER>

5. 按照提示为密钥命名和描述。记下密钥名称，因为您将在 CDK 代码中需要它（在步骤 3 中使用的变量名 <YOUR_SECRET_NAME>）。
6. 审查并存储密钥。

### 注意

键名必须完全匹配字符串 `clientId`、`clientSecret` 和 `issuerUrl`。

## 步骤3：更新 cdk.json

在您的 cdk.json 文件中，添加身份提供商和密钥名称。

如下所示：

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 请勿更改
        "serviceName": "<您的服务名称>", // 可以设置任意值
        "secretName": "<您的密钥名称>"
      }
    ],
    "userPoolDomainPrefix": "<用户池域前缀的唯一值>"
  }
}
```

### 注意

#### 唯一性

`userPoolDomainPrefix` 必须在所有 Amazon Cognito 用户中全局唯一。如果您选择的前缀已被其他 AWS 账户使用，用户池域的创建将失败。最佳做法是在前缀中包含标识符、项目名称或环境名称，以确保唯一性。

## 步骤4：部署您的CDK堆栈

使用以下命令将CDK堆栈部署到AWS：

```sh
npx cdk deploy --require-approval never --all
```

## 步骤5：使用Cognito重定向URI更新OIDC客户端

部署堆栈后，`AuthApprovedRedirectURI` 将显示在CloudFormation输出中。返回到您的OIDC配置，并使用正确的重定向URI进行更新。