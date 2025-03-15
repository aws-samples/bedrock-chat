import { ReactNode } from 'react';
import { BaseProps } from '../@types/common';
import { useTranslation } from 'react-i18next';
import { AssistantConfig, CreatorConfig } from '../@types/bot';

type Props = BaseProps & {
  bot: {
    id: string;
    title: string;
    description: string;
    available: boolean;
    assistantConfig: AssistantConfig | null;
    creatorConfig: CreatorConfig | null;
    groupId: string | null;
  };
  onClick: (botId: string) => void;
  children: ReactNode;
};

const ListItemBot: React.FC<Props> = (props) => {
  const { t } = useTranslation();
  
  const getImageSrc = () => {
    if (!props.bot.assistantConfig) {
      return "/images/custom_assistant.png";
    }
    
    // Use bracket notation to access the property without TypeScript errors
    // This allows us to access properties not explicitly defined in the interface
    const assistantType = props.bot.assistantConfig['assistantType'] as string || "custom_assistant";
    
    switch (assistantType) {
      case "learning_assistant":
        return "/images/learning_assistant.png";
      case "lesson_plan_assistant":
        return "/images/lesson_plan_assistant.png";
      case "quiz_assistant":
        return "/images/quiz_assistant.png";
      case "custom_assistant":
        return "/images/custom_assistant.png";
      default:
        return "/images/custom_assistant.png";
    }
  };
  
  
  const getCreatorName = (): string | undefined => {
    if (!props.bot.creatorConfig || !props.bot.creatorConfig.userName) {
      return "";
    }
    return props.bot.creatorConfig.userName;
  };
  
  return (
    <div className="assistant-item-container">
      <div className="assistant-item-row">
          <div 
            className={`assistant-item-row-no-buttons-container ${
              props.bot.available
                ? 'cursor-pointer hover:brightness-90'
                : 'text-aws-font-color-light/30 dark:text-aws-font-color-dark/30'
              }`}
            onClick={() => {
              if (props.bot.available) {
                props.onClick(props.bot.id);
              }
            }}>
            <img src={getImageSrc()} className="assistant-item-logo"/>
            <div className="assistant-item-title-and-description">
              <span
                className={
                  props.bot.available
                    ? 'dark:text-aws-font-color-dark'
                    : 'dark:text-aws-font-color-gray'
                }
              >
                {props.bot.title}
              </span>
              {props.bot.description ? (
                <div className="mt-1 overflow-hidden text-ellipsis text-xs dark:text-aws-font-color-dark">
                    {props.bot.description}
                </div>) : (
                <div className="mt-1 overflow-hidden text-ellipsis text-xs italic text-gray dark:text-aws-font-color-gray">
                  {t('bot.label.noDescription')}
                </div>
                )}
            </div>
            <div className="assistant-item-attribute-no-buttons"> 
              <div className="assistant-item-type-and-name">{getCreatorName()}</div>
            </div>
          </div>
          <div className="assistant-item-buttons-container">
            {props.children}
          </div>
      </div>
    </div>
  );
};

export default ListItemBot;