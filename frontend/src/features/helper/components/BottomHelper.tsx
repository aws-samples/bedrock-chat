import { useState } from 'react';
import ModalDialog from '../../../components/ModalDialog';
import { useTranslation } from 'react-i18next';
import { useIsWindows } from '../../../hooks/useIsWindows';
export const BottomHelper = () => {
  const { t } = useTranslation();
  const { isWindows } = useIsWindows();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <div className="fixed bottom-3 right-3">
        <img
          src="/images/Qikr_logo_black_filled.png"
          alt="Logo"
          className="w-12 h-12"
          onClick={() => setIsOpen(() => true)}
        />
      </div>
      <ModalDialog
        title={t('helper.shortcuts.title')}
        isOpen={isOpen}
        onClose={() => setIsOpen(() => false)}>
        <div className="flex items-center justify-between overflow-hidden">
          <div className="flex shrink items-center overflow-hidden text-sm">
            <div className="truncate">
              {t('helper.shortcuts.items.newChat')}
            </div>
          </div>
          <div className="ml-3 flex flex-row gap-2">
            <div className="my-2 flex h-8 min-w-[32px] items-center justify-center rounded-md border capitalize">
              <span className="text-sm">{isWindows ? 'Ctrl' : '⌘'}</span>
            </div>
            <div className="my-2 flex h-8 min-w-[50px] items-center justify-center rounded-md border capitalize">
              <span className="text-xs">Shift</span>
            </div>
            <div className="my-2 flex h-8 min-w-[32px] items-center justify-center rounded-md border capitalize">
              <span className="text-sm">o</span>
            </div>
          </div>
        </div>
        <div className="flex items-center justify-between overflow-hidden">
          <div className="flex shrink items-center overflow-hidden text-sm">
            <div className="truncate">
              {t('helper.shortcuts.items.focusInput')}
            </div>
          </div>
          <div className="ml-3 flex flex-row gap-2">
            <div className="my-2 flex h-8 min-w-[50px] items-center justify-center rounded-md border capitalize">
              <span className="text-xs">Shift</span>
            </div>
            <div className="my-2 flex h-8 min-w-[32px] items-center justify-center rounded-md border capitalize">
              <span className="text-xs">Esc</span>
            </div>
          </div>
        </div>
      </ModalDialog>
    </>
  );
};
