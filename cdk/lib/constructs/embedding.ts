import { Construct } from "constructs";
import * as path from "path";
import { Duration, RemovalPolicy, Stack } from "aws-cdk-lib";
import * as iam from "aws-cdk-lib/aws-iam";
import * as logs from "aws-cdk-lib/aws-logs";
import { IBucket } from "aws-cdk-lib/aws-s3";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as codebuild from "aws-cdk-lib/aws-codebuild";
import { excludeDockerImage } from "../constants/docker";
import {
  DockerImageCode,
  DockerImageFunction,
  IFunction,
} from "aws-cdk-lib/aws-lambda";
import { DynamoEventSource } from "aws-cdk-lib/aws-lambda-event-sources";
import * as sfn from "aws-cdk-lib/aws-stepfunctions";
import * as tasks from "aws-cdk-lib/aws-stepfunctions-tasks";
import { Platform } from "aws-cdk-lib/aws-ecr-assets";
import { Database } from "./database";

export interface EmbeddingProps {
  readonly database: Database;
  readonly bedrockRegion: string;
  readonly documentBucket: IBucket;
  readonly bedrockCustomBotProject: codebuild.IProject;
  readonly bedrockSharedKnowledgeBasesProject: codebuild.IProject;
  readonly enableRagReplicas: boolean;
}

export class Embedding extends Construct {
  readonly stateMachine: sfn.StateMachine;
  readonly removalHandler: IFunction;

  private _updateSyncStatusHandler: IFunction;
  private _bootstrapStateMachineHandler: IFunction;
  private _finalizeCustomBotBuildHandler: IFunction;
  private _finalizeSharedKnowledgeBasesBuildHandler: IFunction;
  private _synchronizeDataSourceHandler: IFunction;
  private _lockHandler: IFunction;

  constructor(scope: Construct, id: string, props: EmbeddingProps) {
    super(scope, id);

    this.setupStateMachineHandlers(props);
    this.stateMachine = this.setupStateMachine(props)
    this.removalHandler = this.setupRemovalHandler(props);
  }

  private setupStateMachineHandlers(props: EmbeddingProps) {
    const handlerRole = new iam.Role(this, "HandlerRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });
    handlerRole.addToPolicy(
      // Assume the table access role for row-level access control.
      new iam.PolicyStatement({
        actions: ["sts:AssumeRole"],
        resources: [props.database.tableAccessRole.roleArn],
      })
    );
    handlerRole.addToPolicy(
      new iam.PolicyStatement({
        actions: ["bedrock:*"],
        resources: ["*"],
      })
    );
    handlerRole.addToPolicy(
      new iam.PolicyStatement({
        actions: [
          "cloudformation:DescribeStacks",
          "cloudformation:DescribeStackEvents",
          "cloudformation:DescribeStackResource",
          "cloudformation:DescribeStackResources",
        ],
        resources: [`*`],
      })
    );
    handlerRole.addToPolicy(
      new iam.PolicyStatement({
        actions: [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ],
        resources: ["arn:aws:logs:*:*:*"],
      })
    );
    props.documentBucket.grantReadWrite(handlerRole);

    this._updateSyncStatusHandler = new DockerImageFunction(
      this,
      "UpdateSyncStatusHandler",
      {
        code: DockerImageCode.fromImageAsset(
          path.join(__dirname, "../../../backend"),
          {
            platform: Platform.LINUX_AMD64,
            file: "lambda.Dockerfile",
            cmd: [
              "embedding_statemachine.bedrock_knowledge_base.update_bot_status.handler",
            ],
            exclude: [...excludeDockerImage],
          }
        ),
        memorySize: 512,
        timeout: Duration.minutes(1),
        environment: {
          ACCOUNT: Stack.of(this).account,
          REGION: Stack.of(this).region,
          CONVERSATION_TABLE_NAME: props.database.conversationTable.tableName,
          BOT_TABLE_NAME: props.database.botTable.tableName,
          TABLE_ACCESS_ROLE_ARN: props.database.tableAccessRole.roleArn,
        },
        role: handlerRole,
        logRetention: logs.RetentionDays.THREE_MONTHS,
      }
    );

    this._bootstrapStateMachineHandler = new DockerImageFunction(
      this,
      "BootstrapStateMachineHandler",
      {
        code: DockerImageCode.fromImageAsset(
          path.join(__dirname, "../../../backend"),
          {
            platform: Platform.LINUX_AMD64,
            file: "lambda.Dockerfile",
            cmd: [
              "embedding_statemachine.bedrock_knowledge_base.bootstrap_state_machine.handler",
            ],
            exclude: [...excludeDockerImage],
          }
        ),
        memorySize: 512,
        timeout: Duration.minutes(1),
        role: handlerRole,
        environment: {
          ACCOUNT: Stack.of(this).account,
          REGION: Stack.of(this).region,
          BOT_TABLE_NAME: props.database.botTable.tableName,
          TABLE_ACCESS_ROLE_ARN: props.database.tableAccessRole.roleArn,
        },
        logRetention: logs.RetentionDays.THREE_MONTHS,
      }
    );
    this._finalizeCustomBotBuildHandler = new DockerImageFunction(
      this,
      "FinalizeCustomBotBuildHandler",
      {
        code: DockerImageCode.fromImageAsset(
          path.join(__dirname, "../../../backend"),
          {
            platform: Platform.LINUX_AMD64,
            file: "lambda.Dockerfile",
            cmd: [
              "embedding_statemachine.bedrock_knowledge_base.finalize_custom_bot_build.handler",
            ],
            exclude: [...excludeDockerImage],
          }
        ),
        memorySize: 512,
        timeout: Duration.minutes(1),
        role: handlerRole,
        environment: {
          ACCOUNT: Stack.of(this).account,
          REGION: Stack.of(this).region,
          BEDROCK_REGION: props.bedrockRegion,
          CONVERSATION_TABLE_NAME: props.database.conversationTable.tableName,
          BOT_TABLE_NAME: props.database.botTable.tableName,
          TABLE_ACCESS_ROLE_ARN: props.database.tableAccessRole.roleArn,
        },
        logRetention: logs.RetentionDays.THREE_MONTHS,
      }
    );
    this._finalizeSharedKnowledgeBasesBuildHandler = new DockerImageFunction(
      this,
      "FinalizeSharedKnowledgeBasesBuildHandler",
      {
        code: DockerImageCode.fromImageAsset(
          path.join(__dirname, "../../../backend"),
          {
            platform: Platform.LINUX_AMD64,
            file: "lambda.Dockerfile",
            cmd: [
              "embedding_statemachine.bedrock_knowledge_base.finalize_shared_knowledge_bases_build.handler",
            ],
            exclude: [...excludeDockerImage],
          }
        ),
        memorySize: 512,
        timeout: Duration.minutes(1),
        role: handlerRole,
        environment: {
          ACCOUNT: Stack.of(this).account,
          REGION: Stack.of(this).region,
          BEDROCK_REGION: props.bedrockRegion,
          CONVERSATION_TABLE_NAME: props.database.conversationTable.tableName,
          BOT_TABLE_NAME: props.database.botTable.tableName,
          TABLE_ACCESS_ROLE_ARN: props.database.tableAccessRole.roleArn,
        },
        logRetention: logs.RetentionDays.THREE_MONTHS,
      }
    );

    this._synchronizeDataSourceHandler = new DockerImageFunction(this, "SynchronizeDataSourceHandler", {
      code: DockerImageCode.fromImageAsset(path.join(__dirname, "../../../backend"), {
        platform: Platform.LINUX_AMD64,
        file: "lambda.Dockerfile",
        cmd: [
          "embedding_statemachine.bedrock_knowledge_base.synchronize_data_source.handler",
        ],
        exclude: [...excludeDockerImage],
      }),
      memorySize: 512,
      timeout: Duration.minutes(15),
      environment: {
        ACCOUNT: Stack.of(this).account,
        REGION: Stack.of(this).region,
        BEDROCK_REGION: props.bedrockRegion,
        DOCUMENT_BUCKET: props.documentBucket.bucketName,
      },
      role: handlerRole,
      logRetention: logs.RetentionDays.THREE_MONTHS,
    });

    this._lockHandler = new DockerImageFunction(this, "LockHandler", {
      code: DockerImageCode.fromImageAsset(path.join(__dirname, "../../../backend"), {
        platform: Platform.LINUX_AMD64,
        file: "lambda.Dockerfile",
        cmd: [
          "embedding_statemachine.bedrock_knowledge_base.lock.handler",
        ],
        exclude: [...excludeDockerImage],
      }),
      memorySize: 512,
      timeout: Duration.minutes(1),
      environment: {
        ACCOUNT: Stack.of(this).account,
        REGION: Stack.of(this).region,
        BEDROCK_REGION: props.bedrockRegion,
        DOCUMENT_BUCKET: props.documentBucket.bucketName,
      },
      role: handlerRole,
      logRetention: logs.RetentionDays.THREE_MONTHS,
    });
  }

  private setupStateMachine(props: EmbeddingProps): sfn.StateMachine {
    // To build the information necessary for processing the embedded state machine, retrieve information about bots and shared Knowledge Bases from the database.
    const bootstrapStateMachine = new tasks.LambdaInvoke(this, "BootstrapStateMachine", {
      lambdaFunction: this._bootstrapStateMachineHandler,
      resultSelector: {
        QueuedBots: sfn.JsonPath.objectAt("$.Payload.QueuedBots"),
        SharedKnowledgeBases: sfn.JsonPath.objectAt("$.Payload.SharedKnowledgeBases"),
      },
    });

    const checkSyncSharedKnowledgeBasesRequired = new sfn.Choice(this, "CheckSyncSharedKnowledgeBasesRequired");

    // Acquire a distributed lock for shared Knowledge Bases.
    const acquireLockForSharedKnowledgeBases = this.createAcquireLockTask("ForSharedKnowledgeBases", {
      name: "shared-knowledge-bases",
      resultPath: "$.Lock",
    });

    // Release the acquired lock for shared Knowledge Bases.
    const releaseLockForSharedKnowledgeBasesOnFailed = this.createReleaseLockTask("ForSharedKnowledgeBasesOnFailed", {
      name: "shared-knowledge-bases",
      lockId: sfn.JsonPath.stringAt("$.Lock.LockId"),
    });
    const syncSharedKnowledgeBasesFailed = new sfn.Fail(this, "SyncSharedKnowledgeBasesFailed", {
      cause: "Shared knowledge bases sync failed",
    });
    const releaseLockFallback = (
      releaseLockForSharedKnowledgeBasesOnFailed
        .next(syncSharedKnowledgeBasesFailed)
    );

    const updateSyncStatusRunning = new tasks.LambdaInvoke(this, "UpdateSyncStatusRunning", {
      lambdaFunction: this._updateSyncStatusHandler,
      payload: sfn.TaskInput.fromObject({
        QueuedBots: sfn.JsonPath.objectAt("$.QueuedBots"),
        SyncStatus: "RUNNING",
      }),
      resultPath: sfn.JsonPath.DISCARD,
    });
    updateSyncStatusRunning.addCatch(releaseLockFallback, {
      resultPath: "$.Error",
    });

    const buildSharedKnowledgeBases = new tasks.CodeBuildStartBuild(this, "BuildSharedKnowledgeBases", {
      project: props.bedrockSharedKnowledgeBasesProject,
      integrationPattern: sfn.IntegrationPattern.RUN_JOB,
      environmentVariablesOverride: {
        SHARED_KNOWLEDGE_BASES: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: sfn.JsonPath.jsonToString(sfn.JsonPath.objectAt("$.SharedKnowledgeBases")),
        },
        // Bucket name provisioned by the bedrock stack
        BEDROCK_CLAUDE_CHAT_DOCUMENT_BUCKET_NAME: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: props.documentBucket.bucketName,
        },
        ENABLE_RAG_REPLICAS: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: props.enableRagReplicas.toString(),
        },
      },
      resultPath: sfn.JsonPath.DISCARD,
    });

    const passSharedKnowledgeBasesBuildError = new sfn.Pass(this, "PassSharedKnowledgeBasesBuildError", {
      parameters: {
        QueuedBots: sfn.JsonPath.objectAt("$.QueuedBots"),
        Lock: sfn.JsonPath.objectAt("$.Lock"),
        Error: sfn.JsonPath.stringAt("$.Error.Error"),
        Cause: sfn.JsonPath.stringToJson(sfn.JsonPath.stringAt("$.Error.Cause")),
      },
    });
    const updateSyncStatusFailedForSharedKnowledgeBasesBuild = new tasks.LambdaInvoke(this, "UpdateSyncStatusFailedForSharedKnowledgeBasesBuild", {
      lambdaFunction: this._updateSyncStatusHandler,
      payload: sfn.TaskInput.fromObject({
        QueuedBots: sfn.JsonPath.objectAt("$.QueuedBots"),
        SyncStatus: "FAILED",
        Build: sfn.JsonPath.objectAt("$.Cause.Build"),
      }),
      resultPath: sfn.JsonPath.DISCARD,
    });
    updateSyncStatusFailedForSharedKnowledgeBasesBuild.addCatch(releaseLockFallback, {
      resultPath: "$.Error",
    });

    const buildSharedKnowledgeBasesFallback = (
      passSharedKnowledgeBasesBuildError
        .next(updateSyncStatusFailedForSharedKnowledgeBasesBuild)
        .next(releaseLockFallback)
    );
    buildSharedKnowledgeBases.addCatch(buildSharedKnowledgeBasesFallback, {
      resultPath: "$.Error",
    })

    // Obtain the ID of the shared Knowledge Bases built by `BrChatSharedKbStack`, and update `knowledge_base_id` of the referring bots.
    const finalizeSharedKnowledgeBasesBuild = new tasks.LambdaInvoke(this, "FinalizeSharedKnowledgeBasesBuild", {
      lambdaFunction: this._finalizeSharedKnowledgeBasesBuildHandler,
      resultSelector: {
        QueuedBots: sfn.JsonPath.objectAt("$.Payload.QueuedBots"),
        SharedKnowledgeBases: sfn.JsonPath.objectAt("$.Payload.SharedKnowledgeBases"),
        DataSources: sfn.JsonPath.objectAt("$.Payload.DataSources"),
        Lock: sfn.JsonPath.objectAt("$.Payload.Lock"),
      },
    });

    const mapIngestionJobsForSharedKnowledgeBases = new sfn.Map(this, "MapIngestionJobsForSharedKnowledgeBases", {
      inputPath: "$.DataSources",
      resultPath: sfn.JsonPath.DISCARD,
      maxConcurrency: 1,
    });
    // Perform entire synchronization into the data source of shared Knowledge Bases.
    const ingestionJobForSharedKnowledgeBases = this.createIngestionTask("Shared", {});

    const updateSyncStatusFailedForSharedKnowledgeBases = new tasks.LambdaInvoke(this, "UpdateSyncStatusFailedForSharedKnowledgeBases", {
      lambdaFunction: this._updateSyncStatusHandler,
      payload: sfn.TaskInput.fromObject({
        QueuedBots: sfn.JsonPath.objectAt("$.QueuedBots"),
        SyncStatus: "FAILED",
      }),
      resultPath: sfn.JsonPath.DISCARD,
    })
    updateSyncStatusFailedForSharedKnowledgeBases.addCatch(releaseLockFallback, {
      resultPath: "$.Error",
    });

    const syncSharedKnowledgeBasesFallback = (
      updateSyncStatusFailedForSharedKnowledgeBases
        .next(releaseLockFallback)
    );
    finalizeSharedKnowledgeBasesBuild.addCatch(syncSharedKnowledgeBasesFallback, {
      resultPath: "$.Error",
    });
    mapIngestionJobsForSharedKnowledgeBases.addCatch(syncSharedKnowledgeBasesFallback, {
      resultPath: "$.Error",
    });

    // Release the acquired lock for shared Knowledge Bases.
    const releaseLockForSharedKnowledgeBases = this.createReleaseLockTask("ForSharedKnowledgeBases", {
      name: "shared-knowledge-bases",
      lockId: sfn.JsonPath.stringAt("$.Lock.LockId"),
    });

    const mapQueuedBots = new sfn.Map(this, "MapQueuedBots", {
      itemsPath: "$.QueuedBots",
      resultPath: sfn.JsonPath.DISCARD,
    });

    // Acquire a distributed lock for custom bots.
    const acquireLockForCustomBot = this.createAcquireLockTask("ForCustomBot", {
      name: sfn.JsonPath.format("custombot-{}", sfn.JsonPath.stringAt("$.BotId")),
      resultPath: "$.Lock",
    });

    const startCustomBotBuild = new tasks.CodeBuildStartBuild(this, "StartCustomBotBuild", {
      project: props.bedrockCustomBotProject,
      integrationPattern: sfn.IntegrationPattern.RUN_JOB,
      environmentVariablesOverride: {
        OWNER_USER_ID: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: sfn.JsonPath.stringAt("$.OwnerUserId"),
        },
        BOT_ID: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: sfn.JsonPath.stringAt("$.BotId"),
        },
        // Bucket name provisioned by the bedrock stack
        BEDROCK_CLAUDE_CHAT_DOCUMENT_BUCKET_NAME: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: props.documentBucket.bucketName,
        },
        // Source info e.g. file names, URLs, etc.
        KNOWLEDGE: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: sfn.JsonPath.jsonToString(sfn.JsonPath.objectAt("$.Knowledge")),
        },
        // Bedrock Knowledge Base configuration
        KNOWLEDGE_BASE: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: sfn.JsonPath.jsonToString(sfn.JsonPath.objectAt("$.KnowledgeBase")),
        },
        GUARDRAILS: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: sfn.JsonPath.jsonToString(sfn.JsonPath.objectAt("$.Guardrails")),
        },
        ENABLE_RAG_REPLICAS: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: props.enableRagReplicas.toString(),
        },
      },
      resultPath: sfn.JsonPath.DISCARD,
    });

    // Release the acquired lock for custom bots.
    const releaseLockForCustomBot = this.createReleaseLockTask("ForCustomBot", {
      name: sfn.JsonPath.format("custombot-{}", sfn.JsonPath.stringAt("$.BotId")),
      lockId: sfn.JsonPath.stringAt("$.Lock.LockId"),
    });
    const syncCustomBotSucceeded = new sfn.Succeed(this, "SyncCustomBotSucceeded");
    const syncCustomBotFinished = (
      releaseLockForCustomBot
        .next(syncCustomBotSucceeded)
    );

    const passCustomBotBuildError = new sfn.Pass(this, "PassCustomBotBuildError", {
      parameters: {
        OwnerUserId: sfn.JsonPath.stringAt("$.OwnerUserId"),
        BotId: sfn.JsonPath.stringAt("$.BotId"),
        Lock: sfn.JsonPath.objectAt("$.Lock"),
        Error: sfn.JsonPath.stringAt("$.Error.Error"),
        Cause: sfn.JsonPath.stringToJson(sfn.JsonPath.stringAt("$.Error.Cause")),
      },
    });
    const updateSyncStatusFailedForCustomBotBuild = new tasks.LambdaInvoke(this, "UpdateSyncStatusFailedForCustomBotBuild", {
      lambdaFunction: this._updateSyncStatusHandler,
      payload: sfn.TaskInput.fromObject({
        OwnerUserId: sfn.JsonPath.stringAt("$.OwnerUserId"),
        BotId: sfn.JsonPath.stringAt("$.BotId"),
        SyncStatus: "FAILED",
        Build: sfn.JsonPath.objectAt("$.Cause.Build"),
      }),
      resultPath: sfn.JsonPath.DISCARD,
    });
    updateSyncStatusFailedForCustomBotBuild.addCatch(syncCustomBotFinished, {
      resultPath: "$.Error",
    });

    const buildCustomBotFallback = (
      passCustomBotBuildError
        .next(updateSyncStatusFailedForCustomBotBuild)
        .next(syncCustomBotFinished)
    );

    startCustomBotBuild.addCatch(buildCustomBotFallback, {
      resultPath: "$.Error",
    });

    // Obtain the ID of the dedicated Knowledge Bases and Guardrails built by `BrChatKbStackXXX`, and update `knowledge_base_id` and `guardrail_arn` of the bot.
    const finalizeCustomBotBuild = new tasks.LambdaInvoke(this, "FinalizeCustomBotBuild", {
      lambdaFunction: this._finalizeCustomBotBuildHandler,
      resultSelector: {
        OwnerUserId: sfn.JsonPath.stringAt("$.Payload.OwnerUserId"),
        BotId: sfn.JsonPath.stringAt("$.Payload.BotId"),
        DataSources: sfn.JsonPath.objectAt("$.Payload.DataSources"),
        Lock: sfn.JsonPath.objectAt("$.Payload.Lock"),
      },
    });

    const mapIngestionJobsForCustomBot = new sfn.Map(this, "MapIngestionJobsForCustomBot", {
      inputPath: "$.DataSources",
      resultPath: sfn.JsonPath.DISCARD,
      maxConcurrency: 1,
    });
    // Perform direct ingestion or entire synchronization into the data source of dedicated Knowledge Bases.
    const ingestionJobForCustomBot = this.createIngestionTask("CustomBot", {});

    const updateSyncStatusFailedForCustomBot = new tasks.LambdaInvoke(this, "UpdateSyncStatusFailedForCustomBot", {
      lambdaFunction: this._updateSyncStatusHandler,
      payload: sfn.TaskInput.fromObject({
        OwnerUserId: sfn.JsonPath.stringAt("$.OwnerUserId"),
        BotId: sfn.JsonPath.stringAt("$.BotId"),
        SyncStatus: "FAILED",
      }),
      resultPath: sfn.JsonPath.DISCARD,
    });
    updateSyncStatusFailedForCustomBot.addCatch(syncCustomBotFinished, {
      resultPath: "$.Error",
    });

    const syncCustomBotFallback = (
      updateSyncStatusFailedForCustomBot
        .next(syncCustomBotFinished)
    );
    finalizeCustomBotBuild.addCatch(syncCustomBotFallback, {
      resultPath: "$.Error",
    });
    mapIngestionJobsForCustomBot.addCatch(syncCustomBotFallback, {
      resultPath: "$.Error",
    });

    const updateSyncStatusSucceeded = new tasks.LambdaInvoke(this, "UpdateSyncStatusSuccess", {
      lambdaFunction: this._updateSyncStatusHandler,
      payload: sfn.TaskInput.fromObject({
        OwnerUserId: sfn.JsonPath.stringAt("$.OwnerUserId"),
        BotId: sfn.JsonPath.stringAt("$.BotId"),
        SyncStatus: "SUCCEEDED",
        SyncStatusReason: "Knowledge base sync succeeded",
      }),
      resultPath: sfn.JsonPath.DISCARD,
    });
    updateSyncStatusSucceeded.addCatch(syncCustomBotFinished, {
      resultPath: "$.Error",
    });

    /**
     * Knowledge Base Synchronization State Machine
     * 
     * This state machine processes both Shared and Dedicated Knowledge Bases through two main flows:
     * 
     * 1. SharedKnowledgeBases Flow:
     *    - Executes when SharedKnowledgeBases != null
     *    - Handles full synchronization of shared Knowledge Bases
     *    - Processes bots without file diffs via global data source sync
     * 
     * 2. MapQueuedBots Flow:
     *    - Always executes (after SharedKnowledgeBases flow or standalone)
     *    - Processes each queued bot individually for:
     *      a) Dedicated bots: Creates KB + processes file diffs
     *      b) Shared bots with file diffs: Processes bot-specific file changes to shared KB
     *      c) Guardrails management for all bots
     * 
     * Why shared bots with file diffs use MapQueuedBots flow:
     * - File diffs contain bot-specific metadata (OwnerUserId, BotId)
     * - Requires bot-specific S3 path construction (user_id/bot_id/filename)
     * - Enables individual bot status tracking during ingestion
     */
    const definition = (
      bootstrapStateMachine
        .next(
          checkSyncSharedKnowledgeBasesRequired
            .when(sfn.Condition.isNotNull("$.SharedKnowledgeBases"), (
              // If there are updates to the shared Knowledge Base, build shared Knowledge Bases and synchronize data sources.
              acquireLockForSharedKnowledgeBases
                .next(updateSyncStatusRunning)
                .next(buildSharedKnowledgeBases)
                .next(finalizeSharedKnowledgeBasesBuild)
                .next(
                  mapIngestionJobsForSharedKnowledgeBases.itemProcessor(
                    ingestionJobForSharedKnowledgeBases
                  )
                )
                .next(releaseLockForSharedKnowledgeBases)
                .next(mapQueuedBots)
            ))
            .otherwise(
              // Otherwise, skip the processing related to shared Knowledge Bases.
              mapQueuedBots.itemProcessor(
                acquireLockForCustomBot
                  .next(startCustomBotBuild)
                  .next(finalizeCustomBotBuild)
                  .next(
                    mapIngestionJobsForCustomBot.itemProcessor(
                      ingestionJobForCustomBot
                    )
                  )
                  .next(updateSyncStatusSucceeded)
                  .next(syncCustomBotFinished)
              )
            )
        )
    );

    return new sfn.StateMachine(this, "StateMachine", {
      definitionBody: sfn.DefinitionBody.fromChainable(definition),
    });
  }

  private setupRemovalHandler(props: EmbeddingProps) {
    const removeHandlerRole = new iam.Role(this, "RemovalHandlerRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });
    removeHandlerRole.addToPolicy(
      // Assume the table access role for row-level access control.
      new iam.PolicyStatement({
        actions: ["sts:AssumeRole"],
        resources: [props.database.tableAccessRole.roleArn],
      })
    );
    removeHandlerRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          "cloudformation:DescribeStacks",
          "cloudformation:DescribeStackEvents",
          "cloudformation:DescribeStackResource",
          "cloudformation:DescribeStackResources",
          "cloudformation:DeleteStack",
        ],
        resources: [`*`],
      })
    );
    removeHandlerRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          "apigateway:GET",
          "apigateway:POST",
          "apigateway:PUT",
          "apigateway:DELETE",
        ],
        resources: [`arn:aws:apigateway:${Stack.of(this).region}::/*`],
      })
    );
    removeHandlerRole.addToPolicy(
      new iam.PolicyStatement({
        actions: [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ],
        resources: ["arn:aws:logs:*:*:*"],
      })
    );
    removeHandlerRole.addToPolicy(
      new iam.PolicyStatement({
        actions: ["secretsmanager:DeleteSecret"],
        resources: [
          `arn:aws:secretsmanager:${Stack.of(this).region}:${
            Stack.of(this).account
          }:secret:firecrawl/*/*`,
        ],
      })
    );
    props.database.botTable.grantStreamRead(removeHandlerRole);
    props.documentBucket.grantReadWrite(removeHandlerRole);

    const removalHandler = new DockerImageFunction(this, "BotRemovalHandler", {
      code: DockerImageCode.fromImageAsset(
        path.join(__dirname, "../../../backend"),
        {
          platform: Platform.LINUX_AMD64,
          file: "lambda.Dockerfile",
          cmd: ["app.bot_remove.handler"],
          exclude: [...excludeDockerImage],
        }
      ),
      timeout: Duration.minutes(1),
      environment: {
        ACCOUNT: Stack.of(this).account,
        REGION: Stack.of(this).region,
        BEDROCK_REGION: props.bedrockRegion,
        CONVERSATION_TABLE_NAME: props.database.conversationTable.tableName,
        BOT_TABLE_NAME: props.database.botTable.tableName,
        TABLE_ACCESS_ROLE_ARN: props.database.tableAccessRole.roleArn,
        DOCUMENT_BUCKET: props.documentBucket.bucketName,
      },
      role: removeHandlerRole,
      logRetention: logs.RetentionDays.THREE_MONTHS,
    });
    removalHandler.addEventSource(
      new DynamoEventSource(props.database.botTable, {
        startingPosition: lambda.StartingPosition.TRIM_HORIZON,
        batchSize: 1,
        retryAttempts: 2,
        filters: [
          {
            pattern: '{"eventName":["REMOVE"]}',
          },
        ],
      })
    );

    return removalHandler;
  }

  private createIngestionTask(idSuffix: string, {
    timeout = Duration.hours(12),
  }: {
    timeout?: Duration,
  }) {
    // Perform direct ingestion or entire synchronization into the data source
    const startIngestionJob = new tasks.LambdaInvoke(this, `StartIngestionJob${idSuffix}`, {
      lambdaFunction: this._synchronizeDataSourceHandler,
      payload: sfn.TaskInput.fromObject({
        Action: "Ingest",
        KnowledgeBaseId: sfn.JsonPath.stringAt("$.KnowledgeBaseId"),
        DataSourceId: sfn.JsonPath.stringAt("$.DataSourceId"),
        FilesDiffs: sfn.JsonPath.objectAt("$.FilesDiffs"),
      }),
      resultSelector: {
        KnowledgeBaseId: sfn.JsonPath.stringAt("$.Payload.KnowledgeBaseId"),
        DataSourceId: sfn.JsonPath.stringAt("$.Payload.DataSourceId"),
        DocumentsDiff: sfn.JsonPath.objectAt("$.Payload.DocumentsDiff"),
        IngestionJobId: sfn.JsonPath.stringAt("$.Payload.IngestionJobId"),
      },
      resultPath: "$.IngestionJob",
    });

    // Check for the completion of direct ingestion or entire synchronization.
    const checkIngestionJob = new tasks.LambdaInvoke(this, `CheckIngestionJob${idSuffix}`, {
      lambdaFunction: this._synchronizeDataSourceHandler,
      payload: sfn.TaskInput.fromObject({
        Action: "Check",
        IngestionJob: sfn.JsonPath.objectAt("$.IngestionJob"),
      }),
      resultPath: sfn.JsonPath.DISCARD,
    });

    const ingestionComplete = new sfn.Pass(this, `IngestionComplete${idSuffix}`);
    return startIngestionJob
      .next(
        checkIngestionJob.addRetry({
          interval: Duration.seconds(15),
          maxAttempts: timeout.toSeconds() / 15,
          backoffRate: 1,
          errors: [
            'RetryException',
          ],
        }).addCatch(ingestionComplete, {
          resultPath: sfn.JsonPath.stringAt('$.Error'),
        })
      ).next(ingestionComplete)
  }

  private createAcquireLockTask(idSuffix: string, {
    name,
    owner = sfn.JsonPath.executionName,
    timeout = Duration.hours(12),
    resultPath,
  }: {
    name: string;
    owner?: string;
    timeout?: Duration;
    resultPath?: string;
  }) {
    // Acquire a distributed lock.
    return new tasks.LambdaInvoke(this, `AcquireLock${idSuffix}`, {
      lambdaFunction: this._lockHandler,
      payload: sfn.TaskInput.fromObject({
        Action: "Acquire",
        LockName: name,
        Owner: owner,
      }),
      resultSelector: {
        LockId: sfn.JsonPath.stringAt("$.Payload.LockId"),
      },
      resultPath: resultPath,
    }).addRetry({
      interval: Duration.seconds(15),
      maxAttempts: timeout.toSeconds() / 15,
      backoffRate: 1,
      errors: [
        'RetryException',
      ],
    });
  }

  private createReleaseLockTask(idSuffix: string, {
    name,
    lockId,
  }: {
    name: string;
    lockId: string;
  }) {
    // Release the acquired lock.
    return new tasks.LambdaInvoke(this, `ReleaseLock${idSuffix}`, {
      lambdaFunction: this._lockHandler,
      payload: sfn.TaskInput.fromObject({
        Action: "Release",
        LockName: name,
        LockId: lockId,
      }),
      resultPath: sfn.JsonPath.DISCARD,
    }).addRetry({
      maxAttempts: 5,
      errors: [
        'RetryException',
      ],
    });
  }
}
