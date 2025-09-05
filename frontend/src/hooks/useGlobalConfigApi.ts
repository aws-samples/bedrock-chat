import { GetGlobalConfigResponse } from '../@types/global-config';
import useHttp from './useHttp';

const useGlobalConfigApi = () => {
  const http = useHttp();

  return {
    getGlobalConfig: () => {
      return http.get<GetGlobalConfigResponse>('config/global');
    },
  };
};

export default useGlobalConfigApi;
