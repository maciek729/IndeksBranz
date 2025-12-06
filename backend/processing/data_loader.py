import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

class DataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.bankruptcies_df = None
        self.financials_df = None

    def load_bankruptcies(self) -> pd.DataFrame:
        """Load bankruptcy data from CSV"""
        file_path = self.data_dir / "krz_pkd.csv"
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')

        # Convert PKD to 2-digit (division level)
        df['pkd_division'] = df['pkd'].str[:2]

        self.bankruptcies_df = df
        return df

    def load_financials(self) -> pd.DataFrame:
        """Load financial indicators from CSV"""
        file_path = self.data_dir / "wsk_fin.csv"
        df = pd.read_csv(file_path, sep=';', encoding='utf-8', decimal=',')

        # Filter only division level (2 digits) - more data availability
        # Division codes are like "01.", "02.", etc.
        df_division = df[df['PKD'].str.match(r'^\d{2}\.$', na=False)].copy()

        # Clean PKD code - remove the dot
        df_division['pkd_division'] = df_division['PKD'].str.replace('.', '')

        self.financials_df = df_division
        return df_division

    def pivot_financials(self) -> pd.DataFrame:
        """Transform financial data from wide to long format"""
        if self.financials_df is None:
            self.load_financials()

        # Get year columns (2005-2024)
        year_cols = [col for col in self.financials_df.columns if col.isdigit()]

        # Extract indicator code (first part before space) from WSKAZNIK column
        # e.g., "EN Liczba jednostek gospodarczych " -> "EN"
        self.financials_df['indicator_code'] = self.financials_df['WSKAZNIK'].str.split(' ').str[0]

        # Pivot to long format
        df_long = pd.melt(
            self.financials_df,
            id_vars=['PKD', 'NAZWA_PKD', 'indicator_code', 'pkd_division'],
            value_vars=year_cols,
            var_name='year',
            value_name='value'
        )

        # Convert year to int
        df_long['year'] = df_long['year'].astype(int)

        # Convert value to numeric (handle commas if any)
        df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')

        return df_long

    def get_aggregated_data(self, start_year: int = 2018, end_year: int = 2024) -> pd.DataFrame:
        """
        Get aggregated data combining bankruptcies and financial indicators
        at division level (2 digits)
        """
        # Load data
        bankruptcies = self.load_bankruptcies()
        financials_long = self.pivot_financials()

        # Filter years
        bankruptcies = bankruptcies[
            (bankruptcies['rok'] >= start_year) &
            (bankruptcies['rok'] <= end_year)
        ]
        financials_long = financials_long[
            (financials_long['year'] >= start_year) &
            (financials_long['year'] <= end_year)
        ]

        # Aggregate bankruptcies to division level
        bankruptcies_agg = bankruptcies.groupby(['rok', 'pkd_division']).agg({
            'liczba_upadlosci': 'sum'
        }).reset_index()
        bankruptcies_agg.rename(columns={'rok': 'year'}, inplace=True)

        # Pivot financial indicators to wide format (one row per PKD-year)
        financials_wide = financials_long.pivot_table(
            index=['pkd_division', 'year', 'NAZWA_PKD'],
            columns='indicator_code',
            values='value',
            aggfunc='first'
        ).reset_index()

        # Reset column names (remove multi-index from columns)
        financials_wide.columns.name = None

        # Merge
        merged = pd.merge(
            financials_wide,
            bankruptcies_agg,
            on=['pkd_division', 'year'],
            how='left'
        )

        # Fill NaN bankruptcies with 0
        merged['liczba_upadlosci'] = merged['liczba_upadlosci'].fillna(0)

        return merged

    def get_industry_names(self) -> Dict[str, str]:
        """Get mapping of PKD codes to industry names"""
        if self.financials_df is None:
            self.load_financials()

        return dict(zip(
            self.financials_df['pkd_division'],
            self.financials_df['NAZWA_PKD']
        ))


if __name__ == "__main__":
    # Test the loader
    loader = DataLoader()
    data = loader.get_aggregated_data()
    print(f"Loaded {len(data)} rows")
    print(f"\nColumns: {data.columns.tolist()}")
    print(f"\nSample data:\n{data.head()}")
    print(f"\nYears: {sorted(data['year'].unique())}")
    print(f"\nIndustries: {sorted(data['pkd_division'].unique())}")
