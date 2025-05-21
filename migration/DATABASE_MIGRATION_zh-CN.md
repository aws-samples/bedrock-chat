# 数据库迁移指南

> [!Warning]
> 本指南适用于从 v0 到 v1 的版本升级。

本指南概述了在更新包含 Aurora 集群替换的 Bedrock Chat 时进行数据迁移的步骤。以下流程确保在最大程度地减少停机时间和数据丢失的情况下顺利过渡。

## 概述

迁移过程涉及扫描所有机器人并为每个机器人启动嵌入式 ECS 任务。这种方法需要重新计算嵌入，可能会因 ECS 任务执行和 Bedrock Cohere 使用费而耗费大量时间和成本。如果您希望避免这些成本和时间要求，请参考本指南后续部分提供的[替代迁移选项](#alternative-migration-options)。

## 迁移步骤

- 在使用 Aurora 替换执行 [npx cdk deploy](../README.md#deploy-using-cdk) 后，打开 [migrate_v0_v1.py](./migrate_v0_v1.py) 脚本，并使用适当的值更新以下变量。这些值可以在 `CloudFormation` > `BedrockChatStack` > `Outputs` 选项卡中查看。

```py
# 在 AWS 管理控制台中打开 CloudFormation 堆栈，并从 Outputs 选项卡复制值。
# 键：DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# 键：EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# 键：EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 无需更改
# 键：PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# 键：EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 运行 `migrate_v0_v1.py` 脚本以启动迁移过程。此脚本将扫描所有机器人，启动嵌入 ECS 任务，并将数据创建到新的 Aurora 集群。请注意：
  - 脚本需要 `boto3`。
  - 环境需要 IAM 权限以访问 DynamoDB 表并调用 ECS 任务。

## 替代迁移选项

如果由于时间和成本影响，您不想使用上述方法，可以考虑以下替代方案：

### 快照恢复和 DMS 迁移

首先，记录访问当前 Aurora 集群的密码。然后运行 `npx cdk deploy`，这将触发集群替换。之后，通过从原始数据库的快照中恢复来创建临时数据库。
使用 [AWS 数据库迁移服务 (DMS)](https://aws.amazon.com/dms/) 将数据从临时数据库迁移到新的 Aurora 集群。

注意：截至 2024 年 5 月 29 日，DMS 不原生支持 pgvector 扩展。但是，您可以探索以下选项来解决此限制：

使用 [DMS 同构迁移](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)，它利用原生逻辑复制。在这种情况下，源和目标数据库都必须是 PostgreSQL。DMS 可以利用原生逻辑复制来实现此目的。

在选择最合适的迁移方法时，请考虑项目的具体要求和约束。