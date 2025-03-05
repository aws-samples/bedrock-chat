import { GenerationParams } from '../@types/bot';
import { AssistantType } from '../features/knowledgeBase/types';


export const VERSION_02_17_25 = '02.17.25';

export const EDGE_GENERATION_PARAMS = {
  maxTokens: {
    MAX: 4096,
    MIN: 1,
    STEP: 1,
  },
  temperature: {
    MAX: 1,
    MIN: 0,
    STEP: 0.05,
  },
  topP: {
    MAX: 1,
    MIN: 0,
    STEP: 0.001,
  },
  topK: {
    MAX: 500,
    MIN: 0,
    STEP: 1,
  },
};

export const EDGE_MISTRAL_GENERATION_PARAMS = {
  maxTokens: {
    MAX: 8192,
    MIN: 1,
    STEP: 1,
  },
  temperature: {
    MAX: 1,
    MIN: 0,
    STEP: 0.05,
  },
  topP: {
    MAX: 1,
    MIN: 0,
    STEP: 0.001,
  },
  topK: {
    MAX: 200,
    MIN: 0,
    STEP: 1,
  },
};

export const DEFAULT_GENERATION_CONFIG: GenerationParams = {
  maxTokens: 3000,
  topK: 128,
  topP: 0.999,
  temperature: 0.0,
  stopSequences: ['Human: ', 'Assistant: '],
};

export const DEFAULT_MISTRAL_GENERATION_CONFIG: GenerationParams = {
  maxTokens: 4096,
  topK: 50,
  topP: 0.9,
  temperature: 0.0,
  stopSequences: ['[INST]', '[/INST]'],
};

export const SyncStatus = {
  QUEUED: 'QUEUED',
  FAILED: 'FAILED',
  RUNNING: 'RUNNING',
  SUCCEEDED: 'SUCCEEDED',
} as const;

export const TooltipDirection = {
  LEFT: 'left',
  RIGHT: 'right',
} as const;

export type Direction =
  (typeof TooltipDirection)[keyof typeof TooltipDirection];

export const PostStreamingStatus = {
  START: 'START',
  BODY: 'BODY',
  STREAMING: 'STREAMING',
  STREAMING_END: 'STREAMING_END',
  AGENT_THINKING: 'AGENT_THINKING',
  AGENT_TOOL_RESULT: 'AGENT_TOOL_RESULT',
  AGENT_RELATED_DOCUMENT: 'AGENT_RELATED_DOCUMENT',
  ERROR: 'ERROR',
  END: 'END',
  // Additional statuses for responses
  CONNECTED: 'CONNECTED',
  SUCCESS: 'SUCCESS',
} as const;

export const GUARDRAILS_FILTERS_THRESHOLD = {
  MAX: 3,
  MIN: 0,
  STEP: 1,
};

export const GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD = {
  MAX: 0.99,
  MIN: 0,
  STEP: 0.01,
};

export const MODEL_REGISTRY = {
  CLAUDE: {
    'claude-v3-haiku': {
      supportMediaType: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxTokens: 200000, // Context window: 200,000 tokens
    },
    'claude-v3-sonnet': {
      supportMediaType: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxTokens: 200000, // Context window: 200,000 tokens
    },
    'claude-v3-opus': {
      supportMediaType: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxTokens: 200000, // Context window: 200,000 tokens
    },
    'claude-v3.5-haiku': {
      supportMediaType: [],
      maxTokens: 200000, // Context window: 200,000 tokens
    },
    'claude-v3.5-sonnet': {
      supportMediaType: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxTokens: 200000, // Context window: 200,000 tokens
    },
    'claude-v3.5-sonnet-v2': {
      supportMediaType: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxTokens: 200000, // Context window: 200,000 tokens
    },
    'claude-v3.7-sonnet': {
      supportMediaType: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxTokens: 200000, // Context window: 200,000 tokens
    },
  },
  AMAZON: {
    'amazon-nova-pro': {
      supportMediaType: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxTokens: 300000, // Context window: 300,000 tokens
    },
    'amazon-nova-lite': {
      supportMediaType: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxTokens: 300000, // Context window: 300,000 tokens
    },
    'amazon-nova-micro': {
      supportMediaType: [],
      maxTokens: 128000, // Context window: 128,000 tokens
    },
  },
  MISTRAL: {
    'mistral-7b-instruct': {
      supportMediaType: [],
      maxTokens: 32000, // Context window: 8,192 tokens
    },
    'mixtral-8x7b-instruct': {
      supportMediaType: [],
      maxTokens: 32000, // Context window: 8,192 tokens
    },
    'mistral-large': {
      supportMediaType: [],
      maxTokens: 32000, // Context window: 8,192 tokens
    },
  },
} as const;


// Add type exports
export type ModelCategory = keyof typeof MODEL_REGISTRY;
export type ModelId = {
  [K in ModelCategory]: keyof typeof MODEL_REGISTRY[K];
}[ModelCategory];

// Feature flags for model categories
export const ENABLED_MODEL_CATEGORIES = {
  CLAUDE: true,
  AMAZON: true,
  MISTRAL: import.meta.env.VITE_APP_ENABLE_MISTRAL === 'true'
} as const;

// List of allowed models
const ALLOWED_MODELS = [
  'claude-v3.5-sonnet',
  'claude-v3.5-sonnet-v2',
  'claude-v3.7-sonnet',
  'claude-v3.5-haiku',
  'claude-v3-haiku',
  'amazon-nova-pro',
  'amazon-nova-lite'
];

export const AVAILABLE_MODEL_KEYS = Object.entries(MODEL_REGISTRY)
  .filter(([category]) => ENABLED_MODEL_CATEGORIES[category as keyof typeof ENABLED_MODEL_CATEGORIES])
  .flatMap(([_, models]) => Object.keys(models))
  .filter(model => ALLOWED_MODELS.includes(model)) as ModelId[];


// Refresh Interval
export const BASE_REFRESH_INTERVAL = 15000;

export const COURSE_ID_MAP = {
  "353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f-9": "Algebra 1",
  "353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f-10": "Chemistry",
  "353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f-11": "US History",
  "353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f-12": "Algebra 1",
  "353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f-13": "Chemistry",
  "353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f-14": "US History",
  "353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f-15": "Intro to Qikr"

}

export type ValidCourseId = keyof typeof COURSE_ID_MAP;

export const LTI_DEPLOYMENT_ID_MAP = {
  "353:ce504bb9edc03fa62d3f80c5d1fadcb2f7346e0f": "SDCC"
}

export type ValidLTIDeploymentId = keyof typeof LTI_DEPLOYMENT_ID_MAP;



export const ASSISTANT_TYPE_MAP: {
  label: string;
  value: AssistantType;
}[] = [
  {
    label: 'Learning Assistant',
    value: 'learning_assistant',
  },
  {
    label: 'Quiz Assistant',
    value: 'quiz_assistant',
  },
  {
    label: 'Lesson Plan Assistant',
    value: 'lesson_plan_assistant',
  },
  {
    label: 'Custom Assistant',
    value: 'custom_assistant',
  },
];

export const P0_FEATURE_FLAG = false;
