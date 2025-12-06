import os
import pandas as pd
from typing import Dict, List, Optional
from gusregon import GUS
from .bdl_client import BDLClient

class GusIntegrationService:
    def __init__(self, bdl_api_key: str = None, regon_api_key: str = None):
        self.bdl_client = BDLClient(api_key=bdl_api_key)
        
        self.regon_client = GUS(api_key=regon_api_key, sandbox=True if not regon_api_key else False)

    def get_industry_stats(self, pkd_code: str, year: int) -> Dict:
        stats = {
            'entity_count': 0,
            'year': year,
            'source': 'BDL'
        }
        
        # Logika pobierania z BDL (jak w poprzednim kroku)
        # variable_id = self.find_variable_for_pkd(pkd_code)
        # data = self.bdl_client.get_data_by_variable(variable_id, year_from=year, year_to=year)
        # if not data.empty:
        #    stats['entity_count'] = data.iloc[0]['value']
            
        return stats

    def get_company_info(self, nip: str) -> Dict:
        try:
            data = self.regon_client.search(nip=nip)
            if data:
                return {
                    'name': data['nazwa'],
                    'pkd': data['silosID'],
                    'city': data['miejscowosc'],
                    'status': 'Aktywna' 
                }
        except Exception as e:
            print(f"Błąd REGON dla NIP {nip}: {e}")
        return {}

    def get_industry_report(self, pkd_code: str, sample_nips: List[str] = []) -> Dict:
        stats = self.get_industry_stats(pkd_code, 2023)
        
        companies = []
        for nip in sample_nips:
            info = self.get_company_info(nip)
            if info:
                companies.append(info)
                
        return {
            'pkd': pkd_code,
            'statistics': stats,
            'sample_companies': companies
        }