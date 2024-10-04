import { BedrockKnowledgeBase, OpenSearchParams, SearchParams } from '../types';

export const OPENSEARCH_ANALYZER: {
  [key: string]: OpenSearchParams;
} = {
  icu: {
    analyzer: {
      characterFilters: ['icu_normalizer'],
      tokenizer: 'icu_tokenizer',
      tokenFilters: ['icu_folding'],
    },
  } as OpenSearchParams,
  kuromoji: {
    analyzer: {
      characterFilters: ['icu_normalizer'],
      tokenizer: 'kuromoji_tokenizer',
      tokenFilters: [
        'kuromoji_baseform',
        'kuromoji_part_of_speech',
        'kuromoji_stemmer',
        'cjk_width',
        'ja_stop',
        'lowercase',
        'icu_folding',
      ],
    },
  } as OpenSearchParams,
  none: {
    // as fallback
    analyzer: null,
  },
} as const;

export const DEFAULT_OPENSEARCH_ANALYZER: {
  [key: string]: string;
} = {
  ja: 'kuromoji',
  ko: 'icu',
  zhhans: 'icu',
  zhhant: 'icu',
} as const;

export const DEFAULT_BEDROCK_KNOWLEDGEBASE: BedrockKnowledgeBase = {
  knowledgeBaseId: null,
  embeddingsModel: 'cohere_multilingual_v3',
  openSearch: OPENSEARCH_ANALYZER['none'],
  chunkingStrategy: 'default',
  maxTokens: null,
  overlapPercentage: null,
  searchParams: {
    maxResults: 20,
    searchType: 'hybrid',
  },
};

export const DEFAULT_CHUNKING_MAX_TOKENS = 300;
export const DEFAULT_CHUNKING_OVERLAP_PERCENTAGE = 20;

export const EDGE_CHUNKING_MAX_TOKENS = {
  MAX: {
    titan_v2: 8192,
    cohere_multilingual_v3: 512,
  },
  MIN: 20,
  STEP: 1,
};

export const EDGE_CHUNKING_OVERLAP_PERCENTAGE = {
  MAX: 100,
  MIN: 0,
  STEP: 1,
};

export const DEFAULT_SEARCH_CONFIG: SearchParams = {
  maxResults: 20,
  searchType: 'hybrid',
};
