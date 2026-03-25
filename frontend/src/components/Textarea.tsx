import { forwardRef, useEffect, useRef, useState } from 'react';
import { BaseProps } from '../@types/common';
import { twMerge } from 'tailwind-merge';

type Props = BaseProps & {
  value?: string;
  label?: string;
  placeholder?: string;
  disabled?: boolean;
  hint?: string;
  noBorder?: boolean;
  rows?: number;
  onChange?: (value: string) => void;
};

const MAX_HEIGHT = 300;

const Textarea = forwardRef<HTMLElement, Props>((props, focusInputRef) => {
  const ref = useRef<HTMLTextAreaElement | null>(null);
  const [isMax, setIsMax] = useState(false);

  useEffect(() => {
    if (!ref.current) {
      return;
    }

    ref.current.style.height = 'auto';

    if (ref.current.scrollHeight > MAX_HEIGHT) {
      ref.current.style.height = MAX_HEIGHT + 'px';
      setIsMax(true);
    } else {
      ref.current.style.height = ref.current.scrollHeight + 'px';
      setIsMax(false);
    }
  }, [props.value]);

  return (
    <div className={`${props.className ?? ''} flex w-full flex-col`}>
      <textarea
        ref={element => {
          ref.current = element;
          if (focusInputRef) {
            if (typeof focusInputRef === 'function') {
              focusInputRef(element);
            } else {
              focusInputRef.current = element;
            }
          }
        }}
        className={twMerge(
          'peer w-full resize-none rounded-lg p-2 text-sm tracking-tight outline-none transition-all duration-200',
          'dark:bg-aws-ui-color-dark dark:placeholder-aws-font-color-gray',
          isMax ? 'overflow-y-auto' : 'overflow-hidden',
          props.noBorder
            ? ''
            : 'border border-black/10 bg-white focus:ring-2 focus:ring-aa-purple-3/20 focus:border-aa-purple-3 dark:border-white/10 dark:focus:ring-white/10 dark:focus:border-white/30',
          props.className
        )}
        rows={props.rows ?? 1}
        placeholder={props.placeholder}
        disabled={props.disabled}
        value={props.value}
        onChange={(e) => {
          props.onChange ? props.onChange(e.target.value) : null;
        }}
      />
      {props.label && (
        <div className="order-first mb-1.5 text-[13px] font-medium tracking-tight text-aws-font-color-light peer-focus:text-aa-purple-3 dark:text-aws-font-color-dark">
          {props.label}
        </div>
      )}
      {props.hint && (
        <div className="mt-1 text-xs text-gray dark:text-aws-font-color-dark">{props.hint}</div>
      )}
    </div>
  );
});

export default Textarea;
