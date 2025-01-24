import React from 'react';
import { useTranslation } from 'react-i18next';
import { PiSmileyXEyesFill } from 'react-icons/pi';

const ErrorFallback: React.FC = () => {
  const { t } = useTranslation();
  return (
    <div className="flex h-dvh flex-col items-center justify-center bg-aws-paper-light dark:bg-aws-paper-dark">
      <div className="flex text-5xl font-bold dark:text-aws-font-color-dark">
        <PiSmileyXEyesFill />
        ERROR
      </div>
      <div className="mt-4 text-lg dark:text-aws-font-color-dark">{t('error.unexpectedError.title')}</div>
      <button
        className="underline dark:text-aws-font-color-blue dark:hover:text-aws-sea-blue-hover-dark"
        onClick={() => (window.location.href = '/')}>
        {t('error.unexpectedError.restore')}
      </button>
    </div>
  );
};

export default ErrorFallback;
