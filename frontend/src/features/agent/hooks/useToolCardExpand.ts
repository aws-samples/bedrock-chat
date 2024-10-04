import { create } from 'zustand';

interface ToolState {
  expandedTools: { [toolId: string]: boolean };
  inputExpandedTools: { [toolId: string]: boolean };
  contentExpandedTools: { [toolId: string]: boolean };
  toggleExpand: (toolId: string) => void;
  toggleInputExpand: (toolId: string) => void;
  toggleContentExpand: (toolId: string) => void;
}

const useToolState = create<ToolState>((set) => ({
  expandedTools: {},
  inputExpandedTools: {},
  contentExpandedTools: {},
  toggleExpand: (toolId) =>
    set((state) => {
      const isNowExpanded = !state.expandedTools[toolId];
      return {
        expandedTools: {
          ...state.expandedTools,
          [toolId]: isNowExpanded,
        },
        inputExpandedTools: {
          ...state.inputExpandedTools,
          [toolId]: isNowExpanded,
        },
        contentExpandedTools: {
          ...state.contentExpandedTools,
          [toolId]: isNowExpanded,
        },
      };
    }),
  toggleInputExpand: (toolId) =>
    set((state) => ({
      inputExpandedTools: {
        ...state.inputExpandedTools,
        [toolId]: !state.inputExpandedTools[toolId],
      },
    })),
  toggleContentExpand: (toolId) =>
    set((state) => ({
      contentExpandedTools: {
        ...state.contentExpandedTools,
        [toolId]: !state.contentExpandedTools[toolId],
      },
    })),
}));

const useToolCardExpand = () => {
  const expandedTools = useToolState((state) => state.expandedTools);
  const inputExpandedTools = useToolState((state) => state.inputExpandedTools);
  const contentExpandedTools = useToolState(
    (state) => state.contentExpandedTools
  );
  const toggleExpand = useToolState((state) => state.toggleExpand);
  const toggleInputExpand = useToolState((state) => state.toggleInputExpand);
  const toggleContentExpand = useToolState(
    (state) => state.toggleContentExpand
  );

  return {
    expandedTools,
    inputExpandedTools,
    contentExpandedTools,
    toggleExpand,
    toggleInputExpand,
    toggleContentExpand,
  };
};

export default useToolCardExpand;
