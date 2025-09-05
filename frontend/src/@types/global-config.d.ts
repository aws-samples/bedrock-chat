import { AVAILABLE_MODEL_KEYS } from '../constants/index';

export interface GlobalConfig {
  globalAvailableModels: string[];
}

export interface GetGlobalConfigResponse extends GlobalConfig {}

export interface ModelItem {
  modelId: (typeof AVAILABLE_MODEL_KEYS)[number];
  label: string;
  supportMediaType: string[];
  supportReasoning: boolean;
  forceReasoningEnabled?: boolean;
  description?: string;
}
