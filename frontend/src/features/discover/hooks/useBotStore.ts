import useBotApi from '../../../hooks/useBotApi';
import useBotStoreApi from './useBotStoreApi';
import { BotMeta } from '../../../@types/bot';
import { useCallback } from 'react';

const useBotStore = () => {
  const { getPickupBots, getPopularBots } = useBotStoreApi();
  const { getPinnedBots, updateBotStarred } = useBotApi();

  const {
    data: pickupBots,
    isLoading: isLoadingPickupBots,
    mutate: mutatePickupBots,
  } = getPickupBots(50);

  const {
    data: popularBots,
    isLoading: isLoadingPopularBots,
    mutate: mutatePopularBots,
  } = getPopularBots(50);

  const {
    data: pinnedBots,
    isLoading: isLoadingPinnedBots,
    mutate: mutatePinnedBots,
  } = getPinnedBots();

  // Utility function for optimistic updates
  const updateBotStarredStatus = useCallback(
    (botId: string, isStarred: boolean) => {
      // Update pinnedBots
      if (pinnedBots) {
        mutatePinnedBots(
          pinnedBots.map((bot: BotMeta) =>
            bot.id === botId ? { ...bot, isStarred } : bot
          ),
          false
        );
      }

      // Update pickupBots
      if (pickupBots) {
        mutatePickupBots(
          pickupBots.map((bot: BotMeta) =>
            bot.id === botId ? { ...bot, isStarred } : bot
          ),
          false
        );
      }

      // Update popularBots
      if (popularBots) {
        mutatePopularBots(
          popularBots.map((bot: BotMeta) =>
            bot.id === botId ? { ...bot, isStarred } : bot
          ),
          false
        );
      }
    },
    [
      pinnedBots,
      pickupBots,
      popularBots,
      mutatePinnedBots,
      mutatePickupBots,
      mutatePopularBots,
    ]
  );

  // Toggle star status (includes API call and optimistic update)
  const toggleBotStarred = useCallback(
    (botId: string, starred: boolean) => {
      // Optimistic update
      updateBotStarredStatus(botId, starred);

      // API request
      return updateBotStarred(botId, { starred }).catch((error) => {
        console.error('Failed to update star status:', error);
        // Revert to original state on error
        updateBotStarredStatus(botId, !starred);
        throw error; // Re-throw the error
      });
    },
    [updateBotStarred, updateBotStarredStatus]
  );

  return {
    pinnedBots: pinnedBots ?? [],
    isLoadingPinnedBots,
    popularBots: popularBots ?? [],
    isLoadingPopularBots,
    pickupBots: pickupBots ?? [],
    isLoadingPickupBots,
    toggleBotStarred,
  };
};

export default useBotStore;
