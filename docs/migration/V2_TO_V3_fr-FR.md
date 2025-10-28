# Guide de migration (v2 à v3)

## TL;DR

- La V3 introduit un contrôle des permissions plus précis et la fonctionnalité Bot Store, nécessitant des changements de schéma DynamoDB
- **Sauvegardez votre table DynamoDB ConversationTable avant la migration**
- Mettez à jour l'URL de votre dépôt de `bedrock-claude-chat` à `bedrock-chat`
- Exécutez le script de migration pour convertir vos données vers le nouveau schéma
- Tous vos bots et conversations seront préservés avec le nouveau modèle de permissions
- **IMPORTANT : Pendant le processus de migration, l'application sera indisponible pour tous les utilisateurs jusqu'à ce que la migration soit terminée. Ce processus prend généralement environ 60 minutes, selon la quantité de données et les performances de votre environnement de développement.**
- **IMPORTANT : Toutes les API publiées doivent être supprimées pendant le processus de migration.**
- **AVERTISSEMENT : Le processus de migration ne peut pas garantir un succès à 100% pour tous les bots. Veuillez documenter vos configurations de bots importantes avant la migration au cas où vous devriez les recréer manuellement**

## Introduction

### Nouveautés de la V3

La V3 introduit des améliorations significatives à Bedrock Chat :

1. **Contrôle des permissions détaillé** : Contrôlez l'accès à vos bots avec des permissions basées sur les groupes d'utilisateurs
2. **Bot Store** : Partagez et découvrez des bots via une place de marché centralisée
3. **Fonctionnalités administratives** : Gérez les API, marquez les bots comme essentiels et analysez leur utilisation

Ces nouvelles fonctionnalités ont nécessité des modifications du schéma DynamoDB, rendant nécessaire un processus de migration pour les utilisateurs existants.

### Pourquoi cette migration est nécessaire

Le nouveau modèle de permissions et les fonctionnalités du Bot Store ont nécessité une restructuration de la façon dont les données des bots sont stockées et accessibles. Le processus de migration convertit vos bots et conversations existants vers le nouveau schéma tout en préservant toutes vos données.

> [!WARNING]
> Avis d'interruption de service : **Pendant le processus de migration, l'application sera indisponible pour tous les utilisateurs.** Prévoyez d'effectuer cette migration pendant une fenêtre de maintenance lorsque les utilisateurs n'ont pas besoin d'accéder au système. L'application ne redeviendra disponible qu'après que le script de migration se soit terminé avec succès et que toutes les données aient été correctement converties vers le nouveau schéma. Ce processus prend généralement environ 60 minutes, selon la quantité de données et les performances de votre environnement de développement.

> [!IMPORTANT]
> Avant de procéder à la migration : **Le processus de migration ne peut pas garantir un succès à 100% pour tous les bots**, en particulier ceux créés avec des versions plus anciennes ou avec des configurations personnalisées. Veuillez documenter vos configurations de bots importantes (instructions, sources de connaissances, paramètres) avant de commencer le processus de migration au cas où vous devriez les recréer manuellement.

## Processus de Migration

### Note Importante Concernant la Visibilité des Bots dans V3

Dans V3, **tous les bots v2 avec le partage public activé seront consultables dans le Bot Store.** Si vous avez des bots contenant des informations sensibles que vous ne souhaitez pas rendre découvrables, envisagez de les rendre privés avant de migrer vers V3.

### Étape 1 : Identifier le nom de votre environnement

Dans cette procédure, `{YOUR_ENV_PREFIX}` est spécifié pour identifier le nom de vos Stacks CloudFormation. Si vous utilisez la fonctionnalité [Deploying Multiple Environments](../../README.md#deploying-multiple-environments), remplacez-le par le nom de l'environnement à migrer. Sinon, remplacez-le par une chaîne vide.

### Étape 2 : Mettre à jour l'URL du dépôt (Recommandé)

Le dépôt a été renommé de `bedrock-claude-chat` à `bedrock-chat`. Mettez à jour votre dépôt local :

```bash
# Vérifiez votre URL distante actuelle
git remote -v

# Mettez à jour l'URL distante
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Vérifiez le changement
git remote -v
```

### Étape 3 : Assurez-vous d'être sur la dernière version V2

> [!WARNING]
> Vous DEVEZ mettre à jour vers v2.10.0 avant de migrer vers V3. **Ignorer cette étape peut entraîner une perte de données pendant la migration.**

Avant de commencer la migration, assurez-vous d'exécuter la dernière version de V2 (**v2.10.0**). Cela garantit que vous disposez de toutes les corrections de bugs et améliorations nécessaires avant la mise à niveau vers V3 :

```bash
# Récupérez les derniers tags
git fetch --tags

# Basculez sur la dernière version V2
git checkout v2.10.0

# Déployez la dernière version V2
cd cdk
npm ci
npx cdk deploy --all
```

### Étape 4 : Noter le nom de votre table DynamoDB V2

Obtenez le nom de la ConversationTable V2 depuis les sorties CloudFormation :

```bash
# Obtenez le nom de la ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Assurez-vous de sauvegarder ce nom de table dans un endroit sûr, car vous en aurez besoin pour le script de migration plus tard.

### Étape 5 : Sauvegarder votre table DynamoDB

Avant de continuer, créez une sauvegarde de votre ConversationTable DynamoDB en utilisant le nom que vous venez d'enregistrer :

```bash
# Créez une sauvegarde de votre table V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Vérifiez que l'état de la sauvegarde est disponible
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Étape 6 : Supprimer toutes les API publiées

> [!IMPORTANT]
> Avant de déployer V3, vous devez supprimer toutes les API publiées pour éviter les conflits de valeurs de sortie Cloudformation pendant le processus de mise à niveau.

1. Connectez-vous à votre application en tant qu'administrateur
2. Naviguez vers la section Admin et sélectionnez "API Management"
3. Examinez la liste de toutes les API publiées
4. Supprimez chaque API publiée en cliquant sur le bouton de suppression à côté

Vous pouvez trouver plus d'informations sur la publication et la gestion des API dans la documentation [PUBLISH_API.md](../PUBLISH_API_fr-FR.md), [ADMINISTRATOR.md](../ADMINISTRATOR_fr-FR.md) respectivement.

### Étape 7 : Récupérer V3 et déployer

Récupérez le dernier code V3 et déployez :

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Une fois que vous déployez V3, l'application sera indisponible pour tous les utilisateurs jusqu'à ce que le processus de migration soit terminé. Le nouveau schéma est incompatible avec l'ancien format de données, donc les utilisateurs ne pourront pas accéder à leurs bots ou conversations jusqu'à ce que vous complétiez le script de migration dans les prochaines étapes.

### Étape 8 : Noter les noms de vos tables DynamoDB V3

Après avoir déployé V3, vous devez obtenir les noms de la nouvelle ConversationTable et de la BotTable :

```bash
# Obtenez le nom de la ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Obtenez le nom de la BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Assurez-vous de sauvegarder ces noms de tables V3 avec votre nom de table V2 précédemment sauvegardé, car vous aurez besoin de tous pour le script de migration.

### Étape 9 : Exécuter le script de migration

Le script de migration convertira vos données V2 vers le schéma V3. D'abord, modifiez le script de migration `docs/migration/migrate_v2_v3.py` pour définir vos noms de tables et votre région :

```python
# Région où se trouve dynamodb
REGION = "ap-northeast-1" # Remplacez par votre région

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Remplacez par votre valeur enregistrée à l'Étape 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Remplacez par votre valeur enregistrée à l'Étape 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Remplacez par votre valeur enregistrée à l'Étape 8
```

Puis exécutez le script en utilisant Poetry depuis le répertoire backend :

> [!NOTE]
> La version requise de Python a été changée à 3.13.0 ou ultérieure (Peut être modifiée dans le développement futur. Voir pyproject.toml). Si vous avez venv installé avec une version différente de Python, vous devrez le supprimer une fois.

```bash
# Naviguez vers le répertoire backend
cd backend

# Installez les dépendances si vous ne l'avez pas déjà fait
poetry install

# Effectuez d'abord un dry run pour voir ce qui serait migré
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Si tout semble bon, exécutez la migration réelle
poetry run python ../docs/migration/migrate_v2_v3.py

# Vérifiez que la migration a réussi
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Le script de migration générera un fichier de rapport dans votre répertoire actuel avec les détails du processus de migration. Vérifiez ce fichier pour vous assurer que toutes vos données ont été migrées correctement.

#### Gestion des grands volumes de données

Pour les environnements avec beaucoup d'utilisateurs ou de grandes quantités de données, considérez ces approches :

1. **Migrer les utilisateurs individuellement** : Pour les utilisateurs avec de grands volumes de données, migrez-les un par un :

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Considérations de mémoire** : Le processus de migration charge les données en mémoire. Si vous rencontrez des erreurs de mémoire insuffisante (OOM), essayez :

   - De migrer un utilisateur à la fois
   - D'exécuter la migration sur une machine avec plus de mémoire
   - De diviser la migration en plus petits lots d'utilisateurs

3. **Surveiller la migration** : Vérifiez les fichiers de rapport générés pour vous assurer que toutes les données sont migrées correctement, particulièrement pour les grands ensembles de données.

### Étape 10 : Vérifier l'application

Après la migration, ouvrez votre application et vérifiez :

- Tous vos bots sont disponibles
- Les conversations sont préservées
- Les nouveaux contrôles de permission fonctionnent

### Nettoyage (Optionnel)

Après avoir confirmé que la migration a réussi et que toutes vos données sont correctement accessibles dans V3, vous pouvez optionnellement supprimer la table de conversation V2 pour économiser des coûts :

```bash
# Supprimez la table de conversation V2 (UNIQUEMENT après avoir confirmé la réussite de la migration)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Ne supprimez la table V2 qu'après avoir vérifié minutieusement que toutes vos données importantes ont été migrées avec succès vers V3. Nous recommandons de conserver la sauvegarde créée à l'Étape 2 pendant au moins quelques semaines après la migration, même si vous supprimez la table d'origine.

## FAQ V3

### Accès et Permissions des Bots

**Q : Que se passe-t-il si un bot que j'utilise est supprimé ou si mon autorisation d'accès est révoquée ?**
R : L'autorisation est vérifiée au moment de la conversation, donc vous perdrez l'accès immédiatement.

**Q : Que se passe-t-il si un utilisateur est supprimé (par exemple, un employé qui part) ?**
R : Leurs données peuvent être complètement supprimées en effaçant tous les éléments de DynamoDB ayant leur ID utilisateur comme clé de partition (PK).

**Q : Puis-je désactiver le partage pour un bot public essentiel ?**
R : Non, l'administrateur doit d'abord marquer le bot comme non essentiel avant de désactiver le partage.

**Q : Puis-je supprimer un bot public essentiel ?**
R : Non, l'administrateur doit d'abord marquer le bot comme non essentiel avant de le supprimer.

### Sécurité et Implémentation

**Q : La sécurité au niveau des lignes (RLS) est-elle implémentée pour la table des bots ?**
R : Non, compte tenu de la diversité des modèles d'accès. L'autorisation est effectuée lors de l'accès aux bots, et le risque de fuite de métadonnées est considéré comme minimal par rapport à l'historique des conversations.

**Q : Quelles sont les exigences pour publier une API ?**
R : Le bot doit être public.

**Q : Y aura-t-il un écran de gestion pour tous les bots privés ?**
R : Pas dans la version initiale V3. Cependant, les éléments peuvent toujours être supprimés en interrogeant l'ID utilisateur selon les besoins.

**Q : Y aura-t-il une fonctionnalité d'étiquetage des bots pour améliorer l'expérience de recherche ?**
R : Pas dans la version initiale V3, mais l'étiquetage automatique basé sur LLM pourrait être ajouté dans les futures mises à jour.

### Administration

**Q : Que peuvent faire les administrateurs ?**
R : Les administrateurs peuvent :

- Gérer les bots publics (y compris la vérification des bots à coût élevé)
- Gérer les API
- Marquer les bots publics comme essentiels

**Q : Puis-je définir des bots partiellement partagés comme essentiels ?**
R : Non, uniquement pris en charge pour les bots publics.

**Q : Puis-je définir une priorité pour les bots épinglés ?**
R : Pas dans la version initiale.

### Configuration de l'Autorisation

**Q : Comment configurer l'autorisation ?**
R :

1. Ouvrez la console Amazon Cognito et créez des groupes d'utilisateurs dans le pool d'utilisateurs BrChat
2. Ajoutez des utilisateurs à ces groupes selon les besoins
3. Dans BrChat, sélectionnez les groupes d'utilisateurs auxquels vous souhaitez autoriser l'accès lors de la configuration des paramètres de partage du bot

Note : Les changements d'appartenance aux groupes nécessitent une reconnexion pour prendre effet. Les modifications sont reflétées lors du rafraîchissement du jeton, mais pas pendant la période de validité du jeton ID (30 minutes par défaut dans V3, configurable par `tokenValidMinutes` dans `cdk.json` ou `parameter.ts`).

**Q : Le système vérifie-t-il auprès de Cognito à chaque accès à un bot ?**
R : Non, l'autorisation est vérifiée à l'aide du jeton JWT pour éviter les opérations d'E/S inutiles.

### Fonctionnalité de Recherche

**Q : La recherche de bots prend-elle en charge la recherche sémantique ?**
R : Non, seule la correspondance partielle de texte est prise en charge. La recherche sémantique (par exemple, "automobile" → "voiture", "VE", "véhicule") n'est pas disponible en raison des contraintes actuelles d'OpenSearch Serverless (mars 2025).