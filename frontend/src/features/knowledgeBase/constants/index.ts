import {
  BedrockKnowledgeBase,
  OpenSearchParams,
  SearchParams,
  FixedSizeParams,
  HierarchicalParams,
  SemanticParams,
} from '../types';

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
  existKnowledgeBaseId: null,
  embeddingsModel: 'cohere_multilingual_v3',
  openSearch: OPENSEARCH_ANALYZER['none'],
  chunkingConfiguration: {
    chunkingStrategy: 'default'
  },
  searchParams: {
    maxResults: 20,
    searchType: 'hybrid',
  },
};

export const DEFAULT_FIXED_CHUNK_PARAMS: FixedSizeParams = {
  chunkingStrategy: 'fixed_size',
  maxTokens: 300,
  overlapPercentage: 20,
};

// Fixed size chunking valid range
// Ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_FixedSizeChunkingConfiguration.html 
export const EDGE_FIXED_CHUNK_PARAMS = {
  maxTokens: {
    MAX: {
      titan_v2: 8192,
      cohere_multilingual_v3: 512,
    },
    MIN: 1,
    STEP: 1,
  },
  overlapPercentage: {
    MAX: 99,
    MIN: 1,
    STEP: 1,
  },
};

export const DEFAULT_HIERARCHICAL_CHUNK_PARAMS: HierarchicalParams = {
  chunkingStrategy: 'hierarchical',
  overlapTokens: 60,
  maxParentTokenSize: 1500,
  maxChildTokenSize: 300,
};

// Hierarchical chunking valid range
// Ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_HierarchicalChunkingConfiguration.html
export const EDGE_HIERARCHICAL_CHUNK_PARAMS = {
  overlapTokens: {
    MIN: 1,
    STEP: 1,
  },
  maxParentTokenSize: {
    MAX: {
      titan_v2: 8192,
      cohere_multilingual_v3: 512,
    },
    MIN: 1,
    STEP: 1,
  },
  maxChildTokenSize: {
    MAX: {
      titan_v2: 8192,
      cohere_multilingual_v3: 512,
    },
    MIN: 1,
    STEP: 1,
  },
};

export const DEFAULT_SEMANTIC_CHUNK_PARAMS: SemanticParams = {
  chunkingStrategy: 'semantic',
  maxTokens: 300,
  bufferSize: 0,
  breakpointPercentileThreshold: 95,
};

// Semantic chunking valid range
// Ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_SemanticChunkingConfiguration.html
export const EDGE_SEMANTIC_CHUNK_PARAMS = {
  maxTokens: {
    MAX: {
      titan_v2: 8192,
      cohere_multilingual_v3: 512,
    },
    MIN: 1,
    STEP: 1,
  },
  bufferSize: {
    MAX: 1,
    MIN: 0,
    STEP: 1,
  },
  breakpointPercentileThreshold: {
    MAX: 99,
    MIN: 50,
    STEP: 1,
  },
};

export const EDGE_SEARCH_PARAMS = {
  maxResults: {
    MAX: 100,
    MIN: 1,
    STEP: 1,
  },
};

export const DEFAULT_SEARCH_CONFIG: SearchParams = {
  maxResults: 5,
  searchType: 'hybrid',
};
