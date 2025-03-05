# Guida alla Migrazione del Database

Questa guida illustra i passaggi per migrare i dati durante un aggiornamento di Bedrock Claude Chat che comporta la sostituzione di un cluster Aurora. La seguente procedura garantisce una transizione fluida, minimizzando i tempi di inattività e la perdita di dati.

## Panoramica

Il processo di migrazione prevede la scansione di tutti i bot e l'avvio di attività ECS per l'embedding di ciascuno di essi. Questo approccio richiede il ricalcolo degli embedding, che può essere dispendioso in termini di tempo e comportare costi aggiuntivi dovuti all'esecuzione di attività ECS e alle tariffe di utilizzo di Bedrock Cohere. Se si preferisce evitare questi costi e requisiti temporali, fare riferimento alle [opzioni alternative di migrazione](#alternative-migration-options) descritte più avanti in questa guida.

## Passaggi di Migrazione

- Dopo [npx cdk deploy](../README.md#deploy-using-cdk) con sostituzione Aurora, aprire lo script [migrate.py](./migrate.py) e aggiornare le seguenti variabili con i valori appropriati. I valori possono essere consultati nella scheda `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Aprire lo stack CloudFormation nella Console di gestione AWS e copiare i valori dalla scheda Outputs.
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

- Eseguire lo script `migrate.py` per avviare il processo di migrazione. Questo script eseguirà la scansione di tutti i bot, avvierà attività di embedding ECS e creerà i dati nel nuovo cluster Aurora. Nota che:
  - Lo script richiede `boto3`.
  - L'ambiente richiede autorizzazioni IAM per accedere alla tabella DynamoDB e invocare le attività ECS.

## Opzioni Alternative di Migrazione

Se preferisci non utilizzare il metodo precedente a causa delle implicazioni di tempo e costi, considera i seguenti approcci alternativi:

### Ripristino da Snapshot e Migrazione DMS

Per prima cosa, prendi nota della password per accedere al cluster Aurora corrente. Quindi esegui `npx cdk deploy`, che attiva la sostituzione del cluster. Successivamente, crea un database temporaneo ripristinando da uno snapshot del database originale.
Usa [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) per migrare i dati dal database temporaneo al nuovo cluster Aurora.

Nota: A partire dal 29 maggio 2024, DMS non supporta nativamente l'estensione pgvector. Tuttavia, puoi esplorare le seguenti opzioni per aggirare questa limitazione:

Utilizza la [migrazione omogenea DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), che sfrutta la replica logica nativa. In questo caso, sia il database di origine che quello di destinazione devono essere PostgreSQL. DMS può sfruttare la replica logica nativa a questo scopo.

Considera i requisiti e i vincoli specifici del tuo progetto quando scegli l'approccio di migrazione più adatto.