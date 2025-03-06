import React, { useCallback, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { PiArrowDown } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';

import Help from '../components/Help';
import InputText from '../components/InputText';
import Button from '../components/Button';
import Skeleton from '../components/Skeleton';

import usePublicBotsForAdmin from '../hooks/usePublicBotsForAdmin';
import { addDate, formatDate } from '../utils/DateUtils';
import { TooltipDirection, COURSE_ID_MAP, LTI_DEPLOYMENT_ID_MAP, ValidCourseId, ValidLTIDeploymentId } from '../constants';

// Reuse the existing type
import { ListPublicBotsResponse } from '../@types/api-publication';

// Extract a single item type from the array type
type PublicBotItem = ListPublicBotsResponse[number];

// --------------------
// Optional: Helper Functions
// --------------------
const getImageSrc = (bot: PublicBotItem) => {
  if (!bot.assistantConfig) {
    return '/images/custom_assistant.png';
  }
  // If older property names exist, you can account for them:
  const assistantType =
    bot.assistantConfig.assistantType ||
    (bot.assistantConfig as any).assistant_type ||
    'custom_assistant';

  switch (assistantType) {
    case 'learning_assistant':
      return '/images/learning_assistant.png';
    case 'lesson_plan_assistant':
      return '/images/lesson_plan_assistant.png';
    case 'quiz_assistant':
      return '/images/quiz_assistant.png';
    default:
      return '/images/custom_assistant.png';
  }
};

const getCreatorName = (bot: PublicBotItem) => {
  if (!bot.creatorConfig || !bot.creatorConfig.userName) {
    return '';
  }
  return bot.creatorConfig.userName;
};

const getCanvasInstanceName = (bot: PublicBotItem) => {
  if (!bot.groupId) {
    return '';
  }
  const lti_deploymentId: ValidLTIDeploymentId = bot.groupId.split("-")[0] as ValidLTIDeploymentId;
  return LTI_DEPLOYMENT_ID_MAP[lti_deploymentId] || "";
}

const getCourseName = (bot: PublicBotItem) => {
  if (!bot.groupId) {
    return '';
  }
  const courseId: ValidCourseId = bot.groupId as ValidCourseId;
  return COURSE_ID_MAP[courseId] || "";
};


// --------------------
// Component
// --------------------
const AdminSharedBotAnalyticsPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  // Date format for backend
  const DATA_FORMAT = 'YYYYMMDD';

  // Date range state
  const [searchDateFrom, setSearchDateFrom] = useState<null | string>(
    formatDate(addDate(new Date(), -1, 'month'), DATA_FORMAT)
  );
  const [searchDateTo, setSearchDateTo] = useState<null | string>(
    formatDate(new Date(), DATA_FORMAT)
  );

  // Sort order toggle (descending by cost initially)
  const [isDescCost, setIsDescCost] = useState(true);

  // Custom hook retrieving the bots
  const { publicBots, isLoading: isLoadingPublicBots } = usePublicBotsForAdmin({
    start: searchDateFrom ? searchDateFrom + '00' : undefined,
    end: searchDateTo ? searchDateTo + '23' : undefined,
  });

  // Validation for missing date fields
  const validationErrorMessage = useMemo(() => {
    return !!searchDateFrom === !!searchDateTo
      ? null
      : t('admin.validationError.period');
  }, [searchDateFrom, searchDateTo, t]);

  // Sort the bots by cost
  const sortedBots = useMemo(() => {
    if (!publicBots) return [];

    // Avoid mutating the original array
    const copy = [...publicBots];
    const orderFactor = isDescCost ? -1 : 1;

    return copy.sort((a, b) =>
      a.totalPrice > b.totalPrice ? orderFactor : orderFactor * -1
    );
  }, [isDescCost, publicBots]);

  // Navigation to bot details
  const onClickViewBot = useCallback(
    (botId: string) => {
      navigate(`/admin/bot/${botId}`);
    },
    [navigate]
  );

  return (
    <div className="flex h-full justify-center">
      <div className="w-full px-4">
        <div className="size-full pt-8">
          {/* Page Header Section */}
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

          {/* Date Range Search Condition Section */}
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
                label={t('admin.sharedBotAnalytics.label.SearchCondition.from')}
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

          {/* Sort Button */}
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
              onClick={() => setIsDescCost(!isDescCost)}
            >
              {t('admin.sharedBotAnalytics.label.sortByCost')}
            </Button>
          </div>

          {/* Table Section */}
          <div className="overflow-x-auto">
            {/* role="table" for accessibility */}
            <div className="min-w-[900px]" role="table">
              {/* Header Row */}
              <div
                className="grid grid-cols-12 border-b border-gray py-3 text-sm font-medium"
                role="row"
              >
                <div className="col-span-3 flex items-center px-4" role="columnheader">
                  {t('admin.sharedBotAnalytics.label.assistantName') ||
                    'Assistant Name'}
                </div>
                <div className="col-span-2 flex items-center px-4" role="columnheader">
                  {t('admin.sharedBotAnalytics.label.course') || 'Course'}
                </div>
                <div className="col-span-2 flex items-center px-4" role="columnheader">
                  {t('admin.sharedBotAnalytics.label.school') || 'School'}
                </div>
                <div className="col-span-2 flex items-center px-4" role="columnheader">
                  {t('admin.sharedBotAnalytics.label.owner') || 'Owner'}
                </div>
                {/* Right-align numeric columns */}
                <div className="col-span-1 flex items-center justify-end px-4" role="columnheader">
                  {t('admin.sharedBotAnalytics.label.conversations') ||
                    'Conversations'}
                </div>
                <div className="col-span-1 flex items-center justify-end px-4" role="columnheader">
                  {t('admin.sharedBotAnalytics.label.users') || 'Users'}
                </div>
                <div className="col-span-1 flex items-center justify-end px-4" role="columnheader">
                  {t('admin.sharedBotAnalytics.label.cost') || 'Cost'}
                </div>
              </div>

              <div
                className="h-4/5 overflow-y-auto border-b border-gray pr-1 scrollbar-thin scrollbar-thumb-aws-font-color-light/20 dark:scrollbar-thumb-aws-font-color-dark/20"
                role="rowgroup"
              >
                {/* Loading Skeleton */}
                {isLoadingPublicBots && (
                  <div className="flex flex-col gap-2">
                    {new Array(15).fill('').map((_, idx) => (
                      <Skeleton key={idx} className="h-12 w-full" />
                    ))}
                  </div>
                )}

                {/* No Results */}
                {!isLoadingPublicBots && sortedBots.length === 0 && (
                  <div className="flex size-full items-center justify-center py-8 italic text-dark-gray dark:text-light-gray">
                    {t('admin.sharedBotAnalytics.label.noPublicBotUsages')}
                  </div>
                )}

                {/* Data Rows */}
                {sortedBots.map((bot: PublicBotItem, idx) => {
                  const imageSrc = getImageSrc(bot);
                  const ownerName = getCreatorName(bot) || '—';
                  const schoolName = getCanvasInstanceName(bot) || '—';
                  const courseName = getCourseName(bot) || '—';
                  const cost = (Math.floor(bot.totalPrice * 100) / 100).toFixed(2);

                  return (
                    <div
                      key={idx}
                      onClick={() => onClickViewBot(bot.id)}
                      className="grid grid-cols-12 border-b border-gray py-3 transition-colors hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer"
                      role="row"
                    >
                      {/* Assistant Name & Icon */}
                      <div className="col-span-3 px-4 flex" role="cell">
                        <div className="mr-3 flex-shrink-0" style={{ width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          <img
                            src={imageSrc}
                            alt={`Assistant icon for ${bot.title}`}
                            className="h-10 w-10 rounded-full object-contain"
                          />
                        </div>
                        <div className="flex flex-col">
                          <div className="font-medium">
                            {bot.title || '—'}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2">
                            {bot.description || t('bot.label.noDescription')}
                          </div>
                        </div>
                      </div>

                      {/* Course */}
                      <div
                        className="col-span-2 px-4 flex items-center truncate"
                        role="cell"
                      >
                        {courseName}
                      </div>

                      {/* School */}
                      <div
                        className="col-span-2 px-4 flex items-center truncate"
                        role="cell"
                      >
                        {schoolName}
                      </div>

                      {/* Owner */}
                      <div
                        className="col-span-2 px-4 flex items-center truncate"
                        role="cell"
                      >
                        {ownerName}
                      </div>

                      {/* Conversations */}
                      <div
                        className="col-span-1 flex items-center justify-end px-4 text-right font-medium"
                        role="cell"
                      >
                        {bot.numOfConvos || 0}
                      </div>

                      {/* Users */}
                      <div
                        className="col-span-1 flex items-center justify-end px-4 text-right font-medium"
                        role="cell"
                      >
                        {bot.numOfUsers || 0}
                      </div>

                      {/* Cost */}
                      <div
                        className="col-span-1 flex flex-col items-end justify-center px-4 text-right"
                        role="cell"
                      >
                        <div className="font-medium">{cost} USD</div>
                        {bot.isPublished && (
                          <div className="text-xs font-light">
                            {t('admin.sharedBotAnalytics.label.published')}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
          {/* End of Table */}
        </div>
      </div>
    </div>
  );
};

export default AdminSharedBotAnalyticsPage;
