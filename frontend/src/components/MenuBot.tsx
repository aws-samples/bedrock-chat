import React, { useCallback, useState } from 'react';
import { BaseProps } from '../@types/common';
import PopoverMenu from './PopoverMenu';
import PopoverItem from './PopoverItem';
import {
  PiEraser,
  PiLink,
  PiPencilLine,
  PiPlugs,
  PiShareNetwork,
  PiTrashBold,
  PiWrench,
} from 'react-icons/pi';
import { useTranslation } from 'react-i18next';
import { twMerge } from 'tailwind-merge';
import IconPinnedBot from './IconPinnedBot';

type Props = BaseProps & {
  onlyIcon?: boolean;
  disabled?: boolean;
  onClickEdit?: () => void;
  onClickCopyUrl?: () => void;
  onClickShare?: () => void;
  onClickBotManagement?: () => void;
  onClickApiSettings?: () => void;
  onClickRemoveFromRecentlyUsed?: () => void;
  onClickDelete?: () => void;
} & (
    | {
        onClickSwitchPinned: () => void;
        isPinned: boolean;
      }
    | {
        onClickSwitchPinned?: undefined;
        isPinned?: undefined;
      }
  );

const MenuBot: React.FC<Props> = (props) => {
  const { t } = useTranslation();

  const [copyLabel, setCopyLabel] = useState(t('bot.titleSubmenu.copyLink'));
  const handleClickCopyUrl = useCallback(() => {
    props.onClickCopyUrl && props.onClickCopyUrl();
    setCopyLabel(t('bot.titleSubmenu.copiedLink'));
    setTimeout(() => {
      setCopyLabel(t('bot.titleSubmenu.copyLink'));
    }, 3000);
  }, [props, t]);

  return (
    <PopoverMenu
      className={twMerge(
        'h-8',
        props.onlyIcon &&
          'border-0 bg-transparent hover:bg-aws-squid-ink-light/20',
        props.className
      )}
      target="bottom-right"
      disabled={props.disabled}>
      {props.onClickEdit && (
        <PopoverItem onClick={props.onClickEdit}>
          <PiPencilLine />
          {t('bot.titleSubmenu.edit')}
        </PopoverItem>
      )}
      {props.onClickCopyUrl && (
        <PopoverItem onClick={handleClickCopyUrl}>
          <PiLink />
          {copyLabel}
        </PopoverItem>
      )}
      {props.onClickShare && (
        <PopoverItem onClick={props.onClickShare}>
          <PiShareNetwork />
          {t('bot.button.share')}
        </PopoverItem>
      )}

      {props.onClickBotManagement && (
        <PopoverItem onClick={props.onClickBotManagement}>
          <PiWrench />
          {t('button.botManagement')}
        </PopoverItem>
      )}

      {props.onClickApiSettings && (
        <PopoverItem onClick={props.onClickApiSettings}>
          <PiPlugs />
          {t('bot.button.apiSettings')}
        </PopoverItem>
      )}

      {props.onClickSwitchPinned && (
        <PopoverItem onClick={props.onClickSwitchPinned}>
          {props.isPinned ? (
            <>
              <IconPinnedBot showAlways className="text-aws-aqua" />
              {t('bot.titleSubmenu.removeEssential')}
            </>
          ) : (
            <>
              <IconPinnedBot showAlways outlined />
              {t('bot.titleSubmenu.markAsEssential')}
            </>
          )}
        </PopoverItem>
      )}
      {props.onClickRemoveFromRecentlyUsed && (
        <PopoverItem onClick={props.onClickRemoveFromRecentlyUsed}>
          <PiEraser />
          {t('bot.button.removeFromRecent')}
        </PopoverItem>
      )}
      {props.onClickDelete && (
        <PopoverItem
          className="font-bold text-red"
          onClick={props.onClickDelete}>
          <PiTrashBold />
          {t('bot.button.delete')}
        </PopoverItem>
      )}
    </PopoverMenu>
  );
};

export default MenuBot;
