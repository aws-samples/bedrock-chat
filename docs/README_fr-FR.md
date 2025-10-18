<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)


Une plateforme d'IA générative multilingue alimentée par [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Prend en charge le chat, les bots personnalisés avec connaissances (RAG), le partage de bots via une boutique de bots, et l'automatisation des tâches à l'aide d'agents.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 publiée. Pour mettre à jour, veuillez examiner attentivement le [guide de migration](./migration/V2_TO_V3_fr-FR.md).** Sans précaution, **LES BOTS DE LA V2 DEVIENDRONT INUTILISABLES.**

### Personnalisation des Bots / Boutique de bots

Ajoutez vos propres instructions et connaissances (aussi appelé [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/). Le bot peut être partagé entre les utilisateurs de l'application via la boutique de bots. Le bot personnalisé peut également être publié comme API autonome (Voir les [détails](./PUBLISH_API_fr-FR.md)).

<details>
<summary>Captures d'écran</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Vous pouvez également importer des [KnowledgeBase Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/) existantes.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> Pour des raisons de gouvernance, seuls les utilisateurs autorisés peuvent créer des bots personnalisés. Pour autoriser la création de bots personnalisés, l'utilisateur doit être membre du groupe appelé `CreatingBotAllowed`, qui peut être configuré via la console de gestion > Amazon Cognito User pools ou aws cli. Notez que l'ID du pool d'utilisateurs peut être référencé en accédant à CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Fonctionnalités administratives

Gestion des API, Marquer les bots comme essentiels, Analyser l'utilisation des bots. [détails](./ADMINISTRATOR_fr-FR.md)

<details>
<summary>Captures d'écran</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agent

En utilisant la [fonctionnalité Agent](./AGENT_fr-FR.md), votre chatbot peut automatiquement gérer des tâches plus complexes. Par exemple, pour répondre à la question d'un utilisateur, l'Agent peut récupérer les informations nécessaires à partir d'outils externes ou décomposer la tâche en plusieurs étapes pour le traitement.

<details>
<summary>Captures d'écran</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Déploiement ultra-simple

- Dans la région us-east-1, ouvrez [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > Cochez tous les modèles que vous souhaitez utiliser puis `Save changes`.

<details>
<summary>Capture d'écran</summary>

![](./imgs/model_screenshot.png)

</details>

### Régions prises en charge

Veuillez vous assurer de déployer Bedrock Chat dans une région [où OpenSearch Serverless et les API d'ingestion sont disponibles](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html), si vous souhaitez utiliser des bots et créer des bases de connaissances (OpenSearch Serverless est le choix par défaut). En août 2025, les régions suivantes sont prises en charge : us-east-1, us-east-2, us-west-1, us-west-2, ap-south-1, ap-northeast-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-south-2, eu-north-1, sa-east-1

Pour le paramètre **bedrock-region**, vous devez choisir une région [où Bedrock est disponible](https://docs.aws.amazon.com/general/latest/gr/bedrock.html).

- Ouvrez [CloudShell](https://console.aws.amazon.com/cloudshell/home) dans la région où vous souhaitez déployer
- Exécutez le déploiement via les commandes suivantes. Si vous souhaitez spécifier la version à déployer ou devez appliquer des politiques de sécurité, veuillez spécifier les paramètres appropriés dans [Paramètres optionnels](#optional-parameters).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- On vous demandera si vous êtes un nouvel utilisateur ou si vous utilisez la v3. Si vous n'êtes pas un utilisateur continu depuis la v0, veuillez saisir `y`.

### Paramètres optionnels

Vous pouvez spécifier les paramètres suivants lors du déploiement pour améliorer la sécurité et la personnalisation :

- **--disable-self-register** : Désactive l'auto-inscription (activée par défaut). Si ce drapeau est défini, vous devrez créer tous les utilisateurs sur cognito et l'auto-inscription ne sera pas autorisée.
- **--enable-lambda-snapstart** : Active [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (désactivé par défaut). Si ce drapeau est défini, améliore les temps de démarrage à froid des fonctions Lambda, offrant des temps de réponse plus rapides pour une meilleure expérience utilisateur.
- **--ipv4-ranges** : Liste séparée par des virgules des plages IPv4 autorisées. (par défaut : autorise toutes les adresses ipv4)
- **--ipv6-ranges** : Liste séparée par des virgules des plages IPv6 autorisées. (par défaut : autorise toutes les adresses ipv6)
- **--disable-ipv6** : Désactive les connexions via IPv6. (activé par défaut)
- **--allowed-signup-email-domains** : Liste séparée par des virgules des domaines d'e-mail autorisés pour l'inscription. (par défaut : aucune restriction de domaine)
- **--bedrock-region** : Définit la région où bedrock est disponible. (par défaut : us-east-1)
- **--repo-url** : Le dépôt personnalisé de Bedrock Chat à déployer, si forké ou contrôle de source personnalisé. (par défaut : https://github.com/aws-samples/bedrock-chat.git)
- **--version** : La version de Bedrock Chat à déployer. (par défaut : dernière version en développement)
- **--cdk-json-override** : Vous pouvez remplacer n'importe quelle valeur de contexte CDK pendant le déploiement en utilisant le bloc JSON de remplacement. Cela vous permet de modifier la configuration sans éditer directement le fichier cdk.json.

Exemple d'utilisation :

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedCountries": ["US", "CA"],
    "allowedSignUpEmailDomains": ["example.com"],
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ]
  }
}'
```

Le JSON de remplacement doit suivre la même structure que cdk.json. Vous pouvez remplacer n'importe quelle valeur de contexte, notamment :

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels` : accepte une liste d'ID de modèles à activer. La valeur par défaut est une liste vide, qui active tous les modèles.
- `logoPath` : chemin relatif vers l'asset logo dans le répertoire frontend `public/` qui apparaît en haut du tiroir de navigation.
- Et d'autres valeurs de contexte définies dans cdk.json

> [!Note]
> Les valeurs de remplacement seront fusionnées avec la configuration cdk.json existante pendant le déploiement dans l'AWS code build. Les valeurs spécifiées dans le remplacement auront la priorité sur les valeurs dans cdk.json.

#### Exemple de commande avec paramètres :

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Après environ 35 minutes, vous obtiendrez la sortie suivante, à laquelle vous pourrez accéder depuis votre navigateur

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

L'écran d'inscription apparaîtra comme montré ci-dessus, où vous pourrez enregistrer votre e-mail et vous connecter.

> [!Important]
> Sans définir le paramètre optionnel, cette méthode de déploiement permet à quiconque connaissant l'URL de s'inscrire. Pour une utilisation en production, il est fortement recommandé d'ajouter des restrictions d'adresses IP et de désactiver l'auto-inscription pour atténuer les risques de sécurité (vous pouvez définir allowed-signup-email-domains pour restreindre les utilisateurs afin que seules les adresses e-mail de votre domaine d'entreprise puissent s'inscrire). Utilisez à la fois ipv4-ranges et ipv6-ranges pour les restrictions d'adresses IP, et désactivez l'auto-inscription en utilisant disable-self-register lors de l'exécution de ./bin.

> [!TIP]
> Si l'`URL Frontend` n'apparaît pas ou si Bedrock Chat ne fonctionne pas correctement, il peut s'agir d'un problème avec la dernière version. Dans ce cas, veuillez ajouter `--version "v3.0.0"` aux paramètres et réessayer le déploiement.

## Architecture

C'est une architecture construite sur des services managés AWS, éliminant le besoin de gestion d'infrastructure. En utilisant Amazon Bedrock, il n'est pas nécessaire de communiquer avec des API externes à AWS. Cela permet de déployer des applications évolutives, fiables et sécurisées.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) : Base de données NoSQL pour le stockage de l'historique des conversations
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/) : Point de terminaison API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/) : Distribution de l'application frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/) : Restriction des adresses IP
- [Amazon Cognito](https://aws.amazon.com/cognito/) : Authentification des utilisateurs
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) : Service managé pour utiliser des modèles fondamentaux via des API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) : Fournit une interface managée pour la génération augmentée par récupération ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), offrant des services pour l'embedding et l'analyse de documents
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/) : Réception d'événements depuis le flux DynamoDB et lancement de Step Functions pour intégrer des connaissances externes
- [AWS Step Functions](https://aws.amazon.com/step-functions/) : Orchestration du pipeline d'ingestion pour intégrer des connaissances externes dans Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/) : Sert de base de données backend pour Bedrock Knowledge Bases, fournissant des capacités de recherche plein texte et de recherche vectorielle, permettant une récupération précise des informations pertinentes
- [Amazon Athena](https://aws.amazon.com/athena/) : Service de requêtes pour analyser le bucket S3

![](./imgs/arch.png)

## Déploiement avec CDK

Le déploiement Super-easy utilise [AWS CodeBuild](https://aws.amazon.com/codebuild/) pour effectuer le déploiement via CDK en interne. Cette section décrit la procédure de déploiement direct avec CDK.

- Veuillez disposer d'un environnement UNIX, Docker et Node.js.

> [!Important]
> Si l'espace de stockage est insuffisant dans l'environnement local pendant le déploiement, l'amorçage CDK peut générer une erreur. Nous recommandons d'augmenter la taille du volume de l'instance avant le déploiement.

- Clonez ce dépôt

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Installez les packages npm

```
cd bedrock-chat
cd cdk
npm ci
```

- Si nécessaire, modifiez les entrées suivantes dans [cdk.json](./cdk/cdk.json).

  - `bedrockRegion`: Région où Bedrock est disponible. **NOTE : Bedrock ne prend PAS en charge toutes les régions pour le moment.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Plages d'adresses IP autorisées.
  - `enableLambdaSnapStart`: Par défaut à true. Mettre à false si le déploiement se fait dans une [région qui ne prend pas en charge Lambda SnapStart pour les fonctions Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).
  - `globalAvailableModels`: Par défaut tous. Si défini (liste d'ID de modèles), permet de contrôler globalement quels modèles apparaissent dans les menus déroulants des chats pour tous les utilisateurs et lors de la création de bots dans l'application Bedrock Chat.
  - `logoPath`: Chemin relatif sous `frontend/public` qui pointe vers l'image affichée en haut du tiroir de l'application.
Les ID de modèles suivants sont pris en charge (assurez-vous qu'ils sont également activés dans la console Bedrock sous Model access dans votre région de déploiement) :
- **Modèles Claude :** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Modèles Amazon Nova :** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Modèles Mistral :** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **Modèles DeepSeek :** `deepseek-r1`
- **Modèles Meta Llama :** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

La liste complète se trouve dans [index.ts](./frontend/src/constants/index.ts).

- Avant de déployer le CDK, vous devrez effectuer une fois le Bootstrap pour la région dans laquelle vous déployez.

```
npx cdk bootstrap
```

- Déployez ce projet exemple

```
npx cdk deploy --require-approval never --all
```

- Vous obtiendrez une sortie similaire à ce qui suit. L'URL de l'application web sera affichée dans `BedrockChatStack.FrontendURL`, veuillez y accéder depuis votre navigateur.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Définition des paramètres

Vous pouvez définir les paramètres de votre déploiement de deux manières : en utilisant `cdk.json` ou en utilisant le fichier `parameter.ts` avec typage sûr.

#### Utilisation de cdk.json (Méthode traditionnelle)

La façon traditionnelle de configurer les paramètres consiste à éditer le fichier `cdk.json`. Cette approche est simple mais ne dispose pas de vérification de type :

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true,
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet", 
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
  }
}
```

#### Utilisation de parameter.ts (Méthode recommandée avec typage sûr)

Pour une meilleure sécurité des types et une meilleure expérience développeur, vous pouvez utiliser le fichier `parameter.ts` pour définir vos paramètres :

```typescript
// Définir les paramètres pour l'environnement par défaut
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// Définir les paramètres pour les environnements supplémentaires
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Économie de coûts pour l'environnement dev
  enableBotStoreReplicas: false, // Économie de coûts pour l'environnement dev
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Disponibilité améliorée pour la production
  enableBotStoreReplicas: true, // Disponibilité améliorée pour la production
});
```

> [!Note]
> Les utilisateurs existants peuvent continuer à utiliser `cdk.json` sans changement. L'approche `parameter.ts` est recommandée pour les nouveaux déploiements ou lorsque vous devez gérer plusieurs environnements.

### Déploiement de plusieurs environnements

Vous pouvez déployer plusieurs environnements à partir de la même base de code en utilisant le fichier `parameter.ts` et l'option `-c envName`.

#### Prérequis

1. Définissez vos environnements dans `parameter.ts` comme montré ci-dessus
2. Chaque environnement aura son propre ensemble de ressources avec des préfixes spécifiques à l'environnement

#### Commandes de déploiement

Pour déployer un environnement spécifique :

```bash
# Déployer l'environnement dev
npx cdk deploy --all -c envName=dev

# Déployer l'environnement prod
npx cdk deploy --all -c envName=prod
```

Si aucun environnement n'est spécifié, l'environnement "default" est utilisé :

```bash
# Déployer l'environnement par défaut
npx cdk deploy --all
```

#### Notes importantes

1. **Nommage des stacks** :

   - Les stacks principales pour chaque environnement seront préfixées avec le nom de l'environnement (par exemple, `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Cependant, les stacks de bots personnalisés (`BrChatKbStack*`) et les stacks de publication d'API (`ApiPublishmentStack*`) ne reçoivent pas de préfixes d'environnement car ils sont créés dynamiquement lors de l'exécution

2. **Nommage des ressources** :

   - Seules certaines ressources reçoivent des préfixes d'environnement dans leurs noms (par exemple, table `dev_ddb_export`, `dev-FrontendWebAcl`)
   - La plupart des ressources conservent leurs noms d'origine mais sont isolées en étant dans différentes stacks

3. **Identification de l'environnement** :

   - Toutes les ressources sont étiquetées avec une balise `CDKEnvironment` contenant le nom de l'environnement
   - Vous pouvez utiliser cette balise pour identifier à quel environnement appartient une ressource
   - Exemple : `CDKEnvironment: dev` ou `CDKEnvironment: prod`

4. **Remplacement de l'environnement par défaut** : Si vous définissez un environnement "default" dans `parameter.ts`, il remplacera les paramètres dans `cdk.json`. Pour continuer à utiliser `cdk.json`, ne définissez pas d'environnement "default" dans `parameter.ts`.

5. **Exigences d'environnement** : Pour créer des environnements autres que "default", vous devez utiliser `parameter.ts`. L'option `-c envName` seule n'est pas suffisante sans définitions d'environnement correspondantes.

6. **Isolation des ressources** : Chaque environnement crée son propre ensemble de ressources, vous permettant d'avoir des environnements de développement, de test et de production dans le même compte AWS sans conflits.

## Autres

Vous pouvez définir les paramètres de votre déploiement de deux manières : en utilisant `cdk.json` ou en utilisant le fichier `parameter.ts` avec typage sécurisé.

#### Utilisation de cdk.json (Méthode traditionnelle)

La façon traditionnelle de configurer les paramètres consiste à modifier le fichier `cdk.json`. Cette approche est simple mais ne dispose pas de vérification des types :

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

#### Utilisation de parameter.ts (Méthode recommandée avec typage sécurisé)

Pour une meilleure sécurité des types et une meilleure expérience développeur, vous pouvez utiliser le fichier `parameter.ts` pour définir vos paramètres :

```typescript
// Define parameters for the default environment
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Define parameters for additional environments
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Cost-saving for dev environment
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Enhanced availability for production
});
```

> [!Note]
> Les utilisateurs existants peuvent continuer à utiliser `cdk.json` sans changement. L'approche `parameter.ts` est recommandée pour les nouveaux déploiements ou lorsque vous devez gérer plusieurs environnements.

### Déploiement de plusieurs environnements

Vous pouvez déployer plusieurs environnements à partir du même code source en utilisant le fichier `parameter.ts` et l'option `-c envName`.

#### Prérequis

1. Définissez vos environnements dans `parameter.ts` comme montré ci-dessus
2. Chaque environnement aura son propre ensemble de ressources avec des préfixes spécifiques

#### Commandes de déploiement

Pour déployer un environnement spécifique :

```bash
# Deploy the dev environment
npx cdk deploy --all -c envName=dev

# Deploy the prod environment
npx cdk deploy --all -c envName=prod
```

Si aucun environnement n'est spécifié, l'environnement "default" est utilisé :

```bash
# Deploy the default environment
npx cdk deploy --all
```

#### Notes importantes

1. **Nommage des stacks** :

   - Les stacks principaux pour chaque environnement seront préfixés avec le nom de l'environnement (par ex. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Cependant, les stacks de bot personnalisés (`BrChatKbStack*`) et les stacks de publication d'API (`ApiPublishmentStack*`) ne reçoivent pas de préfixes d'environnement car ils sont créés dynamiquement à l'exécution

2. **Nommage des ressources** :

   - Seules certaines ressources reçoivent des préfixes d'environnement dans leurs noms (par ex. `dev_ddb_export` table, `dev-FrontendWebAcl`)
   - La plupart des ressources conservent leurs noms d'origine mais sont isolées en étant dans différentes stacks

3. **Identification de l'environnement** :

   - Toutes les ressources sont étiquetées avec une balise `CDKEnvironment` contenant le nom de l'environnement
   - Vous pouvez utiliser cette balise pour identifier à quel environnement appartient une ressource
   - Exemple : `CDKEnvironment: dev` ou `CDKEnvironment: prod`

4. **Remplacement de l'environnement par défaut** : Si vous définissez un environnement "default" dans `parameter.ts`, il remplacera les paramètres dans `cdk.json`. Pour continuer à utiliser `cdk.json`, ne définissez pas d'environnement "default" dans `parameter.ts`.

5. **Exigences d'environnement** : Pour créer des environnements autres que "default", vous devez utiliser `parameter.ts`. L'option `-c envName` seule n'est pas suffisante sans les définitions d'environnement correspondantes.

6. **Isolation des ressources** : Chaque environnement crée son propre ensemble de ressources, vous permettant d'avoir des environnements de développement, de test et de production dans le même compte AWS sans conflits.

## Autres

### Supprimer les ressources

Si vous utilisez cli et CDK, veuillez exécuter `npx cdk destroy`. Sinon, accédez à [CloudFormation](https://console.aws.amazon.com/cloudformation/home) puis supprimez manuellement `BedrockChatStack` et `FrontendWafStack`. Notez que `FrontendWafStack` se trouve dans la région `us-east-1`.

### Paramètres de langue

Cet actif détecte automatiquement la langue en utilisant [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Vous pouvez changer de langue depuis le menu de l'application. Alternativement, vous pouvez utiliser une chaîne de requête pour définir la langue comme indiqué ci-dessous.

> `https://example.com?lng=ja`

### Désactiver l'auto-inscription

Cet exemple a l'auto-inscription activée par défaut. Pour désactiver l'auto-inscription, ouvrez [cdk.json](./cdk/cdk.json) et définissez `selfSignUpEnabled` sur `false`. Si vous configurez un [fournisseur d'identité externe](#external-identity-provider), cette valeur sera ignorée et automatiquement désactivée.

### Restreindre les domaines pour les adresses e-mail d'inscription

Par défaut, cet exemple ne restreint pas les domaines pour les adresses e-mail d'inscription. Pour n'autoriser les inscriptions que depuis des domaines spécifiques, ouvrez `cdk.json` et spécifiez les domaines dans une liste sous `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Fournisseur d'identité externe

Cet exemple prend en charge les fournisseurs d'identité externes. Actuellement, nous prenons en charge [Google](./idp/SET_UP_GOOGLE_fr-FR.md) et [un fournisseur OIDC personnalisé](./idp/SET_UP_CUSTOM_OIDC_fr-FR.md).

### WAF Frontend optionnel

Pour les distributions CloudFront, les WebACL AWS WAF doivent être créés dans la région us-east-1. Dans certaines organisations, la création de ressources en dehors de la région principale est restreinte par des politiques. Dans ces environnements, le déploiement CDK peut échouer lors de la tentative de provisionnement du WAF Frontend en us-east-1.

Pour tenir compte de ces restrictions, la pile WAF Frontend est optionnelle. Lorsqu'elle est désactivée, la distribution CloudFront est déployée sans WebACL. Cela signifie que vous n'aurez pas de contrôles d'autorisation/refus d'IP au niveau du frontend. L'authentification et tous les autres contrôles d'application continuent de fonctionner normalement. Notez que ce paramètre n'affecte que le WAF Frontend (portée CloudFront) ; le WAF de l'API publiée (régional) reste inchangé.

Pour désactiver le WAF Frontend, définissez ce qui suit dans `parameter.ts` (Méthode recommandée avec typage) :

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

Ou si vous utilisez le `cdk/cdk.json` classique, définissez :

```json
"enableFrontendWaf": false
```

### Ajouter automatiquement de nouveaux utilisateurs aux groupes

Cet exemple comporte les groupes suivants pour donner des autorisations aux utilisateurs :

- [`Admin`](./ADMINISTRATOR_fr-FR.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_fr-FR.md)

Si vous souhaitez que les nouveaux utilisateurs rejoignent automatiquement des groupes, vous pouvez les spécifier dans [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Par défaut, les nouveaux utilisateurs seront ajoutés au groupe `CreatingBotAllowed`.

### Configurer les réplicas RAG

`enableRagReplicas` est une option dans [cdk.json](./cdk/cdk.json) qui contrôle les paramètres de réplication pour la base de données RAG, en particulier les bases de connaissances utilisant Amazon OpenSearch Serverless.

- **Par défaut** : true
- **true** : Améliore la disponibilité en activant des réplicas supplémentaires, ce qui convient aux environnements de production mais augmente les coûts.
- **false** : Réduit les coûts en utilisant moins de réplicas, ce qui convient au développement et aux tests.

C'est un paramètre au niveau du compte/région, affectant l'application entière plutôt que des bots individuels.

> [!Note]
> À partir de juin 2024, Amazon OpenSearch Serverless prend en charge 0,5 OCU, réduisant les coûts d'entrée pour les charges de travail à petite échelle. Les déploiements de production peuvent commencer avec 2 OCU, tandis que les charges de développement/test peuvent utiliser 1 OCU. OpenSearch Serverless s'adapte automatiquement en fonction des demandes de charge de travail. Pour plus de détails, visitez l'[annonce](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Configurer le Bot Store

La fonctionnalité de bot store permet aux utilisateurs de partager et de découvrir des bots personnalisés. Vous pouvez configurer le bot store via les paramètres suivants dans [cdk.json](./cdk/cdk.json) :

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore** : Contrôle si la fonctionnalité bot store est activée (par défaut : `true`)
- **botStoreLanguage** : Définit la langue principale pour la recherche et la découverte de bots (par défaut : `"en"`). Cela affecte la façon dont les bots sont indexés et recherchés dans le bot store, en optimisant l'analyse de texte pour la langue spécifiée.
- **enableBotStoreReplicas** : Contrôle si les réplicas de secours sont activés pour la collection OpenSearch Serverless utilisée par le bot store (par défaut : `false`). Le définir sur `true` améliore la disponibilité mais augmente les coûts, tandis que `false` réduit les coûts mais peut affecter la disponibilité.
  > **Important** : Vous ne pouvez pas mettre à jour cette propriété une fois que la collection est déjà créée. Si vous tentez de modifier cette propriété, la collection continuera d'utiliser la valeur d'origine.

### Inférence inter-régions et globale

[L'inférence inter-régions et globale](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) permet à Amazon Bedrock de router dynamiquement les requêtes d'inférence de modèle à travers plusieurs régions AWS, améliorant le débit et la résilience pendant les périodes de forte demande. L'inférence globale route les requêtes vers la région optimale en fonction de la latence et de la disponibilité partout dans le monde, tandis que l'inférence inter-régions route les requêtes au sein de la même région AWS, par exemple aux États-Unis. Certains SCP peuvent restreindre l'un ou l'autre ou les deux, et vous pouvez donc les configurer indépendamment. Par défaut, les deux sont activés.

Pour configurer, modifiez les paramètres suivants dans `cdk.json` ou `parameters.ts` :

```json
"enableBedrockGlobalInference": false,
"enableBedrockCrossRegionInference": false,
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) améliore les temps de démarrage à froid des fonctions Lambda, offrant des temps de réponse plus rapides pour une meilleure expérience utilisateur. En revanche, pour les fonctions Python, il y a des [frais en fonction de la taille du cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) et ce n'est [pas disponible dans certaines régions](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) actuellement. Pour désactiver SnapStart, modifiez `cdk.json`.

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
- Créer les enregistrements DNS nécessaires dans votre zone hébergée Route 53
- Configurer CloudFront pour utiliser votre domaine personnalisé

> [!Note]
> Le domaine doit être géré par Route 53 dans votre compte AWS. L'ID de la zone hébergée peut être trouvé dans la console Route 53.

### Configurer les pays autorisés (restriction géographique)

Vous pouvez restreindre l'accès à Bedrock-Chat en fonction du pays d'où le client y accède.
Utilisez le paramètre `allowedCountries` dans [cdk.json](./cdk/cdk.json) qui prend une liste de [codes pays ISO-3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).
Par exemple, une entreprise basée en Nouvelle-Zélande peut décider que seules les adresses IP de Nouvelle-Zélande (NZ) et d'Australie (AU) peuvent accéder au portail et que tous les autres doivent être refusés.
Pour configurer ce comportement, utilisez le paramètre suivant dans [cdk.json](./cdk/cdk.json) :

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

Ou, en utilisant `parameter.ts` (Méthode recommandée avec typage) :

```ts
// Définir les paramètres pour l'environnement par défaut
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### Désactiver le support IPv6

Le frontend reçoit par défaut des adresses IP et IPv6. Dans certains cas rares, vous devrez peut-être désactiver explicitement le support IPv6. Pour ce faire, définissez le paramètre suivant dans [parameter.ts](./cdk/parameter.ts) ou de manière similaire dans [cdk.json](./cdk/cdk.json) :

```ts
"enableFrontendIpv6": false
```

Si non défini, le support IPv6 sera activé par défaut.

### Développement local

Voir [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_fr-FR.md).

### Contribution

Merci d'envisager de contribuer à ce dépôt ! Nous accueillons les corrections de bugs, les traductions linguistiques (i18n), les améliorations de fonctionnalités, les [outils d'agent](./docs/AGENT.md#how-to-develop-your-own-tools), et autres améliorations.

Pour les améliorations de fonctionnalités et autres améliorations, **avant de créer une Pull Request, nous vous serions reconnaissants de créer une Issue de demande de fonctionnalité pour discuter de l'approche d'implémentation et des détails. Pour les corrections de bugs et les traductions linguistiques (i18n), procédez directement à la création d'une Pull Request.**

Veuillez également consulter les directives suivantes avant de contribuer :

- [Développement local](./LOCAL_DEVELOPMENT_fr-FR.md)
- [CONTRIBUTING](./CONTRIBUTING_fr-FR.md)

## Contacts

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Contributeurs Importants

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Contributeurs

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Licence

Cette bibliothèque est distribuée sous la licence MIT-0. Voir [le fichier LICENSE](./LICENSE).