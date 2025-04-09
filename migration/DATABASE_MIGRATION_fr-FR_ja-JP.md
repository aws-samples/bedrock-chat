# データベース移行ガイド

このガイドは、Auroraクラスターの置き換えを伴うBedrock Claude Chatの更新時のデータ移行手順について説明します。以下の手順により、最小限のダウンタイムとデータ損失で円滑な移行を保証します。

## 概要

移行プロセスには、すべてのボットをスキャンし、各ボットに対してECSエンベディングタスクを実行することが含まれます。このアプローチでは、エンベディングの再計算が必要となり、ECSタスクの実行とBedrock Cohere の使用料により、時間がかかり追加のコストが発生する可能性があります。これらのコストと時間の制約を回避したい場合は、このガイドで後述する[代替移行オプション](#alternative-migration-options)をご確認ください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) を Aurora の置き換えと共に実行した後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を適切な値に更新します。値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで参照できます。

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

- 移行プロセスを開始するには、`migrate_v0_v1.py` スクリプトを実行します。このスクリプトは、すべてのボットをスキャンし、埋め込み用の ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを呼び出すための IAM 権限が必要です。

## 移行の代替オプション

以前の方法に関連する時間とコストの影響により、別のアプローチを検討したい場合は、次の代替手段を検討してください：

### スナップショットの復元とDMSによる移行

まず、現在のAuroraクラスターにアクセスするためのパスワードを確認します。次に、`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから復元して、一時的なデータベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[同種移行DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これはネイティブな論理レプリケーションに依存しています。この場合、ソースとターゲットのデータベースはPostgreSQLである必要があります。DMSはこの目的のためにネイティブな論理レプリケーションを使用できます。

プロジェクトの特定の要件と制約を考慮して、最適な移行アプローチを選択してください。