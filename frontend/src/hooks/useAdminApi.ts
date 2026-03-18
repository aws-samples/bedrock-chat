import {
  GetUserUsagesRequest,
  GetUserUsagesResponse,
  ListBotApisRequest,
  ListBotApisResponse,
  ListPublicBotsRequest,
  ListPublicBotsResponse,
} from '../@types/api-publication';
import { GetPublicBotResponse, UpdateBotPushedRequest } from '../@types/bot';
import useHttp from './useHttp';

const useAdminApi = () => {
  const http = useHttp();

  return {
    listBotApis: (req: ListBotApisRequest) => {
      return http.get<ListBotApisResponse>(['/admin/published-bots', req]);
    },
    listPublicBots: (req: ListPublicBotsRequest) => {
      return http.get<ListPublicBotsResponse>(
        !!req.start === !!req.end ? ['/admin/public-bots', req] : null
      );
    },
    getUserUsages: (req: GetUserUsagesRequest) => {
      return http.get<GetUserUsagesResponse>(
        !!req.start === !!req.end ? ['/admin/users', req] : null
      );
    },
    getPublicBot: (botId: string) => {
      return http.get<GetPublicBotResponse>(`/admin/bot/public/${botId}`);
    },
    updatePinnedBot: (botId: string, params: UpdateBotPushedRequest) => {
      return http.patch<null>(`/admin/bot/${botId}/pushed`, params);
    },
  };
};

export default useAdminApi;
