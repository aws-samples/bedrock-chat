# Guida alla Migrazione del Database

> [!Warning]
> Questa guida è per la migrazione da v0 a v1.

Questa guida descrive i passaggi per migrare i dati durante un aggiornamento di Bedrock Chat che comporta la sostituzione di un cluster Aurora. La seguente procedura garantisce una transizione fluida riducendo al minimo i tempi di inattività e la perdita di dati.

## Panoramica

Il processo di migrazione prevede la scansione di tutti i bot e l'avvio di attività ECS per l'embedding di ciascuno di essi. Questo approccio richiede il ricalcolo degli embedding, che può essere dispendioso in termini di tempo e comportare costi aggiuntivi dovuti all'esecuzione di attività ECS e alle tariffe di utilizzo di Bedrock Cohere. Se si preferisce evitare questi costi e requisiti temporali, fare riferimento alle [opzioni alternative di migrazione](#alternative-migration-options) descritte più avanti in questa guida.

## Passaggi di Migrazione

- Dopo [npx cdk deploy](../README.md#deploy-using-cdk) con sostituzione Aurora, aprire lo script [migrate_v0_v1.py](./migrate_v0_v1.py) e aggiornare le seguenti variabili con i valori appropriati. I valori possono essere trovati nella scheda `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Aprire lo stack CloudFormation nella Console di Gestione AWS e copiare i valori dalla scheda Outputs.
# Chiave: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Chiave: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Chiave: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Non è necessario modificare
# Chiave: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Chiave: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Eseguire lo script `migrate_v0_v1.py` per avviare il processo di migrazione. Questo script eseguirà la scansione di tutti i bot, avvierà attività ECS di embedding e creerà i dati nel nuovo cluster Aurora. Nota che:
  - Lo script richiede `boto3`.
  - L'ambiente richiede autorizzazioni IAM per accedere alla tabella DynamoDB e richiamare le attività ECS.

## Opzioni Alternative di Migrazione

Se non si desidera utilizzare il metodo precedente a causa delle relative implicazioni di tempo e costi, considerare i seguenti approcci alternativi:

### Ripristino Snapshot e Migrazione DMS

Innanzitutto, annotare la password per accedere all'attuale cluster Aurora. Quindi eseguire `npx cdk deploy`, che attiva la sostituzione del cluster. Successivamente, creare un database temporaneo ripristinando da uno snapshot del database originale.
Utilizzare [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) per migrare i dati dal database temporaneo al nuovo cluster Aurora.

Nota: Al 29 maggio 2024, DMS non supporta nativamente l'estensione pgvector. Tuttavia, è possibile esplorare le seguenti opzioni per aggirare questa limitazione:

Utilizzare la [migrazione omogenea DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), che sfrutta la replica logica nativa. In questo caso, sia il database di origine che quello di destinazione devono essere PostgreSQL. DMS può sfruttare la replica logica nativa a questo scopo.

Considerare i requisiti e i vincoli specifici del proprio progetto quando si sceglie l'approccio di migrazione più adatto.