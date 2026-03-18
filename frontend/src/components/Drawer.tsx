import React, {
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { BaseProps } from '../@types/common';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import useDrawer from '../hooks/useDrawer';
import ButtonIcon from './ButtonIcon';
import {
  PiArrowRight,
  PiChartLine,
  PiChat,
  PiChatCenteredDotsDuotone,
  PiCheck,
  PiCompass,
  PiListBullets,
  PiNotePencil,
  PiPencilLine,
  PiPlugs,
  PiPresentationChart,
  PiRobot,
  PiTrash,
  PiUsers,
  PiX,
} from 'react-icons/pi';
import LazyOutputText from './LazyOutputText';
import { ConversationMeta } from '../@types/conversation';
import { BotListItem } from '../@types/bot';
import { isMobile } from 'react-device-detect';
import useChat from '../hooks/useChat';
import { useTranslation } from 'react-i18next';
import Menu from './Menu';
import DrawerItem from './DrawerItem';
import ExpandableDrawerGroup from './ExpandableDrawerGroup';
import { usePageLabel } from '../routes';
import { twMerge } from 'tailwind-merge';
import Button from './Button';
import Skeleton from './Skeleton';
import { isPinnedBot } from '../utils/BotUtils';
import IconPinnedBot from './IconPinnedBot';
import useGlobalConfig from '../hooks/useGlobalConfig';

type Props = BaseProps & {
  isAdmin: boolean;
  conversations?: ConversationMeta[];
  pinnedBots?: BotListItem[];
  starredBots?: BotListItem[];
  recentlyUsedUnstarredBots?: BotListItem[];
  updateConversationTitle: (
    conversationId: string,
    title: string
  ) => Promise<void>;
  onSignOut: () => void;
  onDeleteConversation: (conversation: ConversationMeta) => void;
  onClearConversations: () => void;
  onSelectLanguage: () => void;
  onClickDrawerOptions: () => void;
};

type ItemProps = BaseProps & {
  label: string;
  conversationId: string;
  generatedTitle?: boolean;
  updateTitle: (conversationId: string, title: string) => Promise<void>;
  onClick: () => void;
  onDelete: () => void;
};

const Item: React.FC<ItemProps> = (props) => {
  const { pathname } = useLocation();
  const { conversationId: pathParam } = useParams();
  const { conversationId } = useChat();
  const [tempLabel, setTempLabel] = useState('');
  const [editing, setEditing] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);

  const active = useMemo<boolean>(() => {
    return (
      pathParam === props.conversationId ||
      ((pathname === '/' || pathname.startsWith('/bot/')) &&
        conversationId == props.conversationId)
    );
  }, [conversationId, pathParam, pathname, props.conversationId]);

  const onClickEdit = useCallback(() => {
    setEditing(true);
    setTempLabel(props.label);
  }, [props.label]);

  const onClickUpdate = useCallback(() => {
    props.updateTitle(props.conversationId, tempLabel).then(() => {
      setEditing(false);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tempLabel, props.conversationId, props.updateTitle]);

  const onClickDelete = useCallback(() => {
    props.onDelete();
  }, [props]);

  useLayoutEffect(() => {
    if (editing) {
      inputRef.current?.focus();
    }
  }, [editing]);

  useLayoutEffect(() => {
    if (editing) {
      const listener = (e: DocumentEventMap['keypress']) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();

          // dispatch 処理の中で Title の更新を行う（同期を取るため）
          setTempLabel((newLabel) => {
            props.updateTitle(props.conversationId, newLabel).then(() => {
              setEditing(false);
            });
            return newLabel;
          });
        }
      };
      inputRef.current?.addEventListener('keypress', listener);

      inputRef.current?.focus();

      return () => {
        // eslint-disable-next-line react-hooks/exhaustive-deps
        inputRef.current?.removeEventListener('keypress', listener);
      };
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [editing]);

  return (
    <DrawerItem
      isActive={active}
      isBlur={!editing}
      to={`/${props.conversationId}`}
      onClick={props.onClick}
      icon={<PiChat />}
      labelComponent={
        <>
          {editing ? (
            <input
              ref={inputRef}
              type="text"
              className="w-full bg-transparent"
              value={tempLabel}
              onChange={(e) => {
                setTempLabel(e.target.value);
              }}
            />
          ) : (
            <>
              {props.generatedTitle ? (
                <LazyOutputText text={props.label} />
              ) : (
                <>{props.label}</>
              )}
            </>
          )}
        </>
      }
      actionComponent={
        <>
          {active && !editing && (
            <>
              <ButtonIcon className="text-base" onClick={onClickEdit}>
                <PiPencilLine />
              </ButtonIcon>

              <ButtonIcon className="text-base" onClick={onClickDelete}>
                <PiTrash />
              </ButtonIcon>
            </>
          )}
          {editing && (
            <>
              <ButtonIcon className="text-base" onClick={onClickUpdate}>
                <PiCheck />
              </ButtonIcon>

              <ButtonIcon
                className="text-base"
                onClick={() => {
                  setEditing(false);
                }}>
                <PiX />
              </ButtonIcon>
            </>
          )}
        </>
      }
    />
  );
};

const Drawer: React.FC<Props> = (props) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { getPageLabel } = usePageLabel();
  const { opened, switchOpen, drawerOptions } = useDrawer();
  const { conversations, pinnedBots, starredBots, recentlyUsedUnstarredBots } = props;

  const location = useLocation();

  const [prevConversations, setPrevConversations] =
    useState<typeof conversations>();
  const [generateTitleIndex, setGenerateTitleIndex] = useState(-1);

  const { newChat, conversationId } = useChat();
  const { botId } = useParams();
  const { getGlobalConfig } = useGlobalConfig();
  const { data: globalConfig } = getGlobalConfig();
  const logoSrc = globalConfig?.logoPath ?? '';

  useEffect(() => {
    setPrevConversations(conversations);
  }, [conversations]);

  useEffect(() => {
    // 新規チャットの場合はTitleをLazy表示にする
    if (!conversations || !prevConversations) {
      return;
    }
    if (conversations.length > prevConversations?.length) {
      setGenerateTitleIndex(
        conversations?.findIndex(
          (c) =>
            (prevConversations?.findIndex((pc) => c.id === pc.id) ?? -1) < 0
        ) ?? -1
      );
    }
  }, [conversations, prevConversations]);

  const onClickNewChat = useCallback(() => {
    newChat();
    closeSmallDrawer();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onClickNewBotChat = useCallback(
    () => {
      newChat();
      closeSmallDrawer();
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const smallDrawer = useRef<HTMLDivElement>(null);

  const closeSmallDrawer = useCallback(() => {
    if (smallDrawer.current?.classList.contains('visible')) {
      switchOpen();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onClickLogo = useCallback(() => {
    navigate('/');
    closeSmallDrawer();
  }, [navigate, closeSmallDrawer]);

  useLayoutEffect(() => {
    // リサイズイベントを拾って状態を更新する
    const onResize = () => {
      if (isMobile) {
        return;
      }

      // 狭い画面のDrawerが表示されていて、画面サイズが大きくなったら状態を更新
      if (!smallDrawer.current?.checkVisibility() && opened) {
        switchOpen();
      }
    };
    onResize();

    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [opened]);

  const isAdminPanel = useMemo(() => {
    return location.pathname.startsWith('/admin');
  }, [location.pathname]);

  return (
    <>
      <div className="relative h-full overflow-y-auto bg-aws-squid-ink-light scrollbar-thin scrollbar-track-transparent scrollbar-thumb-white/10 hover:scrollbar-thumb-white/20 dark:bg-aws-ui-color-dark dark:scrollbar-thumb-white/10">
        <nav
          className={`lg:visible lg:w-64 ${
            opened ? 'visible w-64' : 'invisible w-0'
          } text-sm text-white transition-width`}>
          {/* Logo / Header area */}
          <div className="sticky top-0 z-10 flex items-center justify-between border-b border-white/10 bg-aws-squid-ink-light px-3 py-3 dark:bg-aws-ui-color-dark">
            <button
              type="button"
              onClick={onClickLogo}
              className="flex min-w-0 flex-1 items-center gap-2 rounded-lg px-1 py-1 transition-colors hover:bg-white/10 focus:outline-none">
              {logoSrc ? (
                <img
                  src={logoSrc}
                  alt={t('app.name')}
                  className="h-8 w-auto max-w-[140px] shrink-0"
                  loading="lazy"
                />
              ) : (
                <span className="font-heading truncate text-sm font-semibold tracking-wide text-white/90">
                  {t('app.name')}
                </span>
              )}
            </button>
          </div>

          {!isAdminPanel && (
            <>
              {/* Primary nav items */}
              <div className="px-2 pt-2">
                {drawerOptions.show.newChat && (
                  <DrawerItem
                    isActive={false}
                    icon={<PiNotePencil />}
                    to="/"
                    onClick={onClickNewChat}
                    labelComponent={t('button.newChat')}
                  />
                )}
                {drawerOptions.show.myBots && (
                  <DrawerItem
                    isActive={false}
                    icon={<PiListBullets />}
                    to="/bot/my"
                    labelComponent={getPageLabel('/bot/my')}
                    onClick={closeSmallDrawer}
                  />
                )}
                {drawerOptions.show.discoverBots && (
                  <DrawerItem
                    isActive={false}
                    icon={<PiCompass />}
                    to="/bot/discover"
                    labelComponent={getPageLabel('/bot/discover')}
                    onClick={closeSmallDrawer}
                  />
                )}
              </div>

              {drawerOptions.show.pinnedBots &&
                pinnedBots?.filter((bot) => bot.available).length ? (
                  <ExpandableDrawerGroup
                    label={t('app.pinnedBots')}
                    className="mt-1 border-t border-white/10 pt-1">
                    {pinnedBots
                      .filter((bot) => bot.available)
                      .map((bot) => (
                        <DrawerItem
                          key={bot.id}
                          isActive={botId === bot.id && !conversationId}
                          to={`/bot/${bot.id}`}
                          icon={<IconPinnedBot showAlways />}
                          labelComponent={bot.title}
                          onClick={onClickNewBotChat}
                        />
                      ))}
                  </ExpandableDrawerGroup>
                ) : null}

              {drawerOptions.show.starredBots && (
                <ExpandableDrawerGroup
                  label={t('app.starredBots')}
                  className="mt-1 border-t border-white/10 pt-1">
                  {starredBots === undefined && (
                    <div className="flex flex-col gap-1.5 px-2 py-1">
                      <Skeleton className="h-8 w-full bg-white/10" />
                      <Skeleton className="h-8 w-full bg-white/10" />
                      <Skeleton className="h-8 w-full bg-white/10" />
                    </div>
                  )}
                  {starredBots
                    ?.slice(0, drawerOptions.displayCount.starredBots)
                    .map((bot) => (
                      <DrawerItem
                        key={bot.id}
                        isActive={botId === bot.id && !conversationId}
                        to={`/bot/${bot.id}`}
                        icon={
                          isPinnedBot(bot.sharedStatus) ? (
                            <IconPinnedBot showAlways />
                          ) : (
                            <PiRobot />
                          )
                        }
                        labelComponent={bot.title}
                        onClick={onClickNewBotChat}
                      />
                    ))}

                  {starredBots && starredBots.length > 15 && (
                    <Button
                      text
                      rightIcon={<PiArrowRight />}
                      className="w-full text-white/70 hover:text-white"
                      onClick={() => {
                        navigate('/bot/starred');
                        closeSmallDrawer();
                      }}>
                      {t('bot.button.viewAll')}
                    </Button>
                  )}
                </ExpandableDrawerGroup>
              )}

              {drawerOptions.show.recentlyUsedBots && (
                <ExpandableDrawerGroup
                  label={t('app.recentlyUsedBots')}
                  className="mt-1 border-t border-white/10 pt-1">
                  {recentlyUsedUnstarredBots === undefined && (
                    <div className="flex flex-col gap-1.5 px-2 py-1">
                      <Skeleton className="h-8 w-full bg-white/10" />
                      <Skeleton className="h-8 w-full bg-white/10" />
                      <Skeleton className="h-8 w-full bg-white/10" />
                    </div>
                  )}
                  {recentlyUsedUnstarredBots
                    ?.slice(0, drawerOptions.displayCount.recentlyUsedBots)
                    .map((bot) => (
                      <DrawerItem
                        key={bot.id}
                        isActive={false}
                        to={`/bot/${bot.id}`}
                        icon={
                          isPinnedBot(bot.sharedStatus) ? (
                            <IconPinnedBot showAlways />
                          ) : (
                            <PiRobot />
                          )
                        }
                        labelComponent={bot.title}
                        onClick={onClickNewBotChat}
                      />
                    ))}

                  {recentlyUsedUnstarredBots && (
                    <Button
                      text
                      rightIcon={<PiArrowRight />}
                      className="w-full text-white/70 hover:text-white"
                      onClick={() => {
                        navigate('/bot/recently-used');
                        closeSmallDrawer();
                      }}>
                      {t('bot.button.viewAll')}
                    </Button>
                  )}
                </ExpandableDrawerGroup>
              )}

              {drawerOptions.show.conversationHistory && (
                <ExpandableDrawerGroup
                  label={t('app.conversationHistory')}
                  className={twMerge(
                    'mt-1 border-t border-white/10 pt-1',
                    props.isAdmin ? 'mb-20' : 'mb-10'
                  )}>
                  {conversations === undefined && (
                    <div className="flex flex-col gap-1.5 px-2 py-1">
                      <Skeleton className="h-8 w-full bg-white/10" />
                      <Skeleton className="h-8 w-full bg-white/10" />
                      <Skeleton className="h-8 w-4/5 bg-white/10" />
                      <Skeleton className="h-8 w-full bg-white/10" />
                      <Skeleton className="h-8 w-3/4 bg-white/10" />
                    </div>
                  )}
                  {conversations
                    ?.slice(0, drawerOptions.displayCount.conversationHistory)
                    .map((conversation, idx) => (
                      <Item
                        key={idx}
                        className="grow"
                        label={conversation.title}
                        conversationId={conversation.id}
                        generatedTitle={idx === generateTitleIndex}
                        updateTitle={props.updateConversationTitle}
                        onClick={closeSmallDrawer}
                        onDelete={() => props.onDeleteConversation(conversation)}
                      />
                    ))}

                  {conversations && (
                    <Button
                      text
                      rightIcon={<PiArrowRight />}
                      className="w-full text-white/70 hover:text-white"
                      onClick={() => {
                        navigate('/conversations');
                        closeSmallDrawer();
                      }}>
                      {t('bot.button.viewAll')}
                    </Button>
                  )}
                </ExpandableDrawerGroup>
              )}
            </>
          )}

          {isAdminPanel && (
            <>
              <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-white/50">
                {t('app.adminConsoles')}
              </div>
              <div className="px-2">
                <DrawerItem
                  className="w-60"
                  isActive={location.pathname === '/admin/shared-bot-analytics'}
                  icon={<PiChartLine />}
                  to="/admin/shared-bot-analytics"
                  labelComponent={getPageLabel('/admin/shared-bot-analytics')}
                  onClick={closeSmallDrawer}
                />
                <DrawerItem
                  className="w-60"
                  isActive={location.pathname === '/admin/user-analytics'}
                  icon={<PiUsers />}
                  to="/admin/user-analytics"
                  labelComponent={getPageLabel('/admin/user-analytics')}
                  onClick={closeSmallDrawer}
                />
                <DrawerItem
                  className="w-60"
                  isActive={location.pathname === '/admin/api-management'}
                  icon={<PiPlugs />}
                  to="/admin/api-management"
                  labelComponent={getPageLabel('/admin/api-management')}
                  onClick={closeSmallDrawer}
                />
              </div>
            </>
          )}

          {/* Bottom fixed area */}
          <div
            className={twMerge(
              opened ? 'w-64' : 'w-0',
              props.isAdmin ? 'h-20' : 'h-12',
              'fixed -bottom-2 z-50 mb-2 flex flex-col items-start border-t border-white/10 bg-aws-squid-ink-light transition-width dark:bg-aws-ui-color-dark lg:w-64'
            )}>
            {props.isAdmin && !isAdminPanel && (
              <DrawerItem
                className="w-60"
                isActive={false}
                icon={<PiPresentationChart />}
                to="/admin/shared-bot-analytics"
                labelComponent={t('app.adminConsoles')}
                onClick={closeSmallDrawer}
              />
            )}
            {isAdminPanel && (
              <DrawerItem
                className="w-60"
                isActive={false}
                icon={<PiChatCenteredDotsDuotone />}
                to="/"
                labelComponent={t('app.backChat')}
                onClick={closeSmallDrawer}
              />
            )}
            <Menu
              className="mx-2 flex h-10 w-60 justify-start"
              onSignOut={props.onSignOut}
              onSelectLanguage={props.onSelectLanguage}
              onClearConversations={props.onClearConversations}
              onClickDrawerOptions={props.onClickDrawerOptions}
            />
          </div>
        </nav>
      </div>

      <div
        ref={smallDrawer}
        className={`lg:hidden ${opened ? 'visible' : 'hidden'}`}>
        <ButtonIcon
          className="fixed left-64 top-0 z-50 text-white"
          onClick={switchOpen}>
          <PiX />
        </ButtonIcon>
        <div
          className="fixed z-40 h-dvh w-screen bg-black/60 backdrop-blur-sm"
          onClick={switchOpen}></div>
      </div>
    </>
  );
};

export default Drawer;
