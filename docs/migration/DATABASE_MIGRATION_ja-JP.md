# データベース移行ガイド

> [!Warning]
> このガイドは v0 から v1 向けです。

このガイドは、Bedrock Chatの更新時にAuroraクラスターの置き換えを伴うデータ移行の手順を説明します。以下の手順により、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を確保します。

## 概要

移行プロセスは、すべてのボットをスキャンし、それぞれに対して埋め込み ECS タスクを起動することを伴います。このアプローチは、埋め込みの再計算が必要であり、ECS タスクの実行と Bedrock Cohere の使用料金により、時間とコストがかかる可能性があります。これらのコストと時間要件を回避したい場合は、後述の[代替移行オプション](#alternative-migration-options)を参照してください。

## マイグレーションステップ

- [npx cdk deploy](../README.md#deploy-using-cdk) で Aurora の置き換えを行った後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数に適切な値を設定してください。値は `CloudFormation` > `BedrockChatStack` > `出力` タブで確認できます。

```py
# AWS 管理コンソールで CloudFormation スタックを開き、出力タブから値をコピーしてください。
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

- `migrate_v0_v1.py` スクリプトを実行して、マイグレーションプロセスを開始します。このスクリプトは、すべてのボットをスキャンし、埋め込み ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを起動するための IAM 権限が必要です。

## 代替移行オプション

上記の方法が時間とコストの観点から望ましくない場合は、以下の代替アプローチを検討してください：

### スナップショット復元とDMS移行

まず、現在のAuroraクラスターにアクセスするためのパスワードを確認します。次に、`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから一時データベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[DMSホモジニアス移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これは、ネイティブの論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースがPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを活用できます。

プロジェクトの特定の要件と制約を考慮して、最適な移行アプローチを選択してください。