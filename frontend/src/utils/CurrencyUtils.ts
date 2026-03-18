// Approximate fixed exchange rate: 1 USD = USD_TO_AUD AUD.
// Update this constant to reflect the current rate.
export const USD_TO_AUD = 1.6;

const audFormatter = new Intl.NumberFormat('en-AU', {
  style: 'currency',
  currency: 'AUD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

/** Convert a USD amount to AUD and return a formatted string, e.g. "A$2.56". */
export const formatCostAUD = (usdAmount: number): string => {
  return audFormatter.format(usdAmount * USD_TO_AUD);
};
