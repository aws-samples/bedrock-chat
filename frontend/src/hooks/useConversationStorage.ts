/**
 * Ephemeral mode utilities for local conversation storage.
 *
 * In ephemeral mode (VITE_EPHEMERAL_MODE=true):
 * - Conversations are stored in IndexedDB on the user's device
 * - No prompts or messages are sent to DynamoDB/S3
 * - Bedrock inference still happens normally
 */

import { Conversation, MessageMap, RelatedDocument } from '../@types/conversation';

export const EPHEMERAL_MODE = import.meta.env.VITE_EPHEMERAL_MODE === 'true';

const DB_NAME = 'bedrock-chat-local';
const DB_VERSION = 1;
const CONVERSATIONS_STORE = 'conversations';

let dbPromise: Promise<IDBDatabase> | null = null;

const openDB = (): Promise<IDBDatabase> => {
  if (dbPromise) return dbPromise;

  dbPromise = new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      if (!db.objectStoreNames.contains(CONVERSATIONS_STORE)) {
        const store = db.createObjectStore(CONVERSATIONS_STORE, { keyPath: 'id' });
        store.createIndex('createTime', 'createTime', { unique: false });
      }
    };
  });

  return dbPromise;
};

export type StoredConversation = Conversation & {
  relatedDocuments?: RelatedDocument[];
};

/**
 * Save or update a conversation in local storage
 */
export const saveConversationLocally = async (
  conversationId: string,
  messageMap: MessageMap,
  lastMessageId: string,
  shouldContinue: boolean,
  title?: string,
  botId?: string,
  createTime?: number
): Promise<void> => {
  if (!EPHEMERAL_MODE) return;

  const db = await openDB();

  return new Promise((resolve, reject) => {
    const transaction = db.transaction(CONVERSATIONS_STORE, 'readwrite');
    const store = transaction.objectStore(CONVERSATIONS_STORE);

    // First try to get existing
    const getRequest = store.get(conversationId);

    getRequest.onsuccess = () => {
      const existing = getRequest.result as StoredConversation | undefined;

      const conversation: StoredConversation = {
        id: conversationId,
        title: title || existing?.title || 'New conversation',
        createTime: existing?.createTime || createTime || Date.now(),
        lastMessageId,
        messageMap,
        shouldContinue,
        model: messageMap?.system?.model ?? existing?.model ?? '',
        botId: botId || existing?.botId,
        relatedDocuments: existing?.relatedDocuments,
      };

      const putRequest = store.put(conversation);
      putRequest.onsuccess = () => resolve();
      putRequest.onerror = () => reject(putRequest.error);
    };

    getRequest.onerror = () => reject(getRequest.error);
  });
};

/**
 * Get a conversation from local storage
 */
export const getConversationLocally = async (
  conversationId: string
): Promise<StoredConversation | undefined> => {
  const db = await openDB();

  return new Promise((resolve, reject) => {
    const transaction = db.transaction(CONVERSATIONS_STORE, 'readonly');
    const store = transaction.objectStore(CONVERSATIONS_STORE);
    const request = store.get(conversationId);

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
};

/**
 * Get all conversations from local storage (sorted by createTime desc)
 */
export const getAllConversationsLocally = async (): Promise<StoredConversation[]> => {
  const db = await openDB();

  return new Promise((resolve, reject) => {
    const transaction = db.transaction(CONVERSATIONS_STORE, 'readonly');
    const store = transaction.objectStore(CONVERSATIONS_STORE);
    const request = store.getAll();

    request.onsuccess = () => {
      const conversations = request.result as StoredConversation[];
      conversations.sort((a, b) => b.createTime - a.createTime);
      resolve(conversations);
    };
    request.onerror = () => reject(request.error);
  });
};

/**
 * Delete a conversation from local storage
 */
export const deleteConversationLocally = async (
  conversationId: string
): Promise<void> => {
  if (!EPHEMERAL_MODE) return;

  const db = await openDB();

  return new Promise((resolve, reject) => {
    const transaction = db.transaction(CONVERSATIONS_STORE, 'readwrite');
    const store = transaction.objectStore(CONVERSATIONS_STORE);
    const request = store.delete(conversationId);

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
};

/**
 * Clear all conversations from local storage
 */
export const clearAllConversationsLocally = async (): Promise<void> => {
  if (!EPHEMERAL_MODE) return;

  const db = await openDB();

  return new Promise((resolve, reject) => {
    const transaction = db.transaction(CONVERSATIONS_STORE, 'readwrite');
    const store = transaction.objectStore(CONVERSATIONS_STORE);
    const request = store.clear();

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
};

/**
 * Update conversation title in local storage
 */
export const updateTitleLocally = async (
  conversationId: string,
  title: string
): Promise<void> => {
  if (!EPHEMERAL_MODE) return;

  const conversation = await getConversationLocally(conversationId);
  if (conversation) {
    conversation.title = title;
    const db = await openDB();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(CONVERSATIONS_STORE, 'readwrite');
      const store = transaction.objectStore(CONVERSATIONS_STORE);
      const request = store.put(conversation);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }
};

/**
 * Save related documents to a conversation in local storage
 */
export const saveRelatedDocumentsLocally = async (
  conversationId: string,
  documents: RelatedDocument[]
): Promise<void> => {
  if (!EPHEMERAL_MODE) return;

  const conversation = await getConversationLocally(conversationId);
  if (conversation) {
    conversation.relatedDocuments = [
      ...(conversation.relatedDocuments || []),
      ...documents,
    ];

    const db = await openDB();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(CONVERSATIONS_STORE, 'readwrite');
      const store = transaction.objectStore(CONVERSATIONS_STORE);
      const request = store.put(conversation);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }
};

/**
 * Generate a title from the first user message
 */
export const generateLocalTitle = async (conversationId: string): Promise<string> => {
  const conversation = await getConversationLocally(conversationId);
  if (!conversation) return 'New conversation';

  const firstUserMsg = Object.values(conversation.messageMap).find(
    (m) => m.role === 'user'
  );

  if (!firstUserMsg) return 'New conversation';

  const textContent = firstUserMsg.content.find((c) => c.contentType === 'text');
  const body = (textContent as { body?: string })?.body || '';

  // Take first 50 chars, trim to last complete word
  let title = body.slice(0, 50);
  if (body.length > 50) {
    const lastSpace = title.lastIndexOf(' ');
    if (lastSpace > 20) {
      title = title.slice(0, lastSpace);
    }
    title += '...';
  }

  return title || 'New conversation';
};
