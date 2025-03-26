# Guide de Migration (v0 à v1)

Si vous utilisez déjà Bedrock Claude Chat avec une version précédente (~`0.4.x`), vous devez suivre les étapes ci-dessous pour migrer.

## Pourquoi dois-je le faire ?

Cette mise à jour majeure comprend des mises à jour de sécurité importantes.

- Le stockage de la base de données vectorielle (c'est-à-dire pgvector sur Aurora PostgreSQL) est maintenant chiffré, ce qui provoque un remplacement lors du déploiement. Cela signifie que les éléments vectoriels existants seront supprimés.
- Nous avons introduit le groupe d'utilisateurs Cognito `CreatingBotAllowed` pour limiter les utilisateurs qui peuvent créer des bots. Les utilisateurs existants actuels ne font pas partie de ce groupe, vous devez donc attacher manuellement l'autorisation si vous voulez leur donner la capacité de créer des bots. Voir : [Personnalisation du bot](../../README.md#bot-personalization)

## Prérequis

Lisez le [Guide de Migration de Base de Données](./DATABASE_MIGRATION_fr-FR.md) et déterminez la méthode de restauration des éléments.

## Étapes

### Migration du magasin de vecteurs

- Ouvrez votre terminal et naviguez jusqu'au répertoire du projet
- Tirez la branche que vous souhaitez déployer. Passez à la branche désirée (dans ce cas, `v1`) et tirez les dernières modifications :

```sh
git fetch
git checkout v1
git pull origin v1
```

- Si vous souhaitez restaurer des éléments avec DMS, N'OUBLIEZ PAS de désactiver la rotation du mot de passe et de noter le mot de passe pour accéder à la base de données. Si la restauration se fait avec le script de migration([migrate.py](./migrate.py)), vous n'avez pas besoin de noter le mot de passe.
- Supprimez toutes les [API publiées](../PUBLISH_API_fr-FR.md) afin que CloudFormation puisse supprimer le cluster Aurora existant.
- Exécutez [npx cdk deploy](../README.md#deploy-using-cdk) qui déclenche le remplacement du cluster Aurora et SUPPRIME TOUS LES ÉLÉMENTS DE VECTEUR.
- Suivez le [Guide de migration de base de données](./DATABASE_MIGRATION_fr-FR.md) pour restaurer les éléments de vecteur.
- Vérifiez que l'utilisateur peut utiliser les bots existants qui ont des connaissances, c'est-à-dire les bots RAG.

### Attacher l'autorisation CreatingBotAllowed

- Après le déploiement, tous les utilisateurs ne pourront pas créer de nouveaux bots.
- Si vous voulez que des utilisateurs spécifiques puissent créer des bots, ajoutez ces utilisateurs au groupe `CreatingBotAllowed` en utilisant la console de gestion ou l'interface en ligne de commande.
- Vérifiez si l'utilisateur peut créer un bot. Notez que les utilisateurs doivent se reconnecter.