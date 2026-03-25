import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { twMerge } from 'tailwind-merge';
import ChatMessageMarkdown from './ChatMessageMarkdown';
import ButtonCopy from './ButtonCopy';
import {
  PiCaretLeftBold,
  PiNotePencil,
  PiThumbsDown,
  PiThumbsDownFill,
} from 'react-icons/pi';
import { BaseProps } from '../@types/common';
import {
  DisplayMessageContent,
  RelatedDocument,
  PutFeedbackRequest,
  ReasoningContent,
  TextContent,
} from '../@types/conversation';
import ButtonIcon from './ButtonIcon';
import Textarea from './Textarea';
import Button from './Button';
import ModalDialog from './ModalDialog';
import { useTranslation } from 'react-i18next';
import DialogFeedback from './DialogFeedback';
import UploadedAttachedFile from './UploadedAttachedFile';
import { TEXT_FILE_EXTENSIONS } from '../constants/supportedAttachedFiles';
import AgentToolList from '../features/agent/components/AgentToolList';
import { AgentToolsProps } from '../features/agent/types';
import { convertThinkingLogToAgentToolProps } from '../features/agent/utils/AgentUtils';
import { convertUsedChunkToRelatedDocument } from '../utils/MessageUtils';
import ReasoningCard from '../features/reasoning/components/ReasoningCard';
import TypingIndicator from './TypingIndicator';

type Props = BaseProps & {
  tools?: AgentToolsProps[];
  reasoning?: string;
  chatContent?: DisplayMessageContent;
  isStreaming?: boolean;
  relatedDocuments?: RelatedDocument[];
  onChangeMessageId?: (messageId: string) => void;
  onSubmit?: (messageId: string, content: string) => void;
  onSubmitFeedback?: (messageId: string, feedback: PutFeedbackRequest) => void;
};

const ChatMessage: React.FC<Props> = (props) => {
  const { t } = useTranslation();
  const [isEdit, setIsEdit] = useState(false);
  const [changedContent, setChangedContent] = useState('');
  const [isFeedbackOpen, setIsFeedbackOpen] = useState(false);

  const [firstTextContent, setFirstTextContent] = useState(0);

  useEffect(() => {
    if (props.chatContent) {
      setFirstTextContent(
        props.chatContent.content.findIndex(
          (content) => content.contentType === 'text'
        )
      );
    }
  }, [props.chatContent]);

  const [previewImageUrl, setPreviewImageUrl] = useState<string | null>(null);
  const [isOpenPreviewImage, setIsOpenPreviewImage] = useState(false);
  const [isFileModalOpen, setIsFileModalOpen] = useState(false);
  const [dialogFileName, setDialogFileName] = useState<string>('');
  const [dialogFileContent, setDialogFileContent] = useState<string | null>(
    null
  );

  const chatContent = useMemo(() => {
    return props.chatContent;
  }, [props.chatContent]);

  const relatedDocuments = useMemo(() => {
    if (chatContent?.usedChunks) {
      return [
        ...(props.relatedDocuments ?? []),
        ...chatContent.usedChunks.map((chunk) =>
          convertUsedChunkToRelatedDocument(chunk)
        ),
      ];
    } else {
      return props.relatedDocuments;
    }
  }, [props.relatedDocuments, chatContent]);

  const reasoning = useMemo(() => {
    if (props.reasoning) {
      return props.reasoning;
    }

    if (chatContent?.content == null) {
      return undefined;
    }

    const reasoningContent = chatContent.content.find(
      (content): content is ReasoningContent =>
        content.contentType === 'reasoning'
    );

    if (reasoningContent) {
      return reasoningContent.text;
    }

    return undefined;
  }, [props.reasoning, chatContent]);

  const tools = useMemo(() => {
    if (props.tools != null) {
      return props.tools;
    }
    if (chatContent?.thinkingLog == null) {
      return undefined;
    }
    return convertThinkingLogToAgentToolProps(
      chatContent.thinkingLog,
      relatedDocuments
    );
  }, [props.tools, chatContent, relatedDocuments]);

  const nodeIndex = useMemo(() => {
    return chatContent?.sibling.findIndex((s) => s === chatContent.id) ?? -1;
  }, [chatContent]);

  const onClickChange = useCallback(
    (idx: number) => {
      props.onChangeMessageId
        ? props.onChangeMessageId(chatContent?.sibling[idx] ?? '')
        : null;
    },
    [chatContent?.sibling, props]
  );

  const onSubmit = useCallback(() => {
    props.onSubmit
      ? props.onSubmit(chatContent?.sibling[0] ?? '', changedContent)
      : null;
    setIsEdit(false);
  }, [changedContent, chatContent?.sibling, props]);

  const handleFeedbackSubmit = useCallback(
    (messageId: string, feedback: PutFeedbackRequest) => {
      if (chatContent) {
        props.onSubmitFeedback?.(messageId, feedback);
      }
      setIsFeedbackOpen(false);
    },
    [chatContent, props]
  );

  const isUser = chatContent?.role === 'user';
  const isAssistant = chatContent?.role === 'assistant';

  return (
    <div className={twMerge(props.className, 'animate-fade-in px-4 py-4')}>
      {/* ── SIBLING NAVIGATOR ── */}
      {(chatContent?.sibling.length ?? 0) > 1 && (
        <div className={twMerge(
          'mb-1 flex items-center gap-1 text-xs text-dark-gray dark:text-light-gray',
          isUser ? 'justify-end' : 'justify-start pl-10'
        )}>
          <ButtonIcon
            className="text-xs"
            disabled={nodeIndex === 0}
            onClick={() => onClickChange(nodeIndex - 1)}>
            <PiCaretLeftBold />
          </ButtonIcon>
          {nodeIndex + 1} / {chatContent?.sibling.length}
          <ButtonIcon
            className="text-xs"
            disabled={nodeIndex >= (chatContent?.sibling.length ?? 0) - 1}
            onClick={() => onClickChange(nodeIndex + 1)}>
            <PiCaretLeftBold className="rotate-180" />
          </ButtonIcon>
        </div>
      )}

      {/* ── USER MESSAGE — right-aligned pill ── */}
      {isUser && (
        <div className="flex justify-end">
          <div className="max-w-[80%]">
            {!isEdit ? (
              <div className="group relative">
                {/* Attachments above bubble */}
                {chatContent!.content.some((c) => c.contentType === 'image') && (
                  <div className="mb-2 flex flex-wrap gap-2 justify-end">
                    {chatContent!.content.map((content, idx) => {
                      if (content.contentType !== 'image') return null;
                      const imageUrl = `data:${content.mediaType};base64,${content.body}`;
                      return (
                        <img
                          key={idx}
                          src={imageUrl}
                          className="h-40 cursor-pointer rounded-xl border border-black/10 object-cover"
                          onClick={() => {
                            setPreviewImageUrl(imageUrl);
                            setIsOpenPreviewImage(true);
                          }}
                        />
                      );
                    })}
                  </div>
                )}
                {chatContent!.content.some((c) => c.contentType === 'attachment') && (
                  <div className="mb-2 flex flex-wrap justify-end gap-2">
                    {chatContent!.content.map((content, idx) => {
                      if (content.contentType !== 'attachment') return null;
                      const isTextFile = TEXT_FILE_EXTENSIONS.some((ext) =>
                        content.fileName?.toLowerCase().endsWith(ext)
                      );
                      return (
                        <UploadedAttachedFile
                          key={idx}
                          fileName={content.fileName ?? ''}
                          onClick={
                            isTextFile
                              ? () => {
                                  const textContent = new TextDecoder('utf-8').decode(
                                    Uint8Array.from(atob(content.body), (c) =>
                                      c.charCodeAt(0)
                                    )
                                  );
                                  setDialogFileName(content.fileName ?? '');
                                  setDialogFileContent(textContent);
                                  setIsFileModalOpen(true);
                                }
                              : undefined
                          }
                        />
                      );
                    })}
                  </div>
                )}

                {/* Text bubble */}
                {chatContent!.content.some((c) => c.contentType === 'text') && (
                  <div className="rounded-2xl rounded-tr-sm bg-aa-purple-3 px-4 py-3 text-sm leading-relaxed text-white shadow-sm dark:bg-white/15 dark:text-white/90">
                    {chatContent!.content.map((content, idx) => {
                      if (content.contentType !== 'text') return null;
                      return (
                        <React.Fragment key={idx}>
                          {content.body.split('\n').map((line, lineIdx) => (
                            <div key={lineIdx}>{line || <br />}</div>
                          ))}
                        </React.Fragment>
                      );
                    })}
                  </div>
                )}

                {/* Edit button — shown on hover */}
                <div className="mt-1 flex justify-end opacity-0 transition-opacity group-hover:opacity-100">
                  <ButtonIcon
                    className="text-dark-gray dark:text-light-gray"
                    onClick={() => {
                      const textContent = chatContent!.content[firstTextContent] as TextContent;
                      setChangedContent(textContent.body);
                      setIsEdit(true);
                    }}>
                    <PiNotePencil />
                  </ButtonIcon>
                </div>
              </div>
            ) : (
              <div className="w-full">
                <Textarea
                  className="bg-transparent"
                  value={changedContent}
                  noBorder
                  onChange={(v) => setChangedContent(v)}
                />
                <div className="flex justify-center gap-3 pt-2">
                  <Button onClick={onSubmit}>{t('button.SaveAndSubmit')}</Button>
                  <Button outlined onClick={() => setIsEdit(false)}>
                    {t('button.cancel')}
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── ASSISTANT MESSAGE — left-aligned with avatar ── */}
      {isAssistant && (
        <div className="flex items-start gap-3">
          {/* Avatar */}
          <div className="mt-0.5 shrink-0">
            <div className="flex size-8 items-center justify-center overflow-hidden rounded-full border border-black/[0.06] bg-white shadow-sm dark:border-white/[0.08] dark:bg-aws-paper-dark">
              <img
                src="/images/bedrock_icon_64.png"
                className="size-6 object-contain"
                alt="Assistant"
              />
            </div>
          </div>

          {/* Content */}
          <div className="group min-w-0 flex-1">
            {/* Agent tools */}
            {tools != null && tools.length > 0 && (
              <div className="mb-3 flex flex-col gap-2">
                {tools.map((toolGroup, index) => (
                  <AgentToolList
                    key={index}
                    messageId={chatContent!.id}
                    tools={toolGroup}
                    relatedDocuments={relatedDocuments}
                  />
                ))}
              </div>
            )}

            {/* Reasoning */}
            {reasoning && (
              <ReasoningCard
                content={reasoning}
                className="mb-3 flex w-full flex-col rounded-xl border border-black/[0.06] bg-black/[0.02] text-aws-font-color-light/70 dark:border-white/[0.06] dark:bg-white/[0.02] dark:text-aws-font-color-dark/70"
              />
            )}

            {/* Typing indicator while streaming with no content yet */}
            {props.isStreaming &&
              chatContent!.content.filter((c) => c.contentType === 'text').every(
                (c) => (c as TextContent).body === ''
              ) && (
                <TypingIndicator className="py-1" />
              )}

            {/* Message text */}
            <ChatMessageMarkdown
              isStreaming={props.isStreaming}
              relatedDocuments={relatedDocuments}
              messageId={chatContent!.id}>
              {chatContent!.content
                .filter((content) => content.contentType === 'text')
                .map((content) => (content as TextContent).body)
                .join('\n')}
            </ChatMessageMarkdown>

            {/* Action bar — shown on hover */}
            <div className="mt-1 flex items-center gap-0.5 opacity-0 transition-opacity group-hover:opacity-100">
              <ButtonIcon
                className="text-dark-gray dark:text-light-gray"
                onClick={() => setIsFeedbackOpen(true)}>
                {chatContent!.feedback && !chatContent!.feedback.thumbsUp ? (
                  <PiThumbsDownFill />
                ) : (
                  <PiThumbsDown />
                )}
              </ButtonIcon>
              <ButtonCopy
                className="text-dark-gray dark:text-light-gray"
                text={
                  chatContent!.content.find((c) => c.contentType === 'text')
                    ? (chatContent!.content.find((c) => c.contentType === 'text') as TextContent).body
                    : ''
                }
              />
            </div>
          </div>
        </div>
      )}

      {/* ── SHARED MODALS ── */}
      <ModalDialog
        isOpen={isOpenPreviewImage}
        onClose={() => setIsOpenPreviewImage(false)}
        widthFromContent={true}
        onAfterLeave={() => setPreviewImageUrl(null)}>
        {previewImageUrl && (
          <img
            src={previewImageUrl}
            className="mx-auto max-h-[80vh] max-w-full rounded-xl"
          />
        )}
      </ModalDialog>
      <ModalDialog
        isOpen={isFileModalOpen}
        onClose={() => setIsFileModalOpen(false)}
        widthFromContent={true}
        title={dialogFileName ?? ''}>
        <div className="relative flex size-auto max-h-[80vh] max-w-[80vh] flex-col">
          <div className="overflow-auto px-4">
            <pre className="whitespace-pre-wrap break-all">{dialogFileContent}</pre>
          </div>
        </div>
      </ModalDialog>

      <DialogFeedback
        isOpen={isFeedbackOpen}
        thumbsUp={false}
        feedback={chatContent?.feedback ?? undefined}
        onClose={() => setIsFeedbackOpen(false)}
        onSubmit={(feedback) => {
          if (chatContent) {
            handleFeedbackSubmit(chatContent.id, feedback);
          }
        }}
      />
    </div>
  );
};

export default ChatMessage;
