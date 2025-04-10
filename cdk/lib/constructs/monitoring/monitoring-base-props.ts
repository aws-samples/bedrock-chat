import * as apigwv2 from 'aws-cdk-lib/aws-apigatewayv2';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import { CfnPipe } from 'aws-cdk-lib/aws-pipes';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';

/**
 * Base properties required by monitoring constructs.
 * Assumes Api construct exposes `api: apigwv2.HttpApi` and `handler: lambda.IFunction`.
 * Assumes Database construct exposes `table: dynamodb.ITable` (conversation)
 * and `botsMetadataTable: dynamodb.ITable`.
 */
export interface MonitoringBaseProps {
  // API Gateway - Assuming HttpApi (v2)
  readonly httpApi: apigwv2.IHttpApi;

  // Lambda Functions
  readonly apiLambdaHandler: lambda.IFunction;
  // Add other core function references here if needed in later phases

  // DynamoDB Tables
  readonly conversationTable: dynamodb.ITable;
  readonly botsMetadataTable: dynamodb.ITable;
  // readonly ltiDataTable?: dynamodb.ITable; // Add if needed later

  // Optional prefix for dashboards/alarms (e.g., 'Dev', 'Prod')
  readonly dashboardNamePrefix?: string;
}

/**
 * Properties specifically for the BaseDashboard construct, including
 * outputs from other monitoring components if needed later.
 */
export interface BaseDashboardProps extends MonitoringBaseProps {
    // This might receive alarm lists from other dashboard constructs later
    // For Phase 1, it primarily generates its own critical alarms.

    // --- Phase 2 Props ---
    readonly s3ExporterLambda?: lambda.IFunction; // Optional for incremental addition
    readonly embeddingStateMachine?: sfn.IStateMachine;
    readonly knowledgeBaseCodeBuild?: codebuild.IProject;
    readonly embeddingPipe?: CfnPipe; // Use CfnPipe as it was defined
    readonly embeddingPipeRole?: iam.IRole;
    readonly updateSyncStatusLambda?: lambda.IFunction; // Specific lambda from SF
    readonly webSocketHandler?: lambda.IFunction; // ADDED: Optional WebSocket handler

    // --- Configuration ---
    readonly anomalyDetectionStandardDeviation?: number; // Optional: std dev for anomaly detection (defaults to 2)

    // --- ADD THESE PROPERTIES ---
    readonly athenaWorkgroupName?: string; // Add Athena Workgroup name
    readonly ddbExportBucket?: s3.IBucket;   // Add the DDB Export S3 Bucket
    readonly knowledgeBaseBucket?: s3.IBucket; // Add the Knowledge Base source data S3 Bucket
    readonly queryResultBucket?: s3.IBucket; // Add Athena results bucket
    readonly botsBucket?: s3.IBucket;      // Add Bots analytics bucket
    // --- END OF ADDED PROPERTIES ---
}

/**
 * Properties for Alert Management components (used in later phases)
 */
export interface AlertManagerProps {
    readonly alertTopic: sns.ITopic;
    readonly criticalPageEmail?: string;
    readonly chatWebhookUrl?: string; // e.g., Slack/Teams
    readonly pagerDutyServiceKey?: string;
    readonly reportEmailAddress?: string;
    readonly reportRecipients?: string;
}

// Add other Prop interfaces for specific dashboards as needed... 