import {
  CfnOutput,
  Duration,
  RemovalPolicy,
  Stack,
  StackProps,
} from "aws-cdk-lib";
import { Construct } from "constructs";
import {
  BlockPublicAccess,
  Bucket,
  BucketEncryption,
  ObjectOwnership,
} from "aws-cdk-lib/aws-s3";


interface BedrockRegionResourcesStackProps extends StackProps {
}

export class BedrockRegionResourcesStack extends Stack {
  readonly documentBucket: Bucket

  constructor(
    scope: Construct,
    id: string,
    props: BedrockRegionResourcesStackProps
  ) {
    super(scope, id, props);

    const prefix = Stack.of(this).region

    const accessLogBucket = new Bucket(this, `${prefix}AccessLogBucket`, {
      encryption: BucketEncryption.S3_MANAGED,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      objectOwnership: ObjectOwnership.OBJECT_WRITER,
      autoDeleteObjects: true,
    });

    this.documentBucket = new Bucket(this, `${prefix}DocumentBucket`, {
      encryption: BucketEncryption.S3_MANAGED,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      objectOwnership: ObjectOwnership.OBJECT_WRITER,
      autoDeleteObjects: true,
      serverAccessLogsBucket: accessLogBucket,
      serverAccessLogsPrefix: "DocumentBucket",
    });
    this.documentBucket.addLifecycleRule({
      prefix: ".temp/",
      expiration: Duration.days(1),
    });

    new CfnOutput(this, "DocumentBucketName", {
      value: this.documentBucket.bucketName,
    });

  } 
}
