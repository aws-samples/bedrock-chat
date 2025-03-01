// import { useState } from 'react';
// import { BotMeta } from '../@types/bot';
// import DialogConfirmAddApiKey from './DialogConfirmAddApiKey';
// import DialogConfirmClearConversations from './DialogConfirmClearConversations';
// import DialogConfirmDeleteApi from './DialogConfirmDeleteApi';
// import DialogConfirmDeleteApiKey from './DialogConfirmDeleteApiKey';
// import DialogConfirmDeleteBot from './DialogConfirmDeleteBot';
// import DialogConfirmDeleteChat from './DialogConfirmDeleteChat';
// import DialogFeedback from './DialogFeedback';
// import DialogInstructionsSamples from './DialogInstructionsSamples';
// import DialogSelectLanguage from './DialogSelectLanguage';
// import DialogShareBot from './DialogShareBot';

// export const AddApiKey = () => {
//   const [isOpenAddApiKeyDialog, setIsOpenAddApiKeyDialog] = useState(true);
//   const [isAddingApiKey, setIsAddingApiKey] = useState(false);
//   return (
//     <DialogConfirmAddApiKey
//       isOpen={isOpenAddApiKeyDialog}
//       loading={isAddingApiKey}
//       onAdd={() => {
//         setIsAddingApiKey(true);
//       }}
//       onClose={() => {
//         setIsOpenAddApiKeyDialog(false);
//       }}
//     />
//   );
// };

// export const ClearConversations = () => {
//   const [isOpenClearConversation, setIsOpenClearConversation] = useState(true);
//   return (
//     <DialogConfirmClearConversations
//       isOpen={isOpenClearConversation}
//       onDelete={() => {
//         setIsOpenClearConversation(false);
//       }}
//       onClose={() => {
//         setIsOpenClearConversation(false);
//       }}
//     />
//   );
// };

// export const DeleteApi = () => {
//   const [isOpenDeleteApiDialog, setIsOpenDeleteApiDialog] = useState(true);
//   return (
//     <DialogConfirmDeleteApi
//       isOpen={isOpenDeleteApiDialog}
//       onDelete={() => {
//         setIsOpenDeleteApiDialog(false);
//       }}
//       onClose={() => {
//         setIsOpenDeleteApiDialog(false);
//       }}
//     />
//   );
// };

// export const DeleteApiKey = () => {
//   const [isOpenDialog, setIsOpenDialog] = useState(true);
//   return (
//     <DialogConfirmDeleteApiKey
//       apiKeyTitle='API Key 1'
//       isOpen={isOpenDialog}
//       onDelete={() => {
//         setIsOpenDialog(false);
//       }}
//       onClose={() => {
//         setIsOpenDialog(false);
//       }}
//     />
//   );
// };

// export const DeleteBot = () => {
//   const [isOpenDeleteDialog, setIsOpenDeleteDialog] = useState(true);
//   return (
//     <DialogConfirmDeleteBot
//       isOpen={isOpenDeleteDialog}
//       target={{
//         id: '1',
//         title: 'Bot 1',
//         description: 'Bot 1',
//         createTime: new Date(),
//         lastUsedTime: new Date(),
//         isPublic: false,
//         isPinned: false,
//         owned: true,
//         syncStatus: 'SUCCEEDED',
//       }}
//       onDelete={() => {
//         setIsOpenDeleteDialog(false);
//       }}
//       onClose={() => {
//         setIsOpenDeleteDialog(false);
//       }}
//     />
//   );
// };

// export const DeleteConversation = () => {
//   const [isOpenDeleteModal, setIsOpenDeleteModal] = useState(true);
//   return (
//     <DialogConfirmDeleteChat
//       isOpen={isOpenDeleteModal}
//       target={{
//         id: '1',
//         title: 'Conversation 1',
//         createTime: new Date().getTime(),
//         lastMessageId: '1',
//         model: 'claude-v3.5-sonnet'
//       }}
//       onDelete={() => {
//         setIsOpenDeleteModal(false);
//       }}
//       onClose={() => {
//         setIsOpenDeleteModal(false);
//       }}
//     />
//   );
// };

// export const Feedback = () => {
//   const [isFeedbackOpen, setIsFeedbackOpen] = useState(true);
//   return (
//     <DialogFeedback
//       isOpen={isFeedbackOpen}
//       thumbsUp={false}
//       onClose={() => {
//         setIsFeedbackOpen(false);
//       }}
//       onSubmit={() => {
//         setIsFeedbackOpen(false);
//       }}
//     />
//   );
// };

// export const InstructionsSamples = () => {
//   const [isOpenSamples, setIsOpenSamples] = useState(true);
//   return (
//     <DialogInstructionsSamples
//       isOpen={isOpenSamples}
//       onClose={() => {
//         setIsOpenSamples(false);
//       }}
//     />
//   );
// };

// export const SelectLanguage = () => {
//   const [isOpenLangage, setIsOpenLangage] = useState(true);
//   return (
//     <DialogSelectLanguage
//       isOpen={isOpenLangage}
//       onSelectLanguage={() => {
//         setIsOpenLangage(false);
//       }}
//       onClose={() => {
//         setIsOpenLangage(false);
//       }}
//     />
//   );
// };

// export const ShareBot = () => {
//   const [isOpenShareDialog, setIsOpenShareDialog] = useState(true);
//   const [bot, setBot] = useState<BotMeta>({
//     id: '1',
//     title: 'Bot 1',
//     description: 'Bot 1',
//     createTime: new Date(),
//     lastUsedTime: new Date(),
//     isPublic: false,
//     isPinned: false,
//     owned: true,
//     syncStatus: 'SUCCEEDED',
//   });
//   return (
//     <DialogShareBot
//       isOpen={isOpenShareDialog}
//       target={bot}
//       onToggleShare={() => {
//         setBot(current => ({
//           ...current,
//           isPublic: !current.isPublic,
//         }));
//       }}
//       onClose={() => {
//         setIsOpenShareDialog(false);
//       }}
//     />
//   );
// };
