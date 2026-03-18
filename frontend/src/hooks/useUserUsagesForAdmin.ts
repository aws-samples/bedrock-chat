import { GetUserUsagesRequest } from '../@types/api-publication';
import useAdminApi from './useAdminApi';

const useUserUsagesForAdmin = (params: GetUserUsagesRequest) => {
  const { getUserUsages } = useAdminApi();

  const { data, isLoading, mutate } = getUserUsages(params);

  return {
    userUsages: data,
    isLoading,
    mutate,
  };
};

export default useUserUsagesForAdmin;
