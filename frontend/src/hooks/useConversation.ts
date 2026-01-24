import { produce } from 'immer';
import { useCallback, useEffect, useState } from 'react';
import useConversationApi from './useConversationApi';
import {
  EPHEMERAL_MODE,
  getAllConversationsLocally,
  deleteConversationLocally,
  clearAllConversationsLocally,
  updateTitleLocally,
} from './useConversationStorage';
import { ConversationMeta } from '../@types/conversation';

/**
 * Hook for ephemeral mode - uses IndexedDB instead of API
 */
const useEphemeralConversation = () => {
  const [conversations, setConversations] = useState<ConversationMeta[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadConversations = useCallback(async () => {
    setIsLoading(true);
    try {
      const convs = await getAllConversationsLocally();
      setConversations(
        convs.map((c) => ({
          id: c.id,
          title: c.title,
          createTime: c.createTime,
          lastMessageId: c.lastMessageId,
          model: c.model,
          botId: c.botId,
        }))
      );
    } catch (error) {
      console.error('Failed to load local conversations:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  return {
    conversations,
    isLoadingConversations: isLoading,
    mutateConversations: loadConversations,
    syncConversations: loadConversations,
    getTitle: (conversationId: string) => {
      return (
        conversations?.find((c) => c.id === conversationId)?.title ?? 'New Chat'
      );
    },
    getBotId: (conversationId: string) => {
      return conversations?.find((c) => c.id === conversationId)?.botId ?? null;
    },
    deleteConversation: async (conversationId: string) => {
      // Optimistic update
      setConversations((prev) => prev.filter((c) => c.id !== conversationId));
      await deleteConversationLocally(conversationId);
    },
    clearConversations: async () => {
      setConversations([]);
      await clearAllConversationsLocally();
    },
    updateTitle: async (conversationId: string, title: string) => {
      // Optimistic update
      setConversations((prev) =>
        prev.map((c) => (c.id === conversationId ? { ...c, title } : c))
      );
      await updateTitleLocally(conversationId, title);
    },
  };
};

/**
 * Hook for normal mode - uses API
 */
const useServerConversation = () => {
  const conversationApi = useConversationApi();

  const { data: conversations, isLoading: isLoadingConversations } =
    conversationApi.getConversations();
  const mutate = conversationApi.mutateConversations;

  return {
    conversations,
    isLoadingConversations,
    mutateConversations: mutate,
    syncConversations: () => {
      return mutate(conversations);
    },
    getTitle: (conversationId: string) => {
      return (
        conversations?.find((c) => c.id === conversationId)?.title ?? 'New Chat'
      );
    },
    getBotId: (conversationId: string) => {
      return conversations?.find((c) => c.id === conversationId)?.botId ?? null;
    },
    deleteConversation: (conversationId: string) => {
      // Optimistic update: Update UI before deletion
      mutate(
        produce(conversations, (draft) => {
          if (draft) {
            const index = draft.findIndex((c) => c.id === conversationId);
            if (index !== -1) {
              draft.splice(index, 1);
            }
          }
        }),
        { revalidate: false }
      );

      // Actual API call
      return conversationApi
        .deleteConversation(conversationId)
        .catch((error) => {
          console.error('Failed to delete conversation:', error);
          // Revert to original state on error
          mutate();
          throw error; // Re-throw error so it can be caught by the caller
        });
    },
    clearConversations: () => {
      return mutate(async () => {
        await conversationApi.clearConversations();
        return [];
      });
    },
    updateTitle: (conversationId: string, title: string) => {
      // Optimistic update
      mutate(
        produce(conversations, (draft) => {
          if (draft) {
            const target = draft.find((c) => c.id === conversationId);
            if (target) {
              target.title = title;
            }
          }
        }),
        { revalidate: false }
      );

      // Actual API call
      return conversationApi
        .updateTitle(conversationId, title)
        .catch((error) => {
          console.error('Failed to update title:', error);
          // Revert to original state on error
          mutate();
          throw error; // Re-throw error so it can be caught by the caller
        });
    },
  };
};

const useConversation = EPHEMERAL_MODE
  ? useEphemeralConversation
  : useServerConversation;

export default useConversation;
