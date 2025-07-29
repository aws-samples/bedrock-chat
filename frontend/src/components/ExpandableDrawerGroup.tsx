import React, { ReactNode, useState } from 'react';
import { PiCaretDown } from 'react-icons/pi';
import { twMerge } from 'tailwind-merge';

type Props = {
  className?: string;
  label: string;
  children: ReactNode;
  isDefaultShow?: boolean;
  icon?: ReactNode;
};

const ExpandableDrawerGroup: React.FC<Props> = ({
  isDefaultShow = true,
  icon,
  ...props
}) => {
  const [isShow, setIsShow] = useState(isDefaultShow);

  return (
    <div className={twMerge(props.className)}>
      <div
        className="flex w-full cursor-pointer items-center transition hover:brightness-75"
        onClick={() => {
          setIsShow(!isShow);
        }}>
        <PiCaretDown className={`mx-1 text-sm ${isShow ? '' : 'rotate-180'}`} />
        {icon && <span className="mr-1">{icon}</span>}
        <div className="italic">{props.label}</div>
      </div>
      <div className="">
        <div
          className={`origin-top transition-all ${
            isShow ? 'visible' : 'h-0 scale-y-0'
          }`}>
          {props.children}
        </div>
      </div>
    </div>
  );
};

export default ExpandableDrawerGroup;
