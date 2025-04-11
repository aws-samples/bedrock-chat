import React, { useEffect, useState, useMemo, useCallback, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { formatDate } from '../utils/DateUtils';
import InputText from '../components/InputText';
import Skeleton from '../components/Skeleton';
import Help from '../components/Help';
import { TooltipDirection } from '../constants';
import { useAnalytics, BotAnalytics } from '../hooks/useAnalytics';
import SummaryStats from '../components/analytics/SummaryStats';
import UsageTrendChart from '../components/analytics/UsageTrendChart';
import TopUsersTable from '../components/analytics/TopUsersTable';
// import TopicAnalysisChart from '../components/analytics/TopicAnalysisChart';
import TokenCountsChart from '../components/analytics/TokenCountsChart';
import { debounce } from 'lodash';
import Button from '../components/Button';
import useUser from '../hooks/useUser';
import { fillMissingDatesWithZeros } from '../utils/chartUtils';

// Define the structure for transformed chart data
interface BotChartDataPoint {
  date: string; // YYYY-MM-DD
  // Map directly from DailyUsage properties returned by API/hook
  num_messages: number;
  num_sessions: number;
  input_tokens: number;
  output_tokens: number;
  cost: number;
  // Remove additional properties not directly available daily
  // total_messages: number;
  // total_cost: number;
  // total_prompt_tokens: number;
  // total_completion_tokens: number;
}

// Define the summary stats structure to match SummaryStats component requirements
interface BotSummaryStats {
  total_bots: number;
  total_users: number;
  total_sessions: number;
  total_messages: number;
  total_input_tokens: number;
  total_output_tokens: number;
  total_cost: number;
  showTotalBots?: boolean;
}

const QikrBotAnalyticsPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { botId } = useParams<{ botId: string }>();
  const { emailId } = useUser();
  const { 
    getBotAnalytics, 
    loadingState, 
    error,
    clearAnalyticsEndpointErrors
  } = useAnalytics(emailId);
  const [analyticsData, setAnalyticsData] = useState<BotAnalytics | null>(null);
  const [searchDateFrom, setSearchDateFrom] = useState<string | null>(null);
  const [searchDateTo, setSearchDateTo] = useState<string | null>(null);
  
  // Temporary date state for input
  const [tempDateFrom, setTempDateFrom] = useState<string | null>(null);
  const [tempDateTo, setTempDateTo] = useState<string | null>(null);

  const [chartData, setChartData] = useState<BotChartDataPoint[]>([]);
  const [summaryStats, setSummaryStats] = useState<BotSummaryStats | null>(null);
  
  // Ref to track the last successfully fetched date range
  const lastSuccessfulDateRangeRef = useRef<{ from: string | null; to: string | null }>({ from: null, to: null });
  const location = useLocation();

  const debouncedFetch = useMemo(() => {
    return debounce((botIdParam: string, from: string, to: string, forceRefresh: boolean = false) => {
      if (botIdParam && from && to) {
        console.debug(`Fetching analytics for bot ${botIdParam} from ${from} to ${to}, forceRefresh: ${forceRefresh}`);
        clearAnalyticsEndpointErrors?.(); 
        getBotAnalytics(botIdParam, from, to, undefined, forceRefresh)
          .then((data) => {
            if (data) {
              setAnalyticsData(data);
              
              // Use the utility function to fill missing dates (now expects YYYYMMDD)
              console.log('[AnalyticsBotPage] Calling fillMissingDatesWithZeros with dates:', from, to); // Keep YYYYMMDD

              const filledChartData = fillMissingDatesWithZeros<BotChartDataPoint>(
                from || '', // Pass original YYYYMMDD
                to || '',   // Pass original YYYYMMDD
                data.daily_usage || [], // Use data from the hook
                (rawPoint) => { // mapDataPoint function
                    // Convert rawPoint.date (assume YYYY-MM-DD) to YYYYMMDD
                    let dateYYYYMMDD = '';
                    if (rawPoint.date && /^\d{4}-\d{2}-\d{2}$/.test(rawPoint.date)) {
                        dateYYYYMMDD = rawPoint.date.replace(/-/g, '');
                    } else if (rawPoint.date && /^\d{8}$/.test(rawPoint.date)) {
                         dateYYYYMMDD = rawPoint.date; // Already YYYYMMDD
                    } else {
                         console.warn("Unrecognized date format in rawPoint for mapping:", rawPoint.date);
                    }

                    return {
                        date: dateYYYYMMDD, // Ensure YYYYMMDD format
                        num_messages: rawPoint.num_messages ?? 0,
                        num_sessions: rawPoint.num_sessions ?? 0,
                        input_tokens: rawPoint.input_tokens ?? 0,
                        output_tokens: rawPoint.output_tokens ?? 0,
                        cost: rawPoint.cost ?? 0,
                    };
                },
                (dateStrYYYYMMDD) => ({ // createZeroPoint function (receives YYYYMMDD)
                  date: dateStrYYYYMMDD, // Use YYYYMMDD directly
                  num_messages: 0,
                  num_sessions: 0,
                  input_tokens: 0,
                  output_tokens: 0,
                  cost: 0,
                })
              );
              setChartData(filledChartData); // Chart data now has YYYYMMDD dates

              // Set summary stats - ensure this uses appropriate fields from 'data'
              setSummaryStats({
                total_bots: 1, // Assuming single bot view
                total_users: data.total_users ?? 0,
                total_sessions: data.total_sessions ?? 0,
                total_messages: data.total_messages ?? 0,
                total_input_tokens: data.total_input_tokens ?? 0,
                total_output_tokens: data.total_output_tokens ?? 0,
                total_cost: data.total_cost ?? 0,
                showTotalBots: false,
              });

              // Update last successful range only *after* a successful fetch
              lastSuccessfulDateRangeRef.current = { from, to }; 
            } else {
              setAnalyticsData(null);
              setChartData([]);
              setSummaryStats(null);
              // Optionally clear the last successful range on error
              lastSuccessfulDateRangeRef.current = { from: null, to: null }; 
            }
          })
          .catch((err) => {
            console.error('Error fetching bot analytics:', err);
            setAnalyticsData(null);
            setChartData([]);
            setSummaryStats(null);
            // Optionally clear the last successful range on error
            lastSuccessfulDateRangeRef.current = { from: null, to: null }; 
          });
      }
    }, 300);
  }, [getBotAnalytics, clearAnalyticsEndpointErrors]);

  // Initialize date range on component mount
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const startDateParam = queryParams.get('startDate');
    const endDateParam = queryParams.get('endDate');

    let initialStartDate: string;
    let initialEndDate: string;

    if (startDateParam && endDateParam) {
      // Use dates from query parameters if available
      initialStartDate = startDateParam;
      initialEndDate = endDateParam;
      console.debug(`Using date range from URL params: ${initialStartDate} - ${initialEndDate}`);
    } else {
      // Fallback to default (last 30 days)
      const today = new Date();
      initialEndDate = today.toISOString().slice(0, 10).replace(/-/g, '');
      const defaultStartDate = new Date(new Date().setDate(today.getDate() - 29));
      initialStartDate = defaultStartDate.toISOString().slice(0, 10).replace(/-/g, '');
       console.debug(`No date range in URL params, defaulting to last 30 days: ${initialStartDate} - ${initialEndDate}`);
    }

    setSearchDateFrom(initialStartDate);
    setSearchDateTo(initialEndDate);
    setTempDateFrom(initialStartDate);
    setTempDateTo(initialEndDate);

  }, [location.search]);

  // Effect to reset state when botId changes
  useEffect(() => {
    if (botId) {
      console.debug("Bot ID changed, resetting state:", { newBotId: botId });
      
      // Reset data and loading state for the new bot
      setAnalyticsData(null);
      setChartData([]);
      setSummaryStats(null);
      lastSuccessfulDateRangeRef.current = { from: null, to: null }; // Reset last successful fetch range
      
      // Note: We no longer call fetch directly here. The main fetch effect will handle it.
    }
  }, [botId]); // Only depends on botId

  // Main effect to trigger data load when botId or *applied* dates change,
  // or on initial load when all parameters are available.
  useEffect(() => {
    // Only proceed if we have all required parameters and not currently loading
    if (botId && searchDateFrom && searchDateTo && !loadingState.botAnalytics && !error) {
      
      // Check if data for this exact range has already been successfully fetched
      if (lastSuccessfulDateRangeRef.current.from === searchDateFrom &&
          lastSuccessfulDateRangeRef.current.to === searchDateTo) {
            console.debug(`Skipping fetch - already have data for ${searchDateFrom} - ${searchDateTo}`);
            return; // Don't fetch again
      }

      console.debug(`Data load triggered for bot ${botId}, dates: ${searchDateFrom}-${searchDateTo}`);
            
      // Force refresh should generally be false for default fetches, true only for manual reload
      
      // Add a small delay before fetching
      const timeoutId = setTimeout(() => {
        // Pass false for forceRefresh here to allow caching
        debouncedFetch(botId, searchDateFrom, searchDateTo, false); 
      }, 50); // Reduced delay, maybe 50ms is enough
      
      return () => {
        clearTimeout(timeoutId);
        // Cancel the debounced fetch if component unmounts or params change quickly
        debouncedFetch.cancel(); 
      };
    }
  // Dependencies: botId, applied dates, fetch function, loading state, error
  }, [botId, searchDateFrom, searchDateTo, debouncedFetch, loadingState.botAnalytics, error]); 
  
  // Update the date range function to set both temp and applied dates
  const setDateRangeAndApply = useCallback((days: number) => {
    // Allow new fetch by resetting the last successful range
    lastSuccessfulDateRangeRef.current = { from: null, to: null }; 
    const today = new Date();
    const endDate = formatDate(today, 'YYYYMMDD');
    const startDate = new Date();
    startDate.setDate(today.getDate() - (days - 1));
    const formattedStartDate = formatDate(startDate, 'YYYYMMDD');
    
    console.debug(`Setting and applying date range: ${formattedStartDate} to ${endDate}`);
    
    // Set temp state for UI consistency
    setTempDateFrom(formattedStartDate);
    setTempDateTo(endDate);
    
    // Apply the dates immediately to trigger fetch
    setSearchDateFrom(formattedStartDate);
    setSearchDateTo(endDate);

  }, []);

  // Function to handle changes in date inputs (updates temp state only)
  const handleTempDateChange = useCallback((type: 'from' | 'to', value: string | null) => {
    const formattedValue = value ? formatDate(value, 'YYYYMMDD') : null;
    if (type === 'from') {
      setTempDateFrom(formattedValue);
    } else {
      setTempDateTo(formattedValue);
    }
  }, []);

  // Function to apply the temporary date range
  const handleApplyDateRange = useCallback(() => {
    if (tempDateFrom && tempDateTo) {
       // Allow new fetch by resetting the last successful range
       lastSuccessfulDateRangeRef.current = { from: null, to: null };
      console.debug(`Applying custom date range: ${tempDateFrom} - ${tempDateTo}`);
      setSearchDateFrom(tempDateFrom);
      setSearchDateTo(tempDateTo);
    } else {
      console.warn("Cannot apply incomplete date range.");
      // Maybe add user feedback here
    }
  }, [tempDateFrom, tempDateTo]);

  // Update the Reload button click handler
  const handleReload = useCallback(() => {
    if (botId && searchDateFrom && searchDateTo && !loadingState.botAnalytics) {
      console.debug("Manual reload initiated", { botId, dates: { from: searchDateFrom, to: searchDateTo } });
      
      // Clear previous analytics data and reset last successful fetch range
      setAnalyticsData(null);
      setChartData([]);
      setSummaryStats(null);
      lastSuccessfulDateRangeRef.current = { from: null, to: null };
            
      // Use a small timeout to ensure state updates have processed
      setTimeout(() => {
        // Force a refresh to bypass cache
        debouncedFetch(botId, searchDateFrom, searchDateTo, true);
      }, 50);
    }
  }, [botId, searchDateFrom, searchDateTo, debouncedFetch, loadingState.botAnalytics]); // Removed resetDataLoadingState dependency

  if (error) {
    return (
      <div className="flex h-full flex-col items-center justify-center p-8">
        <div className="bg-red-50 dark:bg-red-900/30 p-6 rounded-lg max-w-2xl w-full text-center">
          <svg className="w-16 h-16 text-red-500 dark:text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 className="text-xl font-bold text-red-700 dark:text-red-300 mb-2">Analytics Unavailable</h2>
          <p className="text-gray-700 dark:text-gray-300 mb-4">{error}</p>
          <div className="flex flex-wrap justify-center gap-4 mt-6">
            <button
              onClick={() => navigate('/analytics')}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
            >
              Return to Main Analytics
            </button>
            <button
              onClick={() => {
                if (botId && searchDateFrom && searchDateTo) {
                  debouncedFetch(botId, searchDateFrom, searchDateTo, true);
                }
              }}
              className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white rounded hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!botId) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-red-500">Invalid bot ID</div>
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-end justify-between p-4 border-b">
        <div className="flex items-center gap-2">
          <div className="text-xl font-bold">
            {loadingState.botAnalytics ? 'Loading...' : (analyticsData?.title || `Bot ID: ${botId}`)}
          </div>
          <Help
            direction={TooltipDirection.RIGHT}
            message={t('analytics.botAnalytics.help.overview', 'Detailed analytics for this specific assistant.')}
          />
        </div>
        <button
          onClick={() => {
            // Check if dates are set before appending
            if (searchDateFrom && searchDateTo) {
              navigate(`/analytics?startDate=${searchDateFrom}&endDate=${searchDateTo}`);
            } else {
              navigate('/analytics'); // Fallback if no dates are set
            }
          }}
          className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          {t('analytics.botAnalytics.button.backToDashboard', 'Back to Dashboard')}
        </button>
      </div>

      <div className="flex-grow p-4 overflow-y-auto">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 mb-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-1">
              <span className="font-medium text-gray-700 dark:text-gray-300">Calculation Period</span>
              <Help message={t('analytics.help.calculationPeriod', 'Select a date range to view analytics data for that period.')} />
            </div>
            <div className="flex gap-2">
               <button onClick={() => setDateRangeAndApply(1)} className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm rounded-md hover:bg-blue-200 transition-colors font-medium">Today</button>
               <button onClick={() => setDateRangeAndApply(7)} className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm rounded-md hover:bg-blue-200 transition-colors font-medium">7 Days</button>
               <button onClick={() => setDateRangeAndApply(30)} className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm rounded-md hover:bg-blue-200 transition-colors font-medium">30 Days</button>
               <button 
                 onClick={handleReload}
                 className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors font-medium"
                 data-testid="reload-bot-button"
               >
                 Reload
               </button>
             </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 items-end">
            <div className="w-full sm:w-1/2">
              <InputText
                className="w-full"
                type="date"
                label="From"
                value={tempDateFrom ? formatDate(tempDateFrom, 'YYYY-MM-DD') : ''}
                onChange={(val) => handleTempDateChange('from', val ? val : null)}
                data-testid="date-from-input"
              />
            </div>
            <div className="w-full sm:w-1/2">
              <InputText
                className="w-full"
                type="date"
                label="To"
                value={tempDateTo ? formatDate(tempDateTo, 'YYYY-MM-DD') : ''}
                onChange={(val) => handleTempDateChange('to', val ? val : null)}
                data-testid="date-to-input"
              />
            </div>
            <Button
              onClick={handleApplyDateRange}
              disabled={!tempDateFrom || !tempDateTo}
              className="px-3 py-1.5 h-[38px] text-sm font-medium mb-[1px]"
              data-testid="apply-dates-button-bot"
            >
              Apply
            </Button>
          </div>
        </div>

        {loadingState.botAnalytics ? (
          <div className="space-y-4" aria-busy="true" aria-label="Loading bot analytics">
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-48 w-full" />
            <Skeleton className="h-48 w-full" />
          </div>
        ) : analyticsData && summaryStats ? (
          <div className="space-y-6">
            <SummaryStats stats={summaryStats} />

            {chartData.length > 0 ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 1. Sessions */}
                <UsageTrendChart
                  data={chartData}
                  title={t('analytics.botAnalytics.charts.dailySessions', 'Daily Sessions')}
                  dataKey="num_sessions"
                  yAxisLabel="Sessions"
                />
                {/* 2. Messages */}
                <UsageTrendChart
                  data={chartData}
                  title={t('analytics.botAnalytics.charts.dailyMessages', 'Daily Messages')}
                  dataKey="num_messages"
                  yAxisLabel="Messages"
                />
                {/* 3. Cost */}
                {summaryStats?.total_cost !== null && (
                  <UsageTrendChart
                    data={chartData}
                    title={t('analytics.botAnalytics.charts.dailyCost', 'Daily Cost')}
                    dataKey="cost"
                    yAxisLabel="Cost ($)"
                  />
                )}
                {/* 4. Tokens */}
                {summaryStats?.total_input_tokens !== null && summaryStats?.total_output_tokens !== null && (
                  <TokenCountsChart
                    data={chartData}
                    title={t('analytics.botAnalytics.charts.tokenUsage', 'Token Usage')}
                    yAxisLabel="Tokens"
                  />
                )}
              </div>
            ) : (
              <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg text-center">
                 <h3 className="text-lg font-semibold mb-2">No Daily Activity</h3>
                 <p>No messages or token usage recorded for this bot in this period.</p>
                 {summaryStats && (
                   <p className="text-sm mt-2">
                     Summary: {summaryStats.total_users} Users, {summaryStats.total_sessions} Sessions.
                   </p>
                 )}
              </div>
            )}

            {analyticsData.top_users && analyticsData.top_users.length > 0 ? (
              <TopUsersTable
                users={analyticsData.top_users}
                title={t('analytics.botAnalytics.tables.topUsers', 'Top Users')}
              />
            ) : (
               !loadingState.botAnalytics && chartData.length > 0 &&
               <p className="text-center text-gray-500 dark:text-gray-400">No specific user data available for this period.</p>
            )}
          </div>
        ) : (
           !loadingState.botAnalytics && !error && (
             <div className="text-center p-8">
               <p>No analytics data found for this bot in the selected period.</p>
               <p className="text-sm text-gray-500">Try selecting a different date range.</p>
             </div>
           )
        )}
      </div>
    </div>
  );
};

export default QikrBotAnalyticsPage; 