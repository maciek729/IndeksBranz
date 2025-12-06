from pydantic import BaseModel
from typing import List, Literal

class IndustryMetrics(BaseModel):
    revenue: float
    growth_rate: float
    profit_margin: float
    bankruptcy_rate: float
    profitable_share: float

class Industry(BaseModel):
    pkd_code: str
    name: str
    index_score: float
    category: Literal['A', 'B', 'C', 'D']
    trend: Literal['growing', 'stable', 'declining']
    metrics: IndustryMetrics

class TopIndustry(BaseModel):
    code: str
    name: str
    score: float

class CategoryCounts(BaseModel):
    A: int
    B: int
    C: int
    D: int

class Stats(BaseModel):
    total_industries: int
    last_update: str
    top_industry: TopIndustry
    worst_industry: TopIndustry
    categories: CategoryCounts

class RankingItem(BaseModel):
    pkd_code: str
    name: str
    index_score: float
    category: str
    trend: str

class Ranking(BaseModel):
    year: int
    top: List[RankingItem]
    bottom: List[RankingItem]

class IndustriesResponse(BaseModel):
    year: int
    count: int
    industries: List[Industry]

class TimelineItem(BaseModel):
    year: int
    index_score: float
    category: str
    revenue: float
    bankruptcies: int
    companies_count: int

class IndustryMetricsDetailed(BaseModel):
    revenue: float
    growth_rate: float
    profit_margin: float
    bankruptcy_rate: float
    profitable_share: float
    companies_count: int
    profitable_count: int
    bankruptcies: int

class IndustryDetails(BaseModel):
    pkd_code: str
    name: str
    current_score: float
    current_category: str
    trend: str
    timeline: List[TimelineItem]
    latest_metrics: IndustryMetricsDetailed
