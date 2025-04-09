# データベース移行ガイド

このガイドは、Auroraクラスターの置き換えを含むBedrock Claude Chatの更新時のデータ移行手順を説明します。以下の手順により、最小限のダウンタイムとデータ損失で円滑な移行を確保します。

## 概要

移行プロセスは、すべてのボットをスキャンし、それぞれに対してECSタスクの埋め込みを起動することを含みます。このアプローチは、埋め込みの再計算が必要であり、ECSタスクの実行とBedrock Cohereの使用料金により、時間とコストがかかる可能性があります。これらのコストと時間の必要性を避けたい場合は、この後のガイドで紹介される[代替移行オプション](#alternative-migration-options)をご確認ください。

## 移行ステップ

- [npx cdk deploy](../README.md#deploy-using-cdk) で Aurora 置換後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、以下の変数を該当する値に更新します。値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブから参照できます。

```py
# AWS Management Consoleで CloudFormation スタックを開き、Outputs タブから値をコピーします。
# キー: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# キー: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# キー: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 変更の必要はありません
# キー: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# キー: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- `migrate_v0_v1.py` スクリプトを実行して、移行プロセスを開始します。このスクリプトは、すべてのボットを検索し、埋め込み ECS タスクを起動し、新しい Aurora クラスターにデータを作成します。以下に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを起動するための IAM 権限が必要です。

## 代替の移行オプション

上記の方法が時間とコストの観点から望ましくない場合、以下の代替アプローチを検討できます：

### スナップショットリストアとDMS移行

まず、現在のAuroraクラスターにアクセスするためのパスワードを確認します。次に、`npx cdk deploy`を実行し、クラスターの置き換えをトリガーします。その後、元のデータベースのスナップショットから一時データベースを復元します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意：2024年5月29日現在、DMSはpgvectorエクステンションをネイティブにサポートしていません。ただし、この制限を回避するために以下のオプションを検討できます：

[DMSの同種移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これは組み込みの論理レプリケーションを利用します。この場合、ソースとターゲットのデータベースは両方ともPostgreSQLである必要があります。DMSはこの目的のために組み込みの論理レプリケーションを活用できます。

プロジェクトの特定の要件と制約を考慮して、最も適切な移行アプローチを選択してください。