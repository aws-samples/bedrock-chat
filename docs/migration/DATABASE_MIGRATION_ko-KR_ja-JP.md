# データベース移行ガイド

このガイドは、Auroraクラスターの置き換えを含むBedrock Claude Chatの更新時にデータを移行する手順を説明します。以下の手順は、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を保証します。

## 概要

マイグレーションプロセスには、すべてのボットをスキャンし、各ボットの埋め込みECSタスクを開始することが含まれます。このアプローチは、埋め込みを再計算する必要があるため、時間がかかる可能性があり、ECSタスクの実行とBedrock Cohereの使用料金により追加のコストが発生する可能性があります。これらのコストと時間の要件を避けたい場合は、このガイドの後半で提供されている[代替マイグレーションオプション](#alternative-migration-options)を参照してください。

## マイグレーションステップ

- [npx cdk deploy](../README.md#deploy-using-cdk)でAuroraを置き換えた後、[migrate_v0_v1.py](./migrate_v0_v1.py)スクリプトを開き、以下の変数を適切な値に更新してください。値は`CloudFormation` > `BedrockChatStack` > `Outputs`タブから参照できます。

```py
# AWS管理コンソールでCloudFormationスタックを開き、Outputsタブから値をコピーしてください。
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

- マイグレーションプロセスを開始するには、`migrate_v0_v1.py`スクリプトを実行してください。このスクリプトはすべてのボットをスキャンし、埋め込みECSタスクを実行し、新しいAuroraクラスターにデータを作成します。以下の点に注意してください：
  - スクリプトは`boto3`を必要とします。
  - 環境には、DynamoDBテーブルにアクセスし、ECSタスクを呼び出すためのIAMアクセス許可が必要です。

## 代替マイグレーションオプション

時間とコストの観点から、前述の方法が好ましくない場合は、次の代替アプローチを検討してください：

### スナップショット復元とDMSマイグレーション

まず、現在のAuroraクラスターにアクセスするためのパスワードをメモしてください。次に、`npx cdk deploy`を実行してクラスターを置き換えます。その後、ソースデータベースのスナップショットを復元して、一時データベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意: 2024年5月29日現在、DMSはpgvectorエクステンションをデフォルトでサポートしていません。ただし、この制限を解決するために次のオプションを検討できます：

[DMS同種マイグレーション](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用して、ネイティブな論理レプリケーションを活用します。この場合、ソースとターゲットのデータベースはどちらもPostgreSQLである必要があります。DMSはこのためにネイティブな論理レプリケーションを活用できます。

プロジェクトの特定の要件と制約を考慮して、最適なマイグレーションアプローチを選択してください。