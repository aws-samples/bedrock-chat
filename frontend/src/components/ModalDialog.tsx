import { Dialog, Transition } from '@headlessui/react';
import { Fragment, useCallback } from 'react';
import { BaseProps } from '../@types/common';
import ButtonIcon from './ButtonIcon';
import { PiX } from 'react-icons/pi';

type Props = BaseProps & {
  isOpen: boolean;
  title?: string;
  widthFromContent?: boolean;
  showCloseIcon?: boolean;
  children: React.ReactNode;
  onClose?: () => void;
  onAfterLeave?: () => void;
};

const ModalDialog: React.FC<Props> = (props) => {
  const onClose = useCallback(() => {
    if (props.onClose) {
      props.onClose();
    }
  }, [props]);

  const onAfterLeave = useCallback(() => {
    if (props.onAfterLeave) {
      props.onAfterLeave();
    }
  }, [props]);

  return (
    <>
      <Transition
        appear
        show={props.isOpen}
        as={Fragment}
        afterLeave={onAfterLeave}>
        <Dialog as="div" className="relative z-50" onClose={() => onClose()}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-200"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-150"
            leaveFrom="opacity-100"
            leaveTo="opacity-0">
            <div className="fixed inset-0 bg-black/40 backdrop-blur-sm" />
          </Transition.Child>

          <div className="fixed inset-0 overflow-y-auto">
            <div
              className={`mx-auto flex min-h-full items-center justify-center p-4 text-center ${
                props.className ?? ''
              }`}>
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95 translate-y-2"
                enterTo="opacity-100 scale-100 translate-y-0"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100 translate-y-0"
                leaveTo="opacity-0 scale-95 translate-y-2">
                <Dialog.Panel
                  className={`relative rounded-2xl border border-black/[0.06] bg-white p-6 text-left align-middle shadow-vercel-lg transition-all dark:border-white/[0.08] dark:bg-aws-paper-dark dark:shadow-vercel-dark-lg ${
                    !props.widthFromContent && 'w-full max-w-md'
                  }`}>
                  {props.title && (
                    <Dialog.Title
                      as="h3"
                      className="border-b border-black/[0.06] pb-3 text-base font-semibold tracking-tight text-aws-font-color-light dark:border-white/[0.06] dark:text-aws-font-color-white-dark">
                      {props.title}
                    </Dialog.Title>
                  )}
                  {props.showCloseIcon && (
                    <ButtonIcon
                      className="absolute right-3 top-3"
                      onClick={onClose}>
                      <PiX />
                    </ButtonIcon>
                  )}

                  <div className="mt-4">
                    <div className="text-sm text-aws-font-color-light/70 dark:text-aws-font-color-dark">
                      {props.children}
                    </div>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
    </>
  );
};

export default ModalDialog;
