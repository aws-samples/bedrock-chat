import React from 'react';
import { BaseProps } from '../@types/common';
import { PiGlobe } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';
import { useTranslation } from 'react-i18next';

type Props = BaseProps & {
  disabled?: boolean;
  showInternetSearch: boolean;
  icon?: boolean;
  onToggleInternetSearch: () => void;
};

const ButtonInternetSearch: React.FC<Props> = ({
  disabled,
  showInternetSearch,
  icon,
  onToggleInternetSearch,
}) => {
  const { t } = useTranslation();
  return (
    <button
      className={twMerge(
        'flex items-center justify-center whitespace-nowrap rounded-lg border',
        showInternetSearch
          ? 'border-aws-sea-blue-light bg-aws-sea-blue-light/10 text-aws-sea-blue-light dark:border-aws-sea-blue-dark dark:bg-aws-sea-blue-dark/10 dark:text-aws-sea-blue-dark'
          : 'border-aws-font-color-light/20 text-aws-font-color-light/70 dark:border-aws-font-color-dark/20 dark:text-aws-font-color-dark/70',
        icon ? 'p-2 text-xl' : 'p-1 px-3',
        'transition-colors hover:brightness-90',
        disabled ? 'opacity-30 ' : 'cursor-pointer'
      )}
      onClick={(e) => {
        e.stopPropagation();
        e.preventDefault();
        onToggleInternetSearch();
      }}
      aria-pressed={showInternetSearch}
      title="Internet Search">
      <PiGlobe className={icon ? '' : 'mr-2'} />
      {!icon && t('internetSearch.button.label')}
    </button>
  );
};

export default ButtonInternetSearch;
