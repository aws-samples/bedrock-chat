export type AgentInput = {
  tools: AgentTool[];
};

export type FirecrawlConfig = {
  apiKey: string;
  maxResults: number;
};

export type SearchEngine = 'duckduckgo' | 'firecrawl';
export type ToolType = 'internet' | 'plain' | 'bedrock_agent' | 'mcp';

export type BedrockAgentConfig = {
  agentId: string;
  aliasId: string;
};

export type InternetAgentTool = {
  toolType: 'internet';
  name: string;
  description: string;
  searchEngine: SearchEngine;
  firecrawlConfig?: FirecrawlConfig;
};

export type PlainAgentTool = {
  toolType: 'plain';
  name: string;
  description: string;
};

export type BedrockAgentTool = {
  toolType: 'bedrock_agent';
  name: string;
  description: string;
  bedrockAgentConfig?: BedrockAgentConfig;
};

export type MCPAgentTool = {
  name: string;
  description: string;
  inputSchema: Record<string, any>;
} 

export type MCPServerTools = {
  available: MCPAgentTool[];
  selected: string[];
} 

export type MCPServer = {
  name: string;
  endpoint: string;
  apiKey: string | null;
  secretArn: string | null;
  tools: MCPServerTools;
}

export type MCPConfig = {
  toolType: "mcp";
  name: string;
  description: string;
  mcpServers: MCPServer[];
};

export type AgentTool = InternetAgentTool | PlainAgentTool | BedrockAgentTool | MCPConfig;

export type Agent = {
  tools: AgentTool[];
};
