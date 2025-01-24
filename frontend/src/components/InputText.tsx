import React, { HTMLInputTypeAttribute } from 'react';
import { twMerge } from 'tailwind-merge';

type Props = {
  className?: string;
  label?: string;
  type?: HTMLInputTypeAttribute;
  value: string;
  disabled?: boolean;
  placeholder?: string;
  hint?: string;
  errorMessage?: string;
  onChange?: (s: string) => void;
};

const InputText: React.FC<Props> = (props) => {
  return (
    <div className={twMerge('flex flex-col', props.className)}>
      <input
        type={props.type ?? 'text'}
        className={twMerge(
          'peer h-9 rounded border p-1 dark:[color-scheme:dark]',
          'dark:bg-aws-ui-color-dark dark:placeholder-aws-font-color-gray dark:text-aws-font-color-dark',
          props.errorMessage
            ? 'border-2 border-red'
            : 'border-aws-font-color-light/50 dark:border-aws-font-color-dark/50'
        )}
        disabled={props.disabled}
        value={props.value}
        placeholder={props.placeholder}
        onChange={(e) => {
          props.onChange ? props.onChange(e.target.value) : null;
        }}
      />
      {props.label && (
        <div
          className={twMerge(
            'order-first text-sm peer-focus:font-semibold peer-focus:italic',
            props.errorMessage
              ? 'font-bold text-red'
              : 'text-dark-gray dark:text-light-gray peer-focus:text-aws-font-color-light dark:peer-focus:text-aws-font-color-dark'
          )}>
          {props.label}
        </div>
      )}
      {props.hint && !props.errorMessage && (
        <div className="mt-0.5 text-xs text-gray dark:text-aws-font-color-dark">{props.hint}</div>
      )}
      {props.errorMessage && (
        <div className="mt-0.5 text-xs text-red ">{props.errorMessage}</div>
      )}
    </div>
  );
};

export default InputText;
