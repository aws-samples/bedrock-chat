import React from 'react';
import { useTranslation } from 'react-i18next';
import { ConversationMeta } from '../@types/conversation';
import { PiArrowLeft, PiMagnifyingGlass } from 'react-icons/pi';
import Button from './Button';
import Skeleton from './Skeleton';

type ConversationItemProps = {
  conversation: ConversationMeta;
  onClick: (id: string) => void;
  searchQuery: string;
};

// Helper function to highlight search terms in the text
const highlightSearchTerms = (text: string, searchQuery: string): string => {
  if (!searchQuery.trim()) {return text;}
  
  // Escape special characters in the search query
  const escapedQuery = searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  
  // Create a regex to match the search query (case insensitive)
  const regex = new RegExp(`(${escapedQuery})`, 'gi');
  
  // Replace matches with highlighted version
  return text.replace(regex, '<mark class="bg-light-yellow dark:bg-light-yellow">$1</mark>');
};

export const ConversationItem: React.FC<ConversationItemProps> = ({ conversation, onClick, searchQuery }) => {
  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  // Function to render highlight fragments
  const renderHighlights = () => {
    if (!conversation.highlights || conversation.highlights.length === 0) {
      return null;
    }

    //Highlight the messageBody field according to the response from the backend
    const messageHighlights = conversation.highlights.filter(h => h.fieldName === 'MessageBody');
    
    if (messageHighlights.length === 0) {
      return null;
    }
    
    return (
      <div className="mt-1">
        {messageHighlights.map((highlight, highlightIndex) => (
          <div key={highlightIndex}>
            {highlight.fragments.map((fragment, fragmentIndex) => (
              <div 
                key={fragmentIndex} 
                className="text-sm text-dark-gray dark:text-gray p-1 border-l-2 border-gray mt-1 line-clamp-2"
              >
                <span 
                  dangerouslySetInnerHTML={{ 
                    __html: `...${fragment}...`
                  }}
                  className="[&_em]:bg-light-yellow [&_em]:dark:bg-light-yellow"
                />
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div
      className="group flex flex-col cursor-pointer border-b border-gray p-2 hover:bg-light-gray dark:border-dark-gray dark:hover:bg-aws-squid-ink-light"
      onClick={() => onClick(conversation.id)}>
      <div className="flex items-center justify-between">
        <div className="flex flex-col">
          <div className="text-base font-medium">
            <span dangerouslySetInnerHTML={{
              __html: highlightSearchTerms(conversation.title, searchQuery)
            }} />
          </div>
          <div className="text-xs text-gray">
            {formatDate(conversation.createTime)}
          </div>
        </div>
      </div>
      {/* Display highlight fragments */}
      {renderHighlights()}
    </div>
  );
};

export const SkeletonConversation: React.FC = () => {
  return <Skeleton className="h-16 w-full rounded" />;
};

type ConversationSearchResultsProps = {
  results: ConversationMeta[];
  isSearching: boolean;
  hasSearched: boolean;
  searchQuery: string;
  onbackToConversationHistory: () => void;
  onSelectConversation: (id: string) => void;
};

const ConversationSearchResults: React.FC<ConversationSearchResultsProps> = ({
  results,
  isSearching,
  hasSearched,
  searchQuery,
  onbackToConversationHistory,
  onSelectConversation,
}) => {
  const { t } = useTranslation();

  if (!hasSearched) {
    return null;
  }

  if (isSearching) {
    return (
      <div className="mt-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center text-2xl font-bold">
            <PiMagnifyingGlass className="mr-2" />
            {t('conversationHistory.searchConversation.searching', 'Searching...')}
          </div>
          <Button
            className="text-sm"
            outlined
            icon={<PiArrowLeft />}
            onClick={onbackToConversationHistory}>
            {t('button.backToConversationHistory', 'Back to History')}
          </Button>
        </div>
        <div className="mt-4 space-y-2">
          <SkeletonConversation />
          <SkeletonConversation />
          <SkeletonConversation />
        </div>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="mt-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center text-2xl font-bold">
            <PiMagnifyingGlass className="mr-2" />
            {t('conversationHistory.searchConversation.resultsTitle', 'Search Results')}
          </div>
          <Button
            className="text-sm"
            outlined
            icon={<PiArrowLeft />}
            onClick={onbackToConversationHistory}>
            {t('button.backToConversationHistory', 'Back to History')}
          </Button>
        </div>
        
        <div className="mt-1 text-sm text-gray">
          {searchQuery && (
            <span>
              {t('conversationHistory.searchConversation.queryLabel', 'Query')}: <strong>{searchQuery}</strong>
            </span>
          )}
        </div>

        <div className="mt-10 flex flex-col items-center justify-center">
          <div className="text-xl font-medium">
            {t('conversationHistory.searchConversation.noResults', 'No conversations found')}
          </div>
          <div className="mt-2 text-gray">
            {t('conversationHistory.searchConversation.tryDifferentKeywords', 'Try different keywords')}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mt-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center text-2xl font-bold">
          <PiMagnifyingGlass className="mr-2" />
          {t('conversationHistory.searchConversation.resultsTitle', 'Search Results')}
        </div>
        <Button
          className="text-sm"
          outlined
          icon={<PiArrowLeft />}
          onClick={onbackToConversationHistory}>
          {t('button.backToConversationHistory', 'Back to History')}
        </Button>
      </div>
      
      <div className="mt-1 text-sm text-gray">
        {searchQuery && (
          <span>
            {t('conversationHistory.searchConversation.queryLabel', 'Query')}: <strong>{searchQuery}</strong>
            {' '}
            ({t('conversationHistory.searchConversation.resultsCount', '{{count}} results found', { count: results.length })})
          </span>
        )}
      </div>

      <div className="mt-3">
        {results.map((conversation) => (
          <ConversationItem
            key={conversation.id}
            conversation={conversation}
            onClick={onSelectConversation}
            searchQuery={searchQuery}
          />
        ))}
      </div>
    </div>
  );
};

export default ConversationSearchResults;
