import { useEffect, useState } from 'react';
import { useAgentApi } from './useAgentToolApi';
import { AgentTool } from '../types';

export const useAgent = (botId: string) => {
  const api = useAgentApi();
  const [availableTools, setAvailableTools] = useState<AgentTool[]>();
  const getAvailableTools = async (botId: string) => await api.availableTools(botId);

  useEffect(() => {
    getAvailableTools(botId).then((res) => setAvailableTools(() => res.data));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    availableTools,
  };
};
