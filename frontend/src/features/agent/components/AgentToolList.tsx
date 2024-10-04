import React from 'react';
import ToolCard from './ToolCard';
import { AgentToolsProps } from '../xstates/agentThink';
import { useTranslation } from 'react-i18next';
import { PiCircleNotchBold } from 'react-icons/pi';

type AgentToolListProps = {
  tools: AgentToolsProps;
  isRunning: boolean;
};

const AgentToolList: React.FC<AgentToolListProps> = ({ tools, isRunning }) => {
  const { t } = useTranslation();
  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col rounded border border-gray bg-aws-paper text-aws-font-color/80">
      {isRunning && (
        <div className="flex items-center border-b border-gray p-2 last:border-b-0">
          <PiCircleNotchBold className="mr-2 animate-spin" />
          {t('agent.progress.label')}
        </div>
      )}

      {Object.keys(tools).map((toolUseId) => (
        <ToolCard
          className=" border-b border-gray last:border-b-0"
          key={toolUseId}
          toolUseId={toolUseId}
          name={tools[toolUseId].name}
          status={tools[toolUseId].status}
          input={tools[toolUseId].input}
          content={tools[toolUseId].content}
        />
      ))}
    </div>
  );
};

export default AgentToolList;
