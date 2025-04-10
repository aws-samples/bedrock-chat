import { Construct } from "constructs";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as athena from "aws-cdk-lib/aws-athena";
import { CfnOutput, RemovalPolicy, Stack } from "aws-cdk-lib";
import * as glue from "@aws-cdk/aws-glue-alpha";
import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as python from "@aws-cdk/aws-lambda-python-alpha";
import * as path from "path";
import { Runtime } from "aws-cdk-lib/aws-lambda";
import { aws_glue } from "aws-cdk-lib";
import { Database } from "./database";
import * as iam from "aws-cdk-lib/aws-iam";
import * as logs from "aws-cdk-lib/aws-logs";

export interface UsageAnalysisProps {
  sourceDatabase: Database;
  accessLogBucket?: s3.Bucket;
}

export class UsageAnalysis extends Construct {
  public readonly database: glue.IDatabase;
  public readonly ddbExportTable: glue.ITable;
  public readonly ddbBucket: s3.IBucket;
  public readonly resultOutputBucket: s3.IBucket;
  public readonly workgroupName: string;
  public readonly workgroupArn: string;
  public readonly botsBucket: s3.IBucket;
  public readonly botsAnalyticsTable: glue.ITable;
  public readonly sourceDatabase: Database;
  public readonly exportHandler: python.PythonFunction;
  public readonly scheduleRule: events.Rule;

  constructor(scope: Construct, id: string, props: UsageAnalysisProps) {
    super(scope, id);

    this.sourceDatabase = props.sourceDatabase;

    const GLUE_DATABASE_NAME = `${Stack.of(
      this
    ).stackName.toLowerCase()}_usage_analysis`;
    const DDB_EXPORT_TABLE_NAME = "ddb_export";

    // Bucket to export DynamoDB data
    const ddbBucket = new s3.Bucket(this, "DdbBucket", {
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      objectOwnership: s3.ObjectOwnership.OBJECT_WRITER,
      autoDeleteObjects: true,
      serverAccessLogsBucket: props.accessLogBucket,
      serverAccessLogsPrefix: "DdbBucket",
    });

    // Bucket for Athena query results
    const queryResultBucket = new s3.Bucket(this, "QueryResultBucket", {
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      objectOwnership: s3.ObjectOwnership.OBJECT_WRITER,
      autoDeleteObjects: true,
      serverAccessLogsBucket: props.accessLogBucket,
      serverAccessLogsPrefix: "QueryResultBucket",
    });

    // Workgroup for Athena
    const wg = new athena.CfnWorkGroup(this, "Wg", {
      name: `${Stack.of(this).stackName.toLowerCase()}_wg`,
      description: "Workgroup for Athena",
      recursiveDeleteOption: true,
      workGroupConfiguration: {
        resultConfiguration: {
          outputLocation: `s3://${queryResultBucket.bucketName}`,
        },
      },
    });

    const database = new glue.Database(this, "Database", {
      databaseName: GLUE_DATABASE_NAME,
    });

    const imageSchemaType = glue.Schema.struct([
      {
        name: "CreateTime",
        type: glue.Schema.struct([{ name: "N", type: glue.Schema.STRING }]),
      },
      {
        name: "LastMessageId",
        type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
      },
      {
        name: "MessageMap",
        type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
      },
      {
        name: "IsLargeMessage",
        type: glue.Schema.struct([{ name: "BOOL", type: glue.Schema.BOOLEAN }]),
      },
      {
        name: "PK",
        type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
      },
      {
        name: "SK",
        type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
      },
      {
        name: "Title",
        type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
      },
      {
        name: "TotalPrice",
        type: glue.Schema.struct([
          { name: "N", type: glue.Schema.decimal(20, 10) },
        ]),
      },
      {
        name: "InputTokens",
        type: glue.Schema.struct([
          { name: "N", type: glue.Schema.decimal(20, 0) },
        ]),
      },
      {
        name: "OutputTokens",
        type: glue.Schema.struct([
          { name: "N", type: glue.Schema.decimal(20, 0) },
        ]),
      },
      {
        name: "BotId",
        type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
      },
      {
        name: "Metadata",
        type: glue.Schema.struct([{
          name: "L",
          type: glue.Schema.array(
            glue.Schema.struct([
              {
                name: "M",
                type: glue.Schema.struct([
                  { name: "key", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
                  { name: "value", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
                  { name: "type", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
                  { name: "parent_key", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) }
                ])
              }
            ])
          )
        }])
      },
      {
        name: "Feedback",
        type: glue.Schema.struct([{
          name: "M",
          type: glue.Schema.struct([
            { name: "rating", type: glue.Schema.struct([{ name: "N", type: glue.Schema.INTEGER }]) },
            { name: "category", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
            { name: "comment", type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]) },
            { name: "tags", type: glue.Schema.struct([{ 
              name: "L", 
              type: glue.Schema.array(glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]))
            }]) },
            { name: "metrics", type: glue.Schema.struct([{
              name: "M",
              type: glue.Schema.map(glue.Schema.STRING, glue.Schema.decimal(10, 2))
            }]) },
            { name: "created_at", type: glue.Schema.struct([{ name: "N", type: glue.Schema.decimal(20, 0) }]) }
          ])
        }])
      },
      {
        name: "Sentiment",
        type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
      },
      {
        name: "Topic",
        type: glue.Schema.struct([{ name: "S", type: glue.Schema.STRING }]),
      }
    ]);

    const ddbExportTable = new glue.S3Table(this, "DdbExportTable", {
      database,
      bucket: ddbBucket,
      tableName: DDB_EXPORT_TABLE_NAME,
      partitionKeys: [
        {
          name: "datehour",
          type: glue.Schema.STRING,
        },
      ],
      columns: [
        {
          name: "Metadata",
          type: glue.Schema.struct([
            {
              name: "WriteTimestampMicros",
              type: glue.Schema.struct([
                { name: "N", type: glue.Schema.STRING },
              ]),
            },
          ]),
        },
        {
          name: "Keys",
          type: glue.Schema.struct([
            {
              name: "PK",
              type: glue.Schema.struct([
                { name: "S", type: glue.Schema.STRING },
              ]),
            },
            {
              name: "SK",
              type: glue.Schema.struct([
                { name: "S", type: glue.Schema.STRING },
              ]),
            },
          ]),
        },
        {
          name: "OldImage",
          type: imageSchemaType,
        },
        {
          name: "NewImage",
          type: imageSchemaType,
        },
      ],
      dataFormat: glue.DataFormat.JSON,
    });
    // Add partition projection using escape hatch
    // Ref: https://docs.aws.amazon.com/cdk/v2/guide/cfn_layer.html
    const cfnDdbExportTable = ddbExportTable.node
      .defaultChild as aws_glue.CfnTable;
    cfnDdbExportTable.addPropertyOverride("TableInput.Parameters", {
      "projection.enabled": true,
      "projection.datehour.type": "date",
      // NOTE: To account for timezones that are ahead of UTC, specify a far future date instead of `NOW` for the end of the range.
      "projection.datehour.range": "2023/01/01/00,2123/01/01/00",
      "projection.datehour.format": "yyyy/MM/dd/HH",
      "projection.datehour.interval": 1,
      "projection.datehour.interval.unit": "HOURS",
      "storage.location.template":
        `s3://${ddbBucket.bucketName}/` + "${datehour}/AWSDynamoDB/data/",
    });

    new CfnOutput(this, "ConversationAnalyticsTableRef", {
      value: cfnDdbExportTable.ref,
      description: "The name of the Glue table containing conversation analytics data",
    });

    // Create bots table for analytics
    const botsBucket = new s3.Bucket(this, "BotsBucket", {
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.DESTROY,
      objectOwnership: s3.ObjectOwnership.OBJECT_WRITER,
      autoDeleteObjects: true,
      serverAccessLogsBucket: props.accessLogBucket,
      serverAccessLogsPrefix: "BotsBucket",
    });

    // Define the bots analytics table
    const BOTS_ANALYTICS_TABLE_NAME = 'bots_analytics';

    const botsAnalyticsTable = new aws_glue.CfnTable(this, 'BotsAnalyticsTable', {
      catalogId: Stack.of(this).account,
      databaseName: GLUE_DATABASE_NAME,
      tableInput: {
        name: BOTS_ANALYTICS_TABLE_NAME,
        storageDescriptor: {
          columns: [
            { name: 'bot_id', type: 'string' },          // 1
            { name: 'course_id', type: 'string' },       // 2
            { name: 'course_name', type: 'string' },     // 3
            { name: 'create_time', type: 'string' },     // 4
            { name: 'deleted_at', type: 'string' },      // 5
            { name: 'description', type: 'string' },     // 6
            { name: 'district_id', type: 'string' },     // 7
            { name: 'district_name', type: 'string' },   // 8
            { name: 'is_deleted', type: 'string' },      // 9
            { name: 'is_public', type: 'string' },       // 10
            { name: 'last_used_time', type: 'string' },  // 11
            { name: 'owner_user_id', type: 'string' },   // 12
            { name: 'school_id', type: 'string' },       // 13
            { name: 'school_name', type: 'string' },     // 14
            { name: 'title', type: 'string' },           // 15
            { name: 'updated_at', type: 'string' }       // 16
          ],
          location: `s3://${botsBucket.bucketName}/bots_analytics`,
          inputFormat: 'org.apache.hadoop.mapred.TextInputFormat',
          outputFormat: 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
          serdeInfo: {
            serializationLibrary: 'org.apache.hadoop.hive.serde2.OpenCSVSerde',
            parameters: {
              'separatorChar': ',',
              'quoteChar': '"',
              'escapeChar': '\\'
            }
          }
        },
        tableType: 'EXTERNAL_TABLE',
        parameters: { 
          'EXTERNAL': 'TRUE',
          'skip.header.line.count': '1' 
        } 
      }
    });

    this.exportHandler = new python.PythonFunction(this, "ExportHandler", {
      entry: path.join(__dirname, "../../../backend/s3_exporter/"),
      runtime: Runtime.PYTHON_3_12,
      environment: {
        BUCKET_NAME: ddbBucket.bucketName,
        BOTS_BUCKET_NAME: botsBucket.bucketName,
        TABLE_ARN: props.sourceDatabase.table.tableArn,
        BOTS_METADATA_TABLE_ARN: props.sourceDatabase.botsMetadataTableArn,
        BOTS_METADATA_CONFIG_TABLE_ARN: props.sourceDatabase.botsMetadataConfigTableNameArn,
      },
      logRetention: logs.RetentionDays.THREE_MONTHS,
      bundling: {
        assetExcludes: ['.venv', '__pycache__', '*.pyc', '.pytest_cache'],
      }
    });
    this.exportHandler.role?.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["dynamodb:ExportTableToPointInTime", "dynamodb:Scan", "dynamodb:Query"],
        resources: [props.sourceDatabase.table.tableArn, props.sourceDatabase.botsMetadataTableArn, props.sourceDatabase.botsMetadataConfigTableNameArn],
      })
    );
    ddbBucket.grantReadWrite(this.exportHandler);
    botsBucket.grantReadWrite(this.exportHandler);

    this.scheduleRule = new events.Rule(this, "ScheduleRule", {
      schedule: events.Schedule.cron({ minute: "5" }),
      targets: [new targets.LambdaFunction(this.exportHandler)],
    });

    new CfnOutput(this, "AnalyticsWorkgroup", {
      value: wg.name,
    });
    new CfnOutput(this, "AnalyticsOutputLocation", {
      value: `s3://${queryResultBucket.bucketName}`,
    });

    new CfnOutput(this, "BotsBucketName", {
      value: botsBucket.bucketName,
      description: "The name of the S3 bucket containing bot analytics data",
    });

    new CfnOutput(this, "DdbBucketName", {
      value: ddbBucket.bucketName,
      description: "The name of the S3 bucket containing DynamoDB exports for analytics",
    });

    new CfnOutput(this, "BotsBucketArn", {
      value: botsBucket.bucketArn,
      description: "The ARN of the S3 bucket containing bot analytics data",
    });

    this.database = database;
    this.ddbBucket = ddbBucket;
    this.ddbExportTable = ddbExportTable;
    this.workgroupName = wg.name;
    this.resultOutputBucket = queryResultBucket;
    this.workgroupArn = `arn:aws:athena:*:${Stack.of(this).account}:workgroup/${
      wg.name
    }`;
    this.botsBucket = botsBucket;
    
    // Create a proper table reference
    const botsAnalyticsTableArn = Stack.of(this).formatArn({
      service: 'glue',
      resource: 'table',
      resourceName: `${database.databaseName}/${BOTS_ANALYTICS_TABLE_NAME}`
    });
    this.botsAnalyticsTable = glue.Table.fromTableArn(this, 'BotsAnalyticsTableRef', botsAnalyticsTableArn);

    new CfnOutput(this, "BotsAnalyticsTableArn", {
      value: botsAnalyticsTableArn,
      description: "The name of the Glue table containing bot analytics data",
    });

    new CfnOutput(this, "BotsAnalyticsTableName", {
      value: BOTS_ANALYTICS_TABLE_NAME,
      description: "The name of the Glue table containing bot analytics data",
    });
  }
}
