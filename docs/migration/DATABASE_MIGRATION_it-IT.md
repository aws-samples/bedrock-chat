# Guida alla Migrazione del Database

> [!Warning]
> Questa guida è per la migrazione da v0 a v1.

Questa guida delinea i passaggi per migrare i dati durante l'aggiornamento di Bedrock Chat che include la sostituzione di un cluster Aurora. La seguente procedura garantisce una transizione fluida minimizzando i tempi di inattività e la perdita di dati.

## Panoramica

Il processo di migrazione prevede la scansione di tutti i bot e l'avvio di task ECS di embedding per ciascuno di essi. Questo approccio richiede il ricalcolo degli embedding, che può richiedere tempo e comportare costi aggiuntivi dovuti all'esecuzione dei task ECS e alle tariffe di utilizzo di Bedrock Cohere. Se preferisci evitare questi costi e requisiti di tempo, consulta le [opzioni alternative di migrazione](#alternative-migration-options) fornite più avanti in questa guida.

## Passaggi per la Migrazione

- Dopo [npx cdk deploy](../README.md#deploy-using-cdk) con la sostituzione di Aurora, aprire lo script [migrate_v0_v1.py](./migrate_v0_v1.py) e aggiornare le seguenti variabili con i valori appropriati. I valori possono essere consultati nella scheda `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Aprire lo stack CloudFormation nella Console di Gestione AWS e copiare i valori dalla scheda Outputs.
# Chiave: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Chiave: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Chiave: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Non necessita modifiche
# Chiave: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Chiave: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Eseguire lo script `migrate_v0_v1.py` per avviare il processo di migrazione. Questo script eseguirà la scansione di tutti i bot, avvierà i task ECS di embedding e creerà i dati nel nuovo cluster Aurora. Da notare che:
  - Lo script richiede `boto3`.
  - L'ambiente richiede permessi IAM per accedere alla tabella dynamodb e per invocare i task ECS.

## Opzioni Alternative di Migrazione

Se preferisci non utilizzare il metodo sopra indicato a causa delle implicazioni di tempo e costi associate, considera i seguenti approcci alternativi:

### Ripristino da Snapshot e Migrazione DMS

Prima di tutto, prendi nota della password per accedere al cluster Aurora attuale. Quindi esegui `npx cdk deploy`, che attiva la sostituzione del cluster. Successivamente, crea un database temporaneo ripristinandolo da uno snapshot del database originale.
Utilizza [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) per migrare i dati dal database temporaneo al nuovo cluster Aurora.

Nota: Al 29 maggio 2024, DMS non supporta nativamente l'estensione pgvector. Tuttavia, puoi esplorare le seguenti opzioni per aggirare questa limitazione:

Utilizza la [migrazione omogenea DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), che sfrutta la replica logica nativa. In questo caso, sia il database di origine che quello di destinazione devono essere PostgreSQL. DMS può sfruttare la replica logica nativa per questo scopo.

Considera i requisiti specifici e i vincoli del tuo progetto quando scegli l'approccio di migrazione più adatto.