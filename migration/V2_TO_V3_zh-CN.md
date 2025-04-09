# 迁移指南（v2 到 v3）

## 摘要

- V3 引入了细粒度的权限控制和机器人商店功能，需要对 DynamoDB 架构进行更改
- **在迁移前备份您的 DynamoDB ConversationTable**
- 将仓库 URL 从 `bedrock-claude-chat` 更新为 `bedrock-chat`
- 运行迁移脚本以将数据转换为新架构
- 所有机器人和对话将在新的权限模型中保留
- **重要：在迁移过程中，应用程序将对所有用户不可用，直到迁移完成。此过程通常需要大约 60 分钟，具体取决于数据量和开发环境的性能。**
- **重要：在迁移过程中必须删除所有已发布的 API。**
- **警告：迁移过程无法保证对所有机器人 100% 成功。请在迁移前记录重要的机器人配置，以便在需要时可以手动重新创建。**

## 介绍

### V3 的新特性

V3 为 Bedrock Chat 引入了重大增强：

1. **细粒度权限控制**：通过用户组权限控制对机器人的访问
2. **机器人商店**：通过集中的市场共享和发现机器人
3. **管理功能**：管理 API、标记机器人为必要，并分析机器人使用情况

这些新功能需要对 DynamoDB 架构进行更改，这对于现有用户来说需要进行迁移过程。

### 为什么需要这次迁移

新的权限模型和机器人商店功能需要重新构建机器人数据的存储和访问方式。迁移过程会将现有的机器人和对话转换为新的架构，同时保留所有数据。

> [!WARNING]
> 服务中断通知：**在迁移过程中，应用程序将对所有用户不可用。**请计划在用户不需要访问系统的维护窗口期间执行此迁移。只有在迁移脚本成功完成并且所有数据已正确转换为新架构后，应用程序才会再次可用。根据数据量和开发环境的性能，此过程通常需要大约 60 分钟。

> [!IMPORTANT]
> 在继续迁移之前：**迁移过程无法保证对所有机器人 100% 成功**，尤其是使用旧版本或具有自定义配置的机器人。请在开始迁移过程之前记录重要的机器人配置（指令、知识源、设置），以防需要手动重新创建。

## 迁移流程

### 关于 V3 中机器人可见性的重要通知

在 V3 中，**所有启用了公开共享的 V2 机器人都将在机器人商店中可搜索。** 如果您有包含敏感信息且不希望被发现的机器人，请考虑在迁移到 V3 之前将其设为私有。

### 第 1 步：识别您的环境名称

在此过程中，`{YOUR_ENV_PREFIX}` 用于标识您的 CloudFormation 堆栈的名称。如果您正在使用[部署多个环境](../../README.md#deploying-multiple-environments)功能，请将其替换为要迁移的环境名称。如果没有，请替换为空字符串。

### 第 2 步：更新仓库 URL（推荐）

仓库已从 `bedrock-claude-chat` 重命名为 `bedrock-chat`。更新您的本地仓库：

```bash
# 检查您当前的远程 URL
git remote -v

# 更新远程 URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# 验证更改
git remote -v
```

### 第 3 步：确保使用最新的 V2 版本

> [!WARNING]
> 在迁移到 V3 之前，您必须更新到 v2.10.0。**跳过此步骤可能导致迁移过程中数据丢失。**

在开始迁移之前，请确保您正在运行 V2 的最新版本（**v2.10.0**）。这确保在升级到 V3 之前已具备所有必要的错误修复和改进：

```bash
# 获取最新标签
git fetch --tags

# 检出最新的 V2 版本
git checkout v2.10.0

# 部署最新的 V2 版本
cd cdk
npm ci
npx cdk deploy --all
```

### 第 4 步：记录您的 V2 DynamoDB 表名

从 CloudFormation 输出中获取 V2 ConversationTable 名称：

```bash
# 获取 V2 ConversationTable 名称
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

确保将此表名保存在安全位置，因为您稍后需要在迁移脚本中使用。

### 第 5 步：备份您的 DynamoDB 表

在继续之前，使用您刚刚记录的名称创建 DynamoDB ConversationTable 的备份：

```bash
# 创建 V2 表的备份
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# 检查备份状态是否可用
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### 第 6 步：删除所有已发布的 API

> [!IMPORTANT]
> 在部署 V3 之前，您必须删除所有已发布的 API，以避免在升级过程中出现 Cloudformation 输出值冲突。

1. 以管理员身份登录您的应用程序
2. 导航到管理员部分并选择"API 管理"
3. 查看所有已发布 API 的列表
4. 通过点击每个 API 旁边的删除按钮来删除它们

您可以在 [PUBLISH_API.md](../PUBLISH_API_zh-CN.md)、[ADMINISTRATOR.md](../ADMINISTRATOR_zh-CN.md) 文档中找到有关 API 发布和管理的更多信息。

### 第 7 步：拉取 V3 并部署

拉取最新的 V3 代码并部署：

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> 一旦部署 V3，在迁移过程完成之前，应用程序将对所有用户不可用。新的架构与旧的数据格式不兼容，因此用户在完成下一步的迁移脚本之前将无法访问他们的机器人或对话。

### 第 8 步：记录您的 V3 DynamoDB 表名

部署 V3 后，您需要获取新的 ConversationTable 和 BotTable 名称：

```bash
# 获取 V3 ConversationTable 名称
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# 获取 V3 BotTable 名称
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> 确保保存这些 V3 表名以及之前保存的 V2 表名，因为您在迁移脚本中需要所有这些名称。

### 第 9 步：运行迁移脚本

迁移脚本将把您的 V2 数据转换为 V3 架构。首先，编辑迁移脚本 `docs/migration/migrate_v2_v3.py` 以设置您的表名和区域：

```python
# DynamoDB 所在的区域
REGION = "ap-northeast-1" # 替换为您的区域

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # 替换为您在第 4 步记录的值
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # 替换为您在第 8 步记录的值
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # 替换为您在第 8 步记录的值
```

然后从后端目录使用 Poetry 运行脚本：

> [!NOTE]
> Python 要求的版本已更改为 3.13.0 或更高版本（可能在未来开发中发生变化。请参见 pyproject.toml）。如果您使用不同的 Python 版本安装了 venv，则需要删除它。

```bash
# 导航到后端目录
cd backend

# 如果尚未安装依赖项，请安装
poetry install

# 首先进行试运行，查看将迁移哪些内容
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# 如果一切看起来正常，则运行实际迁移
poetry run python ../docs/migration/migrate_v2_v3.py

# 验证迁移是否成功
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

迁移脚本将在当前目录生成一个报告文件，其中包含迁移过程的详细信息。检查此文件，确保所有数据都已正确迁移。

#### 处理大量数据

对于用户量大或数据量大的环境，请考虑以下方法：

1. **逐个用户迁移**：对于数据量大的用户，逐个迁移：

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **内存注意事项**：迁移过程会将数据加载到内存中。如果遇到内存不足（OOM）错误，请尝试：

   - 逐个用户迁移
   - 在内存更大的机器上运行迁移
   - 将迁移分批处理用户

3. **监控迁移**：检查生成的报告文件，确保所有数据（尤其是大型数据集）都正确迁移。

### 第 10 步：验证应用程序

迁移后，打开您的应用程序并验证：

- 所有机器人都可用
- 对话已保留
- 新的权限控制正常工作

### 清理（可选）

在确认迁移成功且所有数据在 V3 中正确可访问后，您可以选择删除 V2 对话表以节省成本：

```bash
# 删除 V2 对话表（仅在确认成功迁移后）
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> 仅在彻底验证所有重要数据已成功迁移到 V3 后才删除 V2 表。即使删除原始表，我们建议至少在迁移后几周内保留在第 2 步创建的备份。

## V3 常见问题解答

### 机器人访问和权限

**Q: 如果我使用的机器人被删除或我的访问权限被移除会发生什么？**
A: 授权在聊天时进行检查，因此您将立即失去访问权限。

**Q: 如果用户被删除（例如，员工离职）会发生什么？**
A: 通过使用用户ID作为分区键(PK)删除DynamoDB中的所有项目，可以完全删除他们的数据。

**Q: 我可以关闭重要公共机器人的共享功能吗？**
A: 不可以，管理员必须先将机器人标记为非重要，然后才能关闭共享。

**Q: 我可以删除重要的公共机器人吗？**
A: 不可以，管理员必须先将机器人标记为非重要，然后才能删除。

### 安全性和实现

**Q: 机器人表是否实现了行级安全(RLS)？**
A: 不，考虑到访问模式的多样性。在访问机器人时执行授权，与对话历史记录相比，元数据泄露的风险被认为是最小的。

**Q: 发布API的要求是什么？**
A: 机器人必须是公共的。

**Q: 是否会有管理所有私有机器人的界面？**
A: 在初始V3版本中不会。但是，仍然可以通过使用用户ID进行查询来删除项目。

**Q: 是否会有机器人标记功能以改善搜索用户体验？**
A: 在初始V3版本中不会，但可能在未来更新中添加基于法学硕士的自动标记。

### 管理

**Q: 管理员可以做什么？**
A: 管理员可以：

- 管理公共机器人（包括检查高成本机器人）
- 管理API
- 将公共机器人标记为重要

**Q: 我可以将部分共享的机器人标记为重要吗？**
A: 不可以，仅支持公共机器人。

**Q: 我可以为固定机器人设置优先级吗？**
A: 在初始版本中，不可以。

### 授权配置

**Q: 如何设置授权？**
A:

1. 打开Amazon Cognito控制台，在BrChat用户池中创建用户组
2. 根据需要向这些组添加用户
3. 在BrChat中，配置机器人共享设置时选择要允许访问的用户组

注意：组成员资格变更需要重新登录才能生效。更改将在令牌刷新时反映，但在ID令牌有效期间（V3中默认30分钟，可通过`cdk.json`或`parameter.ts`中的`tokenValidMinutes`配置）不会生效。

**Q: 系统是否每次访问机器人时都会与Cognito进行检查？**
A: 不会，授权是使用JWT令牌检查的，以避免不必要的I/O操作。

### 搜索功能

**Q: 机器人搜索是否支持语义搜索？**
A: 不支持，仅支持部分文本匹配。由于当前OpenSearch Serverless的限制（2025年3月），不支持语义搜索（例如，"汽车" → "car"，"电动汽车"，"车辆"）。