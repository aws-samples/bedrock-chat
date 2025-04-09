import {
  GetPickupBotsRequest,
  GetPickupBotsResponse,
  GetPopularBotsRequest,
  GetPopularBotsResponse,
  SearchBotsRequest,
  SearchBotsResponse,
} from '../types/bot-store';
import useHttp from '../../../hooks/useHttp';

const useBotStoreApi = () => {
  const http = useHttp();

  return {
    searchBots: (query: string, limit?: number) => {
      const res: SearchBotsRequest = {
        query,
        limit,
      };
      return http.get<SearchBotsResponse>(query ? ['store/search', res] : null);
    },
    getPopularBots: (limit?: number) => {
      const res: GetPopularBotsRequest = {
        limit,
      };
      return http.get<GetPopularBotsResponse>(['store/popular', res]);
    },
    getPickupBots: (limit?: number) => {
      const res: GetPickupBotsRequest = {
        limit,
      };
      return http.get<GetPickupBotsResponse>(['store/pickup', res]);
    },
  };
};

export default useBotStoreApi;
