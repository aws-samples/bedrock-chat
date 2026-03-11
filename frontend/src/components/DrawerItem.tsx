import React, { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { twMerge } from 'tailwind-merge';

type Props = {
  className?: string;
  isActive?: boolean;
  isBlur?: boolean;
  to: string;
  icon: ReactNode;
  labelComponent: ReactNode;
  actionComponent?: ReactNode;
  onClick?: () => void;
};

const DrawerItem: React.FC<Props> = (props) => {
  return (
    <Link
      className={twMerge(
        'group mx-1 my-0.5 flex h-9 items-center rounded-lg px-2 transition-colors duration-150',
        (props.isActive ?? true)
          ? 'bg-white/20 text-white'
          : 'text-white/80 hover:bg-white/10 hover:text-white',
        props.className
      )}
      to={props.to}
      onClick={props.onClick}>
      <div className={`flex h-8 max-h-5 w-full items-center justify-start overflow-hidden`}>
        <div className="mr-2 shrink-0 text-base opacity-80">{props.icon}</div>
        <div className="relative flex-1 truncate text-sm">
          {props.labelComponent}
          {(props.isBlur ?? true) && (
            <div
              className={twMerge(
                'absolute inset-y-0 right-0 w-6 bg-gradient-to-l',
                props.isActive
                  ? 'from-white/20'
                  : 'from-aws-squid-ink-light group-hover:from-white/10 dark:from-aws-ui-color-dark'
              )}
            />
          )}
        </div>

        <div className="flex shrink-0">{props.actionComponent}</div>
      </div>
    </Link>
  );
};

export default DrawerItem;
