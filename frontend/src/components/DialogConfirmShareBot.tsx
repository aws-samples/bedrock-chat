import React from 'react';
import { BaseProps } from '../@types/common';
import Button from './Button';
import ModalDialog from './ModalDialog';
import { Trans, useTranslation } from 'react-i18next';
import { BotMeta } from '../@types/bot';

type Props = BaseProps & {
  isOpen: boolean;
  target?: BotMeta;
  onShare: (botId: string) => void;
  onClose: () => void;
};

const DialogConfirmShareBot: React.FC<Props> = (props) => {
  const { t } = useTranslation();

  return (
    <ModalDialog {...props} title={(props.target?.isPublic) ? t('shareConfirmDialog.titleUnshare') : t('shareConfirmDialog.titleShare')}>
      <div>
        <Trans
          i18nKey={(props.target?.isPublic) ? "shareConfirmDialog.contentUnshare": "shareConfirmDialog.contentShare"}
          values={{
            title: props.target?.title,
          }}
          components={{
            Bold: <span className="font-bold" />,
          }}
        />
      </div>

      <div className="mt-4 flex justify-end gap-2">
        <Button onClick={props.onClose} className="p-2" outlined>
          {t('button.cancel')}
        </Button>
        <Button
          onClick={() => {
            props.onShare(props.target?.id ?? '');
          }}
          className="p-2 text-aws-font-color-white-light dark:text-aws-font-color-white-dark">
          {"Confirm"}
        </Button>
      </div>
    </ModalDialog>
  );
};

export default DialogConfirmShareBot;
