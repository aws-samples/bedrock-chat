import React from 'react';
import ToolCard from './ToolCard';
import ChatMessageMarkdown from '../../../components/ChatMessageMarkdown';
import { AgentToolsProps } from '../xstates/agentThink';
import { useTranslation } from 'react-i18next';
import { PiCircleNotchBold } from 'react-icons/pi';
import { getAgentName } from '../functions/formatDescription';

type AgentToolListProps = {
  tools: AgentToolsProps;
};

const AgentToolList: React.FC<AgentToolListProps> = ({tools}) => {
  const { t } = useTranslation();
  const isRunning = (
    Object.keys(tools.tools).length === 0 ||
    Object.values(tools.tools).some(tool => tool.status === 'running')
  );
  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col rounded border border-gray bg-aws-paper text-aws-font-color/80">
      {(isRunning || tools.thought) && (
        <div className="flex items-center border-b border-gray p-2 last:border-b-0">
          {isRunning && <PiCircleNotchBold className="mr-2 animate-spin" />}
          {tools.thought ? (
            <ChatMessageMarkdown messageId="">
              {tools.thought}
            </ChatMessageMarkdown>
          ) : t('agent.progress.label')}
        </div>
      )}

      {Object.entries(tools.tools).map(([toolUseId, toolUse]) => (
        <ToolCard
          className=" border-b border-gray last:border-b-0"
          key={toolUseId}
          toolUseId={toolUseId}
          name={getAgentName(toolUse.name, t)}
          status={toolUse.status}
          input={toolUse.input}
          content={toolUse.content}
        />
      ))}
    </div>
  );
};

export default AgentToolList;
