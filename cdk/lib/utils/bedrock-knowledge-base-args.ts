import {
  BedrockFoundationModel,
  ChunkingStrategy,
} from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/bedrock";
import { Analyzer } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/opensearch-vectorindex";
import {
  CharacterFilterType,
  TokenFilterType,
  TokenizerType,
} from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/opensearchserverless";

export const getEmbeddingModel = (
  embeddingsModel: string
): BedrockFoundationModel => {
  switch (embeddingsModel) {
    case "titan_v2":
      return BedrockFoundationModel.TITAN_EMBED_TEXT_V2_1024;
    case "cohere_multilingual_v3":
      return BedrockFoundationModel.COHERE_EMBED_MULTILINGUAL_V3;
    default:
      throw new Error(`Unknown embeddings model: ${embeddingsModel}`);
  }
};

export const getChunkingStrategy = (
  chunkingStrategy: string
): ChunkingStrategy => {
  switch (chunkingStrategy) {
    case "default":
      return ChunkingStrategy.DEFAULT;
    case "fixed_size":
      return ChunkingStrategy.FIXED_SIZE;
    case "none":
      return ChunkingStrategy.NONE;
    default:
      throw new Error(`Unknown chunking strategy: ${chunkingStrategy}`);
  }
};

export const getAnalyzer = (analyzer: any): Analyzer | undefined => {
  // Example of analyzer:
  //    {
  //     "character_filters": {
  //       "L": [
  //         {
  //           "S": "icu_normalizer"
  //         }
  //       ]
  //     },
  //     "token_filters": {
  //       "L": [
  //         {
  //           "S": "kuromoji_baseform"
  //         },
  //         {
  //           "S": "kuromoji_part_of_speech"
  //         }
  //       ]
  //     },
  //     "tokenizer": {
  //       "S": "kuromoji_tokenizer"
  //     }
  //   }
  console.log("getAnalyzer: analyzer: ", analyzer);
  if (
    !analyzer ||
    !analyzer.character_filters ||
    !analyzer.character_filters.L
  ) {
    return undefined;
  }

  const characterFilters: CharacterFilterType[] =
    analyzer.character_filters.L.map((filter: any) => {
      switch (filter.S) {
        case "icu_normalizer":
          return CharacterFilterType.ICU_NORMALIZER;
        default:
          throw new Error(`Unknown character filter: ${filter.S}`);
      }
    });

  const tokenizer: TokenizerType = (() => {
    if (!analyzer.tokenizer || !analyzer.tokenizer.S) {
      throw new Error(`Tokenizer is not defined`);
    }
    switch (analyzer.tokenizer.S) {
      case "kuromoji_tokenizer":
        return TokenizerType.KUROMOJI_TOKENIZER;
      case "icu_tokenizer":
        return TokenizerType.ICU_TOKENIZER;
      default:
        throw new Error(`Unknown tokenizer: ${analyzer.tokenizer.S}`);
    }
  })();

  const tokenFilters: TokenFilterType[] =
    analyzer.token_filters?.L.map((filter: any) => {
      switch (filter.S) {
        case "kuromoji_baseform":
          return TokenFilterType.KUROMOJI_BASEFORM;
        case "kuromoji_part_of_speech":
          return TokenFilterType.KUROMOJI_PART_OF_SPEECH;
        case "kuromoji_stemmer":
          return TokenFilterType.KUROMOJI_STEMMER;
        case "cjk_width":
          return TokenFilterType.CJK_WIDTH;
        case "ja_stop":
          return TokenFilterType.JA_STOP;
        case "lowercase":
          return TokenFilterType.LOWERCASE;
        case "icu_folding":
          return TokenFilterType.ICU_FOLDING;
        default:
          throw new Error(`Unknown token filter: ${filter.S}`);
      }
    }) || [];

  return {
    characterFilters,
    tokenizer,
    tokenFilters,
  };
};
