# データベース移行ガイド

このガイドでは、Aurora クラスターの置き換えを含む Bedrock Claude Chat のアップグレードを実行する際のデータ移行手順について説明します。以下の手順により、最小限のダウンタイムとデータ損失で円滑な移行を保証します。

## 概要

移行プロセスには、すべてのボットをスキャンし、それぞれに対してECSの埋め込みタスクを開始することが含まれます。このアプローチでは、埋め込みの再計算が必要となり、ECSタスクとBedrockのCohere使用タスクの実行により、処理が遅くなり、追加のコストが発生する可能性があります。これらのコストと時間要件を避けたい場合は、このガイドの後半で提供されている[代替移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) で Aurora の置き換えを行った後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数に適切な値を設定します。値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで確認できます。

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

- 移行プロセスを開始するには、`migrate_v0_v1.py` スクリプトを実行します。このスクリプトは、すべてのボットをスキャンし、埋め込みのための ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを呼び出すための IAM 権限が必要です。

## 代替の移行オプション

前述の方法が時間とコストの観点から望ましくない場合は、以下の代替アプローチを検討してください：

### スナップショットの復元とDMSによる移行

まず、現在のAuroraクラスターにアクセスするためのパスワードをメモします。次に、`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから一時的なデータベースを復元します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意: 2024年5月29日現在、DMSはpgvector拡張機能をネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[DMS同種移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これは、ネイティブの論理レプリケーションを活用します。この場合、ソースデータベースとターゲットデータベースの両方がPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを活用できます。

プロジェクトの特定の要件と制約を考慮して、最も適切な移行アプローチを選択してください。