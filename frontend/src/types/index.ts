export interface Industry {
  pkd_code: string;
  pkd_2007: string;
  pkd_2025: string;
  name: string;
  index_score: number;
  category: 'A' | 'B' | 'C' | 'D';
  trend: 'growing' | 'stable' | 'declining';
  metrics: {
    revenue: number;
    growth_rate: number;
    profit_margin: number;
    bankruptcy_rate: number;
    profitable_share: number;
  };
}

export interface Stats {
  total_industries: number;
  last_update: string;
  top_industry: {
    code: string;
    name: string;
    score: number;
  };
  worst_industry: {
    code: string;
    name: string;
    score: number;
  };
  categories: {
    A: number;
    B: number;
    C: number;
    D: number;
  };
}

export interface Ranking {
  year: number;
  top: Array<{
    pkd_code: string;
    pkd_2007: string;
    pkd_2025: string;
    name: string;
    index_score: number;
    category: string;
    trend: string;
  }>;
  bottom: Array<{
    pkd_code: string;
    pkd_2007: string;
    pkd_2025: string;
    name: string;
    index_score: number;
    category: string;
    trend: string;
  }>;
}

export interface IndustriesResponse {
  year: number;
  count: number;
  industries: Industry[];
}
