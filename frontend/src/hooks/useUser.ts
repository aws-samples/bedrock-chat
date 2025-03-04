import { fetchAuthSession } from 'aws-amplify/auth';
import { useEffect, useState } from 'react';
import useSWR from 'swr';

const GROUP_PUBLISH_ALLOWED = 'PublishAllowed';
const GROUP_CREATING_BOT_ALLOWED = 'CreatingBotAllowed';
const GROUP_ADMIN = 'Admin';

const useUser = () => {
  const [isAllowApiSettings, setIsAllowApiSettings] = useState(false);
  const [isAllowCreatingBot, setIsAllowCreatingBot] = useState(false);
  const [emailId, setEmailId] = useState('');

  const { data: session } = useSWR('current-session', () =>
    fetchAuthSession()
  );

  useEffect(() => {
    const groups = session?.tokens?.idToken?.payload?.['cognito:groups'];
    const emailId = session?.tokens?.signInDetails?.loginId;
    if (emailId) {
      setEmailId(emailId);
    }

    if (Array.isArray(groups)) {
      setIsAllowApiSettings(groups.some(group =>
        group === GROUP_PUBLISH_ALLOWED || group === GROUP_ADMIN
      ));
      setIsAllowCreatingBot(groups.some(group =>
        group === GROUP_CREATING_BOT_ALLOWED || group === GROUP_ADMIN
      ));
    } else {
      setIsAllowApiSettings(false);
      setIsAllowCreatingBot(false);
    }
  }, [session]);
  return {
    isAllowApiSettings,
    isAllowCreatingBot,
    emailId,
  };
};

export default useUser;
