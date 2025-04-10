import React from 'react';
import { useTranslation } from 'react-i18next';

interface SummaryStatsProps {
  stats: {
    total_bots: number;
    total_users: number;
    total_sessions: number;
    total_messages: number;
    total_input_tokens: number | null;
    total_output_tokens: number | null;
    total_cost: number | null;
    showTotalBots?: boolean; // Add an explicit flag to control display of total bots
  };
}

const SummaryStats: React.FC<SummaryStatsProps> = ({ stats }) => {
  useTranslation();

  const formatNumber = (num: number | null) => {
    if (num === null) {
      return 'N/A';
    }
    return new Intl.NumberFormat().format(num);
  };

  const formatCost = (cost: number | null) => {
    if (cost === null) {
      return 'N/A';
    }
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(cost);
  };

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      {stats.showTotalBots !== false && (
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Active Assistants</h3>
          <p className="mt-2 text-2xl font-semibold text-gray-900 dark:text-gray-100">
            {formatNumber(stats.total_bots)}
          </p>
        </div>
      )}
      <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Active Users</h3>
        <p className="mt-2 text-2xl font-semibold text-gray-900 dark:text-gray-100">
          {formatNumber(stats.total_users)}
        </p>
      </div>
      <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Sessions</h3>
        <p className="mt-2 text-2xl font-semibold text-gray-900 dark:text-gray-100">
          {formatNumber(stats.total_sessions)}
        </p>
      </div>
      <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Messages</h3>
        <p className="mt-2 text-2xl font-semibold text-gray-900 dark:text-gray-100">
          {formatNumber(stats.total_messages)}
        </p>
      </div>
      {stats.total_input_tokens !== null && (
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Input Tokens</h3>
          <p className="mt-2 text-2xl font-semibold text-gray-900 dark:text-gray-100">
            {formatNumber(stats.total_input_tokens)}
          </p>
        </div>
      )}
      {stats.total_output_tokens !== null && (
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Output Tokens</h3>
          <p className="mt-2 text-2xl font-semibold text-gray-900 dark:text-gray-100">
            {formatNumber(stats.total_output_tokens)}
          </p>
        </div>
      )}
      {stats.total_cost !== null && (
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow flex flex-col">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Conversation Cost</h3>
          <p className="mt-2 text-2xl font-semibold text-gray-900 dark:text-gray-100">
            {formatCost(stats.total_cost)}
          </p>
        </div>
      )}
    </div>
  );
};

export default SummaryStats; 