"""
Utilitários para trabalhar com waits e condições de espera
"""

from typing import Callable, Any, Optional
from time import sleep, time
from automation_framework.core.logger import Logger
from automation_framework.core.exceptions import TimeoutException


class Wait:
    """
    Classe para implementar waits inteligentes
    """

    def __init__(self, timeout: int = 10, poll_frequency: float = 0.5):
        self.timeout = timeout
        self.poll_frequency = poll_frequency
        self.logger = Logger.get_logger(self.__class__.__name__)

    def until(self, condition: Callable[[], bool], message: str = "Condição não atendida") -> bool:
        """
        Aguarda até que condição seja verdadeira

        Args:
            condition: Função que retorna bool
            message: Mensagem de erro

        Returns:
            True se condição atendida
        """
        start_time = time()

        while True:
            try:
                if condition():
                    elapsed = time() - start_time
                    self.logger.debug(f"Condição atendida em {elapsed:.2f}s")
                    return True
            except Exception as e:
                self.logger.debug(f"Erro na condição: {str(e)}")

            if time() - start_time > self.timeout:
                self.logger.error(f"Timeout: {message}")
                raise TimeoutException(f"Timeout (>{self.timeout}s): {message}")

            sleep(self.poll_frequency)

    def until_not(self, condition: Callable[[], bool], message: str = "Condição ainda é verdadeira") -> bool:
        """Aguarda até que condição seja falsa"""
        return self.until(lambda: not condition(), message)

    def until_value_changes(self, value_func: Callable[[], Any], timeout: Optional[int] = None) -> Any:
        """Aguarda até que valor mude"""
        timeout = timeout or self.timeout
        initial_value = value_func()

        def changed():
            return value_func() != initial_value

        self.until(changed, "Valor não mudou")
        return value_func()

    def until_value_equals(self, value_func: Callable[[], Any], expected_value: Any, timeout: Optional[int] = None) -> bool:
        """Aguarda até que valor seja igual a esperado"""
        timeout = timeout or self.timeout
        old_timeout = self.timeout
        self.timeout = timeout

        try:
            self.until(lambda: value_func() == expected_value, f"Valor não é igual a {expected_value}")
            return True
        finally:
            self.timeout = old_timeout

    def until_no_exception(self, func: Callable[[], Any], timeout: Optional[int] = None) -> Any:
        """Aguarda até que função não lance exceção"""
        timeout = timeout or self.timeout
        old_timeout = self.timeout
        self.timeout = timeout

        try:
            result = None

            def execute():
                nonlocal result
                result = func()
                return True

            self.until(execute, "Função continua lançando exceção")
            return result
        finally:
            self.timeout = old_timeout


class Retry:
    """
    Implementa padrão Retry com backoff exponencial
    """

    def __init__(self, max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff = backoff
        self.logger = Logger.get_logger(self.__class__.__name__)

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Executa função com retry

        Args:
            func: Função a executar
            *args: Argumentos
            **kwargs: Keyword arguments

        Returns:
            Resultado da função
        """
        last_exception = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                result = func(*args, **kwargs)
                if attempt > 1:
                    self.logger.info(f"Sucesso na tentativa {attempt}")
                return result
            except Exception as e:
                last_exception = e
                if attempt < self.max_attempts:
                    wait_time = self.delay * (self.backoff ** (attempt - 1))
                    self.logger.warning(
                        f"Tentativa {attempt} falhou. Aguardando {wait_time:.1f}s antes de tentar novamente"
                    )
                    sleep(wait_time)
                else:
                    self.logger.error(f"Todas as {self.max_attempts} tentativas falharam")

        raise last_exception


def wait_for(condition: Callable[[], bool], timeout: int = 10, message: str = "Timeout") -> None:
    """
    Função helper para esperar condição simples

    Args:
        condition: Função que retorna bool
        timeout: Timeout em segundos
        message: Mensagem de erro
    """
    waiter = Wait(timeout=timeout)
    waiter.until(condition, message)


def retry(func: Callable, max_attempts: int = 3, delay: float = 1.0) -> Any:
    """
    Função helper para executar com retry

    Args:
        func: Função a executar
        max_attempts: Máximo de tentativas
        delay: Delay entre tentativas

    Returns:
        Resultado da função
    """
    retrier = Retry(max_attempts=max_attempts, delay=delay)
    return retrier.execute(func)
