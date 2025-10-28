# Guide de Migration de Base de Données

> [!Warning]
> Ce guide concerne la migration de v0 vers v1.

Ce guide décrit les étapes pour migrer les données lors d'une mise à jour de Bedrock Chat qui comprend un remplacement de cluster Aurora. La procédure suivante assure une transition en douceur tout en minimisant les temps d'arrêt et la perte de données.

## Vue d'ensemble

Le processus de migration implique l'analyse de tous les bots et le lancement de tâches ECS d'embedding pour chacun d'entre eux. Cette approche nécessite un recalcul des embeddings, ce qui peut prendre du temps et entraîner des coûts supplémentaires en raison des frais d'exécution des tâches ECS et d'utilisation de Bedrock Cohere. Si vous préférez éviter ces coûts et ces contraintes de temps, veuillez consulter les [options alternatives de migration](#alternative-migration-options) présentées plus loin dans ce guide.

## Étapes de Migration

- Après [npx cdk deploy](../README.md#deploy-using-cdk) avec le remplacement Aurora, ouvrez le script [migrate_v0_v1.py](./migrate_v0_v1.py) et mettez à jour les variables suivantes avec les valeurs appropriées. Les valeurs peuvent être consultées dans l'onglet `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Ouvrez la pile CloudFormation dans la console AWS Management et copiez les valeurs depuis l'onglet Outputs.
# Clé : DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Clé : EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Clé : EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Pas besoin de modifier
# Clé : PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Clé : EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Exécutez le script `migrate_v0_v1.py` pour lancer le processus de migration. Ce script analysera tous les bots, lancera les tâches d'embedding ECS et créera les données dans le nouveau cluster Aurora. Notez que :
  - Le script nécessite `boto3`.
  - L'environnement nécessite des autorisations IAM pour accéder à la table dynamodb et pour invoquer les tâches ECS.

## Options de Migration Alternatives

Si vous préférez ne pas utiliser la méthode ci-dessus en raison des implications en termes de temps et de coûts, considérez les approches alternatives suivantes :

### Restauration de Snapshot et Migration DMS

Tout d'abord, notez le mot de passe pour accéder au cluster Aurora actuel. Ensuite, exécutez `npx cdk deploy`, qui déclenche le remplacement du cluster. Après cela, créez une base de données temporaire en restaurant à partir d'un snapshot de la base de données d'origine.
Utilisez [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) pour migrer les données de la base de données temporaire vers le nouveau cluster Aurora.

Note : Au 29 mai 2024, DMS ne prend pas nativement en charge l'extension pgvector. Cependant, vous pouvez explorer les options suivantes pour contourner cette limitation :

Utilisez la [migration homogène DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), qui exploite la réplication logique native. Dans ce cas, les bases de données source et cible doivent être PostgreSQL. DMS peut utiliser la réplication logique native à cette fin.

Prenez en compte les exigences et contraintes spécifiques de votre projet lors du choix de l'approche de migration la plus appropriée.