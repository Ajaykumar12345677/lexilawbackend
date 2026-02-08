import json
import os
from typing import List, Dict

class LegalDataLoader:
    def __init__(self, data_dir: str = "app/data"):
        self.data_dir = data_dir
        self.ipc_data = []
        self.crpc_data = []
        self.combined_data = []

    def load_data(self):
        # Load IPC
        ipc_path = os.path.join(self.data_dir, "ipc.json")
        if os.path.exists(ipc_path):
            with open(ipc_path, "r", encoding="utf-8") as f:
                raw_ipc = json.load(f)
                self.ipc_data = self._process_ipc(raw_ipc)
        
        # Load CrPC
        crpc_path = os.path.join(self.data_dir, "crpc.json")
        if os.path.exists(crpc_path):
            with open(crpc_path, "r", encoding="utf-8") as f:
                raw_crpc = json.load(f)
                self.crpc_data = self._process_crpc(raw_crpc)
        
        self.combined_data = self.ipc_data + self.crpc_data
        print(f"Loaded {len(self.ipc_data)} IPC sections and {len(self.crpc_data)} CrPC sections.")
        return self.combined_data

    def _process_ipc(self, data: List[Dict]) -> List[Dict]:
        processed = []
        for item in data:
            # Safely handle section key
            raw_sec = item.get('section')
            if raw_sec is None:
                sec = ""
            else:
                sec = str(raw_sec).replace('section-', '')
            
            # Helper to clean "nan" values
            def clean(val):
                s = str(val).strip()
                if s.lower() == 'nan' or s.lower() == 'none' or not s:
                    return ""
                return s

            desc = clean(item.get('desc'))
            simple_desc = clean(item.get('simpleDesc'))
            offence = clean(item.get('offence'))
            punishment = clean(item.get('Punishment'))
            bailable = clean(item.get('bailable'))
            cognizable = clean(item.get('cognizable'))
            
            # Fallbacks if important fields are missing
            if not offence: offence = 'Legal Offense'
            if not punishment: punishment = 'See detailed legal section for punishment'

            processed.append({
                "code": f"IPC {sec}",
                "source": "IPC",
                "section_number": sec,
                "title": offence,
                "description": desc,
                "simple_desc": simple_desc,
                "punishment": punishment,
                "bailable": bailable,
                "cognizable": cognizable,
                "court": clean(item.get('court')),
                "search_text": f"{desc} {simple_desc} {offence}"
            })
        return processed

    def _process_crpc(self, data: List[Dict]) -> List[Dict]:
        processed = []
        for item in data:
            raw_sec = item.get('section')
            if raw_sec is None:
                sec = ""
            else:
                sec = str(raw_sec).replace('section-', '')
            
            def clean(val):
                s = str(val).strip()
                if s.lower() == 'nan' or s.lower() == 'none' or not s:
                    return ""
                return s

            desc = clean(item.get('desc'))
            simple_desc = clean(item.get('simpleDesc'))
            # Keywords might be list or string
            raw_keywords = item.get('keywords', [])
            if isinstance(raw_keywords, list):
                keywords = " ".join([str(k) for k in raw_keywords])
            else:
                keywords = str(raw_keywords)
            
            punishment = clean(item.get('punishment'))
            if not punishment: punishment = 'Procedural / Not specified'

            processed.append({
                "code": f"CrPC {sec}",
                "source": "CrPC",
                "section_number": sec,
                "title": f"Section {sec}",
                "description": desc,
                "simple_desc": simple_desc,
                "punishment": punishment,
                "bailable": "See Description",
                "cognizable": "See Description",
                "search_text": f"{desc} {simple_desc} {keywords}"
            })
        return processed

loader = LegalDataLoader()
