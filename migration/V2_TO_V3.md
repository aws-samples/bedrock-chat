# Migration Guide (v2 to v3)

## TL;DR

- V3 introduces fine-grained permission control and Bot Store functionality, requiring DynamoDB schema changes
- **Backup your DynamoDB ConversationTable before migration**
- Update your repository URL from `bedrock-claude-chat` to `bedrock-chat`
- Run the migration script to convert your data to the new schema
- All your bots and conversations will be preserved with the new permission model
- **IMPORTANT: During the migration process, the application will be unavailable to all users until the migration is complete. This process typically takes around 60 minutes, depending on the amount of data and the performance of your development environment.**
- **IMPORTANT: All Published APIs must be deleted during the migration process.**
- **WARNING: The migration process cannot guarantee 100% success for all bots. Please document your important bot configurations before migration in case you need to recreate them manually**

## Introduction

### What's New in V3

V3 introduces significant enhancements to Bedrock Chat:

1. **Fine-grained permission control**: Control access to your bots with user group-based permissions
2. **Bot Store**: Share and discover bots through a centralized marketplace
3. **Administrative features**: Manage APIs, mark bots as essential, and analyze bot usage

These new features required changes to the DynamoDB schema, necessitating a migration process for existing users.

### Why This Migration Is Necessary

The new permission model and Bot Store functionality required restructuring how bot data is stored and accessed. The migration process converts your existing bots and conversations to the new schema while preserving all your data.

> [!WARNING]
> Service Disruption Notice: **During the migration process, the application will be unavailable to all users.** Plan to perform this migration during a maintenance window when users do not need access to the system. The application will only become available again after the migration script has successfully completed and all data has been properly converted to the new schema. This process typically takes around 60 minutes, depending on the amount of data and the performance of your development environment.

> [!IMPORTANT]
> Before proceeding with migration: **The migration process cannot guarantee 100% success for all bots**, especially those created with older versions or with custom configurations. Please document your important bot configurations (instructions, knowledge sources, settings) before starting the migration process in case you need to recreate them manually.

## Migration Process

### Important Notice About Bot Visibility in V3

In V3, **all v2 bots with public sharing enabled will be searchable in the Bot Store.** If you have bots containing sensitive information that you don't want to be discoverable, consider making them private before migrating to V3.

### Step 1: Identify your environment name

In this procedure, `{YOUR_ENV_PREFIX}` is specified to identify the name of your CloudFormation Stacks. If you are using [Deploying Multiple Environments](../../README.md#deploying-multiple-environments) feature, replace it with the name of the environment to be migrated. If not, replace it with empty string.

### Step 2: Update Repository URL (Recommended)

The repository has been renamed from `bedrock-claude-chat` to `bedrock-chat`. Update your local repository:

```bash
# Check your current remote URL
git remote -v

# Update the remote URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verify the change
git remote -v
```

### Step 3: Ensure You're on the Latest V2 Version

> [!WARNING]
> You MUST update to v2.10.0 before migrating to V3. **Skipping this step may result in data loss during migration.**

Before starting the migration, make sure you're running the latest version of V2 (**v2.10.0**). This ensures you have all the necessary bug fixes and improvements before upgrading to V3:

```bash
# Fetch the latest tags
git fetch --tags

# Checkout the latest V2 version
git checkout v2.10.0

# Deploy the latest V2 version
cd cdk
npm ci
npx cdk deploy --all
```

### Step 4: Record Your V2 DynamoDB Table Name

Get the V2 ConversationTable name from CloudFormation outputs:

```bash
# Get the V2 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Make sure to save this table name in a secure location, as you'll need it for the migration script later.

### Step 5: Backup Your DynamoDB Table

Before proceeding, create a backup of your DynamoDB ConversationTable using the name you just recorded:

```bash
# Create a backup of your V2 table
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Check the backup status is available
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Step 6: Delete All Published APIs

> [!IMPORTANT]
> Before deploying V3, you must delete all published APIs to avoid Cloudformation output value conflicts during the upgrade process.

1. Log in to your application as an administrator
2. Navigate to the Admin section and select "API Management"
3. Review the list of all published APIs
4. Delete each published API by clicking the delete button next to it

You can find more information about API publishing and management in the [PUBLISH_API.md](../PUBLISH_API.md), [ADMINISTRATOR.md](../ADMINISTRATOR.md) documentation respectively.

### Step 7: Pull V3 and Deploy

Pull the latest V3 code and deploy:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Once you deploy V3, the application will be unavailable to all users until the migration process is complete. The new schema is incompatible with the old data format, so users will not be able to access their bots or conversations until you complete the migration script in the next steps.

### Step 8: Record Your V3 DynamoDB Table Names

After deploying V3, you need to get both the new ConversationTable and BotTable names:

```bash
# Get the V3 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Get the V3 BotTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Make sure to save these V3 table names along with your previously saved V2 table name, as you'll need all of them for the migration script.

### Step 9: Run the Migration Script

The migration script will convert your V2 data to the V3 schema. First, edit the migration script `docs/migration/migrate_v2_v3.py` to set your table names and region:

```python
# Region where dynamodb is located
REGION = "ap-northeast-1" # Replace with your region

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Replace with your  value recorded in Step 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Replace with your  value recorded in Step 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Replace with your  value recorded in Step 8
```

Then run the script using Poetry from the backend directory:

> [!NOTE]
> The Python requirements version was changed to 3.13.0 or later (Possibly changed in future development. See pyproject.toml). If you have venv installed with a different Python version, you'll need to remove it once.

```bash
# Navigate to the backend directory
cd backend

# Install dependencies if you haven't already
poetry install

# Run a dry run first to see what would be migrated
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# If everything looks good, run the actual migration
poetry run python ../docs/migration/migrate_v2_v3.py

# Verify the migration was successful
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

The migration script will generate a report file in your current directory with details about the migration process. Check this file to ensure all your data was migrated correctly.

#### Handling Large Data Volumes

For environments with heavy users or large amounts of data, consider these approaches:

1. **Migrate users individually**: For users with large data volumes, migrate them one at a time:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Memory considerations**: The migration process loads data into memory. If you encounter Out-Of-Memory (OOM) errors, try:

   - Migrating one user at a time
   - Running the migration on a machine with more memory
   - Breaking up the migration into smaller batches of users

3. **Monitor the migration**: Check the generated report files to ensure all data is migrated correctly, especially for large datasets.

### Step 10: Verify the Application

After migration, open your application and verify:

- All your bots are available
- Conversations are preserved
- New permission controls are working

### Clean Up (Optional)

After confirming that the migration was successful and all your data is properly accessible in V3, you may optionally delete the V2 conversation table to save costs:

```bash
# Delete the V2 conversation table (ONLY after confirming successful migration)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Only delete the V2 table after thoroughly verifying that all your important data has been successfully migrated to V3. We recommend keeping the backup created in Step 2 for at least a few weeks after migration, even if you delete the original table.

## V3 FAQ

### Bot Access and Permissions

**Q: What happens if a bot I'm using is deleted or my access permission is removed?**
A: Authorization is checked at chat time, so you'll lose access immediately.

**Q: What happens if a user is deleted (e.g., employee leaves)?**
A: Their data can be completely removed by deleting all items from DynamoDB with their user ID as the partition key (PK).

**Q: Can I turn off sharing for a essential public bot?**
A: No, admin must mark the bot as not essential first before turning off sharing.

**Q: Can I delete a essential public bot?**
A: No, admin must mark the bot as not essential first before deleting it.

### Security and Implementation

**Q: Is row-level security (RLS) implemented for bot table?**
A: No, considering the diversity of access patterns. Authorization is performed when accessing bots, and the risk of metadata leakage is considered minimal compared to conversation history.

**Q: What are the requirements for publishing an API?**
A: The bot must be public.

**Q: Will there be a management screen for all private bots?**
A: Not in the initial V3 release. However, items can still be deleted by querying with the user ID as needed.

**Q: Will there be bot tagging functionality for better search UX?**
A: Not in the initial V3 release, but LLM-based automatic tagging may be added in future updates.

### Administration

**Q: What can administrators do?**
A: Administrators can:

- Manage public bots (including checking high-cost bots)
- Manage APIs
- Mark public bots as essential

**Q: Can I make partially shared bots as essential?**
A: No, only support public bots.

**Q: Can I set priority for pinned bots?**
A: At the initial release, no.

### Authorization Configuration

**Q: How do I set up authorization?**
A:

1. Open the Amazon Cognito console and create user groups in the BrChat user pool
2. Add users to these groups as needed
3. In BrChat, select the user groups you want to allow access to when configuring bot sharing settings

Note: Group membership changes require re-login to take effect. Changes are reflected at token refresh, but not during the ID token validity period (default 30 minutes in V3, configurable by `tokenValidMinutes` in `cdk.json` or `parameter.ts`).

**Q: Does the system check with Cognito every time a bot is accessed?**
A: No, authorization is checked using the JWT token to avoid unnecessary I/O operations.

### Search Functionality

**Q: Does bot search support semantic search?**
A: No, only partial text matching is supported. Semantic search (e.g., "automobile" → "car", "EV", "vehicle") is not available due to current OpenSearch Serverless constraints (Mar 2025).
