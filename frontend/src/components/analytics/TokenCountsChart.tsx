import React, { useRef, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

// Define chart data interface here to avoid circular dependencies
interface AnalyticsDataPoint {
  date: string;
  num_messages: number;
  input_tokens: number | null;
  output_tokens: number | null;
  cost: number | null;
  num_sessions: number;
}

interface TokenCountsChartProps {
  data: AnalyticsDataPoint[];
  title: string;
  yAxisLabel?: string;
}

/**
 * Format large numbers to abbreviated format (K, M, B)
 */
const formatYAxisTick = (value: number): string => {
  if (value === 0) {
    return '0';
  }
  
  if (Math.abs(value) >= 1000000000) {
    return `${Math.round(value / 1000000000)}B`;
  }
  if (Math.abs(value) >= 1000000) {
    return `${Math.round(value / 1000000)}M`;
  }
  if (Math.abs(value) >= 1000) {
    return `${Math.round(value / 1000)}K`;
  }
  
  return value.toString();
};

const TokenCountsChart: React.FC<TokenCountsChartProps> = ({
  data,
  title,
  yAxisLabel = 'Token Count',
}) => {
  useTranslation();
  const lastYearRef = useRef<string>('');

  // Format date to show year only when it changes
  const formatXAxis = (dateStr: string) => {
    if (!dateStr) {
      return '';
    }
    
    const parts = dateStr.split('-');
    if (parts.length !== 3) {
      return dateStr;
    }
    
    const year = parts[0];
    const month = parts[1];
    const day = parts[2];
    
    // If this is the first date or the year has changed, show the full date
    if (year !== lastYearRef.current) {
      lastYearRef.current = year;
      return `${year}-${month}-${day}`;
    }
    
    // Otherwise just show month-day
    return `${month}-${day}`;
  };

  // Determine the appropriate interval based on the date range
  const xAxisInterval = useMemo(() => {
    // For short date ranges (14 days or less), show all labels
    if (data.length <= 14) {
      return 0; // 0 means show every tick
    }
    // For medium ranges (15-30 days), show every other day
    else if (data.length <= 30) {
      return 1; // Show every other tick
    }
    // For longer ranges, use preserveStartEnd to just show first, last and some in between
    else {
      return 'preserveStartEnd';
    }
  }, [data.length]);

  // Calculate chart margins based on data length
  const chartMargins = useMemo(() => {
    const isShortRange = data.length <= 14;
    return {
      top: 10,
      right: isShortRange ? 30 : 20, // Increase right margin for short ranges with angled labels
      bottom: isShortRange ? 60 : 30, // Increase bottom margin for short ranges
      left: yAxisLabel ? 10 : 15 // Increased left margin for axis label
    };
  }, [data.length, yAxisLabel]);

  // Custom tooltip formatter to show formatted values
  const formatTooltipValue = (value: number | null) => {
    if (value === null) {
      return 'N/A';
    }
    return new Intl.NumberFormat().format(value);
  };

  // Custom tooltip component to show formatted values
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-2 border border-gray-200 dark:border-gray-700 shadow-md rounded" style={{ fontSize: '11px' }}>
          <p className="text-gray-600 dark:text-gray-300">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={`tooltip-${index}`} style={{ color: entry.color }}>
              {entry.name}: {formatTooltipValue(entry.value)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-[300px] p-4 pb-4 pl-2 pr-4 pt-4 bg-white dark:bg-gray-800 rounded-lg shadow">
      {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height="100%">
        <LineChart 
          data={data}
          margin={chartMargins}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tickFormatter={formatXAxis}
            interval={xAxisInterval}
            angle={data.length > 14 ? 0 : -15}
            textAnchor={data.length > 14 ? 'middle' : 'end'}
            height={data.length > 14 ? 30 : 50}
            tickMargin={5}
            tick={{ fontSize: 11 }}
          />
          <YAxis 
            tickFormatter={formatYAxisTick}
            label={{ 
              value: yAxisLabel, 
              angle: -90, 
              position: 'center', 
              offset: -5,
              dx: -30,
              style: { 
                fontSize: 12,
                fontWeight: 'bold'
              } 
            }} 
            tick={{ fontSize: 11 }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: '11px', fontWeight: 600 }} />
          <Line
            type="monotone"
            dataKey="input_tokens"
            name="Input Tokens"
            stroke="#8884d8"
            strokeWidth={2}
            dot={{ r: 3 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="output_tokens"
            name="Output Tokens"
            stroke="#82ca9d"
            strokeWidth={2}
            dot={{ r: 3 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TokenCountsChart; 