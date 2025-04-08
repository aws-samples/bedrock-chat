import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { formatDate } from '../utils/DateUtils';
import InputText from './InputText';

export const TextInput = () => {
  const { t } = useTranslation();
  const [text, setText] = useState('');
  return (
    <InputText
      label={t('bot.item.title')}
      placeholder='Bot 1'
      hint={t('input.hint.required')}
      value={text}
      disabled={false}
      onChange={setText}
    />
  );
};

export const TextInputError = () => {
  const { t } = useTranslation();
  const [text, setText] = useState('');
  return (
    <InputText
      label={t('bot.item.title')}
      placeholder='Bot 1'
      hint={t('input.hint.required')}
      value={text}
      errorMessage={text === '' ? t('input.validationError.required') : undefined}
      disabled={false}
      onChange={setText}
    />
  );
};

export const TextInputDisabled = () => {
  const { t } = useTranslation();
  return (
    <InputText
      label={t('bot.item.title')}
      hint={t('input.hint.required')}
      value='Bot 1'
      disabled={true}
      onChange={() => {}}
    />
  );
};

export const UrlInput = () => {
  const [url, setUrl] = useState('http://example.com');
  return (
    <InputText
      type='url'
      value={url}
      placeholder='http://example.com'
      disabled={false}
      onChange={setUrl}
    />
  );
};

export const UrlInputDisabled = () => (
  <InputText
    type='url'
    value='http://example.com'
    disabled={true}
    onChange={() => {}}
  />
);

export const DateInput = () => {
  const { t } = useTranslation();
  const [date, setDate] = useState(formatDate(new Date(), 'YYYY-MM-DD'));
  return (
    <InputText
      className="w-full"
      type='date'
      label={t('analytics.label.SearchCondition.from', 'From')}
      value={date}
      disabled={false}
      onChange={setDate}
    />
  );
};

export const DateInputError = () => {
  const { t } = useTranslation();
  return (
    <InputText
      className="w-full"
      type='date'
      label={t('analytics.label.SearchCondition.from', 'From')}
      value={formatDate(new Date(), 'YYYY-MM-DD')}
      errorMessage={t('admin.validationError.period')}
      disabled={false}
      onChange={() => {}}
    />
  );
};

export const DateInputDisabled = () => {
  const { t } = useTranslation();
  return (
    <InputText
      className="w-full"
      type='date'
      label={t('analytics.label.SearchCondition.from', 'From')}
      value={formatDate(new Date(), 'YYYY-MM-DD')}
      disabled={true}
      onChange={() => {}}
    />
  );
};

export const NumberInput = () => {
  const { t } = useTranslation();
  const [value, setValue] = useState('5');
  return (
    <InputText
      type='number'
      label={t('bot.apiSettings.item.rateLimit')}
      placeholder='5'
      hint={t('bot.apiSettings.help.rateLimit')}
      value={value}
      disabled={false}
      onChange={setValue}
    />
  );
};

export const NumberInputError = () => {
  const { t } = useTranslation();
  const [value, setValue] = useState('');
  return (
    <InputText
      type='number'
      label={t('bot.apiSettings.item.rateLimit')}
      hint={t('bot.apiSettings.help.rateLimit')}
      value={value}
      errorMessage={value === '' ? t('input.validationError.required') : undefined}
      disabled={false}
      onChange={setValue}
    />
  );
};

export const NumberInputDisabled = () => {
  const { t } = useTranslation();
  return (
    <InputText
      type='number'
      label={t('bot.apiSettings.item.rateLimit')}
      hint={t('bot.apiSettings.help.rateLimit')}
      value='5'
      disabled={true}
      onChange={() => {}}
    />
  );
};
