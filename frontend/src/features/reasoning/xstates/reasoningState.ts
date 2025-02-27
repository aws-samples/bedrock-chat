import { setup, assign } from 'xstate';

export type ReasoningContext = {
  content: string;
};

export type ReasoningEvent =
  | { type: 'start' }
  | { type: 'write'; content: string }
  | { type: 'end' };

export const reasoningState = setup({
  types: {
    context: {} as ReasoningContext,
    events: {} as ReasoningEvent,
  },
  actions: {
    reset: assign({
      content: '',
    }),
    appendContent: assign({
      content: ({ context, event }) =>
        event.type === 'write'
          ? context.content + event.content
          : context.content,
    }),
    clear: assign({
      content: '',
    }),
  },
}).createMachine({
  id: 'reasoning',
  context: {
    content: '',
  },
  initial: 'inactive',
  states: {
    inactive: {
      on: {
        start: {
          actions: 'reset',
          target: 'active',
        },
      },
    },
    active: {
      on: {
        write: {
          actions: 'appendContent',
        },
        end: {
          actions: 'clear',
          target: 'inactive',
        },
      },
    },
  },
});
