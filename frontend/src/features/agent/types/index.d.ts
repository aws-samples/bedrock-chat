export type AgentInput = {
  tools: string[];
};

export type FirecrawlConfig = {
  apiKey: string;
  maxResults: number;
};

export type SearchEngine = 'duckduckgo' | 'firecrawl';
export type ToolType = 'internet' | 'plain';

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

export type AgentTool = InternetAgentTool | PlainAgentTool;

export type Agent = {
  tools: AgentTool[];
};
