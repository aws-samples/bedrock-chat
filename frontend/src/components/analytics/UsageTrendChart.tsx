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

interface UsageTrendChartProps {
  data: AnalyticsDataPoint[];
  title: string;
  dataKey: keyof AnalyticsDataPoint;
  color?: string;
  yAxisLabel?: string;
  yAxisTickFormatter?: (value: number) => string;
}

// Format legend text to be more user-friendly
const formatLegend = (value: string): string => {
  const legendMap: { [key: string]: string } = {
    num_sessions: 'Sessions',
    num_messages: 'Message Count',
    input_tokens: 'Input Tokens',
    output_tokens: 'Output Tokens',
    cost: 'Cost'
  };
  return legendMap[value] || value;
};

const UsageTrendChart: React.FC<UsageTrendChartProps> = ({
  data,
  title,
  dataKey,
  color = '#8884d8',
  yAxisLabel,
  yAxisTickFormatter,
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
            tickMargin={5} // Add some margin between ticks and axis line
            tick={{ fontSize: 11 }} // Use smaller font size for x-axis labels
          />
          <YAxis 
            tickFormatter={yAxisTickFormatter}
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
            tick={{ fontSize: 11 }} // Also make y-axis tick labels smaller
          />
          <Tooltip 
            contentStyle={{ fontSize: '11px' }}
            itemStyle={{ fontSize: '11px' }}
            labelStyle={{ fontSize: '11px' }}
          />
          <Legend 
            formatter={formatLegend}
            wrapperStyle={{ fontSize: '11px', fontWeight: 600 }}
          />
          <Line
            type="monotone"
            dataKey={dataKey}
            name={formatLegend(dataKey as string)}
            stroke={color}
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default UsageTrendChart; 