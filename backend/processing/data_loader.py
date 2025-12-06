import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

class DataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.bankruptcies_df = None
        self.financials_df = None
        self.mapping_df = None

    def load_pkd_mapping(self) -> pd.DataFrame:
        """Load PKD 2007 -> 2025 mapping"""
        if self.mapping_df is None:
            file_path = self.data_dir / "mapowanie_pkd.xlsx"
            self.mapping_df = pd.read_excel(file_path)
        return self.mapping_df

    def load_bankruptcies(self) -> pd.DataFrame:
        """Load bankruptcy data from CSV"""
        file_path = self.data_dir / "krz_pkd.csv"
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')

        df['pkd_group'] = df['pkd'].str[:4]

        self.bankruptcies_df = df
        return df

    def load_financials(self) -> pd.DataFrame:
        """Load financial indicators from CSV"""
        file_path = self.data_dir / "wsk_fin.csv"
        df = pd.read_csv(file_path, sep=';', encoding='utf-8', decimal=',')

        df_group = df[df['PKD'].str.match(r'^\d{2}\.\d$', na=False)].copy()

        df_group['pkd_group'] = df_group['PKD'].str.replace('.', '')

        self.financials_df = df_group
        return df_group

    def pivot_financials(self) -> pd.DataFrame:
        """Transform financial data from wide to long format"""
        if self.financials_df is None:
            self.load_financials()

        year_cols = [col for col in self.financials_df.columns if col.isdigit()]

        self.financials_df['indicator_code'] = self.financials_df['WSKAZNIK'].str.split(' ').str[0]

        df_long = pd.melt(
            self.financials_df,
            id_vars=['PKD', 'NAZWA_PKD', 'indicator_code', 'pkd_group'],
            value_vars=year_cols,
            var_name='year',
            value_name='value'
        )

        df_long['year'] = df_long['year'].astype(int)

        df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')

        return df_long

    def get_aggregated_data(self, start_year: int = 2018, end_year: int = 2024) -> pd.DataFrame:
        """
        Get aggregated data combining bankruptcies and financial indicators
        at group level (3 digits) with PKD 2025 mapping
        """
        bankruptcies = self.load_bankruptcies()
        financials_long = self.pivot_financials()
        mapping = self.load_pkd_mapping()

        bankruptcies = bankruptcies[
            (bankruptcies['rok'] >= start_year) &
            (bankruptcies['rok'] <= end_year)
        ]
        financials_long = financials_long[
            (financials_long['year'] >= start_year) &
            (financials_long['year'] <= end_year)
        ]

        bankruptcies_agg = bankruptcies.groupby(['rok', 'pkd_group']).agg({
            'liczba_upadlosci': 'sum'
        }).reset_index()
        bankruptcies_agg.rename(columns={'rok': 'year'}, inplace=True)

        financials_wide = financials_long.pivot_table(
            index=['pkd_group', 'year', 'NAZWA_PKD'],
            columns='indicator_code',
            values='value',
            aggfunc='first'
        ).reset_index()

        financials_wide.columns.name = None

        merged = pd.merge(
            financials_wide,
            bankruptcies_agg,
            on=['pkd_group', 'year'],
            how='left'
        )

        merged['liczba_upadlosci'] = merged['liczba_upadlosci'].fillna(0)

        mapping_3digit = mapping[mapping['symbol_2007'].str.match(r'^\d{2}\.\d$', na=False)].copy()
        mapping_3digit['pkd_group_2007'] = mapping_3digit['symbol_2007'].str.replace('.', '')
        mapping_3digit['pkd_group_2025'] = mapping_3digit['symbol_2025'].str.replace('.', '')
        mapping_3digit = mapping_3digit[['pkd_group_2007', 'pkd_group_2025']]

        merged = pd.merge(
            merged,
            mapping_3digit,
            left_on='pkd_group',
            right_on='pkd_group_2007',
            how='left'
        )

        merged['pkd_2025'] = merged['pkd_group_2025'].fillna(merged['pkd_group'])
        merged['pkd_2007'] = merged['pkd_group']

        merged = merged.drop(columns=['pkd_group_2007', 'pkd_group_2025'])

        return merged

    def get_industry_names(self) -> Dict[str, str]:
        """Get mapping of PKD codes to industry names"""
        if self.financials_df is None:
            self.load_financials()

        return dict(zip(
            self.financials_df['pkd_group'],
            self.financials_df['NAZWA_PKD']
        ))


if __name__ == "__main__":
    loader = DataLoader()
    data = loader.get_aggregated_data()
    print(f"Loaded {len(data)} rows")
    print(f"\nColumns: {data.columns.tolist()}")
    print(f"\nSample data:\n{data.head()}")
    print(f"\nYears: {sorted(data['year'].unique())}")
    print(f"\nIndustries PKD 2007: {sorted(data['pkd_2007'].unique())}")
    print(f"\nIndustries PKD 2025: {sorted(data['pkd_2025'].unique())}")
    print(f"\nNumber of industries: {len(data['pkd_group'].unique())}")
