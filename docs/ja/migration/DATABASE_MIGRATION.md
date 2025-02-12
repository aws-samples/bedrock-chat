# データベース移行ガイド

このガイドは、Bedrock Claude Chatの更新時にAuroraクラスターの置き換えを伴うデータ移行の手順を概説します。以下の手順により、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を確保します。

## 概要

移行プロセスには、すべてのボットをスキャンし、各ボットに対して埋め込みECSタスクを起動することが含まれます。このアプローチでは、埋め込みの再計算が必要で、時間がかかり、ECSタスクの実行とBedrock Cohereの使用料金により追加のコストが発生する可能性があります。これらのコストと時間要件を避けたい場合は、このガイドの後半にある[代替移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk)でAuroraの置き換え後、[migrate.py](./migrate.py)スクリプトを開き、以下の変数を適切な値に更新します。値は`CloudFormation` > `BedrockChatStack` > `Outputs`タブで参照できます。

```py
# AWS管理コンソールでCloudFormationスタックを開き、Outputsタブから値をコピーします。
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 変更不要
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 移行プロセスを開始するために`migrate.py`スクリプトを実行します。このスクリプトは、すべてのボットをスキャンし、埋め込みECSタスクを起動し、新しいAuroraクラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには`boto3`が必要です。
  - 環境には、dynamodbテーブルにアクセスし、ECSタスクを呼び出すIAMアクセス権限が必要です。

## 代替移行オプション

上記の方法に伴う時間とコストの影響を避けたい場合は、以下の代替アプローチを検討してください：

### スナップショット復元とDMS移行

まず、現在のAuroraクラスターにアクセスするためのパスワードに注意してください。次に`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから復元して一時的なデータベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時的なデータベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[DMSの同種移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用し、ネイティブの論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースがPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを活用できます。

プロジェクトの特定の要件と制約を考慮して、最も適切な移行アプローチを選択してください。