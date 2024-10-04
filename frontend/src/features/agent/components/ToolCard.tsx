import { useTranslation } from 'react-i18next';
import React, { useCallback } from 'react';
import { AgentToolState } from '../xstates/agentThink';
import { JSONTree } from 'react-json-tree';
import {
  PiCaretDown,
  PiCaretUp,
  PiCheckCircle,
  PiCircleNotch,
  PiXCircle,
} from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';
import useToolCardExpand from '../hooks/useToolCardExpand';

// Theme of JSONTree
// NOTE: need to set the theme as base16 style
const THEME = {
  scheme: 'aws',
  author: 'aws',
  base00: '#f1f3f3', // AWS Paper
  base01: '#000000',
  base02: '#000000',
  base03: '#000000',
  base04: '#000000',
  base05: '#000000',
  base06: '#000000',
  base07: '#000000',
  base08: '#000000',
  base09: '#000000',
  base0A: '#000000',
  base0B: '#000000',
  base0C: '#000000',
  base0D: '#000000',
  base0E: '#000000',
  base0F: '#000000',
};

type ToolCardProps = {
  className?: string;
  toolUseId: string;
  name: string;
  status: AgentToolState;
  input: { [key: string]: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
  content?: { text: string };
};

const ToolCard: React.FC<ToolCardProps> = ({
  className,
  toolUseId,
  name,
  status,
  input,
  content,
}) => {
  const { t } = useTranslation();

  // To avoid re-rendering of all ToolCard components when scrolling, we use a custom hook to manage the expanded state.
  const {
    expandedTools,
    inputExpandedTools,
    contentExpandedTools,
    toggleExpand,
    toggleInputExpand,
    toggleContentExpand,
  } = useToolCardExpand();

  const isExpanded = expandedTools[toolUseId] ?? false;
  const isInputExpanded = inputExpandedTools[toolUseId] ?? false;
  const isContentExpanded = contentExpandedTools[toolUseId] ?? false;

  const handleToggleExpand = useCallback(() => {
    toggleExpand(toolUseId);
  }, [toggleExpand, toolUseId]);

  const handleToggleInputExpand = useCallback(() => {
    toggleInputExpand(toolUseId);
  }, [toggleInputExpand, toolUseId]);

  const handleToggleContentExpand = useCallback(() => {
    toggleContentExpand(toolUseId);
  }, [toggleContentExpand, toolUseId]);

  // Convert output content text to JSON object if possible.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let displayContent: any = null;
  if (content?.text) {
    try {
      displayContent = JSON.parse(content.text);
    } catch (e) {
      displayContent = content;
    }
  }

  return (
    <div className={twMerge('relative', className)}>
      <div
        className="flex cursor-pointer items-center justify-between p-2 hover:bg-light-gray"
        onClick={handleToggleExpand}>
        <div className="flex items-center text-base">
          {status === 'running' && (
            <PiCircleNotch className="mr-2 animate-spin text-aws-aqua" />
          )}
          {status === 'success' && (
            <PiCheckCircle className="mr-2 text-aws-aqua" />
          )}
          {status === 'error' && <PiXCircle className="mr-2  text-red" />}
          <h3 className="">{name}</h3>
        </div>
        <div>
          {isExpanded ? (
            <PiCaretUp className="text-lg" />
          ) : (
            <PiCaretDown className="text-lg" />
          )}
        </div>
      </div>

      <div
        className={twMerge(
          `origin-top overflow-hidden transition-transform duration-200 ease-in-out`,
          isExpanded ? 'max-h-full scale-y-100 px-2 pb-2' : 'max-h-0 scale-y-0'
        )}>
        {input && (
          <div>
            <div
              className="mt-2 flex cursor-pointer items-center text-sm"
              onClick={handleToggleInputExpand}>
              <p className="font-bold">{t('agent.progressCard.toolInput')}</p>
              {isInputExpanded ? (
                <PiCaretDown className="ml-2" />
              ) : (
                <PiCaretUp className="ml-2" />
              )}
            </div>

            <div
              className={twMerge(
                `overflow-hidden transition-all duration-300 ease-in-out`,
                isInputExpanded ? 'max-h-full ' : 'max-h-0'
              )}>
              <div className="ml-4 mt-2 text-sm">
                <ul className="list-disc">
                  {Object.entries(input).map(([key, value]) => (
                    <li key={key}>
                      <span className="font-semibold">{key}:</span> {value}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {(status === 'success' || status === 'error') && displayContent && (
          <div>
            <div
              className="mt-2 flex cursor-pointer items-center text-sm"
              onClick={handleToggleContentExpand}>
              <p className="font-bold">{t('agent.progressCard.toolOutput')}</p>
              {isContentExpanded ? (
                <PiCaretDown className="ml-2" />
              ) : (
                <PiCaretUp className="ml-2" />
              )}
            </div>

            <div
              className={twMerge(
                `overflow-hidden transition-all duration-300 ease-in-out`,
                isContentExpanded ? 'max-h-full' : 'max-h-0'
              )}>
              {displayContent ? (
                <div className="ml-4 mt-2 text-sm">
                  {typeof displayContent === 'object' ? (
                    // Render as JSON tree if the content is an object. Otherwise, render as a string.
                    <JSONTree
                      data={displayContent}
                      theme={THEME}
                      invertTheme={false} // disable dark theme
                    />
                  ) : (
                    <p>{String(displayContent)}</p>
                  )}
                </div>
              ) : null}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ToolCard;
