"""
Exemplo 4: Uso de Utilities - Wait, Retry, Credenciais, Dados
"""

import sys
from pathlib import Path

# Garantir que a raiz do projeto esteja no sys.path para permitir execução
# a partir da pasta `automation_framework/` ou de qualquer outra
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from automation_framework.utils.wait import Wait, Retry, wait_for, retry
from automation_framework.utils.credentials import CredentialManager
from automation_framework.utils.data import DataHelper
from automation_framework.core.logger import Logger
import time


def main():
    logger = Logger.get_logger(__name__)
    logger.info("Iniciando exemplo de utilities")

    # Exemplo 1: Wait
    logger.info("--- Exemplo 1: Wait ---")
    counter = {'value': 0}

    def increment_counter():
        counter['value'] += 1
        return counter['value'] >= 3

    waiter = Wait(timeout=5, poll_frequency=0.5)
    try:
        waiter.until(increment_counter, "Contador não atingiu 3")
        logger.info(f"Contador atingiu: {counter['value']}")
    except Exception as e:
        logger.error(str(e))

    # Exemplo 2: Retry
    logger.info("--- Exemplo 2: Retry ---")
    attempt_count = {'value': 0}

    def unstable_function():
        attempt_count['value'] += 1
        if attempt_count['value'] < 2:
            raise Exception(f"Erro na tentativa {attempt_count['value']}")
        return "Sucesso!"

    retrier = Retry(max_attempts=3, delay=0.5)
    result = retrier.execute(unstable_function)
    logger.info(f"Resultado: {result}")

    # Exemplo 3: Credenciais
    logger.info("--- Exemplo 3: Credenciais ---")
    cred_manager = CredentialManager()

    # Simular credenciais
    cred_manager.set_credential("usuario", "admin")
    cred_manager.set_credential("senha", "senha123")

    usuario = cred_manager.get_credential("usuario", "padrão")
    logger.info(f"Usuário: {usuario}")

    # Salvar para posterior uso
    cred_manager.save_credentials("credenciais.json")
    logger.info("Credenciais salvas")

    # Exemplo 4: Data Helper
    logger.info("--- Exemplo 4: Data Helper ---")

    # Trabalhar com JSON
    data = {"nome": "Framework", "tipo": "Automação", "versao": 1.0}
    json_str = DataHelper.to_json(data)
    logger.info(f"JSON: {json_str}")

    # Carregar de JSON
    parsed = DataHelper.parse_json(json_str)
    logger.info(f"Parseado: {parsed}")

    # Achatar dicionário
    nested = {"config": {"database": {"host": "localhost", "port": 5432}}}
    flattened = DataHelper.flatten_dict(nested)
    logger.info(f"Achatado: {flattened}")

    # Comparar dicionários
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 20, "d": 4}
    differences = DataHelper.compare_dictionaries(dict1, dict2)
    logger.info(f"Diferenças: {differences}")


if __name__ == "__main__":
    main()
