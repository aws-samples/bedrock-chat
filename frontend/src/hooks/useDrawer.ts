import { create } from 'zustand';
import { DrawerOptions } from '../@types/common';

const DEFAULT_OPTIONS: DrawerOptions = {
  displayCount: {
    starredBots: 15,
    recentlyUsedBots: 15,
    conversationHistory: 5,
  },
};

const useDrawerStore = create<{
  opened: boolean;
  drawerOptions: DrawerOptions;
  switchOpen: () => void;
  setDrawerOptions: (options: DrawerOptions) => void;
}>((set) => {
  // get drawer option from local storage
  let initialOptions = DEFAULT_OPTIONS;
  try {
    const savedOptions = localStorage.getItem('DrawerOptions');
    if (savedOptions) {
      initialOptions = JSON.parse(savedOptions);
    }
  } catch (e) {
    console.error('Failed to parse DrawerOptions from localStorage', e);
  }

  return {
    opened: false,
    drawerOptions: initialOptions,
    switchOpen: () => {
      set((state) => ({
        opened: !state.opened,
      }));
    },
    setDrawerOptions: (options: DrawerOptions) => {
      // save local storage
      localStorage.setItem('DrawerOptions', JSON.stringify(options));
      // update state
      set({ drawerOptions: options });
    },
  };
});

const useDrawer = () => {
  const { opened, switchOpen, drawerOptions, setDrawerOptions } =
    useDrawerStore();

  return {
    opened,
    switchOpen,
    drawerOptions,
    setDrawerOptions,
  };
};

export default useDrawer;
