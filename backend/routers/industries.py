from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter(prefix="/api", tags=["industries"])

processed_data = None

def set_processed_data(data):
    global processed_data
    processed_data = data

@router.get("/stats")
def get_statistics():
    latest_year = processed_data['year'].max()
    latest_data = processed_data[processed_data['year'] == latest_year]

    top_industry = latest_data.nlargest(1, 'index_score').iloc[0]
    worst_industry = latest_data.nsmallest(1, 'index_score').iloc[0]
    category_counts = latest_data['category'].value_counts().to_dict()

    return {
        "total_industries": int(latest_data['pkd_division'].nunique()),
        "last_update": f"{int(latest_year)}-12-31",
        "top_industry": {
            "code": top_industry['pkd_division'],
            "name": top_industry['NAZWA_PKD'],
            "score": float(top_industry['index_score'])
        },
        "worst_industry": {
            "code": worst_industry['pkd_division'],
            "name": worst_industry['NAZWA_PKD'],
            "score": float(worst_industry['index_score'])
        },
        "categories": {
            "A": int(category_counts.get('A', 0)),
            "B": int(category_counts.get('B', 0)),
            "C": int(category_counts.get('C', 0)),
            "D": int(category_counts.get('D', 0))
        }
    }

@router.get("/industries")
def get_industries(
    year: Optional[int] = None,
    category: Optional[str] = None,
    limit: Optional[int] = None
):
    if year is None:
        year = int(processed_data['year'].max())

    data = processed_data[processed_data['year'] == year].copy()

    if category:
        data = data[data['category'] == category.upper()]

    data = data.sort_values('index_score', ascending=False)

    if limit:
        data = data.head(limit)

    industries = []
    for _, row in data.iterrows():
        industries.append({
            "pkd_code": row['pkd_division'],
            "name": row['NAZWA_PKD'],
            "index_score": float(row['index_score']),
            "category": row['category'],
            "trend": row['trend_label'],
            "metrics": {
                "revenue": float(row.get('GS', 0)),
                "growth_rate": float(row.get('indicator_growth', 0)),
                "profit_margin": float(row.get('indicator_profitability', 0)),
                "bankruptcy_rate": float(row.get('indicator_risk', 0)),
                "profitable_share": float(row.get('indicator_efficiency', 0))
            }
        })

    return {
        "year": year,
        "count": len(industries),
        "industries": industries
    }

@router.get("/industries/{pkd_code}")
def get_industry_details(pkd_code: str):
    industry_data = processed_data[processed_data['pkd_division'] == pkd_code].copy()

    if len(industry_data) == 0:
        raise HTTPException(status_code=404, detail="Industry not found")

    industry_data = industry_data.sort_values('year')
    latest = industry_data.iloc[-1]

    timeline = []
    for _, row in industry_data.iterrows():
        timeline.append({
            "year": int(row['year']),
            "index_score": float(row['index_score']),
            "category": row['category'],
            "revenue": float(row.get('GS', 0)),
            "bankruptcies": int(row.get('liczba_upadlosci', 0)),
            "companies_count": int(row.get('EN', 0))
        })

    return {
        "pkd_code": pkd_code,
        "name": latest['NAZWA_PKD'],
        "current_score": float(latest['index_score']),
        "current_category": latest['category'],
        "trend": latest['trend_label'],
        "timeline": timeline,
        "latest_metrics": {
            "revenue": float(latest.get('GS', 0)),
            "growth_rate": float(latest.get('indicator_growth', 0)),
            "profit_margin": float(latest.get('indicator_profitability', 0)),
            "bankruptcy_rate": float(latest.get('indicator_risk', 0)),
            "profitable_share": float(latest.get('indicator_efficiency', 0)),
            "companies_count": int(latest.get('EN', 0)),
            "profitable_count": int(latest.get('PEN', 0)),
            "bankruptcies": int(latest.get('liczba_upadlosci', 0))
        }
    }

@router.get("/ranking")
def get_ranking(year: Optional[int] = None, top: int = 10):
    if year is None:
        year = int(processed_data['year'].max())

    data = processed_data[processed_data['year'] == year].copy()
    data = data.sort_values('index_score', ascending=False)

    def format_industry(row):
        return {
            "pkd_code": row['pkd_division'],
            "name": row['NAZWA_PKD'],
            "index_score": float(row['index_score']),
            "category": row['category'],
            "trend": row['trend_label']
        }

    top_industries = [format_industry(row) for _, row in data.head(top).iterrows()]
    bottom_industries = [format_industry(row) for _, row in data.tail(top).iterrows()]

    return {
        "year": year,
        "top": top_industries,
        "bottom": bottom_industries[::-1]
    }
