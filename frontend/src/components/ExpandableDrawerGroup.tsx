import React, { ReactNode, useState } from 'react';

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
  const [isShow] = useState(isDefaultShow);

  return (
    <div className={`${props.className ?? ''}`}>
      <div
        className="flex w-full items-center px-4">
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
