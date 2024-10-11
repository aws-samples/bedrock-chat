# Migration Guide (v1 to v2)

## TL;DR

- **For users of v1.2 or earlier**: Upgrade to v1.4 and recreate your bots using Knowledge Base (KB). After a transition period, once you confirm everything works as expected with KB, proceed with upgrading to v2.
- **For users of v1.3**: Even if you are already using KB, it is **strongly recommended** to upgrade to v1.4 and recreate your bots. If you are still using pgvector, migrate by recreating your bots using KB in v1.4.
- **For users who wish to continue using pgvector**: Upgrading to v2 is not recommended if you plan to continue using pgvector. Upgrading to v2 will remove all resources related to pgvector, and future support will no longer be available. Continue using v1 in this case.
- Note that **upgrading to v2 will result in the deletion of all Aurora-related resources.** Future updates will focus exclusively on v2, with v1 being deprecated.

## Introduction

### What will happen

The v2 update introduces a major change by replacing pgvector on Aurora Serverless and ECS-based embedding with [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). This change is not backward compatible.

### Why this repository has adopted Knowledge Bases and discontinued pgvector

There are several reasons for this change:

#### Improved RAG Accuracy

- Knowledge Bases use OpenSearch Serverless as the backend, allowing hybrid searches with both full-text and vector search. This leads to better accuracy in responding to questions that include proper nouns, which pgvector struggled with.
- It also supports more options for improving RAG accuracy, such as advanced chunking and parsing.
- Knowledge Bases have been generally available for almost a year as of October 2024, with features like web crawling already added. Future updates are expected, making it easier to adopt advanced functionality over the long term. For example, while this repository has not implemented features like importing from existing S3 buckets (a frequently requested feature) in pgvector, it is already supported in KB (KnowledgeBases).

#### Maintenance

- The current ECS + Aurora setup depends on numerous libraries, including those for PDF parsing, web crawling, and extracting YouTube transcripts. In comparison, managed solutions like Knowledge Bases reduce the maintenance burden for both users and the repository's development team.

## Migration Process (Summary)

We strongly recommend upgrading to v1.4 before moving to v2. In v1.4, you can use both pgvector and Knowledge Base bots, allowing a transition period to recreate your existing pgvector bots in Knowledge Base and verify they work as expected. Even if the RAG documents remain identical, note that the backend changes to OpenSearch may produce slightly different results, though generally similar, due to differences like k-NN algorithms.

By setting `useBedrockKnowledgeBasesForRag` to true in `cdk.json`, you can create bots using Knowledge Bases. However, pgvector bots will become read-only, preventing the creation or editing of new pgvector bots.

![](../imgs/v1_to_v2_readonly_bot.png)

In v1.4, [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) are also introduced. Due to regional restrictions of Knowledge Bases, the S3 bucket for uploading documents must be in the same region as `bedrockRegion`. We recommend backing up existing document buckets before updating, to avoid manually uploading large numbers of documents later (as S3 bucket import functionality is available).

## Migration Process (Detail)

The steps differ depending on whether you are using v1.2 or earlier, or v1.3.

![](../imgs/v1_to_v2_arch.png)

### Steps for users of v1.2 or earlier

1. **Backup your existing document bucket (optional but recommended).** If your system is already in operation, we strongly recommend this step. Back up the bucket named `bedrockchatstack-documentbucketxxxx-yyyy`. For example, we can use [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Update to v1.4**: Fetch the latest v1.4 tag, modify `cdk.json`, and deploy. Follow these steps:

   1. Fetch the latest tag:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modify `cdk.json` as follows:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Deploy the changes:
      ```bash
      cdk deploy
      ```

3. **Recrate your bots**: Recreate your bots on Knowledge Base with the same definitions (documents, chunk size, etc.) as the pgvector bots. If you have a large volume of documents, restoring from the backup in step 1 will make this process easier. To restore, we can use restoring cross-region copies. For more detail, visit [here](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). To specify the restored bucket, set `S3 Data Source` section as following. The path structure is `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. You can check user id on Cognito user pool and bot id on address bar on bot creation screen.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Note that some features are not available on Knowledge Bases, such as web crawling and YouTube transcript support (Planning to support web crawler ([issue](https://github.com/aws-samples/bedrock-claude-chat/issues/557))).** Also, keep in mind that using Knowledge Bases will incur charges for both Aurora and Knowledge Bases during the transition.

4. **Remove published APIs**: All previously published APIs will need to be republished before deploying v2 due to VPC deletion. To do this, you will need to delete the existing APIs first. Using the [administrator's API Management feature](../ADMINISTRATOR.md) can simplify this process. Once the deletion of all `APIPublishmentStackXXXX` CloudFormation stacks is complete, the environment will be ready.

5. **Deploy v2**: After the release of v2, fetch the tagged source and deploy as follows (this will be possible once released):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   cdk deploy
   ```

> [!Warning]
> After deploying v2, **ALL BOTS WITH THE PREFIX [Unsupported, Read-only] WILL BE HIDDEN.** Ensure you recreate necessary bots before upgrading to avoid any loss of access.

> [!Tip]
> During stack updates, you might encounter repeated messages like: Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." In such cases, navigate to the Management Console > EC2 > Network Interfaces and search for BedrockChatStack. Delete the displayed interfaces associated with this name to help ensure a smoother deployment process.

### Steps for users of v1.3

As mentioned earlier, in v1.4, Knowledge Bases must be created in the bedrockRegion due to regional restrictions. Therefore, you will need to recreate the KB. If you have already tested KB in v1.3, recreate the bot in v1.4 with the same definitions. Follow the steps outlined for v1.2 users.
