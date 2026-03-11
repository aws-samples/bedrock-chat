import React from 'react';
import { BaseProps } from '../@types/common';
import { twMerge } from 'tailwind-merge';

type Props = BaseProps;

const Skeleton: React.FC<Props> = (props) => {
  return (
    <div
      className={twMerge(
        'relative h-4 w-2/3 overflow-hidden rounded-md bg-aws-font-color-light/10 dark:bg-aws-font-color-dark/10',
        props.className
      )}>
      <div className="skeleton-shimmer absolute inset-0" />
    </div>
  );
};

export default Skeleton;
