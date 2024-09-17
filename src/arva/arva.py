from typing import List, Dict, Any, Optional, IO
import requests
import json
import os
from requests_toolbelt import MultipartEncoder

class Arva:
    def __init__(self, api_key: str, base_url: str = 'http://platform.arva-ai.com/api/v0') -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.customers = self.Customers(self)

    class Customers:
        def __init__(self, arva_instance: 'Arva') -> None:
            self.arva_instance = arva_instance

        def create(self, agent_id: str, registered_name: str, state: str) -> Dict[str, Any]:
            url = f"{self.arva_instance.base_url}/customer/create"
            headers = {'Authorization': f'Bearer {self.arva_instance.api_key}'}
            payload = {
                'registeredName': registered_name,
                'state': state,
                'agentId': agent_id
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        
        def update(self, id: str, user_info_patch: Dict[str, Any], websites: Optional[List[str]] = None, files: Optional[List[IO[bytes]]] = None) -> Dict[str, Any]:
            url = f"{self.arva_instance.base_url}/customer/update"
            headers = {'Authorization': f'Bearer {self.arva_instance.api_key}'}

            if websites is None:
                websites = []
            if files is None:
                files = []

            file_tuples = [
                ('file', (os.path.basename(os.path.abspath(f.name)), f, 'application/pdf')) for f in files
            ]

            fields = [
                ('customerId', id),
                ('userInfoPatch', json.dumps(user_info_patch)),
                ('websites', json.dumps(websites)),
            ] + file_tuples

            mp_encoder: MultipartEncoder = MultipartEncoder(fields=fields)
            headers['Content-Type'] = mp_encoder.content_type

            response = requests.post(url, headers=headers, data=mp_encoder)
            response.raise_for_status()
            return response.json()
        
        def getById(self, id: str) -> Dict[str, Any]:
            url = f"{self.arva_instance.base_url}/customer/getById?id={id}"
            headers = {'Authorization': f'Bearer {self.arva_instance.api_key}'}

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    
        def review(self, id: str, verdict: str, reason: str, rfi: Optional[str] = None) -> Dict[str, Any]:
            url = f"{self.arva_instance.base_url}/customer/review"
            headers = {'Authorization': f'Bearer {self.arva_instance.api_key}'}
            payload = {
                'customerId': id,
                'verdict': verdict,
                'reason': reason,
                'rfi': rfi
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
