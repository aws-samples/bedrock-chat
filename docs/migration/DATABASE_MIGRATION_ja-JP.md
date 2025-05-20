# データベース移行ガイド

> [!Warning]
> このガイドはv0からv1用です。

このガイドは、Bedrock Chatの更新時にAuroraクラスターの置き換えを伴うデータ移行の手順を説明します。以下の手順により、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を確保します。

## 概要

移行プロセスは、すべてのボットをスキャンし、それぞれに対して埋め込み ECS タスクを起動することを含みます。このアプローチは、埋め込みの再計算が必要であり、ECS タスクの実行と Bedrock Cohere の使用料金により、時間がかかり追加のコストが発生する可能性があります。これらのコストと時間の要件を回避したい場合は、このガイドの後半で提供される[代替の移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) で Aurora 置換後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を適切な値に更新します。値は `CloudFormation` > `BedrockChatStack` > `出力` タブで参照できます。

```py
# AWS 管理コンソールでクラウドフォーメーションスタックを開き、出力タブから値をコピーします。
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

- 移行プロセスを開始するには、`migrate_v0_v1.py` スクリプトを実行します。このスクリプトは、すべてのボットをスキャンし、埋め込み ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを起動するための IAM 権限が必要です。

## 代替の移行オプション

上記の方法を、関連する時間とコストの影響により使用したくない場合は、以下の代替アプローチを検討してください：

### スナップショット復元とDMS移行

まず、現在のAuroraクラスターにアクセスするためのパスワードに注意してください。その後、`npx cdk deploy`を実行すると、クラスターの置き換えがトリガーされます。その後、元のデータベースのスナップショットから復元して、一時的なデータベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時的なデータベースから新しいAuroraクラスターにデータを移行します。

注意: 2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[DMSホモジニアス移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これは、ネイティブの論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースはPostgreSQLである必要があります。DMSはこの目的のためにネイティブの論理レプリケーションを活用できます。

プロジェクトの特定の要件と制約を考慮して、最も適切な移行アプローチを選択してください。