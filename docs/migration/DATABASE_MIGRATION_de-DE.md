# Leitfaden zur Datenbankmigration

Dieser Leitfaden beschreibt die Schritte zur Datenmigration bei der Durchführung eines Updates von Bedrock Claude Chat, das einen Austausch des Aurora-Clusters beinhaltet. Das folgende Verfahren gewährleistet einen reibungslosen Übergang bei minimaler Ausfallzeit und minimalen Datenverlusten.

## Übersicht

Der Migrationsprozess umfasst das Scannen aller Bots und das Starten von Embedding-ECS-Tasks für jeden einzelnen. Dieser Ansatz erfordert eine Neuberechnung der Einbettungen, was zeitaufwendig sein und zusätzliche Kosten durch ECS-Task-Ausführung und Bedrock Cohere-Nutzungsgebühren verursachen kann. Wenn Sie diese Kosten und Zeitanforderungen vermeiden möchten, lesen Sie bitte die [alternativen Migrationsmöglichkeiten](#alternative-migration-options), die später in dieser Anleitung beschrieben werden.

## Migrationschritte

- Nach [npx cdk deploy](../README.md#deploy-using-cdk) mit Aurora-Ersatz öffnen Sie das Skript [migrate.py](./migrate.py) und aktualisieren Sie die folgenden Variablen mit den entsprechenden Werten. Die Werte können auf der Registerkarte `CloudFormation` > `BedrockChatStack` > `Ausgabe` nachgeschlagen werden.

```py
# Öffnen Sie den CloudFormation-Stack in der AWS Management Console und kopieren Sie die Werte aus der Ausgabe-Registerkarte.
# Schlüssel: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Schlüssel: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Schlüssel: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Nicht ändern
# Schlüssel: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Schlüssel: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Führen Sie das Skript `migrate.py` aus, um den Migrationsprozess zu starten. Dieses Skript scannt alle Bots, startet Embedding-ECS-Tasks und erstellt die Daten im neuen Aurora-Cluster. Beachten Sie dabei:
  - Das Skript erfordert `boto3`.
  - Die Umgebung benötigt IAM-Berechtigungen für den Zugriff auf die DynamoDB-Tabelle und zum Starten von ECS-Tasks.

## Alternative Migrationsmöglichkeiten

Wenn Sie die vorherige Methode aufgrund von Zeit- und Kostenimplikationen nicht nutzen möchten, erwägen Sie die folgenden alternativen Ansätze:

### Snapshot-Wiederherstellung und DMS-Migration

Notieren Sie zunächst das Passwort für den Zugriff auf den aktuellen Aurora-Cluster. Führen Sie dann `npx cdk deploy` aus, was den Ersatz des Clusters auslöst. Erstellen Sie anschließend eine temporäre Datenbank, indem Sie einen Snapshot der ursprünglichen Datenbank wiederherstellen.
Verwenden Sie [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/), um Daten von der temporären Datenbank in den neuen Aurora-Cluster zu migrieren.

Hinweis: Zum Stand 29. Mai 2024 unterstützt DMS die pgvector-Erweiterung nicht nativ. Es gibt jedoch folgende Möglichkeiten, diese Einschränkung zu umgehen:

Nutzen Sie die [DMS homogene Migration](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), die native logische Replikation nutzt. In diesem Fall müssen sowohl die Quell- als auch die Zieldatenbank PostgreSQL sein. DMS kann die native logische Replikation für diesen Zweck nutzen.

Berücksichtigen Sie die spezifischen Anforderungen und Einschränkungen Ihres Projekts bei der Auswahl des am besten geeigneten Migrationsansatzes.