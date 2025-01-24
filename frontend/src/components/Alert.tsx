import React, { useMemo } from 'react';
import { BaseProps } from '../@types/common';
import { PiInfo, PiWarningCircleFill, PiWarningFill } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';

type Props = BaseProps & {
  severity: 'info' | 'warning' | 'error';
  title: string;
  children: React.ReactNode;
};

const Alert: React.FC<Props> = (props) => {
  const icon = useMemo(() => {
    switch (props.severity) {
      case 'info':
        return <PiInfo className="text-2xl" />;
      case 'warning':
        return <PiWarningFill className="text-2xl" />;
      case 'error':
        return <PiWarningCircleFill className="text-2xl" />;
    }
  }, [props.severity]);

  return (
    <div
      className={twMerge(
        'flex flex-col rounded border border-aws-squid-ink-light dark:border-aws-squid-ink-dark shadow-lg',
        props.severity === 'info' && 'bg-aws-aqua',
        props.severity === 'warning' && 'bg-yellow',
        props.severity === 'error' && 'bg-red',
        props.className
      )}>
      <div
        className={twMerge(
          'flex gap-2 p-2 font-bold text-aws-font-color-white-light dark:text-aws-font-color-white-dark'
        )}>
        {icon}
        <div>{props.title}</div>
      </div>

      <div className="px-2 pb-2 text-aws-font-color-white-light dark:text-aws-font-color-white-dark">
        {props.children}
      </div>
    </div>
  );
};

export default Alert;
