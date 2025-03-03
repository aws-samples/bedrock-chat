import { FirecrawlConfig } from '../types';

export const DEFAULT_FIRECRAWL_CONFIG: FirecrawlConfig = {
  apiKey: '',
  maxResults: 5,
};

export const EDGE_FIRECRAWL_CONFIG = {
  maxResults: {
    MIN: 1,
    MAX: 50,
    STEP: 1,
  },
};
