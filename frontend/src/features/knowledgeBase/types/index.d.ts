export type BedrockKnowledgeBase = {
  knowledgeBaseId: string | null;
  dataSourceIds?: string[]; // only present after bot is ready
  embeddingsModel: EmbeddingsModel;
  chunkingStrategy: ChunkingStrategy;
  maxTokens: number | null; // null when chunkingStrategy isn't 'fixed_size'
  overlapPercentage: number | null; // null when chunkingStrategy isn't 'fixed_size'
  openSearch: OpenSearchParams;
  searchParams: SearchParams;
};

export type EmbeddingsModel = 'titan_v2' | 'cohere_multilingual_v3';

export type ChunkingStrategy = 'default' | 'fixed_size' | 'none';

export type OpenSearchParams = {
  analyzer: {
    characterFilters: CharacterFilter[];
    tokenizer: Tokenizer;
    tokenFilters: TokenFilter[];
  } | null;
};

export type CharacterFilter = 'icu_normalizer'; // static

export type Tokenizer = 'kuromoji_tokenizer' | 'icu_tokenizer';

export type TokenFilter =
  | 'kuromoji_baseform'
  | 'kuromoji_part_of_speech'
  | 'kuromoji_stemmer'
  | 'cjk_width'
  | 'ja_stop'
  | 'lowercase'
  | 'icu_folding';

export type SearchParams = {
  maxResults: number;
  searchType: SearchType;
};

export type SearchType = 'hybrid' | 'semantic';
