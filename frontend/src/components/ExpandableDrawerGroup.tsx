import React, { ReactNode, useState } from 'react';
import { PiCaretDown } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';

type Props = {
  className?: string;
  label: string;
  children: ReactNode;
  isDefaultShow?: boolean;
};

const ExpandableDrawerGroup: React.FC<Props> = ({
  isDefaultShow = true,
  ...props
}) => {
  const [isShow, setIsShow] = useState(isDefaultShow);

  return (
    <div className={twMerge(props.className)}>
      <div
        className="flex w-full cursor-pointer items-center px-3 py-1.5 transition-colors duration-150 hover:bg-white/5"
        onClick={() => {
          setIsShow(!isShow);
        }}>
        <PiCaretDown
          className={twMerge(
            'mr-1.5 text-xs text-white/40 transition-transform duration-200',
            isShow ? '' : '-rotate-90'
          )}
        />
        <div className="text-[11px] font-semibold uppercase tracking-wider text-white/40">
          {props.label}
        </div>
      </div>
      <div
        className={twMerge(
          'origin-top transition-all duration-200',
          isShow ? 'visible opacity-100' : 'h-0 scale-y-0 opacity-0'
        )}>
        {props.children}
      </div>
    </div>
  );
};

export default ExpandableDrawerGroup;
