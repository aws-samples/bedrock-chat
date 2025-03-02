import i18next from 'i18next';
import detector from 'i18next-browser-languagedetector';
import { initReactI18next } from 'react-i18next';
import en from './en';
import ja from './ja';
import ko from './ko';
import es from './es';
import zhhans from './zh-hans';
import zhhant from './zh-hant';
import fr from './fr';
import de from './de';
import it from './it';
import nb from './nb';
import th from './th';
import id from './id';
import ms from './ms';
import vi from './vi';
import pl from './pl';

export const LANGUAGES: {
  value: string;
  label: string;
}[] = [
  {
    value: 'en',
    label: 'English',
  },
  {
    value: 'de',
    label: 'Deutsch',
  },
  {
    value: 'fr',
    label: 'Français',
  },
  {
    value: 'es',
    label: 'Español',
  },
  {
    value: 'ja',
    label: '日本語',
  },
  {
    value: 'ko',
    label: '한국어',
  },
  {
    value: 'zhhans',
    label: '中文 (简体)',
  },
  {
    value: 'zhhant',
    label: '中文 (繁體)',
  },
  {
    value: 'it',
    label: 'Italian',
  },
  {
    value: 'nb',
    label: 'Norsk (Bokmål)',
  },
  {
    value: 'th',
    label: 'ไทย',
  },
  {
    value: 'id',
    label: 'Bahasa Indonesia',
  },
  {
    value: 'ms',
    label: 'Bahasa Melayu',
  },
  {
    value: 'vi',
    label: 'Tiếng Việt',
  },
  {
    value: 'pl',
    label: 'Polski',
  },
];

const resources = {
  en,
  de,
  fr,
  es,
  ja,
  ko,
  it,
  zhhans,
  zhhant,
  nb,
  th,
  id,
  ms,
  vi,
  pl,
};

// Settings i18n
const i18n = i18next
  .use(initReactI18next)
  .use(detector)
  .init({
    resources,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false, // react already safes from xss => https://www.i18next.com/translation-function/interpolation#unescape
    },
  });

export default i18n;
