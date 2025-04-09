import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { BaseProps, DrawerOptions } from '../@types/common';
import Button from './Button';
import ModalDialog from './ModalDialog';
import { useTranslation } from 'react-i18next';
import InputText from './InputText';

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

  useEffect(() => {
    if (props.isOpen) {
      setStarredBotsCount(props.drawerOptions.displayCount.starredBots);
      setRecentlyUsedBotsCount(
        props.drawerOptions.displayCount.recentlyUsedBots
      );
      setConversationHistoryCount(
        props.drawerOptions.displayCount.conversationHistory
      );
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
            {t('drawerOptionsDialog.label.displayCount')}
          </div>
          <div className="ml-3 mt-1 flex flex-col gap-2">
            <InputText
              label={t('app.starredBots')}
              type="number"
              value={starredBotsCount?.toString() ?? ''}
              errorMessage={errorMessages['starredBots']}
              onChange={(s) => {
                setStarredBotsCount(s === '' ? null : parseInt(s));
              }}
            />
            <InputText
              label={t('app.recentlyUsedBots')}
              type="number"
              value={recentlyUsedBotsCount?.toString() ?? ''}
              errorMessage={errorMessages['recentlyUsedBots']}
              onChange={(s) => {
                setRecentlyUsedBotsCount(s === '' ? null : parseInt(s));
              }}
            />
            <InputText
              label={t('app.conversationHistory')}
              type="number"
              value={conversationHistoryCount?.toString() ?? ''}
              errorMessage={errorMessages['conversationHistory']}
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
