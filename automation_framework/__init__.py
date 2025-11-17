"""
Automation Framework - Framework padrão para automações em Python
Versão: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Automation Team"

from automation_framework.core.logger import Logger
from automation_framework.web.driver_manager import DriverManager
from automation_framework.core.config import ConfigManager

__all__ = [
    'Logger',
    'DriverManager',
    'ConfigManager',
]
