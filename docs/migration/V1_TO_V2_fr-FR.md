# Guide de Migration (v1 à v2)

## TL;DR

- **Pour les utilisateurs de v1.2 ou antérieure** : Effectuez une mise à niveau vers v1.4 et recréez vos bots en utilisant la Base de Connaissances (BC). Après une période de transition, une fois que vous avez confirmé que tout fonctionne comme prévu avec BC, procédez à la mise à niveau vers v2.
- **Pour les utilisateurs de v1.3** : Même si vous utilisez déjà BC, il est **fortement recommandé** de mettre à niveau vers v1.4 et de recréer vos bots. Si vous utilisez encore pgvector, migrez en recréant vos bots à l'aide de BC dans v1.4.
- **Pour les utilisateurs qui souhaitent continuer à utiliser pgvector** : La mise à niveau vers v2 n'est pas recommandée si vous prévoyez de continuer à utiliser pgvector. La mise à niveau vers v2 supprimera toutes les ressources liées à pgvector, et le support futur ne sera plus disponible. Dans ce cas, continuez à utiliser v1.
- Notez que **la mise à niveau vers v2 entraînera la suppression de toutes les ressources liées à Aurora.** Les futures mises à jour se concentreront exclusivement sur v2, v1 étant abandonné.

## Introduction

### Ce qui va se passer

La mise à jour v2 introduit un changement majeur en remplaçant pgvector sur Aurora Serverless et l'intégration basée sur ECS par [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Ce changement n'est pas rétrocompatible.

### Pourquoi ce dépôt a adopté Knowledge Bases et abandonné pgvector

Plusieurs raisons motivent ce changement :

#### Amélioration de la précision RAG

- Knowledge Bases utilise OpenSearch Serverless comme backend, permettant des recherches hybrides avec recherche de texte intégral et vectorielle. Cela conduit à une meilleure précision pour répondre aux questions incluant des noms propres, un domaine où pgvector avait des difficultés.
- Il offre également plus d'options pour améliorer la précision RAG, comme le découpage et l'analyse avancés.
- Knowledge Bases est généralement disponible depuis presque un an en octobre 2024, avec des fonctionnalités comme le web crawling déjà ajoutées. Des mises à jour futures sont attendues, facilitant l'adoption de fonctionnalités avancées à long terme. Par exemple, bien que ce dépôt n'ait pas implémenté des fonctionnalités comme l'importation depuis des compartiments S3 existants (une fonctionnalité fréquemment demandée) dans pgvector, cela est déjà pris en charge dans KB (Knowledge Bases).

#### Maintenance

- La configuration actuelle ECS + Aurora dépend de nombreuses bibliothèques, notamment pour l'analyse PDF, le web crawling et l'extraction de transcriptions YouTube. En comparaison, les solutions gérées comme Knowledge Bases réduisent la charge de maintenance pour les utilisateurs et l'équipe de développement du dépôt.

## Processus de Migration (Résumé)

Nous recommandons fortement de mettre à niveau vers la v1.4 avant de passer à la v2. Dans la v1.4, vous pouvez utiliser à la fois les bots pgvector et les bots Knowledge Base, ce qui permet une période de transition pour recréer vos bots pgvector existants dans Knowledge Base et vérifier qu'ils fonctionnent comme prévu. Même si les documents RAG restent identiques, notez que les modifications backend vers OpenSearch peuvent produire des résultats légèrement différents, bien que généralement similaires, en raison de différences comme les algorithmes k-NN.

En définissant `useBedrockKnowledgeBasesForRag` sur true dans `cdk.json`, vous pouvez créer des bots utilisant Knowledge Bases. Cependant, les bots pgvector deviendront en lecture seule, empêchant la création ou la modification de nouveaux bots pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

Dans la v1.4, [Guardrails pour Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) sont également introduits. En raison des restrictions régionales de Knowledge Bases, le compartiment S3 pour le téléchargement des documents doit se trouver dans la même région que `bedrockRegion`. Nous recommandons de sauvegarder les compartiments de documents existants avant la mise à jour, afin d'éviter de télécharger manuellement un grand nombre de documents plus tard (car la fonctionnalité d'importation de compartiments S3 est disponible).

## Processus de Migration (Détail)

Les étapes diffèrent selon que vous utilisez la version 1.2 ou antérieure, ou la version 1.3.

![](../imgs/v1_to_v2_arch.png)

### Étapes pour les utilisateurs de v1.2 ou antérieure

1. **Sauvegardez votre bucket de documents existant (optionnel mais recommandé).** Si votre système est déjà en fonctionnement, nous recommandons fortement cette étape. Sauvegardez le bucket nommé `bedrockchatstack-documentbucketxxxx-yyyy`. Par exemple, nous pouvons utiliser [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Mise à jour vers v1.4** : Récupérez le dernier tag v1.4, modifiez `cdk.json`, et déployez. Suivez ces étapes :

   1. Récupérez le dernier tag :
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modifiez `cdk.json` comme suit :
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Déployez les modifications :
      ```bash
      npx cdk deploy
      ```

3. **Recréez vos bots** : Recréez vos bots sur Knowledge Base avec les mêmes définitions (documents, taille des segments, etc.) que les bots pgvector. Si vous avez un grand volume de documents, la restauration à partir de la sauvegarde à l'étape 1 facilitera ce processus. Pour restaurer, nous pouvons utiliser la restauration de copies inter-régions. Pour plus de détails, visitez [ici](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Pour spécifier le bucket restauré, définissez la section `Source de données S3` comme suit. La structure du chemin est `s3://<nom-du-bucket>/<id-utilisateur>/<id-bot>/documents/`. Vous pouvez vérifier l'ID utilisateur dans le pool d'utilisateurs Cognito et l'ID du bot dans la barre d'adresse de l'écran de création de bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Notez que certaines fonctionnalités ne sont pas disponibles sur Knowledge Bases, comme le crawling web et le support des transcriptions YouTube (Prévision de supporter le crawler web ([issue](https://github.com/aws-samples/bedrock-claude-chat/issues/557))).** Gardez à l'esprit que l'utilisation de Knowledge Bases entraînera des frais pour Aurora et Knowledge Bases pendant la transition.

4. **Supprimez les API publiées** : Toutes les API précédemment publiées devront être republiées avant de déployer v2 en raison de la suppression du VPC. Pour ce faire, vous devrez d'abord supprimer les API existantes. L'utilisation de la [fonctionnalité de gestion d'API de l'administrateur](../ADMINISTRATOR_fr-FR.md) peut simplifier ce processus. Une fois la suppression de toutes les piles CloudFormation `APIPublishmentStackXXXX` terminée, l'environnement sera prêt.

5. **Déployez v2** : Après la sortie de v2, récupérez le source tagué et déployez comme suit (cela sera possible une fois sorti) :
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Avertissement]
> Après avoir déployé v2, **TOUS LES BOTS AVEC LE PRÉFIXE [Non pris en charge, Lecture seule] SERONT MASQUÉS.** Assurez-vous de recréer les bots nécessaires avant la mise à niveau pour éviter toute perte d'accès.

> [!Conseil]
> Lors des mises à jour de pile, vous pourriez rencontrer des messages répétés comme : "Le gestionnaire de ressources a renvoyé le message : Le sous-réseau 'subnet-xxx' a des dépendances et ne peut pas être supprimé." Dans ce cas, accédez à la Console de gestion > EC2 > Interfaces réseau et recherchez BedrockChatStack. Supprimez les interfaces associées à ce nom pour faciliter un processus de déploiement plus fluide.

### Étapes pour les utilisateurs de v1.3

Comme mentionné précédemment, dans v1.4, les Knowledge Bases doivent être créées dans la région bedrockRegion en raison des restrictions régionales. Par conséquent, vous devrez recréer le KB. Si vous avez déjà testé KB dans v1.3, recréez le bot dans v1.4 avec les mêmes définitions. Suivez les étapes décrites pour les utilisateurs de v1.2.