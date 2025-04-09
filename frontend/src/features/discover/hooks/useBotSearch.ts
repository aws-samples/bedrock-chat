import { useCallback, useState, useEffect } from 'react';
import { BotMeta } from '../../../@types/bot';
import useBotStoreApi from './useBotStoreApi';
import { useDebounce } from 'use-debounce';

const useBotSearch = () => {
  const { searchBots } = useBotStoreApi();
  const [searchQuery, setSearchQuery] = useState('');
  const [displayQuery, setDisplayQuery] = useState('');
  const [hasSearched, setHasSearched] = useState(false);
  const [debouncedQuery] = useDebounce(searchQuery, 300);

  // Fetch search results using SWR
  const {
    data: searchResults,
    isLoading: isSearching,
    mutate: mutateSearchResults,
  } = searchBots(hasSearched ? debouncedQuery : '');

  // Execute search when debouncedQuery changes
  useEffect(() => {
    if (debouncedQuery) {
      setHasSearched(true);
      // Update display query when search is executed
      setDisplayQuery(debouncedQuery);
      mutateSearchResults();
    } else if (debouncedQuery === '') {
      setHasSearched(false);
      setDisplayQuery('');
    }
  }, [debouncedQuery, mutateSearchResults]);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);

    if (!query.trim()) {
      setHasSearched(false);
      setDisplayQuery('');
    }
    // Actual search is executed in useEffect when debouncedQuery changes
  }, []);

  const clearSearch = useCallback(() => {
    setSearchQuery('');
    setDisplayQuery('');
    setHasSearched(false);
  }, []);

  // Utility function to update star status in search results
  const updateSearchResultStarredStatus = useCallback(
    (botId: string, isStarred: boolean) => {
      if (searchResults) {
        // Optimistic update for search results
        mutateSearchResults(
          searchResults.map((bot: BotMeta) =>
            bot.id === botId ? { ...bot, isStarred } : bot
          ),
          // false = don't revalidate (optimistic update)
          false
        );
      }
    },
    [searchResults, mutateSearchResults]
  );

  return {
    searchQuery,
    displayQuery, // Query for displaying search results
    searchResults: searchResults ?? [],
    isSearching,
    hasSearched,
    handleSearch,
    clearSearch,
    updateSearchResultStarredStatus,
  };
};

export default useBotSearch;
