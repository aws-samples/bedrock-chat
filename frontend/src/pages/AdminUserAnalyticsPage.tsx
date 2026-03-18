import React, { useCallback, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import Help from '../components/Help';
import useUserUsagesForAdmin from '../hooks/useUserUsagesForAdmin';
import { addDate, formatDate } from '../utils/DateUtils';
import InputText from '../components/InputText';
import Button from '../components/Button';
import { PiArrowDown, PiArrowRight, PiUser } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';
import ListPageLayout from '../layouts/ListPageLayout';
import { useNavigate } from 'react-router-dom';

const DATA_FORMAT = 'YYYYMMDD';

const AdminUserAnalyticsPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const [searchDateFrom, setSearchDateFrom] = useState<null | string>(
    formatDate(addDate(new Date(), -1, 'month'), DATA_FORMAT)
  );
  const [searchDateTo, setSearchDateTo] = useState<null | string>(
    formatDate(new Date(), DATA_FORMAT)
  );
  const [isDescCost, setIsDescCost] = useState(true);

  const start = searchDateFrom ? searchDateFrom + '00' : undefined;
  const end = searchDateTo ? searchDateTo + '23' : undefined;

  const { userUsages, isLoading } = useUserUsagesForAdmin({ start, end });

  const sortedUsers = useMemo(() => {
    const dir = isDescCost ? -1 : 1;
    return userUsages
      ?.slice()
      .sort((a, b) => (a.totalPrice > b.totalPrice ? dir : dir * -1));
  }, [isDescCost, userUsages]);

  const validationErrorMessage = useMemo(() => {
    return !!searchDateFrom === !!searchDateTo
      ? null
      : t('admin.validationError.period');
  }, [searchDateFrom, searchDateTo, t]);

  const onClickUser = useCallback(
    (userId: string, email: string) => {
      const params = new URLSearchParams({ email });
      if (start) params.set('start', start);
      if (end) params.set('end', end);
      navigate(`/admin/user/${userId}?${params.toString()}`);
    },
    [navigate, start, end]
  );

  return (
    <ListPageLayout
      pageTitle={t('admin.userAnalytics.label.pageTitle')}
      pageTitleHelp={t('admin.userAnalytics.help.overview')}
      searchCondition={
        <div>
          <div className="rounded border p-2">
            <div className="flex items-center gap-1 text-sm font-bold">
              {t('admin.userAnalytics.label.SearchCondition.title')}
              <Help message={t('admin.userAnalytics.help.calculationPeriod')} />
            </div>
            <div className="flex gap-2 sm:w-full md:w-3/4">
              <InputText
                className="w-full"
                type="date"
                label={t('admin.userAnalytics.label.SearchCondition.from')}
                value={formatDate(searchDateFrom, 'YYYY-MM-DD')}
                onChange={(val) => {
                  if (val === '') {
                    setSearchDateFrom(null);
                    return;
                  }
                  setSearchDateFrom(formatDate(val, DATA_FORMAT));
                }}
                errorMessage={
                  searchDateFrom
                    ? undefined
                    : (validationErrorMessage ?? undefined)
                }
              />
              <InputText
                className="w-full"
                type="date"
                label={t('admin.userAnalytics.label.SearchCondition.to')}
                value={formatDate(searchDateTo, 'YYYY-MM-DD')}
                onChange={(val) => {
                  if (val === '') {
                    setSearchDateTo(null);
                    return;
                  }
                  setSearchDateTo(formatDate(val, DATA_FORMAT));
                }}
                errorMessage={
                  searchDateTo
                    ? undefined
                    : (validationErrorMessage ?? undefined)
                }
              />
            </div>
          </div>
          <div className="mt-2 flex justify-end">
            <Button
              outlined
              rightIcon={
                <PiArrowDown
                  className={twMerge(
                    'transition',
                    isDescCost ? 'rotate-0' : 'rotate-180'
                  )}
                />
              }
              onClick={() => setIsDescCost(!isDescCost)}>
              {t('admin.userAnalytics.label.sortByCost')}
            </Button>
          </div>
        </div>
      }
      isLoading={isLoading}
      isEmpty={userUsages?.length === 0}
      emptyMessage={t('admin.userAnalytics.label.noUserUsages')}>
      {sortedUsers?.map((user, idx) => (
        <button
          key={idx}
          className="flex w-full cursor-pointer items-center justify-between rounded-lg border border-black/10 bg-white px-4 py-3 text-left transition hover:bg-aws-paper dark:border-white/10 dark:bg-aws-ui-color-dark dark:hover:bg-aws-ui-color-dark/80"
          onClick={() => onClickUser(user.id, user.email)}>
          <div className="flex items-center gap-3 overflow-hidden">
            <PiUser className="shrink-0 text-xl text-aws-font-color-light/60 dark:text-aws-font-color-dark/60" />
            <div className="overflow-hidden">
              <div className="truncate font-semibold">{user.email}</div>
              <div className="truncate text-xs text-aws-font-color-light/60 dark:text-aws-font-color-dark/60">
                {user.id}
              </div>
            </div>
          </div>
          <div className="ml-4 flex shrink-0 items-center gap-3">
            <div className="text-lg font-bold">
              {(Math.floor(user.totalPrice * 100) / 100).toFixed(2)} USD
            </div>
            <PiArrowRight className="text-aws-font-color-light/40 dark:text-aws-font-color-dark/40" />
          </div>
        </button>
      ))}
    </ListPageLayout>
  );
};

export default AdminUserAnalyticsPage;
