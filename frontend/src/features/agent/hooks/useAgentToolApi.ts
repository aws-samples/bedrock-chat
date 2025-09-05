import useHttp from '../../../hooks/useHttp';
import { AgentTool } from '../types';

export const useAgentApi = () => {
  const http = useHttp();
  return {
    availableTools: (botId: string) =>
      http.getOnce<AgentTool[]>(`/bot/${botId}/agent/available-tools`),
  };
};
