# データベース移行ガイド

> [!Warning]
> このガイドはv0からv1用です。

このガイドは、Bedrock Chatの更新時にAuroraクラスターの置き換えを伴うデータ移行の手順を説明します。以下の手順により、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を確保します。

## 概要

移行プロセスは、すべてのボットをスキャンし、それぞれのボットに対して埋め込み ECS タスクを起動することを含みます。このアプローチは、埋め込みの再計算を必要とし、ECS タスクの実行と Bedrock Cohere の使用料金により、時間がかかり追加のコストが発生する可能性があります。これらのコストと時間の要件を避けたい場合は、このガイドの後半で提供される[代替の移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) を Aurora 置換と共に実行した後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数に適切な値を更新してください。値は `CloudFormation` > `BedrockChatStack` > `出力` タブで参照できます。

```py
# AWS Management Consoleで CloudFormation スタックを開き、出力タブから値をコピーします。
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

- 移行プロセスを開始するために `migrate_v0_v1.py` スクリプトを実行します。このスクリプトは、すべてのボットをスキャンし、埋め込み ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを呼び出すための IAM 権限が必要です。

## 代替の移行オプション

上記の方法が時間とコストの観点から望ましくない場合、以下の代替アプローチを検討してください：

### スナップショット復元とDMS移行

まず、現在のAuroraクラスターにアクセスするためのパスワードをメモしてください。その後、`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから一時データベースを復元します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[DMSの同種移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これはネイティブの論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースがPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを活用できます。

プロジェクトの具体的な要件と制約を考慮して、最適な移行アプローチを選択してください。