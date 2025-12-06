import pandas as pd
import numpy as np
from typing import Dict
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app.config import INDEX_WEIGHTS, CATEGORY_THRESHOLDS

class IndustryIndexCalculator:
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or INDEX_WEIGHTS
        self.thresholds = CATEGORY_THRESHOLDS

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate raw indicators for each industry-year
        Required columns: EN, PEN, GS, NP, liczba_upadlosci
        """
        result = df.copy()

        result['indicator_size'] = result['GS']

        result = result.sort_values(['pkd_division', 'year'])
        result['revenue_prev_year'] = result.groupby('pkd_division')['GS'].shift(1)
        result['indicator_growth'] = (
            (result['GS'] - result['revenue_prev_year']) / result['revenue_prev_year'] * 100
        )

        result['indicator_profitability'] = (result['NP'] / result['GS'] * 100).replace([np.inf, -np.inf], 0)

        result['indicator_risk'] = (result['liczba_upadlosci'] / result['EN'] * 100).replace([np.inf, -np.inf], 0)

        result['indicator_efficiency'] = (result['PEN'] / result['EN'] * 100).replace([np.inf, -np.inf], 0)

        return result

    def normalize_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize indicators to 0-1 scale
        Risk indicator is inverted (lower risk = higher score)
        """
        result = df.copy()

        indicators = ['indicator_size', 'indicator_growth', 'indicator_profitability',
                     'indicator_risk', 'indicator_efficiency']

        for ind in indicators:
            if ind in result.columns:
                result[ind] = result[ind].replace([np.inf, -np.inf], np.nan)

                median_val = result[ind].median()
                result[ind] = result[ind].fillna(median_val)

                min_val = result[ind].min()
                max_val = result[ind].max()

                if max_val > min_val:
                    result[f'{ind}_norm'] = (result[ind] - min_val) / (max_val - min_val)
                else:
                    result[f'{ind}_norm'] = 0.5  
        
        if 'indicator_risk_norm' in result.columns:
            result['indicator_risk_norm'] = 1 - result['indicator_risk_norm']

        return result

    def calculate_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate final Industry Health Index (0-100 scale)
        """
        result = df.copy()

        result['index_raw'] = (
            self.weights['size'] * result['indicator_size_norm'] +
            self.weights['growth'] * result['indicator_growth_norm'] +
            self.weights['profitability'] * result['indicator_profitability_norm'] +
            self.weights['risk'] * result['indicator_risk_norm'] +
            self.weights['efficiency'] * result['indicator_efficiency_norm']
        )

        result['index_score'] = (result['index_raw'] * 100).round(1)

        return result

    def classify_industries(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()

        def get_category(score):
            if score >= self.thresholds['A']:
                return 'A'
            elif score >= self.thresholds['B']:
                return 'B'
            elif score >= self.thresholds['C']:
                return 'C'
            else:
                return 'D'

        result['category'] = result['index_score'].apply(get_category)

        return result

    def get_trend(self, df: pd.DataFrame, periods: int = 3) -> pd.DataFrame:
        """
        Calculate trend direction for each industry
        """
        result = df.copy()
        result = result.sort_values(['pkd_division', 'year'])

        result['index_rolling'] = result.groupby('pkd_division')['index_score'].transform(
            lambda x: x.rolling(window=min(periods, len(x)), min_periods=1).mean()
        )

        result['index_trend'] = result.groupby('pkd_division')['index_rolling'].diff()

        def get_trend_label(val):
            if pd.isna(val):
                return 'stable'
            elif val > 2:
                return 'growing'
            elif val < -2:
                return 'declining'
            else:
                return 'stable'

        result['trend_label'] = result['index_trend'].apply(get_trend_label)

        return result

    def process_full_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Run full processing pipeline:
        1. Calculate indicators
        2. Normalize
        3. Calculate index
        4. Classify
        5. Get trends
        """
        result = df.copy()

        print("Step 1: Calculating indicators...")
        result = self.calculate_indicators(result)

        print("Step 2: Normalizing indicators...")
        result = self.normalize_indicators(result)

        print("Step 3: Calculating index...")
        result = self.calculate_index(result)

        print("Step 4: Classifying industries...")
        result = self.classify_industries(result)

        print("Step 5: Calculating trends...")
        result = self.get_trend(result)

        return result


if __name__ == "__main__":
    from data_loader import DataLoader

    loader = DataLoader()
    data = loader.get_aggregated_data(start_year=2020, end_year=2024)

    calculator = IndustryIndexCalculator()
    result = calculator.process_full_pipeline(data)

    latest = result[result['year'] == result['year'].max()]
    latest_sorted = latest.sort_values('index_score', ascending=False)

    print("\n=== TOP 5 INDUSTRIES ===")
    print(latest_sorted[['pkd_division', 'NAZWA_PKD', 'index_score', 'category']].head())

    print("\n=== BOTTOM 5 INDUSTRIES ===")
    print(latest_sorted[['pkd_division', 'NAZWA_PKD', 'index_score', 'category']].tail())
