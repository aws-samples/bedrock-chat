import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { PiCaretDown, PiCaretUp, PiBrain } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';

type ReasoningCardProps = {
  className?: string;
  content: string;
};

const ReasoningCard: React.FC<ReasoningCardProps> = ({
  className,
  content,
}) => {
  const { t } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className={twMerge('relative', className)}>
      <div
        className="flex cursor-pointer items-center justify-between p-2 hover:bg-light-gray dark:text-aws-font-color-dark dark:hover:bg-aws-font-color-dark/10"
        onClick={() => setIsExpanded(!isExpanded)}>
        <div className="flex items-center text-base">
          <PiBrain className="mr-2 text-aws-aqua" />
          {t('reasoning.card.label')}
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
          'origin-top overflow-hidden transition-transform duration-200 ease-in-out',
          isExpanded ? 'max-h-full scale-y-100 px-1 pb-1' : 'max-h-0 scale-y-0'
        )}>
        <div className="mt-0 whitespace-pre-wrap break-all rounded-md p-3 text-sm italic leading-relaxed text-aws-squid-ink-light/90 dark:text-aws-font-color-dark/90">
          {content}
        </div>
      </div>
    </div>
  );
};

export default ReasoningCard;
