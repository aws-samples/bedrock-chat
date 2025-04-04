# Chat Bedrock Claude (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_pl-PL.md)

> [!Avertissement]
>
> **V2 publiée. Pour mettre à jour, veuillez examiner attentivement le [guide de migration](./migration/V1_TO_V2_fr-FR.md).** Sans précaution, **LES BOTS DE LA V1 DEVIENDRONT INUTILISABLES.**

Un chatbot multilingue utilisant des modèles LLM fournis par [Amazon Bedrock](https://aws.amazon.com/bedrock/) pour l'IA générative.

### Regardez la présentation et l'installation sur YouTube

[![Présentation](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Conversation de base

![](./imgs/demo.gif)

### Personnalisation du Bot

Ajoutez vos propres instructions et fournissez des connaissances externes via une URL ou des fichiers (alias [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Le bot peut être partagé entre les utilisateurs de l'application. Le bot personnalisé peut également être publié en tant qu'API autonome (Voir les [détails](./PUBLISH_API_fr-FR.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> Pour des raisons de gouvernance, seuls les utilisateurs autorisés peuvent créer des bots personnalisés. Pour autoriser la création de bots personnalisés, l'utilisateur doit être membre du groupe `CreatingBotAllowed`, qui peut être configuré via la console de gestion > Pools d'utilisateurs Amazon Cognito ou l'interface CLI AWS. Notez que l'ID du pool d'utilisateurs peut être consulté en accédant à CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Tableau de bord administrateur

<details>
<summary>Tableau de bord administrateur</summary>

Analysez l'utilisation pour chaque utilisateur / bot sur le tableau de bord administrateur. [détails](./ADMINISTRATOR_fr-FR.md)

![](./imgs/admin_bot_analytics.png)

</details>

### Agent alimenté par LLM

<details>
<summary>Agent alimenté par LLM</summary>

En utilisant la [fonctionnalité d'Agent](./AGENT_fr-FR.md), votre chatbot peut automatiquement gérer des tâches plus complexes. Par exemple, pour répondre à une question d'un utilisateur, l'Agent peut récupérer les informations nécessaires à partir d'outils externes ou décomposer la tâche en plusieurs étapes pour la traiter.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Déploiement ultra-simple

- Dans la région us-east-1, ouvrez [Accès au modèle Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Gérer l'accès au modèle` > Cochez toutes les options de `Anthropic / Claude 3`, toutes les options de `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` et `Cohere / Embed Multilingual`, puis `Enregistrer les modifications`.

<details>
<summary>Capture d'écran</summary>

![](./imgs/model_screenshot.png)

</details>

- Ouvrez [CloudShell](https://console.aws.amazon.com/cloudshell/home) dans la région où vous souhaitez déployer
- Exécutez le déploiement via les commandes suivantes. Si vous souhaitez spécifier la version à déployer ou appliquer des politiques de sécurité, veuillez spécifier les paramètres appropriés à partir des [Paramètres optionnels](#paramètres-optionnels).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- On vous demandera si vous êtes un nouvel utilisateur ou si vous utilisez la v2. Si vous n'êtes pas un utilisateur continuant depuis la v0, veuillez entrer `y`.

### Paramètres optionnels

Vous pouvez spécifier les paramètres suivants lors du déploiement pour améliorer la sécurité et la personnalisation :

- **--disable-self-register** : Désactiver l'auto-inscription (par défaut : activé). Si cet indicateur est défini, vous devrez créer tous les utilisateurs sur Cognito et il n'autorisera pas les utilisateurs à s'inscrire eux-mêmes.
- **--enable-lambda-snapstart** : Activer [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (par défaut : désactivé). Si cet indicateur est défini, améliore les temps de démarrage à froid pour les fonctions Lambda, offrant des temps de réponse plus rapides pour une meilleure expérience utilisateur.
- **--ipv4-ranges** : Liste séparée par des virgules des plages IPv4 autorisées. (par défaut : autoriser toutes les adresses IPv4)
- **--ipv6-ranges** : Liste séparée par des virgules des plages IPv6 autorisées. (par défaut : autoriser toutes les adresses IPv6)
- **--disable-ipv6** : Désactiver les connexions sur IPv6. (par défaut : activé)
- **--allowed-signup-email-domains** : Liste séparée par des virgules des domaines de courrier électronique autorisés pour l'inscription. (par défaut : aucune restriction de domaine)
- **--bedrock-region** : Définir la région où Bedrock est disponible. (par défaut : us-east-1)
- **--repo-url** : Le dépôt personnalisé de Bedrock Claude Chat à déployer, s'il est forké ou si le contrôle source est personnalisé. (par défaut : https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version** : La version de Bedrock Claude Chat à déployer. (par défaut : dernière version en développement)
- **--cdk-json-override** : Vous pouvez remplacer toutes les valeurs de contexte CDK pendant le déploiement à l'aide du bloc JSON de remplacement. Cela vous permet de modifier la configuration sans éditer directement le fichier cdk.json.

Exemple d'utilisation :

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

Le JSON de remplacement doit suivre la même structure que cdk.json. Vous pouvez remplacer toutes les valeurs de contexte, y compris :

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- Et d'autres valeurs de contexte définies dans cdk.json

> [!Note]
> Les valeurs de remplacement seront fusionnées avec la configuration cdk.json existante lors du déploiement dans la build AWS. Les valeurs spécifiées dans le remplacement prévaudront sur les valeurs dans cdk.json.

#### Exemple de commande avec des paramètres :

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Après environ 35 minutes, vous obtiendrez la sortie suivante, à laquelle vous pouvez accéder depuis votre navigateur

```
URL Frontend : https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

L'écran d'inscription s'affichera comme indiqué ci-dessus, où vous pouvez enregistrer votre e-mail et vous connecter.

> [!Important]
> Sans définir le paramètre optionnel, cette méthode de déploiement permet à quiconque connaît l'URL de s'inscrire. Pour une utilisation en production, il est fortement recommandé d'ajouter des restrictions d'adresse IP et de désactiver l'auto-inscription pour atténuer les risques de sécurité (vous pouvez définir allowed-signup-email-domains pour restreindre les utilisateurs afin que seules les adresses e-mail de votre domaine d'entreprise puissent s'inscrire). Utilisez à la fois ipv4-ranges et ipv6-ranges pour les restrictions d'adresse IP, et désactivez l'auto-inscription en utilisant disable-self-register lors de l'exécution de ./bin.

> [!TIP]
> Si l'`URL Frontend` n'apparaît pas ou si Bedrock Claude Chat ne fonctionne pas correctement, il peut s'agir d'un problème avec la dernière version. Dans ce cas, veuillez ajouter `--version "v1.2.6"` aux paramètres et réessayer le déploiement.

## Architecture

C'est une architecture construite sur des services gérés par AWS, éliminant le besoin de gestion d'infrastructure. En utilisant Amazon Bedrock, il n'est pas nécessaire de communiquer avec des API externes à AWS. Cela permet de déployer des applications évolutives, fiables et sécurisées.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) : Base de données NoSQL pour le stockage de l'historique des conversations
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/) : Point de terminaison d'API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/) : Distribution de l'application frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/) : Restriction d'adresses IP
- [Amazon Cognito](https://aws.amazon.com/cognito/) : Authentification des utilisateurs
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) : Service géré pour utiliser des modèles fondamentaux via des API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) : Fournit une interface gérée pour la Génération Augmentée par Récupération ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), offrant des services d'intégration et d'analyse de documents
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/) : Réception d'événements du flux DynamoDB et lancement de Step Functions pour intégrer des connaissances externes
- [AWS Step Functions](https://aws.amazon.com/step-functions/) : Orchestration du pipeline d'ingestion pour intégrer des connaissances externes dans Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/) : Sert de base de données backend pour Bedrock Knowledge Bases, fournissant des capacités de recherche texte intégral et de recherche vectorielle, permettant une récupération précise des informations pertinentes
- [Amazon Athena](https://aws.amazon.com/athena/) : Service de requête pour analyser le compartiment S3

![](./imgs/arch.png)

## Déploiement à l'aide de CDK

Le déploiement super-facile utilise [AWS CodeBuild](https://aws.amazon.com/codebuild/) pour effectuer le déploiement via CDK en interne. Cette section décrit la procédure de déploiement directement avec CDK.

- Veuillez disposer de UNIX, Docker et d'un environnement d'exécution Node.js. Si ce n'est pas le cas, vous pouvez également utiliser [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Important]
> S'il n'y a pas suffisamment d'espace de stockage dans l'environnement local pendant le déploiement, l'amorçage CDK peut générer une erreur. Si vous exécutez l'environnement dans Cloud9, etc., nous vous recommandons d'augmenter la taille du volume de l'instance avant de déployer.

- Clonez ce dépôt

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Installez les packages npm

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Si nécessaire, modifiez les entrées suivantes dans [cdk.json](./cdk/cdk.json) si nécessaire.

  - `bedrockRegion` : Région où Bedrock est disponible. **REMARQUE : Bedrock ne prend pas en charge toutes les régions pour le moment.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges` : Plage d'adresses IP autorisées.
  - `enableLambdaSnapStart` : Par défaut à true. Définissez à false si vous déployez dans une [région qui ne prend pas en charge Lambda SnapStart pour les fonctions Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Avant de déployer le CDK, vous devrez effectuer un Bootstrap une fois pour la région dans laquelle vous déployez.

```
npx cdk bootstrap
```

- Déployez cet exemple de projet

```
npx cdk deploy --require-approval never --all
```

- Vous obtiendrez une sortie similaire à ce qui suit. L'URL de l'application web sera affichée dans `BedrockChatStack.FrontendURL`, alors veuillez y accéder depuis votre navigateur.

```sh
 ✅  BedrockChatStack

✨  Durée de déploiement : 78,57s

Sorties :
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Définition des paramètres

Vous pouvez définir des paramètres pour votre déploiement de deux manières : en utilisant `cdk.json` ou en utilisant le fichier `parameter.ts` avec vérification de type.

#### Utilisation de cdk.json (Méthode traditionnelle)

La méthode traditionnelle pour configurer les paramètres consiste à modifier le fichier `cdk.json`. Cette approche est simple mais manque de vérification de type :

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Utilisation de parameter.ts (Méthode recommandée avec vérification de type)

Pour une meilleure sécurité de type et une meilleure expérience de développement, vous pouvez utiliser le fichier `parameter.ts` pour définir vos paramètres :

```typescript
// Définir des paramètres pour l'environnement par défaut
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Définir des paramètres pour des environnements supplémentaires
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Économie de coûts pour l'environnement de développement
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Disponibilité améliorée pour la production
});
```

> [!Note]
> Les utilisateurs existants peuvent continuer à utiliser `cdk.json` sans aucune modification. L'approche `parameter.ts` est recommandée pour les nouveaux déploiements ou lorsque vous devez gérer plusieurs environnements.

### Déploiement de plusieurs environnements

Vous pouvez déployer plusieurs environnements à partir du même code base en utilisant le fichier `parameter.ts` et l'option `-c envName`.

#### Prérequis

1. Définissez vos environnements dans `parameter.ts` comme indiqué ci-dessus
2. Chaque environnement aura son propre ensemble de ressources avec des préfixes spécifiques à l'environnement

#### Commandes de déploiement

Pour déployer un environnement spécifique :

```bash
# Déployer l'environnement de développement
npx cdk deploy --all -c envName=dev

# Déployer l'environnement de production
npx cdk deploy --all -c envName=prod
```

Si aucun environnement n'est spécifié, l'environnement "default" est utilisé :

```bash
# Déployer l'environnement par défaut
npx cdk deploy --all
```

#### Notes importantes

1. **Nommage des piles** :

   - Les piles principales de chaque environnement seront préfixées avec le nom de l'environnement (par exemple, `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Cependant, les piles de bot personnalisées (`BrChatKbStack*`) et les piles de publication d'API (`ApiPublishmentStack*`) ne reçoivent pas de préfixes d'environnement car elles sont créées dynamiquement à l'exécution

2. **Nommage des ressources** :

   - Seules certaines ressources reçoivent des préfixes d'environnement dans leurs noms (par exemple, table `dev_ddb_export`, `dev-FrontendWebAcl`)
   - La plupart des ressources conservent leurs noms d'origine mais sont isolées en étant dans différentes piles

3. **Identification de l'environnement** :

   - Toutes les ressources sont étiquetées avec une balise `CDKEnvironment` contenant le nom de l'environnement
   - Vous pouvez utiliser cette balise pour identifier à quel environnement une ressource appartient
   - Exemple : `CDKEnvironment: dev` ou `CDKEnvironment: prod`

4. **Remplacement de l'environnement par défaut** : Si vous définissez un environnement "default" dans `parameter.ts`, il remplacera les paramètres de `cdk.json`. Pour continuer à utiliser `cdk.json`, ne définissez pas d'environnement "default" dans `parameter.ts`.

5. **Exigences d'environnement** : Pour créer des environnements autres que "default", vous devez utiliser `parameter.ts`. L'option `-c envName` seule n'est pas suffisante sans définitions d'environnement correspondantes.

6. **Isolation des ressources** : Chaque environnement crée son propre ensemble de ressources, vous permettant d'avoir des environnements de développement, de test et de production dans le même compte AWS sans conflits.

## Autres

### Configurer la génération de texte par défaut

Les utilisateurs peuvent ajuster les [paramètres de génération de texte](https://docs.anthropic.com/claude/reference/complete_post) à partir de l'écran de création de bot personnalisé. Si le bot n'est pas utilisé, les paramètres par défaut définis dans [config.py](./backend/app/config.py) seront utilisés.

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Supprimer les ressources

Si vous utilisez cli et CDK, veuillez exécuter `npx cdk destroy`. Sinon, accédez à [CloudFormation](https://console.aws.amazon.com/cloudformation/home) et supprimez manuellement `BedrockChatStack` et `FrontendWafStack`. Veuillez noter que `FrontendWafStack` se trouve dans la région `us-east-1`.

### Paramètres de langue

Cet asset détecte automatiquement la langue à l'aide de [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Vous pouvez changer de langue depuis le menu de l'application. Vous pouvez également utiliser la chaîne de requête pour définir la langue comme indiqué ci-dessous.

> `https://example.com?lng=ja`

### Désactiver l'inscription automatique

Cet exemple a l'inscription automatique activée par défaut. Pour la désactiver, ouvrez [cdk.json](./cdk/cdk.json) et passez `selfSignUpEnabled` à `false`. Si vous configurez un [fournisseur d'identité externe](#external-identity-provider), la valeur sera ignorée et automatiquement désactivée.

### Restreindre les domaines pour les adresses e-mail d'inscription

Par défaut, cet exemple ne restreint pas les domaines des adresses e-mail d'inscription. Pour n'autoriser les inscriptions que depuis des domaines spécifiques, ouvrez `cdk.json` et spécifiez les domaines sous forme de liste dans `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Fournisseur d'identité externe

Cet exemple prend en charge les fournisseurs d'identité externes. Actuellement, nous prenons en charge [Google](./idp/SET_UP_GOOGLE_fr-FR.md) et [fournisseur OIDC personnalisé](./idp/SET_UP_CUSTOM_OIDC_fr-FR.md).

### Ajouter automatiquement de nouveaux utilisateurs aux groupes

Cet exemple dispose des groupes suivants pour donner des autorisations aux utilisateurs :

- [`Admin`](./ADMINISTRATOR_fr-FR.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_fr-FR.md)

Si vous souhaitez que les nouveaux utilisateurs rejoignent automatiquement des groupes, vous pouvez les spécifier dans [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Par défaut, les nouveaux utilisateurs créés rejoindront le groupe `CreatingBotAllowed`.

### Configurer les réplicas RAG

`enableRagReplicas` est une option dans [cdk.json](./cdk/cdk.json) qui contrôle les paramètres de réplica pour la base de données RAG, spécifiquement les bases de connaissances utilisant Amazon OpenSearch Serverless.

- **Par défaut** : true
- **true** : Améliore la disponibilité en activant des réplicas supplémentaires, adapté aux environnements de production mais augmentant les coûts.
- **false** : Réduit les coûts en utilisant moins de réplicas, adapté au développement et aux tests.

Il s'agit d'un paramètre au niveau du compte/région, affectant l'ensemble de l'application plutôt que des bots individuels.

> [!Note]
> En juin 2024, Amazon OpenSearch Serverless prend en charge 0,5 OCU, réduisant les coûts d'entrée pour les charges de travail à petite échelle. Les déploiements de production peuvent commencer avec 2 OCUs, tandis que les charges de travail de développement/test peuvent utiliser 1 OCU. OpenSearch Serverless met automatiquement à l'échelle en fonction des demandes de charge de travail. Pour plus de détails, consultez [l'annonce](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Inférence inter-régions

[L'inférence inter-régions](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) permet à Amazon Bedrock d'acheminer dynamiquement les demandes d'inférence de modèle entre plusieurs régions AWS, améliorant le débit et la résilience pendant les périodes de demande de pointe. Pour configurer, modifiez `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) améliore les temps de démarrage à froid pour les fonctions Lambda, offrant des temps de réponse plus rapides pour une meilleure expérience utilisateur. D'autre part, pour les fonctions Python, il y a des [frais en fonction de la taille du cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) et [non disponible dans certaines régions](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) actuellement. Pour désactiver SnapStart, modifiez `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Configurer un domaine personnalisé

Vous pouvez configurer un domaine personnalisé pour la distribution CloudFront en définissant les paramètres suivants dans [cdk.json](./cdk/cdk.json) :

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName` : Le nom de domaine personnalisé pour votre application de chat (par exemple, chat.example.com)
- `hostedZoneId` : L'ID de votre zone hébergée Route 53 où les enregistrements DNS seront créés

Lorsque ces paramètres sont fournis, le déploiement va automatiquement :

- Créer un certificat ACM avec validation DNS dans la région us-east-1
- Créer les enregistrements DNS nécessaires dans votre zone Route 53
- Configurer CloudFront pour utiliser votre domaine personnalisé

> [!Note]
> Le domaine doit être géré par Route 53 dans votre compte AWS. L'ID de la zone hébergée peut être trouvé dans la console Route 53.

### Développement local

Voir [DÉVELOPPEMENT LOCAL](./LOCAL_DEVELOPMENT_fr-FR.md).

### Contribution

Merci de considérer contribuer à ce dépôt ! Nous accueillons les corrections de bugs, les traductions de langue (i18n), les améliorations de fonctionnalités, les [outils d'agent](./docs/AGENT.md#how-to-develop-your-own-tools) et autres améliorations.

Pour les améliorations de fonctionnalités et autres améliorations, **avant de créer une Pull Request, nous vous serions reconnaissants de créer un problème de demande de fonctionnalité pour discuter de l'approche et des détails de mise en œuvre. Pour les corrections de bugs et les traductions de langue (i18n), procédez directement à la création d'une Pull Request.**

Veuillez également consulter les directives suivantes avant de contribuer :

- [Développement local](./LOCAL_DEVELOPMENT_fr-FR.md)
- [CONTRIBUTION](./CONTRIBUTING_fr-FR.md)

## Contacts

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

(Note: Since this section contains only names and links, no translation was necessary. All personal names and GitHub profile links remain unchanged.)

## 🏆 Contributeurs Significatifs

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Contributeurs

[![contributeurs de bedrock claude chat](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Licence

Cette bibliothèque est sous licence MIT-0. Consultez [le fichier LICENSE](./LICENSE).