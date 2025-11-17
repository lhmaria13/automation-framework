"""
Utilitários para trabalhar com dados e conversões
"""

from typing import Any, List, Dict, Optional
import json
import csv
from pathlib import Path
from automation_framework.core.logger import Logger


class DataHelper:
    """
    Helper para operações com dados
    """

    @staticmethod
    def parse_json(json_str: str) -> Dict[str, Any]:
        """Faz parse de JSON"""
        try:
            return json.loads(json_str)
        except Exception as e:
            raise ValueError(f"JSON inválido: {str(e)}")

    @staticmethod
    def to_json(data: Any, pretty: bool = True) -> str:
        """Converte dados para JSON"""
        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def load_json_file(file_path: str) -> Dict[str, Any]:
        """Carrega JSON de arquivo"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_json_file(data: Any, file_path: str) -> None:
        """Salva dados como JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_csv_file(file_path: str, headers: bool = True) -> List[Dict[str, str]]:
        """Carrega dados de CSV"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            if headers:
                reader = csv.DictReader(f)
                data = list(reader)
            else:
                reader = csv.reader(f)
                data = list(reader)
        return data

    @staticmethod
    def save_csv_file(data: List[Dict[str, str]], file_path: str, headers: Optional[List[str]] = None) -> None:
        """Salva dados como CSV"""
        if not data:
            return

        if headers is None:
            headers = list(data[0].keys())

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def flatten_dict(data: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """Achata dicionário aninhado"""
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataHelper.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def compare_dictionaries(dict1: Dict, dict2: Dict) -> Dict[str, Any]:
        """Compara dois dicionários e retorna diferenças"""
        differences = {
            'only_in_first': {},
            'only_in_second': {},
            'different_values': {}
        }

        # Chaves apenas em dict1
        for key in dict1:
            if key not in dict2:
                differences['only_in_first'][key] = dict1[key]
            elif dict1[key] != dict2[key]:
                differences['different_values'][key] = {
                    'first': dict1[key],
                    'second': dict2[key]
                }

        # Chaves apenas em dict2
        for key in dict2:
            if key not in dict1:
                differences['only_in_second'][key] = dict2[key]

        return differences
