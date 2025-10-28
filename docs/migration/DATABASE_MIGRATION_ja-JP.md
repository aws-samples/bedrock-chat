# データベース移行ガイド

> [!Warning]
> このガイドはv0からv1用です。

このガイドでは、Auroraクラスターの置き換えを含むBedrock Chatのアップデートを実行する際のデータ移行手順について説明します。以下の手順に従うことで、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を実現できます。

## 概要

移行プロセスでは、すべてのボットをスキャンし、それぞれに対して埋め込みECSタスクを起動します。このアプローチでは埋め込みの再計算が必要となり、時間がかかる上、ECSタスクの実行とBedrock Cohereの使用料金により追加コストが発生する可能性があります。これらのコストと時間的な要件を避けたい場合は、このガイドの後半で説明する[代替移行オプション](#alternative-migration-options)を参照してください。

## 移行手順

- Aurora の置き換えを含む [npx cdk deploy](../README.md#deploy-using-cdk) の実行後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を適切な値で更新してください。これらの値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで確認できます。

```py
# AWS Management Console の CloudFormation スタックを開き、Outputs タブから値をコピーしてください。
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 変更の必要なし
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- `migrate_v0_v1.py` スクリプトを実行して移行プロセスを開始してください。このスクリプトは全てのボットをスキャンし、埋め込み ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - このスクリプトには `boto3` が必要です。
  - 環境には DynamoDB テーブルへのアクセスと ECS タスクを呼び出すための IAM 権限が必要です。

## 代替移行オプション

時間とコストの影響により上記の方法を使用したくない場合は、以下の代替アプローチを検討してください：

### スナップショットの復元とDMS移行

まず、現在のAuroraクラスターにアクセスするためのパスワードをメモしておきます。次に`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから一時的なデータベースを作成します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvector拡張機能をネイティブにサポートしていません。ただし、この制限に対処するために以下のオプションを検討できます：

[DMSの同種移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これはネイティブの論理レプリケーションを活用します。この場合、ソースとターゲットの両方のデータベースがPostgreSQLである必要があります。DMSはこの目的でネイティブの論理レプリケーションを活用できます。

最適な移行アプローチを選択する際は、プロジェクトの具体的な要件と制約を考慮してください。