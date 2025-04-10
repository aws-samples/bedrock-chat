import React, { useCallback, useEffect, useState, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { formatDate } from '../utils/DateUtils';
import InputText from '../components/InputText';
import Skeleton from '../components/Skeleton';
import Help from '../components/Help';
import { TooltipDirection } from '../constants';
import useUser from '../hooks/useUser';
import { 
  useAnalytics, 
  SummaryAnalyticsData, 
  TopEntitiesData, 
  TopicsData,
  DailyUsage
} from '../hooks/useAnalytics';
import SummaryStats from '../components/analytics/SummaryStats';
import UsageTrendChart from '../components/analytics/UsageTrendChart';
import TopUsersTable from '../components/analytics/TopUsersTable';
import TokenCountsChart from '../components/analytics/TokenCountsChart';
import Button from '../components/Button';

// Define a separate interface for chart data
interface DashboardChartDataPoint {
  date: string;
  num_messages: number;
  input_tokens: number | null;
  output_tokens: number | null;
  cost: number | null;
  num_sessions: number;
}

// Define a type for the summary stats based on SummaryStats component props
interface SummaryStatsProps {
  total_bots: number;
  total_users: number;
  total_sessions: number;
  total_messages: number;
  total_input_tokens: number | null;
  total_output_tokens: number | null;
  total_cost: number | null;
  showTotalBots?: boolean;
}

/**
 * Analytics Dashboard component for Qikr
 * Provides a progressive loading experience with fast metrics loading first,
 * followed by supplementary data
 */
const QikrAnalyticsDashboard: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { emailId } = useUser();
  // Use analytics hook with destructured properties for cleaner code
  const { 
    getSummaryMetrics,
    getTopEntities,
    getTopicsAnalysis,
    loadingState, 
    error: apiError,
    clearAnalyticsEndpointErrors,
    clearAllAnalyticsCaches
  } = useAnalytics(emailId);
  
  // Date range state (these now represent the *applied* range)
  const [searchDateFrom, setSearchDateFrom] = useState<string | null>(null);
  const [searchDateTo, setSearchDateTo] = useState<string | null>(null);
  
  // Temporary date state for user input before applying
  const [tempDateFrom, setTempDateFrom] = useState<string | null>(null);
  const [tempDateTo, setTempDateTo] = useState<string | null>(null);

  // UI state
  const [localError, setLocalError] = useState<string | null>(null);
  
  // Data state - using null to indicate not loaded yet
  const [summaryData, setSummaryData] = useState<SummaryAnalyticsData | null>(null);
  const [topEntities, setTopEntities] = useState<TopEntitiesData | null>(null);
  const [topicsData, setTopicsData] = useState<TopicsData | null>(null);
  // Add these derived states instead of redeclaring them later
  const [chartData, setChartData] = useState<DashboardChartDataPoint[]>([]);
  const [summaryStats, setSummaryStats] = useState<SummaryStatsProps | null>(null);
  
  // Memoized combined error from API or local state
  const displayError = useMemo(() => 
    apiError || localError, 
    [apiError, localError]
  );
  
  /**
   * Reference to track if we're already loading data to prevent loops
   */
  const loadingRef = React.useRef(false);
  
  /**
   * Track all pending requests to ensure we only mark loading as complete
   * when ALL scheduled API calls have finished
   */
  const pendingRequestsRef = React.useRef(0);
  
  // Add request counter to prevent excessive retries
  const requestCountRef = React.useRef(0);
  const lastRequestTimeRef = React.useRef(0);
  
  // Create a stable reference to track the last successful date range
  const lastSuccessfulDateRange = React.useRef<{from: string | null, to: string | null}>({
    from: null,
    to: null
  });
  
  /**
   * Calculate the number of days between two dates in YYYYMMDD format
   */
  const calculateDateRange = useCallback((from: string | null, to: string | null): number => {
    if (!from || !to) {
      return 0;
    }
    
    try {
      const fromDate = new Date(
        parseInt(from.substring(0, 4)),
        parseInt(from.substring(4, 6)) - 1,
        parseInt(from.substring(6, 8))
      );
      
      const toDate = new Date(
        parseInt(to.substring(0, 4)),
        parseInt(to.substring(4, 6)) - 1, 
        parseInt(to.substring(6, 8))
      );
      
      const diffTime = Math.abs(toDate.getTime() - fromDate.getTime());
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    } catch (err) {
      console.error("Error calculating date range:", err);
      return 0;
    }
  }, []);

  /**
   * Calculate date range warning
   */
  const dateRangeWarning = useMemo(() => {
    const days = calculateDateRange(searchDateFrom, searchDateTo);
    if (days > 30) {
      return `Date range is ${days} days. Large date ranges may take longer to load. Consider using a smaller range for better performance.`;
    }
    return null;
  }, [searchDateFrom, searchDateTo, calculateDateRange]);

  /**
   * Load dashboard data in stages - first fast metrics, then supplementary data
   * Add forceRefresh flag to bypass cache
   */
  const loadDashboardData = useCallback(async (forceRefresh: boolean = false) => {
    // Validate required inputs
    if (!searchDateFrom || !searchDateTo) {
      return;
    }
    
    // Reset error state when starting a new data load
    setLocalError(null);
    setChartData([]);
    setSummaryStats(null);
    
    try {
      // Track request start time for logging
      const fullStartTime = Date.now();
      
      // Initialize pending requests counter for this loading cycle
      // Start with 1 for the fast metrics request
      pendingRequestsRef.current = 1;
      
      // Stage 1: Load essential metrics first (critical for dashboard)
      console.debug(`Requesting summary data${forceRefresh ? ' (forcing refresh)' : ''}`);
      const startTime = Date.now();
      
      try {
        // Pass forceRefresh flag to hook call
        const fetchedSummaryData = await getSummaryMetrics(searchDateFrom, searchDateTo, undefined, forceRefresh);
        const elapsed = Date.now() - startTime;
        console.debug(`Summary data request completed in ${elapsed}ms`);
        
        // First request complete
        pendingRequestsRef.current--;
        
        // Make sure we received valid data and not an aborted/canceled request
        if (!fetchedSummaryData) {
          console.warn("No summary data received - request may have been canceled");
          // Only set error if we're forcing a refresh and still didn't get data
          if (forceRefresh) {
            setLocalError("Failed to fetch basic analytics data. Please try a smaller date range.");
          }
          loadingRef.current = false; // Ensure loading state is reset
          return;
        }
        
        // Check if we have valid summary data
        if (!fetchedSummaryData.summary) {
          console.warn("Received summary data but missing summary object");
          setLocalError("Incomplete analytics data received. Please try again.");
          loadingRef.current = false;
          return;
        }
        
        // Clear any existing error since we have data
        setLocalError(null);
        setSummaryData(fetchedSummaryData);
        
        // Process the fetched data
        if (!fetchedSummaryData.daily_usage || fetchedSummaryData.daily_usage.length === 0) {
          console.debug('No daily usage data available for the selected period');
          setChartData([]);
          // Populate summary stats even without daily data - Map backend field names to frontend component expectations
          if (fetchedSummaryData.summary) {
            setSummaryStats({
              total_bots: fetchedSummaryData.summary.total_bots || 0,
              total_users: fetchedSummaryData.summary.total_users || 0,
              total_sessions: fetchedSummaryData.summary.num_sessions || 0,
              total_messages: fetchedSummaryData.summary.num_messages || 0,
              total_input_tokens: fetchedSummaryData.summary.input_tokens,
              total_output_tokens: fetchedSummaryData.summary.output_tokens,
              total_cost: fetchedSummaryData.summary.cost,
            });
          }
        } else {
          // Transform daily usage data for charts with proper type conversion
          const transformedChartData: DashboardChartDataPoint[] = fetchedSummaryData.daily_usage.map((day: DailyUsage) => ({
            date: day.date,
            num_messages: Number(day.num_messages) || 0,
            input_tokens: day.input_tokens !== null ? Number(day.input_tokens) : null,
            output_tokens: day.output_tokens !== null ? Number(day.output_tokens) : null,
            cost: day.cost !== null ? Number(day.cost) : null,
            num_sessions: Number(day.num_sessions) || 0
          }));
          
          console.debug('Transformed chart data:', transformedChartData);
          setChartData(transformedChartData);

          // Set summary statistics - Map backend field names to frontend component expectations
          if (fetchedSummaryData.summary) {
            setSummaryStats({
              total_bots: fetchedSummaryData.summary.total_bots || 0,
              total_users: fetchedSummaryData.summary.total_users || 0,
              total_sessions: fetchedSummaryData.summary.num_sessions || 0,
              total_messages: fetchedSummaryData.summary.num_messages || 0,
              total_input_tokens: fetchedSummaryData.summary.input_tokens,
              total_output_tokens: fetchedSummaryData.summary.output_tokens,
              total_cost: fetchedSummaryData.summary.cost,
            });
          }
        }
        
        // Update the successful date range reference ONLY after successful fetch and processing
        lastSuccessfulDateRange.current = {
          from: searchDateFrom,
          to: searchDateTo
        };
        console.debug(`Updated successful date range reference: ${searchDateFrom} to ${searchDateTo}`);

        // Stage 2: Load top entities asynchronously after basic metrics are available
        const dateRange = calculateDateRange(searchDateFrom, searchDateTo);
        
        // No artificial delay needed, fetch immediately - increment counter before starting
        pendingRequestsRef.current++;
        
        // Load top entities 
        getTopEntities(searchDateFrom, searchDateTo, undefined, undefined, forceRefresh)
          .then(data => {
            if (data) {
              setTopEntities(data);
            }
          })
          .catch(err => {
            console.warn("Failed to load top entities data:", err);
            // Don't fail the whole dashboard for this secondary data
          })
          .finally(() => {
            // Decrement pending requests when entities load finishes
            pendingRequestsRef.current = Math.max(0, pendingRequestsRef.current - 1);
            
            // Check if we should mark loading as complete
            if (pendingRequestsRef.current === 0) {
              console.debug('All analytics requests complete - marking loading as done');
              loadingRef.current = false;
              // Reset request counter on success of ALL requests
              requestCountRef.current = 0;
            }
          });
        
        // Stage 3: For smaller date ranges, also load topic analysis 
        if (dateRange <= 30) { 
          // Increment pending requests before starting topics load
          pendingRequestsRef.current++;
          
          // Load topic analysis 
          getTopicsAnalysis(searchDateFrom, searchDateTo, undefined, undefined, forceRefresh)
            .then(data => {
              if (data) {
                setTopicsData(data);
              }
            })
            .catch(err => {
              console.warn("Failed to load topic analysis data:", err);
              // Don't fail the whole dashboard for this secondary data
            })
            .finally(() => {
              // Decrement pending requests when topics load finishes
              pendingRequestsRef.current = Math.max(0, pendingRequestsRef.current - 1);
              
              // Check if we should mark loading as complete
              if (pendingRequestsRef.current === 0) {
                console.debug('All analytics requests complete - marking loading as done');
                loadingRef.current = false;
                // Reset request counter on success of ALL requests
                requestCountRef.current = 0;
              }
            });
        }
      } catch (error) {
        console.error("Error loading summary data:", error);
        pendingRequestsRef.current--;
        throw error; // Propagate for the outer catch
      }
      
      // Check if all requests completed synchronously (unlikely but possible)
      if (pendingRequestsRef.current === 0) {
        const totalElapsed = Date.now() - fullStartTime;
        console.debug(`All analytics requests completed synchronously in ${totalElapsed}ms`);
        loadingRef.current = false;
        requestCountRef.current = 0;
      }
      
    } catch (err) {
      console.error("Error loading dashboard data:", err);
      
      // Any error in the main request should decrement the pending count
      pendingRequestsRef.current = Math.max(0, pendingRequestsRef.current - 1);
      
      // Check if this is a timeout error
      const isTimeout = err && (
        (err instanceof Error && err.message.includes('timeout')) || 
        (typeof err === 'object' && err !== null && 'code' in err && err.code === 'ECONNABORTED')
      );
      
      if (isTimeout) {
        setLocalError(
          `Request timed out after 30 seconds. The analytics query might be too complex. ` +
          `Try a smaller date range or try again later when the server is less busy.`
        );
      } else {
        setLocalError(
          err instanceof Error 
            ? err.message 
            : 'An error occurred while loading analytics data. Please try again.'
        );
      }
      
      // Mark loading as complete if this was the last pending request
      if (pendingRequestsRef.current === 0) {
        loadingRef.current = false;
      }
    }
  }, [searchDateFrom, searchDateTo, getSummaryMetrics, calculateDateRange, 
      getTopEntities, getTopicsAnalysis]);

  // Initialize date range on component mount
  useEffect(() => {
    console.debug("Analytics dashboard mounted - initializing date range");
    const today = new Date();
    const endDate = today.toISOString().slice(0, 10).replace(/-/g, ''); // YYYYMMDD
    const startDate = new Date(new Date().setDate(today.getDate() - 6)).toISOString().slice(0, 10).replace(/-/g, ''); // YYYYMMDD, 7 days ago
    
    // Only set dates if they haven't been set yet to prevent reload loops
    if (!searchDateFrom) {
      setSearchDateFrom(startDate);
      setTempDateFrom(startDate); // Initialize temp state as well
    }
    
    if (!searchDateTo) {
      setSearchDateTo(endDate);
      setTempDateTo(endDate); // Initialize temp state as well
    }
  }, []); // Run only on mount

  /**
   * Load data when applied date range changes
   */
  useEffect(() => {
    // Only proceed if we have applied dates and aren't already loading data
    if (searchDateFrom && searchDateTo && !loadingRef.current && !displayError) {
      // Skip reload if we've already successfully loaded data for this exact date range
      if (lastSuccessfulDateRange.current.from === searchDateFrom && 
          lastSuccessfulDateRange.current.to === searchDateTo) {
        console.debug(`Skipping reload - already have data for ${searchDateFrom} to ${searchDateTo}`);
        return;
      }
      
      // Store current date values for comparison 
      const currentFromDate = searchDateFrom;
      const currentToDate = searchDateTo;
      
      // Prevent excessive API calls - throttle to max 1 request every 5 seconds
      const now = Date.now();
      const timeSinceLastRequest = now - lastRequestTimeRef.current;
      
      if (timeSinceLastRequest < 5000 && requestCountRef.current > 0) {
        console.debug(`Throttling API request - last request was ${timeSinceLastRequest}ms ago`);
        return;
      }
      
      // Prevent infinite retry loops - max 2 consecutive requests with the same params
      if (requestCountRef.current >= 2) {
        console.warn('Too many consecutive requests - stopping to prevent infinite loop');
        setLocalError('Too many consecutive API requests. Please refresh the page or try again later.');
        // Explicitly reset loading state to recover from potential deadlocks
        loadingRef.current = false;
        pendingRequestsRef.current = 0;
        return;
      }
      
      // Only clear cached endpoint errors on manual refresh or first load, not on every date change
      // This prevents the loop of requesting endpoints that have already failed
      if (requestCountRef.current === 0) {
        clearAnalyticsEndpointErrors();
      }
      
      // Mark that we're loading data
      loadingRef.current = true;
      requestCountRef.current += 1;
      lastRequestTimeRef.current = now;
      
      console.debug(`Starting request cycle #${requestCountRef.current} at ${new Date().toISOString()}, dates: ${currentFromDate}-${currentToDate}`);
      
      // Wait briefly to ensure the cache clearing completes
      const timeoutId = setTimeout(() => {
        // Check if dates changed during timeout - if so, abort this cycle
        if (searchDateFrom !== currentFromDate || searchDateTo !== currentToDate) {
          console.debug('Date values changed during request preparation - aborting this cycle');
          loadingRef.current = false;
          requestCountRef.current = Math.max(0, requestCountRef.current - 1);
          return;
        }
        
        loadDashboardData()
          .catch((err) => {
            console.error('Dashboard data loading failed:', err);
            // Ensure loading state is reset even on errors
            loadingRef.current = false;
            pendingRequestsRef.current = 0;
          });
      }, 200); // Increased timeout for better stability
      
      // Cleanup function to cancel timeout and prevent stale requests
      return () => {
        clearTimeout(timeoutId);
      };
    }
  }, [searchDateFrom, searchDateTo, loadDashboardData, clearAnalyticsEndpointErrors, displayError]);

  // Add a safeguard effect to reset loading state after 30 seconds in case something gets stuck
  useEffect(() => {
    let timeoutId: NodeJS.Timeout;
    
    if (loadingRef.current) {
      timeoutId = setTimeout(() => {
        if (loadingRef.current) {
          console.warn('Loading state was stuck for 30 seconds, forcibly resetting');
          loadingRef.current = false;
          pendingRequestsRef.current = 0;
          setLocalError('Request timeout - try refreshing the page.');
        }
      }, 30000);
    }
    
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [/* No dependencies here to avoid infinite loops */]);

  // Helper function for quick date selections 
  // Sets both temp and applied dates to trigger reload
  const setDateRangeAndReload = useCallback((startDate: string, endDate: string) => {
    setTempDateFrom(startDate); // Update temp state for UI consistency
    setTempDateTo(endDate);     // Update temp state for UI consistency
    setSearchDateFrom(startDate); // Apply dates immediately
    setSearchDateTo(endDate);     // Apply dates immediately

    setLocalError(null); // Clear any previous errors
    requestCountRef.current = 0; // Reset retry counter for the new range
  
  }, []); // No dependencies needed as it only sets state

  // --- Date range quick select functions using the helper ---
  const handleUseToday = useCallback(() => {
    const today = new Date();
    const formattedToday = formatDate(today, 'YYYYMMDD');
    setDateRangeAndReload(formattedToday, formattedToday);
  }, [setDateRangeAndReload]);

  const handleLast7Days = useCallback(() => {
    const today = new Date();
    const last7Days = new Date();
    last7Days.setDate(today.getDate() - 6);
    const startDate = formatDate(last7Days, 'YYYYMMDD');
    const endDate = formatDate(today, 'YYYYMMDD');
    setDateRangeAndReload(startDate, endDate);
  }, [setDateRangeAndReload]);

  const handleLast30Days = useCallback(() => {
    const today = new Date();
    const last30Days = new Date();
    last30Days.setDate(today.getDate() - 29);
    const startDate = formatDate(last30Days, 'YYYYMMDD');
    const endDate = formatDate(today, 'YYYYMMDD');
    setDateRangeAndReload(startDate, endDate);
  }, [setDateRangeAndReload]);

  // Function to apply the temporary date range
  const handleApplyDateRange = useCallback(() => {
    // Validate that temp dates are set before applying
    if (tempDateFrom && tempDateTo) {
        console.debug(`Applying date range: ${tempDateFrom} to ${tempDateTo}`);
        setSearchDateFrom(tempDateFrom);
        setSearchDateTo(tempDateTo);
        setLocalError(null); // Clear errors on successful application
        requestCountRef.current = 0; // Reset retry counter
    } else {
        console.warn("Attempted to apply date range with null values.");
        // Optionally set an error or provide feedback
        setLocalError("Please select both a 'From' and 'To' date.");
    }
  }, [tempDateFrom, tempDateTo]); // Depends on temp dates

  const onClickBot = useCallback((botId: string) => {
    if (!botId) {
      return;
    }
    // Construct search parameters
    const searchParams = new URLSearchParams();
    if (searchDateFrom) {
      searchParams.set('startDate', searchDateFrom);
    }
    if (searchDateTo) {
      searchParams.set('endDate', searchDateTo);
    }
    // Navigate with search parameters
    navigate(`/analytics/bots/${botId}?${searchParams.toString()}`);
  }, [navigate, searchDateFrom, searchDateTo]); // Added dependencies


  // Determine if we're in a loading state
  const isLoading = loadingState.fastMetrics && loadingState.topEntities && loadingState.topics && !summaryData;

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center">
          <div className="text-xl font-bold">Usage Analytics</div>
          <Help
            direction={TooltipDirection.RIGHT}
            message={t('analytics.help.overview', 'Overview of the analytics dashboard.')}
          />
        </div>
        <div className="right-2 top-10 text-xs text-dark-gray dark:text-light-gray">
            {emailId}
        </div>
      </div>

      <div className="h-full flex-grow flex flex-col p-4">
        <div className="mb-4">
          <h1 className="text-xl font-bold mb-2">Analytics Summary</h1>
          
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-1">
                <span className="font-medium text-gray-700 dark:text-gray-300">Calculation Period</span>
                <Help 
                  direction={TooltipDirection.RIGHT} 
                  message={t('analytics.help.calculationPeriod', 'Select a date range to view analytics data for that period.')} 
                />
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={handleUseToday}
                  className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm rounded-md hover:bg-blue-200 transition-colors font-medium"
                  data-testid="today-button"
                >
                  Today
                </button>
                <button 
                  onClick={handleLast7Days}
                  className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm rounded-md hover:bg-blue-200 transition-colors font-medium"
                  data-testid="last-7-days-button"
                >
                  7 Days
                </button>
                <button 
                  onClick={handleLast30Days}
                  className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm rounded-md hover:bg-blue-200 transition-colors font-medium"
                  data-testid="last-30-days-button"
                >
                  30 Days
                </button>
                <button 
                  onClick={() => {
                    // Reset loading state and counters
                    loadingRef.current = false;
                    pendingRequestsRef.current = 0;
                    requestCountRef.current = 0;
                    
                    // Clear all analytics caches including endpoints and pending requests
                    clearAllAnalyticsCaches();
                    setLocalError(null);
                    
                    // Set a flag to indicate this is a manual reload
                    const manualReloadTime = Date.now();
                    lastRequestTimeRef.current = manualReloadTime;
                    
                    // Give time for the cache clearing to take effect
                    setTimeout(() => {
                      // Directly call loadDashboardData with force refresh
                      loadDashboardData(true);
                    }, 100);
                  }}
                  className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors font-medium"
                  data-testid="reset-cache-button"
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
                  // Value now comes from temp state
                  value={tempDateFrom ? formatDate(tempDateFrom, 'YYYY-MM-DD') : ''} 
                  onChange={(val) => {
                    if (val === '') {
                      setTempDateFrom(null); // Update temp state
                      return;
                    }
                    setTempDateFrom(formatDate(val, 'YYYYMMDD')); // Update temp state
                  }}
                  data-testid="date-from-input"
                />
              </div>
              <div className="w-full sm:w-1/2">
                <InputText
                  className="w-full"
                  type="date"
                  label="To"
                  // Value now comes from temp state
                  value={tempDateTo ? formatDate(tempDateTo, 'YYYY-MM-DD') : ''} 
                  onChange={(val) => {
                    if (val === '') {
                      setTempDateTo(null); // Update temp state
                      return;
                    }
                    setTempDateTo(formatDate(val, 'YYYYMMDD')); // Update temp state
                  }}
                  data-testid="date-to-input"
                />
              </div>
              {/* Apply button moved here */}
              <Button
                onClick={handleApplyDateRange}
                disabled={!tempDateFrom || !tempDateTo} // Disable if dates aren't selected
                className="px-3 py-1.5 h-[38px] text-sm font-medium mb-[1px]" // Adjust height/margin for alignment
                data-testid="apply-dates-button"
              >
                Apply
              </Button>
            </div>
          </div>
        </div>
        
        {dateRangeWarning && (
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
            <p className="text-yellow-700">
              {dateRangeWarning}
            </p>
          </div>
        )}

        {/* Progressive loading status indicators */}
        {Object.values(loadingState).some(Boolean) && (
          <div className="flex gap-2 mb-4" aria-live="polite">
            {loadingState.fastMetrics && (
              <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full animate-pulse">
                Loading metrics...
              </span>
            )}
            {loadingState.topEntities && (
              <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full animate-pulse">
                Loading top users & bots...
              </span>
            )}
            {loadingState.topics && (
              <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full animate-pulse">
                Loading topic analysis...
              </span>
            )}
          </div>
        )}

        {/* Error display */}
        {displayError && (
          <div className="mb-4 p-4 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded" role="alert">
            <h3 className="font-bold text-lg mb-2">Error Loading Analytics</h3>
            <p>{displayError}</p>
            <div className="mt-3 flex flex-wrap gap-2">
              <button 
                // Retry should use the currently *applied* dates
                onClick={() => loadDashboardData()} 
                className="px-3 h-[38px] bg-blue-100 text-blue-700 text-sm rounded hover:bg-blue-200 transition-colors border border-blue-200"
              >
                Retry
              </button>
              <button 
                onClick={handleUseToday} 
                className="px-3 h-[38px] bg-blue-100 text-blue-700 text-sm rounded hover:bg-blue-200 transition-colors border border-blue-200"
              >
                Today
              </button>
              <button 
                onClick={handleLast7Days} 
                className="px-3 h-[38px] bg-blue-100 text-blue-700 text-sm rounded hover:bg-blue-200 transition-colors border border-blue-200"
              >
                7 Days
              </button>
            </div>
          </div>
        )}


        {/* Main dashboard content with proper loading states */}
        {isLoading ? (
          <div className="space-y-4" aria-busy="true" aria-label="Loading dashboard data">
            <Skeleton className="h-32 w-full" />
            <Skeleton className="h-64 w-full" />
            <Skeleton className="h-64 w-full" />
          </div>
        ) : summaryData ? (
          <div className="space-y-6">
            {/* Display no data message if the daily_usage array is empty */}
            {!isLoading &&
             (!summaryData.daily_usage || summaryData.daily_usage.length === 0) &&
             (
               <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg text-center">
                 <h3 className="text-lg font-semibold mb-2">No Analytics Data Available</h3>
                 <p>There is no conversation activity recorded for this time period.</p>
                 <p className="text-sm mt-2">The system found {summaryData.summary?.total_users || 0} users but no messages or sessions.</p>
                 <div className="mt-4 flex justify-center gap-2">
                   <button 
                     onClick={handleLast7Days} 
                     className="px-3 py-1 bg-blue-100 dark:bg-blue-800 rounded hover:bg-blue-300 dark:hover:bg-blue-700"
                   >
                     Try Last 7 Days
                   </button>
                   <button 
                     onClick={handleLast30Days} 
                     className="px-3 py-1 bg-blue-100 dark:bg-blue-800 rounded hover:bg-blue-300 dark:hover:bg-blue-700"
                   >
                     Try Last 30 Days
                   </button>
                 </div>
               </div>
             )}
            
            {/* Only render charts and stats if we have chart data OR summary data */}
            {(chartData.length > 0 || summaryStats) && (
              <>
                {/* Summary stats cards */}
                {summaryStats && <SummaryStats stats={summaryStats} />}

                {/* Chart Grid Layout */}
                {chartData.length > 0 && (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
                      <UsageTrendChart 
                        data={chartData} 
                        title="Daily Sessions"
                        dataKey="num_sessions"
                        yAxisLabel="Sessions"
                      />
                    </div>
                    
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
                      <UsageTrendChart 
                        data={chartData} 
                        title="Daily Messages"
                        dataKey="num_messages"
                        yAxisLabel="Messages"
                      />
                    </div>
                    
                    {summaryStats?.total_cost !== null && (
                      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
                        <UsageTrendChart 
                          data={chartData} 
                          title="Daily Cost"
                          dataKey="cost"
                          yAxisLabel="Cost ($)"
                          color="#82ca9d"
                        />
                      </div>
                    )}
                    
                    {summaryStats?.total_input_tokens !== null && summaryStats?.total_output_tokens !== null && (
                      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
                        <TokenCountsChart 
                          data={chartData} 
                          title="Token Usage" 
                        />
                      </div>
                    )}
                  </div>
                )}

                {/* Top entities section - conditionally rendered */}
                {(chartData.length > 0 || (summaryData.daily_usage && summaryData.daily_usage.length > 0)) && (
                  <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                    {/* Top Users Table - Use specific loading state */}
                    {loadingState.topEntities ? (
                      <Skeleton className="h-48 w-full rounded-lg" />
                    ) : topEntities?.top_users && topEntities.top_users.length > 0 ? (
                      <TopUsersTable 
                        users={topEntities.top_users || []} 
                        title="Top Users" 
                      />
                    ) : (
                      <div className="space-y-4 bg-white dark:bg-gray-800 rounded-lg shadow p-4">
                        <h3 className="text-lg font-semibold">Top Users</h3>
                        <p className="text-center text-gray-500">No user data available for this period.</p>
                      </div>
                    )}
                    
                    {/* Top bots table - Use specific loading state */}
                    {loadingState.topEntities ? (
                       <Skeleton className="h-48 w-full rounded-lg" />
                    ) : topEntities?.top_bots && topEntities.top_bots.length > 0 ? (
                      <div className="space-y-4 bg-white dark:bg-gray-800 rounded-lg shadow p-4">
                        <h3 className="text-lg font-semibold">Top Assistants</h3>
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                            <thead>
                              <tr>
                                <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                  Name
                                </th>
                                <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                  Users
                                </th>
                                <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                  Sessions
                                </th>
                                {topEntities.top_bots?.some(bot => bot.total_price !== null) && (
                                <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                  Conversation Cost
                                </th>
                                )}
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                              {topEntities?.top_bots?.map((bot: any, index: number) => (
                                <tr 
                                  key={`bot-${bot.id}-${index}`}
                                  className="hover:bg-blue-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                                  onClick={() => onClickBot(bot.id)}
                                >
                                  <td className="px-3 py-2 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100">
                                    {bot.title.includes('Bot metadata not available') ? bot.id : bot.title || 'Unnamed Bot'}
                                  </td>
                                  <td className="px-3 py-2 text-right text-sm text-gray-500 dark:text-gray-400">
                                    {bot.num_of_users || 0}
                                  </td>
                                  <td className="px-3 py-2 text-right text-sm text-gray-500 dark:text-gray-400">
                                    {bot.num_of_convos || 0}
                                  </td>
                                  {topEntities.top_bots?.some(bot => bot.total_price !== null) && (
                                  <td className="px-3 py-2 text-right text-sm text-gray-500 dark:text-gray-400">
                                    {bot.total_price !== null ? `$${(bot.total_price || 0).toFixed(3)}` : 'N/A'}
                                  </td>
                                  )}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    ) : (
                       // Optional: Add a 'No bot data' message if needed when not loading and no data
                       <div className="space-y-4 bg-white dark:bg-gray-800 rounded-lg shadow p-4">
                        <h3 className="text-lg font-semibold">Top Assistants</h3>
                        <p className="text-center text-gray-500">No assistant data available for this period.</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Topic analysis section - only shown if data is available */}
                {(chartData.length > 0 || (summaryData.daily_usage && summaryData.daily_usage.length > 0)) && 
                  topicsData?.topics && topicsData.topics.length > 0 && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Top Topics</h3>
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
                      <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                          <thead>
                            <tr>
                              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Topic
                              </th>
                              <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Messages
                              </th>
                              <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                Percentage
                              </th>
                            </tr>
                          </thead>
                          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                            {topicsData.topics.map((topic, index) => (
                              <tr key={`topic-${index}`}>
                                <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                  {topic.topic}
                                </td>
                                <td className="px-3 py-2 whitespace-nowrap text-sm text-right text-gray-500 dark:text-gray-400">
                                  {topic.message_count}
                                </td>
                                <td className="px-3 py-2 whitespace-nowrap text-right">
                                  <div className="flex items-center justify-end">
                                    <span className="text-sm text-gray-500 dark:text-gray-400 mr-2">
                                      {topicsData && topicsData.total_count ? Math.round((topic.message_count / topicsData.total_count) * 100) : 0}%
                                    </span>
                                    <div className="w-24 bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                                      <div 
                                        className="bg-blue-600 h-2.5 rounded-full" 
                                        style={{ width: `${topicsData && topicsData.total_count ? Math.round((topic.message_count / topicsData.total_count) * 100) : 0}%` }}
                                      ></div>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        ) : (
          !loadingState.fastMetrics && !loadingState.topEntities && !loadingState.topics && !displayError && ( 
            // No data loaded yet or error state
            <div className="text-center p-8">
              <p>No data available. Please select a date range and try again.</p>
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default QikrAnalyticsDashboard; 