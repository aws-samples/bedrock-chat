import { setup, assign } from 'xstate';
import { produce } from 'immer';
import { AgentToolResultContent, RelatedDocument } from '../../../@types/conversation';

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
  resultContents?: AgentToolResultContent[];
  relatedDocuments?: RelatedDocument[];
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
    }
  | {
      type: 'related-document';
      toolUseId: string;
      relatedDocument: RelatedDocument;
    }
  | { type: 'goodbye' };

export type AgentEventKeys = AgentEvent['type'];

export const agentThinkingState = setup({
  types: {
    context: {} as {
      tools: AgentToolsProps[];
      relatedDocuments: RelatedDocument[];
    },
    events: {} as AgentEvent,
  },
  actions: {
    reset: assign({
      tools: [],
      relatedDocuments: [],
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
          // Update status of the tool
          const tool = draft.find(tool => event.toolUseId in tool.tools);
          if (tool != null) {
            tool.tools[event.toolUseId].status = event.status;
          }
        }
      }),
    }),
    addRelatedDocument: assign(({ context, event }) => produce(context, draft => {
      if (event.type === 'related-document') {
        // Add related document of the tool
        const tool = draft.tools.find(tool => event.toolUseId in tool.tools);
        if (tool != null) {
          const toolUse = tool.tools[event.toolUseId];
          if (toolUse.relatedDocuments == null) {
            toolUse.relatedDocuments = [event.relatedDocument];
          } else {
            toolUse.relatedDocuments.push(event.relatedDocument);
          }
        }
        draft.relatedDocuments.push(event.relatedDocument);
      }
    })),
    close: assign({
      tools: [],
      relatedDocuments: [],
    }),
  },
}).createMachine({
  context: {
    tools: [],
    relatedDocuments: [],
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
        'related-document': {
          actions: ['addRelatedDocument'],
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
