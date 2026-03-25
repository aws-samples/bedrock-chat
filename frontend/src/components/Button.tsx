import React, { forwardRef } from 'react';
import { BaseProps } from '../@types/common';
import { PiSpinnerGap } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';

type Props = BaseProps & {
  icon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  disabled?: boolean;
  text?: boolean;
  outlined?: boolean;
  loading?: boolean;
  onClick: () => void;
  children: React.ReactNode;
};

const Button = forwardRef<HTMLButtonElement, Props>((props, ref) => {
  return (
    <button
      ref={ref}
      className={twMerge(
        'flex items-center justify-center whitespace-nowrap rounded-lg border px-3 py-1.5 text-sm font-medium tracking-tight transition-all duration-200',
        props.text && 'border-0 dark:text-aws-font-color-dark',
        props.outlined && 'border-black/10 bg-white hover:bg-black/[0.03] dark:border-white/10 dark:bg-transparent dark:text-aws-font-color-dark dark:hover:bg-white/[0.05]',
        !props.text &&
          !props.outlined &&
          'border-transparent bg-aws-sea-blue-light text-white shadow-sm hover:bg-aws-sea-blue-hover-light dark:bg-white/10 dark:text-aws-font-color-white-dark dark:hover:bg-white/15',
        props.disabled || props.loading ? 'opacity-30 cursor-not-allowed' : '',
        props.className
      )}
      onClick={(e) => {
        e.stopPropagation();
        e.preventDefault();
        props.onClick();
      }}
      disabled={props.disabled || props.loading}>
      {props.icon && !props.loading && (
        <div className="-ml-0.5 mr-2">{props.icon}</div>
      )}
      {props.loading && <PiSpinnerGap className="-ml-0.5 mr-2 animate-spin" />}
      {props.children}
      {props.rightIcon && <div className="ml-2">{props.rightIcon}</div>}
    </button>
  );
});

export default Button;
