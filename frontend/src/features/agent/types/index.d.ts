export type AgentInput = {
  tools: string[];
};

export type FirecrawlConfig = {
  apiKey?: string;
  secretArn?: string;
  maxResults: number;
};

export type SearchEngine = 'duckduckgo' | 'firecrawl';

export type AgentTool = {
  name: string;
  description: string;
  firecrawlConfig?: FirecrawlConfig;
  searchEngine?: SearchEngine;
};

export type Agent = {
  tools: AgentTool[];
};
