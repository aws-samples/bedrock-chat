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
  readonly removalHandler: IFunction;
  private _updateSyncStatusHandler: IFunction;
  private _bootstrapStateMachineHandler: IFunction;
  private _finalizeCustomBotBuildHandler: IFunction;
  private _finalizeSharedKnowledgeBasesBuildHandler: IFunction;
  private _stateMachine: sfn.StateMachine;
  private _removalHandler: IFunction;

  constructor(scope: Construct, id: string, props: EmbeddingProps) {
    super(scope, id);

    this.setupStateMachineHandlers(props)
      .setupStateMachine(props)
      .setupRemovalHandler(props);

    this.removalHandler = this._removalHandler;
  }

  private setupStateMachineHandlers(props: EmbeddingProps): this {
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
    return this;
  }

  private setupStateMachine(props: EmbeddingProps): this {
    const bootstrapStateMachine = new tasks.LambdaInvoke(this, "BootstrapStateMachine", {
      lambdaFunction: this._bootstrapStateMachineHandler,
      resultSelector: {
        Bots: sfn.JsonPath.objectAt("$.Payload.Bots"),
        SharedKnowledgeBases: sfn.JsonPath.objectAt("$.Payload.SharedKnowledgeBases"),
      },
    });

    const buildSharedKnowledgeBases = new tasks.CodeBuildStartBuild(this, "BuildSharedKnowledgeBases", {
      project: props.bedrockSharedKnowledgeBasesProject,
      integrationPattern: sfn.IntegrationPattern.RUN_JOB,
      environmentVariablesOverride: {
        SHARED_KNOWLEDGE_BASES: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: sfn.JsonPath.stringAt("States.JsonToString($.SharedKnowledgeBases)"),
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

    const updateSyncStatusRunning = this.createUpdateSyncStatusTask(
      "UpdateSyncStatusRunning",
      "RUNNING"
    );

    const updateSyncStatusSucceeded = this.createUpdateSyncStatusTask(
      "UpdateSyncStatusSuccess",
      "SUCCEEDED",
      "Knowledge base sync succeeded"
    );

    // const updateSyncStatusFailed = new tasks.LambdaInvoke(
    //   this,
    //   "UpdateSyncStatusFailed",
    //   {
    //     lambdaFunction: this._updateSyncStatusHandler,
    //     payload: sfn.TaskInput.fromObject({
    //       "cause.$": "$.Cause",
    //     }),
    //     resultPath: sfn.JsonPath.DISCARD,
    //   }
    // );

    // const fallback = updateSyncStatusFailed.next(
    //   new sfn.Fail(this, "Fail", {
    //     cause: "Knowledge base sync failed",
    //     error: "Knowledge base sync failed",
    //   })
    // );
    // buildSharedKnowledgeBases.addCatch(fallback);

    const finalizeSharedKnowledgeBasesBuild = new tasks.LambdaInvoke(this, "FinalizeSharedKnowledgeBasesBuild", {
      lambdaFunction: this._finalizeSharedKnowledgeBasesBuildHandler,
      resultSelector: {
        DataSources: sfn.JsonPath.objectAt("$.Payload.DataSources"),
      },
      resultPath: "$.StackOutput",
    });
    // finalizeSharedKnowledgeBasesBuild.addCatch(fallback);

    const startIngestionJobForSharedKnowledgeBases = new tasks.CallAwsServiceCrossRegion(this, "StartIngestionJobstartIngestionJobForSharedKnowledgeBases", {
      service: "bedrock-agent",
      action: "startIngestionJob",
      iamAction: "bedrock:StartIngestionJob",
      region: props.bedrockRegion,
      parameters: {
        dataSourceId: sfn.JsonPath.stringAt("$.DataSourceId"),
        knowledgeBaseId: sfn.JsonPath.stringAt("$.KnowledgeBaseId"),
      },
      // Ref: https://docs.aws.amazon.com/ja_jp/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-knowledge-base
      iamResources: [
        `arn:${Stack.of(this).partition}:bedrock:${props.bedrockRegion}:${
          Stack.of(this).account
        }:knowledge-base/*`,
      ],
      resultPath: "$.IngestionJob",
    });

    const getIngestionJobForSharedKnowledgeBases = new tasks.CallAwsServiceCrossRegion(this, "GetIngestionJobForSharedKnowledgeBases", {
      service: "bedrock-agent",
      action: "getIngestionJob",
      iamAction: "bedrock:GetIngestionJob",
      region: props.bedrockRegion,
      parameters: {
        dataSourceId: sfn.JsonPath.stringAt(
          "$.IngestionJob.ingestionJob.dataSourceId"
        ),
        knowledgeBaseId: sfn.JsonPath.stringAt(
          "$.IngestionJob.ingestionJob.knowledgeBaseId"
        ),
        ingestionJobId: sfn.JsonPath.stringAt(
          "$.IngestionJob.ingestionJob.ingestionJobId"
        ),
      },
      // Ref: https://docs.aws.amazon.com/ja_jp/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-knowledge-base
      iamResources: [
        `arn:${Stack.of(this).partition}:bedrock:${props.bedrockRegion}:${
          Stack.of(this).account
        }:knowledge-base/*`,
      ],
      resultPath: "$.IngestionJob",
    });

    const waitTaskForSharedKnowledgeBases = new sfn.Wait(this, "WaitSecondsForSharedKnowledgeBases", {
      time: sfn.WaitTime.duration(Duration.seconds(3)),
    });

    const checkIngestionJobStatusForSharedKnowledgeBases = new sfn.Choice(this, "CheckIngestionJobStatusForSharedKnowledgeBases")
      .when(
        sfn.Condition.stringEquals(
          "$.IngestionJob.ingestionJob.status",
          "COMPLETE"
        ),
        new sfn.Pass(this, "IngestionJobCompletedForSharedKnowledgeBases")
      )
      .when(
        sfn.Condition.stringEquals(
          "$.IngestionJob.ingestionJob.status",
          "FAILED"
        ),
        new sfn.Fail(this, "IngestionFailForSharedKnowledgeBases", {
          cause: "Ingestion job failed",
          error: "Ingestion job failed",
        })
        // new tasks.LambdaInvoke(this, "UpdateSyncStatusFailedForIngestion", {
        //   lambdaFunction: this._updateSyncStatusHandler,
        //   payload: sfn.TaskInput.fromObject({
        //     pk: sfn.JsonPath.stringAt("$.PK"),
        //     sk: sfn.JsonPath.stringAt("$.SK"),
        //     ingestion_job: sfn.JsonPath.stringAt("$.IngestionJob"),
        //   }),
        //   resultPath: sfn.JsonPath.DISCARD,
        // })
        // .next(
        //   new sfn.Fail(this, "IngestionFail", {
        //     cause: "Ingestion job failed",
        //     error: "Ingestion job failed",
        //   })
        // )
      )
      .otherwise(waitTaskForSharedKnowledgeBases.next(getIngestionJobForSharedKnowledgeBases));

    const mapIngestionJobsForSharedKnowledgeBases = new sfn.Map(this, "MapIngestionJobsForSharedKnowledgeBases", {
      inputPath: "$.StackOutput.DataSources",
      resultPath: sfn.JsonPath.DISCARD,
      maxConcurrency: 1,
    }).itemProcessor(
      startIngestionJobForSharedKnowledgeBases
        .next(getIngestionJobForSharedKnowledgeBases)
        .next(checkIngestionJobStatusForSharedKnowledgeBases)
    );

    const mapBots = new sfn.Map(this, "MapBots", {
      itemsPath: "$.Bots",
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
    // startCustomBotBuild.addCatch(fallback);

    const finalizeCustomBotBuild = new tasks.LambdaInvoke(this, "FinalizeCustomBotBuild", {
      lambdaFunction: this._finalizeCustomBotBuildHandler,
      resultSelector: {
        DataSources: sfn.JsonPath.objectAt("$.Payload.DataSources"),
        Bots: sfn.JsonPath.objectAt("$.Payload.Bots"),
      },
      resultPath: "$.StackOutput",
    });
    // finalizeCustomBotBuild.addCatch(fallback);

    const startIngestionJob = new tasks.CallAwsServiceCrossRegion(
      this,
      "StartIngestionJob",
      {
        service: "bedrock-agent",
        action: "startIngestionJob",
        iamAction: "bedrock:StartIngestionJob",
        region: props.bedrockRegion,
        parameters: {
          dataSourceId: sfn.JsonPath.stringAt("$.DataSourceId"),
          knowledgeBaseId: sfn.JsonPath.stringAt("$.KnowledgeBaseId"),
        },
        // Ref: https://docs.aws.amazon.com/ja_jp/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-knowledge-base
        iamResources: [
          `arn:${Stack.of(this).partition}:bedrock:${props.bedrockRegion}:${
            Stack.of(this).account
          }:knowledge-base/*`,
        ],
        resultPath: "$.IngestionJob",
      }
    );

    const getIngestionJob = new tasks.CallAwsServiceCrossRegion(
      this,
      "GetIngestionJob",
      {
        service: "bedrock-agent",
        action: "getIngestionJob",
        iamAction: "bedrock:GetIngestionJob",
        region: props.bedrockRegion,
        parameters: {
          dataSourceId: sfn.JsonPath.stringAt(
            "$.IngestionJob.ingestionJob.dataSourceId"
          ),
          knowledgeBaseId: sfn.JsonPath.stringAt(
            "$.IngestionJob.ingestionJob.knowledgeBaseId"
          ),
          ingestionJobId: sfn.JsonPath.stringAt(
            "$.IngestionJob.ingestionJob.ingestionJobId"
          ),
        },
        // Ref: https://docs.aws.amazon.com/ja_jp/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-knowledge-base
        iamResources: [
          `arn:${Stack.of(this).partition}:bedrock:${props.bedrockRegion}:${
            Stack.of(this).account
          }:knowledge-base/*`,
        ],
        resultPath: "$.IngestionJob",
      }
    );

    const waitTask = new sfn.Wait(this, "WaitSeconds", {
      time: sfn.WaitTime.duration(Duration.seconds(3)),
    });

    const checkIngestionJobStatus = new sfn.Choice(
      this,
      "CheckIngestionJobStatus"
    )
      .when(
        sfn.Condition.stringEquals(
          "$.IngestionJob.ingestionJob.status",
          "COMPLETE"
        ),
        new sfn.Pass(this, "IngestionJobCompleted")
      )
      .when(
        sfn.Condition.stringEquals(
          "$.IngestionJob.ingestionJob.status",
          "FAILED"
        ),
        new sfn.Fail(this, "IngestionFail", {
          cause: "Ingestion job failed",
          error: "Ingestion job failed",
        })
        // new tasks.LambdaInvoke(this, "UpdateSyncStatusFailedForIngestion", {
        //   lambdaFunction: this._updateSyncStatusHandler,
        //   payload: sfn.TaskInput.fromObject({
        //     pk: sfn.JsonPath.stringAt("$.PK"),
        //     sk: sfn.JsonPath.stringAt("$.SK"),
        //     ingestion_job: sfn.JsonPath.stringAt("$.IngestionJob"),
        //   }),
        //   resultPath: sfn.JsonPath.DISCARD,
        // })
        // .next(
        //   new sfn.Fail(this, "IngestionFail", {
        //     cause: "Ingestion job failed",
        //     error: "Ingestion job failed",
        //   })
        // )
      )
      .otherwise(waitTask.next(getIngestionJob));

    const mapIngestionJobs = new sfn.Map(this, "MapIngestionJobs", {
      inputPath: "$.StackOutput.DataSources",
      resultPath: sfn.JsonPath.DISCARD,
      maxConcurrency: 1,
    }).itemProcessor(
      startIngestionJob.next(getIngestionJob).next(checkIngestionJobStatus)
    );

    const definition = bootstrapStateMachine
      .next(buildSharedKnowledgeBases)
      .next(finalizeSharedKnowledgeBasesBuild)
      .next(mapIngestionJobsForSharedKnowledgeBases)
      .next(
        mapBots.itemProcessor(
          updateSyncStatusRunning
            .next(startCustomBotBuild)
            .next(finalizeCustomBotBuild)
            .next(mapIngestionJobs)
            .next(updateSyncStatusSucceeded)
        )
      )

    // const definition = extractFirstElement
    //   .next(updateSyncStatusRunning)
    //   .next(startCustomBotBuild)
    //   .next(finalizeCustomBotBuild)
    //   .next(mapIngestionJobs)
    //   .next(updateSyncStatusSucceeded);

    this._stateMachine = new sfn.StateMachine(this, "StateMachine", {
      definitionBody: sfn.DefinitionBody.fromChainable(definition),
    });
    return this;
  }

  private setupRemovalHandler(props: EmbeddingProps): this {
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

    this._removalHandler = new DockerImageFunction(this, "BotRemovalHandler", {
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
    this._removalHandler.addEventSource(
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

    return this;
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
}
