import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import useChat from '../../../hooks/useChat';
import IconPinnedBot from '../../../components/IconPinnedBot';
import ModalDialog from '../../../components/ModalDialog';
import { BotMeta } from '../../../@types/bot';
import Button from '../../../components/Button';
import { PiChat } from 'react-icons/pi';
import MenuBot from '../../../components/MenuBot';
import { copyBotUrl } from '../../../utils/BotUtils';

type Props = {
  bot: BotMeta;
  hidePinnedIcon?: boolean;
};

const CardBotForDiscover: React.FC<Props> = (props) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { newChat } = useChat();

  const [isOpen, setIsOpen] = useState(false);

  const handleClick = () => {
    setIsOpen(true);
  };

  const gotoNewChat = () => {
    newChat();
    navigate(`/bot/${props.bot.id}`);
  };

  return (
    <>
      <ModalDialog
        isOpen={isOpen}
        showCloseIcon
        onClose={() => {
          setIsOpen(false);
        }}>
        <div className="-mt-6 flex w-full justify-end pr-4">
          <MenuBot
            onlyIcon
            onClickCopyUrl={() => {
              copyBotUrl(props.bot.id);
            }}
          />
        </div>
        <div className="flex flex-col items-center gap-3">
          <div className="flex items-center gap-1.5 text-xl font-bold tracking-tight text-aws-font-color-light dark:text-aws-font-color-dark">
            <IconPinnedBot
              botSharedStatus={props.bot.sharedStatus}
              className="text-aws-aqua"
            />
            {props.bot.title}
          </div>
          <div className="text-sm text-dark-gray dark:text-light-gray">
            {props.bot.description === ''
              ? t('bot.label.noDescription')
              : props.bot.description}
          </div>

          <Button
            className="mt-6 h-10 w-full"
            icon={<PiChat />}
            onClick={gotoNewChat}>
            Start Chat
          </Button>
        </div>
      </ModalDialog>

      <div
        className="hover-card flex h-28 w-full cursor-pointer flex-col rounded-xl border border-black/[0.06] bg-white px-4 py-3 dark:border-white/[0.06] dark:bg-aws-paper-dark"
        onClick={handleClick}>
        <div className="flex items-center">
          {!props.hidePinnedIcon && (
            <IconPinnedBot
              className="mr-1.5 shrink-0 text-aws-aqua"
              botSharedStatus={props.bot.sharedStatus}
            />
          )}
          <div className="truncate text-sm font-semibold tracking-tight">{props.bot.title}</div>
        </div>
        <div className="mt-1 line-clamp-3 overflow-hidden text-xs text-dark-gray dark:text-light-gray">
          {props.bot.description === ''
            ? t('bot.label.noDescription')
            : props.bot.description}
        </div>
      </div>
    </>
  );
};

export default CardBotForDiscover;
