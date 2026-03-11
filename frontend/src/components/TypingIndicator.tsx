import React from 'react';
import { twMerge } from 'tailwind-merge';
import { BaseProps } from '../@types/common';

type Props = BaseProps;

/**
 * Animated typing indicator — three bouncing dots shown when the AI is
 * composing a response.
 */
const TypingIndicator: React.FC<Props> = ({ className }) => {
  return (
    <div
      className={twMerge(
        'flex items-center gap-1 text-aws-font-color-light/50 dark:text-aws-font-color-dark/50',
        className
      )}
      aria-label="AI is typing">
      <span className="typing-dot" />
      <span className="typing-dot" />
      <span className="typing-dot" />
    </div>
  );
};

export default TypingIndicator;
