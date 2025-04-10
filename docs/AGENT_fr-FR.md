# Agent alimenté par LLM (ReAct)

## Qu'est-ce que l'Agent (ReAct) ?

Un Agent est un système d'IA avancé qui utilise des modèles de langage à grande échelle (LLM) comme moteur de calcul central. Il combine les capacités de raisonnement des LLM avec des fonctionnalités supplémentaires telles que la planification et l'utilisation d'outils pour effectuer des tâches complexes de manière autonome. Les Agents peuvent décomposer des requêtes compliquées, générer des solutions étape par étape et interagir avec des outils externes ou des API pour collecter des informations ou exécuter des sous-tâches.

Cet exemple implémente un Agent en utilisant l'approche [ReAct (Raisonnement + Action)](https://www.promptingguide.ai/techniques/react). ReAct permet à l'agent de résoudre des tâches complexes en combinant le raisonnement et les actions dans une boucle de rétroaction itérative. L'agent passe à plusieurs reprises par trois étapes clés : Pensée, Action et Observation. Il analyse la situation actuelle à l'aide du LLM, décide de l'action suivante à entreprendre, exécute l'action en utilisant des outils ou des API disponibles, et apprend des résultats observés. Ce processus continu permet à l'agent de s'adapter à des environnements dynamiques, d'améliorer sa précision dans la résolution de tâches et de fournir des solutions contextuelles.

## Exemple de Cas d'Utilisation

Un Agent utilisant ReAct peut être appliqué dans divers scénarios, offrant des solutions précises et efficaces.

### Texte-vers-SQL

Un utilisateur demande "le total des ventes du dernier trimestre". L'Agent interprète cette requête, la convertit en une requête SQL, l'exécute sur la base de données et présente les résultats.

### Prévisions Financières

Un analyste financier a besoin de prévoir le chiffre d'affaires du prochain trimestre. L'Agent collecte les données pertinentes, effectue les calculs nécessaires à l'aide de modèles financiers et génère un rapport de prévision détaillé, garantissant la précision des projections.

## Pour utiliser la fonctionnalité Agent

Pour activer la fonctionnalité Agent pour votre chatbot personnalisé, suivez ces étapes :

Il existe deux façons d'utiliser la fonctionnalité Agent :

### Utilisation de Tool Use

Pour activer la fonctionnalité Agent avec Tool Use pour votre chatbot personnalisé, suivez ces étapes :

1. Accédez à la section Agent dans l'écran du bot personnalisé.

2. Dans la section Agent, vous trouverez une liste d'outils disponibles pouvant être utilisés par l'Agent. Par défaut, tous les outils sont désactivés.

3. Pour activer un outil, il vous suffit de basculer l'interrupteur à côté de l'outil souhaité. Une fois un outil activé, l'Agent y aura accès et pourra l'utiliser lors du traitement des requêtes utilisateur.

![](./imgs/agent_tools.png)

4. Par exemple, l'outil "Recherche Internet" permet à l'Agent de récupérer des informations sur internet pour répondre aux questions des utilisateurs.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Vous pouvez développer et ajouter vos propres outils personnalisés pour étendre les capacités de l'Agent. Reportez-vous à la section [Comment développer vos propres outils](#how-to-develop-your-own-tools) pour plus d'informations sur la création et l'intégration d'outils personnalisés.

### Utilisation de Bedrock Agent

Vous pouvez utiliser un [Agent Bedrock](https://aws.amazon.com/bedrock/agents/) créé dans Amazon Bedrock.

Commencez par créer un Agent dans Bedrock (par exemple, via la Console de gestion). Ensuite, spécifiez l'ID de l'Agent dans l'écran des paramètres du bot personnalisé. Une fois configuré, votre chatbot utilisera l'Agent Bedrock pour traiter les requêtes utilisateur.

![](./imgs/bedrock_agent_tool.png)

## Comment développer vos propres outils

Pour développer des outils personnalisés pour l'Agent, suivez ces directives :

- Créez une nouvelle classe qui hérite de la classe `AgentTool`. Bien que l'interface soit compatible avec LangChain, cette implémentation d'exemple fournit sa propre classe `AgentTool`, dont vous devez hériter ([source](../backend/app/agents/tools/agent_tool.py)).

- Référez-vous à l'implémentation exemple d'un [outil de calcul d'IMC](../examples/agents/tools/bmi/bmi.py). Cet exemple montre comment créer un outil qui calcule l'Indice de Masse Corporelle (IMC) en fonction de la saisie de l'utilisateur.

  - Le nom et la description déclarés sur l'outil sont utilisés lorsque le LLM considère quel outil doit être utilisé pour répondre à la question de l'utilisateur. En d'autres termes, ils sont intégrés dans l'invite lors de l'appel du LLM. Il est donc recommandé de les décrire le plus précisément possible.

- [Optionnel] Une fois que vous avez implémenté votre outil personnalisé, il est recommandé de vérifier sa fonctionnalité à l'aide d'un script de test ([exemple](../examples/agents/tools/bmi/test_bmi.py)). Ce script vous aidera à vous assurer que votre outil fonctionne comme prévu.

- Après avoir terminé le développement et les tests de votre outil personnalisé, déplacez le fichier d'implémentation dans le répertoire [backend/app/agents/tools/](../backend/app/agents/tools/). Puis ouvrez [backend/app/agents/utils.py](../backend/app/agents/utils.py) et modifiez `get_available_tools` pour que l'utilisateur puisse sélectionner l'outil développé.

- [Optionnel] Ajoutez des noms et des descriptions clairs pour le frontend. Cette étape est facultative, mais si vous ne la faites pas, le nom et la description de l'outil déclarés dans votre outil seront utilisés. Ils sont destinés au LLM mais pas à l'utilisateur, il est donc recommandé d'ajouter une explication dédiée pour une meilleure expérience utilisateur.

  - Modifiez les fichiers i18n. Ouvrez [en/index.ts](../frontend/src/i18n/en/index.ts) et ajoutez votre propre `name` et `description` dans `agent.tools`.
  - Modifiez également `xx/index.ts`. Où `xx` représente le code de pays que vous souhaitez.

- Exécutez `npx cdk deploy` pour déployer vos modifications. Cela rendra votre outil personnalisé disponible dans l'écran du bot personnalisé.

## Contribution

**Les contributions au dépôt d'outils sont les bienvenues !** Si vous développez un outil utile et bien implémenté, envisagez de le contribuer au projet en soumettant un problème ou une pull request.