# 数据库迁移指南

> [!Warning]
> 本指南适用于从 v0 升级到 v1。

本指南概述了在更新包含 Aurora 集群替换的 Bedrock Chat 时迁移数据的步骤。以下流程确保平稳过渡，同时将停机时间和数据丢失降至最低。

## 概述

迁移过程包括扫描所有机器人并为每个机器人启动嵌入式 ECS 任务。这种方法需要重新计算嵌入向量，这可能会耗费大量时间，并且由于 ECS 任务执行和 Bedrock Cohere 使用费用而产生额外成本。如果您希望避免这些成本和时间要求，请参阅本指南后面提供的[替代迁移选项](#alternative-migration-options)。

## 迁移步骤

- 在使用 Aurora 替换完成 [npx cdk deploy](../README.md#deploy-using-cdk) 后，打开 [migrate_v0_v1.py](./migrate_v0_v1.py) 脚本并用适当的值更新以下变量。这些值可以在 `CloudFormation` > `BedrockChatStack` > `Outputs` 标签页中找到。

```py
# 在 AWS Management Console 中打开 CloudFormation 堆栈，从 Outputs 标签页复制这些值。
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 无需更改
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 运行 `migrate_v0_v1.py` 脚本以启动迁移过程。此脚本将扫描所有机器人，启动嵌入式 ECS 任务，并将数据创建到新的 Aurora 集群中。请注意：
  - 该脚本需要 `boto3`。
  - 环境需要具有访问 dynamodb 表和调用 ECS 任务的 IAM 权限。

## 替代迁移方案

如果由于时间和成本影响而不想使用上述方法，请考虑以下替代方案：

### 快照恢复和 DMS 迁移

首先，记录当前 Aurora 集群的访问密码。然后运行 `npx cdk deploy`，这将触发集群的替换。之后，通过原始数据库的快照创建一个临时数据库。
使用 [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) 将数据从临时数据库迁移到新的 Aurora 集群。

注意：截至2024年5月29日，DMS 原生不支持 pgvector 扩展。但是，您可以探索以下选项来解决这个限制：

使用 [DMS 同构迁移](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)，它利用原生逻辑复制。在这种情况下，源数据库和目标数据库都必须是 PostgreSQL。DMS 可以利用原生逻辑复制来实现这一目的。

在选择最合适的迁移方法时，请考虑您项目的具体要求和限制。