# Publication d'API

## Vue d'ensemble

Cet exemple inclut une fonctionnalité de publication d'APIs. Bien qu'une interface de chat puisse être pratique pour une validation préliminaire, l'implémentation réelle dépend du cas d'utilisation spécifique et de l'expérience utilisateur (UX) souhaitée pour l'utilisateur final. Dans certains scénarios, une interface de chat peut être le choix privilégié, tandis que dans d'autres, une API autonome pourrait être plus appropriée. Après la validation initiale, cet exemple offre la possibilité de publier des bots personnalisés selon les besoins du projet. En configurant les paramètres de quotas, de limitation de débit, d'origines, etc., un point de terminaison peut être publié avec une clé API, offrant ainsi une flexibilité pour diverses options d'intégration.

## Sécurité

L'utilisation unique d'une clé API n'est pas recommandée comme décrit dans : [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Par conséquent, cet exemple implémente une restriction simple d'adresses IP via AWS WAF. La règle WAF est appliquée de manière commune à l'ensemble de l'application pour des raisons de coût, en partant du principe que les sources que l'on souhaite restreindre sont probablement les mêmes pour toutes les API émises. **Veuillez respecter la politique de sécurité de votre organisation pour l'implémentation réelle.** Consultez également la section [Architecture](#architecture).

## Comment publier une API de bot personnalisée

### Prérequis

Pour des raisons de gouvernance, seuls certains utilisateurs peuvent publier des bots. Avant la publication, l'utilisateur doit être membre du groupe `PublishAllowed`, qui peut être configuré via la console de gestion > Amazon Cognito User pools ou via l'aws cli. Notez que l'ID du pool d'utilisateurs peut être consulté en accédant à CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Paramètres de publication de l'API

Après s'être connecté en tant qu'utilisateur `PublishedAllowed` et avoir créé un bot, sélectionnez `API PublishSettings`. Notez que seul un bot partagé peut être publié.
![](./imgs/bot_api_publish_screenshot.png)

Sur l'écran suivant, nous pouvons configurer plusieurs paramètres concernant la limitation du débit. Pour plus de détails, consultez également : [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Après le déploiement, l'écran suivant apparaîtra où vous pourrez obtenir l'URL du point de terminaison et une clé API. Nous pouvons également ajouter et supprimer des clés API.

![](./imgs/bot_api_publish_screenshot3.png)

## Architecture

L'API est publiée selon le diagramme suivant :

![](./imgs/published_arch.png)

Le WAF est utilisé pour la restriction des adresses IP. L'adresse peut être configurée en définissant les paramètres `publishedApiAllowedIpV4AddressRanges` et `publishedApiAllowedIpV6AddressRanges` dans `cdk.json`.

Lorsqu'un utilisateur clique pour publier le bot, [AWS CodeBuild](https://aws.amazon.com/codebuild/) lance une tâche de déploiement CDK pour provisionner la pile API (Voir aussi : [Définition CDK](../cdk/lib/api-publishment-stack.ts)) qui contient API Gateway, Lambda et SQS. SQS est utilisé pour découpler la requête utilisateur et l'opération LLM car la génération de la sortie peut dépasser 30 secondes, qui est la limite du quota API Gateway. Pour récupérer la sortie, il faut accéder à l'API de manière asynchrone. Pour plus de détails, voir la [Spécification de l'API](#api-specification).

Le client doit définir `x-api-key` dans l'en-tête de la requête.

## Spécification de l'API

Voir [ici](https://aws-samples.github.io/bedrock-chat).