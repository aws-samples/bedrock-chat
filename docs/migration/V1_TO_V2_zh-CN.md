# 迁移指南（v1 到 v2）

## 简要说明

- **v1.2或更早版本用户**: 请升级到v1.4并使用知识库（KB）重新创建您的机器人。在过渡期后，一旦确认KB运行正常，再继续升级到v2。
- **v1.3版本用户**: 即使您已经在使用KB，也**强烈建议**升级到v1.4并重新创建机器人。如果您仍在使用pgvector，请通过在v1.4中使用KB重新创建机器人来进行迁移。
- **希望继续使用pgvector的用户**: 如果您计划继续使用pgvector，不建议升级到v2。升级到v2将删除所有与pgvector相关的资源，且未来将不再提供支持。在这种情况下请继续使用v1。
- 请注意，**升级到v2将导致所有Aurora相关资源被删除。**未来的更新将专注于v2，v1将被弃用。

## 简介

### 将会发生什么

v2 更新引入了一项重大变更，将 Aurora Serverless 上的 pgvector 和基于 ECS 的嵌入替换为 [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)。这一变更不向后兼容。

### 为什么本仓库采用了 Knowledge Bases 并停用 pgvector

这一变更有以下几个原因：

#### 改进 RAG 准确性

- Knowledge Bases 使用 OpenSearch Serverless 作为后端，支持全文搜索和向量搜索的混合搜索。这使得在处理包含专有名词的问题时能够获得更好的准确性，而这正是 pgvector 的不足之处。
- 它还支持更多用于提高 RAG 准确性的选项，如高级分块和解析。
- 截至2024年10月，Knowledge Bases 已经正式发布近一年，并且已添加了网页爬取等功能。预计未来会有更多更新，这使得长期采用高级功能变得更加容易。例如，虽然本仓库尚未在 pgvector 中实现从现有 S3 存储桶导入等经常被请求的功能，但在 KB (KnowledgeBases) 中已经支持这一功能。

#### 维护

- 当前的 ECS + Aurora 设置依赖于众多库，包括用于 PDF 解析、网页爬取和提取 YouTube 字幕的库。相比之下，像 Knowledge Bases 这样的托管解决方案降低了用户和仓库开发团队的维护负担。

## 迁移流程（摘要）

我们强烈建议在升级到v2之前先升级到v1.4版本。在v1.4中，您可以同时使用pgvector和Knowledge Base机器人，这允许有一个过渡期来将现有的pgvector机器人重新创建为Knowledge Base机器人，并验证它们是否按预期工作。即使RAG文档保持相同，由于k-NN算法等差异，后端更改为OpenSearch可能会产生略微不同但通常相似的结果。

通过在`cdk.json`中将`useBedrockKnowledgeBasesForRag`设置为true，您可以使用Knowledge Bases创建机器人。但是，pgvector机器人将变为只读模式，无法创建或编辑新的pgvector机器人。

![](../imgs/v1_to_v2_readonly_bot.png)

v1.4还引入了[Amazon Bedrock的防护机制](https://aws.amazon.com/jp/bedrock/guardrails/)。由于Knowledge Bases的区域限制，用于上传文档的S3存储桶必须与`bedrockRegion`位于同一区域。我们建议在更新之前备份现有的文档存储桶，以避免之后需要手动上传大量文档（因为S3存储桶导入功能是可用的）。

## 迁移流程（详细）

具体步骤因使用的是v1.2及更早版本还是v1.3而异。

![](../imgs/v1_to_v2_arch.png)

### v1.2或更早版本用户的步骤

1. **备份现有文档存储桶（可选但建议）。** 如果您的系统已在运行，我们强烈建议执行此步骤。备份名为`bedrockchatstack-documentbucketxxxx-yyyy`的存储桶。例如，我们可以使用[AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)。

2. **更新至v1.4**：获取最新的v1.4标签，修改`cdk.json`，并部署。按以下步骤操作：

   1. 获取最新标签：
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. 修改`cdk.json`如下：
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

3. **重新创建机器人**：在Knowledge Base上使用与pgvector机器人相同的定义（文档、分块大小等）重新创建机器人。如果您有大量文档，从步骤1的备份中恢复将使此过程更容易。要恢复，我们可以使用跨区域复制恢复。更多详情，请访问[此处](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html)。要指定恢复的存储桶，请按如下方式设置`S3 Data Source`部分。路径结构为`s3://<bucket-name>/<user-id>/<bot-id>/documents/`。您可以在Cognito用户池中查看用户ID，在机器人创建界面的地址栏中查看机器人ID。

![](../imgs/v1_to_v2_KB_s3_source.png)

**请注意，某些功能在Knowledge Bases上不可用，如网页爬取和YouTube转录支持（计划支持网页爬取器（[issue](https://github.com/aws-samples/bedrock-chat/issues/557)））。**另外，请记住，在过渡期间使用Knowledge Bases将同时产生Aurora和Knowledge Bases的费用。

4. **删除已发布的API**：由于VPC删除，在部署v2之前需要重新发布所有之前发布的API。为此，您需要先删除现有的API。使用[管理员的API管理功能](../ADMINISTRATOR_zh-CN.md)可以简化此过程。一旦所有`APIPublishmentStackXXXX` CloudFormation堆栈删除完成，环境就准备就绪了。

5. **部署v2**：v2发布后，获取标记的源代码并按如下方式部署（发布后即可执行）：
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> 部署v2后，**所有带有[Unsupported, Read-only]前缀的机器人将被隐藏。**请确保在升级前重新创建必要的机器人，以避免失去访问权限。

> [!Tip]
> 在堆栈更新期间，您可能会遇到重复的消息，如："Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted."" 在这种情况下，请导航至管理控制台 > EC2 > 网络接口，搜索BedrockChatStack。删除与此名称关联的显示接口，以帮助确保部署过程更顺畅。

### v1.3用户的步骤

如前所述，在v1.4中，由于区域限制，必须在bedrockRegion中创建Knowledge Bases。因此，您需要重新创建KB。如果您已经在v1.3中测试过KB，请在v1.4中使用相同的定义重新创建机器人。按照v1.2用户的步骤操作。