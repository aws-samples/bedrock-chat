import React, { useEffect } from 'react';
import { PiWarningFill, PiX } from 'react-icons/pi';
import ButtonIcon from '../components/ButtonIcon';
import useSnackbar from '../hooks/useSnackbar';
import { Transition } from '@headlessui/react';

type Props = {
  children: React.ReactNode;
};

const SnackbarProvider: React.FC<Props> = ({ children }) => {
  const { isOpen, close, message } = useSnackbar();

  useEffect(() => {
    if (isOpen) {
      // 5000 ms で自動非表示
      setTimeout(() => {
        close();
      }, 5000);
    }
  }, [close, isOpen]);

  return (
    <>
      <div className="fixed left-0 top-0 z-50 w-full lg:left-1/3 lg:w-1/2">
        <Transition
          show={isOpen}
          enter="transform transition duration-200 ease-out"
          enterFrom="opacity-0 -translate-y-2 scale-95"
          enterTo="opacity-100 translate-y-0 scale-100"
          leave="transform duration-150 transition ease-in"
          leaveFrom="opacity-100 translate-y-0 scale-100"
          leaveTo="opacity-0 -translate-y-2 scale-95">
          <div className="mx-4 mt-4 flex items-center justify-between rounded-xl border border-red/20 bg-white p-3 text-sm text-red shadow-vercel-lg dark:border-red/20 dark:bg-aws-paper-dark dark:shadow-vercel-dark-lg">
            <div className="mr-3 text-2xl">
              <PiWarningFill />
            </div>
            <div className="grow font-medium tracking-tight">{message}</div>
            <div className="-mr-1">
              <ButtonIcon onClick={close}>
                <PiX className="text-base" />
              </ButtonIcon>
            </div>
          </div>
        </Transition>
      </div>
      {children}
    </>
  );
};

export default SnackbarProvider;
