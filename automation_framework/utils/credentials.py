"""
Utilitários para gerenciamento de credenciais e dados sensíveis
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from automation_framework.core.logger import Logger


class CredentialManager:
    """
    Gerenciador seguro de credenciais
    Suporta variáveis de ambiente e arquivo de configuração
    """

    def __init__(self, config_file: Optional[str] = None):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.config_file = config_file
        self._credentials: Dict[str, Any] = {}

        if config_file and Path(config_file).exists():
            self._load_from_file(config_file)

    def _load_from_file(self, file_path: str) -> None:
        """Carrega credenciais de arquivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self._credentials = json.load(f)
            self.logger.info("Credenciais carregadas do arquivo")
        except Exception as e:
            self.logger.error(f"Erro ao carregar credenciais: {str(e)}")

    def get_credential(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Obtém credencial por chave

        Prioridade:
        1. Variável de ambiente (chave em maiúscula)
        2. Arquivo de configuração
        3. Valor padrão

        Args:
            key: Chave da credencial
            default: Valor padrão

        Returns:
            Valor da credencial
        """
        # Tenta variável de ambiente
        env_value = os.environ.get(key.upper())
        if env_value:
            return env_value

        # Tenta arquivo de configuração
        file_value = self._credentials.get(key)
        if file_value:
            return file_value

        return default

    def get_credentials(self, prefix: str) -> Dict[str, str]:
        """
        Obtém múltiplas credenciais com prefixo

        Args:
            prefix: Prefixo das credenciais

        Returns:
            Dicionário com credenciais
        """
        credentials = {}

        for key, value in self._credentials.items():
            if key.startswith(prefix):
                credentials[key] = value

        for env_key, env_value in os.environ.items():
            if env_key.startswith(prefix.upper()):
                key = env_key.lower()
                credentials[key] = env_value

        return credentials

    def set_credential(self, key: str, value: str) -> None:
        """Define credencial"""
        self._credentials[key] = value
        self.logger.debug(f"Credencial '{key}' definida")

    def save_credentials(self, file_path: str) -> None:
        """Salva credenciais em arquivo"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._credentials, f, indent=2)
            self.logger.info(f"Credenciais salvas em {file_path}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar credenciais: {str(e)}")
