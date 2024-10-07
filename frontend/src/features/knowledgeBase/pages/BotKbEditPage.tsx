import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import InputText from '../../../components/InputText';
import Button from '../../../components/Button';
import useBot from '../../../hooks/useBot';
import { useNavigate, useParams } from 'react-router-dom';
import { PiCaretLeft, PiNote, PiPlus, PiTrash } from 'react-icons/pi';
import Textarea from '../../../components/Textarea';
import DialogInstructionsSamples from '../../../components/DialogInstructionsSamples';
import ButtonIcon from '../../../components/ButtonIcon';
import { produce } from 'immer';
import Alert from '../../../components/Alert';
import KnowledgeFileUploader from '../../../components/KnowledgeFileUploader';
import GenerationConfig from '../../../components/GenerationConfig';
import Select from '../../../components/Select';
import { BotFile, ConversationQuickStarter } from '../../../@types/bot';

import { ulid } from 'ulid';
import {
  EDGE_GENERATION_PARAMS,
  EDGE_MISTRAL_GENERATION_PARAMS,
  DEFAULT_GENERATION_CONFIG,
  DEFAULT_MISTRAL_GENERATION_CONFIG,
  EDGE_SEARCH_PARAMS,
  TooltipDirection,
} from '../../../constants';
import { Slider } from '../../../components/Slider';
import ExpandableDrawerGroup from '../../../components/ExpandableDrawerGroup';
import useErrorMessage from '../../../hooks/useErrorMessage';
import Help from '../../../components/Help';
import Toggle from '../../../components/Toggle';
import { useAgent } from '../../../features/agent/hooks/useAgent';
import { AgentTool } from '../../../features/agent/types';
import { AvailableTools } from '../../../features/agent/components/AvailableTools';
import {
  DEFAULT_CHUNKING_MAX_TOKENS,
  DEFAULT_CHUNKING_OVERLAP_PERCENTAGE,
  EDGE_CHUNKING_MAX_TOKENS,
  EDGE_CHUNKING_OVERLAP_PERCENTAGE,
  OPENSEARCH_ANALYZER,
  DEFAULT_SEARCH_CONFIG,
  DEFAULT_OPENSEARCH_ANALYZER,
} from '../constants';
import {
  GUARDRAILS_FILTERS_THRESHOLD,
  GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD,
} from '../../../constants';
import {
  ChunkingStrategy,
  EmbeddingsModel,
  OpenSearchParams,
  SearchParams,
  SearchType,
} from '../types';

const edgeGenerationParams =
  import.meta.env.VITE_APP_ENABLE_MISTRAL === 'true'
    ? EDGE_MISTRAL_GENERATION_PARAMS
    : EDGE_GENERATION_PARAMS;

const defaultGenerationConfig =
  import.meta.env.VITE_APP_ENABLE_MISTRAL === 'true'
    ? DEFAULT_MISTRAL_GENERATION_CONFIG
    : DEFAULT_GENERATION_CONFIG;

const BotKbEditPage: React.FC = () => {
  const { i18n, t } = useTranslation();
  const navigate = useNavigate();
  const { botId: paramsBotId } = useParams();
  const { getMyBot, registerBot, updateBot } = useBot();
  const { availableTools } = useAgent();

  const [isLoading, setIsLoading] = useState(false);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [instruction, setInstruction] = useState('');
  const [urls, setUrls] = useState<string[]>(['']);
  const [s3Urls, setS3Urls] = useState<string[]>(['']);
  const [files, setFiles] = useState<BotFile[]>([]);
  const [addedFilenames, setAddedFilenames] = useState<string[]>([]);
  const [unchangedFilenames, setUnchangedFilenames] = useState<string[]>([]);
  const [deletedFilenames, setDeletedFilenames] = useState<string[]>([]);
  const [displayRetrievedChunks, setDisplayRetrievedChunks] = useState(true);
  const [maxTokens, setMaxTokens] = useState<number>(
    defaultGenerationConfig.maxTokens
  );
  const [topK, setTopK] = useState<number>(defaultGenerationConfig.topK);
  const [topP, setTopP] = useState<number>(defaultGenerationConfig.topP);
  const [temperature, setTemperature] = useState<number>(
    defaultGenerationConfig.temperature
  );
  const [stopSequences, setStopSequences] = useState<string>(
    defaultGenerationConfig.stopSequences?.join(',') || ''
  );
  const [tools, setTools] = useState<AgentTool[]>([]);
  const [conversationQuickStarters, setConversationQuickStarters] = useState<
    ConversationQuickStarter[]
  >([
    {
      title: '',
      example: '',
    },
  ]);

  const [knowledgeBaseId, setKnowledgeBaseId] = useState<string | null>(null); // Send null when creating a new bot
  const [embeddingsModel, setEmbeddingsModel] =
    useState<EmbeddingsModel>('titan_v2');

  const [hateThreshold, setHateThreshold] = useState<number>(0);
  const [insultsThreshold, setInsultsThreshold] = useState<number>(0);
  const [sexualThreshold, setSexualThreshold] = useState<number>(0);
  const [violenceThreshold, setViolenceThreshold] = useState<number>(0);
  const [misconductThreshold, setMisconductThreshold] = useState<number>(0);
  const [groundingThreshold, setGroundingThreshold] = useState<number>(0);
  const [relevanceThreshold, setRelevanceThreshold] = useState<number>(0);
  const [guardrailArn, setGuardrailArn] = useState<string>('');
  const [guardrailVersion, setGuardrailVersion] = useState<string>('');

  const embeddingsModelOptions: {
    label: string;
    value: EmbeddingsModel;
  }[] = [
    {
      label: t('knowledgeBaseSettings.embeddingModel.titan_v2.label'),
      value: 'titan_v2',
    },
    {
      label: t(
        'knowledgeBaseSettings.embeddingModel.cohere_multilingual_v3.label'
      ),
      value: 'cohere_multilingual_v3',
    },
  ];

  const [chunkingStrategy, setChunkingStrategy] =
    useState<ChunkingStrategy>('default');

  const chunkingStrategyOptions: {
    label: string;
    value: ChunkingStrategy;
    description: string;
  }[] = [
    {
      label: t('knowledgeBaseSettings.chunkingStrategy.default.label'),
      value: 'default',
      description: t('knowledgeBaseSettings.chunkingStrategy.default.hint'),
    },
    {
      label: t('knowledgeBaseSettings.chunkingStrategy.fixed_size.label'),
      value: 'fixed_size',
      description: t('knowledgeBaseSettings.chunkingStrategy.fixed_size.hint'),
    },
    {
      label: t('knowledgeBaseSettings.chunkingStrategy.none.label'),
      value: 'none',
      description: t('knowledgeBaseSettings.chunkingStrategy.none.hint'),
    },
  ];

  const [chunkingMaxTokens, setChunkingMaxTokens] = useState<number>(
    DEFAULT_CHUNKING_MAX_TOKENS
  );

  const [chunkingOverlapPercentage, setChunkingOverlapPercentage] =
    useState<number>(DEFAULT_CHUNKING_OVERLAP_PERCENTAGE);

  const [analyzer, setAnalyzer] = useState<string>(
    DEFAULT_OPENSEARCH_ANALYZER[i18n.language] ?? 'none'
  );

  const [openSearchParams, setOpenSearchParams] = useState<OpenSearchParams>(
    DEFAULT_OPENSEARCH_ANALYZER[i18n.language]
      ? OPENSEARCH_ANALYZER[DEFAULT_OPENSEARCH_ANALYZER[i18n.language]]
      : OPENSEARCH_ANALYZER['none']
  );

  const analyzerOptions: {
    label: string;
    value: string;
    description: string;
  }[] = [
    {
      label: t('knowledgeBaseSettings.opensearchAnalyzer.icu.label'),
      value: 'icu',
      description: t('knowledgeBaseSettings.opensearchAnalyzer.icu.hint', {
        tokenizer: OPENSEARCH_ANALYZER['icu'].analyzer!.tokenizer,
        normalizer: OPENSEARCH_ANALYZER['icu'].analyzer!.characterFilters,
      }),
    },
    {
      label: t('knowledgeBaseSettings.opensearchAnalyzer.kuromoji.label'),
      value: 'kuromoji',
      description: t('knowledgeBaseSettings.opensearchAnalyzer.kuromoji.hint', {
        tokenizer: OPENSEARCH_ANALYZER['kuromoji'].analyzer!.tokenizer,
        normalizer: OPENSEARCH_ANALYZER['icu'].analyzer!.characterFilters,
      }),
    },
    {
      label: t('knowledgeBaseSettings.opensearchAnalyzer.none.label'),
      value: 'none',
      description: t('knowledgeBaseSettings.opensearchAnalyzer.none.hint'),
    },
  ];

  const [searchParams, setSearchParams] = useState<SearchParams>(
    DEFAULT_SEARCH_CONFIG
  );

  const searchTypeOptions: {
    label: string;
    value: SearchType;
    description: string;
  }[] = [
    {
      label: t('searchSettings.searchType.hybrid.label'),
      value: 'hybrid',
      description: t('searchSettings.searchType.hybrid.hint'),
    },
    {
      label: t('searchSettings.searchType.semantic.label'),
      value: 'semantic',
      description: t('searchSettings.searchType.semantic.hint'),
    },
  ];

  const {
    errorMessages,
    setErrorMessage: setErrorMessages,
    clearAll: clearErrorMessages,
  } = useErrorMessage();

  const isNewBot = useMemo(() => {
    return paramsBotId ? false : true;
  }, [paramsBotId]);

  const botId = useMemo(() => {
    return isNewBot ? ulid() : (paramsBotId ?? '');
  }, [isNewBot, paramsBotId]);

  useEffect(() => {
    if (!isNewBot) {
      setIsLoading(true);
      getMyBot(botId)
        .then((bot) => {
          // Disallow editing of bots created under opposite VITE_APP_ENABLE_KB environment state
          if (!bot.bedrockKnowledgeBase) {
            navigate('/');
            return;
          }

          setTools(bot.agent.tools);
          setTitle(bot.title);
          setDescription(bot.description);
          setInstruction(bot.instruction);
          setUrls(
            bot.knowledge.sourceUrls.length === 0
              ? ['']
              : bot.knowledge.sourceUrls
          );
          setS3Urls(
            bot.knowledge.s3Urls.length === 0 ? [''] : bot.knowledge.s3Urls
          );
          setFiles(
            bot.knowledge.filenames.map((filename) => ({
              filename,
              status: 'UPLOADED',
            }))
          );
          setTopK(bot.generationParams.topK);
          setTopP(bot.generationParams.topP);
          setTemperature(bot.generationParams.temperature);
          setMaxTokens(bot.generationParams.maxTokens);
          setStopSequences(bot.generationParams.stopSequences.join(','));
          setUnchangedFilenames([...bot.knowledge.filenames]);
          setDisplayRetrievedChunks(bot.displayRetrievedChunks);
          if (bot.syncStatus === 'FAILED') {
            setErrorMessages(
              isSyncChunkError(bot.syncStatusReason)
                ? 'syncChunkError'
                : 'syncError',
              bot.syncStatusReason
            );
          }
          setConversationQuickStarters(
            bot.conversationQuickStarters.length > 0
              ? bot.conversationQuickStarters
              : [
                  {
                    title: '',
                    example: '',
                  },
                ]
          );
          setKnowledgeBaseId(bot.bedrockKnowledgeBase.knowledgeBaseId);
          setEmbeddingsModel(bot.bedrockKnowledgeBase!.embeddingsModel);
          setChunkingStrategy(bot.bedrockKnowledgeBase!.chunkingStrategy);
          setChunkingMaxTokens(
            bot.bedrockKnowledgeBase!.maxTokens ?? DEFAULT_CHUNKING_MAX_TOKENS
          );
          setChunkingOverlapPercentage(
            bot.bedrockKnowledgeBase!.overlapPercentage ??
              DEFAULT_CHUNKING_OVERLAP_PERCENTAGE
          );
          setOpenSearchParams(bot.bedrockKnowledgeBase!.openSearch);
          setSearchParams(bot.bedrockKnowledgeBase!.searchParams);
          setGuardrailArn(bot.bedrockGuardrails.guardrailArn);
          setGuardrailVersion(
            bot.bedrockGuardrails.guardrailVersion
              ? bot.bedrockGuardrails.guardrailVersion
              : ''
          );
          setHateThreshold(
            bot.bedrockGuardrails.hateThreshold
              ? bot.bedrockGuardrails.hateThreshold
              : 0
          );
          setInsultsThreshold(
            bot.bedrockGuardrails.insultsThreshold
              ? bot.bedrockGuardrails.insultsThreshold
              : 0
          );
          setSexualThreshold(
            bot.bedrockGuardrails.sexualThreshold
              ? bot.bedrockGuardrails.sexualThreshold
              : 0
          );
          setViolenceThreshold(
            bot.bedrockGuardrails.violenceThreshold
              ? bot.bedrockGuardrails.violenceThreshold
              : 0
          );
          setMisconductThreshold(
            bot.bedrockGuardrails.misconductThreshold
              ? bot.bedrockGuardrails.misconductThreshold
              : 0
          );
          setGroundingThreshold(
            bot.bedrockGuardrails.groundingThreshold
              ? bot.bedrockGuardrails.groundingThreshold
              : 0
          );
          setRelevanceThreshold(
            bot.bedrockGuardrails.relevanceThreshold
              ? bot.bedrockGuardrails.relevanceThreshold
              : 0
          );
        })
        .finally(() => {
          setIsLoading(false);
        });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isNewBot, botId]);

  const isSyncChunkError = useCallback((syncErrorMessage: string) => {
    const pattern =
      /Got a larger chunk overlap \(\d+\) than chunk size \(\d+\), should be smaller\./;
    return pattern.test(syncErrorMessage);
  }, []);

  const onChangeS3Url = useCallback(
    (s3Url: string, idx: number) => {
      setS3Urls(
        produce(s3Urls, (draft) => {
          draft[idx] = s3Url;
        })
      );
    },
    [s3Urls]
  );

  const onClickAddS3Url = useCallback(() => {
    setS3Urls([...s3Urls, '']);
  }, [s3Urls]);

  const onClickRemoveS3Url = useCallback(
    (idx: number) => {
      setS3Urls(
        produce(s3Urls, (draft) => {
          draft.splice(idx, 1);
          if (draft.length === 0) {
            draft.push('');
          }
          return;
        })
      );
    },
    [s3Urls]
  );

  const removeUnchangedFilenames = useCallback(
    (filename: string) => {
      const idx = unchangedFilenames.findIndex(
        (unchangedFilename) => unchangedFilename === filename
      );
      if (idx > -1) {
        setUnchangedFilenames(
          produce(unchangedFilenames, (draft) => {
            draft.splice(idx, 1);
            return;
          })
        );
      }
    },
    [unchangedFilenames]
  );

  const removeAddedFilenames = useCallback(
    (filename: string) => {
      const idx = addedFilenames.findIndex(
        (addedFilename) => addedFilename === filename
      );
      if (idx > -1) {
        setAddedFilenames(
          produce(addedFilenames, (draft) => {
            draft.splice(idx, 1);
            return;
          })
        );
      }
    },
    [addedFilenames]
  );

  const removeDeletedFilenames = useCallback(
    (filename: string) => {
      const idx = deletedFilenames.findIndex(
        (deletedFilename) => deletedFilename === filename
      );
      if (idx > -1) {
        setDeletedFilenames(
          produce(deletedFilenames, (draft) => {
            draft.splice(idx, 1);
          })
        );
      }
    },
    [deletedFilenames]
  );

  const onAddFiles = useCallback(
    (botFiles: BotFile[]) => {
      setFiles(botFiles);
      setAddedFilenames(
        produce(addedFilenames, (draft) => {
          botFiles.forEach((file) => {
            if (file.status === 'UPLOADING') {
              if (!draft.includes(file.filename)) {
                draft.push(file.filename);
              }
              removeUnchangedFilenames(file.filename);
              removeDeletedFilenames(file.filename);
            }
          });
        })
      );
    },
    [addedFilenames, removeDeletedFilenames, removeUnchangedFilenames]
  );

  const onUpdateFiles = useCallback((botFiles: BotFile[]) => {
    setFiles(botFiles);
  }, []);

  const onDeleteFiles = useCallback(
    (botFiles: BotFile[], deletedFilename: string) => {
      setFiles(botFiles);

      if (!deletedFilenames.includes(deletedFilename)) {
        setDeletedFilenames(
          produce(deletedFilenames, (draft) => {
            draft.push(deletedFilename);
          })
        );
      }
      removeAddedFilenames(deletedFilename);
      removeUnchangedFilenames(deletedFilename);
    },
    [deletedFilenames, removeAddedFilenames, removeUnchangedFilenames]
  );

  const addQuickStarter = useCallback(() => {
    setConversationQuickStarters(
      produce(conversationQuickStarters, (draft) => {
        draft.push({
          title: '',
          example: '',
        });
      })
    );
  }, [conversationQuickStarters]);

  const updateQuickStarter = useCallback(
    (quickStart: ConversationQuickStarter, index: number) => {
      setConversationQuickStarters(
        produce(conversationQuickStarters, (draft) => {
          draft[index] = quickStart;
        })
      );
    },
    [conversationQuickStarters]
  );

  const removeQuickStarter = useCallback(
    (index: number) => {
      setConversationQuickStarters(
        produce(conversationQuickStarters, (draft) => {
          draft.splice(index, 1);
          if (draft.length === 0) {
            draft.push({
              title: '',
              example: '',
            });
          }
        })
      );
    },
    [conversationQuickStarters]
  );

  const onChangeEmbeddingsModel = useCallback(
    (value: EmbeddingsModel) => {
      setEmbeddingsModel(value);
      // Update maxTokens based on the selected embeddings model
      const maxEdge = EDGE_CHUNKING_MAX_TOKENS.MAX[value];
      if (chunkingMaxTokens > maxEdge) {
        setChunkingMaxTokens(maxEdge);
      }
    },
    [chunkingMaxTokens]
  );

  const onClickBack = useCallback(() => {
    history.back();
  }, []);

  const isValidGenerationConfigParam = useCallback(
    (value: number, key: 'maxTokens' | 'topK' | 'topP' | 'temperature') => {
      if (value < edgeGenerationParams[key].MIN) {
        setErrorMessages(
          key,
          t('validation.minRange.message', {
            size: edgeGenerationParams[key].MIN,
          })
        );
        return false;
      } else if (value > edgeGenerationParams[key].MAX) {
        setErrorMessages(
          key,
          t('validation.maxRange.message', {
            size: edgeGenerationParams[key].MAX,
          })
        );
        return false;
      }

      return true;
    },
    [setErrorMessages, t]
  );

  const isValid = useCallback((): boolean => {
    clearErrorMessages();

    // S3 URLs validation - s3://example-bucket/path/to/data-source/
    const isS3UrlsValid = s3Urls.every((url, idx) => {
      if (url && !/^s3:\/\/[a-z0-9.-]+\/.+/.test(url)) {
        setErrorMessages(`s3Urls-${idx}`, 'S3 URL is invalid');
        return false;
      } else {
        return true;
      }
    });
    if (!isS3UrlsValid) {
      return false;
    }

    // Chunking Strategy params validation
    if (chunkingStrategy === 'fixed_size') {
      if (chunkingMaxTokens < EDGE_CHUNKING_MAX_TOKENS.MIN) {
        setErrorMessages(
          'chunkingMaxTokens',
          t('validation.minRange.message', {
            size: EDGE_CHUNKING_MAX_TOKENS.MIN,
          })
        );
        return false;
      } else if (
        chunkingMaxTokens > EDGE_CHUNKING_MAX_TOKENS.MAX[embeddingsModel]
      ) {
        setErrorMessages(
          'chunkingMaxTokens',
          t('validation.maxRange.message', {
            size: EDGE_CHUNKING_MAX_TOKENS.MAX[embeddingsModel],
          })
        );
        return false;
      }

      if (chunkingOverlapPercentage < EDGE_CHUNKING_OVERLAP_PERCENTAGE.MIN) {
        setErrorMessages(
          'chunkingOverlapPercentage',
          t('validation.minRange.message', {
            size: EDGE_CHUNKING_OVERLAP_PERCENTAGE.MIN,
          })
        );
        return false;
      } else if (
        chunkingOverlapPercentage > EDGE_CHUNKING_OVERLAP_PERCENTAGE.MAX
      ) {
        setErrorMessages(
          'chunkingOverlapPercentage',
          t('validation.maxRange.message', {
            size: EDGE_CHUNKING_OVERLAP_PERCENTAGE.MAX,
          })
        );
        return false;
      }
    }

    if (stopSequences.length === 0) {
      setErrorMessages('stopSequences', t('input.validationError.required'));
      return false;
    }

    if (searchParams.maxResults < EDGE_SEARCH_PARAMS.maxResults.MIN) {
      setErrorMessages(
        'maxResults',
        t('validation.minRange.message', {
          size: EDGE_SEARCH_PARAMS.maxResults.MIN,
        })
      );
      return false;
    } else if (searchParams.maxResults > EDGE_SEARCH_PARAMS.maxResults.MAX) {
      setErrorMessages(
        'maxResults',
        t('validation.maxRange.message', {
          size: EDGE_SEARCH_PARAMS.maxResults.MAX,
        })
      );
      return false;
    }

    const isQsValid = conversationQuickStarters.every((rs, idx) => {
      if ((!rs.title && !!rs.example) || (!!rs.title && !rs.example)) {
        setErrorMessages(
          `conversationQuickStarter${idx}`,
          t('validation.quickStarter.message')
        );
        return false;
      } else {
        return true;
      }
    });
    if (!isQsValid) {
      return false;
    }

    return (
      isValidGenerationConfigParam(maxTokens, 'maxTokens') &&
      isValidGenerationConfigParam(topK, 'topK') &&
      isValidGenerationConfigParam(topP, 'topP') &&
      isValidGenerationConfigParam(temperature, 'temperature')
    );
  }, [
    clearErrorMessages,
    s3Urls,
    stopSequences.length,
    searchParams.maxResults,
    conversationQuickStarters,
    isValidGenerationConfigParam,
    maxTokens,
    topK,
    topP,
    temperature,
    setErrorMessages,
    embeddingsModel,
    chunkingStrategy,
    chunkingMaxTokens,
    chunkingOverlapPercentage,
    t,
  ]);

  const onClickCreate = useCallback(() => {
    if (!isValid()) {
      return;
    }
    setIsLoading(true);
    registerBot({
      agent: {
        tools: tools.map(({ name }) => name),
      },
      id: botId,
      title,
      description,
      instruction,
      embeddingParams: null,
      generationParams: {
        maxTokens,
        temperature,
        topK,
        topP,
        stopSequences: stopSequences.split(','),
      },
      searchParams: {
        // set same value as bedrockKnowledgeBase.searchParams
        maxResults: searchParams.maxResults,
      },
      knowledge: {
        sourceUrls: urls.filter((s) => s !== ''),
        // Sitemap cannot be used yet.
        sitemapUrls: [],
        s3Urls: s3Urls.filter((s) => s !== ''),
        filenames: files.map((f) => f.filename),
      },
      displayRetrievedChunks,
      conversationQuickStarters: conversationQuickStarters.filter(
        (qs) => qs.title !== '' && qs.example !== ''
      ),
      bedrockKnowledgeBase: {
        knowledgeBaseId,
        embeddingsModel,
        chunkingStrategy,
        maxTokens: chunkingStrategy == 'fixed_size' ? chunkingMaxTokens : null,
        overlapPercentage:
          chunkingStrategy == 'fixed_size' ? chunkingOverlapPercentage : null,
        openSearch: openSearchParams,
        searchParams: searchParams,
      },
      bedrockGuardrails: {
        isGuardrailEnabled:
          hateThreshold > 0 ||
          insultsThreshold > 0 ||
          sexualThreshold > 0 ||
          violenceThreshold > 0 ||
          misconductThreshold > 0 ||
          groundingThreshold > 0 ||
          relevanceThreshold > 0,
        hateThreshold: hateThreshold,
        insultsThreshold: insultsThreshold,
        sexualThreshold: sexualThreshold,
        violenceThreshold: violenceThreshold,
        misconductThreshold: misconductThreshold,
        groundingThreshold: groundingThreshold,
        relevanceThreshold: relevanceThreshold,
        guardrailArn: '',
        guardrailVersion: '',
      },
    })
      .then(() => {
        navigate('/bot/explore');
      })
      .catch(() => {
        setIsLoading(false);
      });
  }, [
    isValid,
    registerBot,
    tools,
    botId,
    title,
    description,
    instruction,
    maxTokens,
    temperature,
    topK,
    topP,
    stopSequences,
    searchParams,
    urls,
    s3Urls,
    files,
    displayRetrievedChunks,
    conversationQuickStarters,
    navigate,
    knowledgeBaseId,
    embeddingsModel,
    chunkingStrategy,
    chunkingMaxTokens,
    chunkingOverlapPercentage,
    openSearchParams,
    hateThreshold,
    insultsThreshold,
    sexualThreshold,
    violenceThreshold,
    misconductThreshold,
    groundingThreshold,
    relevanceThreshold,
  ]);

  const onClickEdit = useCallback(() => {
    if (!isValid()) {
      return;
    }
    if (!isNewBot) {
      setIsLoading(true);
      updateBot(botId, {
        agent: {
          tools: tools.map(({ name }) => name),
        },
        title,
        description,
        instruction,
        embeddingParams: null,
        generationParams: {
          maxTokens,
          temperature,
          topK,
          topP,
          stopSequences: stopSequences.split(','),
        },
        searchParams: {
          // set same value as bedrockKnowledgeBase.searchParams
          maxResults: searchParams.maxResults,
        },
        knowledge: {
          sourceUrls: urls.filter((s) => s !== ''),
          // Sitemap cannot be used yet.
          sitemapUrls: [],
          s3Urls: s3Urls.filter((s) => s !== ''),
          addedFilenames,
          deletedFilenames,
          unchangedFilenames,
        },
        displayRetrievedChunks,
        conversationQuickStarters: conversationQuickStarters.filter(
          (qs) => qs.title !== '' && qs.example !== ''
        ),
        bedrockKnowledgeBase: {
          knowledgeBaseId,
          embeddingsModel,
          chunkingStrategy,
          maxTokens:
            chunkingStrategy == 'fixed_size' ? chunkingMaxTokens : null,
          overlapPercentage:
            chunkingStrategy == 'fixed_size' ? chunkingOverlapPercentage : null,
          openSearch: openSearchParams,
          searchParams: searchParams,
        },
        bedrockGuardrails: {
          isGuardrailEnabled:
            hateThreshold > 0 ||
            insultsThreshold > 0 ||
            sexualThreshold > 0 ||
            violenceThreshold > 0 ||
            misconductThreshold > 0 ||
            groundingThreshold > 0 ||
            relevanceThreshold > 0,
          hateThreshold: hateThreshold,
          insultsThreshold: insultsThreshold,
          sexualThreshold: sexualThreshold,
          violenceThreshold: violenceThreshold,
          misconductThreshold: misconductThreshold,
          groundingThreshold: groundingThreshold,
          relevanceThreshold: relevanceThreshold,
          guardrailArn: guardrailArn,
          guardrailVersion: guardrailVersion,
        },
      })
        .then(() => {
          navigate('/bot/explore');
        })
        .catch(() => {
          setIsLoading(false);
        });
    }
  }, [
    isValid,
    isNewBot,
    updateBot,
    botId,
    tools,
    title,
    description,
    instruction,
    maxTokens,
    temperature,
    topK,
    topP,
    stopSequences,
    searchParams,
    urls,
    s3Urls,
    addedFilenames,
    deletedFilenames,
    unchangedFilenames,
    displayRetrievedChunks,
    conversationQuickStarters,
    navigate,
    knowledgeBaseId,
    embeddingsModel,
    chunkingStrategy,
    chunkingMaxTokens,
    chunkingOverlapPercentage,
    openSearchParams,
    hateThreshold,
    insultsThreshold,
    sexualThreshold,
    violenceThreshold,
    misconductThreshold,
    groundingThreshold,
    relevanceThreshold,
    guardrailArn,
    guardrailVersion,
  ]);

  const [isOpenSamples, setIsOpenSamples] = useState(false);

  const disabledRegister = useMemo(() => {
    return title === '' || files.findIndex((f) => f.status !== 'UPLOADED') > -1;
  }, [files, title]);

  return (
    <>
      <DialogInstructionsSamples
        isOpen={isOpenSamples}
        onClose={() => {
          setIsOpenSamples(false);
        }}
      />
      <div className="mb-20 flex justify-center">
        <div className="w-2/3">
          <div className="mt-5 w-full">
            <div className="text-xl font-bold">
              {isNewBot ? t('bot.create.pageTitle') : t('bot.edit.pageTitle')}
            </div>

            <div className="mt-3 flex flex-col gap-3">
              <InputText
                label={t('bot.item.title')}
                disabled={isLoading}
                value={title}
                onChange={setTitle}
                hint={t('input.hint.required')}
              />
              <InputText
                label={t('bot.item.description')}
                disabled={isLoading}
                value={description}
                onChange={setDescription}
              />
              <div className="relative mt-3">
                <Button
                  className="absolute -top-3 right-0 text-xs"
                  outlined
                  onClick={() => {
                    setIsOpenSamples(true);
                  }}>
                  <PiNote className="mr-1" />
                  {t('bot.button.instructionsSamples')}
                </Button>
                <Textarea
                  label={t('bot.item.instruction')}
                  disabled={isLoading}
                  rows={5}
                  hint={t('bot.help.instructions')}
                  value={instruction}
                  onChange={setInstruction}
                />
              </div>

              <div className="mt-3" />
              <AvailableTools
                availableTools={availableTools}
                tools={tools}
                setTools={setTools}
              />

              <div className="mt-3">
                <div className="flex items-center gap-1">
                  <div className="text-lg font-bold">
                    {t('bot.label.knowledge')}
                  </div>
                </div>

                <div className="text-sm text-aws-font-color/50">
                  {t('bot.help.knowledge.overview')}
                </div>

                {errorMessages['syncError'] && (
                  <Alert
                    className="mt-2"
                    severity="error"
                    title={t('bot.alert.sync.error.title')}>
                    <>
                      <div className="mb-1 text-sm">
                        <div>{t('bot.alert.sync.error.body')}</div>
                        <div> {errorMessages['syncError']}</div>
                      </div>
                    </>
                  </Alert>
                )}

                <div className="mt-3">
                  <div className="font-semibold">{t('bot.label.file')}</div>
                  <div className="text-sm text-aws-font-color/50">
                    {t('bot.help.knowledge.file')}
                  </div>
                  <div className="mt-2 flex w-full flex-col gap-1">
                    <KnowledgeFileUploader
                      className="h-48"
                      botId={botId}
                      files={files}
                      onAdd={onAddFiles}
                      onUpdate={onUpdateFiles}
                      onDelete={onDeleteFiles}
                    />
                  </div>
                </div>

                <div className="mt-4">
                  <div className="font-semibold">{t('bot.label.s3url')}</div>
                  <div className="text-sm text-aws-font-color/50">
                    {t('bot.help.knowledge.s3url')}
                  </div>
                  <div className="mt-2 flex w-full flex-col gap-1">
                    {s3Urls.map((s3Url, idx) => (
                      <div className="flex w-full gap-2" key={idx}>
                        <InputText
                          className="w-full"
                          type="text"
                          disabled={isLoading}
                          value={s3Url}
                          placeholder={
                            's3://example-bucket/path/to/data-source/'
                          }
                          onChange={(s) => {
                            onChangeS3Url(s, idx);
                          }}
                          errorMessage={errorMessages[`s3Urls-${idx}`]}
                        />
                        <ButtonIcon
                          className="text-red"
                          disabled={
                            (s3Urls.length === 1 && !s3Url[0]) || isLoading
                          }
                          onClick={() => {
                            onClickRemoveS3Url(idx);
                          }}>
                          <PiTrash />
                        </ButtonIcon>
                      </div>
                    ))}
                  </div>
                  <div className="mt-2">
                    <Button
                      outlined
                      icon={<PiPlus />}
                      disabled={s3Urls.length >= 4}
                      onClick={onClickAddS3Url}>
                      {t('button.add')}
                    </Button>
                  </div>
                </div>

                <div className="mt-4">
                  <div className="font-semibold">
                    {t('bot.label.citeRetrievedContexts')}
                  </div>
                  <div className="flex">
                    <Toggle
                      value={displayRetrievedChunks}
                      onChange={setDisplayRetrievedChunks}
                    />
                    <div className="whitespace-pre-wrap text-sm text-aws-font-color/50">
                      {t('bot.help.knowledge.citeRetrievedContexts')}
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-3">
                <div className="flex items-center gap-1">
                  <div className="text-lg font-bold">
                    {t('bot.label.quickStarter.title')}
                  </div>
                </div>

                <div className="text-sm text-aws-font-color/50">
                  {t('bot.help.quickStarter.overview')}
                </div>

                <div className="mt-2">
                  <div className="mt-2 flex w-full flex-col gap-1">
                    {conversationQuickStarters.map(
                      (conversationQuickStarter, idx) => (
                        <div
                          className="flex w-full flex-col gap-2 rounded border border-aws-font-color/50 p-2"
                          key={idx}>
                          <InputText
                            className="w-full"
                            placeholder={t(
                              'bot.label.quickStarter.exampleTitle'
                            )}
                            disabled={isLoading}
                            value={conversationQuickStarter.title}
                            onChange={(s) => {
                              updateQuickStarter(
                                {
                                  ...conversationQuickStarter,
                                  title: s,
                                },
                                idx
                              );
                            }}
                            errorMessage={
                              errorMessages[`conversationQuickStarter${idx}`]
                            }
                          />

                          <Textarea
                            className="w-full"
                            label={t('bot.label.quickStarter.example')}
                            disabled={isLoading}
                            rows={3}
                            value={conversationQuickStarter.example}
                            onChange={(s) => {
                              updateQuickStarter(
                                {
                                  ...conversationQuickStarter,
                                  example: s,
                                },
                                idx
                              );
                            }}
                          />
                          <div className="flex justify-end">
                            <Button
                              className="bg-red"
                              disabled={
                                (conversationQuickStarters.length === 1 &&
                                  !conversationQuickStarters[0].title &&
                                  !conversationQuickStarters[0].example) ||
                                isLoading
                              }
                              icon={<PiTrash />}
                              onClick={() => {
                                removeQuickStarter(idx);
                              }}>
                              {t('button.delete')}
                            </Button>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                  <div className="mt-2">
                    <Button
                      outlined
                      icon={<PiPlus />}
                      onClick={addQuickStarter}>
                      {t('button.add')}
                    </Button>
                  </div>
                </div>
              </div>

              <ExpandableDrawerGroup
                isDefaultShow={false}
                label={t('generationConfig.title')}
                className="py-2">
                <GenerationConfig
                  topK={topK}
                  setTopK={setTopK}
                  topP={topP}
                  setTopP={setTopP}
                  temperature={temperature}
                  setTemperature={setTemperature}
                  maxTokens={maxTokens}
                  setMaxTokens={setMaxTokens}
                  stopSequences={stopSequences}
                  setStopSequences={setStopSequences}
                  isLoading={isLoading}
                  errorMessages={errorMessages}
                />
              </ExpandableDrawerGroup>

              <ExpandableDrawerGroup
                isDefaultShow={false}
                label={t('knowledgeBaseSettings.title')}
                className="py-2">
                <div className="text-sm text-aws-font-color/50">
                  {t('knowledgeBaseSettings.description')}
                </div>

                <div className="mt-3">
                  <Select
                    label={t('knowledgeBaseSettings.embeddingModel.label')}
                    value={embeddingsModel}
                    options={embeddingsModelOptions}
                    onChange={(val) => {
                      onChangeEmbeddingsModel(val as EmbeddingsModel);
                    }}
                    disabled={!isNewBot}
                  />
                </div>

                <div className="mt-3">
                  <Select
                    label={t('knowledgeBaseSettings.chunkingStrategy.label')}
                    value={chunkingStrategy}
                    options={chunkingStrategyOptions}
                    onChange={(val) => {
                      setChunkingStrategy(val as ChunkingStrategy);
                    }}
                    disabled={!isNewBot}
                  />
                </div>
                {chunkingStrategy === 'fixed_size' && (
                  <>
                    <div className="mx-4 mt-2">
                      <Slider
                        value={chunkingMaxTokens}
                        hint={t('knowledgeBaseSettings.chunkingMaxTokens.hint')}
                        label={
                          <div className="flex items-center gap-1">
                            {t('knowledgeBaseSettings.chunkingMaxTokens.label')}
                            <Help
                              direction={TooltipDirection.RIGHT}
                              message={t('embeddingSettings.help.chunkSize')}
                            />
                          </div>
                        }
                        range={{
                          min: EDGE_CHUNKING_MAX_TOKENS.MIN,
                          max: EDGE_CHUNKING_MAX_TOKENS.MAX[embeddingsModel],
                          step: EDGE_CHUNKING_MAX_TOKENS.STEP,
                        }}
                        onChange={setChunkingMaxTokens}
                        disabled={!isNewBot}
                        errorMessage={errorMessages['chunkingMaxTokens']}
                      />
                    </div>
                    <div className="mx-4 mt-2">
                      <Slider
                        value={chunkingOverlapPercentage}
                        hint={t(
                          'knowledgeBaseSettings.chunkingOverlapPercentage.hint'
                        )}
                        label={
                          <div className="flex items-center gap-1">
                            {t(
                              'knowledgeBaseSettings.chunkingOverlapPercentage.label'
                            )}
                            <Help
                              direction={TooltipDirection.RIGHT}
                              message={t('embeddingSettings.help.chunkOverlap')}
                            />
                          </div>
                        }
                        range={{
                          min: EDGE_CHUNKING_OVERLAP_PERCENTAGE.MIN,
                          max: EDGE_CHUNKING_OVERLAP_PERCENTAGE.MAX,
                          step: EDGE_CHUNKING_OVERLAP_PERCENTAGE.STEP,
                        }}
                        onChange={(percentage) =>
                          setChunkingOverlapPercentage(percentage)
                        }
                        disabled={!isNewBot}
                        errorMessage={
                          errorMessages['chunkingOverlapPercentage']
                        }
                      />
                    </div>
                  </>
                )}

                {isNewBot && (
                  <div className="mt-3 grid gap-1">
                    <Select
                      label={t(
                        'knowledgeBaseSettings.opensearchAnalyzer.label'
                      )}
                      value={analyzer}
                      options={analyzerOptions}
                      onChange={(val) => {
                        setAnalyzer(val);
                        setOpenSearchParams(OPENSEARCH_ANALYZER[val]);
                      }}
                      className="mt-2"
                    />
                    <div className="text-sm text-aws-font-color/50">
                      {t('knowledgeBaseSettings.opensearchAnalyzer.hint')}
                    </div>
                  </div>
                )}
                {!isNewBot && (
                  <div className="mt-3 grid gap-1">
                    <div className="text-sm">
                      {t('knowledgeBaseSettings.opensearchAnalyzer.label')}
                    </div>
                    <div className="text-sm text-aws-font-color/50">
                      {t('knowledgeBaseSettings.opensearchAnalyzer.hint')}
                    </div>
                    <div
                      className="grid grid-cols-[auto_1fr] gap-2 rounded 
                      border border-aws-font-color/50 p-4 text-sm">
                      <div>
                        {t(
                          'knowledgeBaseSettings.opensearchAnalyzer.tokenizer'
                        )}
                      </div>
                      <div>
                        {openSearchParams.analyzer?.tokenizer ??
                          t(
                            'knowledgeBaseSettings.opensearchAnalyzer.not_specified'
                          )}
                      </div>
                      <div>
                        {t(
                          'knowledgeBaseSettings.opensearchAnalyzer.normalizer'
                        )}
                      </div>
                      <div>
                        {openSearchParams.analyzer?.characterFilters ??
                          t(
                            'knowledgeBaseSettings.opensearchAnalyzer.not_specified'
                          )}
                      </div>
                      <div>
                        {t(
                          'knowledgeBaseSettings.opensearchAnalyzer.token_filter'
                        )}
                      </div>
                      <div className="grid gap-2">
                        {openSearchParams.analyzer?.tokenFilters.join(', ') ??
                          t(
                            'knowledgeBaseSettings.opensearchAnalyzer.not_specified'
                          )}
                      </div>
                    </div>
                  </div>
                )}
              </ExpandableDrawerGroup>

              <ExpandableDrawerGroup
                isDefaultShow={false}
                label={t('searchSettings.title')}
                className="py-2">
                <div className="text-sm text-aws-font-color/50">
                  {t('searchSettings.description')}
                </div>
                <div className="mt-3">
                  <Slider
                    value={searchParams.maxResults}
                    hint={t('searchSettings.maxResults.hint')}
                    label={t('searchSettings.maxResults.label')}
                    range={{
                      min: EDGE_SEARCH_PARAMS.maxResults.MIN,
                      max: EDGE_SEARCH_PARAMS.maxResults.MAX,
                      step: EDGE_SEARCH_PARAMS.maxResults.STEP,
                    }}
                    onChange={(maxResults) =>
                      setSearchParams((params) => ({
                        ...params,
                        maxResults,
                      }))
                    }
                    errorMessage={errorMessages['maxResults']}
                  />
                </div>
                <div className="mt-3">
                  <Select
                    label={t('searchSettings.searchType.label')}
                    value={searchParams.searchType}
                    options={searchTypeOptions}
                    onChange={(searchType) => {
                      setSearchParams(
                        (params) =>
                          ({
                            ...params,
                            searchType,
                          }) as SearchParams
                      );
                    }}
                  />
                </div>
              </ExpandableDrawerGroup>

              <ExpandableDrawerGroup
                isDefaultShow={false}
                label={t('guardrails.harmfulCategories.label')}
                className="py-2">
                <div className="mt-2">
                  <Slider
                    value={hateThreshold}
                    hint={t('guardrails.harmfulCategories.hate.hint')}
                    label={t('guardrails.harmfulCategories.hate.label')}
                    range={{
                      min: GUARDRAILS_FILTERS_THRESHOLD.MIN,
                      max: GUARDRAILS_FILTERS_THRESHOLD.MAX,
                      step: GUARDRAILS_FILTERS_THRESHOLD.STEP,
                    }}
                    onChange={(hateThreshold) => {
                      setHateThreshold(hateThreshold);
                    }}
                    enableDecimal={true}
                    errorMessage={errorMessages['hateThreshold']}
                  />
                </div>
                <div className="mt-2">
                  <Slider
                    value={insultsThreshold}
                    hint={t('guardrails.harmfulCategories.insults.hint')}
                    label={t('guardrails.harmfulCategories.insults.label')}
                    range={{
                      min: GUARDRAILS_FILTERS_THRESHOLD.MIN,
                      max: GUARDRAILS_FILTERS_THRESHOLD.MAX,
                      step: GUARDRAILS_FILTERS_THRESHOLD.STEP,
                    }}
                    onChange={(insultsThreshold) => {
                      setInsultsThreshold(insultsThreshold);
                    }}
                    enableDecimal={true}
                    errorMessage={errorMessages['insultsThreshold']}
                  />
                </div>
                <div className="mt-2">
                  <Slider
                    value={sexualThreshold}
                    hint={t('guardrails.harmfulCategories.sexual.hint')}
                    label={t('guardrails.harmfulCategories.sexual.label')}
                    range={{
                      min: GUARDRAILS_FILTERS_THRESHOLD.MIN,
                      max: GUARDRAILS_FILTERS_THRESHOLD.MAX,
                      step: GUARDRAILS_FILTERS_THRESHOLD.STEP,
                    }}
                    onChange={(sexualThreshold) => {
                      setSexualThreshold(sexualThreshold);
                    }}
                    enableDecimal={true}
                    errorMessage={errorMessages['sexualThreshold']}
                  />
                </div>
                <div className="mt-2">
                  <Slider
                    value={violenceThreshold}
                    hint={t('guardrails.harmfulCategories.violence.hint')}
                    label={t('guardrails.harmfulCategories.violence.label')}
                    range={{
                      min: GUARDRAILS_FILTERS_THRESHOLD.MIN,
                      max: GUARDRAILS_FILTERS_THRESHOLD.MAX,
                      step: GUARDRAILS_FILTERS_THRESHOLD.STEP,
                    }}
                    onChange={(violenceThreshold) => {
                      setViolenceThreshold(violenceThreshold);
                    }}
                    enableDecimal={true}
                    errorMessage={errorMessages['violenceThreshold']}
                  />
                </div>
                <div className="mt-2">
                  <Slider
                    value={misconductThreshold}
                    hint={t('guardrails.harmfulCategories.misconduct.hint')}
                    label={t('guardrails.harmfulCategories.misconduct.label')}
                    range={{
                      min: GUARDRAILS_FILTERS_THRESHOLD.MIN,
                      max: GUARDRAILS_FILTERS_THRESHOLD.MAX,
                      step: GUARDRAILS_FILTERS_THRESHOLD.STEP,
                    }}
                    onChange={(misconductThreshold) => {
                      setMisconductThreshold(misconductThreshold);
                    }}
                    enableDecimal={true}
                    errorMessage={errorMessages['misconductThreshold']}
                  />
                </div>
              </ExpandableDrawerGroup>

              <ExpandableDrawerGroup
                isDefaultShow={false}
                label={t('guardrails.contextualGroundingCheck.label')}
                className="py-2">
                <div className="mt-2">
                  <Slider
                    value={groundingThreshold}
                    hint={t(
                      'guardrails.contextualGroundingCheck.groundingThreshold.hint'
                    )}
                    label={t(
                      'guardrails.contextualGroundingCheck.groundingThreshold.label'
                    )}
                    range={{
                      min: GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD.MIN,
                      max: GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD.MAX,
                      step: GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD.STEP,
                    }}
                    onChange={(groundingThreshold) => {
                      setGroundingThreshold(groundingThreshold);
                    }}
                    enableDecimal={true}
                    errorMessage={errorMessages['groundingThreshold']}
                  />
                </div>
                <div className="mt-2">
                  <Slider
                    value={relevanceThreshold}
                    hint={t(
                      'guardrails.contextualGroundingCheck.relevanceThreshold.hint'
                    )}
                    label={t(
                      'guardrails.contextualGroundingCheck.relevanceThreshold.label'
                    )}
                    range={{
                      min: GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD.MIN,
                      max: GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD.MAX,
                      step: GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD.STEP,
                    }}
                    onChange={(relevanceThreshold) => {
                      setRelevanceThreshold(relevanceThreshold);
                    }}
                    enableDecimal={true}
                    errorMessage={errorMessages['relevanceThreshold']}
                  />
                </div>
              </ExpandableDrawerGroup>

              {errorMessages['syncChunkError'] && (
                <Alert
                  className="mt-2"
                  severity="error"
                  title={t('embeddingSettings.alert.sync.error.title')}>
                  <>
                    <div className="mb-1 text-sm">
                      {t('embeddingSettings.alert.sync.error.body')}
                    </div>
                  </>
                </Alert>
              )}

              <div className="flex justify-between">
                <Button outlined icon={<PiCaretLeft />} onClick={onClickBack}>
                  {t('button.back')}
                </Button>

                {isNewBot ? (
                  <Button
                    onClick={onClickCreate}
                    loading={isLoading}
                    disabled={disabledRegister}>
                    {t('bot.button.create')}
                  </Button>
                ) : (
                  <Button
                    onClick={onClickEdit}
                    loading={isLoading}
                    disabled={disabledRegister}>
                    {t('bot.button.edit')}
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default BotKbEditPage;
