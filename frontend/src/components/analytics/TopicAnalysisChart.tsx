import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { TopicAnalysis } from '../../hooks/useAnalytics';

interface TopicAnalysisChartProps {
  data: TopicAnalysis[];
  title: string;
}

const TopicAnalysisChart: React.FC<TopicAnalysisChartProps> = ({
  data,
  title,
}) => {
  return (
    <div className="w-full h-[300px] p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="topic" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="message_count" fill="#8884d8" name="Messages" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TopicAnalysisChart; 