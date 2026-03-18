import { GetUserConversationsRequest } from '../@types/api-publication';
import useAdminApi from './useAdminApi';

const useUserConversationsForAdmin = (
  userId: string,
  params: GetUserConversationsRequest
) => {
  const { getUserConversations } = useAdminApi();

  const { data, isLoading, mutate } = getUserConversations(userId, params);

  return {
    conversations: data,
    isLoading,
    mutate,
  };
};

export default useUserConversationsForAdmin;
