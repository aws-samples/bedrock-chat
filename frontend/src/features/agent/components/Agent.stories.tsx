import { useState } from 'react';
import { AvailableTools } from './AvailableTools';
import { AgentTool } from '../types';
import ToolCard from './ToolCard';
import AgentToolList from './AgentToolList';

export const Tools = () => {
  const availableTools: AgentTool[] = [
    {
      name: 'get_weather',
      description: '',
    },
    {
      name: 'sql_db_query',
      description: '',
    },
    {
      name: 'sql_db_schema',
      description: '',
    },
    {
      name: 'sql_db_list_tables',
      description: '',
    },
    {
      name: 'sql_db_query_checker',
      description: '',
    },
    {
      name: 'internet_search',
      description: '',
    },
    {
      name: 'knowledge_base_tool',
      description: '',
    },
  ];
  const [tools, setTools] = useState<AgentTool[]>([]);
  return (
    <AvailableTools
      availableTools={availableTools}
      tools={tools}
      setTools={setTools}
    />
  );
};

export const ToolCardRunning = () => (
  <ToolCard
    toolUseId="tool1"
    name="internet_search"
    status="running"
    input={{ country: 'jp-jp', query: '東京 天気', time_limit: 'd' }}
  />
);

export const ToolCardSuccess = () => (
  <ToolCard
    toolUseId="tool2"
    name="Database Query"
    status="success"
    input={{ query: 'SELECT * FROM table' }}
    content={[{
      text: 'some data',
    }]}
  />
);

export const ToolCardError = () => (
  <ToolCard
    toolUseId="tool3"
    name="API Call"
    status="error"
    input={{ query: 'SELECT * FROM table' }}
  />
);

export const ToolListRunning = () => {
  return <AgentToolList
    tools={{
      tools: {
        tool1: {
          name: 'internet_search',
          status: 'running',
          input: { country: 'jp-jp', query: '東京 天気', time_limit: 'd' },
        },
        tool2: {
          name: 'database_query',
          status: 'success',
          input: { query: 'SELECT * FROM table' },
          // Pass the content as stringified JSON
          content: [{
            text: '{"result": "success", "data": "some data"}',
          }],
        },
        tool3: {
          name: 'API Call',
          status: 'running',
          input: { country: 'jp-jp', query: '東京 天気', time_limit: 'd' },
        },
      },
    }}
  />;
};

export const ToolList = () => {
  return <AgentToolList
    tools={{
      thought: '東京の天気について以下のことがわかりました。\n- search result 1\n- search result 2\n- search result 3',
      tools: {
        tool1: {
          name: 'internet_search',
          status: 'success',
          input: { country: 'jp-jp', query: '東京 天気', time_limit: 'd' },
          content: [
            {
              text: "search result 1",
            },
            {
              text: "search result 2",
            },
            {
              text: "search result 3",
            },
          ],
        },
        tool2: {
          name: 'database_query',
          status: 'success',
          input: { query: 'SELECT * FROM table' },
          // Pass the content as stringified JSON
          content: [{
            json: {
              result: "success",
              data: "some data",
            },
          }],
        },
        tool3: {
          name: 'API Call',
          status: 'error',
          input: { country: 'jp-jp', query: '東京 天気', time_limit: 'd' },
          // Pass the content as simple string
          content: [{
            text: 'Error! Connection Timeout',
          }],
        },
      },
    }}
  />;
};
