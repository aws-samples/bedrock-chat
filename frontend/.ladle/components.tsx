import React, { useEffect } from 'react';
import '../src/i18n';
import { GlobalProvider } from '@ladle/react';
import { useLadleContext } from '@ladle/react';
import '../src/index.css';

export const Provider: GlobalProvider = ({ children }) => {
  const { globalState } = useLadleContext();

  useEffect(() => {
    const bodyClass = document.body.classList;

    if (globalState.theme === 'dark') {
      bodyClass.add('dark');
    } else {
      bodyClass.remove('dark');
    }
  }, [globalState.theme]);

  return <>{children}</>;
};
