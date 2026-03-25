import { FC, Dispatch, ReactNode, useEffect, useState, useCallback } from 'react';
import { twMerge } from 'tailwind-merge';

interface Props {
  label?: ReactNode;
  value: number;
  hint?: string;
  range: {
    min: number;
    max: number;
    step: number;
  };
  onChange: Dispatch<number>;
  disabled?: boolean;
  errorMessage?: string;
  enableDecimal?: boolean;
}

export const Slider: FC<Props> = (props) => {
  const [value, setValue] = useState<string>(String(props.value));

  useEffect(() => {
    setValue(prev => prev === String(props.value) ? prev : String(props.value));
  }, [props.value]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const validateReg = props.enableDecimal ? /^\d*\.?\d*$/ : /^\d*$/;
    const newValStr = e.target.value;

    if (newValStr === '' || validateReg.test(newValStr)) {
      setValue(newValStr);
      const parseNumber = props.enableDecimal ? parseFloat : parseInt;
      const newValue = parseNumber(newValStr !== '' ? newValStr : '0');
      props.onChange(newValue);
    }
  }, [props, setValue]);

  return (
    <div className="flex flex-col">
      <label
        className={twMerge(
          'text-[13px] font-medium tracking-tight text-aws-font-color-light dark:text-aws-font-color-dark',
          props.errorMessage && 'text-red dark:text-red'
        )}>
        {props.label}
      </label>
      <div className="mt-1 flex gap-2">
        <input
          className={twMerge(
            'w-full cursor-pointer accent-aa-purple-3 dark:accent-white',
            props.disabled && 'cursor-default opacity-50'
          )}
          type="range"
          min={props.range.min}
          max={props.range.max}
          step={props.range.step}
          value={props.value}
          onChange={handleChange}
          disabled={props.disabled}
        />
        <input
          className={twMerge(
            'peer h-9 w-16 rounded-lg border bg-white p-1 text-center text-sm transition-all duration-200 dark:bg-aws-ui-color-dark',
            props.errorMessage
              ? 'border-2 border-red dark:text-aws-font-color-dark'
              : 'border-black/10 focus:ring-2 focus:ring-aa-purple-3/20 focus:border-aa-purple-3 dark:border-white/10 dark:text-aws-font-color-dark dark:focus:ring-white/10 dark:focus:border-white/30'
          )}
          value={value}
          max={props.range.max}
          min={props.range.min}
          onChange={handleChange}
          disabled={props.disabled}
        />
      </div>
      {props.hint && !props.errorMessage && (
        <span className="mt-1 text-xs text-gray dark:text-aws-font-color-gray">{props.hint}</span>
      )}
      {props.errorMessage && (
        <div className="mt-1 text-xs text-red">{props.errorMessage}</div>
      )}
    </div>
  );
};
