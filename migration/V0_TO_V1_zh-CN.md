# 迁移指南（v0 到 v1）

如果你已经使用了之前版本的 Bedrock Chat（约 `0.4.x`），则需要按照以下步骤进行迁移。

## 为什么需要这样做？

这个重大更新包含重要的安全更新。

- 向量数据库（即 Aurora PostgreSQL 上的 pgvector）存储现在已加密，部署时会触发替换。这意味着现有的向量项目将被删除。
- 我们引入了 `CreatingBotAllowed` Cognito 用户组，以限制可以创建机器人的用户。当前现有用户不在此组中，因此如果您希望他们具有创建机器人的权限，需要手动附加权限。参见：[机器人个性化](../../README.md#bot-personalization)

## 前提条件

阅读 [数据库迁移指南](./DATABASE_MIGRATION_zh-CN.md) 并确定恢复项目的方法。

## 步骤

### 向量存储迁移

- 打开终端并导航到项目目录
- 拉取你想要部署的分支。切换到目标分支（在本例中是 `v1`）并拉取最新更改：

```sh
git fetch
git checkout v1
git pull origin v1
```

- 如果你希望使用 DMS 恢复项目，请务必禁用密码轮换并记录访问数据库的密码。如果使用迁移脚本（[migrate_v0_v1.py](./migrate_v0_v1.py)），则无需记录密码。
- 删除所有[已发布的 API](../PUBLISH_API_zh-CN.md)，以便 CloudFormation 可以移除现有的 Aurora 集群。
- 运行 [npx cdk deploy](../README.md#deploy-using-cdk) 触发 Aurora 集群替换并删除所有向量项目。
- 按照[数据库迁移指南](./DATABASE_MIGRATION_zh-CN.md)恢复向量项目。
- 验证用户是否可以使用现有的具有知识的机器人，即 RAG 机器人。

### 附加 CreatingBotAllowed 权限

- 部署后，所有用户将无法创建新的机器人。
- 如果你希望特定用户能够创建机器人，请使用管理控制台或 CLI 将这些用户添加到 `CreatingBotAllowed` 组。
- 验证用户是否可以创建机器人。请注意，用户需要重新登录。