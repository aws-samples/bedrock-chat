import { setup, assign } from 'xstate';

export type AgentToolsProps = {
  // Note: key is toolUseId
  [key: string]: {
    name: string;
    status: AgentToolState;
    input: { [key: string]: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
    content?: { text: string };
  };
};

export const AgentState = {
  SLEEPING: 'sleeping',
  THINKING: 'thinking',
  LEAVING: 'leaving',
} as const;

export type AgentToolState = 'running' | 'success' | 'error';

export type AgentState = (typeof AgentState)[keyof typeof AgentState];

export type AgentEvent =
  | { type: 'wakeup' }
  | {
      type: 'go-on';
      toolUseId: string;
      name: string;
      input: { [key: string]: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
    }
  | {
      type: 'tool-result';
      toolUseId: string;
      status: AgentToolState;
      content: { text: string };
    }
  | { type: 'goodbye' };

export type AgentEventKeys = AgentEvent['type'];

export const agentThinkingState = setup({
  types: {
    context: {} as {
      tools: AgentToolsProps;
    },
    events: {} as AgentEvent,
  },
  actions: {
    reset: assign({
      tools: () => ({}),
    }),
    addTool: assign({
      tools: ({ context, event }) => {
        if (event.type === 'go-on') {
          return {
            ...context.tools,
            [event.toolUseId]: {
              name: event.name,
              input: event.input,
              status: 'running' as AgentToolState,
            },
          };
        }
        return context.tools;
      },
    }),
    updateToolResult: assign({
      tools: ({ context, event }) => {
        if (event.type === 'tool-result') {
          // Update status and content of the tool
          return {
            ...context.tools,
            [event.toolUseId]: {
              ...context.tools[event.toolUseId],
              status: event.status,
              content: event.content,
            },
          };
        }
        return context.tools;
      },
    }),
    close: assign({
      tools: () => ({}),
    }),
  },
}).createMachine({
  context: {
    tools: {},
    areAllToolsSuccessful: false,
  },
  initial: 'sleeping',
  states: {
    sleeping: {
      on: {
        wakeup: {
          actions: 'reset',
          target: 'thinking',
        },
      },
    },
    thinking: {
      on: {
        'go-on': {
          actions: 'addTool',
        },
        'tool-result': {
          actions: ['updateToolResult'],
        },
        goodbye: {
          actions: 'close',
          target: 'leaving',
        },
      },
    },
    leaving: {
      after: {
        2500: { target: 'sleeping' },
      },
    },
  },
});
