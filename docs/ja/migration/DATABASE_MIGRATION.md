# データベース移行ガイド

このガイドでは、Auroraクラスターの置き換えを含むBedrock Claude Chatの更新時にデータを移行する手順を説明します。以下の手順により、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を実現します。

## 概要

移行プロセスは、すべてのボットをスキャンし、それぞれに対して埋め込み ECS タスクを起動することを含みます。このアプローチでは、埋め込みの再計算が必要となり、時間がかかる可能性があり、ECS タスクの実行と Bedrock Cohere の使用料金により追加のコストが発生する可能性があります。これらのコストと時間の要件を避けたい場合は、このガイドの後半で提供されている[代替の移行オプション](#alternative-migration-options)を参照してください。

## マイグレーションステップ

- [npx cdk deploy](../README.md#deploy-using-cdk) で Aurora の置き換えを行った後、[migrate.py](./migrate.py) スクリプトを開き、以下の変数を適切な値に更新します。値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで確認できます。

```py
# AWS マネジメントコンソールで CloudFormation スタックを開き、Outputs タブから値をコピーします。
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

- マイグレーションプロセスを開始するには、`migrate.py` スクリプトを実行します。このスクリプトは、すべてのボットをスキャンし、埋め込み ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを呼び出すための IAM 権限が必要です。

## 代替の移行オプション

上記の方法が時間とコストの観点から望ましくない場合は、以下の代替アプローチを検討してください：

### スナップショット復元とDMS移行

まず、現在のAuroraクラスタにアクセスするためのパスワードに注意してください。次に`npx cdk deploy`を実行し、クラスタの置き換えをトリガーします。その後、元のデータベースのスナップショットから一時データベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスタにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[DMSホモジニアス移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これはネイティブの論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースはPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを活用できます。

プロジェクトの特定の要件と制約を考慮して、最も適切な移行アプローチを選択してください。