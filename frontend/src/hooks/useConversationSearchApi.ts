import { ConversationSearchMeta } from '../@types/conversation';
import useHttp from './useHttp';

const useConversationSearchApi = () => {
  const http = useHttp();

  return {
    searchConversations: (query: string | null) => {
      return http.get<ConversationSearchMeta[]>(
        query ? `conversations/search?query=${encodeURIComponent(query)}` : null
      );
    }
  };
};

export default useConversationSearchApi;
