# Guide de Migration (v0 à v1)

Si vous utilisez déjà Bedrock Claude Chat avec une version précédente (~`0.4.x`), vous devez suivre les étapes ci-dessous pour effectuer la migration.

## Pourquoi dois-je le faire ?

Cette mise à jour majeure comprend des mises à jour de sécurité importantes.

- Le stockage de la base de données vectorielle (c'est-à-dire pgvector sur Aurora PostgreSQL) est maintenant chiffré, ce qui déclenchera un remplacement lors du déploiement. Cela signifie que les éléments vectoriels existants seront supprimés.
- Nous avons introduit le groupe d'utilisateurs Cognito `CreatingBotAllowed` pour limiter les utilisateurs pouvant créer des bots. Les utilisateurs existants ne font pas partie de ce groupe, vous devrez donc attacher manuellement l'autorisation si vous souhaitez leur donner la capacité de créer des bots. Voir : [Personnalisation du bot](../../README.md#bot-personalization)

## Prérequis

Lisez le [Guide de Migration de Base de Données](./DATABASE_MIGRATION_fr-FR.md) et déterminez la méthode pour restaurer les éléments.

## Étapes

### Migration du magasin de vecteurs

- Ouvrez votre terminal et naviguez jusqu'au répertoire du projet
- Tirez la branche que vous souhaitez déployer. Passez à la branche souhaitée (dans ce cas, `v1`) et tirez les dernières modifications :

```sh
git fetch
git checkout v1
git pull origin v1
```

- Si vous souhaitez restaurer des éléments avec DMS, N'OUBLIEZ PAS de désactiver la rotation des mots de passe et de noter le mot de passe pour accéder à la base de données. Si la restauration se fait avec le script de migration ([migrate.py](./migrate.py)), vous n'avez pas besoin de noter le mot de passe.
- Supprimez toutes les [API publiées](../PUBLISH_API_fr-FR.md) afin que CloudFormation puisse supprimer le cluster Aurora existant.
- Exécutez [npx cdk deploy](../README.md#deploy-using-cdk) qui déclenche le remplacement du cluster Aurora et SUPPRIME TOUS LES ÉLÉMENTS VECTORIELS.
- Suivez le [Guide de migration de base de données](./DATABASE_MIGRATION_fr-FR.md) pour restaurer les éléments vectoriels.
- Vérifiez que l'utilisateur peut utiliser les bots existants avec des connaissances, c'est-à-dire les bots RAG.

### Attacher l'autorisation CreatingBotAllowed

- Après le déploiement, tous les utilisateurs seront dans l'incapacité de créer de nouveaux bots.
- Si vous voulez que des utilisateurs spécifiques puissent créer des bots, ajoutez ces utilisateurs au groupe `CreatingBotAllowed` en utilisant la console de gestion ou l'interface en ligne de commande.
- Vérifiez si l'utilisateur peut créer un bot. Notez que les utilisateurs doivent se reconnecter.