import type { Story, StoryDefault } from '@ladle/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ChatListDrawer from './ChatListDrawer';
import { BotListItem } from '../@types/bot';
import { ConversationMeta } from '../@types/conversation';

const conversations: ConversationMeta[] = [
  {
    id: '1',
    title: 'What is RAG?',
    createTime: new Date().getTime(),
    lastMessageId: '',
    model: 'claude-v3.5-sonnet',
    botId: '1',
  },
];
const bots: BotListItem[] = [
  {
    id: '1',
    title: 'Bot 1',
    description: 'Bot 1',
    createTime: new Date(),
    lastUsedTime: new Date(),
    isPublic: false,
    isPinned: false,
    owned: false,
    syncStatus: 'SUCCEEDED',
    available: true,
  },
  {
    id: '2',
    title: 'Bot 2',
    description: 'Bot 2',
    createTime: new Date(),
    lastUsedTime: new Date(),
    isPublic: true,
    isPinned: true,
    owned: true,
    syncStatus: 'SUCCEEDED',
    available: true,
  },
];

export default {
  decorators: [
    (Story) => (
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Story />} />
          <Route path="/bot/:botId" element={<Story />} />
          <Route path="/bot/explore" element={<Story />} />
          <Route path="/:conversationId" element={<Story />} />
          <Route path="/admin/shared-bot-analytics" element={<Story />} />
          <Route path="/admin/api-management" element={<Story />} />
        </Routes>
      </MemoryRouter>
    ),
  ],
} satisfies StoryDefault;

export const Admin: Story = () => {
  return (
    <ChatListDrawer
      isAdmin={true}
      conversations={conversations}
      starredBots={bots.filter((bot) => bot.isPinned)}
      recentlyUsedUnsterredBots={bots.filter((bot) => !bot.isPinned)}
      updateConversationTitle={async () => {}}
      onSignOut={() => {}}
      onDeleteConversation={() => {}}
      onClearConversations={() => {}}
      onSelectLanguage={() => {}}
    />
  );
};

export const NonAdmin: Story = () => {
  return (
    <ChatListDrawer
      isAdmin={false}
      conversations={conversations}
      starredBots={bots.filter((bot) => bot.isPinned)}
      recentlyUsedUnsterredBots={bots.filter((bot) => !bot.isPinned)}
      updateConversationTitle={async () => {}}
      onSignOut={() => {}}
      onDeleteConversation={() => {}}
      onClearConversations={() => {}}
      onSelectLanguage={() => {}}
    />
  );
};
