import React, { HTMLInputTypeAttribute, KeyboardEvent, ReactNode } from 'react';
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
  icon?: ReactNode;
  onChange?: (s: string) => void;
  onKeyDown?: (e: KeyboardEvent<HTMLInputElement>) => void;
};

const InputText = React.forwardRef<HTMLInputElement, Props>((props, ref) => {
  return (
    <div className={twMerge('flex flex-col', props.className)}>
      {props.icon && (
        <div className="relative inline-block">
          <div className="absolute left-2.5 top-2.5 text-lg text-dark-gray dark:text-light-gray">{props.icon}</div>
        </div>
      )}
      <input
        ref={ref}
        type={props.type ?? 'text'}
        className={twMerge(
          'peer h-10 rounded-lg border bg-white px-3 text-sm tracking-tight transition-all duration-200 dark:[color-scheme:dark]',
          'placeholder:text-gray dark:bg-aws-ui-color-dark dark:text-aws-font-color-dark dark:placeholder-aws-font-color-gray',
          'focus:ring-2 focus:ring-aa-purple-3/20 focus:border-aa-purple-3 dark:focus:ring-white/10 dark:focus:border-white/30',
          props.errorMessage
            ? 'border-2 border-red'
            : 'border-black/10 dark:border-white/10',
          props.icon ? 'pl-9' : ''
        )}
        disabled={props.disabled}
        value={props.value}
        placeholder={props.placeholder}
        onChange={(e) => {
          props.onChange ? props.onChange(e.target.value) : null;
        }}
        onKeyDown={props.onKeyDown}
      />

      {props.label && (
        <div
          className={twMerge(
            'order-first mb-1.5 text-[13px] font-medium tracking-tight peer-focus:text-aa-purple-3',
            props.errorMessage
              ? 'font-semibold text-red'
              : 'text-aws-font-color-light dark:text-aws-font-color-dark'
          )}>
          {props.label}
        </div>
      )}
      {props.hint && !props.errorMessage && (
        <div className="mt-1 text-xs text-gray dark:text-aws-font-color-dark">
          {props.hint}
        </div>
      )}
      {props.errorMessage && (
        <div className="mt-1 text-xs text-red">{props.errorMessage}</div>
      )}
    </div>
  );
});

InputText.displayName = 'InputText';

export default InputText;
