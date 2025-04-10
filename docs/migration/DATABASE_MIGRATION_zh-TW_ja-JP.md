# データベース移行ガイド

本ガイドは、Aurora クラスターの置き換えを含む Bedrock Claude Chat の更新時にデータを移行する手順の概要を説明します。以下の手順により、停止時間とデータ損失を最小限に抑えながら、スムーズな移行を確実に行います。

## 概要

移行プロセスには、すべてのボットをスキャンし、各ボットに対して埋め込み ECS タスクを起動することが含まれます。このアプローチでは埋め込みを再計算する必要があり、ECS タスクの実行と Bedrock Cohere の使用によって時間とコストがかかる可能性があります。これらのコストと時間の要件を回避したい場合は、後述の[代替移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) を使用して Aurora に置き換えた後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を適切な値に更新してください。これらの値は、`CloudFormation` > `BedrockChatStack` > `Outputs` タブで確認できます。

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

- `migrate_v0_v1.py` スクリプトを実行して、移行プロセスを開始します。このスクリプトは、すべてのボットをスキャンし、埋め込み ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを呼び出すための IAM 権限が必要です。

## Alternative Migration Options

如果您不想使用上述方法，考慮到相關的時間和成本影響，可以考慮以下替代方案：

### スナップショット復元とDMSによる移行

まず、現在のAuroraクラスターにアクセスするためのパスワードをメモしておきます。次に、`npx cdk deploy`を実行すると、クラスターの置き換えがトリガーされます。その後、元のデータベースのスナップショットから一時的なデータベースを復元します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時的なデータベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。しかし、この制限を解決するための以下のオプションを検討できます：

[DMSの同種移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これは、ネイティブな論理レプリケーションを活用します。この場合、ソースとターゲットのデータベースは両方ともPostgreSQLである必要があります。DMSはネイティブな論理レプリケーションを利用してこれを実現できます。

プロジェクトの具体的な要件と制約を考慮して、最適な移行方法を選択してください。