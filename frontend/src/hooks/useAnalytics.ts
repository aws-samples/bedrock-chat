import { useCallback, useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import useHttp from './useHttp';

export interface DailyUsage {
  date: string;
  num_sessions: number;
  num_messages: number;
  input_tokens: number;
  output_tokens: number;
  cost: number | null;
}

export interface UsagePerUser {
  id: string;
  email: string;
  num_sessions: number;
  num_messages: number;
  total_price: number | null;
}

export interface TopicAnalysis {
  topic: string;
  message_count: number;
  percentage: number;
}

export interface BotAnalytics {
  bot_id: string;
  title: string;
  description: string;
  owner_user_id: string;
  total_users: number;
  total_sessions: number;
  total_messages: number;
  total_input_tokens: number;
  total_output_tokens: number;
  total_cost: number;
  daily_usage: DailyUsage[];
  top_users: UsagePerUser[];
  top_topics: TopicAnalysis[];
}

export interface AnalyticsSummary {
  num_sessions: number;
  num_messages: number;
  input_tokens: number | null;
  output_tokens: number | null;
  cost: number | null;
  total_bots: number | null;
  total_users: number | null;
}

export interface TopEntitiesData {
  top_bots: UsagePerBotOutput[];
  top_users: UsagePerUser[];
}

export interface TopicsData {
  topics: TopicAnalysis[];
  total_count: number;
}

export interface UsagePerBotOutput {
  id: string;
  title: string | null;
  description: string | null;
  owner_user_id: string | null;
  total_price: number | null;
  num_of_users: number | null;
  num_of_convos: number | null;
  group_id: string | null;
  message_count: number | null;
}

export interface SummaryAnalyticsData {
  summary: AnalyticsSummary;
  daily_usage: DailyUsage[];
}

// Define the keys patterns/names used in sessionStorage
const ANALYTICS_CACHE_PREFIX = 'analytics_cache_';
const ANALYTICS_ENDPOINT_PREFIX = 'analytics_endpoint_';
const PENDING_REQUESTS_KEY = 'pending_analytics_requests';

// Standalone function to clear all analytics-related sessionStorage items
export const clearAllAnalyticsSessionCache = () => {
  try {
    const keysToRemove: string[] = [];
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i);
      if (key && (
        key.startsWith(ANALYTICS_CACHE_PREFIX) ||
        key.startsWith(ANALYTICS_ENDPOINT_PREFIX) ||
        key === PENDING_REQUESTS_KEY
      )) {
        keysToRemove.push(key);
      }
    }

    keysToRemove.forEach(key => {
      try {
        sessionStorage.removeItem(key);
      } catch (e) {
         console.warn(`Failed to remove sessionStorage key ${key}:`, e);
      }
    });

    console.debug(`Cleared ${keysToRemove.length} cached analytics items from sessionStorage`);
  } catch (e) {
    console.error('Error clearing analytics sessionStorage:', e);
  }
};

// Standalone function to clear only endpoint error flags
export const clearAnalyticsEndpointErrorCache = () => {
  try {
    const keysToRemove: string[] = [];
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i);
      if (key && key.startsWith(ANALYTICS_ENDPOINT_PREFIX)) {
        keysToRemove.push(key);
      }
    }
    keysToRemove.forEach(key => {
      try {
        sessionStorage.removeItem(key);
      } catch (e) {
         console.warn(`Failed to remove endpoint error cache key ${key}:`, e);
      }
    });
    console.debug(`Cleared ${keysToRemove.length} cached analytics endpoint errors`);
  } catch (e) {
    console.error('Error clearing analytics endpoint error cache:', e);
  }
};

export interface CachedAnalyticsItem<T> {
  data: T;
  timestamp: number;
  cachedUserId: string | null;
}

export const useAnalytics = (currentUserId: string | null) => {
  console.log('[useAnalytics] Hook initialized with userId:', currentUserId);
  useTranslation();
  const http = useHttp();
  const [error, setError] = useState<string | null>(null);
  
  // Loading state for specific API calls
  const [loadingState, setLoadingState] = useState({
    fastMetrics: false,
    topEntities: false,
    topics: false,
    botAnalytics: false,
  });

  // Use the standalone function internally now
  const clearAnalyticsEndpointErrors = useCallback(() => {
    clearAnalyticsEndpointErrorCache(); // Call the exported function
    // Reset error state to ensure a clean start
    setError(null);
  }, []);

  // Clear endpoint errors on mount (initial behaviour)
  useEffect(() => {
    clearAnalyticsEndpointErrors();
  }, [clearAnalyticsEndpointErrors]);

  // Calculate the number of days between two dates in YYYYMMDD format
  const calculateDateRangeSize = useCallback((start?: string, end?: string): number => {
    if (!start || !end) {
      return 1;
    }
    
    try {
      const startDate = new Date(
        parseInt(start.substring(0, 4)), 
        parseInt(start.substring(4, 6)) - 1, 
        parseInt(start.substring(6, 8))
      );
      
      const endDate = new Date(
        parseInt(end.substring(0, 4)), 
        parseInt(end.substring(4, 6)) - 1, 
        parseInt(end.substring(6, 8))
      );
      
      const diffTime = Math.abs(endDate.getTime() - startDate.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; // +1 to include both start and end dates
      return diffDays;
    } catch (err) {
      console.error("Error calculating date range size:", err);
      return 30;
    }
  }, []);

  const handleError = useCallback((err: any, endpoint: string, timeoutMs?: number, fromDate?: string, toDate?: string) => {
    console.error(`Error fetching analytics from ${endpoint}:`, err);
    const cacheKey = `analytics_cache_${endpoint}`;
    try {
      sessionStorage.removeItem(cacheKey); // Remove potentially bad cache entry on error
      console.warn(`Removed potentially bad cache entry: ${cacheKey}`);
    } catch (e) {
      console.warn("Failed to remove cache entry on error:", e);
    }

    if (err.response && err.response.status === 404) {
      setError(`API endpoint not found (${endpoint}). This feature may require an update or configuration.`);
      try {
         sessionStorage.setItem(`analytics_endpoint_${endpoint}`, 'not_found');
      } catch(e) { console.error("Failed to set session storage for 404", e); }
    } else if (err.response && err.response.status === 504) {
      const dateRangeSize = calculateDateRangeSize(fromDate, toDate);
      const suggestion = dateRangeSize > 7
        ? `Try using a smaller date range (current range: ${dateRangeSize} days).`
        : "Server may be under heavy load or the query is complex. Please try again later.";
      setError(`Request timed out (504). ${suggestion}`);
    } else if (err.code === 'ECONNABORTED' || (err.message && err.message.toLowerCase().includes('timeout'))) {
      const dateRangeSize = calculateDateRangeSize(fromDate, toDate);
      const suggestion = dateRangeSize > 7
        ? `Try using a smaller date range (current range: ${dateRangeSize} days).`
        : "Server may be under heavy load. Please try again later.";
      setError(`Request timed out after ${timeoutMs || 'default'}ms. ${suggestion} You may need to retry the request.`);
    } else if (err.request) {
      setError('No response received from server. Check connection.');
    } else {
      const detail = err.response?.data?.detail;
      setError(detail || err.message || 'An unknown error occurred fetching analytics data.');
    }
  }, [calculateDateRangeSize]);

  // Helper function to generate cache key
  const getCacheKey = (baseEndpoint: string, params: URLSearchParams) => {
    // Sort params for consistent key generation
    params.sort();
    return `analytics_cache_${baseEndpoint}?${params.toString()}`;
  };

  // Helper function for cache checking and force refresh logic
  // Now expects cached items to have { data: T, timestamp: number } structure
  const checkOrRetrieveCache = useCallback(<T,>(cacheKey: string, forceRefresh: boolean): T | null => {
    const MAX_CACHE_AGE_MS = 30 * 60 * 1000; // 30 minutes

    // Log the ID being used for the check
    console.log('[useAnalytics] checkOrRetrieveCache - Checking with currentUserId:', currentUserId);

    if (forceRefresh) {
      try {
        console.debug(`Force refresh: Clearing cache for ${cacheKey}`);
        sessionStorage.removeItem(cacheKey);
      } catch (e) {
        console.warn("Failed to remove cache entry during force refresh:", e);
      }
      return null; // Bypass cache
    } else {
      try {
        const cachedItem = sessionStorage.getItem(cacheKey);
        if (cachedItem) {
          try {
            const parsedItem = JSON.parse(cachedItem) as CachedAnalyticsItem<T>;
            
            // Validate cached structure and timestamp
            if (parsedItem && typeof parsedItem === 'object' && 'data' in parsedItem && 'timestamp' in parsedItem && typeof parsedItem.timestamp === 'number') {

              // ---> USER ID CHECK using hook's currentUserId <---
              let userIdMatch = false; // Flag to track if user check passes
              if (currentUserId && parsedItem.cachedUserId === currentUserId) {
                userIdMatch = true; // IDs match
              } else if (!currentUserId && !parsedItem.cachedUserId) {
                userIdMatch = true; // Both null/undefined, treat as match (e.g., logged out state)
              } else {
                // Mismatch or one is null/undefined
                if (currentUserId) {
                    console.log(`[useAnalytics] CACHE USER MISMATCH DETECTED for key ${cacheKey}`);
                    console.debug(`   Cached User: ${parsedItem.cachedUserId ?? 'N/A'}, Current User: ${currentUserId}`);
                } else {
                    console.log(`[useAnalytics] CACHE INVALID: Current user unknown, but cache has user ${parsedItem.cachedUserId}`);
                }
                // remove this specific stale item now:
                try { sessionStorage.removeItem(cacheKey); } catch (removeError) { console.warn('Failed to remove stale cache item:', removeError); }
                // Don't return null yet, just mark as mismatch
              }
              // ---> End User ID Check <---

              // ---> Proceed ONLY if user ID check passed <-----
              if (userIdMatch) {
                  const cacheAge = Date.now() - parsedItem.timestamp;
                  if (cacheAge < MAX_CACHE_AGE_MS) {
                    // console.debug(`Returning valid cached data for user ${currentUserId ?? 'UNKNOWN'} (age: ${Math.round(cacheAge / 1000)}s) for key ${cacheKey}`);
                    // Basic check for non-empty data object
                    if (parsedItem.data && typeof parsedItem.data === 'object' && Object.keys(parsedItem.data).length > 0) {
                       return parsedItem.data;
                    } else if (parsedItem.data) { // Allow non-object data (e.g., arrays)
                       return parsedItem.data;
                    } else {
                       console.warn(`Cached data for ${cacheKey} is empty.`);
                       return null;
                    }
                  } else {
                    console.debug(`Cache expired (age: ${Math.round(cacheAge / 1000)}s) for key ${cacheKey}.`);
                    // Let expired data be overwritten or cleared on logout
                    return null;
                  }
              } else {
                  // User ID check failed, definitely return null
                  return null;
              }
              // ---> End conditional timestamp check <-----

            } else {
               console.warn(`Invalid cache structure found for ${cacheKey}`);
               try { sessionStorage.removeItem(cacheKey); } catch (removeError) { console.warn(`Failed to remove corrupted cache for ${cacheKey}:`, removeError); }
               return null;
            }
            
          } catch (parseError) {
            console.warn(`Failed to parse cached data for ${cacheKey}:`, parseError);
            // Clear potentially corrupted cache entry
            try { sessionStorage.removeItem(cacheKey); } catch (removeError) {
              console.warn(`Failed to remove corrupted cache for ${cacheKey}:`, removeError);
            }
            return null; // Treat parse error as cache miss
          }
        }
      } catch (e) {
        console.warn(`Failed to read session cache for ${cacheKey}:`, e);
      }
      return null; // Cache miss or error reading cache
    }
  }, [currentUserId]);

  const getSummaryMetrics = useCallback(async (fromDate?: string, toDate?: string, timeoutMs: number = 60000, forceRefresh: boolean = false): Promise<SummaryAnalyticsData | null> => {
    const params = new URLSearchParams();
    if (fromDate) {
      params.append('from_date', fromDate);
    }
    if (toDate) {
      params.append('to_date', toDate);
    }
    const baseEndpoint = '/analytics/dashboard/summary';
    const endpoint = `${baseEndpoint}?${params.toString()}`;
    const cacheKey = getCacheKey(baseEndpoint, params);
    
    // Debug logging for duplicate request tracking
    console.debug(`getSummaryMetrics called with params: ${params.toString()}, forceRefresh: ${forceRefresh}`);

    // Clear cache if forcing a refresh
    if (forceRefresh) {
      try {
        console.debug(`Force refresh: Clearing cache for ${cacheKey}`);
        sessionStorage.removeItem(cacheKey);
      } catch (e) {
        console.warn("Failed to remove cache entry during force refresh:", e);
      }
    }

    // Check 404 cache first (even with force refresh to avoid hammering endpoints)
    if (sessionStorage.getItem(`analytics_endpoint_${endpoint}`) === 'not_found') {
      console.warn(`Skipping request to known missing endpoint: ${endpoint}`);
      setError(`API endpoint not found. Summary data unavailable.`);
      return null;
    }

    // Use helper for cache logic if not forcing refresh
    let cachedResult = null;
    if (!forceRefresh) {
      try {
        cachedResult = checkOrRetrieveCache<SummaryAnalyticsData>(cacheKey, false);
        if (cachedResult !== null) {
          return cachedResult;
        }
      } catch (err) {
        console.warn("Cache read error:", err);
        // Continue with API call if cache fails
      }
    }

    // Proceed with API call
    setLoadingState(prev => ({ ...prev, fastMetrics: true }));
    setError(null);
    
    // Add abort controller for timeout handling
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, timeoutMs);
    
    // Track multiple in-flight requests with the same parameters
    const requestId = `${baseEndpoint}:${params.toString()}:${Date.now()}`;
    const pendingRequestsKey = `pending_analytics_requests`;
    
    try {
      // Store this request as pending to detect duplicates
      let pendingRequests: Record<string, number> = {};
      try {
        const storedRequests = sessionStorage.getItem(pendingRequestsKey);
        const now = Date.now();
        if (storedRequests) {
          pendingRequests = JSON.parse(storedRequests);
          // Clean up old pending requests (older than 10 seconds)
          Object.keys(pendingRequests).forEach(key => {
            if (now - pendingRequests[key] > 10000) {
              delete pendingRequests[key];
            }
          });
        }
        
        // Check if we have a very recent identical request
        const baseRequestKey = `${baseEndpoint}:${params.toString()}`;
        const matchingRequests = Object.keys(pendingRequests).filter(
          key => key.startsWith(baseRequestKey) && now - pendingRequests[key] < 2000
        );
        
        // Only cancel if this is not a forced refresh request
        if (matchingRequests.length > 0 && !forceRefresh) {
          console.warn(`Duplicate request detected for ${baseEndpoint}. Cancelling this one.`);
          controller.abort();
          return null;
        }
        
        // Add this request to pending regardless of whether it's a forced refresh
        pendingRequests[requestId] = Date.now();
        sessionStorage.setItem(pendingRequestsKey, JSON.stringify(pendingRequests));
      } catch (e) {
        console.warn("Failed to update pending requests tracking:", e);
      }
      
      // Check if already aborted to avoid unnecessary API call
      if (controller.signal.aborted) {
        console.debug("Request already aborted before sending");
        return null;
      }
      
      const startTime = Date.now();
      const response = await http.getOnce<SummaryAnalyticsData>(endpoint, { 
        timeout: timeoutMs,
        signal: controller.signal
      });
      console.debug(`Summary metrics received in ${Date.now() - startTime}ms`);
      
      // Store successful response in cache
      try {
        const itemToCache = {
          data: response.data,
          timestamp: Date.now(),
          cachedUserId: currentUserId
        };
        sessionStorage.setItem(cacheKey, JSON.stringify(itemToCache));
      } catch (e) {
        console.warn("Failed to write to session cache:", e);
      }
      return response.data;
    } catch (err: any) {
      // Don't show errors for intentionally aborted requests
      if (err.name === 'AbortError' || controller.signal.aborted) {
        console.debug("Request was aborted");
        return null;
      }
      handleError(err, endpoint, timeoutMs, fromDate, toDate);
      return null;
    } finally {
      clearTimeout(timeoutId);
      setLoadingState(prev => ({ ...prev, fastMetrics: false }));
      
      // Remove this request from pending
      try {
        const storedRequests = sessionStorage.getItem(pendingRequestsKey);
        if (storedRequests) {
          const pendingRequests = JSON.parse(storedRequests);
          delete pendingRequests[requestId];
          sessionStorage.setItem(pendingRequestsKey, JSON.stringify(pendingRequests));
        }
      } catch (e) {
        console.warn("Failed to clean up pending request tracking:", e);
      }
    }
  }, [http, handleError, checkOrRetrieveCache, currentUserId]);

  const getTopEntities = useCallback(async (fromDate?: string, toDate?: string, limit: number = 10, timeoutMs: number = 60000, forceRefresh: boolean = false): Promise<TopEntitiesData | null> => {
    const params = new URLSearchParams();
    if (fromDate) {
      params.append('from_date', fromDate);
    }
    if (toDate) {
      params.append('to_date', toDate);
    }
    params.append('limit', limit.toString());
    const baseEndpoint = '/analytics/dashboard/top-entities';
    const endpoint = `${baseEndpoint}?${params.toString()}`;
    const cacheKey = getCacheKey(baseEndpoint, params);
    
    // Debug logging for duplicate request tracking
    console.debug(`getTopEntities called with params: ${params.toString()}, forceRefresh: ${forceRefresh}`);

    // Clear cache if forcing a refresh
    if (forceRefresh) {
      try {
        console.debug(`Force refresh: Clearing cache for ${cacheKey}`);
        sessionStorage.removeItem(cacheKey);
      } catch (e) {
        console.warn("Failed to remove cache entry during force refresh:", e);
      }
    }

    // Check 404 cache first (even with force refresh to avoid hammering endpoints)
    if (sessionStorage.getItem(`analytics_endpoint_${endpoint}`) === 'not_found') {
      console.warn(`Skipping request to known missing endpoint: ${endpoint}`);
      setError(`API endpoint not found. Top entities data unavailable.`);
      return null;
    }

    // Use helper for cache logic if not forcing refresh
    let cachedResult = null;
    if (!forceRefresh) {
      try {
        cachedResult = checkOrRetrieveCache<TopEntitiesData>(cacheKey, false);
        if (cachedResult !== null) {
          return cachedResult;
        }
      } catch (err) {
        console.warn("Cache read error:", err);
        // Continue with API call if cache fails
      }
    }

    // Proceed with API call
    setLoadingState(prev => ({ ...prev, topEntities: true }));
    setError(null);
    
    // Add abort controller for timeout handling
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, timeoutMs);
    
    // Track multiple in-flight requests with the same parameters
    const requestId = `${baseEndpoint}:${params.toString()}:${Date.now()}`;
    const pendingRequestsKey = `pending_analytics_requests`;
    
    try {
      // Store this request as pending to detect duplicates
      let pendingRequests: Record<string, number> = {};
      try {
        const storedRequests = sessionStorage.getItem(pendingRequestsKey);
        const now = Date.now();
        if (storedRequests) {
          pendingRequests = JSON.parse(storedRequests);
          // Clean up old pending requests (older than 10 seconds)
          Object.keys(pendingRequests).forEach(key => {
            if (now - pendingRequests[key] > 10000) {
              delete pendingRequests[key];
            }
          });
        }
        
        // Check if we have a very recent identical request
        const baseRequestKey = `${baseEndpoint}:${params.toString()}`;
        const matchingRequests = Object.keys(pendingRequests).filter(
          key => key.startsWith(baseRequestKey) && now - pendingRequests[key] < 2000
        );
        
        // Only cancel if this is not a forced refresh request
        if (matchingRequests.length > 0 && !forceRefresh) {
          console.warn(`Duplicate request detected for ${baseEndpoint}. Cancelling this one.`);
          controller.abort();
          return null;
        }
        
        // Add this request to pending regardless of whether it's a forced refresh
        pendingRequests[requestId] = Date.now();
        sessionStorage.setItem(pendingRequestsKey, JSON.stringify(pendingRequests));
      } catch (e) {
        console.warn("Failed to update pending requests tracking:", e);
      }
      
      // Check if already aborted to avoid unnecessary API call
      if (controller.signal.aborted) {
        console.debug("Request already aborted before sending");
        return null;
      }
      
      const startTime = Date.now();
      const response = await http.getOnce<TopEntitiesData>(endpoint, { 
        timeout: timeoutMs,
        signal: controller.signal
      });
      const elapsed = Date.now() - startTime;
      console.debug(`Raw response for top-entities received in ${elapsed}ms:`, response);
      // Check if data exists and log it
      if (response && response.data) {
          console.debug('Top entities data received:', JSON.stringify(response.data).substring(0, 500) + '...'); // Log first 500 chars
      } else {
          console.warn('No data property found in top-entities response or response is null/undefined.');
      }
      
      // Store successful response in cache
      try {
        const itemToCache = {
          data: response.data,
          timestamp: Date.now(),
          cachedUserId: currentUserId
        };
        sessionStorage.setItem(cacheKey, JSON.stringify(itemToCache));
      } catch (e) {
        console.warn("Failed to write to session cache:", e);
      }
      return response.data;
    } catch (err: any) {
      // Don't show errors for intentionally aborted requests
      if (err.name === 'AbortError' || controller.signal.aborted) {
        console.debug("Request was aborted");
        return null;
      }
      handleError(err, endpoint, timeoutMs, fromDate, toDate);
      return null;
    } finally {
      clearTimeout(timeoutId);
      setLoadingState(prev => ({ ...prev, topEntities: false }));
      
      // Remove this request from pending
      try {
        const storedRequests = sessionStorage.getItem(pendingRequestsKey);
        if (storedRequests) {
          const pendingRequests = JSON.parse(storedRequests);
          delete pendingRequests[requestId];
          sessionStorage.setItem(pendingRequestsKey, JSON.stringify(pendingRequests));
        }
      } catch (e) {
        console.warn("Failed to clean up pending request tracking:", e);
      }
    }
  }, [http, handleError, checkOrRetrieveCache, currentUserId]);

  const getTopicsAnalysis = useCallback(async (fromDate?: string, toDate?: string, limit: number = 20, timeoutMs: number = 60000, forceRefresh: boolean = false): Promise<TopicsData | null> => {
    const params = new URLSearchParams();
    if (fromDate) {
      params.append('from_date', fromDate);
    }
    if (toDate) {
      params.append('to_date', toDate);
    }
    params.append('limit', limit.toString());
    const baseEndpoint = '/analytics/dashboard/topics';
    const endpoint = `${baseEndpoint}?${params.toString()}`;
    const cacheKey = getCacheKey(baseEndpoint, params);
    
    // Debug logging for duplicate request tracking
    console.debug(`getTopicsAnalysis called with params: ${params.toString()}, forceRefresh: ${forceRefresh}`);

    // Clear cache if forcing a refresh
    if (forceRefresh) {
      try {
        console.debug(`Force refresh: Clearing cache for ${cacheKey}`);
        sessionStorage.removeItem(cacheKey);
      } catch (e) {
        console.warn("Failed to remove cache entry during force refresh:", e);
      }
    }

    // Check 404 cache first (even with force refresh to avoid hammering endpoints)
    if (sessionStorage.getItem(`analytics_endpoint_${endpoint}`) === 'not_found') {
      console.warn(`Skipping request to known missing endpoint: ${endpoint}`);
      setError(`API endpoint not found. Topics data unavailable.`);
      return null;
    }

    // Use helper for cache logic if not forcing refresh
    let cachedResult = null;
    if (!forceRefresh) {
      try {
        cachedResult = checkOrRetrieveCache<TopicsData>(cacheKey, false);
        if (cachedResult !== null) {
          return cachedResult;
        }
      } catch (err) {
        console.warn("Cache read error:", err);
        // Continue with API call if cache fails
      }
    }

    // Proceed with API call
    setLoadingState(prev => ({ ...prev, topics: true }));
    setError(null);
    
    // Add abort controller for timeout handling
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, timeoutMs);
    
    // Track multiple in-flight requests with the same parameters
    const requestId = `${baseEndpoint}:${params.toString()}:${Date.now()}`;
    const pendingRequestsKey = `pending_analytics_requests`;
    
    try {
      // Store this request as pending to detect duplicates
      let pendingRequests: Record<string, number> = {};
      try {
        const storedRequests = sessionStorage.getItem(pendingRequestsKey);
        const now = Date.now();
        if (storedRequests) {
          pendingRequests = JSON.parse(storedRequests);
          // Clean up old pending requests (older than 10 seconds)
          Object.keys(pendingRequests).forEach(key => {
            if (now - pendingRequests[key] > 10000) {
              delete pendingRequests[key];
            }
          });
        }
        
        // Check if we have a very recent identical request
        const baseRequestKey = `${baseEndpoint}:${params.toString()}`;
        const matchingRequests = Object.keys(pendingRequests).filter(
          key => key.startsWith(baseRequestKey) && now - pendingRequests[key] < 2000
        );
        
        // Only cancel if this is not a forced refresh request
        if (matchingRequests.length > 0 && !forceRefresh) {
          console.warn(`Duplicate request detected for ${baseEndpoint}. Cancelling this one.`);
          controller.abort();
          return null;
        }
        
        // Add this request to pending regardless of whether it's a forced refresh
        pendingRequests[requestId] = Date.now();
        sessionStorage.setItem(pendingRequestsKey, JSON.stringify(pendingRequests));
      } catch (e) {
        console.warn("Failed to update pending requests tracking:", e);
      }
      
      // Check if already aborted to avoid unnecessary API call
      if (controller.signal.aborted) {
        console.debug("Request already aborted before sending");
        return null;
      }
      
      const startTime = Date.now();
      const response = await http.getOnce<TopicsData>(endpoint, { 
        timeout: timeoutMs,
        signal: controller.signal
      });
      console.debug(`Topics analysis received in ${Date.now() - startTime}ms`);
      // Store successful response in cache
      try {
        const itemToCache = {
          data: response.data,
          timestamp: Date.now(),
          cachedUserId: currentUserId
        };
        sessionStorage.setItem(cacheKey, JSON.stringify(itemToCache));
      } catch (e) {
        console.warn("Failed to write to session cache:", e);
      }
      return response.data;
    } catch (err: any) {
      // Don't show errors for intentionally aborted requests
      if (err.name === 'AbortError' || controller.signal.aborted) {
        console.debug("Request was aborted");
        return null;
      }
      handleError(err, endpoint, timeoutMs, fromDate, toDate);
      return null;
    } finally {
      clearTimeout(timeoutId);
      setLoadingState(prev => ({ ...prev, topics: false }));
      
      // Remove this request from pending
      try {
        const storedRequests = sessionStorage.getItem(pendingRequestsKey);
        if (storedRequests) {
          const pendingRequests = JSON.parse(storedRequests);
          delete pendingRequests[requestId];
          sessionStorage.setItem(pendingRequestsKey, JSON.stringify(pendingRequests));
        }
      } catch (e) {
        console.warn("Failed to clean up pending request tracking:", e);
      }
    }
  }, [http, handleError, checkOrRetrieveCache, currentUserId]);

  const getBotAnalytics = useCallback(async (botId: string, fromDate?: string, toDate?: string, timeoutMs: number = 60000, forceRefresh: boolean = false): Promise<BotAnalytics | null> => {
    if (!botId) {
      setError("Bot ID is required to fetch bot analytics.");
      return null;
    }

    const params = new URLSearchParams();
    if (fromDate) {
      params.append('from_date', fromDate);
    }
    if (toDate) {
      params.append('to_date', toDate);
    }
    const baseEndpoint = `/analytics/bot/${botId}`;
    const endpoint = `${baseEndpoint}?${params.toString()}`;
    const cacheKey = getCacheKey(baseEndpoint, params);
    
    // Debug logging for duplicate request tracking
    console.log(`getBotAnalytics called with params: botId=${botId}, from=${fromDate}, to=${toDate}, forceRefresh=${forceRefresh}`);

    // Clear cache if forcing a refresh
    if (forceRefresh) {
      try {
        console.debug(`Force refresh: Clearing cache for ${cacheKey}`);
        sessionStorage.removeItem(cacheKey);
      } catch (e) {
        console.warn("Failed to remove cache entry during force refresh:", e);
      }
    }

    // Check 404 cache first (even with force refresh to avoid hammering endpoints)
    if (sessionStorage.getItem(`analytics_endpoint_${endpoint}`) === 'not_found') {
      console.warn(`Skipping request to known missing endpoint: ${endpoint}`);
      setError(`API endpoint not found for bot ${botId}. Bot analytics unavailable.`);
      return null;
    }

    // Use helper for cache logic if not forcing refresh
    let cachedResult = null;
    if (!forceRefresh) {
      try {
        cachedResult = checkOrRetrieveCache<BotAnalytics>(cacheKey, false);
        if (cachedResult !== null) {
          return cachedResult;
        }
      } catch (err) {
        console.warn("Cache read error:", err);
        // Continue with API call if cache fails
      }
    }

    // Proceed with API call
    setLoadingState(prev => ({ ...prev, botAnalytics: true }));
    setError(null);
    
    // Add abort controller for timeout handling
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, timeoutMs);
    
    // Track multiple in-flight requests with the same parameters
    const requestId = `${baseEndpoint}:${params.toString()}:${Date.now()}`;
    const pendingRequestsKey = `pending_analytics_requests`;
    
    try {
      // Store this request as pending to detect duplicates
      let pendingRequests: Record<string, number> = {};
      try {
        const storedRequests = sessionStorage.getItem(pendingRequestsKey);
        const now = Date.now();
        if (storedRequests) {
          pendingRequests = JSON.parse(storedRequests);
          // Clean up old pending requests (older than 10 seconds)
          Object.keys(pendingRequests).forEach(key => {
            if (now - pendingRequests[key] > 10000) {
              delete pendingRequests[key];
            }
          });
        }
        
        // Check if we have a very recent identical request
        const baseRequestKey = `${baseEndpoint}:${params.toString()}`;
        const matchingRequests = Object.keys(pendingRequests).filter(
          key => key.startsWith(baseRequestKey) && now - pendingRequests[key] < 2000
        );
        
        if (matchingRequests.length > 0 && !forceRefresh) {
          console.warn(`Duplicate request detected for ${baseEndpoint}. Cancelling this one.`);
          controller.abort();
          return null;
        }
        
        // Add this request to pending
        pendingRequests[requestId] = Date.now();
        sessionStorage.setItem(pendingRequestsKey, JSON.stringify(pendingRequests));
      } catch (e) {
        console.warn("Failed to update pending requests tracking:", e);
      }
      
      // Check if already aborted to avoid unnecessary API call
      if (controller.signal.aborted) {
        console.debug("Request already aborted before sending");
        return null;
      }
      
      const startTime = Date.now();
      const response = await http.getOnce<BotAnalytics>(endpoint, { 
        timeout: timeoutMs,
        signal: controller.signal
      });
      console.debug(`Bot analytics for ${botId} received in ${Date.now() - startTime}ms`);
      // Store successful response in cache
      try {
        const itemToCache = {
          data: response.data,
          timestamp: Date.now(),
          cachedUserId: currentUserId
        };
        sessionStorage.setItem(cacheKey, JSON.stringify(itemToCache));
      } catch (e) {
        console.warn("Failed to write to session cache:", e);
      }
      return response.data;
    } catch (err: any) {
      // Don't show errors for intentionally aborted requests
      if (err.name === 'AbortError' || controller.signal.aborted) {
        console.debug("Request was aborted");
        return null;
      }
      handleError(err, endpoint, timeoutMs, fromDate, toDate);
      return null;
    } finally {
      clearTimeout(timeoutId);
      setLoadingState(prev => ({ ...prev, botAnalytics: false }));
      
      // Remove this request from pending
      try {
        const storedRequests = sessionStorage.getItem(pendingRequestsKey);
        if (storedRequests) {
          const pendingRequests = JSON.parse(storedRequests);
          delete pendingRequests[requestId];
          sessionStorage.setItem(pendingRequestsKey, JSON.stringify(pendingRequests));
        }
      } catch (e) {
        console.warn("Failed to clean up pending request tracking:", e);
      }
    }
  }, [http, handleError, checkOrRetrieveCache, currentUserId]);

  // Use the standalone function internally now
  const clearAllAnalyticsCaches = useCallback(() => {
    clearAllAnalyticsSessionCache(); // Call the exported function
     // Also reset local error state when clearing everything
    setError(null);
  }, []);

  return {
    loadingState,
    error,
    setError,
    clearAnalyticsEndpointErrors,
    clearAllAnalyticsCaches,
    getSummaryMetrics,
    getTopEntities,
    getTopicsAnalysis,
    getBotAnalytics,
  };
};