# 数据库迁移指南

> [!Warning]
> 本指南适用于从v0升级到v1。

本指南概述了在更新包含Aurora集群替换的Bedrock Chat时迁移数据的步骤。以下流程确保在最大限度减少停机时间和数据丢失的同时实现平稳过渡。

## 概述

迁移过程包括扫描所有机器人并为每个机器人启动嵌入式 ECS 任务。这种方法需要重新计算嵌入向量，这可能会耗费较长时间，并且由于 ECS 任务执行和 Bedrock Cohere 使用费用而产生额外成本。如果您希望避免这些成本和时间消耗，请参阅本指南后面提供的[替代迁移选项](#alternative-migration-options)。

## 迁移步骤

- 使用Aurora替换后执行[npx cdk deploy](../README.md#deploy-using-cdk)，打开[migrate_v0_v1.py](./migrate_v0_v1.py)脚本并用适当的值更新以下变量。这些值可以在`CloudFormation` > `BedrockChatStack` > `Outputs`标签页中找到。

```py
# 在AWS管理控制台中打开CloudFormation堆栈，从Outputs标签页复制值。
# 键: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# 键: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# 键: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 无需更改
# 键: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# 键: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 运行`migrate_v0_v1.py`脚本以启动迁移过程。该脚本将扫描所有机器人，启动嵌入式ECS任务，并在新的Aurora集群中创建数据。请注意：
  - 该脚本需要`boto3`。
  - 环境需要具有访问dynamodb表和调用ECS任务的IAM权限。

## 替代迁移方案

如果由于时间和成本影响而不想使用上述方法，请考虑以下替代方案：

### 快照恢复和 DMS 迁移

首先，记录访问当前 Aurora 集群的密码。然后运行 `npx cdk deploy`，这将触发集群的替换。之后，通过从原始数据库的快照中恢复来创建一个临时数据库。
使用 [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) 将数据从临时数据库迁移到新的 Aurora 集群。

注意：截至 2024 年 5 月 29 日，DMS 原生不支持 pgvector 扩展。但是，你可以探索以下选项来解决这个限制：

使用 [DMS 同构迁移](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)，它利用原生逻辑复制。在这种情况下，源数据库和目标数据库都必须是 PostgreSQL。DMS 可以利用原生逻辑复制来实现这一目的。

在选择最合适的迁移方案时，请考虑您项目的具体要求和限制。