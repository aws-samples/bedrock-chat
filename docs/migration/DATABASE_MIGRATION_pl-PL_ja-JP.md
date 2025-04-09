# データベース移行ガイド

このガイドは、Bedrock Claude Chatのクラスターの更新に伴うデータ移行の手順を説明します。以下の手順により、ダウンタイムとデータ損失を最小限に抑えながら、スムーズな移行を実現します。

## 概要

移行プロセスは、すべてのボットをスキャンし、各ボットに対してECSの埋め込みタスクを実行することで構成されます。このアプローチでは、埋め込みの再計算が必要となり、ECSタスクの実行とBedrockのCohere サービス利用に伴う追加コストにより、時間とコストがかかる可能性があります。これらのコストと時間の要件を回避したい場合は、このガイドの後半で説明する[代替の移行オプション](#alternative-migration-options)をご確認ください。

## 移行手順

- [npx cdk deploy](../README.md#deploy-using-cdk) を実行して Aurora を置き換えた後、[migrate_v0_v1.py](./migrate_v0_v1.py) スクリプトを開き、次の変数を適切な値に更新します。値は `CloudFormation` > `BedrockChatStack` > `Outputs` タブで確認できます。

```py
# AWS Management Console で CloudFormation スタックを開き、Outputs タブから値をコピーしてください。
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

- `migrate_v0_v1.py` スクリプトを実行して、移行プロセスを初期化します。このスクリプトはすべてのボットをスキャンし、ECS 埋め込みタスクを実行して、新しい Aurora クラスターにデータを作成します。以下の点に注意してください：
  - スクリプトには `boto3` が必要です。
  - 環境には、DynamoDB テーブルにアクセスし、ECS タスクを呼び出すための IAM 権限が必要です。

## 移行の代替オプション

上記の方法が時間とコストの観点から望ましくない場合は、以下の代替アプローチを検討してください：

### スナップショットの復元とDMSによる移行

まず、現在のAuroraクラスターへのアクセスパスワードをメモします。次に、`npx cdk deploy`を実行して、クラスターを置き換えます。その後、元のデータベースのスナップショットから一時的なデータベースを復元します。
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)を使用して、一時データベースから新しいAuroraクラスターにデータを移行します。

注意: 2024年5月29日現在、DMSはpgvectorの拡張機能をネイティブにサポートしていません。ただし、以下の回避策を検討できます：

[同種のDMS移行](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)を使用します。これはネイティブな論理レプリケーションを活用します。この場合、ソースとターゲットのデータベースの両方がPostgreSQLである必要があります。DMSはこの目的のためにネイティブな論理レプリケーションを利用できます。

プロジェクトの特定の要件と制約を考慮して、最も適切な移行アプローチを選択してください。