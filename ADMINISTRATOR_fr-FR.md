# Fonctionnalités administratives

## Prérequis

L'utilisateur administrateur doit être membre du groupe appelé `Admin`, qui peut être configuré via la console de gestion > Pools d'utilisateurs Amazon Cognito ou l'interface de ligne de commande AWS. Notez que l'ID du pool d'utilisateurs peut être consulté en accédant à CloudFormation > BedrockChatStack > Sorties > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Marquer les bots publics comme Essentiels

Les bots publics peuvent désormais être marqués comme "Essentiels" par les administrateurs. Les bots marqués comme Essentiels seront mis en vedette dans la section "Essentiels" du magasin de bots, les rendant facilement accessibles aux utilisateurs. Cela permet aux administrateurs de mettre en avant des bots importants que tous les utilisateurs doivent utiliser.

### Exemples

- Bot Assistant RH : Aide les employés avec des questions et des tâches liées aux ressources humaines.
- Bot Support IT : Fournit une assistance pour les problèmes techniques internes et la gestion des comptes.
- Bot Guide des Politiques Internes : Répond aux questions fréquemment posées sur les règles de présence, les politiques de sécurité et autres réglementations internes.
- Bot d'Intégration des Nouveaux Employés : Guide les nouveaux employés à travers les procédures et l'utilisation des systèmes lors de leur premier jour.
- Bot d'Information sur les Avantages : Explique les programmes d'avantages sociaux de l'entreprise et les services de bien-être.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Boucle de rétroaction

La sortie d'un LLM peut ne pas toujours répondre aux attentes de l'utilisateur. Parfois, il ne parvient pas à satisfaire ses besoins. Pour intégrer efficacement les LLM dans les opérations commerciales et la vie quotidienne, la mise en place d'une boucle de rétroaction est essentielle. Bedrock Chat est doté d'une fonctionnalité de feedback conçue pour permettre aux utilisateurs d'analyser les raisons de l'insatisfaction. Sur la base des résultats de l'analyse, les utilisateurs peuvent ajuster les invites, les sources de données RAG et les paramètres en conséquence.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Les analystes de données peuvent accéder aux journaux de conversation à l'aide d'[Amazon Athena](https://aws.amazon.com/jp/athena/). S'ils souhaitent analyser les données via [Jupyter Notebook](https://jupyter.org/), [cet exemple de notebook](../examples/notebooks/feedback_analysis_example.ipynb) peut servir de référence.

## Tableau de bord

Fournit actuellement un aperçu de base de l'utilisation du chatbot et des utilisateurs, en se concentrant sur l'agrégation des données pour chaque bot et utilisateur sur des périodes de temps spécifiées et en triant les résultats par frais d'utilisation.

![](./imgs/admin_bot_analytics.png)

## Notes

- Comme indiqué dans l'[architecture](../README.md#architecture), les fonctionnalités d'administration feront référence au compartiment S3 exporté à partir de DynamoDB. Veuillez noter que comme l'exportation est effectuée toutes les heures, les conversations les plus récentes peuvent ne pas être immédiatement reflétées.

- Dans les utilisations publiques de bots, les bots qui n'ont pas été utilisés du tout pendant la période spécifiée ne seront pas listés.

- Dans les utilisations par utilisateur, les utilisateurs qui n'ont pas utilisé le système du tout pendant la période spécifiée ne seront pas listés.

> [!Important]
> Si vous utilisez plusieurs environnements (dev, prod, etc.), le nom de la base de données Athena inclura le préfixe d'environnement. Au lieu de `bedrockchatstack_usage_analysis`, le nom de la base de données sera :
>
> - Pour l'environnement par défaut : `bedrockchatstack_usage_analysis`
> - Pour les environnements nommés : `<préfixe-env>_bedrockchatstack_usage_analysis` (par exemple, `dev_bedrockchatstack_usage_analysis`)
>
> De plus, le nom de la table inclura le préfixe d'environnement :
>
> - Pour l'environnement par défaut : `ddb_export`
> - Pour les environnements nommés : `<préfixe-env>_ddb_export` (par exemple, `dev_ddb_export`)
>
> Assurez-vous d'ajuster vos requêtes en conséquence lors du travail avec plusieurs environnements.

## Télécharger les données de conversation

Vous pouvez interroger les journaux de conversation via Athena, en utilisant SQL. Pour télécharger les journaux, ouvrez l'Éditeur de requêtes Athena depuis la console de gestion et exécutez SQL. Voici quelques exemples de requêtes utiles pour analyser les cas d'utilisation. Les commentaires peuvent être référencés dans l'attribut `MessageMap`.

### Requête par ID de Bot

Modifiez `bot-id` et `datehour`. `bot-id` peut être consulté sur l'écran de gestion des bots, accessible depuis les API de publication de bots, visible dans la barre latérale gauche. Notez la dernière partie de l'URL comme `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> Si vous utilisez un environnement nommé (par exemple, "dev"), remplacez `bedrockchatstack_usage_analysis.ddb_export` par `dev_bedrockchatstack_usage_analysis.dev_ddb_export` dans la requête ci-dessus.

### Requête par ID Utilisateur

Modifiez `user-id` et `datehour`. `user-id` peut être consulté sur l'écran de gestion des bots.

> [!Note]
> Les analyses d'utilisation des utilisateurs sont à venir.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> Si vous utilisez un environnement nommé (par exemple, "dev"), remplacez `bedrockchatstack_usage_analysis.ddb_export` par `dev_bedrockchatstack_usage_analysis.dev_ddb_export` dans la requête ci-dessus.