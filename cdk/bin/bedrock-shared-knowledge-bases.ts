import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { BedrockSharedKnowledgeBasesStack } from "../lib/bedrock-shared-knowledge-bases-stack";
import {
  getEmbeddingModel,
  getChunkingStrategy,
  getAnalyzer,
  getParsingModel,
} from "../lib/utils/bedrock-knowledge-base-args";
import { BedrockFoundationModel } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock";
import { ChunkingStrategy } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock/data-sources/chunking";
import { Analyzer } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/opensearch-vectorindex";
import { resolveBedrockSharedKnowledgeBasesParameters } from "../lib/utils/parameter-models";

const app = new cdk.App();

// Get parameters specific to Bedrock Custom Bot
const params = resolveBedrockSharedKnowledgeBasesParameters();

// Parse JSON strings into objects
const sharedKnowledgeBasesJson = JSON.parse(params.sharedKnowledgeBases);

// Define interfaces for typed configuration objects
interface BaseConfig {
  envName: string;
  envPrefix: string;
  bedrockRegion: string;
  documentBucketName: string;
  enableRagReplicas: boolean;
}

interface KnowledgeConfig {
  knowledgeBaseHash: string;
  embeddingsModel: BedrockFoundationModel;
  parsingModel: BedrockFoundationModel | undefined;
  instruction?: string;
  analyzer?: Analyzer | undefined;
}

interface ChunkingConfig {
  chunkingStrategy: ChunkingStrategy;
  maxTokens?: number;
  overlapPercentage?: number;
  overlapTokens?: number;
  maxParentTokenSize?: number;
  maxChildTokenSize?: number;
  bufferSize?: number;
  breakpointPercentileThreshold?: number;
}

// Extract and organize configuration by category
const baseConfig: BaseConfig = {
  envName: params.envName,
  envPrefix: params.envPrefix,
  bedrockRegion: params.bedrockRegion,
  documentBucketName: params.documentBucketName,
  enableRagReplicas: params.enableRagReplicas === true,
};

const knowledgeBases = sharedKnowledgeBasesJson.map((sharedKnowledgeBase: any) => {
  const knowledgeBaseJson = sharedKnowledgeBase.KnowledgeBase;
  const knowledgeBaseHash = sharedKnowledgeBase.KnowledgeBaseHash;
  const knowledgeConfig: KnowledgeConfig = {
    knowledgeBaseHash: knowledgeBaseHash,
    embeddingsModel: getEmbeddingModel(knowledgeBaseJson.embeddings_model),
    parsingModel: getParsingModel(knowledgeBaseJson.parsing_model),
    instruction: knowledgeBaseJson.instruction,
    analyzer: knowledgeBaseJson.open_search?.analyzer
      ? getAnalyzer(knowledgeBaseJson.open_search.analyzer)
      : undefined,
  };

  // Extract chunking configuration
  const chunkingParams = {
    maxTokens: knowledgeBaseJson.chunking_configuration?.max_tokens
      ? knowledgeBaseJson.chunking_configuration.max_tokens
      : undefined,
    overlapPercentage: knowledgeBaseJson.chunking_configuration?.overlap_percentage
      ? knowledgeBaseJson.chunking_configuration.overlap_percentage
      : undefined,
    overlapTokens: knowledgeBaseJson.chunking_configuration?.overlap_tokens
      ? knowledgeBaseJson.chunking_configuration.overlap_tokens
      : undefined,
    maxParentTokenSize: knowledgeBaseJson.chunking_configuration?.max_parent_token_size
      ? knowledgeBaseJson.chunking_configuration.max_parent_token_size
      : undefined,
    maxChildTokenSize: knowledgeBaseJson.chunking_configuration?.max_child_token_size
      ? knowledgeBaseJson.chunking_configuration.max_child_token_size
      : undefined,
    bufferSize: knowledgeBaseJson.chunking_configuration?.buffer_size
      ? knowledgeBaseJson.chunking_configuration.buffer_size
      : undefined,
    breakpointPercentileThreshold: knowledgeBaseJson.chunking_configuration?.breakpoint_percentile_threshold
      ? knowledgeBaseJson.chunking_configuration.breakpoint_percentile_threshold
      : undefined,
  };

  const chunkingConfig: ChunkingConfig = {
    ...chunkingParams,
    chunkingStrategy: getChunkingStrategy(
      knowledgeBaseJson.chunking_configuration?.chunking_strategy,
      knowledgeBaseJson.embeddings_model,
      chunkingParams
    ),
  };

  // Log organized configurations for debugging
  console.log("Base Configuration:", JSON.stringify(baseConfig, null, 2));
  console.log(
    "Knowledge Configuration:",
    JSON.stringify(
      {
        ...knowledgeConfig,
        embeddingsModel: knowledgeConfig.embeddingsModel.toString(),
        parsingModel: knowledgeConfig.parsingModel?.toString(),
        analyzer: knowledgeConfig.analyzer ? "configured" : "undefined",
      },
      null,
      2
    )
  );
  console.log(
    "Chunking Configuration:",
    JSON.stringify(
      {
        ...chunkingConfig,
        chunkingStrategy: chunkingConfig.chunkingStrategy.toString(),
      },
      null,
      2
    )
  );
  return {
    knowledgeConfig,
    chunkingConfig,
  };
});

// Create the stack
new BedrockSharedKnowledgeBasesStack(app, "BrChatSharedKbStack", {
  // Environment configuration
  env: {
    region: baseConfig.bedrockRegion,
  },

  // Base configuration
  documentBucketName: baseConfig.documentBucketName,
  enableRagReplicas: baseConfig.enableRagReplicas,

  knowledgeBases: knowledgeBases.map((knowledgeBase: any) => ({
    // Knowledge base configuration
    knowledgeBaseHash: knowledgeBase.knowledgeConfig.knowledgeBaseHash,
    embeddingsModel: knowledgeBase.knowledgeConfig.embeddingsModel,
    parsingModel: knowledgeBase.knowledgeConfig.parsingModel,
    instruction: knowledgeBase.knowledgeConfig.instruction,
    analyzer: knowledgeBase.knowledgeConfig.analyzer,

    // Chunking configuration
    chunkingStrategy: knowledgeBase.chunkingConfig.chunkingStrategy,
    maxTokens: knowledgeBase.chunkingConfig.maxTokens,
    overlapPercentage: knowledgeBase.chunkingConfig.overlapPercentage,
  })),
});

cdk.Tags.of(app).add("CDKEnvironment", baseConfig.envName);
