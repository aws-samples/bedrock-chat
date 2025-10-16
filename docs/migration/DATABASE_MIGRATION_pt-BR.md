# Guia de Migração de Banco de Dados

> [!Warning]
> Este guia é para v0 a v1.

Este guia descreve os passos para migrar dados ao realizar uma atualização do Bedrock Chat que contém uma substituição de cluster Aurora. O procedimento a seguir garante uma transição suave, minimizando o tempo de inatividade e a perda de dados.

## Visão Geral

O processo de migração envolve a varredura de todos os bots e o lançamento de tarefas ECS de embedding para cada um deles. Essa abordagem requer o recálculo dos embeddings, o que pode consumir muito tempo e incorrer em custos adicionais devido às taxas de execução de tarefas ECS e uso do Bedrock Cohere. Se você preferir evitar esses custos e requisitos de tempo, consulte as [opções alternativas de migração](#alternative-migration-options) fornecidas mais adiante neste guia.

## Etapas de Migração

- Após [npx cdk deploy](../README.md#deploy-using-cdk) com a substituição do Aurora, abra o script [migrate_v0_v1.py](./migrate_v0_v1.py) e atualize as seguintes variáveis com os valores apropriados. Os valores podem ser consultados na aba `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Abra a pilha do CloudFormation no Console de Gerenciamento da AWS e copie os valores da aba Outputs.
# Chave: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Chave: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Chave: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Não precisa alterar
# Chave: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Chave: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Execute o script `migrate_v0_v1.py` para iniciar o processo de migração. Este script irá escanear todos os bots, iniciar tarefas de embedding do ECS e criar os dados no novo cluster Aurora. Observe que:
  - O script requer `boto3`.
  - O ambiente requer permissões IAM para acessar a tabela do DynamoDB e invocar tarefas do ECS.

## Opções Alternativas de Migração

Se você preferir não usar o método acima devido às implicações de tempo e custo associadas, considere as seguintes abordagens alternativas:

### Restauração de Snapshot e Migração DMS

Primeiro, anote a senha para acessar o cluster Aurora atual. Em seguida, execute `npx cdk deploy`, que aciona a substituição do cluster. Depois disso, crie um banco de dados temporário restaurando a partir de um snapshot do banco de dados original.
Use o [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) para migrar dados do banco de dados temporário para o novo cluster Aurora.

Nota: A partir de 29 de maio de 2024, o DMS não suporta nativamente a extensão pgvector. No entanto, você pode explorar as seguintes opções para contornar esta limitação:

Use a [migração homogênea DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), que aproveita a replicação lógica nativa. Neste caso, tanto o banco de dados de origem quanto o de destino devem ser PostgreSQL. O DMS pode aproveitar a replicação lógica nativa para este propósito.

Considere os requisitos específicos e as restrições do seu projeto ao escolher a abordagem de migração mais adequada.