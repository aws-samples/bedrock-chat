import { AVAILABLE_MODEL_KEYS } from '../constants/index';

export interface GlobalConfig {
  globalAvailableModels: string[];
  defaultModel?: string;
  logoPath?: string;
}

// eslint-disable-next-line @typescript-eslint/no-empty-object-type
export interface GetGlobalConfigResponse extends GlobalConfig {}

export interface ModelItem {
  modelId: (typeof AVAILABLE_MODEL_KEYS)[number];
  label: string;
  supportMediaType: string[];
  supportReasoning: boolean;
  forceReasoningEnabled?: boolean;
  description?: string;
}
