export type BaseProps = {
  className?: string | undefined;
};

export type DrawerOptions = {
  displayCount: {
    starredBots: number;
    recentlyUsedBots: number;
    conversationHistory: number;
  };
};
