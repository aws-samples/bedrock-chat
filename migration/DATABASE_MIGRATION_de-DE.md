# Leitfaden zur Datenbankmigration

> [!Warnung]
> Dieser Leitfaden gilt für v0 bis v1.

Dieser Leitfaden beschreibt die Schritte zur Datenmigration bei einem Update von Bedrock Chat, das einen Austausch des Aurora-Clusters beinhaltet. Das folgende Verfahren gewährleistet einen reibungslosen Übergang bei minimaler Ausfallzeit und minimalen Datenverlusten.

## Übersicht

Der Migrationsprozess umfasst das Scannen aller Bots und das Starten von Einbettungs-ECS-Aufgaben für jeden einzelnen. Dieser Ansatz erfordert eine Neuberechnung der Einbettungen, was zeitaufwendig sein kann und zusätzliche Kosten durch ECS-Aufgabenausführung und Bedrock Cohere-Nutzungsgebühren verursacht. Wenn Sie diese Kosten und Zeitanforderungen vermeiden möchten, konsultieren Sie bitte die [alternativen Migrationsoptionen](#alternative-migration-options), die später in dieser Anleitung beschrieben werden.

## Migrationschritte

- Nach [npx cdk deploy](../README.md#deploy-using-cdk) mit Aurora-Ersatz öffnen Sie das Skript [migrate_v0_v1.py](./migrate_v0_v1.py) und aktualisieren Sie die folgenden Variablen mit den entsprechenden Werten. Die Werte können in `CloudFormation` > `BedrockChatStack` > Registerkarte `Ausgaben` nachgeschlagen werden.

```py
# Öffnen Sie den CloudFormation-Stack in der AWS Management Console und kopieren Sie die Werte von der Ausgaben-Registerkarte.
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

- Führen Sie das Skript `migrate_v0_v1.py` aus, um den Migrationsprozess zu starten. Dieses Skript wird alle Bots scannen, Embedding-ECS-Tasks starten und die Daten im neuen Aurora-Cluster erstellen. Bitte beachten Sie:
  - Das Skript benötigt `boto3`.
  - Die Umgebung erfordert IAM-Berechtigungen für den Zugriff auf die DynamoDB-Tabelle und zum Starten von ECS-Tasks.

## Alternative Migrationsmöglichkeiten

Wenn Sie die vorherige Methode aufgrund von Zeit- und Kostenimplikationen nicht nutzen möchten, ziehen Sie die folgenden alternativen Ansätze in Betracht:

### Snapshot-Wiederherstellung und DMS-Migration

Notieren Sie zunächst das Passwort für den Zugriff auf den aktuellen Aurora-Cluster. Führen Sie dann `npx cdk deploy` aus, was den Ersatz des Clusters auslöst. Erstellen Sie anschließend eine temporäre Datenbank, indem Sie einen Snapshot der ursprünglichen Datenbank wiederherstellen.
Verwenden Sie [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/), um Daten von der temporären Datenbank in den neuen Aurora-Cluster zu migrieren.

Hinweis: Bis zum 29. Mai 2024 unterstützt DMS die pgvector-Erweiterung nicht nativ. Sie können jedoch folgende Optionen in Betracht ziehen, um diese Einschränkung zu umgehen:

Verwenden Sie die [DMS homogene Migration](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), die native logische Replikation nutzt. In diesem Fall müssen sowohl die Quell- als auch die Zieldatenbank PostgreSQL sein. DMS kann die native logische Replikation für diesen Zweck nutzen.

Berücksichtigen Sie die spezifischen Anforderungen und Einschränkungen Ihres Projekts bei der Auswahl des am besten geeigneten Migrationansatzes.