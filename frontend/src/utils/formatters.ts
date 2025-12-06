import { CATEGORY_CONFIG, TREND_CONFIG } from '../constants';

export const getCategoryBadge = (category: string) => {
  return CATEGORY_CONFIG[category as keyof typeof CATEGORY_CONFIG] || { label: category, color: '#999' };
};

export const getTrendLabel = (trend: string) => {
  return TREND_CONFIG[trend as keyof typeof TREND_CONFIG]?.symbol || '→';
};

export const getTrendClass = (trend: string) => {
  const config = TREND_CONFIG[trend as keyof typeof TREND_CONFIG];
  if (!config) return 'trendStable';

  if (config.class === 'trend-up') return 'trendUp';
  if (config.class === 'trend-down') return 'trendDown';
  return 'trendStable';
};
