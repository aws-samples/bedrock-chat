import { useTranslation } from 'react-i18next';
import InputChatContent from './InputChatContent';

export const Ideal = () => (
  <InputChatContent
    canRegenerate={false}
    canContinue={false}
    isLoading={false}
    isNewChat={false}
    onSend={() => {}}
    onRegenerate={() => {}}
    continueGenerate={() => {}}
  />
);

export const IdealLoading = () => (
  <InputChatContent
    disabledSend={true}
    disabledRegenerate={true}
    disabledContinue={true}
    canRegenerate={false}
    canContinue={false}
    isLoading={true}
    isNewChat={false}
    onSend={() => {}}
    onRegenerate={() => {}}
    continueGenerate={() => {}}
  />
);

export const IdealDisabled = () => {
  const { t } = useTranslation();
  return (
    <InputChatContent
      canRegenerate={false}
      canContinue={false}
      isLoading={false}
      isNewChat={false}
      disabled={true}
      placeholder={t('bot.label.notAvailableBotInputMessage')}
      onSend={() => {}}
      onRegenerate={() => {}}
      continueGenerate={() => {}}
    />
  );
};

export const WithRegenerate = () => (
  <InputChatContent
    canRegenerate={true}
    canContinue={false}
    isLoading={false}
    isNewChat={false}
    onSend={() => {}}
    onRegenerate={() => {}}
    continueGenerate={() => {}}
  />
);

export const WithContinue = () => (
  <InputChatContent
    canRegenerate={true}
    canContinue={true}
    isLoading={false}
    isNewChat={false}
    onSend={() => {}}
    onRegenerate={() => {}}
    continueGenerate={() => {}}
  />
);
