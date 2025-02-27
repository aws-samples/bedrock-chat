import React, { useCallback, useState } from 'react';
import { useTranslation } from 'react-i18next';
import Button from '../components/Button';
import {
  PiTrashBold,
  PiPencilBold,
} from 'react-icons/pi';
import { useNavigate } from 'react-router-dom';
import useBot from '../hooks/useBot';
import { BotMeta } from '../@types/bot';
import DialogConfirmDeleteBot from '../components/DialogConfirmDeleteBot';
import useChat from '../hooks/useChat';
import Help from '../components/Help';
import StatusSyncBot from '../components/StatusSyncBot';
import ListItemBot from '../components/ListItemBot';
import { TooltipDirection } from '../constants';
import Toggle from '../components/Toggle';

const BotExplorePage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [isOpenDeleteDialog, setIsOpenDeleteDialog] = useState(false);
  const [targetDelete, setTargetDelete] = useState<BotMeta>();

  const { newChat } = useChat();
  const {
    myBots,
    deleteMyBot,
    updateBotSharing,
  } = useBot(true);

  const onClickNewBot = useCallback((assistantType: string) => {
    navigate('/bot/new', { state: { assistantType: assistantType } });
  }, [navigate]);

  const onClickEditBot = useCallback(
    (botId: string) => {
      navigate(`/bot/edit/${botId}`);
    },
    [navigate]
  );

  const onClickDelete = useCallback((target: BotMeta) => {
    setIsOpenDeleteDialog(true);
    setTargetDelete(target);
  }, []);

  const onDeleteMyBot = useCallback(() => {
    if (targetDelete) {
      setIsOpenDeleteDialog(false);
      deleteMyBot(targetDelete.id).catch(() => {
        setIsOpenDeleteDialog(true);
      });
    }
  }, [deleteMyBot, targetDelete]);

  const onToggleShare = useCallback((botId: string, isPublic: boolean) => {
      updateBotSharing(botId, !isPublic);
  }, []);

  const onClickBot = useCallback(
    (botId: string) => {
      newChat();
      navigate(`/bot/${botId}`);
    },
    [navigate, newChat]
  );
  return (
    <>
      <DialogConfirmDeleteBot
        isOpen={isOpenDeleteDialog}
        target={targetDelete}
        onDelete={onDeleteMyBot}
        onClose={() => {
          setIsOpenDeleteDialog(false);
        }}
      />
      <div className="flex h-full justify-center">
        <div className="w-full max-w-screen-xl px-4 lg:w-4/5">
          <div className="h-1/4 w-full pt-8">
            <div className="flex items-end justify-between">
              <div className="flex items-center gap-2">
                <div className="text-xl font-bold">{"Create Assistant"}</div>
                <Help
                  direction={TooltipDirection.RIGHT}
                  message={t('bot.help.overview')}
                />
              </div>
            </div>
            <div className="mt-2 border-b border-gray"></div>

            <div className="h-4/5 overflow-x-auto overflow-y-scroll border-b border-gray pr-1 scrollbar-thin scrollbar-thumb-aws-font-color-light/20 dark:scrollbar-thumb-aws-font-color-dark/20">
              <div className="h-full min-w-[480px]">
                <div className="container-bot-explore">
                  <div className="first-half-bot-explore">
                    <Button
                      className="text-l font-bold create-assistant-btn"
                      outlined
                      onClick={() => onClickNewBot("learning_assistant")}>
                      <img src="/images/learning_assistant.png" className="create-assistant-btn-logo"/>
                      <div className="create-assistant-btn-text-box">
                        <div className="create-assistant-btn-title">Learning Assistant</div>
                        <div className="create-assistant-btn-description">Answer student questions based on uploaded material.</div>  
                      </div>
                    </Button>
                  </div>
                  <div className="first-half-bot-explore">
                    <Button
                      className="text-l font-bold create-assistant-btn"
                      outlined
                      onClick={() => onClickNewBot("custom_assistant")}>
                      <img src="/images/custom_assistant.png" className="create-assistant-btn-logo"/>
                      <div className="create-assistant-btn-text-box">
                        <div className="create-assistant-btn-title">Custom Assistant</div>
                        <div className="create-assistant-btn-description">Build an assistant tailored to your needs.</div>  
                      </div>
                    </Button>
                  </div>
                </div>
                <div className="container-bot-explore">
                  <div className="second-half-bot-explore">
                    <Button
                      className="text-l font-bold create-assistant-btn"
                      outlined
                      onClick={() => onClickNewBot("quiz_assistant")}>
                      <img src="/images/quiz_assistant.png" className="create-assistant-btn-logo"/>
                      <div className="create-assistant-btn-text-box">
                        <div className="create-assistant-btn-title">Quiz Assistant</div>
                        <div className="create-assistant-btn-description">Generate quiz questions based on uploaded material.</div>  
                      </div>
                    </Button>
                  </div>
                  <div className="second-half-bot-explore">
                    <Button
                      className="text-l font-bold create-assistant-btn"
                      outlined
                      onClick={() => onClickNewBot("lesson_plan_assistant")}>
                      <img src="/images/lesson_plan_assistant.png" className="create-assistant-btn-logo"/>
                      <div className="create-assistant-btn-text-box">
                        <div className="create-assistant-btn-title">Lesson Plan Assistant</div>
                        <div className="create-assistant-btn-description">Generate lesson plans based on uploaded material.</div>  
                      </div>
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="h-3/4 w-full">
            <div className='assistant-list-column-headers-row'>
              <div className="text-xl font-bold assistant-list-column-headers-row-title">Assistant List</div>
              <div className='assistant-list-column-headers-row-attributes'>
                <div className='assistant-list-column-attribute-items assistant-item-course'>Course Name</div>
                <div className='assistant-list-column-attribute-items assistant-item-canvas'>District</div>
                <div className='assistant-list-column-attribute-items assistant-item-type-and-name'>Created By</div>
              </div>
              <div className='assistant-list-column-headers-row-buttons'>
                <div className='assistant-list-column-btn-items'>Sync Status</div>
                <div className='assistant-list-column-btn-items'>Public</div>
              </div>
            </div>
            <div className="mt-2 border-b border-gray"></div>
            <div className="h-4/5 overflow-x-auto overflow-y-scroll border-b border-gray pr-1 scrollbar-thin scrollbar-thumb-aws-font-color-light/20 dark:scrollbar-thumb-aws-font-color-dark/20">
              <div className="h-full min-w-[480px]">
                {myBots?.map((bot) => (
                  <ListItemBot
                    key={bot.id}
                    bot={bot}
                    onClick={onClickBot}
                    className="last:border-b-0">
                    <div className="flex items-center">
                      <StatusSyncBot
                        className="mr-5"
                        syncStatus={bot.syncStatus}
                        onClickError={() => {
                          navigate(`/bot/edit/${bot.id}`);
                        }}
                      />
                      <Toggle
                        value={bot.isPublic}
                        onChange={() => onToggleShare(bot.id, bot.isPublic)}/>
                      <Button
                        className="mr-2 h-8 text-sm font-semibold"
                        outlined
                        onClick={() => {
                          onClickEditBot(bot.id);
                        }}>
                        <PiPencilBold />
                      </Button>
                      <Button
                        className="mr-2 h-8 text-sm font-semibold"
                        outlined
                        onClick={() => {
                          onClickDelete(bot);
                        }}>
                        <PiTrashBold />
                      </Button>
                    </div>
                  </ListItemBot>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default BotExplorePage;
