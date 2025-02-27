import ButtonReasoning from './ButtonReasoning';
import { useState } from 'react';

export const Default = () => {
  const [showReasoning, setShowReasoning] = useState(false);
  return (
    <ButtonReasoning
      showReasoning={showReasoning}
      onToggleReasoning={() => setShowReasoning(!showReasoning)}
    />
  );
};

export const IconOnly = () => {
  const [showReasoning, setShowReasoning] = useState(false);
  return (
    <ButtonReasoning
      icon
      showReasoning={showReasoning}
      onToggleReasoning={() => setShowReasoning(!showReasoning)}
    />
  );
};
