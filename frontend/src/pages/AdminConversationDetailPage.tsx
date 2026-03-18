import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import useAdminApi from '../hooks/useAdminApi';
import { formatDatetime } from '../utils/DateUtils';
import { formatCostAUD } from '../utils/CurrencyUtils';
import Button from '../components/Button';
import { PiArrowLeft, PiRobot, PiUser } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';

const AdminConversationDetailPage: React.FC = () => {
  const { t } = useTranslation();
  const { userId, conversationId } = useParams<{
    userId: string;
    conversationId: string;
  }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const email = searchParams.get('email') ?? userId ?? '';
  const start = searchParams.get('start') ?? undefined;
  const end = searchParams.get('end') ?? undefined;

  const { getConversationDetail } = useAdminApi();
  const { data: conversation, isLoading } = getConversationDetail(
    userId ?? '',
    conversationId ?? ''
  );

  const backParams = new URLSearchParams({ email });
  if (start) backParams.set('start', start);
  if (end) backParams.set('end', end);

  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <div className="border-b px-6 py-4 dark:border-white/10">
        <Button
          outlined
          icon={<PiArrowLeft />}
          className="mb-3 w-fit"
          onClick={() =>
            navigate(`/admin/user/${userId}?${backParams.toString()}`)
          }>
          {t('admin.conversationDetail.button.back')}
        </Button>
        <div className="flex items-start justify-between">
          <div className="overflow-hidden">
            <h1 className="truncate text-xl font-bold">
              {isLoading
                ? t('admin.conversationDetail.label.loading')
                : (conversation?.title ||
                  t('admin.conversationDetail.label.untitled'))}
            </h1>
            <div className="mt-1 text-sm text-aws-font-color-light/60 dark:text-aws-font-color-dark/60">
              {email}
            </div>
            {conversation && (
              <div className="mt-1 text-sm text-aws-font-color-light/60 dark:text-aws-font-color-dark/60">
                {formatDatetime(conversation.createTime * 1000)}
              </div>
            )}
          </div>
          {conversation && (
            <div className="ml-4 shrink-0 text-right">
              <div className="text-xs text-aws-font-color-light/60 dark:text-aws-font-color-dark/60">
                {t('admin.conversationDetail.label.totalCost')}
              </div>
              <div className="text-lg font-bold">
                {formatCostAUD(conversation.totalPrice)}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        {isLoading && (
          <div className="flex items-center justify-center py-12 text-aws-font-color-light/60 dark:text-aws-font-color-dark/60">
            {t('admin.conversationDetail.label.loading')}
          </div>
        )}
        {!isLoading && conversation?.messages.length === 0 && (
          <div className="flex items-center justify-center py-12 text-aws-font-color-light/60 dark:text-aws-font-color-dark/60">
            {t('admin.conversationDetail.label.noMessages')}
          </div>
        )}
        <div className="mx-auto max-w-3xl space-y-4">
          {conversation?.messages.map((msg, idx) => {
            const isUser = msg.role === 'user';
            return (
              <div
                key={idx}
                className={twMerge(
                  'flex gap-3',
                  isUser ? 'flex-row-reverse' : 'flex-row'
                )}>
                {/* Avatar */}
                <div
                  className={twMerge(
                    'flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-white',
                    isUser ? 'bg-aws-sea-blue-light' : 'bg-aws-squid-ink dark:bg-aws-paper-dark'
                  )}>
                  {isUser ? (
                    <PiUser className="text-sm" />
                  ) : (
                    <PiRobot className="text-sm" />
                  )}
                </div>
                {/* Bubble */}
                <div
                  className={twMerge(
                    'max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
                    isUser
                      ? 'rounded-tr-sm bg-aws-sea-blue-light text-white'
                      : 'rounded-tl-sm bg-white text-aws-font-color-light shadow-sm dark:bg-aws-ui-color-dark dark:text-aws-font-color-dark'
                  )}>
                  <div className="whitespace-pre-wrap break-words">
                    {msg.content || (
                      <span className="italic opacity-60">
                        {t('admin.conversationDetail.label.emptyMessage')}
                      </span>
                    )}
                  </div>
                  <div
                    className={twMerge(
                      'mt-1 text-xs',
                      isUser
                        ? 'text-right text-white/70'
                        : 'text-aws-font-color-light/50 dark:text-aws-font-color-dark/50'
                    )}>
                    {formatDatetime(msg.createTime * 1000)}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default AdminConversationDetailPage;
