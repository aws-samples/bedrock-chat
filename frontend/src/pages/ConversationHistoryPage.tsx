import React, { useCallback, useLayoutEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  PiCheck,
  PiMagnifyingGlass,
  PiPencilLine,
  PiPlus,
  PiTrash,
  PiX,
} from 'react-icons/pi';
import { useNavigate } from 'react-router-dom';
import useConversation from '../hooks/useConversation';
import useConversationSearch from '../hooks/useConversationSearch';
import { ConversationMeta } from '../@types/conversation';
import ButtonIcon from '../components/ButtonIcon';
import InputText from '../components/InputText';
import useChat from '../hooks/useChat';
import DialogConfirmDeleteChat from '../components/DialogConfirmDeleteChat';
import Button from '../components/Button';
import ListPageLayout from '../layouts/ListPageLayout';
import ConversationSearchResults from '../components/ConversationSearchResults';

const ConversationHistoryPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [isOpenDeleteDialog, setIsOpenDeleteDialog] = useState(false);
  const [targetConversation, setTargetConversation] =
    useState<ConversationMeta>();
  const [editingConversationId, setEditingConversationId] = useState<
    string | null
  >(null);
  const [tempTitle, setTempTitle] = useState('');
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const { setConversationId, newChat } = useChat();
  const {
    conversations,
    deleteConversation,
    updateTitle,
    isLoadingConversations,
  } = useConversation();

  // Search hook
  const {
    searchResults,
    isSearching,
    hasSearched,
    displayQuery,
    handleSearch,
    clearSearch,
  } = useConversationSearch();

  // Input change handler
  const handleInputChange = useCallback(
    (value: string) => {
      setInputValue(value);
      handleSearch(value);
    },
    [handleSearch]
  );

  // Clear search
  const handleClearSearch = useCallback(() => {
    setInputValue('');
    clearSearch();
  }, [clearSearch]);

  const onClickNewChat = useCallback(() => {
    newChat();
    navigate('/');
  }, [newChat, navigate]);

  const onClickDelete = useCallback(
    (e: React.MouseEvent, conversation: ConversationMeta) => {
      e.stopPropagation();
      setIsOpenDeleteDialog(true);
      setTargetConversation(conversation);
    },
    []
  );

  const onClickEdit = useCallback(
    (e: React.MouseEvent, conversation: ConversationMeta) => {
      e.stopPropagation();
      setEditingConversationId(conversation.id);
      setTempTitle(conversation.title);
    },
    []
  );

  const onDeleteConversation = useCallback(() => {
    if (targetConversation) {
      setIsOpenDeleteDialog(false);

      // Deletion process including optimistic update is handled in useConversation
      deleteConversation(targetConversation.id).catch(() => {
        setIsOpenDeleteDialog(true);
      });
    }
  }, [deleteConversation, targetConversation]);

  const onUpdateTitle = useCallback(
    (conversationId: string, title: string) => {
      // Exit edit mode
      setEditingConversationId(null);

      // Update process including optimistic update is handled in useConversation
      updateTitle(conversationId, title);
    },
    [updateTitle]
  );

  const onClickConversation = useCallback(
    (conversationId: string) => {
      if (editingConversationId !== conversationId) {
        setConversationId(conversationId);
        navigate(`/${conversationId}`);
      }
    },
    [navigate, setConversationId, editingConversationId]
  );

  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  useLayoutEffect(() => {
    if (editingConversationId && inputRef.current) {
      inputRef.current.focus();
    }
  }, [editingConversationId]);

  useLayoutEffect(() => {
    if (editingConversationId && inputRef.current) {
      const listener = (e: KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          onUpdateTitle(editingConversationId, tempTitle);
        } else if (e.key === 'Escape') {
          setEditingConversationId(null);
        }
      };

      const currentRef = inputRef.current;

      currentRef.addEventListener('keydown', listener);
      return () => {
        currentRef.removeEventListener('keydown', listener);
      };
    }
  }, [editingConversationId, tempTitle, onUpdateTitle]);

  return (
    <>
      <DialogConfirmDeleteChat
        isOpen={isOpenDeleteDialog}
        target={targetConversation}
        onDelete={onDeleteConversation}
        onClose={() => {
          setIsOpenDeleteDialog(false);
        }}
      />

      <ListPageLayout
        pageTitle={t('conversationHistory.pageTitle')}
        pageTitleActions={
          <Button
            className="text-sm"
            outlined
            icon={<PiPlus />}
            onClick={onClickNewChat}>
            {t('button.newChat')}
          </Button>
        }
        searchCondition={
          <div className="relative mb-2">
            <InputText
              icon={<PiMagnifyingGlass />}
              placeholder={t(
                'conversationHistory.search.placeholder',
                'Search conversations...'
              )}
              value={inputValue}
              onChange={handleInputChange}
            />
            {inputValue && (
              <button
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray hover:text-dark-gray"
                onClick={handleClearSearch}>
                <PiX size={20} />
              </button>
            )}
          </div>
        }
        isLoading={isLoadingConversations && !hasSearched}
        isEmpty={conversations?.length === 0 && !hasSearched}
        emptyMessage={t('conversationHistory.label.noConversations')}>
        {/* Search results */}
        <ConversationSearchResults
          results={searchResults}
          isSearching={isSearching}
          hasSearched={hasSearched}
          searchQuery={displayQuery}
          onbackToConversationHistory={handleClearSearch}
          onSelectConversation={onClickConversation}
        />

        {/* Regular conversation list (hidden during search) */}
        {!hasSearched &&
          conversations?.map((conversation) => (
            <div
              key={conversation.id}
              className="group flex cursor-pointer items-center justify-between border-b border-gray p-2 hover:bg-light-gray"
              onClick={() => onClickConversation(conversation.id)}>
              <div className="flex flex-col">
                {editingConversationId === conversation.id ? (
                  <div
                    className="flex items-center"
                    onClick={(e) => e.stopPropagation()}>
                    <input
                      ref={inputRef}
                      type="text"
                      className="w-64 bg-transparent text-base"
                      value={tempTitle}
                      onChange={(e) => setTempTitle(e.target.value)}
                    />
                    <ButtonIcon
                      className="text-base"
                      onClick={() => onUpdateTitle(conversation.id, tempTitle)}
                      disabled={
                        !tempTitle.trim() ||
                        tempTitle.trim() === conversation.title
                      }>
                      <PiCheck />
                    </ButtonIcon>
                    <ButtonIcon
                      className="text-base"
                      onClick={() => setEditingConversationId(null)}>
                      <PiX />
                    </ButtonIcon>
                  </div>
                ) : (
                  <div className="flex items-center">
                    <div className="text-base font-medium">
                      {conversation.title}
                    </div>
                    <ButtonIcon
                      className="-my-2 mr-6 opacity-0 group-hover:opacity-100"
                      onClick={(e) => onClickEdit(e, conversation)}>
                      <PiPencilLine />
                    </ButtonIcon>
                  </div>
                )}
                <div className="text-xs text-gray">
                  {formatDate(conversation.createTime)}
                </div>
              </div>
              {editingConversationId !== conversation.id && (
                <div className="flex items-center opacity-0 group-hover:opacity-100">
                  <ButtonIcon onClick={(e) => onClickDelete(e, conversation)}>
                    <PiTrash />
                  </ButtonIcon>
                </div>
              )}
            </div>
          ))}
      </ListPageLayout>
    </>
  );
};

export default ConversationHistoryPage;
