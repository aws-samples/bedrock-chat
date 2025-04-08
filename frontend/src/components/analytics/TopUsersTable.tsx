import React from 'react';
import { useTranslation } from 'react-i18next';
import { UsagePerUser } from '../../hooks/useAnalytics';

interface TopUsersTableProps {
  users: UsagePerUser[];
  title: string;
}

const TopUsersTable: React.FC<TopUsersTableProps> = ({ users, title }) => {
  useTranslation();

  // Check if any user has cost data to display
  const hasAnyCostData = users.some(user => user.total_price !== null);

  return (
    <div className="space-y-4 bg-white dark:bg-gray-800 rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold">{title}</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead>
            <tr>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Email
              </th>
              <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Sessions
              </th>
              <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Messages
              </th>
              {hasAnyCostData && (
                <th className="px-3 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Conversation Cost
                </th>
              )}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {users.map((user, index) => (
              <tr key={`user-${user.id}-${index}`}>
                <td className="px-3 py-2 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100">
                  {user.email || `User ${user.id.substring(0, 8)}`}
                </td>
                <td className="px-3 py-2 text-right text-sm text-gray-500 dark:text-gray-400">
                  {user.num_sessions}
                </td>
                <td className="px-3 py-2 text-right text-sm text-gray-500 dark:text-gray-400">
                  {user.num_messages}
                </td>
                {hasAnyCostData && (
                  <td className="px-3 py-2 text-right text-sm text-gray-500 dark:text-gray-400">
                    {user.total_price !== null ? `$${user.total_price.toFixed(3)}` : 'N/A'}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TopUsersTable; 