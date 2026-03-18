import { Construct } from "constructs";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as lambdaEventSources from "aws-cdk-lib/aws-lambda-event-sources";
import * as iam from "aws-cdk-lib/aws-iam";
import * as logs from "aws-cdk-lib/aws-logs";
import * as path from "path";
import { Duration, RemovalPolicy, Stack } from "aws-cdk-lib";
import { PythonFunction } from "@aws-cdk/aws-lambda-python-alpha";
import { generatePhysicalName } from "../utils/generate-physical-name";

export interface S3VectorsStoreProps {
  readonly envPrefix: string;
  readonly botTable: dynamodb.ITable;
  readonly conversationTable: dynamodb.ITable;
  readonly bedrockRegion: string;
}

export class S3VectorsStore extends Construct {
  readonly botVectorBucketName: string;
  readonly conversationVectorBucketName: string;

  constructor(scope: Construct, id: string, props: S3VectorsStoreProps) {
    super(scope, id);

    // Generate stable, unique bucket names (max 63 chars, lowercase, alphanumeric + hyphens)
    this.botVectorBucketName = generatePhysicalName(
      this,
      `${props.envPrefix}botvec`,
      { maxLength: 63, lower: true }
    );
    this.conversationVectorBucketName = generatePhysicalName(
      this,
      `${props.envPrefix}convvec`,
      { maxLength: 63, lower: true }
    );

    const region = Stack.of(this).region;

    // IAM role for the indexing Lambda
    const indexerRole = new iam.Role(this, "IndexerRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });
    indexerRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AWSLambdaBasicExecutionRole"
      )
    );

    // S3 Vectors permissions for the indexer
    indexerRole.addToPolicy(
      new iam.PolicyStatement({
        actions: [
          "s3vectors:CreateVectorBucket",
          "s3vectors:GetVectorBucket",
          "s3vectors:PutVectors",
          "s3vectors:DeleteVectors",
          "s3vectors:ListVectors",
        ],
        resources: ["*"],
      })
    );

    // Bedrock permissions for embedding generation
    indexerRole.addToPolicy(
      new iam.PolicyStatement({
        actions: ["bedrock:InvokeModel"],
        resources: [
          `arn:aws:bedrock:${props.bedrockRegion}::foundation-model/amazon.titan-embed-text-v2:0`,
        ],
      })
    );

    // Grant read access to DynamoDB tables for stream processing
    props.botTable.grantStreamRead(indexerRole);
    props.conversationTable.grantStreamRead(indexerRole);

    // Indexing Lambda — processes DynamoDB Stream events and writes to S3 Vectors
    // Uses a dedicated directory with no pyproject.toml so bundling only copies
    // the handler file (boto3 is already provided by the Lambda runtime).
    const indexerLambda = new PythonFunction(this, "Indexer", {
      entry: path.join(__dirname, "../../../backend/app/handlers/s3vectors_indexer_lambda"),
      index: "index.py",
      handler: "handler",
      runtime: lambda.Runtime.PYTHON_3_13,
      timeout: Duration.minutes(5),
      memorySize: 512,
      role: indexerRole,
      environment: {
        S3_VECTORS_BOT_BUCKET_NAME: this.botVectorBucketName,
        S3_VECTORS_CONVERSATION_BUCKET_NAME: this.conversationVectorBucketName,
        BEDROCK_REGION: props.bedrockRegion,
        REGION: region,
      },
      logRetention: logs.RetentionDays.ONE_WEEK,
    });

    // Trigger from bot table DynamoDB Streams (BOT items only)
    indexerLambda.addEventSource(
      new lambdaEventSources.DynamoEventSource(
        props.botTable as dynamodb.Table,
        {
          startingPosition: lambda.StartingPosition.LATEST,
          batchSize: 50,
          bisectBatchOnError: true,
          retryAttempts: 3,
          filters: [
            lambda.FilterCriteria.filter({
              dynamodb: {
                Keys: {
                  SK: { S: [{ prefix: "BOT" }] },
                },
              },
            }),
          ],
        }
      )
    );

    // Trigger from conversation table DynamoDB Streams (CONV items only)
    indexerLambda.addEventSource(
      new lambdaEventSources.DynamoEventSource(
        props.conversationTable as dynamodb.Table,
        {
          startingPosition: lambda.StartingPosition.LATEST,
          batchSize: 50,
          bisectBatchOnError: true,
          retryAttempts: 3,
          filters: [
            lambda.FilterCriteria.filter({
              dynamodb: {
                Keys: {
                  SK: { S: [{ prefix: "CONV" }] },
                },
              },
            }),
          ],
        }
      )
    );
  }

  /** Grant a role permission to query and list S3 Vectors (for the API Lambda). */
  public grantQueryAccess(role: iam.IRole): void {
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: [
          "s3vectors:QueryVectors",
          "s3vectors:ListVectors",
          "s3vectors:GetVectorBucket",
          "s3vectors:CreateVectorBucket",
          "s3vectors:PutVectors",
          "s3vectors:DeleteVectors",
        ],
        resources: ["*"],
      })
    );
    // Bedrock for generating query embeddings
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["bedrock:InvokeModel"],
        resources: ["*"],
      })
    );
  }
}
