# Datenbank-Migrations-Leitfaden

> [!Warning]
> Dieser Leitfaden gilt für die Migration von v0 auf v1.

Dieser Leitfaden beschreibt die Schritte zur Datenmigration bei der Durchführung eines Updates von Bedrock Chat, das einen Aurora-Cluster-Austausch beinhaltet. Das folgende Verfahren gewährleistet einen reibungslosen Übergang bei minimaler Ausfallzeit und minimalem Datenverlust.

## Überblick

Der Migrationsprozess umfasst das Scannen aller Bots und das Starten von Embedding-ECS-Tasks für jeden von ihnen. Dieser Ansatz erfordert eine Neuberechnung der Embeddings, was zeitaufwändig sein kann und zusätzliche Kosten durch die Ausführung von ECS-Tasks und Bedrock Cohere-Nutzungsgebühren verursacht. Wenn Sie diese Kosten und den zeitlichen Aufwand vermeiden möchten, lesen Sie bitte die [alternativen Migrationsoptionen](#alternative-migration-options), die später in diesem Leitfaden beschrieben werden.

## Migrationsschritte

- Nach [npx cdk deploy](../README.md#deploy-using-cdk) mit Aurora-Ersetzung, öffnen Sie das Skript [migrate_v0_v1.py](./migrate_v0_v1.py) und aktualisieren Sie die folgenden Variablen mit den entsprechenden Werten. Die Werte können unter `CloudFormation` > `BedrockChatStack` > Tab `Outputs` eingesehen werden.

```py
# Open the CloudFormation stack in the AWS Management Console and copy the values from the Outputs tab.
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # No need to change
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Führen Sie das Skript `migrate_v0_v1.py` aus, um den Migrationsprozess zu starten. Dieses Skript wird alle Bots scannen, Embedding-ECS-Tasks starten und die Daten in den neuen Aurora-Cluster schreiben. Beachten Sie:
  - Das Skript benötigt `boto3`.
  - Die Umgebung benötigt IAM-Berechtigungen für den Zugriff auf die DynamoDB-Tabelle und das Ausführen von ECS-Tasks.

## Alternative Migrationsmöglichkeiten

Wenn Sie die oben genannte Methode aufgrund der damit verbundenen Zeit- und Kostenimplikationen nicht verwenden möchten, erwägen Sie die folgenden alternativen Ansätze:

### Snapshot-Wiederherstellung und DMS-Migration

Notieren Sie sich zunächst das Passwort für den Zugriff auf den aktuellen Aurora-Cluster. Führen Sie dann `npx cdk deploy` aus, was den Austausch des Clusters auslöst. Erstellen Sie danach eine temporäre Datenbank durch Wiederherstellung aus einem Snapshot der ursprünglichen Datenbank.
Nutzen Sie den [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/), um Daten von der temporären Datenbank in den neuen Aurora-Cluster zu migrieren.

Hinweis: Stand 29. Mai 2024 unterstützt DMS die pgvector-Erweiterung nicht nativ. Sie können jedoch die folgenden Optionen erkunden, um diese Einschränkung zu umgehen:

Verwenden Sie die [DMS homogene Migration](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), die native logische Replikation nutzt. In diesem Fall müssen sowohl die Quell- als auch die Zieldatenbank PostgreSQL sein. DMS kann die native logische Replikation für diesen Zweck nutzen.

Berücksichtigen Sie die spezifischen Anforderungen und Einschränkungen Ihres Projekts bei der Auswahl des am besten geeigneten Migrationsansatzes.