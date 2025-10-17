import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { BedrockCustomBotStack } from "../lib/bedrock-custom-bot-stack";
import {
  getKnowledgeBaseType,
  getEmbeddingModel,
  getChunkingStrategy,
  getAnalyzer,
  getParsingModel,
  getCrowlingScope,
  getCrawlingFilters,
} from "../lib/utils/bedrock-knowledge-base-args";
import { BedrockFoundationModel } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock";
import { ChunkingStrategy } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock/data-sources/chunking";
import {
  CrawlingFilters,
  CrawlingScope,
} from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock/data-sources/web-crawler-data-source";
import { Analyzer } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/opensearch-vectorindex";
import { resolveBedrockCustomBotParameters } from "../lib/utils/parameter-models";

const app = new cdk.App();

// Get parameters specific to Bedrock Custom Bot
const params = resolveBedrockCustomBotParameters();

// Parse JSON strings into objects
const knowledgeBaseJson = JSON.parse(params.knowledgeBase);
const knowledgeJson = JSON.parse(params.knowledge);
const guardrailsJson = JSON.parse(params.guardrails);

// Define interfaces for typed configuration objects
interface BaseConfig {
  envName: string;
  envPrefix: string;
  bedrockRegion: string;
  ownerUserId: string;
  botId: string;
  documentBucketName: string;
  enableRagReplicas: boolean;
}

interface KnowledgeConfig {
  knowledgeBaseType: "dedicated" | "shared" | undefined;
  embeddingsModel: BedrockFoundationModel;
  parsingModel: BedrockFoundationModel | undefined;
  existKnowledgeBaseId?: string;
  existingS3Urls: string[];
  filenames: string[];
  sourceUrls: string[];
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

interface GuardrailConfig {
  is_guardrail_enabled?: boolean;
  hateThreshold?: number;
  insultsThreshold?: number;
  sexualThreshold?: number;
  violenceThreshold?: number;
  misconductThreshold?: number;
  groundingThreshold?: number;
  relevanceThreshold?: number;
  guardrailArn?: number;
  guardrailVersion?: number;
}

interface CrawlingConfig {
  crawlingScope?: CrawlingScope | undefined;
  crawlingFilters: CrawlingFilters;
}

// Extract and organize configuration by category
const baseConfig: BaseConfig = {
  envName: params.envName,
  envPrefix: params.envPrefix,
  bedrockRegion: params.bedrockRegion,
  ownerUserId: params.ownerUserId,
  botId: params.botId,
  documentBucketName: params.documentBucketName,
  enableRagReplicas: params.enableRagReplicas === true,
};

const knowledgeConfig: KnowledgeConfig = {
  knowledgeBaseType: getKnowledgeBaseType(knowledgeBaseJson.type),
  embeddingsModel: getEmbeddingModel(knowledgeBaseJson.embeddings_model),
  parsingModel: getParsingModel(knowledgeBaseJson.parsing_model),
  existKnowledgeBaseId: knowledgeBaseJson.exist_knowledge_base_id,
  existingS3Urls: knowledgeJson.s3_urls.map((s3Url: any) => s3Url),
  filenames: knowledgeJson.filenames.map((filename: any) => filename),
  sourceUrls: knowledgeJson.source_urls.map((sourceUrl: any) => sourceUrl),
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

const crawlingConfig: CrawlingConfig = {
  crawlingScope: getCrowlingScope(knowledgeBaseJson.web_crawling_scope),
  crawlingFilters: getCrawlingFilters(knowledgeBaseJson.web_crawling_filters),
};

const guardrailConfig: GuardrailConfig = {
  is_guardrail_enabled: guardrailsJson.is_guardrail_enabled
    ? guardrailsJson.is_guardrail_enabled
    : undefined,
  hateThreshold: guardrailsJson.hate_threshold
    ? guardrailsJson.hate_threshold
    : undefined,
  insultsThreshold: guardrailsJson.insults_threshold
    ? guardrailsJson.insults_threshold
    : undefined,
  sexualThreshold: guardrailsJson.sexual_threshold
    ? guardrailsJson.sexual_threshold
    : undefined,
  violenceThreshold: guardrailsJson.violence_threshold
    ? guardrailsJson.violence_threshold
    : undefined,
  misconductThreshold: guardrailsJson.misconduct_threshold
    ? guardrailsJson.misconduct_threshold
    : undefined,
  groundingThreshold: guardrailsJson.grounding_threshold
    ? guardrailsJson.grounding_threshold
    : undefined,
  relevanceThreshold: guardrailsJson.relevance_threshold
    ? guardrailsJson.relevance_threshold
    : undefined,
  guardrailArn: guardrailsJson.guardrail_arn
    ? guardrailsJson.guardrail_arn
    : undefined,
  guardrailVersion: guardrailsJson.guardrail_version
    ? guardrailsJson.guardrail_version
    : undefined,
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
console.log(
  "Guardrail Configuration:",
  JSON.stringify(guardrailConfig, null, 2)
);
console.log(
  "Crawling Configuration:",
  JSON.stringify(
    {
      crawlingScope: crawlingConfig.crawlingScope?.toString(),
      crawlingFilters: crawlingConfig.crawlingFilters,
    },
    null,
    2
  )
);

// Create the stack
new BedrockCustomBotStack(app, `BrChatKbStack${baseConfig.botId}`, {
  // Environment configuration
  env: {
    region: baseConfig.bedrockRegion,
  },

  // Base configuration
  ownerUserId: baseConfig.ownerUserId,
  botId: baseConfig.botId,
  bedrockClaudeChatDocumentBucketName: baseConfig.documentBucketName,
  enableRagReplicas: baseConfig.enableRagReplicas,

  // Knowledge base configuration
  knowledgeBaseType: knowledgeConfig.knowledgeBaseType,
  embeddingsModel: knowledgeConfig.embeddingsModel,
  parsingModel: knowledgeConfig.parsingModel,
  existKnowledgeBaseId: knowledgeConfig.existKnowledgeBaseId,
  existingS3Urls: knowledgeConfig.existingS3Urls,
  filenames: knowledgeConfig.filenames,
  sourceUrls: knowledgeConfig.sourceUrls,
  instruction: knowledgeConfig.instruction,
  analyzer: knowledgeConfig.analyzer,

  // Chunking configuration
  chunkingStrategy: chunkingConfig.chunkingStrategy,
  maxTokens: chunkingConfig.maxTokens,
  overlapPercentage: chunkingConfig.overlapPercentage,

  // Crawling configuration
  crawlingScope: crawlingConfig.crawlingScope,
  crawlingFilters: crawlingConfig.crawlingFilters,

  // Guardrail configuration
  guardrail: guardrailConfig,
});

cdk.Tags.of(app).add("CDKEnvironment", baseConfig.envName);
