import { exists, TFunction } from 'i18next';
import { AgentTool } from '../types';

export const getAgentName = (name: string, t: TFunction) => {
  if (exists(`agent.tools.${name}`)) {
    return t(`agent.tools.${name}.name` as never);
  }

  return name;
};

export const formatDescription = (tool: AgentTool, t: TFunction) => {
  if (exists(`agent.tools.${tool.name}`)) {
    return `${t(`agent.tools.${tool.name}.name` as never)}:${t(
      `agent.tools.${tool.name}.description` as never
    )}`;
  }

  return `${tool.name}:${tool.description}`;
};
