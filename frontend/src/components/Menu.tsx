import React, { useEffect, useRef, useState } from 'react';
import Button from './Button';
import {
  PiList,
  PiSidebar,
  PiSignOut,
  PiTranslate,
  PiTrash,
} from 'react-icons/pi';
import { useTranslation } from 'react-i18next';
import { BaseProps } from '../@types/common';
import { twMerge } from 'tailwind-merge';
import useLoginUser from '../hooks/useLoginUser';
import { IoMoonSharp, IoSunnyOutline } from 'react-icons/io5';
import useLocalStorage from '../hooks/useLocalStorage';
import Toggle from './Toggle';

type Props = BaseProps & {
  onSignOut: () => void;
  onSelectLanguage: () => void;
  onClickDrawerOptions: () => void;
  onClearConversations: () => void;
};

const MenuSettings: React.FC<Props> = (props) => {
  const { t } = useTranslation();
  const { userGroups, userName } = useLoginUser();

  const [isOpen, setIsOpen] = useState(false);
  // If you want to add a theme, change the type from boolean to string and change the UI from pulldown.
  const [isDarkTheme, setIsDarkTheme] = useState(false);
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleClickOutside = (event: any) => {
      // メニューボタンとメニュー以外をクリックしていたらメニューを閉じる
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target) &&
        !buttonRef.current?.contains(event.target)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [menuRef]);

  useEffect(() => {
    if (theme === 'dark') {
      setIsDarkTheme(true);
    }
  }, [theme]);

  const changeTheme = (isDarkTheme: boolean) => {
    setIsDarkTheme(isDarkTheme);
    if (isDarkTheme) {
      document.documentElement.className = 'dark';
      setTheme('dark');
    } else {
      document.documentElement.className = 'light';
      setTheme('light');
    }
  };

  return (
    <>
      <Button
        ref={buttonRef}
        className={twMerge(
          'relative bg-aws-squid-ink-light dark:bg-aws-squid-ink-dark',
          props.className
        )}
        text
        icon={<PiList />}
        onClick={() => {
          setIsOpen(!isOpen);
        }}>
        {t('button.menu')}
      </Button>

      {isOpen && (
        <div
          ref={menuRef}
          className="absolute bottom-12 left-2 w-60 animate-scale-in rounded-xl border border-white/[0.08] bg-aws-squid-ink-light/95 text-white/90 shadow-vercel-dark-lg backdrop-blur-md dark:bg-aws-ui-color-dark/95">
          <div className="flex flex-col gap-0.5 border-b border-white/[0.06] p-3">
            <div className="text-[13px] font-semibold tracking-tight">{userName}</div>
            <div className="mt-1">
              <div className="text-[11px] font-medium uppercase tracking-wider text-white/40">{t('app.userGroups')}</div>
              <ul className="mt-0.5 list-disc pl-4 text-[13px] text-white/60">
                {userGroups.map((group) => (
                  <li key={group}>{group}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="py-1">
            <div
              className="flex w-full cursor-pointer items-center px-3 py-2 text-[13px] transition-colors duration-150 hover:bg-white/[0.06]"
              onClick={() => {
                setIsOpen(false);
                props.onClickDrawerOptions();
              }}>
              <PiSidebar className="mr-2.5 text-white/50" />
              {t('button.drawerOption')}
            </div>

            <div
              className="flex w-full cursor-pointer items-center px-3 py-2 text-[13px] transition-colors duration-150 hover:bg-white/[0.06]"
              onClick={() => {
                setIsOpen(false);
                props.onSelectLanguage();
              }}>
              <PiTranslate className="mr-2.5 text-white/50" />
              {t('button.language')}
            </div>

            <div className="flex w-full items-center px-3 py-2 text-[13px] transition-colors duration-150 hover:bg-white/[0.06]">
              {isDarkTheme ? (
                <IoMoonSharp className="mr-2.5 text-white/50" />
              ) : (
                <IoSunnyOutline className="mr-2.5 text-white/50" />
              )}
              <div className="flex w-full items-center justify-between">
                <span>{t('button.mode')}</span>
                <Toggle
                  value={isDarkTheme}
                  onChange={(isDarkTheme) => {
                    changeTheme(isDarkTheme);
                  }}
                />
              </div>
            </div>
          </div>

          <div className="border-t border-white/[0.06] py-1">
            <div
              className="flex w-full cursor-pointer items-center px-3 py-2 text-[13px] transition-colors duration-150 hover:bg-white/[0.06]"
              onClick={() => {
                setIsOpen(false);
                props.onClearConversations();
              }}>
              <PiTrash className="mr-2.5 text-white/50" />
              {t('button.clearConversation')}
            </div>
            <div
              className="flex w-full cursor-pointer items-center px-3 py-2 text-[13px] transition-colors duration-150 hover:bg-white/[0.06]"
              onClick={props.onSignOut}>
              <PiSignOut className="mr-2.5 text-white/50" />
              {t('button.signOut')}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default MenuSettings;
