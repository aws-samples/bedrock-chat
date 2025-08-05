import { fetchAuthSession } from 'aws-amplify/auth';
import { PostMessageRequest } from '../@types/conversation';
import { create } from 'zustand';
import i18next from 'i18next';
import { AgentEvent } from '../features/agent/xstates/agentThink';
import { PostStreamingStatus } from '../constants';
import { ReasoningEvent } from '../features/reasoning/xstates/reasoningState';

const WS_ENDPOINT: string = import.meta.env.VITE_APP_WS_ENDPOINT;
const CHUNK_SIZE = 32 * 1024; //32KB

const usePostMessageStreaming = create<{
  post: (params: {
    input: PostMessageRequest;
    hasKnowledge?: boolean;
    dispatch: (completion: string) => void;
    thinkingDispatch: (event: AgentEvent) => void;
    reasoningDispatch: (event: ReasoningEvent) => void;
  }) => Promise<string>;
  errorDetail: string | null;
}>((set) => {
  return {
    errorDetail: null,
    post: async ({ input, dispatch, thinkingDispatch, reasoningDispatch }) => {
      const token = (await fetchAuthSession()).tokens?.idToken?.toString();
      const payloadString = JSON.stringify({
        ...input,
        token,
      });

      // chunking
      const chunkedPayloads: string[] = [];
      const chunkCount = Math.ceil(payloadString.length / CHUNK_SIZE);
      for (let i = 0; i < chunkCount; i++) {
        const start = i * CHUNK_SIZE;
        const end = Math.min(start + CHUNK_SIZE, payloadString.length);
        chunkedPayloads.push(payloadString.substring(start, end));
      }

      let receivedCount = 0;
      return new Promise<string>((resolve, reject) => {
        let completion = '';
        const ws = new WebSocket(WS_ENDPOINT);

        ws.onopen = () => {
          console.log('[FRONTEND_WS] WebSocket connection opened');
          ws.send(
            JSON.stringify({
              step: PostStreamingStatus.START,
              token: token,
            })
          );
        };

        ws.onmessage = (message) => {
          try {
            console.log('[FRONTEND_WS] Received message:', message.data);
            if (
              message.data === '' ||
              message.data === 'Message sent.' ||
              // Ignore timeout message from api gateway
              message.data.startsWith(
                '{"message": "Endpoint request timed out",'
              )
            ) {
              return;
            } else if (message.data === 'Session started.') {
              chunkedPayloads.forEach((chunk, index) => {
                ws.send(
                  JSON.stringify({
                    step: PostStreamingStatus.BODY,
                    index,
                    part: chunk,
                  })
                );
              });
              return;
            } else if (message.data === 'Message part received.') {
              receivedCount++;
              if (receivedCount === chunkedPayloads.length) {
                ws.send(
                  JSON.stringify({
                    step: PostStreamingStatus.END,
                    token: token,
                  })
                );
              }
              return;
            }

            const data = JSON.parse(message.data);
            console.log('[FRONTEND_WS] Parsed data:', data);

            if (data.status) {
              console.log('[FRONTEND_WS] Processing status:', data.status);
              switch (data.status) {
                case PostStreamingStatus.AGENT_THINKING:
                  if (completion.length > 0) {
                    dispatch('');
                    thinkingDispatch({
                      type: 'thought',
                      thought: completion,
                    });
                    completion = '';
                  }
                  Object.entries(data.log).forEach(([toolUseId, toolInfo]) => {
                    const typedToolInfo = toolInfo as {
                      name: string;
                      input: { [key: string]: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
                    };
                    thinkingDispatch({
                      type: 'go-on',
                      toolUseId: toolUseId,
                      name: typedToolInfo.name,
                      input: typedToolInfo.input,
                    });
                  });
                  break;
                case PostStreamingStatus.AGENT_TOOL_RESULT:
                  thinkingDispatch({
                    type: 'tool-result',
                    toolUseId: data.result.toolUseId,
                    status: data.result.status,
                  });
                  break;
                case PostStreamingStatus.AGENT_RELATED_DOCUMENT:
                  thinkingDispatch({
                    type: 'related-document',
                    toolUseId: data.result.toolUseId,
                    relatedDocument: data.result.relatedDocument,
                  });
                  break;
                case PostStreamingStatus.REASONING:
                  reasoningDispatch({
                    type: 'write',
                    content: data.completion,
                  });
                  break;
                case PostStreamingStatus.STREAMING:
                  if (data.completion || data.completion === '') {
                    completion += data.completion;
                    dispatch(completion);
                  }
                  break;
                case PostStreamingStatus.STREAMING_END:
                  console.log(
                    '[FRONTEND_WS] Received STREAMING_END, ending thinking state'
                  );
                  try {
                    console.log(
                      '[FRONTEND_WS] Calling thinkingDispatch goodbye'
                    );
                    thinkingDispatch({
                      type: 'goodbye',
                    });
                    console.log(
                      '[FRONTEND_WS] thinkingDispatch goodbye completed'
                    );

                    console.log('[FRONTEND_WS] Calling reasoningDispatch end');
                    reasoningDispatch({ type: 'end' });
                    console.log(
                      '[FRONTEND_WS] reasoningDispatch end completed'
                    );

                    console.log('[FRONTEND_WS] Closing WebSocket');
                    ws.close();
                    console.log('[FRONTEND_WS] WebSocket closed successfully');
                  } catch (error) {
                    console.error(
                      '[FRONTEND_WS] Error in STREAMING_END handling:',
                      error
                    );
                    ws.close();
                  }
                  break;
                case PostStreamingStatus.ERROR:
                  ws.close();
                  console.error(data);
                  set({
                    errorDetail:
                      data.reason || i18next.t('error.predict.invalidResponse'),
                  });
                  throw new Error(
                    data.reason || i18next.t('error.predict.invalidResponse')
                  );
                default:
                  dispatch('');
                  break;
              }
            } else {
              ws.close();
              console.error(data);
              throw new Error(i18next.t('error.predict.invalidResponse'));
            }
          } catch (e) {
            console.error('[FRONTEND_WS] Error in onmessage handler:', e);
            console.error(
              '[FRONTEND_WS] Message data that caused error:',
              message.data
            );
            reject(i18next.t('error.predict.general'));
          }
        };

        ws.onerror = (e) => {
          console.error('[FRONTEND_WS] WebSocket error:', e);
          ws.close();
          reject(i18next.t('error.predict.general'));
        };
        ws.onclose = (event) => {
          console.log(
            '[FRONTEND_WS] WebSocket closed:',
            event.code,
            event.reason
          );
          resolve(completion);
        };
      });
    },
  };
});

export default usePostMessageStreaming;
