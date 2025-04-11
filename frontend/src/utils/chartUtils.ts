/**
 * Base interface for chart data points, requiring a date string.
 */
interface BaseChartDataPoint {
    date: string; // Expect YYYY-MM-DD format
}

/**
 * Assumed structure for raw daily usage data points coming from the API.
 */
interface RawDailyUsageDataPoint {
    date: string; // Expect YYYY-MM-DD format
    [key: string]: any;
}

/**
 * Parses a YYYYMMDD string into a Date object using UTC methods.
 * @param dateStr - The date string in YYYYMMDD format.
 * @returns The Date object or null if parsing fails.
 */
export function parseYYYYMMDD(dateStr: string): Date | null {
    if (!/^\d{8}$/.test(dateStr)) return null;
    const year = parseInt(dateStr.substring(0, 4), 10);
    const month = parseInt(dateStr.substring(4, 6), 10); // 1-12
    const day = parseInt(dateStr.substring(6, 8), 10);

    // Validate components (simple check)
    if (year < 1970 || month < 1 || month > 12 || day < 1 || day > 31) {
        return null;
    }

    // Use UTC to avoid timezone issues. Month is 0-indexed for Date constructor.
    const date = new Date(Date.UTC(year, month - 1, day));

    // Final validation check (e.g., Feb 30)
     if (date.getUTCFullYear() !== year || date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) {
        return null;
     }

    return date;
}

/**
 * Formats a Date object into a YYYYMMDD string using UTC methods.
 * @param date - The Date object to format.
 * @returns The formatted date string (YYYYMMDD).
 */
export function formatDateToYYYYMMDD(date: Date): string {
    const year = date.getUTCFullYear();
    const month = (date.getUTCMonth() + 1).toString().padStart(2, '0');
    const day = date.getUTCDate().toString().padStart(2, '0');
    return `${year}${month}${day}`;
}

/**
 * Fills missing dates in a daily usage dataset with zero values.
 * Accepts and outputs dates in YYYYMMDD format.
 *
 * @template T - The type of the chart data point, extending BaseChartDataPoint (expects date as YYYYMMDD string).
 * @param {string} startDateStr - The start date in YYYYMMDD format.
 * @param {string} endDateStr - The end date in YYYYMMDD format.
 * @param {RawDailyUsageDataPoint[]} dailyUsageData - The raw data array from the API (date field format can vary, handled by mapDataPoint).
 * @param {(rawPoint: RawDailyUsageDataPoint) => T} mapDataPoint - Function to map a raw API data point (potentially with YYYY-MM-DD date) to the target chart data point type T (expecting YYYYMMDD date).
 * @param {(dateYYYYMMDD: string) => T} createZeroPoint - Function to create a zero-filled data point for a missing date (receives and expects YYYYMMDD date).
 * @returns {T[]} An array of chart data points (T) with missing dates filled (date property in YYYYMMDD format). Returns an empty array if dates are invalid.
 */
export function fillMissingDatesWithZeros<T extends BaseChartDataPoint>(
    startDateStr: string, // Expect YYYYMMDD
    endDateStr: string,   // Expect YYYYMMDD
    dailyUsageData: RawDailyUsageDataPoint[],
    mapDataPoint: (rawPoint: RawDailyUsageDataPoint) => T,
    createZeroPoint: (dateYYYYMMDD: string) => T // Receives YYYYMMDD
): T[] {
    // Validate date strings (YYYYMMDD check)
    if (!/^\d{8}$/.test(startDateStr) || !/^\d{8}$/.test(endDateStr)) {
        console.warn('Invalid date format provided to fillMissingDatesWithZeros. Expected YYYYMMDD.');
        return [];
    }

    const startDate = parseYYYYMMDD(startDateStr);
    const endDate = parseYYYYMMDD(endDateStr);

    // Further validation
    if (!startDate || !endDate || startDate > endDate) {
        console.warn('Invalid date range provided to fillMissingDatesWithZeros:', startDateStr, endDateStr);
        return [];
    }

    // Create a map for efficient lookup.
    // IMPORTANT: Assumes mapDataPoint correctly handles the date format from dailyUsageData
    // and converts it to YYYYMMDD for the map key if necessary.
    // Simpler if API also returned YYYYMMDD, but we adapt.
    const dailyUsageMap = new Map<string, RawDailyUsageDataPoint>();
    if (Array.isArray(dailyUsageData)) {
         dailyUsageData.forEach(item => {
            if (item && typeof item.date === 'string') {
                // Assuming item.date is YYYY-MM-DD from API, needs conversion for lookup key
                // If API returns YYYYMMDD, this conversion is not needed.
                 try {
                    // Attempt to parse the API date string flexibly
                    let keyDateStr: string | null = null;
                    if (/^\d{4}-\d{2}-\d{2}$/.test(item.date)) {
                         const parsedApiDate = new Date(item.date + 'T00:00:00Z');
                         if (!isNaN(parsedApiDate.getTime())) {
                            keyDateStr = formatDateToYYYYMMDD(parsedApiDate);
                         }
                    } else if (/^\d{8}$/.test(item.date)) {
                         keyDateStr = item.date; // Already in YYYYMMDD
                    }

                    if(keyDateStr) {
                       dailyUsageMap.set(keyDateStr, item);
                    } else {
                       console.warn('Skipping data point with unparseable date:', item);
                    }
                 } catch (e) {
                      console.warn('Error processing date from dailyUsageData:', item.date, e);
                 }

            } else {
                console.warn('Skipping invalid data point in dailyUsageData:', item);
            }
        });
    } else {
         console.warn('dailyUsageData is not an array:', dailyUsageData);
    }


    const filledData: T[] = [];
    let currentDate = new Date(startDate); // Use Date object for iteration
    const maxIterations = 365 * 10;
    let iterations = 0;

    while (currentDate <= endDate && iterations < maxIterations) {
        const dateStrYYYYMMDD = formatDateToYYYYMMDD(currentDate); // Format for lookup and output
        const existingRawData = dailyUsageMap.get(dateStrYYYYMMDD);

        if (existingRawData) {
             try {
                // mapDataPoint is responsible for converting raw data (including its date format)
                // into the desired chart point structure T (which should have date as YYYYMMDD).
                filledData.push(mapDataPoint(existingRawData));
            } catch (error) {
                console.error(`Error mapping data point for date ${dateStrYYYYMMDD}:`, error, existingRawData);
                filledData.push(createZeroPoint(dateStrYYYYMMDD));
            }
        } else {
            // createZeroPoint receives YYYYMMDD and creates a zero point with date as YYYYMMDD.
            filledData.push(createZeroPoint(dateStrYYYYMMDD));
        }

        currentDate.setUTCDate(currentDate.getUTCDate() + 1);
        iterations++;
    }

     if (iterations >= maxIterations) {
        console.warn('fillMissingDatesWithZeros: Reached maximum iteration limit.');
    }

    return filledData; // Data points now have date as YYYYMMDD
}

/**
 * Formats a date tick label for chart X-axis.
 * Converts YYYYMMDD to MM-DD.
 * @param dateStrYYYYMMDD - The date string in YYYYMMDD format.
 * @returns The formatted date string (MM-DD) or the original string if format is invalid.
 */
export function formatChartDateTick(dateStrYYYYMMDD: string): string {
    if (!dateStrYYYYMMDD || dateStrYYYYMMDD.length !== 8 || !/^\d{8}$/.test(dateStrYYYYMMDD)) {
      return dateStrYYYYMMDD; // Return original if format is unexpected
    }
    const month = dateStrYYYYMMDD.substring(4, 6);
    const day = dateStrYYYYMMDD.substring(6, 8);
    return `${month}-${day}`;
}

// === Configuration Constants ===

export const CHART_TICK_FONT_SIZE = 11;
export const X_AXIS_ANGLE = -15;
export const X_AXIS_TEXT_ANCHOR = 'end' as const; // Use 'as const' for specific string literal type
export const X_AXIS_HEIGHT = 50; // Consistent height for angled labels
export const X_AXIS_TICK_MARGIN = 5;
export const Y_AXIS_LABEL_STYLE = { fontSize: 12, fontWeight: 'bold' };
export const Y_AXIS_LABEL_PROPS = { angle: -90, position: 'center' as const };
export const TOOLTIP_STYLE = { fontSize: CHART_TICK_FONT_SIZE }; // Use constant
export const LEGEND_STYLE = { fontSize: CHART_TICK_FONT_SIZE, fontWeight: 600 }; // Use constant
export const DEFAULT_CHART_MARGINS = { top: 10, right: 30, bottom: 60 }; // Consistent base margins

// Dot styles
export const REGULAR_DOT_STYLE = { r: 2.5, strokeWidth: 1 };
export const ACTIVE_DOT_STYLE = { r: 6 };

// === Configuration Calculation Functions ===

/**
 * Calculates chart margins, adjusting left margin based on Y-axis label presence.
 * @param yAxisLabel - Optional Y-axis label string.
 */
export function calculateChartMargins(yAxisLabel?: string) {
  return {
    ...DEFAULT_CHART_MARGINS,
    // Adjust left margin based on label presence - Use a larger fixed value
    left: yAxisLabel ? 15 : 5, // Increased left margin significantly when label exists
  };
}

/**
 * Determines the X-axis tick interval based on data length.
 */
export function calculateXAxisInterval(dataLength: number): number | 'preserveStartEnd' {
  if (dataLength <= 7) {
    return 0; // Show every tick
  } else if (dataLength <= 30) {
    return 6; // Show approx weekly
  } else {
    return 'preserveStartEnd';
  }
}

// === Formatting Utilities ===

/**
 * Formats Y-axis ticks to K/M/B for large numbers (from TokenCountsChart).
 */
export function formatYAxisTick(value: number): string {
  if (value === 0) return '0';
  if (Math.abs(value) >= 1_000_000_000) return `${Math.round(value / 1_000_000_000)}B`;
  if (Math.abs(value) >= 1_000_000) return `${Math.round(value / 1_000_000)}M`;
  if (Math.abs(value) >= 1000) return `${Math.round(value / 1000)}K`;
  return value.toString();
}

/**
 * Formats legend text (from UsageTrendChart).
 * Can be used by both charts if applicable.
 */
export const formatLegendText = (value: string): string => {
  const legendMap: { [key: string]: string } = {
    num_sessions: 'Sessions',
    num_messages: 'Message Count',
    input_tokens: 'Input Tokens',
    output_tokens: 'Output Tokens',
    cost: 'Cost'
  };
  return legendMap[value] || value;
};

/**
 * Formats tooltip values with commas (could be enhanced).
 */
export const formatTooltipValue = (value: number | null): string => {
    if (value === null) return 'N/A';
    return new Intl.NumberFormat().format(value);
};

/**
 * Formats tooltip label from YYYYMMDD to YYYY-MM-DD.
 */
export const formatTooltipLabelDate = (labelYYYYMMDD: string): string => {
    if (labelYYYYMMDD && labelYYYYMMDD.length === 8 && /^\d{8}$/.test(labelYYYYMMDD)) {
        return `${labelYYYYMMDD.substring(0, 4)}-${labelYYYYMMDD.substring(4, 6)}-${labelYYYYMMDD.substring(6, 8)}`;
    }
    return labelYYYYMMDD; // Fallback
};

// === Chart Container Styling ===
// Centralize the container classes used in page components (optional but good for consistency)
export const CHART_CONTAINER_CLASSES = "bg-white dark:bg-gray-800 rounded-lg shadow";
export const CHART_WRAPPER_CLASSES = "w-full h-[300px] p-4 pb-4 pl-4 pr-4 pt-4"; // Standard padding 