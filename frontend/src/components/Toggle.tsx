import React from 'react';
import { twMerge } from 'tailwind-merge';

type Props = {
  className?: string;
  label?: string;
  value: boolean;
  disabled?: boolean;
  hint?: string;
  onChange?: (b: boolean) => void;
};

const Toggle: React.FC<Props> = (props) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.stopPropagation();
    if (props.onChange) {
      props.onChange(!props.value);
    }
  };

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
  };

  return (
    <div className={twMerge('my-2 flex flex-col pr-3', props.className)}>
      <label
        className={twMerge(
          'relative inline-flex items-center',
          props.disabled ? '' : 'cursor-pointer'
        )}
        onClick={handleClick}>
        <input
          type="checkbox"
          className="peer sr-only"
          checked={props.value}
          disabled={props.disabled}
          onChange={handleChange}
        />
        <div
          className={twMerge(
            "peer h-5 w-9 rounded-full bg-black/10 transition-all duration-200 after:absolute after:start-[2px] after:top-[2px] after:h-4 after:w-4 after:rounded-full after:bg-white after:shadow-sm after:transition-all after:content-[''] peer-checked:bg-aa-purple-3 peer-checked:after:translate-x-full dark:bg-white/20 dark:after:bg-white dark:peer-checked:bg-white/80 dark:peer-checked:after:bg-black rtl:peer-checked:after:-translate-x-full",
            props.disabled ? 'opacity-20' : ''
          )}></div>
        {props.label && (
          <div className="ml-2">
            <div className="text-sm tracking-tight">{props.label}</div>
          </div>
        )}
      </label>
      {props.hint && (
        <div className="ml-11 w-full pl-2 text-xs text-gray dark:text-aws-font-color-dark">
          {props.hint}
        </div>
      )}
    </div>
  );
};

export default Toggle;
