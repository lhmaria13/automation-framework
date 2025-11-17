"""
Gerenciador centralizado de configurações
Suporta carregamento de múltiplas fontes (JSON, YAML, ENV)
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class BrowserConfig:
    """Configuração do navegador"""
    browser_type: str = "chrome"  # chrome, firefox, edge, safari
    headless: bool = False
    implicit_wait: int = 10
    page_load_timeout: int = 30
    window_size: str = "1920,1080"
    proxy: Optional[str] = None
    user_data_dir: Optional[str] = None


@dataclass
class LogConfig:
    """Configuração de logging"""
    level: str = "INFO"
    log_dir: str = "logs"
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5


@dataclass
class DesktopConfig:
    """Configuração para automação de desktop"""
    timeout: int = 10
    pause_between_actions: float = 0.5
    screenshot_on_error: bool = True


@dataclass
class ConsoleConfig:
    """Configuração para automação de console"""
    timeout: int = 30
    encoding: str = "utf-8"
    capture_output: bool = True


class ConfigManager:
    """
    Gerenciador centralizado de configurações
    Implementa padrão Singleton
    """

    _instance: Optional['ConfigManager'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._load_default_config()

    def _load_default_config(self):
        """Carrega configurações padrão"""
        self._config = {
            'browser': asdict(BrowserConfig()),
            'logging': asdict(LogConfig()),
            'desktop': asdict(DesktopConfig()),
            'console': asdict(ConsoleConfig()),
        }

    def load_from_json(self, file_path: str) -> None:
        """
        Carrega configurações de arquivo JSON

        Args:
            file_path: Caminho do arquivo JSON
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self._config.update(config)

    def load_from_env(self, prefix: str = "AUTO_") -> None:
        """
        Carrega configurações de variáveis de ambiente

        Args:
            prefix: Prefixo das variáveis de ambiente
        """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                self._config[config_key] = self._parse_env_value(value)

    @staticmethod
    def _parse_env_value(value: str) -> Any:
        """Converte string de ambiente para tipo apropriado"""
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração

        Args:
            key: Chave (suporta notação de ponto: 'browser.headless')
            default: Valor padrão se a chave não existir

        Returns:
            Valor configurado ou padrão
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """
        Define valor de configuração

        Args:
            key: Chave (suporta notação de ponto)
            value: Novo valor
        """
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_browser_config(self) -> BrowserConfig:
        """Retorna objeto de configuração do navegador"""
        return BrowserConfig(**self._config.get('browser', {}))

    def get_log_config(self) -> LogConfig:
        """Retorna objeto de configuração de logging"""
        return LogConfig(**self._config.get('logging', {}))

    def get_desktop_config(self) -> DesktopConfig:
        """Retorna objeto de configuração de desktop"""
        return DesktopConfig(**self._config.get('desktop', {}))

    def get_console_config(self) -> ConsoleConfig:
        """Retorna objeto de configuração de console"""
        return ConsoleConfig(**self._config.get('console', {}))

    def to_dict(self) -> Dict[str, Any]:
        """Retorna todas as configurações como dicionário"""
        return self._config.copy()

    def to_json(self, file_path: str) -> None:
        """
        Exporta configurações para arquivo JSON

        Args:
            file_path: Caminho do arquivo JSON de destino
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)
