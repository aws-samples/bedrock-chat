# データベース移行ガイド

このガイドでは、Bedrock Claude Chatをアップデートする際のデータ移行手順について説明します。これには、Auroraクラスターの置き換えが含まれます。この方法により、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を確実に実現します。

## 概要

移行プロセスは、すべてのボットをスキャンし、各ボットのデータ埋め込みのためのECSタスクを起動することで構成されています。このアプローチでは、新しいデータ埋め込みを計算する必要があり、長時間かかる可能性があり、ECSタスクの実行とBedrock Cohereサービスの追加コストが発生する可能性があります。これらのコストと時間制約を回避したい場合は、次のセクションで説明する代替データ移行オプションを参照してください。

## データ移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) の実行後、Auroraの置き換えが完了したら、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を適切な値に更新します。これらの値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブから参照できます。

```py
# AWS Management Consoleで CloudFormation スタックを開き、Outputsタブから値をコピーします
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

- データ移行プロセスを開始するには、`migrate_v0_v1.py` スクリプトを実行します。このスクリプトは、すべてのボットをスキャンし、埋め込み ECS タスクを起動し、新しいAuroraクラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です
  - 環境には、DynamoDBテーブルにアクセスし、ECSタスクを起動するためのIAMアクセス権限が必要です

## データ移行の代替方法

時間とコストの制約により、前述の方法を使用したくない場合は、以下の代替アプローチを検討してください：

### スナップショットの復元とDMSによるデータ移行

まず、現在のAuroraクラスターにアクセスするためのパスワードを保存し、`npx cdk deploy`コマンドを実行してクラスターを置き換えます。その後、元のデータベースのスナップショットから一時データベースを復元します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意: 2024年5月29日現在、DMSはpgvectorエクステンションを直接サポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[同等のDMSデータ移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これは、元のロジカルレプリケーションを使用します。この場合、ソースとターゲットの両方のデータベースはPostgreSQLである必要があります。DMSは、この目的のために元のロジカルレプリケーションを使用できます。

プロジェクトの具体的な要件と制約を考慮して、最適なデータ移行方法を選択してください。