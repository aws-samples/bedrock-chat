import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { BedrockCustomBotStack } from "../lib/bedrock-custom-bot-stack";
import {
  getEmbeddingModel,
  getChunkingStrategy,
  getAnalyzer,
  getParsingModel,
  getCrowlingScope,
  getCrawlingFilters,
} from "../lib/utils/bedrock-knowledge-base-args";
import { CrawlingFilters } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock/data-sources/web-crawler-data-source";
import { resolveBedrockCustomBotParameters } from "../lib/utils/parameter-models";

const app = new cdk.App();

// Get parameters specific to Bedrock Custom Bot
const params = resolveBedrockCustomBotParameters();
const sepHyphen = params.envPrefix ? "-" : "";

// Log basic parameters for debugging
console.log(
  "Bedrock Custom Bot Parameters:",
  JSON.stringify({
    envName: params.envName,
    envPrefix: params.envPrefix,
    pk: params.pk,
    sk: params.sk,
    documentBucketName: params.documentBucketName,
    useStandByReplicas: params.useStandByReplicas,
    bedrockRegion: params.bedrockRegion,
  })
);

// Parse JSON strings into objects
const knowledgeBase = JSON.parse(params.knowledgeBase);
const knowledge = JSON.parse(params.knowledge);
const guardrails = JSON.parse(params.guardrails);

// Extract data from parsed objects
const ownerUserId = params.pk;
const botId = params.sk.split("#")[2];
const existingS3Urls = knowledge.s3_urls.L.map((s3Url: any) => s3Url.S);
const sourceUrls = knowledge.source_urls.L.map((sourceUrl: any) => sourceUrl.S);
const useStandbyReplicas = params.useStandByReplicas === true;

console.log(
  "Parsed Configuration:",
  JSON.stringify({
    ownerUserId,
    botId,
    existingS3Urls,
    sourceUrls,
    useStandbyReplicas,
  })
);

// Process knowledge base configuration
const embeddingsModel = getEmbeddingModel(knowledgeBase.embeddings_model.S);
const parsingModel = getParsingModel(knowledgeBase.parsing_model.S);
const crawlingScope = getCrowlingScope(knowledgeBase.web_crawling_scope.S);
const crawlingFilters: CrawlingFilters = getCrawlingFilters(
  knowledgeBase.web_crawling_filters.M
);
const existKnowledgeBaseId = knowledgeBase.exist_knowledge_base_id?.S;
const maxTokens = knowledgeBase.chunking_configuration.M.max_tokens
  ? Number(knowledgeBase.chunking_configuration.M.max_tokens.N)
  : undefined;
const instruction = knowledgeBase.instruction?.S;
const analyzer = knowledgeBase.open_search.M.analyzer.M
  ? getAnalyzer(knowledgeBase.open_search.M.analyzer.M)
  : undefined;
const overlapPercentage = knowledgeBase.chunking_configuration.M
  .overlap_percentage
  ? Number(knowledgeBase.chunking_configuration.M.overlap_percentage.N)
  : undefined;
const overlapTokens = knowledgeBase.chunking_configuration.M.overlap_tokens
  ? Number(knowledgeBase.chunking_configuration.M.overlap_tokens.N)
  : undefined;
const maxParentTokenSize = knowledgeBase.chunking_configuration.M
  .max_parent_token_size
  ? Number(knowledgeBase.chunking_configuration.M.max_parent_token_size.N)
  : undefined;
const maxChildTokenSize = knowledgeBase.chunking_configuration.M
  .max_child_token_size
  ? Number(knowledgeBase.chunking_configuration.M.max_child_token_size.N)
  : undefined;
const bufferSize = knowledgeBase.chunking_configuration.M.buffer_size
  ? Number(knowledgeBase.chunking_configuration.M.buffer_size.N)
  : undefined;
const breakpointPercentileThreshold = knowledgeBase.chunking_configuration.M
  .breakpoint_percentile_threshold
  ? Number(
      knowledgeBase.chunking_configuration.M.breakpoint_percentile_threshold.N
    )
  : undefined;

// Process guardrails configuration
const is_guardrail_enabled = guardrails.is_guardrail_enabled
  ? Boolean(guardrails.is_guardrail_enabled.BOOL)
  : undefined;
const hateThreshold = guardrails.hate_threshold
  ? Number(guardrails.hate_threshold.N)
  : undefined;
const insultsThreshold = guardrails.insults_threshold
  ? Number(guardrails.insults_threshold.N)
  : undefined;
const sexualThreshold = guardrails.sexual_threshold
  ? Number(guardrails.sexual_threshold.N)
  : undefined;
const violenceThreshold = guardrails.violence_threshold
  ? Number(guardrails.violence_threshold.N)
  : undefined;
const misconductThreshold = guardrails.misconduct_threshold
  ? Number(guardrails.misconduct_threshold.N)
  : undefined;
const groundingThreshold = guardrails.grounding_threshold
  ? Number(guardrails.grounding_threshold.N)
  : undefined;
const relevanceThreshold = guardrails.relevance_threshold
  ? Number(guardrails.relevance_threshold.N)
  : undefined;
const guardrailArn = guardrails.guardrail_arn
  ? Number(guardrails.guardrail_arn.N)
  : undefined;
const guardrailVersion = guardrails.guardrail_version
  ? Number(guardrails.guardrail_version.N)
  : undefined;

// Get chunking strategy
const chunkingStrategy = getChunkingStrategy(
  knowledgeBase.chunking_configuration.M.chunking_strategy.S,
  knowledgeBase.embeddings_model.S,
  {
    maxTokens,
    overlapPercentage,
    overlapTokens,
    maxParentTokenSize,
    maxChildTokenSize,
    bufferSize,
    breakpointPercentileThreshold,
  }
);

console.log(
  "Knowledge Base Configuration:",
  JSON.stringify({
    embeddingsModel: embeddingsModel.toString(),
    chunkingStrategy: chunkingStrategy.toString(),
    existKnowledgeBaseId,
    maxTokens,
    instruction,
    is_guardrail_enabled,
    parsingModel: parsingModel?.toString(),
    crawlingScope: crawlingScope?.toString(),
    analyzer: analyzer ? "configured" : "undefined",
  })
);

// Create the stack
const bedrockCustomBotStack = new BedrockCustomBotStack(
  app,
  `${params.envPrefix}${sepHyphen}BrChatKbStack${botId}`,
  {
    env: {
      region: params.bedrockRegion,
    },
    ownerUserId,
    botId,
    embeddingsModel,
    parsingModel,
    crawlingScope,
    crawlingFilters,
    existKnowledgeBaseId,
    bedrockClaudeChatDocumentBucketName: params.documentBucketName,
    chunkingStrategy,
    existingS3Urls,
    sourceUrls,
    maxTokens,
    instruction,
    analyzer,
    overlapPercentage,
    guardrail: {
      is_guardrail_enabled,
      hateThreshold,
      insultsThreshold,
      sexualThreshold,
      violenceThreshold,
      misconductThreshold,
      groundingThreshold,
      relevanceThreshold,
      guardrailArn,
      guardrailVersion,
    },
    useStandbyReplicas,
  }
);

cdk.Tags.of(app).add("CDKEnvironment", params.envName);
