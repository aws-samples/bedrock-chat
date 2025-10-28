export type BaseProps = {
  className?: string | undefined;
};

export type DrawerOptions = {
  displayCount: {
    starredBots: number;
    recentlyUsedBots: number;
    conversationHistory: number;
  };
  show: {
    newChat: boolean;
    myBots: boolean;
    discoverBots: boolean;
    pinnedBots: boolean;
    starredBots: boolean;
    recentlyUsedBots: boolean;
    conversationHistory: boolean;
  };
};
