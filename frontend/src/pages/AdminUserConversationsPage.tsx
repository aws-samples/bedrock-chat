import React, { useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import useUserConversationsForAdmin from '../hooks/useUserConversationsForAdmin';
import { formatDatetime } from '../utils/DateUtils';
import ListPageLayout from '../layouts/ListPageLayout';
import { PiArrowLeft, PiRobot } from 'react-icons/pi';
import Button from '../components/Button';

const AdminUserConversationsPage: React.FC = () => {
  const { t } = useTranslation();
  const { userId } = useParams<{ userId: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const start = searchParams.get('start') ?? undefined;
  const end = searchParams.get('end') ?? undefined;
  const email = searchParams.get('email') ?? userId ?? '';

  const { conversations, isLoading } = useUserConversationsForAdmin(
    userId ?? '',
    { start, end }
  );

  const sortedConversations = useMemo(
    () =>
      conversations
        ?.slice()
        .sort((a, b) => b.createTime - a.createTime),
    [conversations]
  );

  return (
    <ListPageLayout
      pageTitle={t('admin.userConversations.label.pageTitle')}
      pageTitleHelp={t('admin.userConversations.help.overview')}
      searchCondition={
        <div className="flex flex-col gap-2">
          <Button
            outlined
            icon={<PiArrowLeft />}
            className="w-fit"
            onClick={() => navigate(-1)}>
            {t('admin.userConversations.button.back')}
          </Button>
          <div className="rounded border p-3 text-sm">
            <div className="font-bold">
              {t('admin.userConversations.label.user')}
            </div>
            <div className="text-aws-font-color-light/70 dark:text-aws-font-color-dark/70">
              {email}
            </div>
          </div>
        </div>
      }
      isLoading={isLoading}
      isEmpty={conversations?.length === 0}
      emptyMessage={t('admin.userConversations.label.noConversations')}>
      {sortedConversations?.map((conv) => (
        <div
          key={conv.id}
          className="flex items-center justify-between rounded-lg border border-black/10 bg-white px-4 py-3 dark:border-white/10 dark:bg-aws-ui-color-dark">
          <div className="overflow-hidden">
            <div className="truncate font-semibold">
              {conv.title || t('admin.userConversations.label.untitled')}
            </div>
            <div className="mt-0.5 flex items-center gap-2 text-xs text-aws-font-color-light/60 dark:text-aws-font-color-dark/60">
              <span>
                {formatDatetime(conv.createTime * 1000)}
              </span>
              {conv.botId && (
                <span className="flex items-center gap-1">
                  <PiRobot className="inline" />
                  {conv.botId}
                </span>
              )}
            </div>
          </div>
          <div className="ml-4 shrink-0 text-lg font-bold">
            {(Math.floor(conv.totalPrice * 100) / 100).toFixed(2)} USD
          </div>
        </div>
      ))}
    </ListPageLayout>
  );
};

export default AdminUserConversationsPage;
