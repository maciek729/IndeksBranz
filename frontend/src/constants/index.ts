export const CATEGORY_CONFIG = {
  A: { label: 'Rozwijające się', color: '#00A65A' },
  B: { label: 'Stabilne', color: '#DC0028' },
  C: { label: 'Monitorowanie', color: '#FF6B00' },
  D: { label: 'Ryzykowne', color: '#8a0019' },
} as const;

export const TREND_CONFIG = {
  growing: { symbol: '↗', color: '#00A65A', class: 'trend-up' },
  declining: { symbol: '↘', color: '#DC0028', class: 'trend-down' },
  stable: { symbol: '→', color: '#666', class: 'trend-stable' },
} as const;

export const API_BASE_URL = 'http://localhost:8000';
