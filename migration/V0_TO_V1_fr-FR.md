# Guide de migration (v0 à v1)

Si vous utilisez déjà Bedrock Chat avec une version précédente (~`0.4.x`), vous devez suivre les étapes ci-dessous pour effectuer la migration.

## Pourquoi dois-je le faire ?

Cette mise à jour majeure comprend d'importantes mises à jour de sécurité.

- Le stockage de la base de données vectorielle (c'est-à-dire pgvector sur Aurora PostgreSQL) est désormais chiffré, ce qui déclenche un remplacement lors du déploiement. Cela signifie que les éléments vectoriels existants seront supprimés.
- Nous avons introduit le groupe d'utilisateurs Cognito `CreatingBotAllowed` pour limiter les utilisateurs qui peuvent créer des bots. Les utilisateurs existants ne font pas partie de ce groupe, vous devez donc attribuer manuellement l'autorisation si vous souhaitez qu'ils aient la capacité de créer des bots. Voir : [Bot Personalization](../../README.md#bot-personalization)

## Prérequis

Lisez le [Guide de Migration de Base de Données](./DATABASE_MIGRATION_fr-FR.md) et déterminez la méthode pour restaurer les éléments.

## Étapes

### Migration du stockage de vecteurs

- Ouvrez votre terminal et accédez au répertoire du projet
- Récupérez la branche que vous souhaitez déployer. Voici comment accéder à la branche souhaitée (dans ce cas, `v1`) et récupérer les derniers changements :

```sh
git fetch
git checkout v1
git pull origin v1
```

- Si vous souhaitez restaurer des éléments avec DMS, N'OUBLIEZ PAS de désactiver la rotation des mots de passe et notez le mot de passe pour accéder à la base de données. Si vous restaurez avec le script de migration ([migrate_v0_v1.py](./migrate_v0_v1.py)), vous n'avez pas besoin de noter le mot de passe.
- Supprimez toutes les [APIs publiées](../PUBLISH_API_fr-FR.md) pour que CloudFormation puisse supprimer le cluster Aurora existant.
- Exécutez [npx cdk deploy](../README.md#deploy-using-cdk) qui déclenche le remplacement du cluster Aurora et SUPPRIME TOUS LES ÉLÉMENTS VECTORIELS.
- Suivez le [Guide de Migration de Base de Données](./DATABASE_MIGRATION_fr-FR.md) pour restaurer les éléments vectoriels.
- Vérifiez que l'utilisateur peut utiliser les bots existants qui ont des connaissances, c'est-à-dire les bots RAG.

### Attacher l'autorisation CreatingBotAllowed

- Après le déploiement, tous les utilisateurs seront dans l'impossibilité de créer de nouveaux bots.
- Si vous souhaitez que des utilisateurs spécifiques puissent créer des bots, ajoutez ces utilisateurs au groupe `CreatingBotAllowed` en utilisant la console de gestion ou la CLI.
- Vérifiez si l'utilisateur peut créer un bot. Notez que les utilisateurs doivent se reconnecter.