export type AgentInput = {
  tools: string[];
};

export type FirecrawlConfig = {
  apiKey: string;
  maxResults: number;
};

export type SearchEngine = 'duckduckgo' | 'firecrawl';
export type ToolType = 'internet' | 'plain' | 'bedrock_agent';

export type BedrockAgentConfig = {
  agentId: string;
  aliasId: string;
};

export type InternetAgentTool = {
  toolType: "internet";
  name: string;
  description: string;
  searchEngine: SearchEngine;
  firecrawlConfig?: FirecrawlConfig;
};

export type PlainAgentTool = {
  toolType: "plain";
  name: string;
  description: string;
};

export type BedrockAgentTool = {
  toolType: "bedrock_agent";
  name: string;
  description: string;
  bedrockAgentConfig?: BedrockAgentConfig;
};

export type AgentTool = InternetAgentTool | PlainAgentTool | BedrockAgentTool;

export type Agent = {
  tools: AgentTool[];
};
