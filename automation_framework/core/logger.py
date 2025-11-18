"""
Logger centralizado para todas as automações
Implementa logging estruturado com níveis configuráveis
"""

import logging
import sys
import io
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    """
    Gerenciador centralizado de logging para o framework
    Suporta múltiplos níveis e saída em console e arquivo
    """

    _instance: Optional['Logger'] = None
    _loggers: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)

    @staticmethod
    def get_logger(name: str, level: str = "INFO") -> logging.Logger:
        """
        Obtém ou cria um logger com configurações padronizadas

        Args:
            name: Nome do logger (geralmente __name__)
            level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Returns:
            logging.Logger: Logger configurado
        """
        if name in Logger._loggers:
            return Logger._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))

        # Evita handlers duplicados
        if logger.handlers:
            return logger

        # Handler para console: garantir que a saída use UTF-8 e não quebre
        try:
            # Re-encapsula stdout com encoding UTF-8 e errors='replace'
            wrapped_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
            console_handler = logging.StreamHandler(wrapped_stdout)
        except Exception:
            # Fallback: usar stdout original
            console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))

        # Handler para arquivo com rotação
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        log_file = logs_dir / f"{name.replace('.', '_')}.log"

        # Handler para arquivo com rotação (usar UTF-8)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level.upper()))

        # Formato padronizado
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        Logger._loggers[name] = logger
        return logger

    @staticmethod
    def get_test_logger(test_name: str) -> logging.Logger:
        """Retorna logger específico para testes"""
        return Logger.get_logger(f"tests.{test_name}", level="DEBUG")

    @staticmethod
    def clear_logs():
        """Limpa todos os logs anteriores"""
        logs_dir = Path("logs")
        if logs_dir.exists():
            for log_file in logs_dir.glob("*.log"):
                log_file.unlink()
