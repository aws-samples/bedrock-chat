import { AgentTool, InternetAgentTool } from '../types';

export const isInternetTool = (tool: AgentTool): tool is InternetAgentTool => 
  tool.toolType === "internet";
