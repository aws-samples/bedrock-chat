import { AVAILABLE_MODEL_KEYS } from '../constants/index';
export type Role = 'system' | 'assistant' | 'user';

export type Model = (typeof AVAILABLE_MODEL_KEYS)[number];

export type Content =
  | TextContent
  | ImageContent
  | AttachmentContent
  | ReasoningContent
  | ToolUseContent
  | ToolResultContent;

export type TextContent = {
  contentType: 'text';
  body: string;
};

export type ImageContent = {
  contentType: 'image';
  mediaType?: string;
  body: string;
};

export type AttachmentContent = {
  contentType: 'attachment';
  fileName?: string;
  body: string;
};

export type ReasoningContent = {
  contentType: 'reasoning';
  text: string;
  signature: string;
  redactedContent: string;
};

export type ToolUseContent = {
  contentType: 'toolUse';
  body: ToolUseContentBody;
};

export type ToolResultContent = {
  contentType: 'toolResult';
  body: ToolResultContentBody;
};

export type UsedChunk = {
  content: string;
  contentType: 's3' | 'url' | 'youtube';
  source: string;
  rank: number;
};

export type ToolUseContentBody = {
  toolUseId: string;
  name: string;
  input: { [key: string]: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
};

export type AgentToolResultTextContent = {
  text: string;
};

export type AgentToolResultJsonContent = {
  json: { [key: string]: any }; // eslint-disable-line @typescript-eslint/no-explicit-any
};

export type AgentToolResultContent =
  | AgentToolResultTextContent
  | AgentToolResultJsonContent;

export type ToolResultContentBody = {
  toolUseId: string;
  content: AgentToolResultContent[];
  status: 'success' | 'error';
};

export type SimpleMessageContent =
  | TextContent
  | ToolUseContent
  | ToolResultContent;

export type SimpleMessage = {
  role: Role;
  content: SimpleMessageContent[];
};

export type MessageContent = {
  role: Role;
  content: Content[];
  model: Model;
  feedback: null | Feedback;
  usedChunks: null | UsedChunk[];
  thinkingLog: null | SimpleMessage[];
};

export type RelatedDocument = {
  content: AgentToolResultContent;
  sourceId: string;
  sourceName?: string;
  sourceLink?: string;
  pageNumber?: number;
};

export type DisplayMessageContent = MessageContent & {
  id: string;
  parent: null | string;
  children: string[];
  sibling: string[];
};

export type PostMessageRequest = {
  conversationId?: string;
  message: MessageContent & {
    parentMessageId: null | string;
  };
  botId?: string;
  continueGenerate?: boolean;
  enableReasoning: boolean;
};

export type PostMessageResponse = {
  conversationId: string;
  createTime: number;
  message: MessageContent;
};

export type SearchHighlightModel = {
  fieldName: string;  // "Title" or "MessageMap"
  fragments: string[]; // Text fragments containing the search term
};

export type ConversationMeta = {
  id: string;
  title: string;
  createTime: number;
  lastMessageId: string; 
  model: Model;
  botId?: string;
};

export type ConversationSearchMeta = {
  id: string;
  title: string;
  createTime: number;
  lastUpdatedTime: number;
  botId?: string;
  highlights?: SearchHighlightModel[]; // Optional highlights information
};

export type MessageMap = {
  [messageId: string]: MessageContent & {
    children: string[];
    parent: null | string;
  };
};

export type Conversation = ConversationMeta & {
  messageMap: MessageMap;
  shouldContinue: boolean;
};

export type PutFeedbackRequest = {
  thumbsUp: boolean;
  category: null | string;
  comment: null | string;
};

export type Feedback = {
  thumbsUp: boolean;
  category: string;
  comment: string;
};
