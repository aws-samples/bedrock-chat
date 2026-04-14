import React, { useCallback, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { PiLink } from 'react-icons/pi';
import { useNavigate } from 'react-router-dom';
import useBot from '../hooks/useBot';
import { BotListItem, BotMeta } from '../@types/bot';
import DialogConfirmDeleteBot from '../components/DialogConfirmDeleteBot';
import DialogShareBot from '../components/DialogShareBot';
import ButtonIcon from '../components/ButtonIcon';
import useChat from '../hooks/useChat';
import useLoginUser from '../hooks/useLoginUser';
import ListItemBot from '../components/ListItemBot';
import useShareBot from '../hooks/useShareBot';
import useBotPinning from '../hooks/useBotPinning';
import { isPinnedBot, canBePinned, copyBotUrl } from '../utils/BotUtils';
import { produce } from 'immer';
import ListPageLayout from '../layouts/ListPageLayout';
import IconShareBot from '../components/IconShareBot';
import ButtonStar from '../components/ButtonStar';
import MenuBot from '../components/MenuBot';

const BotRecentlyUsedPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { isAllowApiSettings, isAdmin } = useLoginUser();
  const [isOpenDeleteDialog, setIsOpenDeleteDialog] = useState(false);
  const [isOpenShareDialog, setIsOpenShareDialog] = useState(false);
  const [targetDelete, setTargetDelete] = useState<BotMeta>();
  const [openedShareDialogBotId, setOpenedShareDialogBotId] = useState<
    string | undefined
  >();
  const { pinBot, unpinBot } = useBotPinning();

  const { newChat } = useChat();
  const {
    recentlyUsedBots,
    isLoadingRecentlyUsedBots,
    deleteMyBot,
    updateStarred,
    mutateRecentlyUsedBots,
    removeFromRecentlyUsed,
  } = useBot(true);

  const {
    isPublication,
    sharedStatus,
    sharedScope,
    allowedGroupIds,
    allowedUserIds,
    isLoading: isLoadingShareBot,
    updateSharedScope,
    updateSharedUsersAndGroups,
  } = useShareBot({
    botId: openedShareDialogBotId,
    myBots: recentlyUsedBots ?? [],
    mutateMyBots: mutateRecentlyUsedBots,
  });

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

  const onClickBot = useCallback(
    (botId: string) => {
      newChat();
      navigate(`/bot/${botId}`);
    },
    [navigate, newChat]
  );

  const onClickShare = useCallback((botId: string) => {
    setIsOpenShareDialog(true);
    setOpenedShareDialogBotId(botId);
  }, []);

  const onClickApiSettings = useCallback(
    (botId: string) => {
      navigate(`/bot/api-settings/${botId}`);
    },
    [navigate]
  );

  const togglePinBot = useCallback(
    (bot: BotListItem) => {
      mutateRecentlyUsedBots(
        produce(recentlyUsedBots, (draft) => {
          if (draft) {
            const target = draft.find((b) => b.id === bot.id);
            if (target) {
              target.sharedStatus = isPinnedBot(bot.sharedStatus)
                ? 'shared'
                : 'pinned@000';
            }
          }
        }),
        {
          revalidate: false,
        }
      );

      if (isPinnedBot(bot.sharedStatus)) {
        unpinBot(bot.id).finally(() => {
          mutateRecentlyUsedBots();
        });
      } else {
        pinBot(bot.id, 0).finally(() => {
          mutateRecentlyUsedBots();
        });
      }
    },
    [mutateRecentlyUsedBots, pinBot, recentlyUsedBots, unpinBot]
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
      <DialogShareBot
        isOpen={isOpenShareDialog}
        isPublication={isPublication}
        botId={openedShareDialogBotId}
        sharedStatus={sharedStatus}
        sharedScope={sharedScope}
        allowedGroupIds={allowedGroupIds}
        allowedUserIds={allowedUserIds}
        isLoading={isLoadingShareBot}
        onChangeSharedScope={(scope) => {
          updateSharedScope(scope);
        }}
        onUpdateAllowedUserAndGroup={(userIds, groupIds) => {
          updateSharedUsersAndGroups(userIds, groupIds);
        }}
        onClose={() => {
          setIsOpenShareDialog(false);
        }}
      />
      <ListPageLayout
        pageTitle={t('bot.label.recentlyUsedBots')}
        isLoading={isLoadingRecentlyUsedBots}
        isEmpty={recentlyUsedBots?.length === 0}
        emptyMessage={t('bot.label.noBotsRecentlyUsed')}>
        {recentlyUsedBots?.map((bot) => (
          <ListItemBot key={bot.id} bot={bot} onClick={onClickBot}>
            <div className="flex items-center">
              {bot.owned && (
                <div className="mr-5 flex justify-end">
                  {bot.sharedScope === 'all' ||
                  bot.sharedScope === 'partial' ? (
                    <div className="flex items-center">
                      <IconShareBot
                        sharedScope={bot.sharedScope}
                        className="mr-2"
                      />
                      <ButtonIcon
                        className="-mr-3"
                        onClick={() => {
                          onClickShare(bot.id);
                        }}>
                        <PiLink />
                      </ButtonIcon>
                    </div>
                  ) : (
                    <div className="ml-7">
                      <IconShareBot sharedScope={bot.sharedScope} />
                    </div>
                  )}
                </div>
              )}

              <div className="mr-5">
                <ButtonStar
                  isStarred={bot.isStarred}
                  disabled={!bot.available}
                  onClick={() => {
                    updateStarred(bot.id, !bot.isStarred);
                  }}
                />
              </div>
              <div className="relative">
                <MenuBot
                  onClickRemoveFromRecentlyUsed={() => {
                    removeFromRecentlyUsed(bot.id);
                  }}
                  {...(isAdmin && canBePinned(bot.sharedScope)
                    ? {
                        onClickSwitchPinned: () => {
                          togglePinBot(bot);
                        },
                        isPinned: isPinnedBot(bot.sharedStatus),
                      }
                    : {
                        onClickSwitchPinned: undefined,
                        isPinned: undefined,
                      })}
                  {...(bot.owned && {
                    onClickEdit: () => {
                      onClickEditBot(bot.id);
                    },
                    onClickShare: () => {
                      onClickShare(bot.id);
                    },
                    onClickDelete: () => {
                      onClickDelete(bot);
                    },
                  })}
                  {...(bot.owned &&
                    isAllowApiSettings && {
                      onClickApiSettings: () => {
                        onClickApiSettings(bot.id);
                      },
                    })}
                  {...(!bot.owned && {
                    onClickCopyUrl: () => {
                      copyBotUrl(bot.id);
                    },
                  })}
                  {...(!bot.owned &&
                    isAdmin && {
                      onClickBotManagement: () => {
                        navigate(`/admin/bot/${bot.id}`);
                      },
                    })}
                />
              </div>
            </div>
          </ListItemBot>
        ))}
      </ListPageLayout>
    </>
  );
};

export default BotRecentlyUsedPage;
