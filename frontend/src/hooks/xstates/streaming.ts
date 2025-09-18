import { setup, assign } from 'xstate';
import { produce } from 'immer';

import { AgentToolsProps, AgentToolState } from '../../features/agent/types';
import { RelatedDocument } from '../../@types/conversation';

export const StreamingState = {
  SLEEPING: 'sleeping',
  STREAMING: 'streaming',
  LEAVING: 'leaving',
} as const;

export type StreamingState = (typeof StreamingState)[keyof typeof StreamingState];

export type StreamingContext = {
  /** ReasoningContent in assistant message itself. */
  reasoning: string;
  /** TextContent in assistant message itself. */
  text: string;
  tools: AgentToolsProps[];
  relatedDocuments: RelatedDocument[];
};

export type StreamingEvent =
  | { type: 'wakeup' }
  | {
      type: 'reasoning';
      reasoning: string;
    }
  | {
      type: 'text';
      text: string;
    }
  | {
      type: 'tool-use';
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
  | { type: 'reset' }
  | { type: 'goodbye' };

export const streamingStateMachine = setup({
  types: {
    context: {} as StreamingContext,
    events: {} as StreamingEvent,
  },
  actions: {
    reset: assign({
      reasoning: '',
      tools: [],
      relatedDocuments: [],
    }),
    appendReasoning: assign({
      reasoning: ({ context, event }) =>
        event.type === 'reasoning'
          ? context.reasoning + event.reasoning
          : context.reasoning,
    }),
    appendText: assign({
      text: ({ context, event }) =>
        event.type === 'text'
          ? context.text + event.text
          : context.text,
    }),
    addTool: assign(
      ({ context, event }) => produce(context, draft => {
        if (event.type === 'tool-use') {
          // If reasoing is streamed before the tool arrives, let it be the tool's reasoning.
          const reasoning = draft.reasoning ? draft.reasoning : undefined;
          draft.reasoning = '';

          // If text is streamed before the tool arrives, let it be the tool's thought.
          const text = draft.text ? draft.text : undefined;
          draft.text = '';

          if (draft.tools.length > 0 && text == null && reasoning == null) {
            // If there is no reasoning or thought, simply add the tool.
            draft.tools[draft.tools.length - 1].tools[event.toolUseId] = {
              name: event.name,
              input: event.input,
              status: 'running',
            };
          } else {
            // Otherwise, append the tool with the reasoning or the thought.
            draft.tools.push({
              reasoning: reasoning,
              thought: text,
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
    ),
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
  },
}).createMachine({
  context: {
    reasoning: '',
    text: '',
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
          target: 'streaming',
        },
      },
    },
    streaming: {
      on: {
        reasoning: {
          actions: 'appendReasoning',
        },
        text: {
          actions: 'appendText',
        },
        'tool-use': {
          actions: 'addTool',
        },
        'tool-result': {
          actions: ['updateToolResult'],
        },
        'related-document': {
          actions: ['addRelatedDocument'],
        },
        reset: {
          actions: 'reset',
        },
        goodbye: {
          actions: 'reset',
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
