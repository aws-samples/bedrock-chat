import React, {
    useCallback,
    useEffect,
    useLayoutEffect,
    useMemo,
    useState,
    useRef,
  } from 'react';
  import InputChatContent from '../components/InputChatContent';
  import useChat from '../hooks/useChat';
  import ChatMessage from '../components/ChatMessage';
  import useScroll from '../hooks/useScroll';
  import { useNavigate, useParams } from 'react-router-dom';
  import {
    PiArrowsCounterClockwise,
    PiWarningCircleFill,
  } from 'react-icons/pi';
  import Button from '../components/Button';
  import { useTranslation } from 'react-i18next';
  import SwitchBedrockModel from '../components/SwitchBedrockModel';
  import useSnackbar from '../hooks/useSnackbar';
  import useBot from '../hooks/useBot';
  import useConversation from '../hooks/useConversation';
  import { ActiveModels, BotSummary } from '../@types/bot';
  import IconPinnedBot from '../components/IconPinnedBot.tsx';
  
  import { copyBotUrl, isPinnedBot, canBePinned } from '../utils/BotUtils';
  import { toCamelCase } from '../utils/StringUtils';
  import { produce } from 'immer';
  import StatusSyncBot from '../components/StatusSyncBot';
  import useBotSummary from '../hooks/useBotSummary';
  import useModel from '../hooks/useModel';
  import {
    AgentState,
    AgentToolsProps,
  } from '../features/agent/xstates/agentThink';
  import { getRelatedDocumentsOfToolUse } from '../features/agent/utils/AgentUtils';
  import { BottomHelper } from '../features/helper/components/BottomHelper';
  import { useIsWindows } from '../hooks/useIsWindows';
  import {
    DisplayMessageContent,
    Model,
    PutFeedbackRequest,
  } from '../@types/conversation.ts';
  import { AVAILABLE_MODEL_KEYS } from '../constants/index';
  import usePostMessageStreaming from '../hooks/usePostMessageStreaming.ts';
  import useLoginUser from '../hooks/useLoginUser';
  import useBotPinning from '../hooks/useBotPinning';
  import Skeleton from '../components/Skeleton.tsx';
  import { twMerge } from 'tailwind-merge';
  import ButtonStar from '../components/ButtonStar.tsx';
  import MenuBot from '../components/MenuBot.tsx';
  import { AttachmentType } from '../hooks/useChat';
  
  // Default model activation settings when no bot is selected
  const defaultActiveModels: ActiveModels = (() => {
    return Object.fromEntries(
      AVAILABLE_MODEL_KEYS.map((key: Model) => [toCamelCase(key), true])
    ) as ActiveModels;
  })();
  
  const SummarizeDocumentsPage: React.FC = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const { open: openSnackbar } = useSnackbar();
    const { errorDetail } = usePostMessageStreaming();
    const { isAdmin } = useLoginUser();
    const { pinBot, unpinBot } = useBotPinning();

    // chatbot response
    const [summary, setSummary] = useState('');
    const [keyPoints, setKeyPoints] = useState('');
    const [keyEntities, setKeyEntities] = useState('');
    const [userInput, setUserInput] = useState('');
    const bottomRef = useRef<HTMLDivElement | null>(null);

    // session history
    const [analysisHistory, setAnalysisHistory] = useState<Array<{
      id: string;
      userInput: string;
      summary: string;
      keyPoints: string;
      keyEntities: string;
      timestamp: Date;
    }>>([]);
  
    const {
      agentThinking,
      reasoningThinking,
      conversationError,
      postingMessage,
      newChat,
      postChat,
      messages,
      conversationId,
      setConversationId,
      hasError,
      retryPostChat,
      regenerate,
      continueGenerate,
      getPostedModel,
      loadingConversation,
      getShouldContinue,
      relatedDocuments,
      reasoningEnabled,
      setReasoningEnabled,
      supportReasoning,
    } = useChat();
  
    // Error Handling
    useEffect(() => {
      if (conversationError) {
        if (conversationError.response?.status === 404) {
          openSnackbar(t('error.notFoundConversation'));
          newChat();
          navigate('/');
        } else {
          openSnackbar(conversationError.message ?? '');
        }
      }
    }, [conversationError, navigate, newChat, openSnackbar, t]);
  
    const { isWindows } = useIsWindows();
  
    const { getBotId } = useConversation();
  
    const { scrollToBottom, scrollToTop } = useScroll();
  
    const { conversationId: paramConversationId, botId: paramBotId } =
      useParams();
  
    const botId = useMemo(() => {
      return paramBotId ?? getBotId(conversationId);
    }, [conversationId, getBotId, paramBotId]);
  
    const {
      data: bot,
      error: botError,
      isLoading: isLoadingBot,
      mutate: mutateBot,
    } = useBotSummary(botId ?? undefined);
  
    const [pageTitle, setPageTitle] = useState('');
    const [isAvailabilityBot, setIsAvailabilityBot] = useState(false);
  
    useEffect(() => {
      setIsAvailabilityBot(false);
      if (bot) {
        setIsAvailabilityBot(true);
        setPageTitle(bot.title);
      } else {
        setPageTitle(t('bot.label.normalChat'));
      }
      if (botError) {
        setPageTitle(t('bot.label.notAvailableBot'));
  
        // redirect to new chat(no bot chat) if not set conversationId
        if (!conversationId) {
          openSnackbar(t('error.cannotAccessBot'));
          newChat();
          navigate('/');
        }
      }
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [bot, botError]);
  
    const description = useMemo<string>(() => {
      if (!bot) {
        return '';
      } else {
        return bot.description;
      }
    }, [bot]);
  
    const disabledInput = useMemo(() => {
      return botId !== null && !isAvailabilityBot && !isLoadingBot;
    }, [botId, isAvailabilityBot, isLoadingBot]);
  
    useEffect(() => {
      setConversationId(paramConversationId ?? '');
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [paramConversationId]);
  
    const inputBotParams = useMemo(() => {
      return botId
        ? {
            botId: botId,
            hasKnowledge: bot?.hasKnowledge ?? false,
            hasAgent: bot?.hasAgent ?? false,
          }
        : undefined;
    }, [bot?.hasKnowledge, botId, bot?.hasAgent]);
  
    const onSend = useCallback(
      (
        content: string,
        enableReasoning: boolean,
        base64EncodedImages?: string[],
        attachments?: AttachmentType[]
      ) => {
        setUserInput(content);

        // Wrap the user's content with a structured summarization prompt
        const structuredPrompt = `Please analyze the following content and provide a structured response with:

        1. Summary: A concise overview of the main content
        2. Key Points: The most important points or findings (short bullet points)
        3. Key Entities: Important people, organizations, places, or concepts mentioned (bullet points only with names)

        Content to analyze:
        ${content}

        Please format your response with clear section headers.`;

        postChat({
          content: structuredPrompt,
          base64EncodedImages,
          attachments,
          bot: inputBotParams,
          enableReasoning,
        });

        // clear the summary contents
        setSummary('');
        setKeyPoints('');
        setKeyEntities('');
      },
      [inputBotParams, postChat]
    );

    useEffect(() => {
      if (bottomRef.current) {
        bottomRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    }, [messages]);
  
    const onRegenerate = useCallback(
      (enableReasoning: boolean) => {
        regenerate({
          bot: inputBotParams,
          enableReasoning,
        });
      },
      [inputBotParams, regenerate]
    );
  
    const onContinueGenerate = useCallback(() => {
      continueGenerate({ bot: inputBotParams });
    }, [inputBotParams, continueGenerate]);
  
    useLayoutEffect(() => {
      if (messages.length > 0) {
        scrollToBottom();
      } else {
        scrollToTop();
      }
    }, [messages, scrollToBottom, scrollToTop]);
  
    const { updateStarred } = useBot();
    const onClickBotEdit = useCallback(
      (botId: string) => {
        navigate(`/bot/edit/${botId}`);
      },
      [navigate]
    );
  
    const onClickStar = useCallback(async () => {
      if (!bot) {
        return;
      }
      const isStarred = !bot.isStarred;
      mutateBot(
        produce(bot, (draft) => {
          draft.isStarred = isStarred;
        }),
        {
          revalidate: false,
        }
      );
  
      updateStarred(bot.id, isStarred).finally(() => {
        mutateBot();
      });
    }, [bot, mutateBot, updateStarred]);
  
    const onClickCopyUrl = useCallback((botId: string) => {
      copyBotUrl(botId);
    }, []);
  
    const onClickSyncError = useCallback(() => {
      navigate(`/bot/edit/${bot?.id}`);
    }, [bot?.id, navigate]);
  
    const { disabledImageUpload } = useModel();
    const [dndMode, setDndMode] = useState(false);
    const onDragOver: React.DragEventHandler<HTMLDivElement> = useCallback(
      (e) => {
        if (!disabledImageUpload) {
          setDndMode(true);
        }
        e.preventDefault();
      },
      [disabledImageUpload]
    );
  
    const endDnd: React.DragEventHandler<HTMLDivElement> = useCallback((e) => {
      setDndMode(false);
      e.preventDefault();
    }, []);
  
    const focusInputRef = useRef<HTMLElement | null>(null);
  
    useEffect(() => {
      const handleKeyDown = (event: KeyboardEvent) => {
        const isNewConversationCommand = (() => {
          if (event.code !== 'KeyO') {
            return false;
          }
          if (isWindows) {
            return event.ctrlKey && event.shiftKey;
          } else {
            return event.metaKey && event.shiftKey;
          }
        })();
        const isFocusChatInputCommand = event.code === 'Escape' && event.shiftKey;
  
        if (isNewConversationCommand) {
          event.preventDefault();
  
          if (botId) {
            navigate(`/bot/${botId}`);
          } else {
            navigate('/');
          }
        } else if (isFocusChatInputCommand) {
          focusInputRef.current?.focus();
        }
      };
      document.addEventListener('keydown', handleKeyDown);
      return () => document.removeEventListener('keydown', handleKeyDown);
    });
  
    const ChatMessageWithRelatedDocuments: React.FC<{
      chatContent: DisplayMessageContent;
      isStreaming: boolean;
      onChangeMessageId?: (messageId: string) => void;
      onSubmit?: (messageId: string, content: string) => void;
      onSubmitFeedback?: (
        messageId: string,
        feedback: PutFeedbackRequest
      ) => void;
    }> = React.memo((props) => {
      const { chatContent: message } = props;
  
      const isReasoningActive = reasoningThinking.matches('active');
      const reasoning = useMemo(
        () => ({
          content: isReasoningActive ? reasoningThinking.context.content : '',
        }),
        [isReasoningActive]
      );
  
      const isAgentThinking = useMemo(
        () =>
          [AgentState.THINKING, AgentState.LEAVING].some(
            (v) => v === agentThinking.value
          ),
        []
      );
  
      const tools: AgentToolsProps[] | undefined = useMemo(() => {
        if (isAgentThinking) {
          if (agentThinking.context.tools.length > 0) {
            return agentThinking.context.tools;
          }
  
          if (bot?.hasAgent) {
            return [
              {
                thought: t('agent.progress.label'),
                tools: {},
              },
            ];
          }
  
          if (bot?.hasKnowledge) {
            return [
              {
                thought: t('bot.label.retrievingKnowledge'), // @@
                tools: {},
              },
            ];
          }
  
          return undefined;
        } else {
          if (bot?.hasKnowledge) {
            const pseudoToolUseId = message.id;
            const relatedDocumentsOfVectorSearch = getRelatedDocumentsOfToolUse(
              relatedDocuments,
              pseudoToolUseId
            );
            if (
              relatedDocumentsOfVectorSearch != null &&
              relatedDocumentsOfVectorSearch.length > 0
            ) {
              return [
                {
                  tools: {
                    [pseudoToolUseId]: {
                      name: 'knowledge_base_tool',
                      status: 'success',
                      input: {},
                      relatedDocuments: relatedDocumentsOfVectorSearch,
                    },
                  },
                },
              ];
            }
          }
  
          return undefined;
        }
      }, [isAgentThinking, message]);
  
      const relatedDocumentsForCitation = useMemo(
        () =>
          isAgentThinking
            ? agentThinking.context.relatedDocuments
            : relatedDocuments,
        [isAgentThinking]
      );
  
      return (
        <ChatMessage
          tools={tools}
          reasoning={reasoning}
          chatContent={message}
          isStreaming={props.isStreaming}
          relatedDocuments={relatedDocumentsForCitation}
          onChangeMessageId={props.onChangeMessageId}
          onSubmit={props.onSubmit}
          onSubmitFeedback={props.onSubmitFeedback}
        />
      );
    });
  
    const activeModels = useMemo(() => {
      if (!bot) {
        return defaultActiveModels;
      }
      const isActiveModelsEmpty =
        Object.keys(bot?.activeModels ?? {}).length === 0;
      return isActiveModelsEmpty ? defaultActiveModels : bot.activeModels;
    }, [bot]);
  
    const togglePinBot = useCallback(
      (bot: BotSummary) => {
        mutateBot(
          produce(bot, (draft) => {
            draft.sharedStatus = isPinnedBot(bot.sharedStatus)
              ? 'shared'
              : 'pinned@000';
          }),
          {
            revalidate: false,
          }
        );
  
        isPinnedBot(bot.sharedStatus)
          ? unpinBot(bot.id).finally(() => {
              mutateBot();
            })
          : pinBot(bot.id, 0).finally(() => {
              mutateBot();
            });
      },
      [mutateBot, pinBot, unpinBot]
    );
  
    const canSwitchPinned = useMemo(() => {
      return isAdmin && canBePinned(bot?.sharedScope ?? 'private');
    }, [bot?.sharedScope, isAdmin]);

    const parseChatbotResponse = useCallback((response: string) => {
      // simple parsing logic 
      const lines = response.split('\n');
      let currentSection = '';
      let summaryText = '';
      let pointsText = '';
      let entitiesText = '';

      for (const line of lines) {
        const trimmedLine = line.trim().toLowerCase();
        
        if (trimmedLine.includes('summary') || trimmedLine.includes('overview')) {
          currentSection = 'summary';
        } else if (trimmedLine.includes('key point') || trimmedLine.includes('main point')) {
          currentSection = 'points';
        } else if (trimmedLine.includes('key entit') || trimmedLine.includes('entity') || trimmedLine.includes('person') || trimmedLine.includes('organization')) {
          currentSection = 'entities';
        } else if (line.trim() && currentSection) {
          switch (currentSection) {
            case 'summary':
              summaryText += (summaryText ? '\n' : '') + line.trim();
              break;
            case 'points':
              pointsText += (pointsText ? '\n' : '') + line.trim();
              break;
            case 'entities':
                const cleanedLine = line.slice(2).trim();
                entitiesText += (entitiesText ? '\n' : '') + cleanedLine.trim();
                break;
          }
        }
      }

      if (summaryText) setSummary(summaryText);
      if (pointsText) setKeyPoints(pointsText);
      if (entitiesText) setKeyEntities(entitiesText);

      // if successfully summarized, add to session history
      if (summaryText || pointsText || entitiesText) {
        const newAnalysis = {
          id: Date.now().toString(),
          userInput: userInput,
          summary: summaryText,
          keyPoints: pointsText,
          keyEntities: entitiesText,
          timestamp: new Date()
        };
        setAnalysisHistory(prev => [newAnalysis, ...prev]);
      }
    }, []);

    useEffect(() => {
      if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        if (lastMessage.role === 'assistant') {
          const textContent = lastMessage.content
            .filter(content => content.contentType === 'text')
            .map(content => (content as any).body)
            .join('\n');
          
          if (textContent) {
            parseChatbotResponse(textContent);
          }
        }
      }
    }, [messages, parseChatbotResponse]);
  
    return (
      <div
        className="relative flex h-full flex-1 flex-col"
        onDragOver={onDragOver}
        onDrop={endDnd}
        onDragEnd={endDnd}>
        <div className="flex-1 overflow-hidden">
          <div className="sticky top-0 z-10 mb-1.5 flex h-14 w-full items-center justify-between border-b border-gray bg-aws-paper-light p-2 dark:bg-aws-paper-dark">
            <div className="flex w-full justify-between">
              <div className="p-2">
                <div className="mr-10 flex items-center whitespace-nowrap font-bold">
                  {isLoadingBot ? (
                    <Skeleton className="h-5 w-32" />
                  ) : (
                    <>
                      <IconPinnedBot
                        botSharedStatus={bot?.sharedStatus}
                        className="mr-1 text-aws-aqua"
                      />
                      {pageTitle}
                    </>
                  )}
                </div>
              </div>
  
              {isLoadingBot && (
                <div className="flex items-center gap-2">
                  <Skeleton className="h-5 w-32" />
                  <Skeleton className="size-7" />
                  <Skeleton className="h-7 w-12" />
                </div>
              )}
  
              {isAvailabilityBot && !isLoadingBot && (
                <div className="absolute -top-1 right-0 flex h-full items-center">
                  <div className="h-full w-12 bg-gradient-to-r from-transparent to-aws-paper-light dark:to-aws-paper-dark"></div>
                  <div className="flex items-center bg-aws-paper-light dark:bg-aws-paper-dark">
                    {bot?.owned && (
                      <StatusSyncBot
                        syncStatus={bot.syncStatus}
                        onClickError={onClickSyncError}
                      />
                    )}
  
                    <ButtonStar
                      isStarred={bot?.isStarred ?? false}
                      onClick={onClickStar}
                    />
  
                    <MenuBot
                      className="mx-1"
                      {...(bot?.owned && {
                        onClickEdit: () => {
                          onClickBotEdit(bot.id);
                        },
                      })}
                      {...(bot?.sharedScope !== 'private' && {
                        onClickCopyUrl: () => {
                          onClickCopyUrl(bot?.id ?? '');
                        },
                      })}
                      {...(canSwitchPinned
                        ? {
                            onClickSwitchPinned: () => {
                              bot && togglePinBot(bot);
                            },
                            isPinned: isPinnedBot(bot?.sharedStatus ?? ''),
                          }
                        : {
                            isPinned: undefined,
                            onClickSwitchPinned: undefined,
                          })}
                    />
                  </div>
                </div>
              )}
            </div>
            {getPostedModel() && (
              <div className="absolute right-2 top-10 text-xs text-dark-gray dark:text-light-gray">
                model: {getPostedModel()}
              </div>
            )}
          </div>
          <section className="relative size-full flex-1 overflow-auto pb-9">
            <div className="h-full">
              <div
                id="messages"
                role="presentation"
                className="flex h-full flex-col overflow-auto pb-16">
                { (
                  <div className="relative mb-[45vh]  flex w-full flex-col items-center justify-center">
                    {!loadingConversation && (
                      <SwitchBedrockModel
                        className="mb-6 mt-3 w-min"
                        activeModels={activeModels}
                        botId={botId}
                      />
                    )}
                    <div className="px-20">
                      <div className="px-10 text-lg font-bold">
                        {isLoadingBot && botId && (
                          <Skeleton className="h-5 w-32" />
                        )}
                        {!isLoadingBot && bot && (
                          <div className="flex items-baseline">
                            <IconPinnedBot
                              botSharedStatus={bot?.sharedStatus}
                              className="mr-1 shrink-0 text-aws-aqua"
                            />
                            <div>{pageTitle}</div>
                          </div>
                        )}
                      </div>
                      <div className="mt-3 text-xs text-dark-gray dark:text-light-gray">
                        {isLoadingBot ? (
                          <Skeleton className="mt-1 h-3 w-64" />
                        ) : (
                          description
                        )}
                      </div>
                    </div>
                  </div>
                )}
                {hasError && (
                  <div className="mb-12 mt-2 flex flex-col items-center">
                    <div className="flex items-center font-bold text-red">
                      <PiWarningCircleFill className="mr-1 text-2xl" />
                      {errorDetail ?? t('error.answerResponse')}
                    </div>
  
                    <Button
                      className="mt-2 shadow "
                      icon={<PiArrowsCounterClockwise />}
                      outlined
                      onClick={() => {
                        retryPostChat({
                          enableReasoning: reasoningEnabled,
                          bot: inputBotParams,
                        });
                      }}>
                      {t('button.resend')}
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </section>
        </div>
  
        <div
          className={twMerge(
            'bottom-0 z-0 flex w-full flex-col items-center justify-center',
            messages.length === 0 ? 'absolute top-2/3 -translate-y-1/2' : ''
          )}>
          

            {/* session history
            <div className="mb-7 w-11/12 md:w-10/12 lg:w-4/6 xl:w-3/6">
              {analysisHistory.map((analysis, index) => (
                <div key={analysis.id} className="mb-8 p-4 border border-gray-200 rounded-lg dark:border-gray-700">
                  <div className="mb-3 text-xs text-gray-500 dark:text-gray-400">
                    Analysis #{analysisHistory.length - index} • {analysis.timestamp.toLocaleString()}
                  </div>
                  
                  <div className="mb-4">
                    <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                      Original Document
                    </div>
                    <pre className="w-full text-wrap break-words min-h-16 p-3 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:text-white text-sm">
                      {analysis.userInput}
                    </pre>
                  </div>

                  <div className="flex gap-4">
                    <div className="flex-1">
                      <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                        Summary
                      </div>
                      <pre className="w-full text-wrap break-words min-h-32 p-3 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:text-white text-sm">
                        {analysis.summary}
                      </pre>
                    </div>

                    <div className="w-1/3">
                      <div className="mb-4">
                        <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                          Key Points
                        </div>
                        <div className="w-full min-h-16 p-3 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:text-white text-sm">
                          {analysis.keyPoints}
                        </div>
                      </div>

                      <div>
                        <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                          Key Entities
                        </div>
                        <div className="w-full min-h-16 p-3 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:text-white">
                          {analysis.keyEntities.split('\n').filter(entity => entity.trim()).map((entity, idx) => (
                            <span key={idx} className="inline-block bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full mr-2 mb-2 dark:bg-blue-900 dark:text-blue-200">
                              {entity.trim()}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div> */}

            {/* current chat */}
            {summary || keyPoints || keyEntities ? (
              <div className="mb-7 w-11/12 md:w-10/12 lg:w-4/6 xl:w-3/6">
                <div className="mb-3 text-xs text-gray-500 dark:text-gray-400">
                  Current Analysis
                </div>
                
                <div className="mb-4">
                  <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                    Original Document
                  </div>
                  <pre className="w-full text-wrap break-words min-h-16 p-3 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:text-white text-sm">
                    {userInput}
                  </pre>
                </div>

                <div className="flex gap-4">
                  <div className="flex-1">
                    <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                      Summary
                    </div>
                    <pre className="w-full text-wrap break-words min-h-32 p-3 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:text-white text-sm">
                      {summary}
                    </pre>
                  </div>

                  <div className="w-1/3">
                    <div className="mb-4">
                      <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                        Key Points
                      </div>
                      <div className="w-full min-h-16 p-3 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:text-white text-sm">
                        {keyPoints}
                      </div>
                    </div>

                    <div>
                      <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                        Key Entities
                      </div>
                      <div className="w-full min-h-16 p-3 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:text-white">
                        {keyEntities.split('\n').filter(entity => entity.trim()).map((entity, idx) => (
                          <span key={idx} className="inline-block bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full mr-2 mb-2 dark:bg-blue-900 dark:text-blue-200">
                            {entity.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div ref={bottomRef} />
                  </div>
                </div>
              </div>
            ) : null}

          <InputChatContent
            className="mb-7 w-11/12 md:w-10/12 lg:w-4/6 xl:w-3/6"
            dndMode={dndMode}
            disabledSend={postingMessage || hasError}
            disabledRegenerate={postingMessage || hasError}
            disabledContinue={postingMessage || hasError}
            disabled={disabledInput}
            placeholder={
              disabledInput
                ? t('bot.label.notAvailableBotInputMessage')
                : undefined
            }
            canRegenerate={messages.length > 1}
            canContinue={getShouldContinue()}
            isLoading={postingMessage}
            isNewChat={messages.length == 0}
            onSend={onSend}
            onRegenerate={onRegenerate}
            continueGenerate={onContinueGenerate}
            ref={focusInputRef}
            supportReasoning={supportReasoning}
            reasoningEnabled={reasoningEnabled}
            onChangeReasoning={setReasoningEnabled}
          />
        </div>
        <BottomHelper />
      </div>
    );
  };
  
  export default SummarizeDocumentsPage;  