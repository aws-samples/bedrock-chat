import { useState, useCallback } from 'react';
import { useDebounce } from 'use-debounce';
import useConversationSearchApi from './useConversationSearchApi';

// Debounce delay in milliseconds
const DEBOUNCE_DELAY = 300;

export function useConversationSearch() {
  const conversationSearchApi = useConversationSearchApi();
  const [searchQuery, setSearchQuery] = useState('');
  const [displayQuery, setDisplayQuery] = useState('');
  const [hasSearched, setHasSearched] = useState(false);
  const [debouncedQuery] = useDebounce(searchQuery, DEBOUNCE_DELAY);

  const {
    data: searchResults,
    isLoading: isSearching,
    mutate: mutateSearchResults,
  } = conversationSearchApi.searchConversations(hasSearched && debouncedQuery ? debouncedQuery : null);

  // Execute search when debouncedQuery changes
  const handleSearch = useCallback(
    (query: string) => {
      setSearchQuery(query);

      if (!query.trim()) {
        setHasSearched(false);
        setDisplayQuery('');
        return;
      }

      setHasSearched(true);
      setDisplayQuery(query);
      mutateSearchResults();
    },
    [mutateSearchResults]
  );

  // Clear search
  const clearSearch = useCallback(() => {
    setSearchQuery('');
    setDisplayQuery('');
    setHasSearched(false);
  }, []);

  return {
    searchResults: searchResults ?? [],
    isSearching,
    hasSearched,
    displayQuery,
    handleSearch,
    clearSearch
  };
}

export default useConversationSearch;
