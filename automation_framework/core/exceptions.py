"""
Exceções personalizadas do framework
"""


class AutomationFrameworkException(Exception):
    """Exceção base do framework"""
    pass


class BrowserException(AutomationFrameworkException):
    """Exceção relacionada a navegadores"""
    pass


class ElementNotFound(AutomationFrameworkException):
    """Elemento não encontrado"""
    pass


class TimeoutException(AutomationFrameworkException):
    """Timeout ao aguardar elemento ou ação"""
    pass


class InvalidBrowserType(AutomationFrameworkException):
    """Tipo de navegador inválido"""
    pass


class DesktopAutomationException(AutomationFrameworkException):
    """Exceção relacionada a automação de desktop"""
    pass


class ConsoleAutomationException(AutomationFrameworkException):
    """Exceção relacionada a automação de console"""
    pass


class ConfigurationException(AutomationFrameworkException):
    """Exceção de configuração"""
    pass
