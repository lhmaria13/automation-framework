"""
Teste unitário básico do framework
Valida funcionalidades principais
"""

import pytest
import sys
from pathlib import Path

# Adicionar raiz do projeto ao path (não apenas a pasta automation_framework)
# Path(__file__).parent.parent.parent = C:\...\COPA\Framework\automation_framework\tests\.. = Framework/
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from automation_framework.core.config import ConfigManager
from automation_framework.core.logger import Logger
from automation_framework.utils.wait import Wait, Retry
from automation_framework.utils.data import DataHelper
from automation_framework.utils.credentials import CredentialManager


class TestConfig:
    def test_singleton(self):
        """ConfigManager deve ser singleton"""
        config1 = ConfigManager()
        config2 = ConfigManager()
        assert config1 is config2

    def test_get_set_config(self):
        """Deve armazenar e recuperar configurações"""
        config = ConfigManager()
        config.set('test.key', 'value')
        assert config.get('test.key') == 'value'

    def test_default_config(self):
        """Deve ter configurações padrão"""
        config = ConfigManager()
        assert config.get('browser.browser_type') == 'chrome'
        assert config.get('browser.implicit_wait') == 10


class TestLogger:
    def test_logger_creation(self):
        """Logger deve ser criado com sucesso"""
        logger = Logger.get_logger('test_logger')
        assert logger is not None
        assert logger.name == 'test_logger'

    def test_logger_singleton(self):
        """Logger com mesmo nome deve ser singleton"""
        logger1 = Logger.get_logger('test')
        logger2 = Logger.get_logger('test')
        assert logger1 is logger2


class TestWait:
    def test_wait_condition_true(self):
        """Wait deve passar quando condição é true"""
        counter = {'value': 0}

        def increment():
            counter['value'] += 1
            return counter['value'] >= 2

        waiter = Wait(timeout=5)
        result = waiter.until(increment, "Contador não atingiu 2")
        assert result is True

    def test_wait_timeout(self):
        """Wait deve lançar TimeoutException"""
        from automation_framework.core.exceptions import TimeoutException

        waiter = Wait(timeout=1)
        with pytest.raises(TimeoutException):
            waiter.until(lambda: False, "Deve falhar")


class TestRetry:
    def test_retry_success(self):
        """Retry deve funcionar na primeira tentativa"""
        def simple_func():
            return "sucesso"

        retrier = Retry(max_attempts=3)
        result = retrier.execute(simple_func)
        assert result == "sucesso"

    def test_retry_after_failures(self):
        """Retry deve tentar novamente após falhas"""
        attempts = {'count': 0}

        def unstable_func():
            attempts['count'] += 1
            if attempts['count'] < 2:
                raise ValueError("Tentativa falhou")
            return "sucesso"

        retrier = Retry(max_attempts=3, delay=0.1)
        result = retrier.execute(unstable_func)
        assert result == "sucesso"
        assert attempts['count'] == 2


class TestDataHelper:
    def test_json_parse(self):
        """Deve fazer parse de JSON"""
        json_str = '{"nome": "teste", "valor": 123}'
        result = DataHelper.parse_json(json_str)
        assert result['nome'] == "teste"
        assert result['valor'] == 123

    def test_json_to_string(self):
        """Deve converter para JSON"""
        data = {"nome": "teste"}
        result = DataHelper.to_json(data, pretty=False)
        assert '"nome"' in result
        assert '"teste"' in result

    def test_flatten_dict(self):
        """Deve achatar dicionário aninhado"""
        nested = {"config": {"database": {"host": "localhost"}}}
        flattened = DataHelper.flatten_dict(nested)
        assert flattened['config.database.host'] == "localhost"

    def test_compare_dictionaries(self):
        """Deve comparar dicionários corretamente"""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"a": 1, "b": 20, "c": 3}
        diff = DataHelper.compare_dictionaries(dict1, dict2)

        assert 'b' in diff['different_values']
        assert 'c' in diff['only_in_second']


class TestCredentials:
    def test_set_get_credential(self):
        """Deve armazenar e recuperar credenciais"""
        cred = CredentialManager()
        cred.set_credential('user', 'admin')
        assert cred.get_credential('user') == 'admin'

    def test_default_credential(self):
        """Deve retornar padrão se não encontrar"""
        cred = CredentialManager()
        result = cred.get_credential('nao_existe', 'padrao')
        assert result == 'padrao'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
