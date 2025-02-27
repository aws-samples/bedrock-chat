import { BedrockKnowledgeBase } from '../features/knowledgeBase/types';
import { Model } from './conversation';
export type BotKind = 'private' | 'mixed';

type ActiveModels = {
  [K in Model]: boolean;
};

export type BotMeta = {
  id: string;
  title: string;
  description: string;
  createTime: Date;
  lastUsedTime: Date;
  isPublic: boolean;
  isPinned: boolean;
  owned: boolean;
  syncStatus: BotSyncStatus;
};

export type BotKnowledge = {
  sourceUrls: string[];
  // Sitemap cannot be used yet.
  sitemapUrls: string[];
  filenames: string[];
  s3Urls: string[];
};

export type ConversationQuickStarter = {
  title: string;
  example: string;
};

export type BotKnowledgeDiff = {
  sourceUrls: string[];
  // Sitemap cannot be used yet.
  sitemapUrls: string[];
  addedFilenames: string[];
  deletedFilenames: string[];
  unchangedFilenames: string[];
  s3Urls: string[];
};

export type BotSyncStatus = 'QUEUED' | 'RUNNING' | 'SUCCEEDED' | 'FAILED';

export type BotListItem = BotMeta & {
  available: boolean;
};

export type ReasoningParams = {
  budgetTokens: number;
};

export type GenerationParams = {
  maxTokens: number;
  topK: number;
  topP: number;
  temperature: number;
  stopSequences: string[];
  reasoningParams: ReasoningParams;
};

export type GuardrailsParams = {
  isGuardrailEnabled: boolean;
  hateThreshold: number;
  insultsThreshold: number;
  sexualThreshold: number;
  violenceThreshold: number;
  misconductThreshold: number;
  groundingThreshold: number;
  relevanceThreshold: number;
  guardrailArn: string;
  guardrailVersion: string;
};

export type BotDetails = BotMeta & {
  instruction: string;
  generationParams: GenerationParams;
  agent: Agent;
  knowledge: BotKnowledge;
  syncStatusReason: string;
  displayRetrievedChunks: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  bedrockGuardrails: GuardrailsParams;
  bedrockKnowledgeBase: BedrockKnowledgeBase;
  activeModels: ActiveModels;
};

export type BotSummary = BotMeta & {
  hasKnowledge: boolean;
  hasAgent: boolean;
  hasExistKnowledngeBaseId: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  activeModels: ActiveModels;
};

export type BotFile = {
  filename: string;
  status: 'UPLOADING' | 'UPLOADED' | 'ERROR';
  errorMessage?: string;
  progress?: number;
};

export type RegisterBotRequest = {
  id: string;
  title: string;
  instruction: string;
  agent: AgentInput;
  description?: string;
  generationParams?: GenerationParams;
  knowledge?: BotKnowledge;
  displayRetrievedChunks: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  bedrockGuardrails?: GuardrailsParams;
  bedrockKnowledgeBase?: BedrockKnowledgeBase;
  activeModels: ActiveModels;
};

export type RegisterBotResponse = BotDetails;

export type UpdateBotRequest = {
  title: string;
  instruction: string;
  description?: string;
  agent: AgentInput;
  generationParams?: BotGenerationConfig;
  knowledge?: BotKnowledgeDiff;
  displayRetrievedChunks: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  bedrockGuardrails?: GuardrailsParams;
  bedrockKnowledgeBase?: BedrockKnowledgeBase;
  activeModels: ActiveModels;
};

export type UpdateBotResponse = {
  id: string;
  title: string;
  instruction: string;
  description: string;
  generationParams: GenerationParams;
  knowledge?: BotKnowledge;
  displayRetrievedChunks: boolean;
  conversationQuickStarters: ConversationQuickStarter[];
  bedrockKnowledgeBase: BedrockKnowledgeBase;
  activeModels: ActiveModels;
};

export type UpdateBotPinnedRequest = {
  pinned: boolean;
};

export type UpdateBotPinnedResponse = null;

export type UpdateBotVisibilityRequest = {
  toPublic: boolean;
};

export type UpdateBotVisibilityResponse = null;

export type GetBotsRequest =
  | {
      kind: 'private';
      limit?: number;
    }
  | {
      kind: 'mixed';
      limit: number;
    }
  | {
      kind: 'mixed';
      pinned: boolean;
    };

export type GetBotsResponse = BotListItem[];

export type GetMyBotResponse = BotDetails;

export type GetBotSummaryResponse = BotSummary;

export type GetPublicBotResponse = BotDetails;

export type GetPresignedUrlResponse = {
  url: string;
};
