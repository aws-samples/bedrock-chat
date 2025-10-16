# Fonctionnalités administratives

## Prérequis

L'utilisateur administrateur doit être membre d'un groupe appelé `Admin`, qui peut être configuré via la console de gestion > Amazon Cognito User pools ou l'interface aws cli. Notez que l'ID du groupe d'utilisateurs peut être consulté en accédant à CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Marquer les bots publics comme Essentiels

Les bots publics peuvent désormais être marqués comme "Essentiels" par les administrateurs. Les bots marqués comme Essentiels seront mis en avant dans la section "Essentiels" de la boutique de bots, les rendant facilement accessibles aux utilisateurs. Cela permet aux administrateurs d'épingler les bots importants qu'ils souhaitent voir utilisés par tous les utilisateurs.

### Exemples

- Bot Assistant RH : Aide les employés pour les questions et tâches liées aux ressources humaines.
- Bot Support Informatique : Fournit une assistance pour les problèmes techniques internes et la gestion des comptes.
- Bot Guide des Politiques Internes : Répond aux questions fréquentes sur les règles de présence, les politiques de sécurité et autres règlements internes.
- Bot d'Intégration des Nouveaux Employés : Guide les nouvelles recrues à travers les procédures et l'utilisation des systèmes lors de leur premier jour.
- Bot d'Information sur les Avantages : Explique les programmes d'avantages sociaux et les services de bien-être de l'entreprise.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Boucle de rétroaction

La sortie du LLM peut ne pas toujours répondre aux attentes de l'utilisateur. Parfois, elle ne parvient pas à satisfaire les besoins de l'utilisateur. Pour "intégrer" efficacement les LLM dans les opérations commerciales et la vie quotidienne, la mise en place d'une boucle de rétroaction est essentielle. Bedrock Chat est équipé d'une fonction de rétroaction conçue pour permettre aux utilisateurs d'analyser l'origine de l'insatisfaction. Sur la base des résultats d'analyse, les utilisateurs peuvent ajuster les prompts, les sources de données RAG et les paramètres en conséquence.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Les analystes de données peuvent accéder aux journaux de conversation en utilisant [Amazon Athena](https://aws.amazon.com/jp/athena/). S'ils souhaitent analyser les données avec [Jupyter Notebook](https://jupyter.org/), [cet exemple de notebook](../examples/notebooks/feedback_analysis_example.ipynb) peut servir de référence.

## Tableau de bord

Fournit actuellement un aperçu de base de l'utilisation des chatbots et des utilisateurs, en se concentrant sur l'agrégation des données pour chaque bot et utilisateur sur des périodes spécifiques et en triant les résultats par frais d'utilisation.

![](./imgs/admin_bot_analytics.png)

## Notes

- Comme indiqué dans l'[architecture](../README.md#architecture), les fonctionnalités d'administration feront référence au bucket S3 exporté depuis DynamoDB. Veuillez noter que puisque l'export est effectué une fois par heure, les conversations les plus récentes peuvent ne pas être reflétées immédiatement.

- Dans les utilisations des bots publics, les bots qui n'ont pas été utilisés du tout pendant la période spécifiée ne seront pas listés.

- Dans les utilisations des utilisateurs, les utilisateurs qui n'ont pas du tout utilisé le système pendant la période spécifiée ne seront pas listés.

> [!Important]
> Si vous utilisez plusieurs environnements (dev, prod, etc.), le nom de la base de données Athena inclura le préfixe d'environnement. Au lieu de `bedrockchatstack_usage_analysis`, le nom de la base de données sera :
>
> - Pour l'environnement par défaut : `bedrockchatstack_usage_analysis`
> - Pour les environnements nommés : `<env-prefix>_bedrockchatstack_usage_analysis` (par exemple, `dev_bedrockchatstack_usage_analysis`)
>
> De plus, le nom de la table inclura le préfixe d'environnement :
>
> - Pour l'environnement par défaut : `ddb_export`
> - Pour les environnements nommés : `<env-prefix>_ddb_export` (par exemple, `dev_ddb_export`)
>
> Assurez-vous d'ajuster vos requêtes en conséquence lorsque vous travaillez avec plusieurs environnements.

## Télécharger les données de conversation

Vous pouvez interroger les journaux de conversation via Athena, en utilisant SQL. Pour télécharger les journaux, ouvrez l'éditeur de requêtes Athena depuis la console de gestion et exécutez SQL. Voici quelques exemples de requêtes utiles pour analyser les cas d'utilisation. Les retours peuvent être consultés dans l'attribut `MessageMap`.

### Requête par ID de Bot

Modifiez `bot-id` et `datehour`. Le `bot-id` peut être consulté sur l'écran de gestion des bots, accessible depuis les API Bot Publish, affichées dans la barre latérale gauche. Notez la partie finale de l'URL comme `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

### Requête par ID utilisateur

Modifiez `user-id` et `datehour`. Le `user-id` peut être consulté sur l'écran de gestion des bots.

> [!Note]
> Les analyses d'utilisation par utilisateur seront bientôt disponibles.

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