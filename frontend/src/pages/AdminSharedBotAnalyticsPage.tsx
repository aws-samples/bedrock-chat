import React, { useCallback, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import Help from '../components/Help';
import usePublicBotsForAdmin from '../hooks/usePublicBotsForAdmin';
import ListItemBot from '../components/ListItemBot';
import { addDate, formatDate } from '../utils/DateUtils';

import InputText from '../components/InputText';
import Button from '../components/Button';
import { PiArrowDown } from 'react-icons/pi';
import Skeleton from '../components/Skeleton';
import { twMerge } from 'tailwind-merge';
import { useNavigate } from 'react-router-dom';
import { TooltipDirection } from '../constants';

const DATA_FORMAT = 'YYYYMMDD';

const AdminSharedBotAnalyticsPage: React.FC = () => {
  const { t } = useTranslation();

  const [searchDateFrom, setSearchDateFrom] = useState<null | string>(
    formatDate(addDate(new Date(), -1, 'month'), DATA_FORMAT)
  );
  const [searchDateTo, setSearchDateTo] = useState<null | string>(
    formatDate(new Date(), DATA_FORMAT)
  );
  const [isDescCost, setIsDescCost] = useState(true);

  const { publicBots, isLoading: isLoadingPublicBots } = usePublicBotsForAdmin({
    start: searchDateFrom ? searchDateFrom + '00' : undefined,
    end: searchDateTo ? searchDateTo + '23' : undefined,
  });

  const sortedBots = useMemo(() => {
    const tmp = isDescCost ? -1 : 1;
    return publicBots?.sort((a, b) =>
      a.totalPrice > b.totalPrice ? tmp : tmp * -1
    );
  }, [isDescCost, publicBots]);

  const validationErrorMessage = useMemo(() => {
    return !!searchDateFrom === !!searchDateTo
      ? null
      : t('admin.validationError.period');
  }, [searchDateFrom, searchDateTo, t]);

  const navigate = useNavigate();

  const onClickViewBot = useCallback(
    (botId: string) => {
      navigate(`/admin/bot/${botId}`);
    },
    [navigate]
  );

  return (
    <>
      <div className="flex h-full justify-center">
        <div className="w-full px-4">
          <div className="size-full pt-8">
            <div className="flex items-end justify-between">
              <div className="flex items-center gap-2">
                <div className="text-xl font-bold">
                  {t('admin.sharedBotAnalytics.label.pageTitle')}
                </div>
                <Help
                  direction={TooltipDirection.RIGHT}
                  message={t('admin.sharedBotAnalytics.help.overview')}
                />
              </div>
            </div>
  
            <div className="my-2 rounded border p-2">
              <div className="flex items-center gap-1 text-sm font-bold">
                {t('admin.sharedBotAnalytics.label.SearchCondition.title')}
                <Help
                  message={t('admin.sharedBotAnalytics.help.calculationPeriod')}
                />
              </div>
  
              <div className="flex gap-2 sm:w-full md:w-3/4">
                <InputText
                  className="w-full"
                  type="date"
                  label={t(
                    'admin.sharedBotAnalytics.label.SearchCondition.from'
                  )}
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
                      : validationErrorMessage ?? undefined
                  }
                />
                <InputText
                  className="w-full"
                  type="date"
                  label={t('admin.sharedBotAnalytics.label.SearchCondition.to')}
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
                      : validationErrorMessage ?? undefined
                  }
                />
              </div>
            </div>
  
            <div className="my-2 flex justify-end">
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
                onClick={() => {
                  setIsDescCost(!isDescCost);
                }}>
                {t('admin.sharedBotAnalytics.label.sortByCost')}
              </Button>
            </div>
  
            {/* Container with horizontal scroll */}
            <div className="overflow-x-auto">
              {/* Table with minimum width to allow horizontal scroll */}
              <div style={{ minWidth: "900px" }}>
                {/* Header row with the same structure as ListItemBot */}
                <div className="flex border-b border-gray py-2 text-sm font-medium">
                  <div className="flex flex-grow">
                    <div className="px-4 w-1/3">Assistant Name</div>
                    <div className="px-4 w-1/3">Class</div>
                    <div className="px-4 w-1/3">School</div>
                  </div>
                  <div className="flex min-w-fit">
                    <div className="w-24 text-center">Conversations</div>
                    <div className="w-16 text-center">Users</div>
                    <div className="w-20 text-center">Cost</div>
                  </div>
                </div>
            
                <div className="h-4/5 overflow-y-auto border-b border-gray pr-1 scrollbar-thin scrollbar-thumb-aws-font-color-light/20 dark:scrollbar-thumb-aws-font-color-dark/20">
                  {isLoadingPublicBots && (
                    <div className="flex flex-col gap-2">
                      {new Array(15).fill('').map((_, idx) => {
                        return <Skeleton key={idx} className="h-12 w-full" />;
                      })}
                    </div>
                  )}
      
                  {publicBots?.length === 0 && (
                    <div className="flex size-full items-center justify-center italic text-dark-gray dark:text-light-gray">
                      {t('admin.sharedBotAnalytics.label.noPublicBotUsages')}
                    </div>
                  )}
                  
                  {sortedBots?.map((bot, idx) => {
                    // Create a properly structured bot object for ListItemBot
                    const enhancedBot = {
                      id: bot.id,
                      title: bot.title || "",
                      description: bot.description || "",
                      available: true,
                      assistantConfig: bot.assistantConfig ? {
                        ...bot.assistantConfig,
                        // Set assistantType based on available data
                        assistantType: bot.assistantConfig.assistantType || 
                                       (bot.assistantConfig as any).assistant_type || 
                                       "custom_assistant"
                      } : null,
                      creatorConfig: bot.creatorConfig,
                      groupId: bot.groupId || null
                    };
                    
                    return (
                      <ListItemBot
                        key={idx}
                        bot={enhancedBot}
                        onClick={() => {
                          onClickViewBot(bot.id);
                        }}>
                        <div className="flex min-w-fit">
                          <div className="w-24 text-center font-bold">
                            {bot.numOfConvos}
                          </div>
                          <div className="w-16 text-center font-bold">
                            {bot.numOfUsers}
                          </div>
                          <div className="w-20 text-center font-bold relative">
                            {(Math.floor(bot.totalPrice * 100) / 100).toFixed(2)} USD
                            {bot.isPublished && (
                              <div className="absolute bottom-0 right-0 text-xs font-light">
                                {t('admin.sharedBotAnalytics.label.published')}
                              </div>
                            )}
                          </div>
                        </div>
                      </ListItemBot>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default AdminSharedBotAnalyticsPage;