# 迁移指南（v2 到 v3）

## 简要说明

- V3版本引入了细粒度权限控制和Bot商店功能，需要对DynamoDB架构进行更改
- **迁移前请备份您的DynamoDB ConversationTable**
- 将您的仓库URL从`bedrock-claude-chat`更新为`bedrock-chat`
- 运行迁移脚本将您的数据转换为新架构
- 所有机器人和对话都将在新的权限模型下得到保留
- **重要提示：在迁移过程中，应用程序将对所有用户不可用，直到迁移完成。该过程通常需要约60分钟，具体取决于数据量和开发环境的性能。**
- **重要提示：在迁移过程中必须删除所有已发布的API。**
- **警告：迁移过程无法保证所有机器人100%成功迁移。请在迁移前记录下重要的机器人配置，以防需要手动重新创建**

## 简介

### V3 新特性

V3 为 Bedrock Chat 引入了重要增强功能:

1. **精细的权限控制**：通过基于用户组的权限来控制对机器人的访问
2. **机器人商店**：通过集中式市场分享和发现机器人
3. **管理功能**：管理 API、标记重要机器人以及分析机器人使用情况

这些新功能需要对 DynamoDB 架构进行更改，因此现有用户需要进行迁移。

### 为什么需要迁移

新的权限模型和机器人商店功能需要重构机器人数据的存储和访问方式。迁移过程会将您现有的机器人和对话转换为新架构，同时保留所有数据。

> [!WARNING]
> 服务中断通知：**在迁移过程中，应用程序将对所有用户不可用。** 请计划在用户不需要访问系统的维护时段内执行此迁移。只有在迁移脚本成功完成且所有数据都已正确转换为新架构后，应用程序才会重新可用。根据数据量和开发环境的性能，此过程通常需要约 60 分钟。

> [!IMPORTANT]
> 开始迁移前注意事项：**迁移过程无法保证所有机器人 100% 成功**，特别是使用较旧版本创建或具有自定义配置的机器人。在开始迁移过程之前，请记录下重要的机器人配置（指令、知识来源、设置），以防需要手动重新创建。

## 迁移流程

### 关于V3中机器人可见性的重要通知

在V3中，**所有启用了公开共享的v2机器人都将可以在机器人商店中被搜索到。**如果您有包含敏感信息且不希望被发现的机器人，请考虑在迁移到V3之前将其设为私有。

### 步骤1：确定您的环境名称

在此过程中，使用`{YOUR_ENV_PREFIX}`来标识您的CloudFormation堆栈名称。如果您使用了[部署多个环境](../../README.md#deploying-multiple-environments)功能，请将其替换为要迁移的环境名称。如果没有使用，则替换为空字符串。

### 步骤2：更新仓库URL（推荐）

仓库已从`bedrock-claude-chat`重命名为`bedrock-chat`。更新您的本地仓库：

```bash
# 检查当前远程URL
git remote -v

# 更新远程URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# 验证更改
git remote -v
```

### 步骤3：确保您使用的是最新的V2版本

> [!WARNING]
> 在迁移到V3之前，您必须更新到v2.10.0。**跳过此步骤可能会导致迁移过程中数据丢失。**

在开始迁移之前，请确保您运行的是最新版本的V2（**v2.10.0**）。这确保您在升级到V3之前拥有所有必要的错误修复和改进：

```bash
# 获取最新标签
git fetch --tags

# 检出最新的V2版本
git checkout v2.10.0

# 部署最新的V2版本
cd cdk
npm ci
npx cdk deploy --all
```

### 步骤4：记录您的V2 DynamoDB表名

从CloudFormation输出中获取V2 ConversationTable名称：

```bash
# 获取V2 ConversationTable名称
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

请确保将此表名保存在安全的位置，因为稍后在迁移脚本中会需要它。

### 步骤5：备份您的DynamoDB表

在继续之前，使用您刚刚记录的名称创建DynamoDB ConversationTable的备份：

```bash
# 创建V2表的备份
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

### 步骤6：删除所有已发布的API

> [!IMPORTANT]
> 在部署V3之前，您必须删除所有已发布的API，以避免升级过程中出现Cloudformation输出值冲突。

1. 以管理员身份登录您的应用程序
2. 导航到管理部分并选择"API管理"
3. 查看所有已发布的API列表
4. 通过点击每个API旁边的删除按钮来删除它

您可以在[PUBLISH_API.md](../PUBLISH_API_zh-CN.md)和[ADMINISTRATOR.md](../ADMINISTRATOR_zh-CN.md)文档中找到有关API发布和管理的更多信息。

### 步骤7：拉取V3并部署

拉取最新的V3代码并部署：

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> 一旦部署V3，在迁移过程完成之前，应用程序将对所有用户不可用。新的架构与旧的数据格式不兼容，因此在完成下一步的迁移脚本之前，用户将无法访问他们的机器人或对话。

### 步骤8：记录您的V3 DynamoDB表名

部署V3后，您需要获取新的ConversationTable和BotTable名称：

```bash
# 获取V3 ConversationTable名称
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# 获取V3 BotTable名称
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> 请确保将这些V3表名与您之前保存的V2表名一起保存，因为您在迁移脚本中会需要所有这些名称。

### 步骤9：运行迁移脚本

迁移脚本将把您的V2数据转换为V3架构。首先，编辑迁移脚本`docs/migration/migrate_v2_v3.py`以设置您的表名和区域：

```python
# DynamoDB所在的区域
REGION = "ap-northeast-1" # 替换为您的区域

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # 替换为您在步骤4中记录的值
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # 替换为您在步骤8中记录的值
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # 替换为您在步骤8中记录的值
```

然后从backend目录使用Poetry运行脚本：

> [!NOTE]
> Python要求版本已更改为3.13.0或更高（可能在未来开发中更改。请参见pyproject.toml）。如果您安装了不同Python版本的venv，您需要先删除它。

```bash
# 导航到backend目录
cd backend

# 如果尚未安装依赖项，请安装
poetry install

# 首先运行演习以查看将迁移的内容
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# 如果一切正常，运行实际迁移
poetry run python ../docs/migration/migrate_v2_v3.py

# 验证迁移是否成功
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

迁移脚本将在当前目录中生成一个报告文件，其中包含有关迁移过程的详细信息。检查此文件以确保所有数据都正确迁移。

#### 处理大量数据

对于有大量用户或数据的环境，请考虑以下方法：

1. **单独迁移用户**：对于拥有大量数据的用户，一次迁移一个用户：

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **内存考虑**：迁移过程会将数据加载到内存中。如果遇到内存不足（OOM）错误，请尝试：

   - 一次迁移一个用户
   - 在内存更大的机器上运行迁移
   - 将迁移分成较小的用户批次

3. **监控迁移**：检查生成的报告文件以确保所有数据都正确迁移，特别是对于大型数据集。

### 步骤10：验证应用程序

迁移后，打开您的应用程序并验证：

- 所有机器人都可用
- 对话已保留
- 新的权限控制正常工作

### 清理（可选）

在确认迁移成功且所有数据都能在V3中正确访问后，您可以选择删除V2对话表以节省成本：

```bash
# 删除V2对话表（仅在确认迁移成功后）
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> 只有在彻底验证所有重要数据都已成功迁移到V3后，才能删除V2表。我们建议即使删除原始表后，也要将在步骤2中创建的备份保留至少几周。

## V3 常见问题

### 机器人访问和权限

**Q: 如果我正在使用的机器人被删除或我的访问权限被移除会发生什么？**
A: 授权在聊天时进行检查，所以你会立即失去访问权限。

**Q: 如果用户被删除（例如，员工离职）会发生什么？**
A: 可以通过删除 DynamoDB 中以其用户 ID 作为分区键（PK）的所有项目来完全移除其数据。

**Q: 我能关闭核心公共机器人的共享吗？**
A: 不能，管理员必须先将机器人标记为非核心才能关闭共享。

**Q: 我能删除核心公共机器人吗？**
A: 不能，管理员必须先将机器人标记为非核心才能删除它。

### 安全和实现

**Q: 机器人表是否实现了行级安全（RLS）？**
A: 没有，考虑到访问模式的多样性。授权在访问机器人时执行，与对话历史相比，元数据泄露的风险被认为是最小的。

**Q: 发布 API 有什么要求？**
A: 机器人必须是公开的。

**Q: 是否会有所有私有机器人的管理界面？**
A: 在初始 V3 版本中没有。但是，仍然可以根据需要通过用户 ID 查询来删除项目。

**Q: 是否会有机器人标签功能以改善搜索体验？**
A: 在初始 V3 版本中没有，但未来更新可能会添加基于 LLM 的自动标签功能。

### 管理

**Q: 管理员可以做什么？**
A: 管理员可以：

- 管理公共机器人（包括检查高成本机器人）
- 管理 API
- 将公共机器人标记为核心

**Q: 我可以将部分共享的机器人设为核心吗？**
A: 不能，只支持公共机器人。

**Q: 我可以为置顶机器人设置优先级吗？**
A: 在初始版本中不能。

### 授权配置

**Q: 如何设置授权？**
A:

1. 打开 Amazon Cognito 控制台，在 BrChat 用户池中创建用户组
2. 根据需要将用户添加到这些组中
3. 在 BrChat 中配置机器人共享设置时，选择你想要允许访问的用户组

注意：组成员变更需要重新登录才能生效。变更在令牌刷新时反映，但在 ID 令牌有效期内不会生效（V3 中默认为 30 分钟，可通过 `cdk.json` 或 `parameter.ts` 中的 `tokenValidMinutes` 配置）。

**Q: 系统是否在每次访问机器人时都检查 Cognito？**
A: 不是，授权使用 JWT 令牌进行检查，以避免不必要的 I/O 操作。

### 搜索功能

**Q: 机器人搜索是否支持语义搜索？**
A: 不支持，仅支持部分文本匹配。由于当前 OpenSearch Serverless 的限制（2025年3月），不支持语义搜索（例如，"automobile" → "car"、"EV"、"vehicle"）。