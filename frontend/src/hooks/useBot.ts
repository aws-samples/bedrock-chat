import { RegisterBotRequest, UpdateBotRequest } from '../@types/bot';
import useBotApi from './useBotApi';
import { produce } from 'immer';

const useBot = (shouldAutoRefreshMyBots?: boolean) => {
  const api = useBotApi();

  const {
    data: myBots,
    mutate: mutateMyBots,
    isLoading: isLoadingMyBots,
  } = api.bots(
    {
      kind: 'private',
    },
    shouldAutoRefreshMyBots
      ? (data) => {
          if (!data) {
            return 0;
          }
          const index = data.findIndex(
            (bot) => bot.syncStatus === 'QUEUED' || bot.syncStatus === 'RUNNING'
          );
          return index > -1 ? 5000 : 0;
        }
      : undefined
  );

  const { data: starredBots, mutate: mutateStarredBots } = api.bots({
    kind: 'mixed',
    starred: true,
  });

  const {
    data: recentlyUsedBots,
    mutate: mutateRecentlyUsedBots,
    isLoading: isLoadingRecentlyUsedBots,
  } = api.bots({
    kind: 'mixed',
    limit: 30,
  });

  return {
    myBots,
    mutateMyBots,
    isLoadingMyBots,
    starredBots: starredBots?.filter((bot) => bot.available),
    mutateStarredBots,
    recentlyUsedBots,
    isLoadingRecentlyUsedBots,
    mutateRecentlyUsedBots,
    recentlyUsedUnstarredBots: recentlyUsedBots?.filter(
      (bot) => !bot.isStarred && bot.available
    ),
    recentlyUsedSharedBots: recentlyUsedBots?.filter((bot) => !bot.owned),
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
            isStarred: false,
            owned: true,
            syncStatus: 'QUEUED',
            sharedScope: 'private',
            sharedStatus: 'private',
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
    updateStarred: (botId: string, isStarred: boolean) => {
      const idxMybots = myBots?.findIndex((bot) => bot.id === botId) ?? -1;
      if (idxMybots > -1) {
        mutateMyBots(
          produce(myBots, (draft) => {
            if (draft) {
              draft[idxMybots].isStarred = isStarred;
            }
          }),
          {
            revalidate: false,
          }
        );
      }

      const idxRecentlyUsed =
        recentlyUsedBots?.findIndex((bot) => bot.id === botId) ?? -1;
      if (idxRecentlyUsed > -1) {
        mutateRecentlyUsedBots(
          produce(recentlyUsedBots, (draft) => {
            if (draft) {
              draft[idxRecentlyUsed].isStarred = isStarred;
            }
          }),
          {
            revalidate: false,
          }
        );
      }

      if (isStarred) {
        // add starred bot
        if (idxMybots > -1 && myBots) {
          mutateStarredBots(
            produce(starredBots, (draft) => {
              draft?.unshift({
                ...myBots[idxMybots],
              });
            })
          );
        } else if (idxRecentlyUsed && recentlyUsedBots) {
          mutateStarredBots(
            produce(starredBots, (draft) => {
              draft?.unshift({
                ...recentlyUsedBots[idxRecentlyUsed],
              });
            })
          );
        }
      } else {
        // remove starred bot
        const idxStarred =
          starredBots?.findIndex((bot) => bot.id === botId) ?? -1;
        if (idxStarred > -1) {
          mutateStarredBots(
            produce(starredBots, (draft) => {
              draft?.splice(idxStarred, 1);
            })
          );
        }
      }

      return api
        .updateBotStarred(botId, {
          starred: isStarred,
        })
        .finally(() => {
          mutateMyBots();
          mutateStarredBots();
          mutateRecentlyUsedBots();
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
      // Also remove from recently used bots if present
      const recentlyUsedIdx =
        recentlyUsedBots?.findIndex((bot) => bot.id === botId) ?? -1;
      if (recentlyUsedIdx > -1) {
        mutateRecentlyUsedBots(
          produce(recentlyUsedBots, (draft) => {
            draft?.splice(recentlyUsedIdx, 1);
          }),
          {
            revalidate: false,
          }
        );
      }
      return api.deleteBot(botId).finally(() => {
        mutateMyBots();
      });
    },
    removeFromRecentlyUsed: (botId: string) => {
      const idx = recentlyUsedBots?.findIndex((bot) => bot.id === botId) ?? -1;
      mutateRecentlyUsedBots(
        produce(recentlyUsedBots, (draft) => {
          draft?.splice(idx, 1);
        }),
        {
          revalidate: false,
        }
      );
      return api.removeFromRecentlyUsed(botId).finally(() => {
        mutateRecentlyUsedBots();
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
