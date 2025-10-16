# Agent alimenté par LLM (ReAct)

## Qu'est-ce que l'Agent (ReAct) ?

Un Agent est un système d'IA avancé qui utilise des grands modèles de langage (LLM) comme moteur de calcul central. Il combine les capacités de raisonnement des LLM avec des fonctionnalités supplémentaires comme la planification et l'utilisation d'outils pour exécuter des tâches complexes de manière autonome. Les Agents peuvent décomposer des requêtes complexes, générer des solutions étape par étape et interagir avec des outils externes ou des API pour recueillir des informations ou exécuter des sous-tâches.

Cet exemple implémente un Agent en utilisant l'approche [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct permet à l'agent de résoudre des tâches complexes en combinant raisonnement et actions dans une boucle de rétroaction itérative. L'agent passe continuellement par trois étapes clés : Réflexion, Action et Observation. Il analyse la situation actuelle en utilisant le LLM, décide de la prochaine action à entreprendre, exécute l'action en utilisant les outils ou API disponibles, et apprend des résultats observés. Ce processus continu permet à l'agent de s'adapter aux environnements dynamiques, d'améliorer sa précision dans la résolution des tâches et de fournir des solutions contextuelles.

L'implémentation est alimentée par [Strands Agents](https://strandsagents.com/), un SDK open-source qui adopte une approche basée sur les modèles pour construire des agents IA. Strands fournit un framework léger et flexible pour créer des outils personnalisés en utilisant des décorateurs Python et prend en charge plusieurs fournisseurs de modèles, y compris Amazon Bedrock.

## Exemple de cas d'utilisation

Un Agent utilisant ReAct peut être appliqué dans divers scénarios, fournissant des solutions précises et efficaces.

### Text-to-SQL

Un utilisateur demande "le total des ventes pour le dernier trimestre". L'Agent interprète cette demande, la convertit en requête SQL, l'exécute sur la base de données et présente les résultats.

### Prévisions financières

Un analyste financier doit prévoir les revenus du prochain trimestre. L'Agent rassemble les données pertinentes, effectue les calculs nécessaires en utilisant des modèles financiers et génère un rapport de prévision détaillé, garantissant l'exactitude des projections.

## Pour utiliser la fonctionnalité Agent

Pour activer la fonctionnalité Agent pour votre chatbot personnalisé, suivez ces étapes :

Il existe deux façons d'utiliser la fonctionnalité Agent :

### Utilisation des outils

Pour activer la fonctionnalité Agent avec les outils pour votre chatbot personnalisé, suivez ces étapes :

1. Accédez à la section Agent dans l'écran du bot personnalisé.

2. Dans la section Agent, vous trouverez une liste d'outils disponibles qui peuvent être utilisés par l'Agent. Par défaut, tous les outils sont désactivés.

3. Pour activer un outil, il suffit de basculer l'interrupteur à côté de l'outil souhaité. Une fois qu'un outil est activé, l'Agent y aura accès et pourra l'utiliser lors du traitement des requêtes utilisateur.

![](./imgs/agent_tools.png)

4. Par exemple, l'outil "Recherche Internet" permet à l'Agent d'obtenir des informations depuis internet pour répondre aux questions des utilisateurs.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Vous pouvez développer et ajouter vos propres outils personnalisés pour étendre les capacités de l'Agent. Consultez la section [Comment développer vos propres outils](#how-to-develop-your-own-tools) pour plus d'informations sur la création et l'intégration d'outils personnalisés.

### Utilisation de Bedrock Agent

Vous pouvez utiliser un [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) créé dans Amazon Bedrock.

Tout d'abord, créez un Agent dans Bedrock (par exemple, via la Console de gestion). Ensuite, spécifiez l'ID de l'Agent dans l'écran des paramètres du bot personnalisé. Une fois configuré, votre chatbot utilisera le Bedrock Agent pour traiter les requêtes des utilisateurs.

![](./imgs/bedrock_agent_tool.png)

## Comment développer vos propres outils

Pour développer vos propres outils personnalisés pour l'Agent en utilisant Strands SDK, suivez ces directives :

### À propos des outils Strands

Strands fournit un simple décorateur `@tool` qui transforme des fonctions Python ordinaires en outils pour agents IA. Le décorateur extrait automatiquement les informations de la docstring et des annotations de type de votre fonction pour créer des spécifications d'outils que le LLM peut comprendre et utiliser. Cette approche exploite les fonctionnalités natives de Python pour une expérience de développement d'outils propre et fonctionnelle.

Pour des informations détaillées sur les outils Strands, consultez la [documentation Python Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Création basique d'un outil

Créez une nouvelle fonction décorée avec le décorateur `@tool` de Strands :

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Effectue des calculs mathématiques de manière sécurisée.

    Args:
        expression: Expression mathématique à évaluer (ex : "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Résultat au format Strands avec toolUseId, status et content
    """
    try:
        # Votre logique de calcul ici
        result = eval(expression)  # Note : Utilisez une évaluation sécurisée en production
        return {
            "toolUseId": "placeholder",
            "status": "success",
            "content": [{"text": str(result)}]
        }
    except Exception as e:
        return {
            "toolUseId": "placeholder",
            "status": "error",
            "content": [{"text": f"Error: {str(e)}"}]
        }
```

### Outils avec contexte de bot (Pattern Closure)

Pour accéder aux informations du bot (BotModel), utilisez un pattern closure qui capture le contexte du bot :

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Crée un outil calculateur avec un contexte de bot en closure."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Effectue des calculs mathématiques de manière sécurisée.

        Args:
            expression: Expression mathématique à évaluer (ex : "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Résultat au format Strands avec toolUseId, status et content
        """
        # Accès au contexte du bot dans l'outil
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # Utilisez une évaluation sécurisée en production
            return {
                "toolUseId": "placeholder",
                "status": "success",
                "content": [{"text": str(result)}]
            }
        except Exception as e:
            return {
                "toolUseId": "placeholder",
                "status": "error",
                "content": [{"text": f"Error: {str(e)}"}]
            }

    return calculator
```

### Exigences de format de retour

Tous les outils Strands doivent retourner un dictionnaire avec la structure suivante :

```python
{
    "toolUseId": "placeholder",  # Sera remplacé par Strands
    "status": "success" | "error",
    "content": [
        {"text": "Réponse texte simple"} |
        {"json": {"key": "Objet de données complexe"}}
    ]
}
```

- Utilisez `{"text": "message"}` pour les réponses texte simples
- Utilisez `{"json": data}` pour les données complexes qui doivent être préservées comme informations structurées
- Définissez toujours `status` sur `"success"` ou `"error"`

### Directives d'implémentation

- Le nom de la fonction et la docstring sont utilisés lorsque le LLM détermine quel outil utiliser. La docstring est intégrée dans le prompt, alors décrivez précisément l'objectif et les paramètres de l'outil.

- Référez-vous à l'implémentation exemple d'un [outil de calcul d'IMC](../examples/agents/tools/bmi/bmi_strands.py). Cet exemple montre comment créer un outil qui calcule l'Indice de Masse Corporelle (IMC) en utilisant le décorateur `@tool` de Strands et le pattern closure.

- Après le développement, placez votre fichier d'implémentation dans le répertoire [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/). Puis ouvrez [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) et modifiez `get_strands_registered_tools` pour inclure votre nouvel outil.

- [Optionnel] Ajoutez des noms et descriptions clairs pour le frontend. Cette étape est optionnelle, mais si vous ne la faites pas, le nom et la description de votre fonction seront utilisés. Comme ceux-ci sont destinés à la consommation du LLM, il est recommandé d'ajouter des explications conviviales pour une meilleure expérience utilisateur.

  - Modifiez les fichiers i18n. Ouvrez [en/index.ts](../frontend/src/i18n/en/index.ts) et ajoutez votre propre `name` et `description` dans `agent.tools`.
  - Modifiez également `xx/index.ts`. Où `xx` représente le code pays souhaité.

- Exécutez `npx cdk deploy` pour déployer vos modifications. Cela rendra votre outil personnalisé disponible dans l'écran de bot personnalisé.