import React from 'react';
import { BaseProps } from '../@types/common';
import { twMerge } from 'tailwind-merge';

type Props = BaseProps;

const Skeleton: React.FC<Props> = (props) => {
  return (
    <div
      className={twMerge(
        'relative h-4 w-2/3 overflow-hidden rounded-lg bg-black/[0.04] dark:bg-white/[0.06]',
        props.className
      )}>
      <div className="skeleton-shimmer absolute inset-0" />
    </div>
  );
};

export default Skeleton;
