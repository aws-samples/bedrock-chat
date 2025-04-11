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
  formatLegendText,
  formatTooltipLabelDate,
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

interface UsageTrendChartProps {
  data: AnalyticsDataPoint[];
  title: string;
  dataKey: keyof AnalyticsDataPoint;
  color?: string;
  yAxisLabel?: string;
  yAxisTickFormatter?: (value: number) => string;
}

const UsageTrendChart: React.FC<UsageTrendChartProps> = ({
  data,
  title,
  dataKey,
  color = '#8884d8',
  yAxisLabel,
  yAxisTickFormatter,
}) => {
  useTranslation();

  // Use calculation functions from utils within useMemo
  const chartMargins = useMemo(() => calculateChartMargins(yAxisLabel), [yAxisLabel]);
  const xAxisInterval = useMemo(() => calculateXAxisInterval(data.length), [data.length]);

  return (
    <div className={`${CHART_WRAPPER_CLASSES} ${CHART_CONTAINER_CLASSES}`}>
      {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={chartMargins}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            tickFormatter={formatChartDateTick}
            interval={xAxisInterval}
            angle={X_AXIS_ANGLE}
            textAnchor={X_AXIS_TEXT_ANCHOR}
            height={X_AXIS_HEIGHT}
            tickMargin={X_AXIS_TICK_MARGIN}
            tick={{ fontSize: CHART_TICK_FONT_SIZE }}
          />
          <YAxis
            tickFormatter={yAxisTickFormatter}
            label={{
              value: yAxisLabel,
              ...Y_AXIS_LABEL_PROPS,
              dx: -40,
              style: Y_AXIS_LABEL_STYLE,
            }}
            tick={{ fontSize: CHART_TICK_FONT_SIZE }}
          />
          <Tooltip
            contentStyle={TOOLTIP_STYLE}
            itemStyle={TOOLTIP_STYLE}
            labelStyle={TOOLTIP_STYLE}
            labelFormatter={formatTooltipLabelDate}
          />
          <Legend
            formatter={formatLegendText}
            wrapperStyle={LEGEND_STYLE}
          />
          <Line
            type="monotone"
            dataKey={dataKey}
            name={formatLegendText(dataKey as string)}
            stroke={color}
            activeDot={ACTIVE_DOT_STYLE}
            dot={REGULAR_DOT_STYLE}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default UsageTrendChart; 