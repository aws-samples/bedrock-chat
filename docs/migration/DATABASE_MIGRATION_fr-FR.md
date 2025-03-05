# Guide de Migration de Base de Données

Ce guide décrit les étapes de migration des données lors de la mise à jour de Bedrock Claude Chat, qui implique le remplacement d'un cluster Aurora. La procédure suivante garantit une transition en douceur tout en minimisant les temps d'arrêt et les pertes de données.

## Vue d'ensemble

Le processus de migration implique de scanner tous les bots et de lancer des tâches ECS d'intégration pour chacun d'entre eux. Cette approche nécessite un recalcul des intégrations, ce qui peut être long et entraîner des coûts supplémentaires en raison de l'exécution des tâches ECS et des frais d'utilisation de Bedrock Cohere. Si vous souhaitez éviter ces coûts et ces contraintes de temps, veuillez consulter les [options de migration alternatives](#alternative-migration-options) présentées plus loin dans ce guide.

## Étapes de Migration

- Après [npx cdk deploy](../README.md#deploy-using-cdk) avec le remplacement Aurora, ouvrez le script [migrate.py](./migrate.py) et mettez à jour les variables suivantes avec les valeurs appropriées. Les valeurs peuvent être consultées dans l'onglet `CloudFormation` > `BedrockChatStack` > `Sorties`.

```py
# Ouvrez la pile CloudFormation dans la console de gestion AWS et copiez les valeurs depuis l'onglet Sorties.
# Clé : DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Clé : EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Clé : EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Pas besoin de changer
# Clé : PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Clé : EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Exécutez le script `migrate.py` pour lancer le processus de migration. Ce script analysera tous les bots, lancera des tâches ECS d'embedding et créera les données dans le nouveau cluster Aurora. Notez que :
  - Le script nécessite `boto3`.
  - L'environnement requiert des autorisations IAM pour accéder à la table DynamoDB et invoquer des tâches ECS.

## Options de Migration Alternative

Si vous préférez ne pas utiliser la méthode précédente en raison des implications de temps et de coût associées, considérez les approches alternatives suivantes :

### Restauration d'Instantané et Migration DMS

Tout d'abord, notez le mot de passe pour accéder au cluster Aurora actuel. Ensuite, exécutez `npx cdk deploy`, ce qui déclenche le remplacement du cluster. Après cela, créez une base de données temporaire en restaurant à partir d'un instantané de la base de données d'origine.
Utilisez [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) pour migrer les données de la base de données temporaire vers le nouveau cluster Aurora.

Remarque : Au 29 mai 2024, DMS ne prend pas nativement en charge l'extension pgvector. Cependant, vous pouvez explorer les options suivantes pour contourner cette limitation :

Utilisez la [migration homogène de DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), qui s'appuie sur la réplication logique native. Dans ce cas, les bases de données source et cible doivent être PostgreSQL. DMS peut utiliser la réplication logique native à cette fin.

Considérez les exigences et contraintes spécifiques de votre projet lors du choix de l'approche de migration la plus appropriée.