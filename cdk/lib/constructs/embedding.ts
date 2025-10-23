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
  }

  private setupStateMachine(props: EmbeddingProps): sfn.StateMachine {
    const bootstrapStateMachine = new tasks.LambdaInvoke(this, "BootstrapStateMachine", {
      lambdaFunction: this._bootstrapStateMachineHandler,
      resultSelector: {
        QueuedBots: sfn.JsonPath.objectAt("$.Payload.QueuedBots"),
        SharedKnowledgeBases: sfn.JsonPath.objectAt("$.Payload.SharedKnowledgeBases"),
      },
    });

    const buildSharedKnowledgeBases = new tasks.CodeBuildStartBuild(this, "BuildSharedKnowledgeBases", {
      project: props.bedrockSharedKnowledgeBasesProject,
      integrationPattern: sfn.IntegrationPattern.RUN_JOB,
      environmentVariablesOverride: {
        SHARED_KNOWLEDGE_BASES: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: sfn.JsonPath.stringAt("States.JsonToString($.SharedKnowledgeBases.KnowledgeBases)"),
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
      resultPath: "$.Build",
    });
    // buildSharedKnowledgeBases.addCatch(fallback);

    const updateSyncStatusRunning = this.createUpdateSyncStatusTask(
      "UpdateSyncStatusRunning",
      "RUNNING"
    );

    const updateSyncStatusSucceeded = this.createUpdateSyncStatusTask(
      "UpdateSyncStatusSuccess",
      "SUCCEEDED",
      "Knowledge base sync succeeded"
    );

    const finalizeSharedKnowledgeBasesBuild = new tasks.LambdaInvoke(this, "FinalizeSharedKnowledgeBasesBuild", {
      lambdaFunction: this._finalizeSharedKnowledgeBasesBuildHandler,
      resultSelector: {
        DataSources: sfn.JsonPath.objectAt("$.Payload.DataSources"),
      },
      resultPath: "$.StackOutput",
    });
    // finalizeSharedKnowledgeBasesBuild.addCatch(fallback);

    const dataSourceSynchronizationForSharedKnowledgeBases = this.createDataSourceSynchronizationTask("Shared");

    const mapIngestionJobsForSharedKnowledgeBases = new sfn.Map(this, "MapIngestionJobsForSharedKnowledgeBases", {
      inputPath: "$.StackOutput.DataSources",
      resultPath: sfn.JsonPath.DISCARD,
      maxConcurrency: 1,
    }).itemProcessor(
      dataSourceSynchronizationForSharedKnowledgeBases
    );

    const mapQueuedBots = new sfn.Map(this, "MapQueuedBots", {
      itemsPath: "$.QueuedBots",
    });

    const updateSyncStatusFailedForDedicated = new tasks.LambdaInvoke(this, "UpdateSyncStatusFailedForDedicated", {
      lambdaFunction: this._updateSyncStatusHandler,
      payload: sfn.TaskInput.fromObject({
        cause: sfn.JsonPath.stringAt("$.Cause"),
      }),
      resultPath: sfn.JsonPath.DISCARD,
    });

    const startCustomBotBuild = new tasks.CodeBuildStartBuild(
      this,
      "StartCustomBotBuild",
      {
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
            value: sfn.JsonPath.stringAt(
              "States.JsonToString($.Knowledge)"
            ),
          },
          // Bedrock Knowledge Base configuration
          KNOWLEDGE_BASE: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: sfn.JsonPath.stringAt(
              "States.JsonToString($.KnowledgeBase)"
            ),
          },
          GUARDRAILS: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: sfn.JsonPath.stringAt(
              "States.JsonToString($.Guardrails)"
            ),
          },
          ENABLE_RAG_REPLICAS: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: props.enableRagReplicas.toString(),
          },
        },
        resultPath: "$.Build",
      }
    );
    startCustomBotBuild.addCatch(updateSyncStatusFailedForDedicated);

    const finalizeCustomBotBuild = new tasks.LambdaInvoke(this, "FinalizeCustomBotBuild", {
      lambdaFunction: this._finalizeCustomBotBuildHandler,
      resultSelector: {
        DataSources: sfn.JsonPath.objectAt("$.Payload.DataSources"),
        Bots: sfn.JsonPath.objectAt("$.Payload.Bots"),
      },
      resultPath: "$.StackOutput",
    });
    finalizeCustomBotBuild.addCatch(updateSyncStatusFailedForDedicated);

    const dataSourceSynchronizationForDedicatedKnowledgeBases = this.createDataSourceSynchronizationTask("Dedicated");

    const mapIngestionJobs = new sfn.Map(this, "MapIngestionJobs", {
      inputPath: "$.StackOutput.DataSources",
      resultPath: sfn.JsonPath.DISCARD,
      maxConcurrency: 1,
    }).itemProcessor(
      dataSourceSynchronizationForDedicatedKnowledgeBases
    );

    const definition = bootstrapStateMachine
      .next(buildSharedKnowledgeBases)
      .next(finalizeSharedKnowledgeBasesBuild)
      .next(mapIngestionJobsForSharedKnowledgeBases)
      .next(
        mapQueuedBots.itemProcessor(
          updateSyncStatusRunning
            .next(startCustomBotBuild)
            .next(finalizeCustomBotBuild)
            .next(mapIngestionJobs)
            .next(updateSyncStatusSucceeded)
        )
      )

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

  private createUpdateSyncStatusTask(
    id: string,
    syncStatus: string,
    syncStatusReason?: string,
    lastExecIdPath?: string
  ): tasks.LambdaInvoke {
    const payload: { [key: string]: any } = {
      "user_id.$": "$.OwnerUserId",
      "bot_id.$": "$.BotId",
      sync_status: syncStatus,
      sync_status_reason: syncStatusReason || "",
    };

    if (lastExecIdPath) {
      payload["last_exec_id.$"] = lastExecIdPath;
    }

    return new tasks.LambdaInvoke(this, id, {
      lambdaFunction: this._updateSyncStatusHandler,
      payload: sfn.TaskInput.fromObject(payload),
      resultPath: sfn.JsonPath.DISCARD,
    });
  }

  private createDataSourceSynchronizationTask(name: string): sfn.IChainable {
    const startIngestionJob = new tasks.LambdaInvoke(this, `StartIngestionJob${name}`, {
      lambdaFunction: this._synchronizeDataSourceHandler,
      payload: sfn.TaskInput.fromObject({
        Action: "Ingest",
        KnowledgeBaseId: sfn.JsonPath.stringAt("$.KnowledgeBaseId"),
        DataSourceId: sfn.JsonPath.stringAt("$.DataSourceId"),
        Files: sfn.JsonPath.objectAt("$.Files"),
      }),
      resultSelector: {
        KnowledgeBaseId: sfn.JsonPath.stringAt("$.Payload.KnowledgeBaseId"),
        DataSourceId: sfn.JsonPath.stringAt("$.Payload.DataSourceId"),
        Files: sfn.JsonPath.objectAt("$.Payload.Files"),
        IngestionJobId: sfn.JsonPath.stringAt("$.Payload.IngestionJobId"),
      },
      resultPath: "$.IngestionJob",
    });

    const checkIngestionJob = new tasks.LambdaInvoke(this, `CheckIngestionJob${name}`, {
      lambdaFunction: this._synchronizeDataSourceHandler,
      payload: sfn.TaskInput.fromObject({
        Action: "Check",
        IngestionJob: sfn.JsonPath.objectAt("$.IngestionJob"),
      }),
      resultPath: sfn.JsonPath.DISCARD,
    });

    const ingestionComplete = new sfn.Pass(this, `IngestionComplete${name}`);
    return startIngestionJob
      .next(
        checkIngestionJob.addRetry({
          interval: Duration.seconds(15),
          maxAttempts: 12 * 60 * 60 / 15,
          backoffRate: 1,
          errors: [
            'RetryException',
          ],
        }).addCatch(ingestionComplete, {
          resultPath: sfn.JsonPath.stringAt('$.Error'),
        })
      ).next(ingestionComplete)
  }
}
