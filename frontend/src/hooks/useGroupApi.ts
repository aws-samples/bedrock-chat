import useHttp from './useHttp';
import { GetGroupListResponse } from '../@types/group';

const useGroupApi = () => {
    const http = useHttp();
    return {
        getGroupListApi: () => {
            return http.getOnce<GetGroupListResponse>('group/self');
        }
    }
}

export default useGroupApi;