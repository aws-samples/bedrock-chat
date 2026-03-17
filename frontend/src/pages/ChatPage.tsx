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
  PiPenNib,
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
import Alert from '../components/Alert';
import useBotSummary from '../hooks/useBotSummary';
import useModel from '../hooks/useModel';
import { StreamingState } from '../hooks/xstates/streaming.ts';
import { AgentToolsProps } from '../features/agent/types';
import { getRelatedDocumentsOfToolUse } from '../features/agent/utils/AgentUtils';
import { SyncStatus } from '../constants';
import { BottomHelper } from '../features/helper/components/BottomHelper';
import { useIsWindows } from '../hooks/useIsWindows';
import {
  DisplayMessageContent,
  Model,
  PutFeedbackRequest,
  RelatedDocument,
} from '../@types/conversation.ts';
import { AVAILABLE_MODEL_KEYS } from '../constants/index';
import usePostMessageStreaming from '../hooks/usePostMessageStreaming.ts';
import useLoginUser from '../hooks/useLoginUser';
import useBotPinning from '../hooks/useBotPinning';
import Skeleton from '../components/Skeleton.tsx';
import { twMerge } from 'tailwind-merge';
import ButtonStar from '../components/ButtonStar.tsx';
import MenuBot from '../components/MenuBot.tsx';

// ChatMessageWithRelatedDocuments component moved outside to prevent re-creation on every render
type ChatMessageWithRelatedDocumentsProps = {
  chatContent: DisplayMessageContent;
  isStreaming: boolean;
  streamingReasoning: string;
  streamingTools: AgentToolsProps[];
  streamingRelatedDocuments: RelatedDocument[];
  streamingStateValue: string;
  botHasAgent: boolean;
  botHasKnowledge: boolean;
  relatedDocuments: RelatedDocument[];
  onChangeMessageId?: (messageId: string) => void;
  onSubmit?: (messageId: string, content: string) => void;
  onSubmitFeedback?: (messageId: string, feedback: PutFeedbackRequest) => void;
};

const ChatMessageWithRelatedDocuments: React.FC<ChatMessageWithRelatedDocumentsProps> = React.memo((props) => {
  const { t } = useTranslation();
  const { chatContent: message } = props;

  const isAgentThinking = useMemo(() => {
    switch (props.streamingStateValue) {
      case StreamingState.STREAMING:
      case StreamingState.LEAVING:
        return props.isStreaming;
      default:
        return false;
    }
  }, [props.streamingStateValue, props.isStreaming]);

  const reasoning = useMemo(() => (
    isAgentThinking ? props.streamingReasoning : ''
  ), [isAgentThinking, props.streamingReasoning]);

  const tools: AgentToolsProps[] | undefined = useMemo(() => {
    if (isAgentThinking) {
      if (props.streamingTools.length > 0) {
        return props.streamingTools;
      }

      if (props.botHasAgent) {
        return [{ thought: t('agent.progress.label'), tools: {} }];
      }

      if (props.botHasKnowledge) {
        return [{ thought: t('bot.label.retrievingKnowledge'), tools: {} }];
      }

      return undefined;
    } else {
      if (props.botHasKnowledge) {
        const pseudoToolUseId = message.id;
        const relatedDocumentsOfVectorSearch = getRelatedDocumentsOfToolUse(
          props.relatedDocuments,
          pseudoToolUseId
        );
        if (relatedDocumentsOfVectorSearch != null && relatedDocumentsOfVectorSearch.length > 0) {
          return [{
            tools: {
              [pseudoToolUseId]: {
                name: 'knowledge_base_tool',
                status: 'success',
                input: {},
                relatedDocuments: relatedDocumentsOfVectorSearch,
              },
            },
          }];
        }
      }
      return undefined;
    }
  }, [isAgentThinking, props.streamingTools, props.botHasAgent, props.botHasKnowledge, message.id, props.relatedDocuments, t]);

  const relatedDocumentsForCitation = useMemo(
    () => isAgentThinking ? props.streamingRelatedDocuments : props.relatedDocuments,
    [isAgentThinking, props.streamingRelatedDocuments, props.relatedDocuments]
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
  const { isAdmin } = useLoginUser();
  const { pinBot, unpinBot } = useBotPinning();

  const {
    streamingState,
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
        navigate('/');
      } else {
        openSnackbar(conversationError.message ?? '');
      }
    }
  }, [conversationError, navigate, newChat, openSnackbar, t]);

  const { isWindows } = useIsWindows();

  const { getBotId } = useConversation();

  const { scrollToBottom, scrollToTop } = useScroll(conversationId);

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

  const isLastAssistantMessageEmpty = useMemo(() => {
    if (messages.length === 0) {
      return false;
    }

    const lastMessage = messages[messages.length - 1];
    return lastMessage.role === 'assistant' && lastMessage.content.length === 0;
  }, [messages]);

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

  return (
    <div
      className="relative flex h-full flex-1 flex-col"
      onDragOver={onDragOver}
      onDrop={endDnd}
      onDragEnd={endDnd}>

      {/* ── TOP HEADER BAR ── */}
      <header className="sticky top-0 z-10 flex h-14 w-full shrink-0 items-center justify-between border-b border-black/5 bg-aws-paper-light/95 px-4 backdrop-blur-sm dark:border-white/5 dark:bg-aws-paper-dark/95">
        {/* Left: title */}
        <div className="flex min-w-0 items-center gap-2">
          {isLoadingBot ? (
            <>
              <Skeleton className="h-5 w-8 rounded-full" />
              <Skeleton className="h-5 w-36" />
            </>
          ) : (
            <>
              <IconPinnedBot
                botSharedStatus={bot?.sharedStatus}
                className="shrink-0 text-aws-aqua"
              />
              <h1 className="font-heading truncate text-sm font-semibold text-aws-font-color-light dark:text-aws-font-color-dark">
                {pageTitle}
              </h1>
            </>
          )}
        </div>

        {/* Right: model selector + bot actions */}
        <div className="flex shrink-0 items-center gap-1">
          {!loadingConversation && (
            <SwitchBedrockModel
              activeModels={activeModels}
              botId={botId}
            />
          )}
          {isLoadingBot && (
            <div className="flex items-center gap-2">
              <Skeleton className="h-7 w-24" />
              <Skeleton className="size-7 rounded-full" />
            </div>
          )}
          {isAvailabilityBot && !isLoadingBot && (
            <div className="flex items-center">
              {bot?.owned && (
                <StatusSyncBot
                  syncStatus={bot.syncStatus}
                  onClickError={onClickSyncError}
                />
              )}
              <ButtonStar isStarred={bot?.isStarred ?? false} onClick={onClickStar} />
              <MenuBot
                className="mx-1"
                {...(bot?.owned && { onClickEdit: () => onClickBotEdit(bot.id) })}
                {...(bot?.sharedScope !== 'private' && {
                  onClickCopyUrl: () => onClickCopyUrl(bot?.id ?? ''),
                })}
                {...(canSwitchPinned
                  ? {
                      onClickSwitchPinned: () => bot && togglePinBot(bot),
                      isPinned: isPinnedBot(bot?.sharedStatus ?? ''),
                    }
                  : { isPinned: undefined, onClickSwitchPinned: undefined })}
              />
            </div>
          )}
        </div>
      </header>

      {/* ── MESSAGE AREA ── */}
      <div className="flex-1 overflow-hidden">
        <section className="relative size-full flex-1 overflow-auto">
          <div className="h-full">
            <div
              id="messages"
              role="presentation"
              className="flex h-full flex-col overflow-auto pb-40">

              {/* Empty state */}
              {messages?.length === 0 && (
                <div className="flex flex-1 flex-col items-center justify-center py-16">
                  {isLoadingBot && botId ? (
                    <div className="flex flex-col items-center gap-3">
                      <Skeleton className="h-7 w-48 rounded-lg" />
                      <Skeleton className="h-4 w-72 rounded" />
                    </div>
                  ) : bot ? (
                    <div className="text-center">
                      <div className="font-heading mb-2 flex items-center justify-center gap-1.5 text-xl font-semibold text-aws-font-color-light dark:text-aws-font-color-dark">
                        <IconPinnedBot
                          botSharedStatus={bot?.sharedStatus}
                          className="shrink-0 text-aws-aqua"
                        />
                        {pageTitle}
                      </div>
                      {description && (
                        <p className="mx-auto max-w-sm text-sm text-dark-gray dark:text-light-gray">
                          {description}
                        </p>
                      )}
                    </div>
                  ) : null}
                </div>
              )}

              {/* Messages list */}
              {messages?.length > 0 && (
                <div className="mx-auto w-full max-w-3xl px-4 py-6">
                  {messages.map((message, idx, array) => (
                    <ChatMessageWithRelatedDocuments
                      key={message.id}
                      chatContent={message}
                      isStreaming={postingMessage && idx + 1 === array.length}
                      streamingReasoning={streamingState.context.reasoning}
                      streamingTools={streamingState.context.tools}
                      streamingRelatedDocuments={streamingState.context.relatedDocuments}
                      streamingStateValue={streamingState.value as string}
                      botHasAgent={bot?.hasAgent ?? false}
                      botHasKnowledge={bot?.hasKnowledge ?? false}
                      relatedDocuments={relatedDocuments ?? []}
                      onChangeMessageId={onChangeCurrentMessageId}
                      onSubmit={onSubmitEditedContent}
                      onSubmitFeedback={(messageId, feedback) => {
                        if (conversationId) {
                          giveFeedback(messageId, feedback);
                        }
                      }}
                    />
                  ))}
                </div>
              )}

              {/* Error state */}
              {hasError && (
                <div className="mb-12 mt-4 flex flex-col items-center gap-3">
                  <div className="flex items-center gap-1.5 rounded-xl border border-red/20 bg-light-red px-4 py-2.5 font-semibold text-red">
                    <PiWarningCircleFill className="shrink-0 text-xl" />
                    {errorDetail ?? t('error.answerResponse')}
                  </div>
                  <Button
                    className="rounded-full shadow"
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

      {/* ── INPUT AREA (fixed at bottom) ── */}
      <div
        className={twMerge(
          'bottom-0 z-10 flex w-full flex-col items-center',
          messages.length === 0
            ? 'absolute top-1/2 -translate-y-1/4'
            : 'relative bg-gradient-to-t from-aws-paper-light via-aws-paper-light/90 to-transparent pb-4 pt-2 dark:from-aws-paper-dark dark:via-aws-paper-dark/90'
        )}>

        {/* Sync warning */}
        {bot && bot.syncStatus !== SyncStatus.SUCCEEDED && (
          <div className="mb-3 w-11/12 md:w-10/12 lg:w-4/6 xl:w-3/6">
            <Alert severity="warning" title={t('bot.alert.sync.incomplete.title')}>
              {t('bot.alert.sync.incomplete.body')}
            </Alert>
          </div>
        )}

        {/* Quick starters */}
        {messages.length === 0 && bot?.conversationQuickStarters && bot.conversationQuickStarters.length > 0 && (
          <div className="mb-3 flex w-11/12 flex-wrap justify-center gap-2 md:w-10/12 lg:w-4/6 xl:w-3/6">
            {bot.conversationQuickStarters.map((qs, idx) => (
              <button
                key={idx}
                className="flex cursor-pointer items-center gap-1.5 rounded-full border border-aws-squid-ink-light/15 bg-white px-3 py-1.5 text-sm text-dark-gray shadow-sm transition-shadow hover:shadow-md dark:border-white/10 dark:bg-aws-paper-dark dark:text-light-gray"
                onClick={() => onSend(qs.example, reasoningEnabled)}>
                <PiPenNib className="shrink-0 text-aws-aqua" />
                {qs.title}
              </button>
            ))}
          </div>
        )}

        <InputChatContent
          className="mb-2 w-11/12 md:w-10/12 lg:w-4/6 xl:w-3/6"
          dndMode={dndMode}
          disabledSend={postingMessage || hasError || isLastAssistantMessageEmpty}
          disabledRegenerate={postingMessage || hasError}
          disabledContinue={postingMessage || hasError}
          disabled={disabledInput}
          placeholder={
            disabledInput ? t('bot.label.notAvailableBotInputMessage') : undefined
          }
          canRegenerate={messages.length > 1}
          canContinue={getShouldContinue()}
          isLoading={postingMessage}
          isNewChat={messages.length === 0}
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
