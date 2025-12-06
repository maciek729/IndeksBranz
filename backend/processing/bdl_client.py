import requests
import time
import pandas as pd
from typing import Dict, List, Optional, Union

class BDLClient:
    BASE_URL = "https://bdl.stat.gov.pl/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"X-ClientId": self.api_key})

    def search_subjects(self, query: str) -> pd.DataFrame:
        url = f"{self.BASE_URL}/subjects/search"
        params = {"name": query, "format": "json", "page-size": 100}
        response = self._make_request(url, params)
        return pd.DataFrame(response.get('results', []))

    def get_variables(self, subject_id: str) -> pd.DataFrame:
        url = f"{self.BASE_URL}/subjects/{subject_id}/variables"
        params = {"format": "json", "page-size": 100}
        response = self._make_request(url, params)
        return pd.DataFrame(response.get('results', []))

    def get_data_by_variable(self, variable_id: int, 
                             year_from: int = 2018, 
                             year_to: int = 2024,
                             unit_level: int = 0) -> pd.DataFrame:

        url = f"{self.BASE_URL}/data/by-variable/{variable_id}"
        params = {
            "format": "json",
            "year": [y for y in range(year_from, year_to + 1)],
            "unit-level": unit_level,
            "page-size": 100
        }
        
        data = []
        response = self._make_request(url, params)
        
        if 'results' in response:
            for item in response['results']:
                unit_name = item.get('name')
                for val in item.get('values', []):
                    data.append({
                        'variable_id': variable_id,
                        'unit': unit_name,
                        'year': val['year'],
                        'value': val['val'],
                        'attr_id': val['attrId']
                    })
        
        return pd.DataFrame(data)

    def _make_request(self, url: str, params: Dict) -> Dict:
        retries = 3
        for i in range(retries):
            try:
                response = self.session.get(url, params=params)
                if response.status_code == 429:
                    time.sleep(2 * (i + 1))
                    continue
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Błąd połączenia z BDL (próba {i+1}): {e}")
                time.sleep(1)
        return {}

if __name__ == "__main__":
    client = BDLClient()
    subjects = client.search_subjects("Finanse przedsiębiorstw")
    print("Znalezione tematy:\n", subjects[['id', 'name']].head())