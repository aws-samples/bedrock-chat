# データベース移行ガイド

本ガイドでは、Aurora クラスターの置き換えを含む Bedrock Claude Chat の更新時にデータ移行を実行する手順の概要を説明します。以下の手順により、停止時間とデータ損失を最小限に抑えながら、スムーズな移行を確保します。

## Overview

The migration process involves scanning all robots and launching embedded ECS tasks for each robot. This approach requires re-computing embeddings, which can be time-consuming and incur additional costs due to ECS task execution and Bedrock Cohere usage fees. If you wish to avoid these cost and time requirements, please refer to the [alternative migration options](#alternative-migration-options) provided later in this guide.

## 移行手順

- Aurora に置き換えた後、[npx cdk deploy](../README.md#deploy-using-cdk) を実行し、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、適切な値で以下の変数を更新します。これらの値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで参照できます。

```py
# AWS 管理コンソールで CloudFormation スタックを開き、Outputs タブから値をコピーします。
# キー：DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# キー：EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# キー：EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 変更不要
# キー：PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# キー：EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- `migrate_v0_v1.py` スクリプトを実行して移行プロセスを開始します。このスクリプトはすべてのボットをスキャンし、埋め込み ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを呼び出すための IAM 権限が必要です。

## Alternative Migration Options

If you do not want to use the previous methods due to time and cost implications, consider the following alternatives:

### Snapshot Restore and DMS Migration

First, document the passwords for accessing the current Aurora cluster. Then run `npx cdk deploy`, which will trigger the cluster's replacement. Afterward, create a temporary database by restoring from a snapshot of the original database.
Use [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) to migrate data from the temporary database to the new Aurora cluster.

Note: As of May 29, 2024, DMS does not natively support the pgvector extension. However, you can explore the following options to address this limitation:

Use [DMS homogeneous migration](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), which leverages native logical replication. In this case, both the source and target databases must be PostgreSQL. DMS can utilize native logical replication for this purpose.

When choosing the most suitable migration approach, consider the specific requirements and constraints of your project.