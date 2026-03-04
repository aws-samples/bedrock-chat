import { CfnOutput, Duration, RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambdaNodeJs from 'aws-cdk-lib/aws-lambda-nodejs';
import {
  VectorBucket,
  VectorIndex,
  VectorIndexDistanceMetric,
} from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/s3vectors";
import * as s3 from "aws-cdk-lib/aws-s3";
import { BedrockFoundationModel, CustomTransformation } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock";
import { ChunkingStrategy } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock/data-sources/chunking";
import { S3DataSource } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock/data-sources/s3-data-source";
import { ParsingStrategy } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock/data-sources/parsing";

import {
  VectorKnowledgeBase,
} from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock";

import * as path from "path";

interface BedrockSharedKnowledgeBasesStackProps extends StackProps {
  // Base configuration
  readonly documentBucketName: string;
  readonly enableRagReplicas?: boolean;

  readonly knowledgeBases: Omit<BedrockKnowledgeBaseProps, "documentBucket" | "enableRagReplicas">[];
}

export class BedrockSharedKnowledgeBasesStack extends Stack {
  constructor(scope: Construct, id: string, props: BedrockSharedKnowledgeBasesStackProps) {
    super(scope, id, props);

    const bucket = s3.Bucket.fromBucketName(
      this,
      props.documentBucketName,
      props.documentBucketName
    );

    props.knowledgeBases.forEach(knowledgeBase => {
      const hash = knowledgeBase.knowledgeBaseHash;
      const sharedKnowledgeBase = new SharedKnowledgeBase(this, `KnowledgeBase${hash}`, {
        documentBucket: bucket,
        enableRagReplicas: props.enableRagReplicas,
        ...knowledgeBase,
      });
      new CfnOutput(this, `KnowledgeBaseId${hash}`, {
        value: sharedKnowledgeBase.kb.knowledgeBaseId,
      });
      new CfnOutput(this, `KnowledgeBaseArn${hash}`, {
        value: sharedKnowledgeBase.kb.knowledgeBaseArn,
      });

      // This output is used by Sfn to synchronize KB data.
      new CfnOutput(this, `DataSource${hash}0`, {
        value: sharedKnowledgeBase.dataSource.dataSourceId,
      });
    });
  }
}

interface BedrockKnowledgeBaseProps {
  // Base configuration
  readonly documentBucket: s3.IBucket;
  readonly enableRagReplicas?: boolean; // unused with S3 Vectors

  // Knowledge base configuration
  readonly knowledgeBaseHash: string;
  readonly embeddingsModel: BedrockFoundationModel;
  readonly parsingModel?: BedrockFoundationModel;
  readonly instruction?: string;

  // Chunking configuration
  readonly chunkingStrategy: ChunkingStrategy;
  readonly maxTokens?: number;
  readonly overlapPercentage?: number;
}

class SharedKnowledgeBase extends Construct {
  readonly kb: VectorKnowledgeBase;
  readonly dataSource: S3DataSource;

  constructor(scope: Construct, id: string, props: BedrockKnowledgeBaseProps) {
    super(scope, id);

    const vectorBucket = new VectorBucket(this, "VectorBucket");
    const vectorIndex = new VectorIndex(this, "VectorIndex", {
      vectorBucket: vectorBucket,
      dimension: props.embeddingsModel.vectorDimensions!,
      distanceMetric: VectorIndexDistanceMetric.COSINE,
    });

    const tempBucket = new s3.Bucket(this, 'TempBucket', {
      enforceSSL: true,
      autoDeleteObjects: true,
      removalPolicy: RemovalPolicy.DESTROY,
    });
    const transformationFunction = new lambdaNodeJs.NodejsFunction(this, 'TransformationFunction', {
      entry: path.resolve(__dirname, '../lambda/knowledge-base-custom-transformation/index.ts'),
      depsLockFilePath: path.resolve(__dirname, '../lambda/knowledge-base-custom-transformation/package-lock.json'),

      timeout: Duration.minutes(15),
    });
    props.documentBucket.grantReadWrite(transformationFunction);
    tempBucket.grantReadWrite(transformationFunction);

    this.kb = new VectorKnowledgeBase(this, "KnowledgeBase", {
      embeddingsModel: props.embeddingsModel,
      vectorStore: vectorIndex,
      instruction: props.instruction,
    });
    tempBucket.grantReadWrite(this.kb.role);

    props.documentBucket.grantRead(this.kb.role);
    this.dataSource = new S3DataSource(this, `DocumentBucketDataSource`, {
      bucket: props.documentBucket,
      knowledgeBase: this.kb,
      dataSourceName: props.documentBucket.bucketName,
      chunkingStrategy: props.chunkingStrategy,
      parsingStrategy: props.parsingModel
        ? ParsingStrategy.foundationModel({
            parsingModel: props.parsingModel,
          })
        : undefined,
      customTransformation: CustomTransformation.lambda({
        lambdaFunction: transformationFunction,
        s3BucketUri: tempBucket.s3UrlForObject(),
      }),
    });
  }
}
