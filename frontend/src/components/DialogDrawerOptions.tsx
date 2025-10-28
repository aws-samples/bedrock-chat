import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { BaseProps, DrawerOptions } from '../@types/common';
import Button from './Button';
import ModalDialog from './ModalDialog';
import { useTranslation } from 'react-i18next';
import InputText from './InputText';
import Toggle from './Toggle';

type Props = BaseProps & {
  isOpen: boolean;
  drawerOptions: DrawerOptions;
  onChangeDrawerOptions: (drawerOptions: DrawerOptions) => void;
  onClose: () => void;
};

const DialogDrawerOptions: React.FC<Props> = (props) => {
  const { t } = useTranslation();

  const [starredBotsCount, setStarredBotsCount] = useState<number | null>(0);
  const [recentlyUsedBotsCount, setRecentlyUsedBotsCount] = useState<
    number | null
  >(0);
  const [conversationHistoryCount, setConversationHistoryCount] = useState<
    number | null
  >(0);

  const [showNewChat, setShowNewChat] = useState(true);
  const [showMyBots, setShowMyBots] = useState(true);
  const [showDiscoverBots, setShowDiscoverBots] = useState(true);
  const [showPinnedBots, setShowPinnedBots] = useState(true);
  const [showStarredBots, setShowStarredBots] = useState(true);
  const [showRecentlyUsedBots, setShowRecentlyUsedBots] = useState(true);
  const [showConversationHistory, setShowConversationHistory] = useState(true);

  useEffect(() => {
    if (props.isOpen) {
      setStarredBotsCount(props.drawerOptions.displayCount.starredBots);
      setRecentlyUsedBotsCount(
        props.drawerOptions.displayCount.recentlyUsedBots
      );
      setConversationHistoryCount(
        props.drawerOptions.displayCount.conversationHistory
      );
      setShowNewChat(props.drawerOptions.show.newChat);
      setShowMyBots(props.drawerOptions.show.myBots);
      setShowDiscoverBots(props.drawerOptions.show.discoverBots);
      setShowPinnedBots(props.drawerOptions.show.pinnedBots);
      setShowStarredBots(props.drawerOptions.show.starredBots);
      setShowRecentlyUsedBots(props.drawerOptions.show.recentlyUsedBots);
      setShowConversationHistory(props.drawerOptions.show.conversationHistory);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [props.isOpen]);

  const validateDisplayCount = useCallback(
    (value: number | null, key: string) => {
      if (value === null) {
        return t('validation.required', {
          key,
        });
      } else if (value < 1) {
        return t('validation.number.greaterThen', {
          key,
          value: '0',
        });
      }
      return undefined;
    },
    [t]
  );

  const errorMessages = useMemo(() => {
    return {
      starredBots: validateDisplayCount(starredBotsCount, t('app.starredBots')),
      recentlyUsedBots: validateDisplayCount(
        recentlyUsedBotsCount,
        t('app.recentlyUsedBots')
      ),
      conversationHistory: validateDisplayCount(
        conversationHistoryCount,
        t('app.conversationHistory')
      ),
    };
  }, [
    conversationHistoryCount,
    recentlyUsedBotsCount,
    starredBotsCount,
    t,
    validateDisplayCount,
  ]);

  const hasError = useMemo(() => {
    return Object.values(errorMessages).some((v) => v != null);
  }, [errorMessages]);

  return (
    <ModalDialog {...props} title={t('drawerOptionsDialog.title')}>
      <div className="flex flex-col gap-3">
        <div>
          <div className="text-base font-bold">
            {t('drawerOptionsDialog.label.visibility')}
          </div>
          <div className="ml-3 mt-1 flex flex-col gap-1">
            <Toggle
              label={t('button.newChat')}
              value={showNewChat}
              onChange={setShowNewChat}
            />
            <Toggle
              label={t('app.myBots')}
              value={showMyBots}
              onChange={setShowMyBots}
            />
            <Toggle
              label={t('app.discoverBots')}
              value={showDiscoverBots}
              onChange={setShowDiscoverBots}
            />
            <Toggle
              label={t('app.pinnedBots')}
              value={showPinnedBots}
              onChange={setShowPinnedBots}
            />
            <Toggle
              label={t('app.starredBots')}
              value={showStarredBots}
              onChange={setShowStarredBots}
            />
            <Toggle
              label={t('app.recentlyUsedBots')}
              value={showRecentlyUsedBots}
              onChange={setShowRecentlyUsedBots}
            />
            <Toggle
              label={t('app.conversationHistory')}
              value={showConversationHistory}
              onChange={setShowConversationHistory}
            />
          </div>
        </div>

        <div>
          <div className="text-base font-bold">
            {t('drawerOptionsDialog.label.displayCount')}
          </div>
          <div className="ml-3 mt-1 flex flex-col gap-2">
            <InputText
              label={t('app.starredBots')}
              type="number"
              value={starredBotsCount?.toString() ?? ''}
              errorMessage={errorMessages['starredBots']}
              disabled={!showStarredBots}
              onChange={(s) => {
                setStarredBotsCount(s === '' ? null : parseInt(s));
              }}
            />
            <InputText
              label={t('app.recentlyUsedBots')}
              type="number"
              value={recentlyUsedBotsCount?.toString() ?? ''}
              errorMessage={errorMessages['recentlyUsedBots']}
              disabled={!showRecentlyUsedBots}
              onChange={(s) => {
                setRecentlyUsedBotsCount(s === '' ? null : parseInt(s));
              }}
            />
            <InputText
              label={t('app.conversationHistory')}
              type="number"
              value={conversationHistoryCount?.toString() ?? ''}
              errorMessage={errorMessages['conversationHistory']}
              disabled={!showConversationHistory}
              onChange={(s) => {
                setConversationHistoryCount(s === '' ? null : parseInt(s));
              }}
            />
          </div>
        </div>
      </div>

      <div className="mt-4 flex justify-end gap-2">
        <Button onClick={props.onClose} className="p-2" outlined>
          {t('button.cancel')}
        </Button>
        <Button
          disabled={hasError}
          onClick={() => {
            props.onChangeDrawerOptions({
              displayCount: {
                starredBots: starredBotsCount!,
                recentlyUsedBots: recentlyUsedBotsCount!,
                conversationHistory: conversationHistoryCount!,
              },
              show: {
                newChat: showNewChat,
                myBots: showMyBots,
                discoverBots: showDiscoverBots,
                pinnedBots: showPinnedBots,
                starredBots: showStarredBots,
                recentlyUsedBots: showRecentlyUsedBots,
                conversationHistory: showConversationHistory,
              },
            });
          }}
          className="p-2">
          {t('button.ok')}
        </Button>
      </div>
    </ModalDialog>
  );
};

export default DialogDrawerOptions;
