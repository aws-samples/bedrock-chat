# 迁移指南（v1 到 v2）

## 总结

- **对于 v1.2 或更早版本的用户**：升级到 v1.4 并使用知识库（KB）重新创建您的机器人。在过渡期后，确认一切正常后，再升级到 v2。
- **对于 v1.3 的用户**：即使您已经在使用 KB，也**强烈建议**升级到 v1.4 并重新创建您的机器人。如果您仍在使用 pgvector，请通过在 v1.4 中使用 KB 重新创建机器人来迁移。
- **对于希望继续使用 pgvector 的用户**：如果您计划继续使用 pgvector，不建议升级到 v2。升级到 v2 将删除所有与 pgvector 相关的资源，并且未来将不再提供支持。在这种情况下，请继续使用 v1。
- 请注意，**升级到 v2 将导致删除所有 Aurora 相关资源。**未来的更新将专注于 v2，v1 将被弃用。

## 介绍

### 将会发生什么

v2 更新通过将 Aurora Serverless 上的 pgvector 和基于 ECS 的嵌入替换为 [Amazon Bedrock 知识库](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)引入了一个重大变更。这一变更不向后兼容。

### 为什么本仓库采用知识库并停止使用 pgvector

这一变更有几个原因：

#### 改进的 RAG 准确性

- 知识库使用 OpenSearch Serverless 作为后端，允许进行混合搜索，包括全文和向量搜索。这提高了在包含专有名词的问题上的响应准确性，而 pgvector 在这方面存在困难。
- 它还支持更多改进 RAG 准确性的选项，如高级分块和解析。
- 截至 2024 年 10 月，知识库已经普遍可用近一年，并已添加了网页爬取等功能。预期未来会有更新，从长远来看更容易采用高级功能。例如，虽然本仓库在 pgvector 中尚未实现从现有 S3 存储桶导入（这是一个频繁被请求的功能），但知识库（KB）中已经支持这一功能。

#### 维护

- 当前的 ECS + Aurora 设置依赖于众多库，包括用于 PDF 解析、网页爬取和提取 YouTube 字幕的库。相比之下，像知识库这样的托管解决方案可以减轻用户和仓库开发团队的维护负担。

## 迁移流程（总结）

我们强烈建议在迁移到v2之前先升级到v1.4。在v1.4版本中，您可以同时使用pgvector和知识库机器人，这为您提供了一个过渡期，可以在知识库中重新创建现有的pgvector机器人并验证它们是否按预期工作。即使RAG文档保持完全相同，请注意由于后端对OpenSearch的更改，可能会产生稍微不同的结果，尽管通常相似，这是由于k-NN算法等差异造成的。

通过在`cdk.json`中将`useBedrockKnowledgeBasesForRag`设置为true，您可以使用知识库创建机器人。但是，pgvector机器人将变为只读状态，阻止创建或编辑新的pgvector机器人。

![](../imgs/v1_to_v2_readonly_bot.png)

在v1.4中，还引入了[Amazon Bedrock的护栏](https://aws.amazon.com/jp/bedrock/guardrails/)。由于知识库的区域限制，用于上传文档的S3存储桶必须与`bedrockRegion`位于同一区域。我们建议在更新前备份现有的文档存储桶，以避免稍后手动上传大量文档（因为S3存储桶导入功能已可用）。

## 迁移流程（详细说明）

根据您是使用v1.2或更早版本，还是v1.3，步骤会有所不同。

![](../imgs/v1_to_v2_arch.png)

### 对于v1.2或更早版本的用户

1. **备份现有文档存储桶（可选但推荐）。** 如果您的系统已经在运行，我们强烈建议执行此步骤。备份名为 `bedrockchatstack-documentbucketxxxx-yyyy` 的存储桶。例如，我们可以使用 [AWS 备份](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)。

2. **更新到v1.4**：获取最新的v1.4标签，修改 `cdk.json`，并部署。按照以下步骤操作：

   1. 获取最新标签：
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. 按如下方式修改 `cdk.json`：
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. 部署更改：
      ```bash
      npx cdk deploy
      ```

3. **重新创建您的机器人**：在知识库上重新创建您的机器人，使用与pgvector机器人相同的定义（文档、分块大小等）。如果您有大量文档，则使用步骤1中的备份将使此过程更加容易。要恢复，我们可以使用跨区域副本恢复。更多详细信息，请访问[此处](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html)。要指定恢复的存储桶，请按如下方式设置 `S3 数据源` 部分。路径结构为 `s3://<bucket-name>/<user-id>/<bot-id>/documents/`。您可以在 Cognito 用户池和机器人创建屏幕的地址栏上查看用户ID和机器人ID。

![](../imgs/v1_to_v2_KB_s3_source.png)

**请注意，知识库上不支持某些功能，如网页爬取和YouTube字幕支持（计划支持网页爬虫（[问题](https://github.com/aws-samples/bedrock-claude-chat/issues/557)））。** 另外，请记住，在过渡期间，使用知识库将同时产生Aurora和知识库的费用。

4. **删除已发布的API**：由于VPC删除，所有先前发布的API都需要在部署v2之前重新发布。为此，您需要先删除现有的API。使用[管理员的API管理功能](../ADMINISTRATOR_zh-CN.md)可以简化此过程。一旦删除了所有 `APIPublishmentStackXXXX` CloudFormation堆栈，环境就准备就绪了。

5. **部署v2**：在v2发布后，获取标记的源代码并按如下方式部署（这将在发布后成为可能）：
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!警告]
> 部署v2后，**所有前缀为 [不支持，只读] 的机器人都将被隐藏。** 确保在升级前重新创建必要的机器人，以避免丢失访问权限。

> [!提示]
> 在堆栈更新期间，您可能会遇到重复的消息，如："资源处理程序返回消息：'子网 'subnet-xxx' 有依赖项，无法删除。'"在这种情况下，请转到管理控制台 > EC2 > 网络接口，并搜索 BedrockChatStack。删除与此名称关联的显示的接口，以帮助确保更顺利的部署过程。

### 对于v1.3版本的用户

如前所述，在v1.4中，由于区域限制，知识库必须在 bedrockRegion 中创建。因此，您需要重新创建知识库。如果您已在v1.3中测试过知识库，请在v1.4中使用相同的定义重新创建机器人。按照针对v1.2用户的步骤进行操作。