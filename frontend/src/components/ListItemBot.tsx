import { ReactNode } from 'react';
import { BaseProps } from '../@types/common';
import { useTranslation } from 'react-i18next';
import { AssistantConfig, CreatorConfig } from '../@types/bot';
import { ASSISTANT_TYPE_MAP, COURSE_ID_MAP, LTI_DEPLOYMENT_ID_MAP, ValidCourseId, ValidLTIDeploymentId } from '../constants';

type Props = BaseProps & {
  bot: {
    id: string;
    title: string;
    description: string;
    available: boolean;
    assistantConfig: AssistantConfig;
    creatorConfig: CreatorConfig | null;
    groupId: string;
  };
  onClick: (botId: string) => void;
  children: ReactNode;
};

const ListItemBot: React.FC<Props> = (props) => {
  const { t } = useTranslation();

  const getImageSrc = () => {
    switch (props.bot.assistantConfig.assistantType) {
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

  const getCanvasInstanceName = () => {
    const lti_deploymentId: ValidLTIDeploymentId = props.bot.groupId.split("-")[0] as ValidLTIDeploymentId;
    return LTI_DEPLOYMENT_ID_MAP[lti_deploymentId];
  }

  const getCourseName = () => {
    const courseId: ValidCourseId = props.bot.groupId as ValidCourseId;
    return COURSE_ID_MAP[courseId];
  }

  const getAssistantTypeName = (): string | undefined => {
    return ASSISTANT_TYPE_MAP.find(option => option.value === props.bot.assistantConfig.assistantType)?.label;
  };

  const getCreatorName = (): string | undefined => {
    if (!props.bot.creatorConfig || !props.bot.creatorConfig.userName) {
      return "";
    }
    return props.bot.creatorConfig.userName;
    
  };
  

  return (
    <div
      key={props.bot.id}
      className={`${
        props.className ?? ''
      } relative flex w-full justify-between border-b border-light-gray`}>
      <div
        className={`assistant-item-row`}>
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
              <div className="assistant-item-course">{getCourseName()}</div>
              <div className="assistant-item-canvas">{getCanvasInstanceName()}</div>
              <div className="assistant-item-type-and-name">{getAssistantTypeName()}</div>
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
