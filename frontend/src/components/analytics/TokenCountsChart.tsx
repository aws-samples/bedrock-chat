import React, { useMemo } from 'react';
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
import {
  formatChartDateTick,
  formatYAxisTick,
  formatTooltipLabelDate,
  formatTooltipValue,
  formatLegendText,
  calculateChartMargins,
  calculateXAxisInterval,
  CHART_TICK_FONT_SIZE,
  X_AXIS_ANGLE,
  X_AXIS_TEXT_ANCHOR,
  X_AXIS_HEIGHT,
  X_AXIS_TICK_MARGIN,
  Y_AXIS_LABEL_STYLE,
  Y_AXIS_LABEL_PROPS,
  TOOLTIP_STYLE,
  LEGEND_STYLE,
  CHART_CONTAINER_CLASSES,
  CHART_WRAPPER_CLASSES,
  REGULAR_DOT_STYLE,
  ACTIVE_DOT_STYLE
} from '../../utils/chartUtils';

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

const TokenCountsChart: React.FC<TokenCountsChartProps> = ({
  data,
  title,
  yAxisLabel = 'Token Count',
}) => {
  useTranslation();

  // Use calculation functions from utils within useMemo
  const chartMargins = useMemo(() => calculateChartMargins(yAxisLabel), [yAxisLabel]);
  const xAxisInterval = useMemo(() => calculateXAxisInterval(data.length), [data.length]);

  // Define a simple custom tooltip content function using shared formatters
  const renderCustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const formattedLabel = formatTooltipLabelDate(label); // Use util
      return (
        <div className="bg-white dark:bg-gray-800 p-2 border border-gray-200 dark:border-gray-700 shadow-md rounded" style={TOOLTIP_STYLE}>
          <p className="text-gray-600 dark:text-gray-300">{formattedLabel}</p>
          {payload.map((entry: any, index: number) => (
            <p key={`tooltip-${index}`} style={{ color: entry.color }}>
              {formatLegendText(entry.name)}: {formatTooltipValue(entry.value)} {/* Use utils */}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    // Use wrapper classes constant
    <div className={`${CHART_WRAPPER_CLASSES} ${CHART_CONTAINER_CLASSES}`}>
      {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={chartMargins}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            tickFormatter={formatChartDateTick} // Use util
            interval={xAxisInterval} // Use calculated interval
            angle={X_AXIS_ANGLE} // Use constant
            textAnchor={X_AXIS_TEXT_ANCHOR} // Use constant
            height={X_AXIS_HEIGHT} // Use constant
            tickMargin={X_AXIS_TICK_MARGIN} // Use constant
            tick={{ fontSize: CHART_TICK_FONT_SIZE }} // Use constant
          />
          <YAxis
            tickFormatter={formatYAxisTick} // Use util
            label={{
              value: yAxisLabel,
              ...Y_AXIS_LABEL_PROPS, // Use constant props
              dx: -40, // Reset dx, rely on margin
              style: Y_AXIS_LABEL_STYLE, // Use constant style
            }}
            tick={{ fontSize: CHART_TICK_FONT_SIZE }} // Use constant
          />
          {/* Use simplified custom tooltip */}
          <Tooltip content={renderCustomTooltip} />
          <Legend
            formatter={formatLegendText} // Use util
            wrapperStyle={LEGEND_STYLE} // Use constant
          />
          {/* Keep the two specific Line components */}
          <Line type="monotone" dataKey="input_tokens" name="Input Tokens" stroke="#8884d8" dot={REGULAR_DOT_STYLE} activeDot={ACTIVE_DOT_STYLE} />
          <Line type="monotone" dataKey="output_tokens" name="Output Tokens" stroke="#82ca9d" dot={REGULAR_DOT_STYLE} activeDot={ACTIVE_DOT_STYLE}/>
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TokenCountsChart; 