import React, {
  ReactNode,
  useState,
  useEffect,
  cloneElement,
  ReactElement,
} from 'react';
import Button from './Button';
import { BaseProps } from '../@types/common';
import { getCurrentUser, signInWithRedirect, signOut } from 'aws-amplify/auth';
import { useTranslation } from 'react-i18next';
import { PiCircleNotch } from 'react-icons/pi';

type Props = BaseProps & {
  children: ReactNode;
};

const AuthCustom: React.FC<Props> = ({ children }) => {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const { t } = useTranslation();

  useEffect(() => {
    getCurrentUser()
      .then(() => {
        setAuthenticated(true);
      })
      .catch(() => {
        setAuthenticated(false);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const handleSignIn = () => {
    signInWithRedirect({
      provider: {
        custom: import.meta.env.VITE_APP_CUSTOM_PROVIDER_NAME,
      },
    });
  };

  const handleSignOut = () => {
    signOut();
  };

  return (
    <>
      {loading ? (
        <div className="flex min-h-screen flex-col items-center justify-center bg-aws-paper-light dark:bg-aws-paper-dark">
          <div className="mb-3 text-xl text-aws-font-color-light dark:text-aws-font-color-dark">
            Loading...
          </div>
          <div className="animate-spin text-aws-squid-ink-light dark:text-white">
            <PiCircleNotch size={48} />
          </div>
        </div>
      ) : !authenticated ? (
        <div className="flex min-h-screen flex-col items-center justify-center bg-aws-paper-light dark:bg-aws-paper-dark">
          <div className="flex w-full max-w-sm flex-col items-center gap-6 rounded-lg bg-white p-10 shadow-md dark:bg-aws-ui-color-dark">
            <div className="text-3xl font-bold text-aws-squid-ink-light dark:text-white">
              {t('app.name')}
            </div>
            <Button onClick={() => handleSignIn()} className="w-full text-lg">
              {t('signIn.button.login')}
            </Button>
          </div>
        </div>
      ) : (
        // Pass the signOut function to the child component
        <>
          {cloneElement(children as ReactElement, { signOut: handleSignOut })}
        </>
      )}
    </>
  );
};

export default AuthCustom;
