# データベース移行ガイド

このガイドは、Bedrock Claude Chatの更新時におけるデータ移行の手順を説明します。これにはAuroraクラスターの置き換えが含まれます。以下のプロセスにより、移行を円滑に実行し、ダウンタイムとデータ損失を最小限に抑えます。

## 概要

移行プロセスには、すべてのボットをスキャンし、各ボットに対してECSの埋め込みタスクを起動することが含まれます。このアプローチでは、埋め込みを再計算する必要があり、時間がかかり、ECSタスクの実行とBedrock Cohereの使用料による追加のコストが発生する可能性があります。これらの時間とコストを避けたい場合は、このガイドの後半で提供されている[代替の移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) で Aurora を置き換えた後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を適切な値に更新します。値は `CloudFormation` タブ > `BedrockChatStack` > `Outputs` から参照できます。

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

- `migrate_v0_v1.py` スクリプトを実行して移行プロセスを開始します。このスクリプトはすべてのボットをスキャンし、ECS 埋め込みタスクを起動し、新しい Aurora クラスターにデータを作成します。注意点は以下の通りです：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを起動するための IAM 権限が必要です。

## 代替の移行オプション

上記の方法が時間とコストの観点から望ましくない場合、以下の代替アプローチを検討してください：

### スナップショットの復元とDMSの移行

まず、現在のAuroraクラスターにアクセスするためのパスワードを記録します。次に、`npx cdk deploy`を実行すると、クラスターの置き換えがトリガーされます。その後、元のデータベースのスナップショットから復元して、一時的なデータベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時的なデータベースから新しいAuroraクラスターにデータを移行します。

注意: 2024年5月29日の時点で、DMSはpgvectorネイティブ拡張機能をサポートしていません。ただし、この制限に対処するために以下のオプションを検討できます：

[DMSの同種移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用し、ネイティブ論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースはPostgreSQLである必要があります。DMSはこの目的のためにネイティブ論理レプリケーションを活用できます。

プロジェクトの具体的な要件と制約を考慮して、最適な移行方法を選択してください。