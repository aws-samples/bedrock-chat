# Guide de Migration (v1 à v2)

## TL;DR

- **Pour les utilisateurs de v1.2 ou antérieure** : Passez à la v1.4 et recréez vos bots en utilisant Knowledge Base (KB). Après une période de transition, une fois que vous aurez confirmé que tout fonctionne comme prévu avec KB, procédez à la mise à niveau vers v2.
- **Pour les utilisateurs de v1.3** : Même si vous utilisez déjà KB, il est **fortement recommandé** de passer à la v1.4 et de recréer vos bots. Si vous utilisez encore pgvector, migrez en recréant vos bots avec KB dans la v1.4.
- **Pour les utilisateurs qui souhaitent continuer à utiliser pgvector** : La mise à niveau vers v2 n'est pas recommandée si vous prévoyez de continuer à utiliser pgvector. La mise à niveau vers v2 supprimera toutes les ressources liées à pgvector, et le support ne sera plus disponible à l'avenir. Continuez à utiliser v1 dans ce cas.
- Notez que **la mise à niveau vers v2 entraînera la suppression de toutes les ressources liées à Aurora.** Les mises à jour futures se concentreront exclusivement sur v2, la v1 étant dépréciée.

## Introduction

### Ce qui va se passer

La mise à jour v2 introduit un changement majeur en remplaçant pgvector sur Aurora Serverless et l'intégration basée sur ECS par [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Ce changement n'est pas rétrocompatible.

### Pourquoi ce dépôt a adopté Knowledge Bases et abandonné pgvector

Il y a plusieurs raisons à ce changement :

#### Amélioration de la précision RAG

- Knowledge Bases utilise OpenSearch Serverless comme backend, permettant des recherches hybrides combinant recherche plein texte et recherche vectorielle. Cela conduit à une meilleure précision dans les réponses aux questions incluant des noms propres, avec lesquels pgvector avait des difficultés.
- Il offre également plus d'options pour améliorer la précision RAG, comme le découpage et l'analyse avancés.
- Knowledge Bases est généralement disponible depuis près d'un an en octobre 2024, avec des fonctionnalités déjà ajoutées comme le crawling web. D'autres mises à jour sont attendues, facilitant l'adoption de fonctionnalités avancées sur le long terme. Par exemple, bien que ce dépôt n'ait pas implémenté des fonctionnalités comme l'importation depuis des buckets S3 existants (une fonctionnalité fréquemment demandée) dans pgvector, celle-ci est déjà prise en charge dans KB (KnowledgeBases).

#### Maintenance

- La configuration actuelle ECS + Aurora dépend de nombreuses bibliothèques, y compris celles pour l'analyse PDF, le crawling web et l'extraction de transcriptions YouTube. En comparaison, les solutions managées comme Knowledge Bases réduisent la charge de maintenance tant pour les utilisateurs que pour l'équipe de développement du dépôt.

## Processus de Migration (Résumé)

Nous recommandons vivement de passer à la v1.4 avant de migrer vers la v2. Dans la v1.4, vous pouvez utiliser à la fois pgvector et les robots Knowledge Base, permettant une période de transition pour recréer vos robots pgvector existants dans Knowledge Base et vérifier qu'ils fonctionnent comme prévu. Même si les documents RAG restent identiques, notez que les changements backend vers OpenSearch peuvent produire des résultats légèrement différents, bien que généralement similaires, en raison de différences comme les algorithmes k-NN.

En définissant `useBedrockKnowledgeBasesForRag` sur true dans `cdk.json`, vous pouvez créer des robots utilisant Knowledge Bases. Cependant, les robots pgvector deviendront en lecture seule, empêchant la création ou la modification de nouveaux robots pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

Dans la v1.4, les [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) sont également introduits. En raison des restrictions régionales de Knowledge Bases, le bucket S3 pour le téléchargement des documents doit être dans la même région que `bedrockRegion`. Nous recommandons de sauvegarder les buckets de documents existants avant la mise à jour, pour éviter d'avoir à télécharger manuellement un grand nombre de documents ultérieurement (car la fonctionnalité d'importation de bucket S3 est disponible).

## Processus de Migration (Détail)

Les étapes diffèrent selon que vous utilisez la v1.2 ou antérieure, ou la v1.3.

![](../imgs/v1_to_v2_arch.png)

### Étapes pour les utilisateurs de v1.2 ou antérieure

1. **Sauvegardez votre bucket de documents existant (optionnel mais recommandé).** Si votre système est déjà en production, nous recommandons fortement cette étape. Sauvegardez le bucket nommé `bedrockchatstack-documentbucketxxxx-yyyy`. Par exemple, nous pouvons utiliser [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Mise à jour vers v1.4**: Récupérez le dernier tag v1.4, modifiez `cdk.json`, et déployez. Suivez ces étapes:

   1. Récupérez le dernier tag:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modifiez `cdk.json` comme suit:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Déployez les changements:
      ```bash
      npx cdk deploy
      ```

3. **Recréez vos bots**: Recréez vos bots sur Knowledge Base avec les mêmes définitions (documents, taille de fragments, etc.) que les bots pgvector. Si vous avez un grand volume de documents, la restauration à partir de la sauvegarde de l'étape 1 facilitera ce processus. Pour restaurer, nous pouvons utiliser la restauration de copies inter-régions. Pour plus de détails, visitez [ici](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Pour spécifier le bucket restauré, configurez la section `S3 Data Source` comme suit. La structure du chemin est `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Vous pouvez vérifier l'ID utilisateur dans le pool d'utilisateurs Cognito et l'ID du bot dans la barre d'adresse sur l'écran de création du bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Notez que certaines fonctionnalités ne sont pas disponibles sur Knowledge Bases, comme le crawling web et le support des transcriptions YouTube (Planification du support du crawler web ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** De plus, gardez à l'esprit que l'utilisation de Knowledge Bases entraînera des frais pour Aurora et Knowledge Bases pendant la transition.

4. **Supprimez les API publiées**: Toutes les API précédemment publiées devront être republiées avant le déploiement de v2 en raison de la suppression du VPC. Pour cela, vous devrez d'abord supprimer les API existantes. L'utilisation de la [fonctionnalité de gestion des API de l'administrateur](../ADMINISTRATOR_fr-FR.md) peut simplifier ce processus. Une fois la suppression de toutes les piles CloudFormation `APIPublishmentStackXXXX` terminée, l'environnement sera prêt.

5. **Déployez v2**: Après la sortie de v2, récupérez le code source tagué et déployez comme suit (ce sera possible une fois publié):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> Après le déploiement de v2, **TOUS LES BOTS AVEC LE PRÉFIXE [Unsupported, Read-only] SERONT MASQUÉS.** Assurez-vous de recréer les bots nécessaires avant la mise à niveau pour éviter toute perte d'accès.

> [!Tip]
> Pendant les mises à jour de la pile, vous pourriez rencontrer des messages répétés comme : Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." Dans ce cas, accédez à la Console de gestion > EC2 > Interfaces réseau et recherchez BedrockChatStack. Supprimez les interfaces affichées associées à ce nom pour faciliter le processus de déploiement.

### Étapes pour les utilisateurs de v1.3

Comme mentionné précédemment, dans v1.4, Knowledge Bases doit être créé dans la bedrockRegion en raison des restrictions régionales. Par conséquent, vous devrez recréer le KB. Si vous avez déjà testé KB dans v1.3, recréez le bot dans v1.4 avec les mêmes définitions. Suivez les étapes décrites pour les utilisateurs de v1.2.