import React, { ReactNode, useState } from 'react';
import { PiCaretDown } from 'react-icons/pi';

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
  
  const isLeftNavBarItem = (label: string) => {
    const lowerStr = label.toLowerCase();
    return lowerStr.includes("available assistants") || lowerStr.includes("history");
  };


  return (
    <div className={`${props.className ?? ''}`}>
      <div
        className="flex w-full items-center px-4" onClick={() => {
          setIsShow(!isShow);
        }}>
          {!isLeftNavBarItem(props.label) && <PiCaretDown className={`mx-1 text-sm ${isShow ? '' : 'rotate-180'}`} />}
        <div className="bold">{props.label}</div>
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
