import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { TextInputChatContent } from './TextInputChatContent';
import { AvailableTools } from './AvailableTools';
import { AgentTool } from '../types';
import ToolCard from './ToolCard';
import AgentToolList from './AgentToolList';
import { AgentToolState } from '../xstates/agentThink';

export const InputChatContent = () => (
  <TextInputChatContent
    canRegenerate={false}
    isLoading={false}
    onSend={() => {}}
    onRegenerate={() => {}}
  />
);

export const InputChatContentLoading = () => (
  <TextInputChatContent
    disabledSend={true}
    disabledRegenerate={true}
    canRegenerate={false}
    isLoading={true}
    onSend={() => {}}
    onRegenerate={() => {}}
  />
);

export const InputChatContentDisabled = () => {
  const { t } = useTranslation();
  return (
    <TextInputChatContent
      canRegenerate={false}
      isLoading={false}
      disabled={true}
      placeholder={t('bot.label.notAvailableBotInputMessage')}
      onSend={() => {}}
      onRegenerate={() => {}}
    />
  );
};

export const InputChatContentWithRegenerate = () => (
  <TextInputChatContent
    canRegenerate={true}
    isLoading={false}
    onSend={() => {}}
    onRegenerate={() => {}}
  />
);

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
    content={{ text: 'some data' }}
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

export const ToolCardList = () => {
  const tools = {
    tool1: {
      name: 'internet_search',
      status: 'running' as AgentToolState,
      input: { country: 'jp-jp', query: '東京 天気', time_limit: 'd' },
    },
    tool2: {
      name: 'database_query',
      status: 'success' as AgentToolState,
      input: { query: 'SELECT * FROM table' },
      // Pass the content as stringified JSON
      content: { text: '{"result": "success", "data": "some data"}' },
    },
    tool4: {
      name: 'API Call',
      status: 'error' as AgentToolState,
      input: { country: 'jp-jp', query: '東京 天気', time_limit: 'd' },
      // Pass the content as simple string
      content: { text: 'Error! Connection Timeout' },
    },
  };

  return <AgentToolList tools={tools} isRunning={true} />;
};
