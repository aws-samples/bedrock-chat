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
import { AttachmentType } from '../hooks/useChat';
import ChatMessage from '../components/ChatMessage';
import useScroll from '../hooks/useScroll';
import { useNavigate, useParams } from 'react-router-dom';
import {
  PiArrowsCounterClockwise,
  PiLink,
  PiPenNib,
  PiPencilLine,
  PiStar,
  PiStarFill,
  PiWarningCircleFill,
} from 'react-icons/pi';
import Button from '../components/Button';
import { useTranslation } from 'react-i18next';
import SwitchBedrockModel from '../components/SwitchBedrockModel';
import useSnackbar from '../hooks/useSnackbar';
import useBot from '../hooks/useBot';
import useConversation from '../hooks/useConversation';
import ButtonPopover from '../components/PopoverMenu';
import PopoverItem from '../components/PopoverItem';
import { ActiveModels } from '../@types/bot';

import { copyBotUrl } from '../utils/BotUtils';
import { toCamelCase } from '../utils/StringUtils';
import { produce } from 'immer';
import ButtonIcon from '../components/ButtonIcon';
import StatusSyncBot from '../components/StatusSyncBot';
import Alert from '../components/Alert';
import useBotSummary from '../hooks/useBotSummary';
import useModel from '../hooks/useModel';
import {
  AgentState,
  AgentToolsProps,
} from '../features/agent/xstates/agentThink';
import { getRelatedDocumentsOfToolUse } from '../features/agent/utils/AgentUtils';
import { SyncStatus } from '../constants';
import { BottomHelper } from '../features/helper/components/BottomHelper';
import { useIsWindows } from '../hooks/useIsWindows';
import {
  DisplayMessageContent,
  Model,
  PutFeedbackRequest,
} from '../@types/conversation.ts';
import { AVAILABLE_MODEL_KEYS } from '../constants/index';
import usePostMessageStreaming from '../hooks/usePostMessageStreaming.ts';

// Default model activation settings when no bot is selected
const defaultActiveModels: ActiveModels = (() => {
  return Object.fromEntries(
    AVAILABLE_MODEL_KEYS.map((key: Model) => [toCamelCase(key), true])
  ) as ActiveModels;
})();

const ChatPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { open: openSnackbar } = useSnackbar();
  const { errorDetail } = usePostMessageStreaming();

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
    setCurrentMessageId,
    regenerate,
    continueGenerate,
    getPostedModel,
    loadingConversation,
    getShouldContinue,
    relatedDocuments,
    giveFeedback,
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
        navigate('');
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
      if (botError.response?.status === 404) {
        setPageTitle(t('bot.label.notAvailableBot'));
      }
    }
  }, [bot, botError, t]);

  const description = useMemo<string>(() => {
    if (!bot) {
      return '';
    } else if (bot.description === '') {
      return t('bot.label.noDescription');
    } else {
      return bot.description;
    }
  }, [bot, t]);

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
      postChat({
        content,
        base64EncodedImages,
        attachments,
        bot: inputBotParams,
        enableReasoning,
      });
    },
    [inputBotParams, postChat]
  );

  const onChangeCurrentMessageId = useCallback(
    (messageId: string) => {
      setCurrentMessageId(messageId);
    },
    [setCurrentMessageId]
  );

  const onSubmitEditedContent = useCallback(
    (messageId: string, content: string) => {
      if (hasError) {
        retryPostChat({
          content,
          bot: inputBotParams,
          enableReasoning: reasoningEnabled,
        });
      } else {
        regenerate({
          messageId,
          content,
          bot: inputBotParams,
          enableReasoning: reasoningEnabled,
        });
      }
    },
    [hasError, inputBotParams, regenerate, retryPostChat, reasoningEnabled]
  );

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

  const { updateMyBotStarred, updateSharedBotStarred } = useBot();
  const onClickBotEdit = useCallback(
    (botId: string) => {
      navigate(`/bot/edit/${botId}`);
    },
    [navigate]
  );

  const onClickStar = useCallback(() => {
    if (!bot) {
      return;
    }
    const isStarred = !bot.isPinned;
    mutateBot(
      produce(bot, (draft) => {
        draft.isPinned = isStarred;
      }),
      {
        revalidate: false,
      }
    );

    try {
      if (bot.owned) {
        updateMyBotStarred(bot.id, isStarred);
      } else {
        updateSharedBotStarred(bot.id, isStarred);
      }
    } finally {
      mutateBot();
    }
  }, [bot, mutateBot, updateMyBotStarred, updateSharedBotStarred]);

  const [copyLabel, setCopyLabel] = useState(t('bot.titleSubmenu.copyLink'));
  const onClickCopyUrl = useCallback(
    (botId: string) => {
      copyBotUrl(botId);
      setCopyLabel(t('bot.titleSubmenu.copiedLink'));
      setTimeout(() => {
        setCopyLabel(t('bot.titleSubmenu.copyLink'));
      }, 3000);
    },
    [t]
  );

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

        if (bot?.hasKnowledge || bot?.hasExistKnowledngeBaseId) {
          return [
            {
              thought: t('bot.label.retrievingKnowledge'), // @@
              tools: {},
            },
          ];
        }

        return undefined;
      } else {
        if (bot?.hasKnowledge || bot?.hasExistKnowledngeBaseId) {
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
              <div className="mr-10 font-bold">{pageTitle}</div>
              <div className="text-xs font-thin text-dark-gray dark:text-light-gray">
                {description}
              </div>
            </div>

            {isAvailabilityBot && (
              <div className="absolute -top-1 right-0 flex h-full items-center">
                <div className="h-full bg-gradient-to-r from-transparent to-aws-paper-light dark:to-aws-paper-dark"></div>
                <div className="flex items-center bg-aws-paper-light dark:bg-aws-paper-dark">
                  {bot?.owned && (
                    <StatusSyncBot
                      syncStatus={bot.syncStatus}
                      onClickError={onClickSyncError}
                    />
                  )}
                  <ButtonIcon onClick={onClickStar}>
                    {bot?.isPinned ? (
                      <PiStarFill className="text-aws-aqua" />
                    ) : (
                      <PiStar />
                    )}
                  </ButtonIcon>
                  <ButtonPopover className="mx-1" target="bottom-right">
                    {bot?.owned && (
                      <PopoverItem
                        onClick={() => {
                          onClickBotEdit(bot.id);
                        }}>
                        <PiPencilLine />
                        {t('bot.titleSubmenu.edit')}
                      </PopoverItem>
                    )}
                    {bot?.isPublic && (
                      <PopoverItem
                        onClick={() => {
                          if (bot) {
                            onClickCopyUrl(bot.id);
                          }
                        }}>
                        <PiLink />
                        {copyLabel}
                      </PopoverItem>
                    )}
                  </ButtonPopover>
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
              className=" flex h-full flex-col overflow-auto pb-16">
              {messages?.length === 0 ? (
                <div className="relative flex w-full justify-center">
                  {!loadingConversation && (
                    <SwitchBedrockModel
                      className="mt-3 w-min"
                      activeModels={activeModels}
                      botId={botId}
                    />
                  )}
                </div>
              ) : (
                <>
                  {messages?.map((message, idx, array) => (
                    <div
                      key={idx}
                      className={`${
                        message.role === 'assistant'
                          ? 'bg-aws-squid-ink-light/5 dark:bg-aws-squid-ink-dark/35'
                          : ''
                      }`}>
                      <ChatMessageWithRelatedDocuments
                        chatContent={message}
                        isStreaming={postingMessage && idx + 1 === array.length}
                        onChangeMessageId={onChangeCurrentMessageId}
                        onSubmit={onSubmitEditedContent}
                        onSubmitFeedback={(messageId, feedback) => {
                          if (conversationId) {
                            giveFeedback(messageId, feedback);
                          }
                        }}
                      />
                      <div className="w-full border-b border-aws-squid-ink-light/10 dark:border-aws-squid-ink-dark/10"></div>
                    </div>
                  ))}
                </>
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
        className={`bottom-0 z-0 flex w-full flex-col items-center justify-center ${messages.length === 0 ? 'absolute top-1/2 -translate-y-1/2' : ''}`}>
        {bot && bot.syncStatus !== SyncStatus.SUCCEEDED && (
          <div className="mb-8 w-1/2">
            <Alert
              severity="warning"
              title={t('bot.alert.sync.incomplete.title')}>
              {t('bot.alert.sync.incomplete.body')}
            </Alert>
          </div>
        )}
        {messages.length === 0 && (
          <div className="mb-3 flex w-11/12 flex-wrap-reverse justify-start gap-2 md:w-10/12 lg:w-4/6 xl:w-3/6">
            {bot?.conversationQuickStarters?.map((qs, idx) => (
              <div
                key={idx}
                className="w-[calc(33.333%-0.5rem)] cursor-pointer rounded-2xl border border-aws-squid-ink-light/20 bg-white p-2 text-sm  text-dark-gray hover:shadow-lg hover:shadow-gray  dark:border-aws-squid-ink-dark/20 dark:text-light-gray"
                onClick={() => {
                  onSend(qs.example, reasoningEnabled);
                }}>
                <div>
                  <PiPenNib />
                </div>
                {qs.title}
              </div>
            ))}
          </div>
        )}

        <InputChatContent
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

export default ChatPage;
