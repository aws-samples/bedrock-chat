import { useState } from 'react';
import { BotSyncStatus, RegisterBotRequest, UpdateBotRequest } from '../@types/bot';
import useBotApi from './useBotApi';
import useLocalStorage from './useLocalStorage';
import { produce } from 'immer';
import { BASE_REFRESH_INTERVAL } from '../constants';

interface SyncState {
  interval: number;
  lastStatus?: BotSyncStatus;
 }

const useBot = (shouldAutoRefreshMyBots?: boolean) => {
  const [syncState, setSyncState] = useState<SyncState>({
    interval: BASE_REFRESH_INTERVAL,
    lastStatus: undefined
  });

  const api = useBotApi();

  const { data: myBots, mutate: mutateMyBots } = api.bots(
    { kind: 'groups' },
    shouldAutoRefreshMyBots
      ? (data) => {
          if (!data) return 0;
          
          const runningBot = data.find(bot => 
            bot.syncStatus === 'QUEUED' || bot.syncStatus === 'RUNNING'
          );

          if (!runningBot) {
            return 0;
          }

          if (runningBot.syncStatus !== syncState.lastStatus) {
            setSyncState({
              interval: BASE_REFRESH_INTERVAL,
              lastStatus: runningBot.syncStatus
            });
            return BASE_REFRESH_INTERVAL;
          }

          return syncState.interval;
        }
      : undefined
  );

  const [groupId] = useLocalStorage(
    'groupId',
    // default value for testing. Will need to change 
    '353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f-15'
  );

  const { data: starredBots } = api.bots({
    // getting the groupId from localstorage
    group_id: groupId,
  });

  return {
    myBots,
    starredBots: starredBots?.filter((bot) => bot.available),
    getAvailableAssistants: async () => {
      return (await api.bots({group_id: groupId})).data;
    },
    getMyBot: async (botId: string) => {
      return (await api.getOnceMyBot(botId)).data;
    },
    registerBot: (params: RegisterBotRequest) => {
      mutateMyBots(
        produce(myBots, (draft) => {
          draft?.unshift({
            id: params.id,
            title: params.title,
            description: params.description ?? '',
            available: true,
            createTime: new Date(),
            lastUsedTime: new Date(),
            isPinned: false,
            isPublic: false,
            owned: true,
            syncStatus: 'QUEUED',
            assistantConfig: params.assistantConfig,
            creatorConfig: null,
            groupId: params.groupId
          });
        }),
        {
          revalidate: false,
        }
      );
      return api.registerBot(params).finally(() => {
        mutateMyBots();
      });
    },
    updateBot: (botId: string, params: UpdateBotRequest) => {
      mutateMyBots(
        produce(myBots, (draft) => {
          const idx = myBots?.findIndex((bot) => bot.id === botId) ?? -1;
          if (draft) {
            draft[idx].title = params.title;
            draft[idx].description = params.description ?? '';
            draft[idx].description = params.assistantConfig.assistantType;
          }
        }),
        {
          revalidate: false,
        }
      );

      return api.updateBot(botId, params).finally(() => {
        mutateMyBots();
      });
    },
    updateBotSharing: (botId: string, isShareing: boolean) => {
      mutateMyBots(
        produce(myBots, (draft) => {
          const idx = draft?.findIndex((bot) => bot.id === botId) ?? -1;
          if (draft) {
            draft[idx].isPublic = isShareing;
          }
        }),
        {
          revalidate: false,
        }
      );

      return api
        .updateBotVisibility(botId, {
          toPublic: isShareing,
        })
        .finally(() => {
          mutateMyBots();
        });
    },
    deleteMyBot: (botId: string) => {
      const idx = myBots?.findIndex((bot) => bot.id === botId) ?? -1;
      mutateMyBots(
        produce(myBots, (draft) => {
          draft?.splice(idx, 1);
        }),
        {
          revalidate: false,
        }
      );
      return api.deleteBot(botId).finally(() => {
        mutateMyBots();
      });
    },
    uploadFile: (
      botId: string,
      file: File,
      onProgress?: (progress: number) => void
    ) => {
      return api.getPresignedUrl(botId, file).then(({ data }) => {
        data.url;
        return api.uploadFile(data.url, file, onProgress);
      });
    },
    deleteUploadedFile: (botId: string, filename: string) => {
      return api.deleteUploadedFile(botId, filename);
    },
  };
};

export default useBot;
