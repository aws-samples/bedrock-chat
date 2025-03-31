import { AgentTool, InternetAgentTool, BedrockAgentTool } from '../types';

export const isInternetTool = (tool: AgentTool): tool is InternetAgentTool => 
  tool.toolType === "internet";

export const isBedrockAgentTool = (tool: AgentTool): tool is BedrockAgentTool =>
  tool.toolType === "bedrock_agent";
