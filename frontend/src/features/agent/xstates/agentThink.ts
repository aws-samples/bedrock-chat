import { setup, assign } from 'xstate';
import { produce } from 'immer';
import { AgentToolResultContent } from '../../../@types/conversation';

export type AgentToolsProps = {
  thought?: string;
  tools: {
    // Note: key is toolUseId
    [key: string]: AgentToolUse;
  };
};

export type AgentToolUse = {
  name: string;
  status: AgentToolState;
  input: { [key: string]: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
  content?: AgentToolResultContent[];
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
      type: 'thought';
      thought: string;
    }
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
      content: AgentToolResultContent[];
    }
  | { type: 'goodbye' };

export type AgentEventKeys = AgentEvent['type'];

export const agentThinkingState = setup({
  types: {
    context: {} as {
      tools: AgentToolsProps[];
    },
    events: {} as AgentEvent,
  },
  actions: {
    reset: assign({
      tools: () => ([]),
    }),
    updateThought: assign({
      tools: ({ context, event }) => produce(context.tools, draft => {
        if (event.type === 'thought') {
          if (draft.length > 0 && draft[draft.length - 1].thought == null) {
            draft[draft.length - 1].thought = event.thought;
          } else {
            draft.push({
              thought: event.thought,
              tools: {},
            });
          }
        }
      }),
    }),
    addTool: assign({
      tools: ({ context, event }) => produce(context.tools, draft => {
        if (event.type === 'go-on') {
          if (draft.length > 0) {
            draft[draft.length - 1].tools[event.toolUseId] = {
              name: event.name,
              input: event.input,
              status: 'running',
            };
          } else {
            draft.push({
              tools: {
                [event.toolUseId]: {
                  name: event.name,
                  input: event.input,
                  status: 'running',
                },
              },
            });
          }
        }
      }),
    }),
    updateToolResult: assign({
      tools: ({ context, event }) => produce(context.tools, draft => {
        if (event.type === 'tool-result') {
          // Update status and content of the tool
          draft.forEach(tool => {
            if (event.toolUseId in tool.tools) {
              tool.tools[event.toolUseId].status = event.status;
              tool.tools[event.toolUseId].content = event.content;
            }
          });
        }
      }),
    }),
    close: assign({
      tools: () => ([]),
    }),
  },
}).createMachine({
  context: {
    tools: [],
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
        'thought': {
          actions: 'updateThought',
        },
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
