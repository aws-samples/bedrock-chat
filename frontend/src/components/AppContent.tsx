import React, { useCallback, useEffect, useState } from 'react';
import ChatListDrawer from './ChatListDrawer';
import { BaseProps } from '../@types/common';
import { ConversationMeta } from '../@types/conversation';
import LazyOutputText from './LazyOutputText';
import { PiList, PiPlus } from 'react-icons/pi';
import ButtonIcon from './ButtonIcon';
import SnackbarProvider from '../providers/SnackbarProvider';
import { Outlet } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams } from 'react-router-dom';
import useDrawer from '../hooks/useDrawer';
import useConversation from '../hooks/useConversation';
import useBot from '../hooks/useBot';
import useChat from '../hooks/useChat';
import { usePageLabel, usePageTitlePathPattern } from '../routes';
import useUser from '../hooks/useUser';
import DialogConfirmDeleteChat from './DialogConfirmDeleteChat';
import DialogConfirmClearConversations from './DialogConfirmClearConversations';
import DialogSelectLanguage from './DialogSelectLanguage';
import useLocalStorage from '../hooks/useLocalStorage';

type Props = BaseProps & {
  signOut?: () => void;
};

const AppContent: React.FC<Props> = (props) => {
  const { i18n } = useTranslation();
  const { getPageLabel } = usePageLabel();
  const { switchOpen: switchDrawer } = useDrawer();
  const navigate = useNavigate();
  const { conversationId } = useParams();
  const { conversations, getTitle, updateTitle, deleteConversation, clearConversations: clear } = useConversation();
  const { starredBots, recentlyUsedUnsterredBots } = useBot();
  const { newChat, isGeneratedTitle } = useChat();
  const { isConversationOrNewChat, pathPattern } = usePageTitlePathPattern();
  const { isAdmin } = useUser();
  const [theme] = useLocalStorage(
    'theme',
    'light'
  );
  useEffect(() => {
    document.documentElement.className = theme;
  }, [theme]);

  const onClickNewChat = useCallback(() => {
    navigate('/');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const [isOpenDeleteChat, setIsOpenDeleteChat] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<
    ConversationMeta | undefined
  >();

  const deleteChat = useCallback(
    (conversationId: string) => {
      deleteConversation(conversationId).then(() => {
        newChat();
        navigate('');
        setIsOpenDeleteChat(false);
        setDeleteTarget(undefined);
      });
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const [isOpenClearConversations, setIsOpenClearConversations] = useState(false);

  const clearConversations = useCallback(
    () => {
      clear().then(() => {
        navigate('');
        setIsOpenClearConversations(false);
      });
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const [isOpenSelectLangage, setIsOpenSelectLangage] = useState(false);

  return (
    <div className="relative flex h-dvh w-screen bg-aws-paper-light dark:bg-aws-paper-dark">
      <ChatListDrawer
        isAdmin={isAdmin}
        conversations={conversations}
        starredBots={starredBots}
        recentlyUsedUnsterredBots={recentlyUsedUnsterredBots}
        updateConversationTitle={async (conversationId, title) => {
          await updateTitle(conversationId, title);
        }}
        onSignOut={() => {
          props.signOut ? props.signOut() : null;
        }}
        onDeleteConversation={(conversation) => {
          setIsOpenDeleteChat(true);
          setDeleteTarget(conversation);
        }}
        onClearConversations={() => setIsOpenClearConversations(true)}
        onSelectLanguage={() => setIsOpenSelectLangage(true)}
      />
      <DialogConfirmDeleteChat
        isOpen={isOpenDeleteChat}
        target={deleteTarget}
        onDelete={deleteChat}
        onClose={() => setIsOpenDeleteChat(false)}
      />
      <DialogConfirmClearConversations
        isOpen={isOpenClearConversations}
        onClose={() => {
          setIsOpenClearConversations(false);
        }}
        onDelete={clearConversations}
      />
      <DialogSelectLanguage
        isOpen={isOpenSelectLangage}
        initialLanguage={i18n.language}
        onSelectLanguage={(language) => {
          i18n.changeLanguage(language);
          setIsOpenSelectLangage(false);
        }}
        onClose={() => {
          setIsOpenSelectLangage(false);
        }}
      />

      <main className="min-h-dvh relative flex flex-col flex-1 overflow-y-hidden transition-width">

        <header className="visible flex h-12 w-full items-center bg-aws-squid-ink-light dark:bg-aws-squid-ink-dark p-3 text-lg text-aws-font-color-white-light dark:text-aws-font-color-white-dark lg:hidden lg:h-0">
          <button
            className="mr-2 rounded-full p-2 hover:brightness-50 focus:outline-none focus:ring-1 "
            onClick={() => {
              switchDrawer();
            }}>
            <PiList />
          </button>

          <div className="flex-1 justify-center">
            {isGeneratedTitle ? (
              <>
                <LazyOutputText text={getTitle(conversationId ?? '')} />
              </>
            ) : (
              <>
                {isConversationOrNewChat
                  ? getTitle(conversationId ?? '')
                  : getPageLabel(pathPattern)}
              </>
            )}
          </div>

          <ButtonIcon onClick={onClickNewChat}>
            <PiPlus />
          </ButtonIcon>
        </header>

        <div
          className="h-full overflow-hidden overflow-y-auto  text-aws-font-color-light dark:text-aws-font-color-dark"
          id="main">
          <SnackbarProvider>
            <Outlet />
          </SnackbarProvider>
        </div>
      </main>
    </div>
  );
};

export default AppContent;
