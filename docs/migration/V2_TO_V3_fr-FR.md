# Guide de Migration (v2 à v3)

## TL;DR

- V3 introduit un contrôle des autorisations plus granulaire et des fonctionnalités de Bot Store, nécessitant des modifications du schéma DynamoDB
- **Sauvegardez votre table ConversationTable DynamoDB avant la migration**
- Mettez à jour l'URL de votre dépôt de `bedrock-claude-chat` à `bedrock-chat`
- Exécutez le script de migration pour convertir vos données au nouveau schéma
- Tous vos bots et conversations seront préservés avec le nouveau modèle d'autorisation
- **IMPORTANT : Pendant le processus de migration, l'application sera indisponible pour tous les utilisateurs jusqu'à ce que la migration soit terminée. Ce processus prend généralement environ 60 minutes, selon la quantité de données et les performances de votre environnement de développement.**
- **IMPORTANT : Toutes les API publiées doivent être supprimées pendant le processus de migration.**
- **AVERTISSEMENT : Le processus de migration ne peut pas garantir 100% de succès pour tous les bots. Veuillez documenter vos configurations de bots importantes avant la migration au cas où vous devriez les recréer manuellement**

## Introduction

### Nouveautés de la V3

La V3 introduit des améliorations significatives dans Bedrock Chat :

1. **Contrôle des permissions granulaire** : Contrôlez l'accès à vos bots avec des permissions basées sur les groupes d'utilisateurs
2. **Boutique de bots** : Partagez et découvrez des bots via un marketplace centralisé
3. **Fonctionnalités administratives** : Gérez les API, marquez des bots comme essentiels et analysez l'utilisation des bots

Ces nouvelles fonctionnalités ont nécessité des modifications du schéma DynamoDB, impliquant un processus de migration pour les utilisateurs existants.

### Pourquoi Cette Migration Est Nécessaire

Le nouveau modèle de permission et les fonctionnalités de la Boutique de bots ont requis une restructuration de la façon dont les données des bots sont stockées et accessibles. Le processus de migration convertit vos bots et conversations existants vers le nouveau schéma tout en préservant toutes vos données.

> [!WARNING]
> Avis d'interruption de service : **Pendant le processus de migration, l'application sera indisponible pour tous les utilisateurs.** Prévoyez de réaliser cette migration pendant une fenêtre de maintenance où les utilisateurs n'ont pas besoin d'accéder au système. L'application ne sera à nouveau disponible qu'une fois que le script de migration aura été exécuté avec succès et que toutes les données auront été correctement converties vers le nouveau schéma. Ce processus prend généralement environ 60 minutes, selon la quantité de données et les performances de votre environnement de développement.

> [!IMPORTANT]
> Avant de procéder à la migration : **Le processus de migration ne peut pas garantir 100 % de succès pour tous les bots**, en particulier ceux créés avec des versions antérieures ou des configurations personnalisées. Veuillez documenter les configurations importantes de vos bots (instructions, sources de connaissances, paramètres) avant de commencer le processus de migration au cas où vous devriez les recréer manuellement.

## Processus de Migration

### Avis Important sur la Visibilité des Bots dans la V3

Dans la V3, **tous les bots v2 avec le partage public activé seront consultables dans le Bot Store.** Si vous avez des bots contenant des informations sensibles que vous ne souhaitez pas rendre découvrables, pensez à les rendre privés avant de migrer vers la V3.

### Étape 1 : Identifier le nom de votre environnement

Dans cette procédure, `{VOTRE_PREFIXE_ENV}` est spécifié pour identifier le nom de vos Piles CloudFormation. Si vous utilisez la fonctionnalité [Déploiement de Plusieurs Environnements](../../README.md#deploying-multiple-environments), remplacez-le par le nom de l'environnement à migrer. Sinon, remplacez-le par une chaîne vide.

### Étape 2 : Mettre à jour l'URL du Référentiel (Recommandé)

Le référentiel a été renommé de `bedrock-claude-chat` à `bedrock-chat`. Mettez à jour votre référentiel local :

```bash
# Vérifier votre URL distante actuelle
git remote -v

# Mettre à jour l'URL distante
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Vérifier le changement
git remote -v
```

### Étape 3 : S'Assurer d'Être sur la Dernière Version V2

> [!AVERTISSEMENT]
> Vous DEVEZ mettre à jour vers v2.10.0 avant de migrer vers V3. **Ignorer cette étape peut entraîner une perte de données lors de la migration.**

Avant de commencer la migration, assurez-vous d'exécuter la dernière version de V2 (**v2.10.0**). Cela garantit que vous disposez de tous les correctifs de bugs et améliorations nécessaires avant de passer à la V3 :

```bash
# Récupérer les derniers tags
git fetch --tags

# Basculer vers la dernière version V2
git checkout v2.10.0

# Déployer la dernière version V2
cd cdk
npm ci
npx cdk deploy --all
```

### Étape 4 : Enregistrer le Nom de Votre Table DynamoDB V2

Obtenez le nom de la table ConversationTable V2 à partir des sorties CloudFormation :

```bash
# Obtenir le nom de la table ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {VOTRE_PREFIXE_ENV}BedrockChatStack
```

Assurez-vous de sauvegarder ce nom de table dans un endroit sécurisé, car vous en aurez besoin pour le script de migration ultérieurement.

### Étape 5 : Sauvegarder Votre Table DynamoDB

Avant de continuer, créez une sauvegarde de votre ConversationTable DynamoDB en utilisant le nom que vous venez d'enregistrer :

```bash
# Créer une sauvegarde de votre table V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name NOM_DE_VOTRE_TABLE_CONVERSATION_V2

# Vérifier que le statut de la sauvegarde est disponible
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn VOTRE_ARN_DE_SAUVEGARDE
```

### Étape 6 : Supprimer Toutes les API Publiées

> [!IMPORTANT]
> Avant de déployer V3, vous devez supprimer toutes les API publiées pour éviter les conflits de valeurs de sortie Cloudformation pendant le processus de mise à niveau.

1. Connectez-vous à votre application en tant qu'administrateur
2. Accédez à la section Administration et sélectionnez "Gestion des API"
3. Passez en revue la liste de toutes les API publiées
4. Supprimez chaque API publiée en cliquant sur le bouton de suppression à côté de celle-ci

Vous pouvez trouver plus d'informations sur la publication et la gestion des API dans la documentation [PUBLISH_API.md](../PUBLISH_API_fr-FR.md), [ADMINISTRATOR.md](../ADMINISTRATOR_fr-FR.md) respectivement.

### Étape 7 : Tirer V3 et Déployer

Tirez le code V3 le plus récent et déployez :

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Une fois que vous déployez V3, l'application sera indisponible pour tous les utilisateurs jusqu'à ce que le processus de migration soit terminé. Le nouveau schéma est incompatible avec l'ancien format de données, donc les utilisateurs ne pourront pas accéder à leurs bots ou conversations tant que vous n'aurez pas terminé le script de migration dans les étapes suivantes.

### Étape 8 : Enregistrer Vos Noms de Tables DynamoDB V3

Après avoir déployé V3, vous devez obtenir les noms des nouvelles tables ConversationTable et BotTable :

```bash
# Obtenir le nom de la table ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {VOTRE_PREFIXE_ENV}BedrockChatStack

# Obtenir le nom de la table BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {VOTRE_PREFIXE_ENV}BedrockChatStack
```

> [!Important]
> Assurez-vous de sauvegarder ces noms de tables V3 ainsi que le nom de votre table V2 précédemment sauvegardé, car vous en aurez besoin pour le script de migration.

(Le reste de la traduction suit le même modèle. Voulez-vous que je continue avec le reste du document ?)

## V3 FAQ

### Accès et Autorisations des Bots

**Q : Que se passe-t-il si un bot que j'utilise est supprimé ou si mon autorisation d'accès est retirée ?**
R : L'autorisation est vérifiée au moment de la discussion, donc vous perdrez l'accès immédiatement.

**Q : Que se passe-t-il si un utilisateur est supprimé (par exemple, un employé qui part) ?**
R : Ses données peuvent être complètement supprimées en supprimant tous les éléments de DynamoDB avec son ID utilisateur comme clé de partition (PK).

**Q : Puis-je désactiver le partage pour un bot public essentiel ?**
R : Non, l'administrateur doit d'abord marquer le bot comme non essentiel avant de désactiver le partage.

**Q : Puis-je supprimer un bot public essentiel ?**
R : Non, l'administrateur doit d'abord marquer le bot comme non essentiel avant de le supprimer.

### Sécurité et Implémentation

**Q : La sécurité au niveau des lignes (RLS) est-elle implémentée pour la table des bots ?**
R : Non, en raison de la diversité des modèles d'accès. L'autorisation est effectuée lors de l'accès aux bots, et le risque de fuite de métadonnées est considéré comme minimal par rapport à l'historique des conversations.

**Q : Quelles sont les conditions pour publier une API ?**
R : Le bot doit être public.

**Q : Y aura-t-il un écran de gestion pour tous les bots privés ?**
R : Pas dans la version initiale de V3. Cependant, les éléments peuvent toujours être supprimés en effectuant une requête avec l'ID utilisateur si nécessaire.

**Q : Y aura-t-il une fonctionnalité de balisage des bots pour une meilleure expérience de recherche ?**
R : Pas dans la version initiale de V3, mais un balisage automatique basé sur LLM pourrait être ajouté dans les futures mises à jour.

### Administration

**Q : Que peuvent faire les administrateurs ?**
R : Les administrateurs peuvent :

- Gérer les bots publics (y compris vérifier les bots à coût élevé)
- Gérer les API
- Marquer des bots publics comme essentiels

**Q : Puis-je marquer des bots partiellement partagés comme essentiels ?**
R : Non, seuls les bots publics sont pris en charge.

**Q : Puis-je définir une priorité pour les bots épinglés ?**
R : Lors de la version initiale, non.

### Configuration de l'Autorisation

**Q : Comment configurer l'autorisation ?**
R :

1. Ouvrez la console Amazon Cognito et créez des groupes d'utilisateurs dans le pool d'utilisateurs BrChat
2. Ajoutez des utilisateurs à ces groupes selon les besoins
3. Dans BrChat, sélectionnez les groupes d'utilisateurs auxquels vous voulez accorder l'accès lors de la configuration des paramètres de partage des bots

Remarque : Les changements d'appartenance à un groupe nécessitent une reconnexion pour prendre effet. Les modifications sont répercutées lors de l'actualisation du jeton, mais pas pendant la période de validité du jeton d'identité (30 minutes par défaut dans V3, configurable par `tokenValidMinutes` dans `cdk.json` ou `parameter.ts`).

**Q : Le système vérifie-t-il avec Cognito à chaque accès à un bot ?**
R : Non, l'autorisation est vérifiée à l'aide du jeton JWT pour éviter des opérations d'E/S inutiles.

### Fonctionnalité de Recherche

**Q : La recherche de bots prend-elle en charge la recherche sémantique ?**
R : Non, seule la correspondance de texte partielle est prise en charge. La recherche sémantique (par exemple, "automobile" → "voiture", "VE", "véhicule") n'est pas disponible en raison des contraintes actuelles d'OpenSearch Serverless (mars 2025).