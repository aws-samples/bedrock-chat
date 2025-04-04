import React from 'react';
import { BaseProps } from '../@types/common';
import { LuTimerReset } from 'react-icons/lu';
import { twMerge } from 'tailwind-merge';
import { useTranslation } from 'react-i18next';

type Props = BaseProps & {
  disabled?: boolean;
  showReasoning: boolean;
  icon?: boolean;
  onToggleReasoning: () => void;
  forceReasoningEnabled?: boolean;
};

const ButtonReasoning: React.FC<Props> = ({
  disabled,
  showReasoning,
  icon,
  onToggleReasoning,
  forceReasoningEnabled = false,
}) => {
  const { t } = useTranslation();
  // Always display as ON when forceReasoningEnabled is true
  const displayShowReasoning = forceReasoningEnabled ? true : showReasoning;
  return (
    <button
      className={twMerge(
        'flex items-center justify-center whitespace-nowrap rounded-lg border',
        displayShowReasoning
          ? 'border-aws-sea-blue-light bg-aws-sea-blue-light/10 text-aws-sea-blue-light dark:border-aws-sea-blue-dark dark:bg-aws-sea-blue-dark/10 dark:text-aws-sea-blue-dark'
          : 'border-aws-font-color-light/20 text-aws-font-color-light/70 dark:border-aws-font-color-dark/20 dark:text-aws-font-color-dark/70',
        icon ? 'p-2 text-xl' : 'p-1 px-3',
        'transition-colors hover:brightness-90',
        disabled ? 'opacity-30 ' : 'cursor-pointer'
      )}
      onClick={(e) => {
        e.stopPropagation();
        e.preventDefault();
        // Only prevent toggle when reasoningEnabled is explicitly set to true in the model
        if (!forceReasoningEnabled) {
          onToggleReasoning();
        }
      }}
      aria-pressed={displayShowReasoning}
      title="Reasoning">
      <LuTimerReset className={icon ? '' : 'mr-2'} />
      {!icon && t('reasoning.button.label')}
    </button>
  );
};

export default ButtonReasoning;
