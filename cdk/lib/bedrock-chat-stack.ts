import { CfnOutput, RemovalPolicy, StackProps, IgnoreMode } from "aws-cdk-lib";
import {
  BlockPublicAccess,
  Bucket,
  BucketEncryption,
  HttpMethods,
  ObjectOwnership,
} from "aws-cdk-lib/aws-s3";
import { CloudFrontWebDistribution } from "aws-cdk-lib/aws-cloudfront";
import { Construct } from "constructs";
import { Auth } from "./constructs/auth";
import { Api } from "./constructs/api";
import { Database } from "./constructs/database";
import { Frontend } from "./constructs/frontend";
import { WebSocket } from "./constructs/websocket";
import * as cdk from "aws-cdk-lib";
import { Embedding } from "./constructs/embedding";
import { UsageAnalysis } from "./constructs/usage-analysis";
import { TIdentityProvider, identityProvider } from "./utils/identity-provider";
import { ApiPublishCodebuild } from "./constructs/api-publish-codebuild";
import { WebAclForPublishedApi } from "./constructs/webacl-for-published-api";
import * as s3deploy from "aws-cdk-lib/aws-s3-deployment";
import * as logs from "aws-cdk-lib/aws-logs";
import * as path from "path";
import { BedrockCustomBotCodebuild } from "./constructs/bedrock-custom-bot-codebuild";
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as cw_actions from 'aws-cdk-lib/aws-cloudwatch-actions';
import { BaseDashboard } from './constructs/monitoring/base-dashboard';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export interface BedrockChatStackProps extends StackProps {
  readonly bedrockRegion: string;
  readonly webAclId: string;
  readonly identityProviders: TIdentityProvider[];
  readonly userPoolDomainPrefix: string;
  readonly publishedApiAllowedIpV4AddressRanges: string[];
  readonly publishedApiAllowedIpV6AddressRanges: string[];
  readonly allowedSignUpEmailDomains: string[];
  readonly autoJoinUserGroups: string[];
  readonly enableMistral: boolean;
  readonly selfSignUpEnabled: boolean;
  readonly enableIpV6: boolean;
  readonly documentBucket: Bucket;
  readonly useStandbyReplicas: boolean;
  readonly enableBedrockCrossRegionInference: boolean;
  readonly enableLambdaSnapStart: boolean;
  readonly alternateDomainName?: string;
  readonly hostedZoneId?: string;
}

export class BedrockChatStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: BedrockChatStackProps) {
    super(scope, id, {
      description: "Bedrock Chat Stack (uksb-1tupboc46)",
      ...props,
    });

    const idp = identityProvider(props.identityProviders);

    const accessLogBucket = new Bucket(this, "AccessLogBucket", {
      encryption: BucketEncryption.S3_MANAGED,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      objectOwnership: ObjectOwnership.OBJECT_WRITER,
      autoDeleteObjects: true,
    });

    // Bucket for source code
    const sourceBucket = new Bucket(this, "SourceBucketForCodeBuild", {
      encryption: BucketEncryption.S3_MANAGED,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      objectOwnership: ObjectOwnership.OBJECT_WRITER,
      autoDeleteObjects: true,
      serverAccessLogsBucket: accessLogBucket,
      serverAccessLogsPrefix: "SourceBucketForCodeBuild",
    });
    new s3deploy.BucketDeployment(this, "SourceDeploy", {
      sources: [
        s3deploy.Source.asset(path.join(__dirname, "../../"), {
          ignoreMode: IgnoreMode.GIT,
          exclude: [
            "**/node_modules/**",
            "**/dist/**",
            "**/dev-dist/**",
            "**/.venv/**",
            "**/__pycache__/**",
            "**/cdk.out/**",
            "**/.vscode/**",
            "**/.DS_Store/**",
            "**/.git/**",
            "**/.github/**",
            "**/.mypy_cache/**",
            "**/examples/**",
            "**/docs/**",
            "**/.env",
            "**/.env.local",
            "**/.gitignore",
            "**/test/**",
            "**/tests/**",
            "**/backend/embedding_statemachine/pdf_ai_ocr/**",
            "**/backend/guardrails/**",
          ],
        }),
      ],
      destinationBucket: sourceBucket,
      logRetention: logs.RetentionDays.THREE_MONTHS,
    });
    // CodeBuild used for api publication
    const apiPublishCodebuild = new ApiPublishCodebuild(
      this,
      "ApiPublishCodebuild",
      {
        sourceBucket,
      }
    );
    // CodeBuild used for KnowledgeBase
    const bedrockCustomBotCodebuild = new BedrockCustomBotCodebuild(
      this,
      "BedrockKnowledgeBaseCodebuild",
      {
        sourceBucket,
      }
    );

    const frontend = new Frontend(this, "Frontend", {
      accessLogBucket,
      webAclId: props.webAclId,
      enableMistral: props.enableMistral,
      enableIpV6: props.enableIpV6,
      alternateDomainName: props.alternateDomainName,
      hostedZoneId: props.hostedZoneId,
    });

    const auth = new Auth(this, "Auth", {
      origin: frontend.getOrigin(),
      userPoolDomainPrefixKey: props.userPoolDomainPrefix,
      idp,
      allowedSignUpEmailDomains: props.allowedSignUpEmailDomains,
      autoJoinUserGroups: props.autoJoinUserGroups,
      selfSignUpEnabled: props.selfSignUpEnabled,
    });
    const largeMessageBucket = new Bucket(this, "LargeMessageBucket", {
      encryption: BucketEncryption.S3_MANAGED,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      objectOwnership: ObjectOwnership.OBJECT_WRITER,
      autoDeleteObjects: true,
      serverAccessLogsBucket: accessLogBucket,
      serverAccessLogsPrefix: "LargeMessageBucket",
    });

    const database = new Database(this, "Database", {
      // Enable PITR to export data to s3
      pointInTimeRecovery: true,
    });

    const usageAnalysis = new UsageAnalysis(this, "UsageAnalysis", {
      accessLogBucket,
      sourceDatabase: database,
    });

    const backendApi = new Api(this, "BackendApi", {
      database: database.table,
      ltiDataTable: database.ltiDataTable,
      auth,
      bedrockRegion: props.bedrockRegion,
      tableAccessRole: database.tableAccessRole,
      documentBucket: props.documentBucket,
      apiPublishProject: apiPublishCodebuild.project,
      bedrockCustomBotProject: bedrockCustomBotCodebuild.project,
      usageAnalysis,
      largeMessageBucket,
      botsMetadataTableArn: database.botsMetadataTableArn,
      botsMetadataConfigTableArn: database.botsMetadataConfigTableNameArn,
      botsMetadataConfigTableName: database.botsMetadataConfigTable.tableName,
      enableMistral: props.enableMistral,
      enableBedrockCrossRegionInference:
        props.enableBedrockCrossRegionInference,
      enableLambdaSnapStart: props.enableLambdaSnapStart,
      frontendURL: frontend.getOrigin(),
    });
    props.documentBucket.grantReadWrite(backendApi.handler);

    // For streaming response
    const websocket = new WebSocket(this, "WebSocket", {
      accessLogBucket,
      database: database.table,
      tableAccessRole: database.tableAccessRole,
      websocketSessionTable: database.websocketSessionTable,
      auth,
      bedrockRegion: props.bedrockRegion,
      largeMessageBucket,
      documentBucket: props.documentBucket,
      enableMistral: props.enableMistral,
      enableBedrockCrossRegionInference:
        props.enableBedrockCrossRegionInference,
      enableLambdaSnapStart: props.enableLambdaSnapStart,
      botsMetadataConfigTableName: database.botsMetadataConfigTable.tableName,
      ltiDataTableName: database.ltiDataTable.tableName,
      botsMetadataTableArn: database.botsMetadataTableArn,
      botsMetadataTable: database.botsMetadataTable,
      botsMetadataConfigTable: database.botsMetadataConfigTable,
    });
    frontend.buildViteApp({
      backendApiEndpoint: backendApi.api.apiEndpoint,
      webSocketApiEndpoint: websocket.apiEndpoint,
      userPoolDomainPrefix: props.userPoolDomainPrefix,
      enableMistral: props.enableMistral,
      auth,
      idp,
    });

    const cloudFrontWebDistribution = frontend.cloudFrontWebDistribution.node
      .defaultChild as CloudFrontWebDistribution;
    props.documentBucket.addCorsRule({
      allowedMethods: [HttpMethods.PUT],
      allowedOrigins: [
        `https://${cloudFrontWebDistribution.distributionDomainName}`,
        "http://localhost:5173",
        "*",
      ],
      allowedHeaders: ["*"],
      maxAge: 3000,
    });

    const embedding = new Embedding(this, "Embedding", {
      bedrockRegion: props.bedrockRegion,
      database: database.table,
      tableAccessRole: database.tableAccessRole,
      documentBucket: props.documentBucket,
      bedrockCustomBotProject: bedrockCustomBotCodebuild.project,
      useStandbyReplicas: props.useStandbyReplicas,
    });

    // WebAcl for published API
    const webAclForPublishedApi = new WebAclForPublishedApi(
      this,
      "WebAclForPublishedApi",
      {
        allowedIpV4AddressRanges: props.publishedApiAllowedIpV4AddressRanges,
        allowedIpV6AddressRanges: props.publishedApiAllowedIpV6AddressRanges,
      }
    );

    new CfnOutput(this, "DocumentBucketName", {
      value: props.documentBucket.bucketName,
    });
    new CfnOutput(this, "FrontendURL", {
      value: frontend.getOrigin(),
    });

    // Outputs for API publication
    new CfnOutput(this, "PublishedApiWebAclArn", {
      value: webAclForPublishedApi.webAclArn,
      exportName: "PublishedApiWebAclArn",
    });
    new CfnOutput(this, "ConversationTableName", {
      value: database.table.tableName,
      exportName: "BedrockClaudeChatConversationTableName",
    });
    new CfnOutput(this, "LtiDataTable", {
      value: database.ltiDataTable.tableName,
      exportName: "BedrockClaudeChatLtiDataTableName",
    });
    new CfnOutput(this, "TableAccessRoleArn", {
      value: database.tableAccessRole.roleArn,
      exportName: "BedrockClaudeChatTableAccessRoleArn",
    });
    new CfnOutput(this, "LargeMessageBucketName", {
      value: largeMessageBucket.bucketName,
      exportName: "BedrockClaudeChatLargeMessageBucketName",
    });

    // --- Instantiate Monitoring Dashboards ---

    // Service Health Dashboard (Phase 1 + Async + Refinements)
    new BaseDashboard(this, 'ServiceHealthDashboard', {
      // Phase 1 Props
      httpApi: backendApi.api,
      apiLambdaHandler: backendApi.handler,
      webSocketHandler: websocket.handler,
      conversationTable: database.table,
      botsMetadataTable: database.botsMetadataTable,
      dashboardNamePrefix: 'Qikr',
      // Phase 2 Props
      s3ExporterLambda: usageAnalysis.exportHandler,
      embeddingStateMachine: embedding.stateMachine,
      knowledgeBaseCodeBuild: bedrockCustomBotCodebuild.project,
      embeddingPipe: embedding.pipe,
      embeddingPipeRole: embedding.pipeRole,
      apiLambdaLogGroup: (backendApi.handler as lambda.Function).logGroup,
      webSocketLogGroup: websocket.handler ? (websocket.handler as lambda.Function).logGroup : undefined,
      codeBuildLogGroup: bedrockCustomBotCodebuild.logGroup,
      s3ExporterLogGroup: (usageAnalysis.exportHandler as lambda.Function).logGroup,
      // Added Props for Athena, S3
      athenaWorkgroupName: usageAnalysis.workgroupName,
      ddbExportBucket: usageAnalysis.ddbBucket,
      knowledgeBaseBucket: props.documentBucket, // Using the stack input documentBucket
      queryResultBucket: usageAnalysis.resultOutputBucket,
      botsBucket: usageAnalysis.botsBucket,
    });
  }
}
