import React, { useCallback, useEffect, useState } from 'react';
import Button from '../components/Button';
import { useTranslation } from 'react-i18next';

import {
  PiTrashBold,
  PiPencilBold,
} from 'react-icons/pi';
import { useNavigate } from 'react-router-dom';
import useBot from '../hooks/useBot';
import { BotListItem, BotMeta, CreatorConfig } from '../@types/bot';
import DialogConfirmDeleteBot from '../components/DialogConfirmDeleteBot';
import DialogConfirmShareBot from '../components/DialogConfirmShareBot';
import useChat from '../hooks/useChat';
import useUser from '../hooks/useUser';
import useGroup from '../hooks/useGroup';
import StatusSyncBot from '../components/StatusSyncBot';
import Toggle from '../components/Toggle';
import { BottomHelper } from '../features/helper/components/BottomHelper';
import { Group } from '../@types/group';

const BotExplorePage: React.FC = () => {
  const navigate = useNavigate();
  const { emailId } = useUser(); 
  const { t } = useTranslation();
  const [isOpenDeleteDialog, setIsOpenDeleteDialog] = useState(false);
  const [targetDelete, setTargetDelete] = useState<BotMeta>();
  const [isOpenShareDialog, setIsOpenShareDialog] = useState(false);
  const [targetShare, setTargetShare] = useState<BotMeta>();
  const { myGroups } = useGroup();
  const [assistantList, setAssistantList] = useState<BotListItem[]>([]);
  const [groupMap, setGroupMap] = useState< Record<string, Group>>();


  const { newChat } = useChat();
  const {
    myBots,
    deleteMyBot,
    updateBotSharing,
  } = useBot(true);

  useEffect(() => {
    if (!myGroups || !myBots) return;
    // set the assistant list
    const sortedData = [...myBots].sort((a, b) => Number(b.createTime) - Number(a.createTime));
    setAssistantList(sortedData);
    
    // set the group list
    
    setGroupMap(groupMap);
  }, [myBots, myGroups])

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

  const onClickShare = useCallback((target: BotMeta) => {
    setIsOpenShareDialog(true);
    setTargetShare(target);
  }, []);

  const onShareMyBot = useCallback(() => {
    if (targetShare) {
      setIsOpenShareDialog(false);
      updateBotSharing(targetShare.id, !targetShare.isPublic).catch(() => {
        setIsOpenShareDialog(true);
      });
    }
  }, [updateBotSharing, targetShare]);

  const onClickBot = useCallback(
    (botId: string) => {
      newChat();
      navigate(`/bot/${botId}`);
    },
    [navigate, newChat]
  );

  const getImageSrc = (assistantType: string) => {
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

  const getCanvasInstanceName = useCallback((groupId: string) => {
    if (!myGroups) return;
    return myGroups[groupId].ltiName;
  }, [myGroups])

  const getCourseName = useCallback((groupId: string) => {
    if (!myGroups) return;
    return myGroups[groupId].groupName;
  }, [myGroups])

  const getCreatorName = (creatorConfig: CreatorConfig): string | undefined => {
    if (!creatorConfig || !creatorConfig.userName) {
      return "";
    }
    return creatorConfig.userName;
  };

  const getCreatedTimeFormatted = (createdTime: Date) => {
    const dateStr =  new Date(createdTime).toLocaleString("en-US", {
      timeZone: "America/Los_Angeles",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    });
    return dateStr.replace(/\//g, "-");
  }

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
      <DialogConfirmShareBot
        isOpen={isOpenShareDialog}
        target={targetShare}
        onShare={onShareMyBot}
        onClose={() => {
          setIsOpenShareDialog(false);
        }}
      />
        <div className="relative flex h-full flex-1 flex-col">
          <div className="flex-1 overflow-hidden assistant-list-title-and-btn-container">
            <div className="sticky top-0 z-10 mb-1.5 flex h-14 w-full items-center justify-between border-b border-gray bg-aws-paper-light dark:bg-aws-paper-dark">
              <div className="flex w-full justify-between">
                <div className="assistant-list-create-new-assistant-div">
                  <div className="text-xl font-bold">{"Create New Assistant"}</div>
                </div>
              </div>
              <div className="absolute right-2 top-10 text-xs text-dark-gray dark:text-light-gray">
                {emailId}
              </div>
            </div>
            <div className="container-bot-explore">
              <Button
                className="text-l font-bold create-assistant-btn"
                outlined
                onClick={() => onClickNewBot("learning_assistant")}>
                <img src="/images/learning_assistant.svg" className="create-assistant-btn-logo"/>
                <div className="create-assistant-btn-text-box">
                  <div className="create-assistant-btn-title">Learning Assistant</div>
                  <div className="create-assistant-btn-description">Answer student questions using provided material.</div>  
                </div>
              </Button>
            </div>
          </div>
          <div className="h-3/4 w-full p-2">
            <div className="flex w-full justify-between">
              <div className="text-xl font-bold">{"Assistant List"}</div>
            </div>
            <div className="mt-2 border-b border-gray"></div>
            <div className="h-5/6 overflow-x-auto overflow-y-scroll border-b border-gray pr-1 scrollbar-thin scrollbar-thumb-aws-font-color-light/20 dark:scrollbar-thumb-aws-font-color-dark/20">
              <table className="assistant-list-table">
                <thead>
                  <tr className="assistant-list-table-headers">
                    <th className="assistant-list-th-header assistant-list-th-logo-name">Name</th>
                    <th className="assistant-list-th-header">Course</th>
                    <th className="assistant-list-th-header">Entity</th>
                    <th className="assistant-list-th-header">Created By</th>
                    <th className="assistant-list-th-header">Created Date</th>
                    <th className="assistant-list-th-header">Sync Status</th>
                    <th className="assistant-list-th-header">Published</th>
                  </tr>
                </thead>
                <tbody id="bot-list">
                {assistantList?.map((bot) => (
                  <tr key={bot.id} className="assistant-list-item-container">
                    <td className={"assistant-list-tr-td-logo-name"} onClick={() => onClickBot(bot.id)}>
                      {/* Logo and Assistant Name in one column */}
                      <img src={getImageSrc(bot.assistantConfig.assistantType)} className="assistant-item-logo"/>
                      <div className="assistant-item-title-and-description">
                        <span
                          className={
                            bot.available
                              ? 'dark:text-aws-font-color-dark'
                              : 'dark:text-aws-font-color-gray'
                          }
                        >
                          {bot.title}
                        </span>
                        {bot.description ? (
                          <div className="mt-1 overflow-hidden text-ellipsis text-xs dark:text-aws-font-color-dark">
                              {bot.description}
                          </div>) : (
                          <div className="mt-1 overflow-hidden text-ellipsis text-xs italic text-gray dark:text-aws-font-color-gray">
                            {t('bot.label.noDescription')}
                          </div>
                          )}
                      </div>
                    </td>
                    <td className="assistant-list-column-td-text">{getCourseName(bot.groupId)}</td>
                    <td className="assistant-list-column-td-text">{getCanvasInstanceName(bot.groupId)}</td>
                    <td className="assistant-list-column-td-text">{(bot.creatorConfig) ? getCreatorName(bot.creatorConfig) : ""}</td>
                    <td className="assistant-list-column-td-text">{getCreatedTimeFormatted(bot.createTime)}</td>
                    <td>
                      <StatusSyncBot
                        className="mr-5 assistant-list-tr-td-sync-icon"
                        syncStatus={bot.syncStatus}
                        onClickError={() => {
                          navigate(`/bot/edit/${bot.id}`);
                        }}
                      />
                    </td>
                    <td className="assistant-list-tr-td-public-edit-delete">
                      {/* Public, Edit, Delete operations in one column */}
                      <Toggle
                        value={bot.isPublic}
                        onChange={() => onClickShare(bot)}/>
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
                    </td>
                  </tr>
                ))}
                </tbody>
              </table>
            </div>
          </div>
        <BottomHelper />
      </div>  
    </>
  );
};

export default BotExplorePage;
