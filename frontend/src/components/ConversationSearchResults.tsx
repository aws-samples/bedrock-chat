import React from 'react';
import { useTranslation } from 'react-i18next';
import { ConversationMeta } from '../@types/conversation';
import { PiArrowLeft, PiMagnifyingGlass } from 'react-icons/pi';
import Button from './Button';
import Skeleton from './Skeleton';

type ConversationItemProps = {
  conversation: ConversationMeta;
  onClick: (id: string) => void;
};

export const ConversationItem: React.FC<ConversationItemProps> = ({ conversation, onClick }) => {
  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div
      className="group flex cursor-pointer items-center justify-between border-b border-gray p-2 hover:bg-light-gray dark:border-dark-gray dark:hover:bg-aws-squid-ink-light"
      onClick={() => onClick(conversation.id)}>
      <div className="flex flex-col">
        <div className="text-base font-medium">{conversation.title}</div>
        <div className="text-xs text-gray">
          {formatDate(conversation.createTime)}
        </div>
      </div>
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
  onBackToHistory: () => void;
  onSelectConversation: (id: string) => void;
};

const ConversationSearchResults: React.FC<ConversationSearchResultsProps> = ({
  results,
  isSearching,
  hasSearched,
  searchQuery,
  onBackToHistory,
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
            {t('conversationHistory.search.searching', 'Searching...')}
          </div>
          <Button
            className="text-sm"
            outlined
            icon={<PiArrowLeft />}
            onClick={onBackToHistory}>
            {t('button.backToHistory', 'Back to History')}
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
            {t('conversationHistory.search.resultsTitle', 'Search Results')}
          </div>
          <Button
            className="text-sm"
            outlined
            icon={<PiArrowLeft />}
            onClick={onBackToHistory}>
            {t('button.backToHistory', 'Back to History')}
          </Button>
        </div>
        
        <div className="mt-1 text-sm text-gray">
          {searchQuery && (
            <span>
              {t('conversationHistory.search.queryLabel', 'Query')}: <strong>{searchQuery}</strong>
            </span>
          )}
        </div>

        <div className="mt-10 flex flex-col items-center justify-center">
          <div className="text-xl font-medium">
            {t('conversationHistory.search.noResults', 'No conversations found')}
          </div>
          <div className="mt-2 text-gray">
            {t('conversationHistory.search.tryDifferentKeywords', 'Try different keywords')}
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
          {t('conversationHistory.search.resultsTitle', 'Search Results')}
        </div>
        <Button
          className="text-sm"
          outlined
          icon={<PiArrowLeft />}
          onClick={onBackToHistory}>
          {t('button.backToHistory', 'Back to History')}
        </Button>
      </div>
      
      <div className="mt-1 text-sm text-gray">
        {searchQuery && (
          <span>
            {t('conversationHistory.search.queryLabel', 'Query')}: <strong>{searchQuery}</strong>
            {' '}
            ({t('conversationHistory.search.resultsCount', '{{count}} results found', { count: results.length })})
          </span>
        )}
      </div>

      <div className="mt-3">
        {results.map((conversation) => (
          <ConversationItem
            key={conversation.id}
            conversation={conversation}
            onClick={onSelectConversation}
          />
        ))}
      </div>
    </div>
  );
};

export default ConversationSearchResults;
