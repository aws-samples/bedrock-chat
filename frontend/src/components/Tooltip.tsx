import React from 'react';
import { BaseProps } from '../@types/common';
import { Direction, TooltipDirection } from '../constants';

type Props = BaseProps & {
  message: string;
  direction?: Direction;
  children: React.ReactNode;
};

const Tooltip: React.FC<Props> = (props) => {
  return (
    <div className={`${props.className ?? ''} group relative dark:text-aws-font-color-dark`}>
      <div
        className={`${
          props.direction === TooltipDirection.LEFT ? 'right-0' : ''
        } invisible absolute -top-5 z-50 bg-transparent p-3 pl-5 pt-8 text-xs font-normal text-white opacity-0 transition-all duration-200 group-hover:visible group-hover:opacity-100`}>
        <div className="w-64 rounded-lg border border-white/10 bg-black/80 p-2 shadow-vercel-dark-lg backdrop-blur-md">
          {props.message}
        </div>
      </div>
      {props.children}
    </div>
  );
};

export default Tooltip;
