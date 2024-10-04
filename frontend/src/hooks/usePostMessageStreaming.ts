import { fetchAuthSession } from 'aws-amplify/auth';
import { PostMessageRequest } from '../@types/conversation';
import { create } from 'zustand';
import i18next from 'i18next';
import { AgentEvent } from '../features/agent/xstates/agentThink';
import { PostStreamingStatus } from '../constants';

const WS_ENDPOINT: string = import.meta.env.VITE_APP_WS_ENDPOINT;
const CHUNK_SIZE = 32 * 1024; //32KB

const usePostMessageStreaming = create<{
  post: (params: {
    input: PostMessageRequest;
    hasKnowledge?: boolean;
    dispatch: (completion: string) => void;
    thinkingDispatch: (event: AgentEvent) => void;
  }) => Promise<string>;
}>(() => {
  return {
    post: async ({ input, dispatch, hasKnowledge, thinkingDispatch }) => {
      if (hasKnowledge) {
        dispatch(i18next.t('bot.label.retrievingKnowledge'));
      } else {
        dispatch(i18next.t('app.chatWaitingSymbol'));
      }
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
          ws.send(
            JSON.stringify({
              step: PostStreamingStatus.START,
              token: token,
            })
          );
        };

        ws.onmessage = (message) => {
          try {
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
                  })
                );
              }
              return;
            }

            const data = JSON.parse(message.data);

            if (data.status) {
              switch (data.status) {
                case PostStreamingStatus.FETCHING_KNOWLEDGE:
                  dispatch(i18next.t('bot.label.retrievingKnowledge'));
                  break;
                case PostStreamingStatus.AGENT_THINKING:
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
                    content: data.result.content,
                  });
                  break;
                case PostStreamingStatus.STREAMING:
                  if (data.completion || data.completion === '') {
                    if (
                      completion.endsWith(i18next.t('app.chatWaitingSymbol'))
                    ) {
                      completion = completion.slice(0, -1);
                    }
                    completion +=
                      data.completion + i18next.t('app.chatWaitingSymbol');
                    dispatch(completion);
                  }
                  break;
                case PostStreamingStatus.STREAMING_END:
                  thinkingDispatch({
                    type: 'goodbye',
                  });

                  if (completion.endsWith(i18next.t('app.chatWaitingSymbol'))) {
                    completion = completion.slice(0, -1);
                    dispatch(completion);
                  }
                  ws.close();
                  break;
                case PostStreamingStatus.ERROR:
                  ws.close();
                  console.error(data);
                  throw new Error(i18next.t('error.predict.invalidResponse'));
                default:
                  dispatch(i18next.t('app.chatWaitingSymbol'));
              }
            } else {
              ws.close();
              console.error(data);
              throw new Error(i18next.t('error.predict.invalidResponse'));
            }
          } catch (e) {
            console.error(e);
            reject(i18next.t('error.predict.general'));
          }
        };

        ws.onerror = (e) => {
          ws.close();
          console.error(e);
          reject(i18next.t('error.predict.general'));
        };
        ws.onclose = () => {
          resolve(completion);
        };
      });
    },
  };
});

export default usePostMessageStreaming;
