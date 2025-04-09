import { BotMeta } from '../../../@types/bot';

export type SearchBotsRequest = {
  query: string;
  limit?: number;
};

export type SearchBotsResponse = BotMeta[];

export type GetPopularBotsRequest = {
  limit?: number;
};

export type GetPopularBotsResponse = BotMeta[];

export type GetPickupBotsRequest = {
  limit?: number;
};

export type GetPickupBotsResponse = BotMeta[];
