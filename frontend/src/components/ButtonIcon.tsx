import React from 'react';
import { BaseProps } from '../@types/common';
import { twMerge } from 'tailwind-merge';

type Props = BaseProps & {
  disabled?: boolean;
  onClick: (e: React.MouseEvent) => void;
  children: React.ReactNode;
};

const ButtonIcon: React.FC<Props> = (props) => {
  return (
    <button
      className={twMerge(
        'flex items-center justify-center rounded-lg p-1.5 text-xl transition-all duration-150',
        'hover:bg-black/[0.05] active:scale-95 dark:hover:bg-white/[0.08]',
        'dark:text-aws-font-color-dark',
        props.disabled ? 'opacity-30 cursor-not-allowed' : '',
        props.className
      )}
      onClick={(e) => {
        e.stopPropagation();
        e.preventDefault();
        props.onClick(e);
      }}
      disabled={props.disabled}>
      {props.children}
    </button>
  );
};

export default ButtonIcon;
