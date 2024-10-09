import { CfnOutput, RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import { VectorCollection } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/opensearchserverless";
import {
  Analyzer,
  VectorIndex,
} from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/opensearch-vectorindex";
import * as s3 from "aws-cdk-lib/aws-s3";
import {
  BedrockFoundationModel,
  ChunkingStrategy,
  S3DataSource,
} from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock";
import { KnowledgeBase } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock";
import { aws_bedrock as bedrock } from "aws-cdk-lib";

import { getThreshold } from "./utils/bedrock-guardrails";

const BLOCKED_INPUT_MESSAGE = "this input message is blocked";
const BLOCKED_OUTPUT_MESSAGE = "this output message is blocked";

interface BedrockGuardrailProps {
  readonly is_guardrail_enabled?: boolean;
  readonly hateThreshold?: number;
  readonly insultsThreshold?: number;
  readonly sexualThreshold?: number;
  readonly violenceThreshold?: number;
  readonly misconductThreshold?: number;
  readonly groundingThreshold?: number;
  readonly relevanceThreshold?: number;
  readonly guardrailArn?: number;
  readonly guardrailVersion?: number;
}

interface BedrockCustomBotStackProps extends StackProps {
  readonly ownerUserId: string;
  readonly botId: string;
  readonly embeddingsModel: BedrockFoundationModel;
  readonly bedrockClaudeChatDocumentBucketName: string;
  readonly chunkingStrategy: ChunkingStrategy;
  readonly existingS3Urls: string[];
  readonly maxTokens?: number;
  readonly instruction?: string;
  readonly analyzer?: Analyzer;
  readonly overlapPercentage?: number;
  readonly guardrail?: BedrockGuardrailProps;
}

export class BedrockCustomBotStack extends Stack {
  constructor(scope: Construct, id: string, props: BedrockCustomBotStackProps) {
    super(scope, id, props);

    const { docBucketsAndPrefixes } = this.setupBucketsAndPrefixes(props);

    const vectorCollection = new VectorCollection(this, "KBVectors");
    const vectorIndex = new VectorIndex(this, "KBIndex", {
      collection: vectorCollection,
      // DO NOT CHANGE THIS VALUE
      indexName: "bedrock-knowledge-base-default-index",
      // DO NOT CHANGE THIS VALUE
      vectorField: "bedrock-knowledge-base-default-vector",
      vectorDimensions: props.embeddingsModel.vectorDimensions!,
      mappings: [
        {
          mappingField: "AMAZON_BEDROCK_TEXT_CHUNK",
          dataType: "text",
          filterable: true,
        },
        {
          mappingField: "AMAZON_BEDROCK_METADATA",
          dataType: "text",
          filterable: false,
        },
      ],
      analyzer: props.analyzer,
    });

    const kb = new KnowledgeBase(this, "KB", {
      embeddingsModel: props.embeddingsModel,
      vectorStore: vectorCollection,
      vectorIndex: vectorIndex,
      instruction: props.instruction,
    });

    const dataSources = docBucketsAndPrefixes.map(({ bucket, prefix }) => {
      bucket.grantRead(kb.role);
      const inclusionPrefixes = prefix === "" ? undefined : [prefix];
      return new S3DataSource(this, `DataSource${prefix}`, {
        bucket: bucket,
        knowledgeBase: kb,
        dataSourceName: bucket.bucketName,
        chunkingStrategy: props.chunkingStrategy,
        maxTokens: props.maxTokens,
        overlapPercentage: props.overlapPercentage,
        inclusionPrefixes: inclusionPrefixes,
      });
    });

    if (props.guardrail?.is_guardrail_enabled == true) {
      // Use only parameters with a value greater than or equal to 0
      let contentPolicyConfigFiltersConfig = [];
      let contextualGroundingFiltersConfig = [];
      console.log("props.guardrail: ", props.guardrail);

      if (
        props.guardrail.hateThreshold != undefined &&
        props.guardrail.hateThreshold > 0
      ) {
        contentPolicyConfigFiltersConfig.push({
          inputStrength: getThreshold(props.guardrail.hateThreshold),
          outputStrength: getThreshold(props.guardrail.hateThreshold),
          type: "HATE",
        });
      }

      if (
        props.guardrail.insultsThreshold != undefined &&
        props.guardrail.insultsThreshold > 0
      ) {
        contentPolicyConfigFiltersConfig.push({
          inputStrength: getThreshold(props.guardrail.insultsThreshold),
          outputStrength: getThreshold(props.guardrail.insultsThreshold),
          type: "INSULTS",
        });
      }

      if (
        props.guardrail.sexualThreshold != undefined &&
        props.guardrail.sexualThreshold > 0
      ) {
        contentPolicyConfigFiltersConfig.push({
          inputStrength: getThreshold(props.guardrail.sexualThreshold),
          outputStrength: getThreshold(props.guardrail.sexualThreshold),
          type: "SEXUAL",
        });
      }

      if (
        props.guardrail.violenceThreshold != undefined &&
        props.guardrail.violenceThreshold > 0
      ) {
        contentPolicyConfigFiltersConfig.push({
          inputStrength: getThreshold(props.guardrail.violenceThreshold),
          outputStrength: getThreshold(props.guardrail.violenceThreshold),
          type: "VIOLENCE",
        });
      }

      if (
        props.guardrail.misconductThreshold != undefined &&
        props.guardrail.misconductThreshold > 0
      ) {
        contentPolicyConfigFiltersConfig.push({
          inputStrength: getThreshold(props.guardrail.misconductThreshold),
          outputStrength: getThreshold(props.guardrail.misconductThreshold),
          type: "MISCONDUCT",
        });
      }

      if (
        props.guardrail.groundingThreshold != undefined &&
        props.guardrail.groundingThreshold > 0
      ) {
        contextualGroundingFiltersConfig.push({
          threshold: props.guardrail.groundingThreshold!,
          type: "GROUNDING",
        });
      }

      if (
        props.guardrail.relevanceThreshold != undefined &&
        props.guardrail.relevanceThreshold > 0
      ) {
        contextualGroundingFiltersConfig.push({
          threshold: props.guardrail.relevanceThreshold!,
          type: "RELEVANCE",
        });
      }

      console.log(
        "contentPolicyConfigFiltersConfig: ",
        contentPolicyConfigFiltersConfig
      );
      console.log(
        "contextualGroundingFiltersConfig: ",
        contextualGroundingFiltersConfig
      );

      // Deploy Guardrail if it contains at least one configuration value
      if (
        contentPolicyConfigFiltersConfig.length > 0 ||
        contextualGroundingFiltersConfig.length > 0
      ) {
        const guardrail = new bedrock.CfnGuardrail(this, "Guardrail", {
          name: props.botId,
          blockedInputMessaging: BLOCKED_INPUT_MESSAGE,
          blockedOutputsMessaging: BLOCKED_OUTPUT_MESSAGE,
          contentPolicyConfig:
            contentPolicyConfigFiltersConfig.length > 0
              ? {
                  filtersConfig: contentPolicyConfigFiltersConfig,
                }
              : undefined,
          contextualGroundingPolicyConfig:
            contextualGroundingFiltersConfig.length > 0
              ? {
                  filtersConfig: contextualGroundingFiltersConfig,
                }
              : undefined,
        });
        new CfnOutput(this, "GuardrailArn", {
          value: guardrail.attrGuardrailArn,
        });
        new CfnOutput(this, "GuardrailVersion", {
          value: guardrail.attrVersion,
        });
      }
    }

    new CfnOutput(this, "KnowledgeBaseId", {
      value: kb.knowledgeBaseId,
    });
    new CfnOutput(this, "KnowledgeBaseArn", {
      value: kb.knowledgeBaseArn,
    });
    new CfnOutput(this, "OwnerUserId", {
      value: props.ownerUserId,
    });
    new CfnOutput(this, "BotId", {
      value: props.botId,
    });
    dataSources.forEach((dataSource, index) => {
      new CfnOutput(this, `DataSource${index}`, {
        value: dataSource.dataSourceId,
      });
    });
  }

  private setupBucketsAndPrefixes(props: BedrockCustomBotStackProps): {
    docBucketsAndPrefixes: { bucket: s3.IBucket; prefix: string }[];
  } {
    /**
     * Setup the document buckets and prefixes based on the provided properties.
     *
     * This method processes the provided existing bucket URLs and sets up the
     * S3 buckets and inclusion prefixes accordingly. It always includes the
     * default bedrockClaudeChatDocumentBucketName in the list of document buckets.
     *
     * @param props The properties passed to the stack, including existing bucket URLs, owner user ID, and bot ID.
     * @returns An object containing the list of document buckets and extracted prefixes.
     */
    const docBucketsAndPrefixes: { bucket: s3.IBucket; prefix: string }[] = [];

    // Always add the default bucket with its default prefix
    docBucketsAndPrefixes.push({
      bucket: s3.Bucket.fromBucketName(
        this,
        props.bedrockClaudeChatDocumentBucketName,
        props.bedrockClaudeChatDocumentBucketName
      ),
      prefix: `${props.ownerUserId}/${props.botId}/documents/`,
    });

    if (props.existingS3Urls && props.existingS3Urls.length > 0) {
      props.existingS3Urls.forEach((url) => {
        const { bucketName, prefix } = this.parseS3Url(url);
        docBucketsAndPrefixes.push({
          bucket: s3.Bucket.fromBucketName(this, bucketName, bucketName),
          prefix: prefix,
        });
      });
    }

    return { docBucketsAndPrefixes };
  }

  private parseS3Url(url: string): { bucketName: string; prefix: string } {
    console.info(`Parsing S3 URL: ${url}`);
    if (!url.startsWith("s3://")) {
      throw new Error(`Invalid S3 URL format: ${url}`);
    }

    const urlParts = url.replace("s3://", "").split("/");
    if (urlParts.length < 1) {
      throw new Error(`Invalid S3 URL format: ${url}`);
    }

    const bucketName = urlParts.shift()!;
    const prefix = urlParts.join("/");
    console.info(`Parsed S3 URL: bucketName=${bucketName}, prefix=${prefix}`);
    return { bucketName, prefix };
  }
}
