# データベース移行ガイド

このガイドは、Auroraクラスターを置き換えるBedrock Claude Chatのアップグレード中のデータ移行手順を説明します。以下の手順により、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を保証します。

## 概要

移行プロセスには、すべてのボットをスキャンし、各ボットの埋め込みのためのECSタスクを起動することが含まれます。このアプローチは埋め込みの再計算を必要とし、ECSタスクの実行とBedrock Cohereの使用料金による時間とコストの追加が発生する可能性があります。これらのコストと時間要件を避けたい場合は、このガイドの後半で説明する[代替移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) を Aurora 置換で実行した後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を適切な値に更新します。値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで確認できます。

```py
# AWS 管理コンソールで CloudFormation スタックを開き、Outputs タブから値をコピーします。
# キー: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# キー: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# キー: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 変更不要
# キー: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# キー: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 移行プロセスを開始するために `migrate_v0_v1.py` スクリプトを実行します。このスクリプトは以下を実行します：
  - すべてのボットをスキャン
  - ECS エンベディングタスクを起動
  - 新しい Aurora クラスターにデータを作成

  注意点：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを呼び出すための IAM 権限が必要です。

## 代替の移行オプション

以前の方法を時間とコストの観点から使用したくない場合は、以下の代替アプローチを検討してください：

### スナップショットからの復元とDMS移行

まず、現在のAuroraクラスターにアクセスするためのパスワードをメモします。次に、`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから一時データベースを復元します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[同種移行DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これは、ネイティブの論理レプリケーションを活用します。この場合、ソースデータベースと宛先データベースの両方がPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを活用できます。

移行アプローチを選択する際は、プロジェクト固有の要件と制約を考慮してください。