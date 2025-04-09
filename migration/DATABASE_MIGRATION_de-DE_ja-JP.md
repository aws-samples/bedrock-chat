# データベース移行ガイド

このガイドは、Auroraクラスターの交換を含むBedrock Claude Chatのアップデートにおけるデータ移行の手順を説明します。以下の手順により、最小限のダウンタイムとデータ損失で円滑な移行を確保します。

## 概要

移行プロセスは、すべてのボットをスキャンし、各ボットに対して埋め込みECSタスクを起動することで構成されます。このアプローチは埋め込みの再計算を必要とし、時間がかかる可能性があり、ECSタスクの実行とBedrock Cohereの使用料による追加のコストを発生させる可能性があります。これらのコストと時間要件を回避したい場合は、このガイドの後半で説明する[代替の移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) を実行して Aurora に置き換えた後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を対応する値に更新します。値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで確認できます。

```py
# AWS Management Console で CloudFormation スタックを開き、Outputs タブから値をコピーします。
# キー: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# キー: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# キー: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 変更しないでください
# キー: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# キー: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 移行プロセスを開始するには、`migrate_v0_v1.py` スクリプトを実行します。このスクリプトは、すべてのボットをスキャンし、Embedding の ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。注意点：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを起動するための IAM 権限が必要です。

## 代替の移行方法

以前の方法を時間とコストの観点から利用したくない場合は、以下の代替アプローチを検討してください：

### スナップショット復元とDMS移行

まず、現在のAuroraクラスターにアクセスするためのパスワードをメモします。次に、`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットを復元して一時データベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日の時点で、DMSはpgvector拡張機能をネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[DMS同種移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を利用し、ネイティブの論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースはPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを利用できます。

プロジェクトの具体的な要件と制約を考慮し、最適な移行アプローチを選択してください。