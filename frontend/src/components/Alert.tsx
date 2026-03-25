import React, { useMemo } from 'react';
import { BaseProps } from '../@types/common';
import { PiInfo, PiWarningCircleFill, PiWarningFill } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';

type Props = BaseProps & {
  severity: 'info' | 'warning' | 'error';
  title?: string;
  children: React.ReactNode;
};

const Alert: React.FC<Props> = (props) => {
  const icon = useMemo(() => {
    switch (props.severity) {
      case 'info':
        return <PiInfo className="text-xl" />;
      case 'warning':
        return <PiWarningFill className="text-xl" />;
      case 'error':
        return <PiWarningCircleFill className="text-xl" />;
    }
  }, [props.severity]);

  return (
    <div
      className={twMerge(
        'flex flex-col rounded-xl border text-sm',
        props.severity === 'info' && 'border-aa-blue-4/30 bg-aa-blue-5/30 text-aa-blue-2 dark:border-aa-blue-3/20 dark:bg-aa-blue-1/20 dark:text-aa-blue-4',
        props.severity === 'warning' && 'border-yellow/30 bg-light-yellow/50 text-yellow dark:border-yellow/20 dark:bg-yellow/10',
        props.severity === 'error' && 'border-red/30 bg-light-red/50 text-red dark:border-red/20 dark:bg-red/10',
        props.className
      )}>
      {props.title && (
        <div className="flex items-center gap-2 px-3 pt-3 font-semibold tracking-tight">
          {icon}
          <div>{props.title}</div>
        </div>
      )}

      <div className="px-3 py-2.5">
        {props.children}
      </div>
    </div>
  );
};

export default Alert;
