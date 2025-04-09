# データベース移行ガイド

このガイドは、Auroraクラスターの置き換えを含むBedrock Claude Chatのアップグレード中のデータ移行手順を概説します。以下の手順により、ダウンタイムと data loss を最小限に抑えながら、スムーズな移行を確保します。

## 全体的な概要

移行プロセスには、すべてのボットをスキャンし、それぞれのECSエンベデッドタスクを円滑に実行することが含まれます。このアプローチでは、エンベデッドの再計算が必要で、ECSタスクの実行とBedrockのCohere使用料による追加のコストと時間がかかる可能性があります。これらのコストと時間の要件を回避したい場合は、このガイドの後半で提供される[代替移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) を実行して Aurora に置き換えた後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を適切な値に更新します。これらの値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで参照できます。

```py
# AWS 管理コンソールで CloudFormation スタックを開き、Outputs タブから値をコピーします。
# キー: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# キー: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# キー: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 変更する必要はありません
# キー: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# キー: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- `migrate_v0_v1.py` スクリプトを実行して、移行プロセスを開始します。このスクリプトはすべてのボットをスキャンし、ECS 埋め込みタスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを起動するための IAM 権限が必要です。

## 移行の代替オプション

上記の方法が時間とコストの影響により好ましくない場合は、以下の代替アプローチを検討してください：

### スナップショットリカバリとDMSによる移行

まず、現在のAuroraクラスターにアクセスするためのパスワードを記録します。次に、`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから復元して一時データベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorの接続をネイティブにサポートしていません。ただし、この制限を回避するための以下のオプションを検討できます：

[同種のDMS移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用し、ネイティブの論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースはPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを活用できます。

プロジェクトの特定の要件と制約を考慮して、最適な移行アプローチを選択してください。